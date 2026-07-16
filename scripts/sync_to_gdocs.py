#!/usr/bin/env python3
"""
sync_to_gdocs.py — 将 docs/ 下所有 .md 文件按分类合流到多个 Google Docs

按顶级目录分组，每组合并为一个或多个文档（按 1M 字符上限自动拆分）。
每个分类可配置多个 Doc ID（含备用），多余的 ID 闲置不动。

环境变量：
  GOOGLE_SERVICE_ACCOUNT_JSON — 服务账号 JSON 内容
  GOOGLE_DOCS_DOCUMENT_IDS   — JSON 映射，如：
    {
      "cursos": ["ID_1", "ID_2", "ID_3"],
      "feature-guide": ["ID_4", "ID_5", "ID_6", "ID_7"],
      "policy-center": ["ID_8", "ID_9", "ID_10"]
    }
    每个分类至少提供一个 ID，多余的作为备用，脚本只使用需要的数量。
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_DIR, "docs")
SCOPES = ["https://www.googleapis.com/auth/documents"]
CHUNK_SIZE = 100_000
MAX_DOC_CHARS = 1_000_000  # Google Docs 上限 ~1.02M，留安全余量


# ---------------------------------------------------------------------------
# 认证
# ---------------------------------------------------------------------------

def get_service():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        print("❌ 缺少环境变量 GOOGLE_SERVICE_ACCOUNT_JSON")
        sys.exit(1)
    info = json.loads(sa_json)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("docs", "v1", credentials=creds)


# ---------------------------------------------------------------------------
# 文件扫描
# ---------------------------------------------------------------------------

def scan_md_files(docs_dir):
    files = []
    for root, dirs, filenames in os.walk(docs_dir):
        dirs.sort()
        for fname in sorted(filenames):
            if fname == "index.md" or not fname.endswith(".md"):
                continue
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, docs_dir)
            files.append((full, rel))
    files.sort(key=lambda x: x[1])
    return files


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            fm_text = text[3:end].strip()
            body = text[end + 3:].strip()
            try:
                import yaml
                fm = yaml.safe_load(fm_text) or {}
                if not isinstance(fm, dict):
                    fm = {}
            except Exception:
                fm = {}
            return fm, body
    return {}, text


def extract_title(fm, body, fallback):
    title = fm.get("title", "") or ""
    if not title:
        m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if m:
            title = m.group(1).strip()
    return title or fallback


# ---------------------------------------------------------------------------
# 合并文档生成
# ---------------------------------------------------------------------------

def build_merged_doc(files, group_label=""):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = []

    if group_label:
        sections.append(f"# 📚 {group_label}\n")
    sections.append(f"> Documento consolidado gerado automaticamente em {now}\n")

    articles = []
    for full_path, rel_path in files:
        with open(full_path, "r", encoding="utf-8") as f:
            raw = f.read()
        fm, body = strip_frontmatter(raw)
        title = extract_title(fm, body, Path(full_path).stem.replace("_", " ").title())
        update_time = fm.get("update_time", "")
        url = fm.get("url", "")
        articles.append({
            "title": title,
            "path": rel_path,
            "update_time": update_time,
            "url": url,
            "body": body.strip(),
        })

    for art in articles:
        url_part = f" [🔗 Original]({art['url']})" if art["url"] else ""
        sections.append(f"- **{art['title']}** — `{art['path']}`{url_part}")

    sections.append("")
    sections.append("<!-- SEPARATOR -->")
    sections.append("")

    for art in articles:
        sections.append("<!-- ARTICLE START -->")
        sections.append(f"# {art['title']}")
        meta = []
        if art["path"]:
            meta.append(f"📁 `{art['path']}`")
        if art["update_time"]:
            meta.append(f"🕐 {art['update_time']}")
        if art["url"]:
            meta.append(f"🔗 [Original]({art['url']})")
        sections.append(f"> {' | '.join(meta)}")
        sections.append("")
        sections.append("---")
        sections.append("")
        sections.append(art["body"])
        sections.append("")
        sections.append("<!-- ARTICLE END -->")
        sections.append("")

    sections.append("---")
    sections.append("")
    sections.append(f"*📄 {len(articles)} artigos — gerado em {now} via GitHub Actions*")
    sections.append("")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# 分组与拆分
# ---------------------------------------------------------------------------

def group_by_category(files):
    groups = {}
    for full_path, rel_path in files:
        top = rel_path.split("/")[0]
        groups.setdefault(top, []).append((full_path, rel_path))
    return groups


def split_if_too_large(files, max_chars):
    """按累计字符数拆分子组，每组不超过 max_chars。"""
    groups = []
    current = []
    current_size = 0

    for full_path, rel_path in files:
        with open(full_path, "r", encoding="utf-8") as f:
            raw = f.read()
        fm, body = strip_frontmatter(raw)
        title = extract_title(fm, body, Path(full_path).stem.replace("_", " ").title())
        article_text = f"# {title}\n---\n{body.strip()}\n"
        article_size = len(article_text)

        if current and current_size + article_size > max_chars:
            groups.append(current)
            current = []
            current_size = 0
        current.append((full_path, rel_path))
        current_size += article_size

    if current:
        groups.append(current)

    return groups


# ---------------------------------------------------------------------------
# Google Docs API
# ---------------------------------------------------------------------------

def ensure_document(service, doc_id):
    try:
        return service.documents().get(documentId=doc_id).execute()
    except HttpError as e:
        if e.resp.status == 404:
            print(f"   📝 文档不存在，请先创建: https://docs.google.com/document/d/{doc_id}")
            sys.exit(1)
        raise


def overwrite_document(service, doc_id, content):
    doc = ensure_document(service, doc_id)
    body_content = doc.get("body", {}).get("content", [])
    if not body_content:
        return False

    # 一步清空正文（endIndex - 1 避免触碰末尾受保护的换行符）
    total_length = body_content[-1]["endIndex"]
    if total_length > 2:
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": total_length - 1}
            }}]}
        ).execute()

    # 逐块插入
    chunks = []
    start = 0
    while start < len(content):
        end = min(start + CHUNK_SIZE, len(content))
        if end < len(content):
            br = content.rfind("\n\n", start, end)
            if br > start:
                end = br + 2
        chunks.append(content[start:end])
        start = end

    idx = 1
    for n, chunk in enumerate(chunks, 1):
        print(f"   📝 插入 {n}/{len(chunks)} ({len(chunk):,} 字符)")
        for attempt in range(3):
            try:
                service.documents().batchUpdate(
                    documentId=doc_id,
                    body={"requests": [{"insertText": {"location": {"index": idx}, "text": chunk}}]}
                ).execute()
                break
            except HttpError as e:
                if e.resp.status == 429 and attempt < 2:
                    wait = 5 * (2 ** attempt)
                    print(f"   ⏳ 限流，等待 {wait}s 后重试...")
                    time.sleep(wait)
                else:
                    raise
        idx += len(chunk)

    return True


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    doc_ids_raw = os.environ.get("GOOGLE_DOCS_DOCUMENT_IDS", "{}")
    try:
        doc_map = json.loads(doc_ids_raw)
    except json.JSONDecodeError:
        print("❌ GOOGLE_DOCS_DOCUMENT_IDS 格式错误，需要 JSON 对象")
        sys.exit(1)

    # 校验：每个分类必须有至少一个 ID
    for cat, ids in doc_map.items():
        if not isinstance(ids, list) or len(ids) == 0:
            print(f"❌ 分类 '{cat}' 需要至少一个 Doc ID（数组格式）")
            sys.exit(1)

    if not doc_map:
        print("❌ 缺少 GOOGLE_DOCS_DOCUMENT_IDS 环境变量")
        sys.exit(1)

    print("🔍 扫描 docs/ 目录...")
    files = scan_md_files(DOCS_DIR)
    print(f"   找到 {len(files)} 个 .md 文件")
    if not files:
        sys.exit(0)

    # 按分类分组
    groups = group_by_category(files)

    # 检查是否有未配置的分类
    configured_cats = set(groups.keys())
    missing = configured_cats - set(doc_map.keys())
    if missing:
        print(f"❌ 以下分类缺少 Doc ID 配置: {', '.join(sorted(missing))}")
        print(f"   已配置: {sorted(doc_map.keys())}")
        sys.exit(1)

    # 对超过上限的分组拆分，按序分配 Doc ID
    service = get_service()
    total_docs_used = 0

    for cat in sorted(groups.keys()):
        cat_files = groups[cat]
        doc_ids = doc_map[cat]

        # 按字符上限拆分子组
        subgroups = split_if_too_large(cat_files, MAX_DOC_CHARS)
        needed = len(subgroups)

        if needed > len(doc_ids):
            print(f"❌ {cat} 需要 {needed} 个文档，但只配置了 {len(doc_ids)} 个 ID")
            sys.exit(1)

        for i, sub_files in enumerate(subgroups, 1):
            doc_id = doc_ids[i - 1]
            label = f"{cat} ({i}/{needed})"
            print(f"\n🔗 合流 {label}...")
            merged = build_merged_doc(sub_files, group_label=label)
            print(f"   📄 {len(merged):,} 字符")

            print(f"☁️  覆写 {doc_id}...")
            try:
                ok = overwrite_document(service, doc_id, merged)
                if ok:
                    print(f"   ✅ {label} — https://docs.google.com/document/d/{doc_id}")
                    total_docs_used += 1
                else:
                    print(f"   ❌ {label} 覆写失败")
            except HttpError as e:
                print(f"   ❌ {label} API 错误 (HTTP {e.resp.status}): {e}")
            except Exception as e:
                print(f"   ❌ {label} 错误: {e}")

        spare = len(doc_ids) - needed
        if spare > 0:
            print(f"   📦 {cat}: 使用 {needed}/{len(doc_ids)} 个 ID，{spare} 个备用")

    print(f"\n✅ 全部完成，写入 {total_docs_used} 个文档")


if __name__ == "__main__":
    main()
