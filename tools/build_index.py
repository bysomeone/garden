#!/usr/bin/env python3
"""garden 索引生成器：扫描 pages/ 下的 HTML，生成 index.html。

每个 HTML 应自带 <title>（作标题）和 <meta name="description">（作摘要）。
按 pages/ 下的一级目录（大类）分组。用法：python3 tools/build_index.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
OUT = ROOT / "index.html"

SKIP_DIRS = {".git", "tools", ".githooks"}

def read_head_text(p: Path) -> tuple[str, str]:
    raw = p.read_text(encoding="utf-8", errors="replace")
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
    desc = ""
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', raw, re.S | re.I)
    if m:
        desc = m.group(1).strip()
    return title, desc

def main() -> int:
    if not PAGES.is_dir():
        print(f"no pages/ dir at {PAGES}")
        return 1
    groups: dict[str, list[tuple[str, str, str]]] = {}
    for p in sorted(PAGES.rglob("*.html")):
        rel = p.relative_to(PAGES)
        parts = rel.parts
        group = parts[0] if len(parts) > 1 else "other"
        title, desc = read_head_text(p)
        if not title:
            title = p.stem
        groups.setdefault(group, []).append((title, desc, rel.as_posix()))

    body = ["<!doctype html>", '<html lang="zh-CN"><head><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>garden 文档库</title></head><body>",
            "<h1>garden · 文档库</h1>", '<p style="color:#666">此页由 tools/build_index.py 自动生成，新增文档后重新运行。</p>']
    total = 0
    for group in sorted(groups):
        body.append(f"<h2>{html.escape(group)}</h2>")
        body.append("<ul>")
        for title, desc, path in sorted(groups[group], key=lambda x: x[0]):
            item = f'<li><a href="pages/{html.escape(path)}">{html.escape(title)}</a>'
            if desc:
                item += f' <span style="color:#666">— {html.escape(desc)}</span>'
            item += "</li>"
            body.append(item)
            total += 1
        body.append("</ul>")
    body.append(f"<p>共 {total} 篇。</p>")
    body.append("</body></html>")
    OUT.write_text("\n".join(body), encoding="utf-8")
    print(f"index.html 已生成：{len(groups)} 个大类 / {total} 篇")
    return 0

if __name__ == "__main__":
    sys.exit(main())
