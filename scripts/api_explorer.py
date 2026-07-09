"""
api_explorer.py — TikTok Seller University (BR) API 探路脚本
============================================================
用途：在本地测试三个 Tab 的分类接口、文章列表接口、文章详情 SSR 解析。
      验证请求参数、鉴权需求、JSON 结构，确认后续 main.py 该怎么写。

前置：pip install requests beautifulsoup4 markdownify
运行：python api_explorer.py

作者：AI assistant
日期：2026-07-08
"""

import json
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# 全局配置
# ---------------------------------------------------------------------------

BASE_URL = "https://seller-br.tiktok.com"
API_BASE = f"{BASE_URL}/api/v1/seller/learning_center"

# 三个 Tab 对应的 category 参数（已实地验证）
TABS = {
    "Cursos":          {"category": 4, "role_type": 1},  # Seller
    "Cursos_Creator":  {"category": 4, "role_type": 2},  # Creator
    "Feature_Guide":   {"category": 3, "role_type": 1},
    "Feature_Guide_C": {"category": 3, "role_type": 2},
    "Policy_Center":   {"category": 2, "role_type": 1},
    "Policy_Center_C": {"category": 2, "role_type": 2},
}

# 通用查询参数（从浏览器抓包中提炼，去掉动态 token 也能工作）
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
    # 下面的可为空（已验证）
    "msToken": "",
    "X-Bogus": "",
    "_signature": "",
}

HEADERS = {
    "User-Agent": COMMON_PARAMS["browser_version"],
    "Referer": f"{BASE_URL}/university/home?identity=1",
    "Accept": "application/json, text/plain, */*",
    # ⚠️ 不要设置 Accept-Language: en-US，否则 essay 页面会返回英文
    # 让服务器按站点默认语言（pt-BR）返回
}

# requests 会话（复用连接、统一 headers）
session = requests.Session()
session.headers.update(HEADERS)


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def http_get(path, params=None, retries=3, sleep=1):
    """带重试的 GET 请求。返回 parsed JSON，失败返回 None。"""
    # path 已经是完整路径（含 /api/v1/...），直接用 urljoin 拼 BASE_URL
    url = urljoin(BASE_URL, path)
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as e:
            print(f"  ⚠️  第 {attempt}/{retries} 次请求失败: {e}")
            time.sleep(sleep)
    return None


def extract_router_data(html):
    """从 essay 页面 HTML 中抽取 window._ROUTER_DATA 的 JSON 对象。

    数据内嵌在一个 <script> 标签里，形如：
        window._ROUTER_DATA = {...};
    由于 JSON 嵌套层级很深，不能用简单的正则贪婪匹配，
    改用 json.JSONDecoder().raw_decode 从等号后第一个 { 开始解析出完整的 JSON 对象。
    """
    marker = "window._ROUTER_DATA"
    idx = html.find(marker)
    if idx == -1:
        return None
    # 找到等号后的第一个 {
    start = html.find("{", idx)
    if start == -1:
        return None
    try:
        # raw_decode 返回 (obj, end_index)，自动处理嵌套大括号
        obj, _ = json.JSONDecoder().raw_decode(html, start)
        return obj
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# 1. 分类树接口（contents/get）
# ---------------------------------------------------------------------------

