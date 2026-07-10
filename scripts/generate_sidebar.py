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
import yaml

DOCS_DIR = "docs"

def scan(path, base):
    items = []
    for entry in sorted(os.listdir(path)):
        full = os.path.join(path, entry)
        rel = os.path.relpath(full, DOCS_DIR)
        if entry == "index.md":
            continue
        if os.path.isdir(full):
            items.append({"text": entry.upper(), "link": f"/{rel}/"})
        elif entry.endswith(".md"):
            title = entry.replace(".md", "").replace("_", " ")
            items.append({"text": title, "link": f"/{rel}"})
    return items

sidebar = {
    "/cursos/": scan(os.path.join(DOCS_DIR, "cursos"), "cursos"),
    "/feature-guide/": scan(os.path.join(DOCS_DIR, "feature-guide"), "feature-guide"),
    "/policy-center/": scan(os.path.join(DOCS_DIR, "policy-center"), "policy-center"),
}

with open("sidebar.yml", "w") as f:
    yaml.dump(sidebar, f, allow_unicode=True, default_flow_style=False)

print("已生成 sidebar.yml")
for k, v in sidebar.items():
    print(f"  {k}: {len(v)} 项")
    for item in v[:3]:
        print(f"    - {item['text'][:20]} -> {item['link']}")
