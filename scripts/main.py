"""
main.py — TikTok Seller University (BR) 知识库镜像工具（核心同步逻辑）
=======================================================================
功能：
  1. 遍历三个 Tab（Cursos / Feature Guide / Policy Center）的分类树
  2. 分页拉取每个分类下的全部文章列表
  3. 与 sync_state.json 比对：新增 / 需更新 / 跳过
  4. 对"新增"和"需更新"的文章，抓取 essay 页面、解析 SSR 数据
  5. HTML → Markdown 转换，注入 YAML frontmatter，写入 docs/ 目录
  6. 更新 sync_state.json

增量同步原理：
  - sync_state.json 记录每篇文章的 last_modified（Unix 毫秒时间戳）
  - 列表接口返回的 modify_time 大于记录 → 更新
  - article_id 不在记录中 → 新增
  - 否则 → 跳过（不请求详情接口，保护 API）

运行：python main.py
"""

import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# ---------------------------------------------------------------------------
# 全局配置
# ---------------------------------------------------------------------------

BASE_URL = "https://seller-br.tiktok.com"
API_BASE = f"{BASE_URL}/api/v1/seller/learning_center"

# 三个 Tab 的 category 参数
TABS = [
    {"name": "cursos",        "category": 4, "role_type": 1},
    {"name": "cursos",        "category": 4, "role_type": 2},  # Creator
    {"name": "feature-guide", "category": 3, "role_type": 1},
    {"name": "feature-guide", "category": 3, "role_type": 2},  # Creator
    {"name": "policy-center", "category": 2, "role_type": 1},
    {"name": "policy-center", "category": 2, "role_type": 2},  # Creator
]

COMMON_PARAMS = {
    "locale": "pt-BR",
    "language": "pt",
    "region": "BR",
    "aid": "4068",
    "app_name": "i18n_ecom_shop",
    "device_id": "0",
    "fp": "verify_mrbv8xzd_axlMHYjO_1SbR_46Ju_81zu_a26hKArDkU7E",
    "device_platform": "web",
    "cookie_enabled": "true",
    "screen_width": "3008",
    "screen_height": "1269",
    "browser_language": "en-US",
    "browser_platform": "MacIntel",
    "browser_name": "Mozilla",
    "browser_version": "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "browser_online": "true",
    "timezone_name": "Asia/Shanghai",
    "msToken": "",
    "X-Bogus": "",
    "_signature": "",
}

HEADERS = {
    "User-Agent": COMMON_PARAMS["browser_version"],
    "Referer": f"{BASE_URL}/university/home?identity=1",
    "Accept": "application/json, text/plain, */*",
    # ⚠️ 不要设置 Accept-Language，否则 essay 返回英文
}

# 限流：每个请求之间的最小间隔（秒）
RATE_LIMIT_SLEEP = 1.0
# 文章详情请求间隔（稍大，因为详情请求更重）
DETAIL_SLEEP = 1.5

# 输出目录（仓库根目录，不随脚本位置变化）
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_DIR, "docs")
STATE_FILE = os.path.join(REPO_DIR, "sync_state.json")

# requests 会话
session = requests.Session()
session.headers.update(HEADERS)


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def http_get(path, params=None, retries=3):
    """带重试的 GET 请求。返回 parsed JSON，失败返回 None。"""
    url = urljoin(BASE_URL, path) if path.startswith("/") else path
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, params=params, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as e:
            print(f"    ⚠️  第 {attempt}/{retries} 次请求失败: {e}")
            time.sleep(1)
    return None


def init_session():
    """初始化 session：访问 home 页触发服务器端语言偏好（pt-BR）。"""
    print("📌 初始化 session（访问 home 页设置语言偏好）...")
    try:
        resp = session.get(f"{BASE_URL}/university/home",
                           params={"identity": 1}, timeout=15)
        resp.raise_for_status()
        print(f"  ✓ home 页加载成功 (status={resp.status_code})")
    except requests.RequestException as e:
        print(f"  ⚠️ home 页加载失败: {e}")
    time.sleep(0.5)


