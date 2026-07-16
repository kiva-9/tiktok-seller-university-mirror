#!/usr/bin/env python3
"""
sync_to_gdocs.py — 将 docs/ 下所有 .md 文件合并为单个 Google Docs 文档

流程：
  1. 递归扫描 docs/，找到所有 .md 文件（排除 index.md）
  2. 按路径排序，逐篇读取
  3. 剥离 YAML frontmatter，提取元数据
  4. 生成合并文档：
     - 顶部：自动知识目录（TOC）
     - 每篇文章：H1 标题 + 路径/更新时间/原始链接 + 水平分割线 + 正文
  5. 通过 Google Docs API 覆写到指定文档 ID

认证方式：服务账号密钥 JSON

环境变量：
  GOOGLE_SERVICE_ACCOUNT_JSON — 服务账号 JSON 内容
  GOOGLE_DOCS_DOCUMENT_ID   — 目标 Google Docs 文档 ID
"""
import json
import os
import re
import sys
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
CHUNK_SIZE = 500_000


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
# Frontmatter 处理
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

def build_merged_doc(files):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = []

    sections.append("# 📚 Índice de Conteúdo\n")
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
    sections.append(f"*📄 Documento consolidado — {len(articles)} artigos — gerado em {now} via GitHub Actions*")
    sections.append("")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Google Docs API
# ---------------------------------------------------------------------------

def ensure_document(service, doc_id):
    try:
        return service.documents().get(documentId=doc_id).execute()
    except HttpError as e:
        if e.resp.status == 404:
            print("   📝 文档不存在，请先手动创建一个 Google Docs，获取 ID 后配置到 Secret")
            sys.exit(1)
        raise


def overwrite_document(service, doc_id, content):
    doc = ensure_document(service, doc_id)
    body_content = doc.get("body", {}).get("content", [])
    if not body_content:
        print("⚠️ 文档结构异常")
        return False

    total_length = body_content[-1]["endIndex"]

    # 清空正文（total_length - 1 避免触碰末尾受保护的换行符）
    if total_length > 1:
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": total_length - 1}
            }}]}
        ).execute()

    # 分块插入
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

    requests_list = []
    idx = 1
    for chunk in chunks:
        requests_list.append({"insertText": {"location": {"index": idx}, "text": chunk}})
        idx += len(chunk)

    service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests_list}
    ).execute()

    return True


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    doc_id = os.environ.get("GOOGLE_DOCS_DOCUMENT_ID")
    if not doc_id:
        print("❌ 缺少环境变量 GOOGLE_DOCS_DOCUMENT_ID")
        sys.exit(1)

    print("🔍 扫描 docs/ 目录...")
    files = scan_md_files(DOCS_DIR)
    print(f"   找到 {len(files)} 个 .md 文件")
    if not files:
        print("⚠️ 没有找到需要同步的文件")
        sys.exit(0)

    print("🔗 合并为单文档...")
    merged = build_merged_doc(files)
    print(f"   合并后大小: {len(merged):,} 字符")

    print("🔐 获取 Google 凭证...")
    service = get_service()

    print("☁️  覆写到 Google Docs...")
    try:
        ok = overwrite_document(service, doc_id, merged)
        if ok:
            print(f"   ✅ 成功覆写文档: https://docs.google.com/document/d/{doc_id}")
        else:
            print("   ❌ 覆写失败")
            sys.exit(1)
    except HttpError as e:
        print(f"   ❌ Google Docs API 错误 (HTTP {e.resp.status}): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"   ❌ 未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
