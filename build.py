#!/usr/bin/env python3
"""静的サイト生成スクリプト（くらしの計算箱）

tools/<slug>.html の先頭コメントブロックにメタ情報を書き、本文（フォーム＋script＋解説）を続ける。
`python3 build.py` で dist/ 以下に完成ページ・index・sitemap・robots を出力する。
"""
import json
import os
import re
import datetime
import html

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(ROOT, "tools")
PAGES_DIR = os.path.join(ROOT, "pages")
DIST = os.path.join(ROOT, "dist")
CONFIG = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))

META_RE = re.compile(r"^<!--meta\s*(\{.*?\})\s*-->", re.S)


def read_tool(path):
    src = open(path, encoding="utf-8").read()
    m = META_RE.match(src)
    if not m:
        raise SystemExit(f"meta block missing: {path}")
    meta = json.loads(m.group(1))
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["body"] = src[m.end():].strip()
    return meta


def layout(title, description, body, path, extra_head="", is_tool=False, meta=None):
    base = CONFIG["base_url"].rstrip("/")
    canonical = f"{base}/{path}".replace("/index.html", "/")
    site = CONFIG["site_name"]
    full_title = f"{title}｜{site}" if title != site else site
    jsonld = ""
    if is_tool and meta:
        data = {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": title,
            "description": description,
            "url": canonical,
            "applicationCategory": "UtilityApplication",
            "operatingSystem": "Any",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"},
            "inLanguage": "ja",
        }
        jsonld = f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'
        if meta.get("faq"):
            faq = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in meta["faq"]
                ],
            }
            jsonld += f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'
    depth = path.count("/")
    rel = "../" * depth if depth else "./"
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{html.escape(site)}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{rel}style.css">
{jsonld}
{extra_head}
</head>
<body>
<header class="site-header">
  <a class="brand" href="{rel}">{html.escape(site)}</a>
  <nav><a href="{rel}#tools">ツール一覧</a><a href="{rel}about/">このサイトについて</a></nav>
</header>
<main class="container">
{body}
</main>
<footer class="site-footer">
  <p><a href="{rel}">{html.escape(site)}</a> ｜ <a href="{rel}about/">このサイトについて</a> ｜ <a href="{rel}privacy/">プライバシーポリシー</a> ｜ <a href="{rel}contact/">お問い合わせ</a></p>
  <p class="small">計算結果は目安です。重要な判断には公式情報・専門家の確認をお願いします。</p>
  <p class="small">© {datetime.date.today().year} {html.escape(site)}</p>
</footer>
</body>
</html>
"""


def tool_page(meta, all_tools):
    h1 = meta.get("h1") or meta["title"].split("｜")[0]
    related = [t for t in all_tools if t["category"] == meta["category"] and t["slug"] != meta["slug"]][:4]
    rel_html = ""
    if related:
        items = "".join(f'<li><a href="../{t["slug"]}/">{html.escape(t.get("h1") or t["title"].split("｜")[0])}</a></li>' for t in related)
        rel_html = f'<section class="related"><h2>関連ツール</h2><ul>{items}</ul></section>'
    faq_html = ""
    if meta.get("faq"):
        qa = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in meta["faq"])
        faq_html = f'<section class="faq"><h2>よくある質問</h2>{qa}</section>'
    body = f"""
<nav class="breadcrumb"><a href="../">ホーム</a> › <span>{html.escape(meta["category"])}</span> › <span>{html.escape(h1)}</span></nav>
<article class="tool">
<h1>{html.escape(h1)}</h1>
<p class="lead">{html.escape(meta["description"])}</p>
{meta["body"]}
{faq_html}
{rel_html}
<p class="updated small">最終更新: {meta.get("updated", datetime.date.today().isoformat())}</p>
</article>
"""
    return layout(meta["title"], meta["description"], body, f"{meta['slug']}/index.html", is_tool=True, meta=meta)


def index_page(all_tools):
    cats = {}
    for t in all_tools:
        cats.setdefault(t["category"], []).append(t)
    sections = ""
    for cat, tools in cats.items():
        cards = "".join(
            f'<a class="card" href="{t["slug"]}/"><h3>{html.escape(t.get("h1") or t["title"].split("｜")[0])}</h3><p>{html.escape(t["summary"])}</p></a>'
            for t in tools
        )
        sections += f'<section class="cat"><h2>{html.escape(cat)}</h2><div class="grid">{cards}</div></section>'
    body = f"""
<section class="hero">
<h1>{html.escape(CONFIG["site_name"])}</h1>
<p class="lead">{html.escape(CONFIG["tagline"])}</p>
<p class="small">登録不要・無料・入力内容はブラウザ内でのみ計算され、送信されません。</p>
</section>
<div id="tools">{sections}</div>
"""
    return layout(CONFIG["site_name"], CONFIG["tagline"], body, "index.html")


def static_page(name, title, description):
    src = open(os.path.join(PAGES_DIR, f"{name}.html"), encoding="utf-8").read()
    body = f'<nav class="breadcrumb"><a href="../">ホーム</a> › <span>{html.escape(title)}</span></nav><article class="page"><h1>{html.escape(title)}</h1>{src}</article>'
    return layout(title, description, body, f"{name}/index.html")


def write(path, content):
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def main():
    tools = [read_tool(os.path.join(TOOLS_DIR, f)) for f in sorted(os.listdir(TOOLS_DIR)) if f.endswith(".html")]
    tools.sort(key=lambda t: (t.get("order", 99), t["slug"]))
    for t in tools:
        write(f"{t['slug']}/index.html", tool_page(t, tools))
    write("index.html", index_page(tools))
    for name, title, desc in CONFIG["pages"]:
        write(f"{name}/index.html", static_page(name, title, desc))
    # assets
    for asset in ("style.css", "favicon.svg"):
        write(asset, open(os.path.join(ROOT, asset), encoding="utf-8").read())
    base = CONFIG["base_url"].rstrip("/")
    today = datetime.date.today().isoformat()
    urls = [f"{base}/"] + [f"{base}/{t['slug']}/" for t in tools] + [f"{base}/{p[0]}/" for p in CONFIG["pages"]]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"built {len(tools)} tools -> {DIST}")


if __name__ == "__main__":
    main()