def load_state():
    """加载 sync_state.json。"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    """保存 sync_state.json。"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def slugify(text):
    """把任意文本转成安全的目录/文件名（保留葡语重音字符）。

    规则：
    - 转小写
    - 保留字母、数字、空格、连字符、下划线、重音字符
    - 其他字符替换为连字符
    - 多个连字符合并，去掉首尾连字符
    """
    text = text.strip().lower()
    # 保留 Unicode 字母/数字（含葡语重音）
    text = unicodedata.normalize("NFC", text)
    # 替换空格和斜杠为连字符
    text = re.sub(r"[\s/]+", "-", text)
    # 去掉不允许的字符（保留字母、数字、连字符、下划线、重音）
    text = re.sub(r"[^\w\-À-ÿ]", "", text, flags=re.UNICODE)
    # 合并多个连字符
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def clean_html_to_markdown(html):
    """把 essay 页面的 HTML 内容转为干净的 Markdown。

    处理步骤：
    1. 去掉 <div class="space"> 等冗余分隔符
    2. 去掉外层 <div class="converted-html">
    3. 提取 <video> 元数据，替换为显式链接段落
    4. markdownify 转换（heading_style='ATX' 用 # 标题）
    5. 清理多余空行

    返回 (markdown_text, videos_list)
    """
    soup = BeautifulSoup(html, "html.parser")
    # 去掉冗余分隔 div
    for d in soup.find_all("div", class_="space"):
        d.decompose()
    # 去掉 <script>/<style>
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    videos = []
    # 处理 <video> 标签：提取元数据，替换为显式链接段落
    for vid in soup.find_all("video"):
        source = vid.find("source")
        video_url = ""
        if source and source.get("src"):
            video_url = source["src"]
        elif vid.get("src"):
            video_url = vid["src"]
        poster_url = vid.get("poster", "")
        if video_url:
            videos.append({"url": video_url, "cover": poster_url})
        # 替换为显式链接段落
        link_text = f"🎬 [视频]({video_url})" if video_url else ""
        new_p = soup.new_tag("p")
        new_p.string = link_text
        vid.replace_with(new_p)

    # 解包外层 wrapper
    wrapper = soup.find("div", class_="converted-html")
    inner = wrapper.decode_contents() if wrapper else str(soup)
    # 转换
    markdown = md(inner, heading_style="ATX", strip=["script", "style"])
    # 清理多余空行（>2 个连续空行 → 2 个）
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip(), videos


def extract_router_data(html):
    """从 essay 页面 HTML 中抽取 window._ROUTER_DATA 的 JSON 对象。"""
    marker = "window._ROUTER_DATA"
    idx = html.find(marker)
    if idx == -1:
        return None
    start = html.find("{", idx)
    if start == -1:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(html, start)
        return obj
    except json.JSONDecodeError:
        return None


