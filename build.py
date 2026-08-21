#!/usr/bin/env python3
"""各アプリの docs/*.md から、公開用の HTML を作る。

**本文の正本は各アプリのリポジトリにある Markdown。**このリポジトリの HTML は生成物なので、
文章を直すときは md を直してから、これを流し直す。
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent

# (出力先, 元の md, ページタイトル, 言語)
PAGES = [
    ("timephoto/privacy-ja.html", "../time-photo/docs/privacy-policy-ja.md",
     "プライバシーポリシー ｜ TimePhoto", "ja"),
    ("timephoto/privacy-en.html", "../time-photo/docs/privacy-policy-en.md",
     "Privacy Policy | TimePhoto", "en"),
    ("timephoto/terms-ja.html", "../time-photo/docs/terms-of-service-ja.md",
     "利用規約 ｜ TimePhoto", "ja"),
]

TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="robots" content="index, follow">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<main>
{body}
<p class="back"><a href="../index.html">{back}</a></p>
</main>
</body>
</html>
"""


def inline(s):
    """行内の記法だけ処理する。エスケープしてから戻すので順番を変えない。"""
    s = html.escape(s)
    s = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    return s


def convert(md):
    out, i = [], 0
    lines = md.split("\n")
    while i < len(lines):
        ln = lines[i]

        if m := re.match(r'^(#{1,4}) (.*)', ln):
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1

        elif ln.startswith("|"):                      # 表
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]   # 2行目は区切り
            out.append("<table><thead><tr>"
                       + "".join(f"<th>{inline(c)}</th>" for c in head)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                                 for r in body)
                       + "</tbody></table>")

        elif re.match(r'^- ', ln):                    # 箇条書き
            items = []
            while i < len(lines) and re.match(r'^\s*- ', lines[i]):
                items.append(inline(re.sub(r'^\s*- ', '', lines[i])))
                i += 1
            out.append("<ul>" + "".join(f"<li>{t}</li>" for t in items) + "</ul>")

        elif re.match(r'^\d+\. ', ln):                # 番号付き
            items = []
            while i < len(lines) and (re.match(r'^\d+\. ', lines[i]) or re.match(r'^\s{2,}- ', lines[i])):
                if re.match(r'^\s{2,}- ', lines[i]):   # ぶら下がりの箇条書き
                    items[-1] += f"<br>{inline(re.sub(r'^\\s*- ', '', lines[i]))}"
                else:
                    items.append(inline(re.sub(r'^\d+\. ', '', lines[i])))
                i += 1
            out.append("<ol>" + "".join(f"<li>{t}</li>" for t in items) + "</ol>")

        elif ln.strip() == "":
            i += 1

        else:                                          # 段落
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||-\s|\d+\.\s)', lines[i]):
                buf.append(lines[i].strip())
                i += 1
            out.append("<p>" + inline("".join(buf)) + "</p>")

    return "\n".join(out)


def main():
    for dst, src, title, lang in PAGES:
        src_path = (ROOT / src).resolve()
        if not src_path.exists():
            raise SystemExit(f"元の md が見つからない: {src_path}")
        body = convert(src_path.read_text(encoding="utf-8"))
        back = "← 一覧にもどる" if lang == "ja" else "← Back to index"
        out = ROOT / dst
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(TEMPLATE.format(lang=lang, title=title, body=body, back=back),
                       encoding="utf-8")
        print(f"{dst}  ←  {src}")


if __name__ == "__main__":
    main()
