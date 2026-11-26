# Tooth & Nail Tattoo Parlour

Static website for **Tooth & Nail Tattoo Parlour** (484 Cherry St, downtown Macon, GA), built from a single JSON source of truth (`data/shop.json`) into clean, zero-dependency HTML, CSS, and vanilla JavaScript.

## Structure & Workflow

- `data/shop.json` — Single source of truth for studio NAP, hours, services, all 8 resident artists, portfolio metadata, FAQs, and aftercare instructions.
- `build.py` — Generates all 14 static HTML pages (with connected Schema.org `@graph` JSON-LD), `sitemap.xml`, `robots.txt`, `llms.txt`, and `llms-full.txt`.
- `scripts/process_assets.py` — Extracts clean transparency on `images/logo.png`, optimizes WebP variants, and generates `images/og.jpg`.
- `css/styles.css` & `js/site.js` — Dark heritage tattoo parlour styling, live Macon (`America/New_York`) open/closed badge, gallery style filter + lightbox, and consult request summary builder.

## Rebuilding Locally

```bash
python3 build.py
python3 -m http.server 8765
```

All internal links use relative paths so the site works cleanly at `/` on a custom domain (`tntparlour.com`) or under `/tntparlour/` on GitHub Pages.
