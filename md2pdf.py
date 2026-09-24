#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2pdf.py — 把 Markdown 转成 PDF(中文友好,图片正常)。

原理:markdown → HTML → 调系统自带 Edge 无头模式打印成 PDF。
依赖:markdown 库(一次性 `pip install markdown`)+ Microsoft Edge(系统自带)。

用法:
    python md2pdf.py 美术对接说明.md        # 生成同名 .pdf
    python md2pdf.py a.md b.md c.md          # 批量
    python md2pdf.py .                        # 转当前目录下所有 .md
"""

import os
import sys
import subprocess
from pathlib import Path

try:
    import markdown
except ImportError:
    print("缺少 markdown 库,请先执行: pip install markdown")
    sys.exit(1)

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
<style>
@page { size: A4; margin: 18mm 16mm; }
body {
    font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", sans-serif;
    font-size: 14px;
    line-height: 1.7;
    color: #222;
    max-width: 820px;
    margin: 0 auto;
}
h1, h2, h3, h4 { color: #111; margin-top: 1.4em; }
h1 { font-size: 1.8em; border-bottom: 2px solid #e0e0e0; padding-bottom: .3em; }
h2 { font-size: 1.4em; border-bottom: 1px solid #eaeaea; padding-bottom: .2em; }
h3 { font-size: 1.15em; }
code {
    font-family: "Consolas", "Courier New", monospace;
    background: #f5f5f5; padding: 2px 5px; border-radius: 3px; font-size: .9em;
}
pre {
    background: #f6f8fa; padding: 12px; border-radius: 6px;
    overflow-x: auto; border: 1px solid #e1e4e8;
}
pre code { background: none; padding: 0; }
img { max-width: 100%; border: 1px solid #eee; border-radius: 4px; }
table { border-collapse: collapse; margin: 1em 0; }
th, td { border: 1px solid #ccc; padding: 6px 12px; text-align: left; }
th { background: #f0f0f0; }
blockquote { color: #666; border-left: 4px solid #ddd; margin: 1em 0; padding: 0 1em; }
hr { border: none; border-top: 1px solid #e0e0e0; margin: 2em 0; }
</style>
"""


def find_edge():
    for p in EDGE_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def md_to_pdf(md_path, pdf_path=None):
    md_path = os.path.abspath(md_path)
    if not pdf_path:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"
    pdf_path = os.path.abspath(pdf_path)

    with open(md_path, encoding="utf-8") as f:
        text = f.read()

    body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "toc", "sane_lists"]
    )
    html = (
        '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
        + CSS
        + "</head><body>"
        + body
        + "</body></html>"
    )

    html_path = os.path.splitext(md_path)[0] + ".tmp.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    edge = find_edge()
    if not edge:
        print("找不到 Microsoft Edge,请确认已安装。")
        os.remove(html_path)
        sys.exit(1)

    url = Path(html_path).as_uri()  # 自动处理中文路径编码
    try:
        subprocess.run(
            [
                edge,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--virtual-time-budget=8000",  # 等图片加载完再打印
                f"--print-to-pdf={pdf_path}",
                url,
            ],
            check=True,
            capture_output=True,
        )
    finally:
        os.remove(html_path)

    print(f"[OK] {os.path.basename(md_path)} -> {os.path.basename(pdf_path)}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    md_files = []
    for a in args:
        if os.path.isdir(a):
            for f in sorted(os.listdir(a)):
                if f.lower().endswith(".md"):
                    md_files.append(os.path.join(a, f))
        elif a.lower().endswith(".md"):
            md_files.append(a)
        else:
            print(f"跳过(非 .md): {a}")

    if not md_files:
        print("没有找到 .md 文件")
        sys.exit(1)

    for m in md_files:
        md_to_pdf(m)


if __name__ == "__main__":
    main()
