#!/usr/bin/env python3
"""
generate_sidebar.py — 为 Rspress 自动生成 sidebar 配置
输出到 sidebar.yml，然后被 rspress.config.ts 引用
Rspress sidebar 格式：
{
  '/cursos/': [
    { text: 'AFILIADO', link: '/cursos/afiliado/' },
    { text: 'AVANÇADO', link: '/cursos/avançado/' },
    ...
  ]
}
"""
import os
import json
import re

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_DIR, "docs")
SIDEBAR_FILE = os.path.join(REPO_DIR, "sidebar.yml")


def prettify(name):
    return name.replace("-", " ").replace("_", " ").strip().title()


def same_label(left, right):
    def normalize(value):
        return re.sub(r"[\s_-]+", " ", value).strip().casefold()

    return normalize(left) == normalize(right)


def read_title(md_path, fallback):
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read(2048)
    except OSError:
        return fallback

    match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', text, re.MULTILINE)
    if match:
        title = match.group(1).replace('\\"', '"').strip()
        return fallback if same_label(title, fallback) else title

    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        return fallback if same_label(title, fallback) else title

    return fallback


def link_for(path, is_dir=False):
    rel = os.path.relpath(path, DOCS_DIR).replace(os.sep, "/")
    return f"/{rel}/" if is_dir else f"/{rel[:-3]}"


def scan(path):
    items = []
    for entry in sorted(os.listdir(path)):
        if entry.startswith(".") or entry == "public":
            continue
        full = os.path.join(path, entry)
        if entry == "index.md":
            continue
        if os.path.isdir(full):
            index_md = os.path.join(full, "index.md")
            title = read_title(index_md, prettify(entry)) if os.path.exists(index_md) else prettify(entry)
            group = {
                "text": title,
                "link": link_for(full, is_dir=True),
                "items": scan(full),
            }
            items.append(group)
        elif entry.endswith(".md"):
            fallback = prettify(entry[:-3].rsplit("_", 1)[0])
            items.append({"text": read_title(full, fallback), "link": link_for(full)})
    return items

sidebar = {
    "/cursos/": scan(os.path.join(DOCS_DIR, "cursos")),
    "/feature-guide/": scan(os.path.join(DOCS_DIR, "feature-guide")),
    "/policy-center/": scan(os.path.join(DOCS_DIR, "policy-center")),
}

with open(SIDEBAR_FILE, "w", encoding="utf-8") as f:
    json.dump(sidebar, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("已生成 sidebar.yml")
for k, v in sidebar.items():
    print(f"  {k}: {len(v)} 项")
    for item in v[:3]:
        print(f"    - {item['text'][:20]} -> {item['link']}")
