#!/usr/bin/env python3
"""Builds the Imprese Favolose static site into ../site/ (Italian at the root, English under en/).
All words live in tools/content.py. site/assets/site.css is edited by hand.
Every HTML page, _headers and _redirects are generated here: never hand-edit them.

No-op maintenance note (22 Nov 2026): this comment triggers a fresh Cloudflare Pages deployment
after fixing the project's Build output directory setting to "site". No content or layout changed."""
import hashlib
import os
from pathlib import Path

from content import (EMAIL, FAB_CAMPAIGNS, HOME, NOTFOUND, PATHS, PROGRAMME, SITE_DRAFT, UI, VENTURES)

OUT = Path(__file__).resolve().parent.parent / "site"
DOMAIN = "https://impresefavolose.it"
LANG_TAG = {"it": "it-IT", "en": "en-GB"}
# Changes whenever site.css changes, so browsers never keep an old stylesheet.
CSS_VERSION = hashlib.sha256((OUT / "assets" / "site.css").read_bytes()).hexdigest()[:10]


def rel(target, current):
    """Relative link from the page at `current` to the file at `target` (both paths under site/).
    The 404 page is served at any address, so it uses links from the site root."""
    if current == "404.html":
        return "/" + target
    return os.path.relpath(target, os.path.dirname(current) or ".").replace(os.sep, "/")


