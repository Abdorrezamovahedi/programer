#!/usr/bin/env python3
"""
MCD Code Up — Bulk SEO Fixer
اجرا از ریشهٔ ریپو:
    python bulk-seo-fix.py

کارهایی که انجام می‌دهد:
- اضافه کردن favicon و apple-touch-icon اگر نباشد
- اضافه کردن og:image و twitter:image اگر نباشد
- مرتب‌سازی نسبی تگ‌های مهم head (charset اول)
"""
from pathlib import Path
import re

ROOT = Path(".")
BASE = "https://abdorrezamovahedi.github.io/programer"
OG_IMAGE = f"{BASE}/assets/img/og-default.svg"
FAVICON = f"{BASE}/assets/img/favicon.svg"
APPLE = f"{BASE}/assets/img/og-default.svg"

FAVICON_TAGS = f'''<link rel="icon" href="{FAVICON}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{APPLE}">'''

OG_IMAGE_TAGS = f'''<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">'''

def ensure_tags(html: str) -> tuple:
    changes = []
    if 'rel="icon"' not in html and "rel='icon'" not in html:
        if "</head>" in html:
            html = html.replace("</head>", FAVICON_TAGS + "\n</head>", 1)
            changes.append("favicon")
    if 'property="og:image"' not in html and "property='og:image'" not in html:
        if "</head>" in html:
            html = html.replace("</head>", OG_IMAGE_TAGS + "\n</head>", 1)
            changes.append("og:image")
    if re.search(r"<head[^>]*>\s*<meta[^>]+charset", html, re.I) is None:
        m = re.search(r"(<head[^>]*>)", html, re.I)
        if m and 'charset' in html.lower():
            charset_m = re.search(r'<meta[^>]+charset[^>]*>', html, re.I)
            if charset_m:
                tag = charset_m.group(0)
                html = html.replace(tag, "", 1)
                html = html[:m.end()] + "\n" + tag + html[m.end():]
                changes.append("charset-order")
    return html, changes

def main():
    html_files = [p for p in ROOT.rglob("*.html") if "node_modules" not in str(p)]
    print(f"Found {len(html_files)} HTML files")
    updated = 0
    for p in html_files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"SKIP {p}: {e}")
            continue
        new_text, changes = ensure_tags(text)
        if changes:
            p.write_text(new_text, encoding="utf-8")
            updated += 1
            print(f"OK  {p}  (+{', '.join(changes)})")
    print(f"\nDone. Updated {updated} files.")
    print("Next: git add -A && git commit -m 'SEO: add favicon + og:image sitewide' && git push")

if __name__ == "__main__":
    main()