def unix_ms_to_iso(unix_ms):
    """Unix 毫秒时间戳 → ISO 8601 日期字符串（UTC）。"""
    if not unix_ms:
        return ""
    dt = datetime.fromtimestamp(unix_ms / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# 分类树遍历
# ---------------------------------------------------------------------------

def fetch_category_tree(category, role_type):
    """请求一个 Tab 的分类树。

    返回 list of dict，每个 dict 代表一个"叶子分类"：
      {
        "content_id": int,
        "content_name": str,
        "path": [一级分类名, 可选的二级分类名],  # 用于构建文件路径
      }
    """
    params = {
        **COMMON_PARAMS,
        "category": category,
        "role_type": role_type,
        "only_directory": "true",
        "list_contents_number": 3,
        "list_contents_limit": 50,  # 足够大以覆盖所有分类
    }
    data = http_get("/api/v1/seller/learning_center/contents/get", params=params)
    if not data or data.get("code") != 0:
        return []

    result = data["data"]["contents"]
    sub_contents = result.get("sub_contents", [])
    leaves = []

    for sub in sub_contents:
        sub_id = sub["content_id"]
        sub_name = sub["content_name"]
        # Feature Guide 有二级嵌套
        sub_sub = sub.get("sub_contents")
        if sub_sub:
            for leaf in sub_sub:
                leaves.append({
                    "content_id": leaf["content_id"],
                    "content_name": leaf["content_name"],
                    "path": [sub_name, leaf["content_name"]],
                })
        else:
            leaves.append({
                "content_id": sub_id,
                "content_name": sub_name,
                "path": [sub_name],
            })

    return leaves


# ---------------------------------------------------------------------------
# 文章列表（分页）
# ---------------------------------------------------------------------------

def fetch_all_articles(content_id, limit=50):
    """分页拉取某个分类下的全部文章。

    返回 list of article summary:
      {
        "learning_id": int,
        "name": str,
        "description": str,
        "modify_time": int (unix ms),
        "views": int,
        "tags": [str, ...],
      }
    """
    articles = []
    page = 1
    while True:
        params = {
            **COMMON_PARAMS,
            "content_id": content_id,
            "page": page,
            "limit": limit,
        }
        data = http_get("/api/v1/seller/learning_center/contents/list", params=params)
        if not data or data.get("code") != 0:
            break

        result = data["data"]
        items = result.get("learning_info", [])
        total = result.get("total", 0)
        articles.extend(items)

        # 判断是否还有下一页
        if len(articles) >= total or not items:
            break
        page += 1
        time.sleep(RATE_LIMIT_SLEEP)

    return articles


# ---------------------------------------------------------------------------
# 文章详情
# ---------------------------------------------------------------------------

def fetch_article_detail(knowledge_id, role_type=1):
    """访问 essay 页面，解析详情。

    返回 dict:
      {
        "knowledge_id": int,
        "knowledge_name": str,
        "keywords": str,
        "html_content": str,    # 用于转 Markdown
        "plain_content": str,   # 纯文本摘要
      }
    失败返回 None。
    """
    url = f"{BASE_URL}/university/essay"
    params = {
        "identity": 1,
        "role": role_type,
        "knowledge_id": knowledge_id,
        "from": "course",
    }
    for attempt in range(1, 4):
        try:
            resp = session.get(url, params=params, timeout=20)
            resp.raise_for_status()
            html = resp.text
            break
        except requests.RequestException as e:
            print(f"      ⚠️  第 {attempt}/3 次请求失败: {e}")
            time.sleep(1)
    else:
        return None

    router_data = extract_router_data(html)
    if not router_data:
        return None

    page_data = router_data.get("loaderData", {}).get("essay/page", {})
    detail = page_data.get("knowledge_detail", {})
    if not detail:
        return None

    return {
        "knowledge_id": detail.get("knowledge_id"),
        "knowledge_name": detail.get("knowledge_name"),
        "keywords": detail.get("keywords", ""),
        "html_content": page_data.get("knowledge_content", ""),
        "plain_content": detail.get("knowledge_plain_content", ""),
    }


# ---------------------------------------------------------------------------
# 文件写入
# ---------------------------------------------------------------------------

def write_article_md(article_meta, content_body, category_path, tab_name):
    """把文章写入 docs/<tab>/<category_path>/<title>_<id>.md

    返回写入的相对路径，失败返回 None。
    """
    # 构建目录：docs/<tab>/<一级分类>/[可选二级分类]
    safe_tab = slugify(tab_name)
    safe_parts = [slugify(p) for p in category_path]
    dir_path = os.path.join(DOCS_DIR, safe_tab, *safe_parts)
    os.makedirs(dir_path, exist_ok=True)

    # 文件名：标题_ID.md
    safe_title = slugify(article_meta["knowledge_name"])
    # 文件名不要太长
    if len(safe_title) > 80:
        safe_title = safe_title[:80]
    filename = f"{safe_title}_{article_meta['knowledge_id']}.md"
    filepath = os.path.join(dir_path, filename)

    # YAML frontmatter（Rspress 兼容：只保留基础字段，URL 用引号包裹）
    frontmatter = {
        "title": article_meta["knowledge_name"],
        "id": article_meta["knowledge_id"],
        "category": category_path[-1] if category_path else "",
        "url": f"{BASE_URL}/university/essay?knowledge_id={article_meta['knowledge_id']}",
        "update_time": unix_ms_to_iso(article_meta.get("modify_time", 0)),
        "keywords": article_meta.get("keywords", ""),
    }

    # 视频信息：放在正文里（避免 Rspress YAML 解析特殊字符崩溃）
    videos = article_meta.get("videos", [])
    video_section = ""
    if videos:
        video_section = "\n\n## 视频\n\n"
        for i, v in enumerate(videos, 1):
            video_section += f"![视频 {i} 封面]({v['cover']})\n\n"
            video_section += f"[🎬 视频 {i}]({v['url']})\n\n"

    # 组装 Markdown
    yaml_lines = ["---"]
    for k, v in frontmatter.items():
        if isinstance(v, str):
            v = v.replace('"', '\\"')
            yaml_lines.append(f'{k}: "{v}"')
        elif isinstance(v, list):
            # YAML 列表格式
            yaml_lines.append(f"{k}:")
            for item in v:
                item_str = str(item).replace('"', '\\"')
                yaml_lines.append(f'  - "{item_str}"')
        else:
            yaml_lines.append(f"{k}: {v}")
    yaml_lines.append("---")
    yaml_lines.append("")

    md_content = "\n".join(yaml_lines) + content_body + video_section + "\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 返回相对路径（用于日志）
    return os.path.relpath(filepath, os.path.dirname(DOCS_DIR))


# ---------------------------------------------------------------------------
# 主同步流程
# ---------------------------------------------------------------------------

def sync_tab(tab_config):
    """同步一个 Tab 的全部文章。

    返回 (新增数, 更新数, 跳过数, 失败数)。
    """
    tab_name = tab_config["name"]
    category = tab_config["category"]
    role_type = tab_config["role_type"]
    role_label = "creator" if role_type == 2 else "seller"

    print(f"\n{'='*60}")
    print(f"📂 Tab: {tab_name} / {role_label}  (category={category})")
    print(f"{'='*60}")

    # 1. 拉分类树
    leaves = fetch_category_tree(category, role_type)
    print(f"  找到 {len(leaves)} 个叶子分类")
    if not leaves:
        print("  ❌ 未获取到分类树，本次同步视为失败")
        return 0, 0, 0, 1

    # 2. 遍历每个叶子分类
    added = updated = skipped = failed = 0
    for leaf in leaves:
        content_id = leaf["content_id"]
        path = leaf["path"]
        print(f"\n  📁 {' / '.join(path)} (id={content_id})")

        # 拉文章列表
        articles = fetch_all_articles(content_id)
        print(f"     共 {len(articles)} 篇文章")
        time.sleep(RATE_LIMIT_SLEEP)

        # 3. 逐篇比对状态
        for art in articles:
            art_id = str(art["learning_id"])
            modify_time = art.get("modify_time", 0)
            title = art["name"]

            state = load_state()
            existing = state.get(art_id)

            if existing is None:
                action = "🆕 新增"
            elif modify_time > existing.get("last_modified", 0):
                action = "🔄 更新"
            else:
                # 跳过
                skipped += 1
                continue

            print(f"     {action} [{art_id}] {title}")

            # 拉详情
            detail = fetch_article_detail(art["learning_id"], role_type)
            time.sleep(DETAIL_SLEEP)

            if not detail:
                print(f"        ❌ 详情获取失败")
                failed += 1
                continue

            # HTML → Markdown（返回 markdown 文本 + 视频列表）
            md_body, videos = clean_html_to_markdown(detail["html_content"])

            # 写入文件
            meta = {
                "knowledge_id": detail["knowledge_id"],
                "knowledge_name": detail["knowledge_name"],
                "keywords": detail.get("keywords", ""),
                "modify_time": modify_time,
                "videos": videos,  # ← 新增：视频结构化数据
            }
            rel_path = write_article_md(meta, md_body, path, tab_name)
            if rel_path:
                print(f"        ✓ 写入: {rel_path}")
                # 更新状态
                state[art_id] = {
                    "title": detail["knowledge_name"],
                    "last_modified": modify_time,
                    "file": rel_path,
                }
                save_state(state)
                if existing is None:
                    added += 1
                else:
                    updated += 1
            else:
                failed += 1

    return added, updated, skipped, failed


def main():
    print("🚀 TikTok Seller University (BR) 知识库镜像同步")
    print(f"   目标站点: {BASE_URL}")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   输出目录: {DOCS_DIR}")

    # 初始化 session
    init_session()

    # 加载现有状态
    state = load_state()
    print(f"  📊 当前已同步文章数: {len(state)}")

    # 同步三个 Tab（Seller + Creator）
    total_added = total_updated = total_skipped = total_failed = 0
    for tab in TABS:
        added, updated, skipped, failed = sync_tab(tab)
        total_added += added
        total_updated += updated
        total_skipped += skipped
        total_failed += failed

    # 汇总
    print(f"\n{'='*60}")
    print(f"✅ 同步完成")
    print(f"   新增: {total_added}")
    print(f"   更新: {total_updated}")
    print(f"   跳过: {total_skipped}")
    print(f"   失败: {total_failed}")
    print(f"   总计已同步: {len(load_state())}")
    print(f"{'='*60}")

    if total_failed > 0:
        print("❌ 存在同步失败项，退出码设为 1，避免 CI 提交半残数据。")
        sys.exit(1)


if __name__ == "__main__":
    main()