def section(inner, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<section{c}><div class="wrap">{inner}</div></section>'


def draft_box(lang, questions):
    if not questions:
        return ""
    ui = UI[lang]
    qs = "".join(f"<li>{q}</li>" for q in questions)
    return section(f'<div class="draft-note"><p class="eyebrow">{ui["draft_title"]}</p>'
                   f'<p>{ui["draft_intro"]}</p><ul class="list">{qs}</ul></div>')


def mail_button(lang, label=None):
    subject = "Imprese%20Favolose"
    return f'<a class="btn" href="mailto:{EMAIL}?subject={subject}">{label or UI[lang]["contact"]}</a>'


def callout(title, text, lang):
    return section(f'<div class="callout"><h2>{title}</h2><p>{text}</p>'
                   f'<p class="contact-line"><a href="mailto:{EMAIL}">{EMAIL}</a></p>'
                   f'<div class="btn-row">{mail_button(lang)}</div></div>')


def public_url(path):
    """Address as Cloudflare Pages serves it (no index.html, no .html)."""
    return DOMAIN + "/" + path.replace("index.html", "").removesuffix(".html")


def page(key, lang, title, desc, body):
    current = PATHS[key][lang] if key in PATHS else "404.html"
    ui = UI[lang]
    nav = "\n".join(
        f'        <li><a href="{rel(PATHS[k][lang], current)}"{" aria-current=\"page\"" if k == key else ""}>{label}</a></li>'
        for k, label in ui["nav"])
    other = ui["switch_lang"]
    alternates = ""
    switch = ""
    if key in PATHS:
        alternates = "\n".join(
            f'<link rel="alternate" hreflang="{l}" href="{public_url(PATHS[key][l])}">' for l in ("it", "en"))
        alternates += f'\n<link rel="alternate" hreflang="x-default" href="{public_url(PATHS[key]["it"])}">'
        switch = f'<a class="lang" href="{rel(PATHS[key][other], current)}" hreflang="{other}" lang="{other}">{ui["switch"]}</a>'
    css = rel("assets/site.css", current)
    font = rel("assets/fonts/source-serif-4-latin-600-normal.woff2", current)
    home = rel(PATHS["home"][lang], current)
    return f"""<!doctype html>
<html lang="{LANG_TAG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="Imprese Favolose">
<meta name="twitter:card" content="summary">
{alternates}
<link rel="preload" href="{font}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{css}?v={CSS_VERSION}">
</head>
<body>
<a class="skip" href="#content">{ui["skip"]}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{home}"><span class="mark" aria-hidden="true"></span><span>Imprese Favolose</span></a>
    <nav class="site-nav" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
    {switch}
  </div>
</header>
<main id="content">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <span>&copy; 2026 {ui["footer"]}</span>
    <span>{ui["footer_by"]} <a href="{FAB_CAMPAIGNS}">Fab Campaigns Ltd</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</footer>
</body>
</html>
"""


def head(title, sub, eyebrow=""):
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f'<div class="page-head"><div class="wrap">{eb}<h1>{title}</h1><p>{sub}</p></div></div>'


# ---------------------------------------------------------------- page bodies
def home_body(lang):
    c = HOME[lang]
    cur = PATHS["home"][lang]
    btns = "".join(f'<a class="btn{" ghost" if i else ""}" href="{rel(PATHS[k][lang], cur)}">{t}</a>' for i, (k, t) in enumerate(c["cta"]))
    body = f"""<div class="hero"><div class="wrap">
<p class="eyebrow">{c["eyebrow"]}</p>
<h1>{c["h1"]}</h1>
<p class="lead">{c["lead"]}</p>
<div class="btn-row">{btns}</div>
</div></div>"""
    body += draft_box(lang, SITE_DRAFT + HOME["draft"])
    for h, paras in c["sections"]:
        body += section(f'<div class="prose"><h2>{h}</h2>' + "".join(f"<p>{p}</p>" for p in paras) + "</div>")
    cards = "".join(f'<div class="card"><span class="tag">{tag}</span><h3>{t}</h3><p>{x}</p></div>' for tag, t, x in c["cards"])
    body += section(f'<h2>{c["cards_title"]}</h2><div class="grid two">{cards}</div>'
                    f'<p class="more-link"><a href="{rel(PATHS["programme"][lang], cur)}">{UI[lang]["nav"][1][1]} &rarr;</a></p>')
    body += section(f'<div class="band"><h2>{c["model_title"]}</h2>' + "".join(f"<p>{p}</p>" for p in c["model"]) + "</div>")
    pr = "".join(f'<div class="card"><h3>{t}</h3><p>{x}</p></div>' for t, x in c["principles"])
    body += section(f'<h2>{c["principles_title"]}</h2><div class="grid">{pr}</div>')
    body += callout(c["callout_title"], c["callout"], lang)
    return c["title"], c["desc"], body


def programme_body(lang):
    c = PROGRAMME[lang]
    body = head(c["h1"], c["sub"])
    body += draft_box(lang, PROGRAMME["draft"])
    steps = ""
    for i, (tag, title, items, close) in enumerate(c["phases"], 1):
        lis = "".join(f"<li>{x}</li>" for x in items)
        steps += (f'<li class="phase"><span class="num" aria-hidden="true">{i}</span><div>'
                  f'<p class="eyebrow">{tag}</p><h2>{title}</h2><ul class="list">{lis}</ul><p>{close}</p></div></li>')
    body += section(f'<ol class="phases">{steps}</ol>')
    body += section(f'<div class="band"><h2>{c["after_title"]}</h2><p>{c["after"]}</p></div>')
    gov = "".join(f'<div class="card"><h3>{t}</h3><p>{x}</p></div>' for t, x in c["gov"])
    body += section(f'<div class="prose"><h2>{c["gov_title"]}</h2><p>{c["gov_lead"]}</p></div><div class="grid">{gov}</div>')
    body += callout(c["callout_title"], c["callout"], lang)
    return c["title"], c["desc"], body


def ventures_body(lang):
    c = VENTURES[lang]
    body = head(c["h1"], c["sub"])
    body += draft_box(lang, VENTURES["draft"])
    cards = ""
    for tag, name, text, link in c["ventures"]:
        more = f'<a class="more" href="{link[0]}">{link[1]} &rarr;</a>' if link else ""
        cards += f'<div class="card venture"><span class="tag">{tag}</span><h2>{name}</h2><p>{text}</p>{more}</div>'
    body += section(f'<div class="grid two">{cards}</div>')
    body += callout(c["callout_title"], c["callout"], lang)
    return c["title"], c["desc"], body


def notfound_body():
    n = NOTFOUND
    return n["title"], n["sub_it"], (
        f'<div class="page-head"><div class="wrap"><h1>{n["h1"]}</h1><p>{n["sub_it"]}</p>'
        f'<p lang="en-GB">{n["sub_en"]}</p></div></div>'
        + section(f'<div class="btn-row"><a class="btn" href="/">Home</a>'
                  f'<a class="btn ghost" href="/en/" lang="en-GB">English</a></div>'))


BODIES = {"home": home_body, "programme": programme_body, "ventures": ventures_body}

# Remove old generated pages so a deleted page cannot linger in site/.
for old in list(OUT.glob("*.html")) + list(OUT.glob("en/*.html")):
    old.unlink()

for key, fn in BODIES.items():
    for lang in ("it", "en"):
        title, desc, body = fn(lang)
        path = OUT / PATHS[key][lang]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page(key, lang, title, desc, body), encoding="utf-8")

t, d, b = notfound_body()
(OUT / "404.html").write_text(page("404", "it", t, d, b), encoding="utf-8")

# Old WordPress addresses -> new pages (Cloudflare Pages _redirects syntax).
(OUT / "_redirects").write_text("""/the-programme/ /en/programme 301
/our-ventures/ /en/ventures 301
/it/* / 301
/feed / 301
/wp-admin / 301
/wp-login.php / 301
""", encoding="utf-8")
(OUT / "_headers").write_text("""/*
  Content-Security-Policy: default-src 'none'; style-src 'self'; font-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  X-Frame-Options: DENY
/assets/*
  Cache-Control: public, max-age=604800
""", encoding="utf-8")
print("built", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()))
