# Imprese Favolose website

Static site for [impresefavolose.it](https://impresefavolose.it), published by Cloudflare Pages.
Italian at the site root, English under `en/`.

- Words (both languages): `tools/content.py`
- Pages: `python3 tools/build.py` → output in `site/`
- Style: `site/assets/site.css`
- Health check: `python3 tools/check.py`
- Rules for Claude: `CLAUDE.md`

**Cloudflare Pages settings:** framework preset *None*, build command *(empty)*, build output directory `site`.
