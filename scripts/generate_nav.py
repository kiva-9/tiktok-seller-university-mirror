#!/usr/bin/env python3
"""
generate_nav.py — 根据 docs/ 目录结构自动生成 mkdocs.yml 的 nav 配置
"""
import os
import yaml

DOCS_DIR = "docs"
MKDOCS_YML = "mkdocs.yml"


def scan_directory(path, prefix=""):
    """递归扫描目录，返回 nav 结构"""
    items = []

    # 先找 index.md（目录页）
    index_md = os.path.join(path, "index.md")
    if os.path.exists(index_md):
        rel_path = os.path.relpath(index_md, DOCS_DIR)
        items.append({rel_path: rel_path})

    # 收集子目录和 md 文件
    subdirs = []
    pages = []
    for entry in sorted(os.listdir(path)):
        full = os.path.join(path, entry)
        if entry == "index.md":
            continue
        if os.path.isdir(full):
            subdirs.append(entry)
        elif entry.endswith(".md"):
            pages.append(entry)

    # 子目录递归
    for d in subdirs:
        full = os.path.join(path, d)
        rel = os.path.relpath(full, DOCS_DIR)
        sub_items = scan_directory(full, prefix=rel)
        if sub_items:
            items.append({d: sub_items})

    # 其他 md 文件
    for p in pages:
        rel_path = os.path.relpath(os.path.join(path, p), DOCS_DIR)
        items.append({p.replace(".md", ""): rel_path})

    return items


def main():
    nav = [
        {"首页": "index.md"},
        {"Cursos": scan_directory(os.path.join(DOCS_DIR, "cursos"))},
        {"Feature Guide": scan_directory(os.path.join(DOCS_DIR, "feature-guide"))},
        {"Policy Center": scan_directory(os.path.join(DOCS_DIR, "policy-center"))},
    ]

    # 读取现有 mkdocs.yml
    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["nav"] = nav

    # 写回
    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"已生成 nav，共 {len(nav)} 个顶级分类")


if __name__ == "__main__":
    main()