def explore_category(tab_name, category, role_type, limit=12):
    """请求一个 Tab 的分类树，并打印结构摘要。

    返回值中的关键字段：
      - data.contents.root_content_id / root_content_name
      - data.contents.sub_contents  ← 一级分类列表
      - data.content_id_to_info[id].total  ← 该分类下文章总数
      - data.content_id_to_info[id].learning_info  ← 文章预览列表
    """
    print(f"\n{'='*60}")
    print(f"📂 Tab: {tab_name}  (category={category}, role_type={role_type})")
    print(f"{'='*60}")

    params = {
        **COMMON_PARAMS,
        "category": category,
        "role_type": role_type,
        "only_directory": "true",
        "list_contents_number": 3,
        "list_contents_limit": limit,
    }
    data = http_get("/api/v1/seller/learning_center/contents/get", params=params)
    if not data:
        print("  ❌ 请求失败")
        return None

    if data.get("code") != 0:
        print(f"  ❌ API 错误: code={data.get('code')}, msg={data.get('message')}")
        return None

    result = data["data"]["contents"]
    root = {"id": result["content_id"], "name": result["content_name"]}
    sub_contents = result.get("sub_contents", [])
    info_map = result.get("content_id_to_info", {})

    print(f"  根节点: {root['name']} (id={root['id']})")
    print(f"  一级分类数: {len(sub_contents)}")

    # 逐个一级分类输出
    for i, sub in enumerate(sub_contents, 1):
        sub_id = sub["content_id"]
        sub_name = sub["content_name"]
        # Feature Guide 有二级嵌套
        sub_sub = sub.get("sub_contents")
        if sub_sub:
            print(f"\n  {i}. 📁 {sub_name} (id={sub_id}) [含二级分类]")
            for j, leaf in enumerate(sub_sub, 1):
                leaf_id = leaf["content_id"]
                leaf_name = leaf["content_name"]
                total = info_map.get(str(leaf_id), {}).get("total", "?")
                print(f"      {i}.{j}  📄 {leaf_name} (id={leaf_id}) 文章数={total}")
        else:
            total = info_map.get(str(sub_id), {}).get("total", "?")
            print(f"\n  {i}. 📁 {sub_name} (id={sub_id}) 文章数={total}")
            # 打印前 3 篇文章预览
            preview = info_map.get(str(sub_id), {}).get("learning_info", [])
            for k, art in enumerate(preview[:3], 1):
                print(f"      └─ [{k}] {art['name']}  (learning_id={art['learning_id']})")

    return result


# ---------------------------------------------------------------------------
# 2. 文章列表接口（contents/list）
# ---------------------------------------------------------------------------

def explore_article_list(content_id, page=1, limit=8):
    """拉取某个 classification 下的文章列表（分页）。"""
    print(f"\n{'='*60}")
    print(f"📃 文章列表  content_id={content_id}  page={page}")
    print(f"{'='*60}")

    params = {
        **COMMON_PARAMS,
        "content_id": content_id,
        "page": page,
        "limit": limit,
    }
    data = http_get("/api/v1/seller/learning_center/contents/list", params=params)
    if not data or data.get("code") != 0:
        print("  ❌ 请求失败")
        return None

    result = data["data"]
    total = result.get("total", "?")
    articles = result.get("learning_info", [])

    print(f"  总文章数: {total}  本页返回: {len(articles)}")
    for i, art in enumerate(articles, 1):
        print(f"  [{i}] {art['name']}")
        print(f"       learning_id={art['learning_id']}")
        print(f"       modify_time={art['modify_time']}")
        print(f"       views={art['views']}")
        print(f"       tags={[t['name'] for t in art.get('tag_info', [])]}")

    return result


# ---------------------------------------------------------------------------
# 3. 文章详情（SSR 页面解析）
# ---------------------------------------------------------------------------

