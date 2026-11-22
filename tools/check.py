#!/usr/bin/env python3
"""Health and safety check for the Imprese Favolose site. GitHub runs it on every pull request.
Run locally with: python3 tools/check.py   (exit code 1 = errors, merge blocked)

Errors: things that must never ship. Warnings: decisions for Fabrizio, never auto-fixed.
Changing this file needs Fabrizio's approval (see CLAUDE.md)."""
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# Outbound link domains Fabrizio has approved. Adding one needs his approval.
LINK_DOMAINS = {"fabcampaigns.com", "smartmountains.net", "fabrizio.deliberali.com"}
# The only email address the site may show or link to.
EMAILS = {"info@impresefavolose.it"}
FORBIDDEN_TAGS = {"script", "iframe", "form", "object", "embed", "frame", "frameset", "base", "svg"}
# File types allowed in site/. Anything else (js, php, svg, pdf, docs) needs Fabrizio's approval.
ALLOWED_FILES = {".html", ".css", ".woff2", ".png", ".jpg", ".jpeg", ".webp", ".ico"}
ALLOWED_NAMES = {"_headers", "_redirects"}
REQUIRED_HEADERS = ["default-src 'none'", "frame-ancestors 'none'", "form-action 'none'", "X-Content-Type-Options: nosniff"]
EXPECTED_REDIRECTS = {
    "/the-programme/ /en/programme 301", "/our-ventures/ /en/ventures 301", "/it/* / 301",
    "/feed / 301", "/wp-admin / 301", "/wp-login.php / 301",
}
LANGS = {"it-IT", "en-GB"}

# Claims that must not appear without Fabrizio's explicit approval (visible text, any case).
# The incubator holds no certification or accreditation: never say or imply it does.
CLAIMS = [
    (r"certificat|certified|certify|accreditat|accredited|mimit|riconosciut[oa] dal ministero",
     "certification or accreditation claim (Imprese Favolose is not certified)"),
    (r"fraction|frazional", "'fractional' framing (dropped everywhere)"),
    (r"thought leader|passionate about|excited to share|just published|unlock|elevate|game.?changer|cutting.?edge|world.?class|best.?in.?class|synerg|sinergi|eccellenz",
     "banned marketing language"),
]
# Numbers that need verification before they go public: equity, percentages, money.
NUMBERS = [
    (r"\d\s?%|per ?cento|percent", "percentage (equity and shareholdings need verified figures and Fabrizio's approval)"),
    (r"[€£$]|\beur\b|\beuro\b|\bgbp\b|\bk€|\bmln\b|\bmillion", "money amount (fees, funding and valuations need Fabrizio's approval)"),
]
# Words that are decisions for Fabrizio: report, never auto-fix.
WATCH = [
    (r"\bseed\b|\bround\b|investment round|raccolta di capitali|valutazione pre.?money", "funding wording"),
    (r"\bequity\b|quote societarie|capitale sociale|azionist|shareholder|soci fondatori|cap table", "ownership wording"),
    (r"centro consorzi|confindustria|universit|\bbanca\b|\bbank\b|\bfondazione\b|\bfoundation\b", "named partner or partner type"),
    (r"\b20(2[7-9]|3\d)\b", "future date or year"),
]
SECRETS = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|github_pat_|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-|api[_-]?key\s*[:=]\s*\S{8,}|password\s*[:=]\s*\S+", re.I)