def explore_article_detail(knowledge_id, role_type=1):
    """访问 essay 页面，解析 window._ROUTER_DATA 获取详情。

    注意：依赖 main() 中已经调用过 home 页初始化的 session，
    不要在函数内部重复访问 home 页（会触发限流）。
    """
    print(f"\n{'='*60}")
    print(f"📖 文章详情  knowledge_id={knowledge_id}")
    print(f"{'='*60}")

    url = f"{BASE_URL}/university/essay"
    params = {
        "identity": 1, "role": role_type, "knowledge_id": knowledge_id, "from": "course",
    }

    for attempt in range(1, 4):
        try:
            resp = session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            html = resp.text
            break
        except requests.RequestException as e:
            print(f"  ⚠️  第 {attempt}/3 次请求失败: {e}")
            time.sleep(1)
    else:
        print("  ❌ 全部失败")
        return None

    router_data = extract_router_data(html)
    if not router_data:
        print("  ❌ 未找到 window._ROUTER_DATA")
        return None

    # 数据路径：loaderData → essay/page → knowledge_detail
    page_data = router_data.get("loaderData", {}).get("essay/page", {})
    detail = page_data.get("knowledge_detail", {})
    if not detail:
        print("  ❌ knowledge_detail 不存在")
        return None

    # 注意：真正的 HTML 在 page_data["knowledge_content"]（含 <div class="converted-html"> + <video>）
    # detail["knowledge_content"] 是 Quill-delta 格式的 JSON 字符串（原始富文本数据）
    # 我们转换 Markdown 用的是 page_data 里的 HTML

    print(f"  knowledge_id   : {detail.get('knowledge_id')}")
    print(f"  knowledge_name : {detail.get('knowledge_name')}")
    print(f"  keywords       : {detail.get('keywords')}")
    print(f"  description    : {detail.get('description')[:100]}..." if detail.get('description') else "  description    : (空)")

    plain = detail.get("knowledge_plain_content", "")
    html_content = page_data.get("knowledge_content", "")  # ← 真正的 HTML 在这里
    print(f"\n  ✏️  knowledge_plain_content (前 300 字):")
    print(f"     {plain[:300]}")
    print(f"\n  🌐 knowledge_content (HTML, 前 300 字):")
    print(f"     {html_content[:300]}")

    # 视频元数据（从 HTML 里解析 <video> 标签）
    videos = BeautifulSoup(html_content, "html.parser").find_all("video")
    if videos:
        print(f"\n  🎬 检测到 {len(videos)} 个视频:")
        for v in videos:
            src = v.get("src") or (v.find("source") and v.find("source").get("src"))
            poster = v.get("poster")
            print(f"     - src={src[:80]}..." if src else "     - (无 src)")

    return {"detail": detail, "html": html_content, "plain": plain}


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    print("🚀 TikTok Seller University (BR) API 探路脚本")
    print(f"   目标站点: {BASE_URL}")
    print(f"   时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # ⚠️ 关键：整个脚本共用一个 session，且在开头初始化一次 home 页，
    # 这样后续所有 essay 请求都会返回葡语 pt-BR 内容。
    # 注意：不能用 http_get，因为 http_get 会尝试 .json() 解析 HTML 失败后重试，
    # 重试多次会破坏 session 状态，导致 essay 返回英文。
    print("\n📌 初始化 session（访问 home 页设置语言偏好）...")
    try:
        resp = session.get(f"{BASE_URL}/university/home", params={"identity": 1}, timeout=15)
        resp.raise_for_status()
        print(f"  ✓ home 页加载成功 (status={resp.status_code})")
    except requests.RequestException as e:
        print(f"  ⚠️ home 页加载失败: {e}")
    time.sleep(0.5)

    # ---- 1. 分类树 ----
    # 只打印 Seller 侧（role_type=1）的 Creator 侧结构类似
    print("\n\n" + "🔍" * 20 + " 1. 分类树探索 " + "🔍" * 20)

    explore_category("Cursos", **TABS["Cursos"], limit=8)
    explore_category("Feature_Guide", **TABS["Feature_Guide"], limit=12)
    explore_category("Policy_Center", **TABS["Policy_Center"], limit=12)

    # ---- 2. 文章列表（拿 Cursos/Start 来验证分页）----
    print("\n\n" + "🔍" * 20 + " 2. 文章列表探索 " + "🔍" * 20)
    explore_article_list(content_id=3875145967404801, page=1, limit=8)
    explore_article_list(content_id=3875145967404801, page=2, limit=8)

    # ---- 3. 文章详情（拿 Cursos/Start 第一篇 ERP 文章验证 SSR 解析）----
    print("\n\n" + "🔍" * 20 + " 3. 文章详情探索 (SSR 解析) " + "🔍" * 20)
    explore_article_detail(knowledge_id=605713333683985, role_type=1)

    # 再验证一篇 Feature Guide 的（两层嵌套的 leaf）
    explore_article_detail(knowledge_id=1721569656112912, role_type=1)

    print("\n\n✅ 探路完成。检查上面的输出，确认结构符合预期后再写 main.py。")


if __name__ == "__main__":
    main()