errors, warnings = [], []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.srcs, self.tags, self.title, self.h1 = [], [], [], "", 0
        self.alternates, self.lang, self.text = {}, "", []
        self._title = False
        self._skip = 0
        self.inline_style = self.handlers = 0
        self.imgs_no_alt = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "alternate":
            self.alternates[a.get("hreflang", "")] = a.get("href", "")
        elif tag == "link" and a.get("href"):
            self.srcs.append(a["href"])
        for k in ("src", "poster", "data"):
            if a.get(k):
                self.srcs.append(a[k])
        if a.get("srcset"):
            self.srcs.extend(part.strip().split()[0] for part in a["srcset"].split(",") if part.strip())
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt += 1
        if "style" in a:
            self.inline_style += 1
        if any(k.startswith("on") for k in a):
            self.handlers += 1
        if tag == "title":
            self._title = True
        if tag == "h1":
            self.h1 += 1
        if tag in ("style", "head"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False
        if tag in ("style", "head"):
            self._skip -= 1

    def handle_data(self, data):
        if self._title:
            self.title += data
        if not self._skip or self._title:
            self.text.append(data)


def host(url):
    return urlparse(url).hostname or ""


def local_target(href, page_path):
    """File in site/ that a local link points to (Cloudflare serves /x for x.html and /dir/ for dir/index.html)."""
    path = href.split("#")[0].split("?")[0]
    base = SITE if path.startswith("/") else page_path.parent
    t = (base / path.lstrip("/")).resolve()
    for cand in (t, t / "index.html", t.with_name(t.name + ".html")):
        if cand.is_file() and SITE.resolve() in cand.parents:
            return cand
    return None


# ---- files in site/
for f in SITE.rglob("*"):
    if f.is_file() and f.suffix.lower() not in ALLOWED_FILES and f.name not in ALLOWED_NAMES:
        errors.append(f"site/{f.relative_to(SITE)}: file type not allowed (needs Fabrizio's approval)")

# ---- secrets anywhere in the repository (it is public)
try:
    tracked = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
except Exception:
    tracked = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
for name in tracked:
    p = ROOT / name
    if p.suffix in {".woff2", ".png", ".jpg", ".jpeg", ".webp", ".ico"} or not p.is_file():
        continue
    if name == "tools/check.py":
        continue
    if SECRETS.search(p.read_text(encoding="utf-8", errors="ignore")):
        errors.append(f"{name}: looks like a secret, key or password. Remove it and tell Fabrizio (the repo is public)")
    if p.name.startswith(".env") or p.suffix in {".pem", ".key"}:
        errors.append(f"{name}: secret-type file committed")

# ---- pages
pages = sorted(SITE.rglob("*.html"))
for page in pages:
    html = page.read_text(encoding="utf-8")
    n = str(page.relative_to(SITE))
    p = Page()
    p.feed(html)
    visible = " ".join(p.text)
    visible_nodraft = re.sub(r'<div class="draft-note">.*?</div></div></section>', "", html, flags=re.S)
    vtext = re.sub(r"<[^>]+>", " ", re.sub(r"<head>.*?</head>", "", visible_nodraft, flags=re.S))

    if not p.title.strip():
        errors.append(f"{n}: missing <title>")
    if p.h1 != 1:
        errors.append(f"{n}: expected exactly one <h1>, found {p.h1}")
    if p.lang not in LANGS:
        errors.append(f"{n}: <html lang> must be one of {sorted(LANGS)}")
    if n.startswith("en/") and p.lang != "en-GB":
        errors.append(f"{n}: English page must have lang=\"en-GB\"")
    if not n.startswith("en/") and p.lang != "it-IT":
        errors.append(f"{n}: Italian page must have lang=\"it-IT\"")
    if n != "404.html":
        for l in ("it", "en", "x-default"):
            if l not in p.alternates:
                errors.append(f"{n}: missing hreflang alternate '{l}' (every page exists in Italian and English)")
    for t in sorted(set(p.tags) & FORBIDDEN_TAGS):
        errors.append(f"{n}: <{t}> is not allowed (no scripts, embeds, inline SVG or forms without Fabrizio's approval)")
    if p.inline_style:
        errors.append(f"{n}: {p.inline_style} inline style attribute(s); the CSP blocks them, use site.css")
    if "<style" in html:
        errors.append(f"{n}: <style> block; the CSP blocks it, use site.css")
    if p.handlers:
        errors.append(f"{n}: inline event handler(s) (onclick etc.) are not allowed")
    if p.imgs_no_alt:
        errors.append(f"{n}: {p.imgs_no_alt} image(s) without alt text")
    if re.search(r"javascript:", html, re.I):
        errors.append(f"{n}: javascript: URL")

    for href in p.links:
        if href.startswith("#"):
            continue
        if href.startswith("mailto:"):
            addr = href[7:].split("?")[0].lower()
            if addr not in EMAILS:
                errors.append(f"{n}: email address not approved -> {addr} (check spelling: {', '.join(EMAILS)})")
            continue
        if href.startswith(("http://", "https://", "//")):
            if href.startswith("http://"):
                errors.append(f"{n}: insecure http link -> {href}")
            if host(href) not in LINK_DOMAINS:
                errors.append(f"{n}: link to unapproved domain {host(href) or href} (add to LINK_DOMAINS only with Fabrizio's approval)")
            continue
        if ":" in href.split("#")[0]:
            errors.append(f"{n}: unexpected link form -> {href}")
            continue
        if href.split("#")[0] and not local_target(href, page):
            errors.append(f"{n}: broken internal link -> {href}")

    for src in p.srcs:
        if src.startswith(("http://", "https://", "//")):
            errors.append(f"{n}: external resource -> {src} (everything is self-hosted)")
        elif not local_target(src, page):
            errors.append(f"{n}: missing local file -> {src}")

    for addr in set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", visible)):
        if addr.lower() not in EMAILS:
            errors.append(f"{n}: email address not approved -> {addr}")
    if re.search(r"Deliberali|De Liberali", visible):
        errors.append(f"{n}: name must be written 'Fabrizio de Liberali' (lowercase de, two words)")
    if re.search(r"(\+44|\+39|\b0)\s?\d{2,4}[\s-]?\d{3}[\s-]?\d{3,4}\b", visible):
        errors.append(f"{n}: looks like a phone number; never publish phone numbers")
    if re.search(r"—|&mdash;|\s–\s|&ndash;", html):
        errors.append(f"{n}: em or en dash used as punctuation; use a comma, colon or full stop")
    if re.search(r"generatepress|wp-content|wordpress|\[contact", html, re.I):
        errors.append(f"{n}: leftover WordPress content")
    if re.search(r"impresefarolose", html, re.I):
        errors.append(f"{n}: misspelt domain 'impresefarolose'")

    for pattern, why in CLAIMS + NUMBERS:
        m = re.search(pattern, vtext, re.I)
        if m:
            errors.append(f"{n}: {why}: '{m.group(0)}'")
    for pattern, why in WATCH:
        m = re.search(pattern, vtext, re.I)
        if m:
            warnings.append(f"{n}: {why} ('{m.group(0)}'), Fabrizio to confirm")

    if 'class="draft-note"' in html:
        errors.append(f"{n}: draft questions still on the page; answer them in tools/content.py before merging")
    if 'name="robots" content="noindex, nofollow"' not in html:
        errors.append(f"{n}: noindex removed; allowed only at the domain switch, with Fabrizio's approval")

# ---- Cloudflare files
headers = (SITE / "_headers").read_text(encoding="utf-8") if (SITE / "_headers").exists() else ""
for h in REQUIRED_HEADERS:
    if h not in headers:
        errors.append(f"_headers: missing or weakened security rule: {h}")
if "script-src" in headers or "unsafe-" in headers:
    errors.append("_headers: scripts or unsafe CSP keywords are not allowed")

redirects = (SITE / "_redirects").read_text(encoding="utf-8") if (SITE / "_redirects").exists() else ""
actual = {" ".join(l.split()) for l in redirects.splitlines() if l.strip() and not l.startswith("#")}
if actual != EXPECTED_REDIRECTS:
    errors.append(f"_redirects changed: {sorted(actual ^ EXPECTED_REDIRECTS)} (needs Fabrizio's approval and an update here)")

for w in sorted(set(warnings)):
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(pages)} pages checked, {len(errors)} errors, {len(set(warnings))} warnings")
sys.exit(1 if errors else 0)
