#!/usr/bin/env python3
"""
Static site generator for Tooth & Nail Tattoo Parlour.
Reads data/shop.json and writes all HTML pages (borderless dark editorial layout),
sitemap.xml, robots.txt, llms.txt, and llms-full.txt.
"""

import hashlib
import html
import json
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "shop.json").read_text(encoding="utf-8"))
TODAY = date.today().isoformat()


def asset_hash(rel_path):
    p = ROOT / rel_path
    if not p.exists():
        return "1"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:8]


def e(val):
    return html.escape(str(val), quote=True)


def json_script(obj):
    raw = json.dumps(obj, indent=2, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{raw}\n</script>'


def shop_entity():
    base = DATA["siteUrl"].rstrip("/")
    addr = DATA["address"]
    return {
        "@type": ["TattooParlor", "LocalBusiness"],
        "@id": f"{base}/#shop",
        "name": DATA["name"],
        "description": (
            "Tattoo and body piercing parlour at 484 Cherry Street in downtown Macon, Georgia. "
            "Eight resident artists serving Macon and Middle Georgia for over a decade. "
            "Walk-ins welcome Tuesday through Saturday alongside custom consultations. "
            "Licensed by the Macon-Bibb County Board of Health."
        ),
        "url": f"{base}/",
        "image": f"{base}/images/og.jpg",
        "logo": f"{base}/images/logo.png",
        "telephone": DATA["phoneHref"],
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": addr["street"],
            "addressLocality": addr["city"],
            "addressRegion": addr["state"],
            "postalCode": addr["zip"],
            "addressCountry": addr["country"],
        },
        "areaServed": [{"@type": "City", "name": area} for area in DATA["areasServed"]],
        "hasMap": DATA["mapsUrl"],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": h["days"],
                "opens": h["opens"],
                "closes": h["closes"],
            }
            for h in DATA["hours"]
            if h["days"]
        ],
        "founder": [
            {"@id": f"{base}/#artist-kevin-dixon"},
            {"@id": f"{base}/#artist-greasy-dreams"},
        ],
        "employee": [{"@id": f"{base}/#artist-{a['slug']}"} for a in DATA["artists"]],
        "knowsAbout": [
            "Custom Tattoos",
            "Walk-In Tattoos",
            "Cover-Up Tattoos",
            "Body Piercing",
            "Curated Ear Styling",
            "Color Anime & Gaming Tattoos",
            "Neo-Traditional Tattoos",
            "American Traditional Tattoos",
            "Fine Line & Ornamental Tattoos",
            "Black & Grey Realism & Pet Portraits",
            "Tattoo Aftercare",
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Tattoo & Piercing Services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": s["name"],
                        "description": s["summary"],
                    },
                }
                for s in DATA["services"]
            ],
        },
        "sameAs": [DATA["social"]["instagram"], DATA["social"]["facebook"]],
    }


def website_entity():
    base = DATA["siteUrl"].rstrip("/")
    return {
        "@type": "WebSite",
        "@id": f"{base}/#website",
        "url": f"{base}/",
        "name": DATA["name"],
        "publisher": {"@id": f"{base}/#shop"},
    }


def breadcrumb_entity(url, crumbs):
    base = DATA["siteUrl"].rstrip("/")
    return {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": label,
                "item": f"{base}/{path.lstrip('/')}" if path else f"{base}/",
            }
            for idx, (label, path) in enumerate(crumbs)
        ],
    }


def artist_person_entity(artist):
    base = DATA["siteUrl"].rstrip("/")
    node = {
        "@type": "Person",
        "@id": f"{base}/#artist-{artist['slug']}",
        "name": artist["displayName"],
        "jobTitle": artist["role"],
        "description": artist["bio"],
        "url": f"{base}/artists/{artist['slug']}.html",
        "worksFor": {"@id": f"{base}/#shop"},
        "knowsAbout": artist["styles"],
        "sameAs": [artist["instagram"]],
    }
    if artist["handle"] != artist["displayName"]:
        node["alternateName"] = artist["handle"]
    return node


def render_head(
    *,
    title,
    description,
    canonical_url,
    prefix="",
    graph=None,
    noindex=False,
    preload_hero=False,
):
    base = DATA["siteUrl"].rstrip("/")
    og_img = f"{base}/images/og.jpg"
    robots_tag = (
        '<meta name="robots" content="noindex, follow">'
        if noindex
        else '<meta name="robots" content="index, follow, max-image-preview:large">'
    )
    canonical_tag = "" if noindex else f'<link rel="canonical" href="{e(canonical_url)}">'
    preload_tag = (
        f'<link rel="preload" href="{prefix}images/hero-editorial.webp" as="image" type="image/webp">'
        if preload_hero
        else ""
    )
    schema_block = json_script({"@context": "https://schema.org", "@graph": graph}) if graph else ""
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  {robots_tag}
  {canonical_tag}
  <meta name="theme-color" content="#070707">
  <meta property="og:site_name" content="{e(DATA['name'])}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{e(canonical_url)}">
  <meta property="og:image" content="{e(og_img)}">
  <meta property="og:image:alt" content="{e(DATA['name'])} — {e(DATA['address']['street'])}, {e(DATA['address']['city'])}, {e(DATA['address']['state'])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{e(og_img)}">
  <link rel="icon" href="{prefix}favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Pirata+One&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
  {preload_tag}
  <link rel="stylesheet" href="{prefix}css/styles.css?v={asset_hash('css/styles.css')}">
  <script>document.documentElement.classList.replace("no-js","js");</script>
  {schema_block}
</head>"""


def render_header(active_nav, prefix=""):
    def current(key):
        return ' aria-current="page"' if active_nav == key else ""

    body_cls = ' class="home-page"' if active_nav == "home" else ""
    return f"""<body{body_cls}>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{prefix}index.html">
        <picture>
          <source srcset="{prefix}images/logo.webp" type="image/webp">
          <img src="{prefix}images/logo.png" alt="{e(DATA['name'])}" width="400" height="183">
        </picture>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
        <span class="when-closed">Menu</span>
        <span class="when-open">Close</span>
      </button>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
        <a href="{prefix}artists/index.html"{current('artists')}>Artists</a>
        <a href="{prefix}index.html#work">Work</a>
        <a href="{prefix}aftercare.html"{current('aftercare')}>Aftercare</a>
        <a href="{prefix}faq.html"{current('faq')}>FAQ</a>
        <a href="{prefix}book.html" class="nav-book"{current('book')}>Book Consult</a>
      </nav>
      <div class="header-actions">
        <span class="shop-status" data-shop-status><i class="status-mark" aria-hidden="true">&#10022;</i><span class="status-text">Tue–Sat · Cherry St</span></span>
      </div>
    </div>
  </header>"""


def render_closer(prefix=""):
    return f"""  <section class="closer">
    <div class="wrap closer-inner">
      <p class="kicker">484 Cherry St · Downtown Macon, GA</p>
      <h2>Walk In Today or Plan Your Custom Piece.</h2>
      <p class="lede">Stop by Cherry Street Tuesday through Saturday while chairs are open, or send your concept ahead of time so we can match you with the right artist.</p>
      <div class="cta-row">
        <a class="btn" href="{prefix}book.html">Book a Consult</a>
        <a class="btn btn-ghost" href="tel:{e(DATA['phoneHref'])}">Call {e(DATA['phoneDisplay'])}</a>
      </div>
    </div>
  </section>"""


def render_footer(prefix="", include_lightbox=False):
    area_pills_html = "\n".join(f"          <li>{e(area)}</li>" for area in DATA["areasServed"])

    hours_rows = "\n".join(
        f'          <li><span>{e(h["label"])}</span><strong>{e(h["short"])}</strong></li>'
        for h in DATA["hours"]
    )
    lightbox_html = """
  <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-labelledby="lb-title" hidden>
    <div class="lightbox-dialog">
      <div class="lightbox-media">
        <img id="lb-img" src="" alt="">
      </div>
      <div class="lightbox-bar">
        <div class="lightbox-meta">
          <strong id="lb-title"></strong>
          <span id="lb-sub"></span>
        </div>
        <div class="lightbox-controls">
          <button type="button" class="lb-btn" id="lb-prev" aria-label="Previous piece">&larr; Prev</button>
          <button type="button" class="lb-btn" id="lb-next" aria-label="Next piece">Next &rarr;</button>
          <button type="button" class="lb-btn" id="lb-close" aria-label="Close lightbox">Close</button>
        </div>
      </div>
    </div>
  </div>""" if include_lightbox else ""

    return f"""  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div class="footer-brand">
        <picture>
          <source srcset="{prefix}images/logo.webp" type="image/webp">
          <img src="{prefix}images/logo.png" alt="{e(DATA['name'])}" width="400" height="183" loading="lazy">
        </picture>
        <address class="old-english-line" style="margin-bottom:0.4rem;">
          {e(DATA['address']['street'])} · {e(DATA['address']['neighborhood'])}, {e(DATA['address']['state'])} {e(DATA['address']['zip'])}
        </address>
        <p><a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a></p>
      </div>
      <div>
        <p class="footer-heading">Hours</p>
        <ul class="hours-list" style="margin:0;">
{hours_rows}
        </ul>
      </div>
      <div>
        <p class="footer-heading">Explore</p>
        <ul class="footer-links">
          <li><a href="{prefix}artists/index.html">Meet the 8 Artists</a></li>
          <li><a href="{prefix}book.html">Request a Consultation</a></li>
          <li><a href="{prefix}aftercare.html">Tattoo Aftercare Guide</a></li>
          <li><a href="{prefix}faq.html">Frequently Asked Questions</a></li>
          <li><a href="{e(DATA['mapsUrl'])}" rel="noopener" target="_blank">Google Maps Directions</a></li>
          <li><a href="{e(DATA['social']['instagram'])}" rel="noopener" target="_blank">Instagram ({e(DATA['social']['instagramHandle'])})</a></li>
          <li><a href="{e(DATA['social']['facebook'])}" rel="noopener" target="_blank">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap footer-bottom">
      <span>{e(DATA['name'])} · Custom Tattoos &amp; Body Piercing in Downtown Macon, GA</span>
      <span>{e(DATA['healthBoard']['authority'])} · {e(DATA['healthBoard']['phoneDisplay'])}</span>
    </div>
  </footer>
  <nav class="dock" aria-label="Quick actions">
    <a href="tel:{e(DATA['phoneHref'])}">Call</a>
    <a href="{e(DATA['mapsUrl'])}" rel="noopener" target="_blank">Directions</a>
    <a class="dock-book" href="{prefix}book.html">Book</a>
  </nav>{lightbox_html}
  <script src="{prefix}js/site.js?v={asset_hash('js/site.js')}" defer></script>
</body>
</html>"""


def render_roster_row(artist, prefix=""):
    if artist["featuredImage"]:
        stem = artist["featuredImage"]
        avatar_html = f"""<picture>
              <source srcset="{prefix}{stem}.webp" type="image/webp">
              <img class="roster-avatar" src="{prefix}{stem}.jpg" alt="{e(artist['displayName'])}" width="108" height="108" loading="lazy" decoding="async">
            </picture>"""
    else:
        avatar_html = f'<span class="roster-monogram" aria-hidden="true">{e(artist.get("monogram", "TN"))}</span>'

    meta_text = f"{artist['role']} · {' · '.join(artist['styles'][:2])}"
    book_q = quote(artist["displayName"])
    if artist.get("bookingUrl"):
        primary_action = f'<a class="btn btn-sm btn-ghost" href="{e(artist["bookingUrl"])}" rel="noopener" target="_blank">Book Online &#8599;</a>'
    elif artist.get("bookingEmail"):
        primary_action = f'<a class="btn btn-sm btn-ghost" href="mailto:{e(artist["bookingEmail"])}">Email to Book</a>'
    else:
        primary_action = f'<a class="btn btn-sm btn-ghost" href="{prefix}book.html?artist={book_q}">Request Seat</a>'

    return f"""        <li class="roster-row">
          <div class="roster-inner">
            <span class="roster-num">{e(artist['number'])}</span>
            <div class="roster-main">
              {avatar_html}
              <a class="roster-name" href="{prefix}artists/{e(artist['slug'])}.html">{e(artist['displayName'])}</a>
            </div>
            <span class="roster-meta">{e(meta_text)}</span>
            <div class="roster-links">
              <a class="text-link" href="{prefix}artists/{e(artist['slug'])}.html">Portfolio &rarr;</a>
              {primary_action}
            </div>
          </div>
        </li>"""


def render_breadcrumbs(crumbs, prefix=""):
    items = []
    for i, (label, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{e(label)}</li>')
        else:
            href = f"{prefix}{path}" if path else f"{prefix}index.html"
            items.append(f'<li><a href="{href}">{e(label)}</a></li>')
    return f'<ol class="breadcrumbs">{"".join(items)}</ol>'


def build_index():
    base = DATA["siteUrl"].rstrip("/")
    url = f"{base}/"
    graph = [
        shop_entity(),
        website_entity(),
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": "Tooth & Nail Tattoo Parlour | Custom Tattoos & Piercings in Macon, GA",
            "description": (
                "Tooth & Nail Tattoo Parlour at 484 Cherry St in downtown Macon, GA. "
                "Eight resident artists, over 10 years in business, walk-in tattoos, custom work, and body piercings. Call (478) 259-1829."
            ),
            "isPartOf": {"@id": f"{base}/#website"},
            "about": {"@id": f"{base}/#shop"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        breadcrumb_entity(url, [("Home", "")]),
    ] + [artist_person_entity(a) for a in DATA["artists"]]

    showcase_tiles = "\n".join(
        f"""        <figure class="work-tile" data-category="{e(p['category'])}">
          <button type="button" class="work-trigger" data-lightbox-src="{p['path']}.webp" data-lightbox-alt="{e(p['alt'])}" data-lightbox-title="{e(p['title'])}" data-lightbox-sub="{e(p['artist'])} · {e(p['categoryLabel'])}">
            <picture>
              <source srcset="{p['path']}.webp" type="image/webp">
              <img src="{p['path']}.jpg" alt="{e(p['alt'])}" width="{p['width']}" height="{p['height']}" loading="lazy" decoding="async">
            </picture>
            <span class="tile-overlay">
              <strong>{e(p['title'])}</strong>
              <span>{e(p['artist'])} · {e(p['categoryLabel'])}</span>
            </span>
          </button>
        </figure>"""
        for p in DATA["portfolio"]["homeShowcase"]
    )

    roster_html = "\n".join(render_roster_row(a, prefix="") for a in DATA["artists"])

    area_pills_html = "\n".join(f"          <li>{e(area)}</li>" for area in DATA["areasServed"])

    hours_rows = "\n".join(
        f'            <li data-hours-row="{"tue-thu" if "Tue" in h["label"] else ("fri-sat" if "Fri" in h["label"] else "sun-mon")}"><span>{e(h["label"])}</span><strong>{e(h["display"])}</strong></li>'
        for h in DATA["hours"]
    )

    html_doc = "\n".join(
        [
            render_head(
                title="Tooth & Nail Tattoo Parlour | Custom Tattoos & Piercings in Macon, GA",
                description=(
                    "Tooth & Nail Tattoo Parlour at 484 Cherry St in downtown Macon, GA. "
                    "Eight resident artists, over 10 years in business, walk-ins welcome, custom tattoos, and body piercings. Call (478) 259-1829."
                ),
                canonical_url=url,
                prefix="",
                graph=graph,
                preload_hero=True,
            ),
            render_header("home", prefix=""),
            f"""  <main id="main">
    <section class="hero">
      <div class="hero-backdrop" aria-hidden="true">
        <picture>
          <source srcset="images/hero-editorial.webp" type="image/webp">
          <img src="images/hero-editorial.jpg" alt="" width="1376" height="768" fetchpriority="high">
        </picture>
      </div>
      <div class="wrap hero-main">
        <div class="hero-copy">
          <p class="hero-address">484 Cherry St · Downtown Macon, GA</p>
          <h1 class="hero-logo-wrap" id="hero-logo">
            <picture>
              <source srcset="images/logo-hero.webp" type="image/webp">
              <img src="images/logo-hero.png" alt="Tooth &amp; Nail Tattoo Parlour — Custom Tattoos &amp; Body Piercings in Downtown Macon, GA" width="960" height="439" fetchpriority="high">
            </picture>
          </h1>
          <p class="lede">Custom tattoos, walk-in flash, and clean body piercing on Cherry Street. Eight resident artists serving Macon and Middle Georgia for over a decade.</p>
          <div class="hero-actions">
            <a class="btn" href="book.html">Book a Consult</a>
            <a class="btn btn-ghost" href="tel:{e(DATA['phoneHref'])}">Call {e(DATA['phoneDisplay'])}</a>
            <div class="social-circles" aria-label="Social and Map links">
              <a class="social-circle" href="{e(DATA['social']['instagram'])}" rel="noopener" target="_blank" aria-label="Instagram @tntparlour">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
              </a>
              <a class="social-circle" href="{e(DATA['social']['facebook'])}" rel="noopener" target="_blank" aria-label="Facebook">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
              </a>
              <a class="social-circle" href="{e(DATA['mapsUrl'])}" rel="noopener" target="_blank" aria-label="Google Maps Directions">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="wrap hero-stats">
        <div class="hero-stat">
          <strong>4.9 &#9733;</strong>
          <span>Google Rating</span>
        </div>
        <div class="hero-stat">
          <strong>10+ Years</strong>
          <span>On Cherry Street</span>
        </div>
        <div class="hero-stat">
          <strong>8 Artists</strong>
          <span>Resident Crew</span>
        </div>
        <div class="hero-stat">
          <strong>Walk-Ins</strong>
          <span>Welcome Tue–Sat</span>
        </div>
      </div>
    </section>

    <section class="triptych-band" aria-label="Services Overview">
      <a class="panel-tile" href="book.html">
        <picture>
          <source srcset="images/work-kidbuu.webp" type="image/webp">
          <img src="images/work-kidbuu.jpg" alt="Full-color custom anime tattoo by Kevin Dixon" width="1400" height="1400" loading="lazy" decoding="async">
        </picture>
        <div class="panel-content">
          <span class="panel-tag">01 · By Consultation</span>
          <h2>Custom Tattoos &amp; Cover-Ups</h2>
          <p>One-of-a-kind sleeves, color anime, traditional, blackwork, and thoughtful reworks.</p>
        </div>
      </a>
      <a class="panel-tile" href="#work">
        <picture>
          <source srcset="images/strip-flash.webp" type="image/webp">
          <img src="images/strip-flash.jpg" alt="Classic framed American Traditional tattoo flash wall" width="1000" height="750" loading="lazy" decoding="async">
        </picture>
        <div class="panel-content">
          <span class="panel-tag">02 · Tue–Sat While Open</span>
          <h2>Walk-Ins &amp; Classic Flash</h2>
          <p>Spontaneous Cherry Street pieces, palm-sized flash, and crisp script whenever a chair is free.</p>
        </div>
      </a>
      <a class="panel-tile" href="faq.html">
        <picture>
          <source srcset="images/strip-piercing.webp" type="image/webp">
          <img src="images/strip-piercing.jpg" alt="Minimalist surgical steel and gold body piercing jewelry" width="1000" height="750" loading="lazy" decoding="async">
        </picture>
        <div class="panel-content">
          <span class="panel-tag">03 · Sterile Studio Care</span>
          <h2>Body Piercing</h2>
          <p>Clean, single-use body piercings in downtown Macon. Call (478) 259-1829 for daily availability.</p>
        </div>
      </a>
    </section>

    <div class="curve-divider curve-overlap-top" aria-hidden="true">
      <svg viewBox="0 0 1440 96" preserveAspectRatio="none">
        <path d="M0,6 C430,86 980,82 1440,22 L1440,96 L0,96 Z" fill="#d48614"></path>
        <path d="M0,26 C460,94 1000,84 1440,24 L1440,96 L0,96 Z" fill="#f2eadc"></path>
      </svg>
    </div>

    <section class="parchment-band" aria-label="Serving Macon and Middle Georgia">
      <div class="wrap parchment-inner">
        <p class="kicker">Cherry Street Roots · Regional Reputation</p>
        <h2>Proudly Tattooing Middle Georgia.</h2>
        <p>From first-time walk-ins to full custom sleeves, collectors make the drive to 484 Cherry St in downtown Macon from across Central Georgia:</p>
        <ul class="area-pills">
{area_pills_html}
        </ul>
      </div>
    </section>

    <div class="curve-divider" style="background:#f2eadc; margin-top:-1px;" aria-hidden="true">
      <svg viewBox="0 0 1440 96" preserveAspectRatio="none">
        <path d="M0,78 C460,12 980,8 1440,58 L1440,96 L0,96 Z" fill="#c97d10"></path>
        <path d="M0,80 C450,16 960,22 1440,78 L1440,96 L0,96 Z" fill="#0c0b0a"></path>
      </svg>
    </div>

    <section class="editorial-split" id="about">
      <div class="split-media">
        <picture>
          <source srcset="images/hero-bg.webp" type="image/webp">
          <img src="images/hero-bg.jpg" alt="Warm Edison bulb illuminating framed traditional flash on Tooth &amp; Nail's dark brick wall" width="1376" height="768" loading="lazy" decoding="async">
        </picture>
      </div>
      <div class="split-copy">
        <p class="kicker">Over a Decade on Cherry Street</p>
        <h2>Who We Are.</h2>
        <p>10+ years downtown, eight very different artists under one roof, zero shop-snob attitude whether it's your first walk-in flash piece or a multi-session custom sleeve.</p>
        <div class="cta-row" style="margin-top:1rem;">
          <a class="btn btn-sm btn-ghost" href="artists/index.html">Meet the Artists</a>
          <a class="btn btn-sm btn-ghost" href="faq.html">Shop FAQ</a>
        </div>
      </div>
    </section>

    <section class="section section-glow" id="work">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="kicker">From the Parlour</p>
            <h2>Recent Work.</h2>
          </div>
          <p class="lede">Click any piece to inspect linework and saturation in full screen, or browse each artist's Instagram for daily healed and fresh uploads.</p>
        </div>
        <div class="filter-bar" role="group" aria-label="Filter gallery by style">
          <button type="button" class="filter-btn is-active" data-filter="all" aria-pressed="true">All Work</button>
          <button type="button" class="filter-btn" data-filter="color-traditional" aria-pressed="false">Color &amp; Traditional</button>
          <button type="button" class="filter-btn" data-filter="black-grey" aria-pressed="false">Black &amp; Grey &amp; Realism</button>
          <button type="button" class="filter-btn" data-filter="fineline-piercing" aria-pressed="false">Fine Line &amp; Piercing</button>
        </div>
        <div class="gallery-wall">
{showcase_tiles}
        </div>
      </div>
    </section>

    <section class="section" id="artists">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="kicker">The Roster</p>
            <h2>Eight Resident Artists.</h2>
          </div>
          <p class="lede">Explore individual artist profiles, check their latest flash and custom work on Instagram, or request a specific seat directly.</p>
        </div>
        <ol class="roster-editorial">
{roster_html}
        </ol>
      </div>
    </section>

    <section class="section visit-band" id="visit">
      <div class="wrap">
        <div class="visit-open-grid">
          <div>
            <p class="kicker">Hours &amp; Walk-Ins</p>
            <h2>Open Five Days.</h2>
            <p><span class="shop-status" data-shop-status><i class="status-mark" aria-hidden="true">&#10022;</i><span class="status-text">Tue–Thu 1–8 PM · Fri–Sat 1–10 PM</span></span></p>
            <ul class="hours-list">
{hours_rows}
            </ul>
            <p class="muted">Walk-ins are welcome Tuesday through Saturday whenever a chair is open. Call <a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a> for real-time walk-in and piercer availability.</p>
          </div>
          <div class="visit-col-right">
            <p class="kicker">Find the Parlour</p>
            <h2>484 Cherry St, Macon.</h2>
            <p class="muted">Right on downtown Macon's Cherry Street corridor (GA 31201), minutes from Mercer University with convenient street parking along Cherry St and surrounding downtown blocks.</p>
            <div class="cta-row">
              <a class="btn btn-sm" href="{e(DATA['mapsUrl'])}" rel="noopener" target="_blank">Google Maps Directions</a>
              <a class="btn btn-sm btn-ghost" href="{e(DATA['social']['instagram'])}" rel="noopener" target="_blank">@tntparlour</a>
            </div>
            <div class="map-minimal">
              <iframe title="Map showing Tooth &amp; Nail Tattoo Parlour at 484 Cherry St, Macon, GA" src="{e(DATA['mapsEmbedUrl'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
          </div>
        </div>

        <dl class="facts-strip" aria-label="Studio Quick Facts">
          <div>
            <dt>Studio &amp; Owners</dt>
            <dd>{e(DATA['name'])} · {e(DATA['owner'])}</dd>
          </div>
          <div>
            <dt>Address &amp; Phone</dt>
            <dd>484 Cherry St, Macon, GA 31201 · <a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a></dd>
          </div>
          <div>
            <dt>Services</dt>
            <dd>Custom tattoos, walk-in flash, cover-ups &amp; body piercing</dd>
          </div>
          <div>
            <dt>Service Area</dt>
            <dd>Downtown Macon, Mercer Univ., Warner Robins, Forsyth &amp; Middle GA</dd>
          </div>
        </dl>
      </div>
    </section>

{render_closer(prefix="")}
  </main>""",
            render_footer(prefix="", include_lightbox=True),
        ]
    )
    (ROOT / "index.html").write_text(html_doc, encoding="utf-8")


def build_artists_index():
    base = DATA["siteUrl"].rstrip("/")
    url = f"{base}/artists/"
    graph = [
        shop_entity(),
        website_entity(),
        {
            "@type": "CollectionPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": "Tattoo Artists in Macon, GA | Tooth & Nail Tattoo Parlour",
            "description": (
                "Meet the eight resident artists at Tooth & Nail Tattoo Parlour on Cherry Street in downtown Macon, GA. "
                "Browse portfolios, Instagram handles, and book a consult."
            ),
            "isPartOf": {"@id": f"{base}/#website"},
            "about": {"@id": f"{base}/#shop"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": idx + 1,
                        "url": f"{base}/artists/{a['slug']}.html",
                        "name": a["displayName"],
                    }
                    for idx, a in enumerate(DATA["artists"])
                ],
            },
        },
        breadcrumb_entity(url, [("Home", ""), ("Artists", "artists/")]),
    ] + [artist_person_entity(a) for a in DATA["artists"]]

    roster_html = "\n".join(render_roster_row(a, prefix="../") for a in DATA["artists"])

    html_doc = "\n".join(
        [
            render_head(
                title="Tattoo Artists in Macon, GA | Tooth & Nail Tattoo Parlour",
                description=(
                    "Meet the eight resident tattoo artists at Tooth & Nail Tattoo Parlour in downtown Macon, GA. "
                    "Explore work, Instagram portfolios, and request your artist."
                ),
                canonical_url=url,
                prefix="../",
                graph=graph,
            ),
            render_header("artists", prefix="../"),
            f"""  <main id="main">
    <section class="page-header">
      <div class="wrap">
        {render_breadcrumbs([("Home", ""), ("Artists", "artists/")], prefix="../")}
        <p class="kicker">484 Cherry St · Resident Crew</p>
        <h1>Eight Resident Artists.</h1>
        <p class="lede">Led by owner Kevin Dixon, our eight-chair studio covers saturated full-color anime and gaming pieces, classic American traditional, blackwork, and custom tattoos in downtown Macon.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <ol class="roster-editorial">
{roster_html}
        </ol>
      </div>
    </section>

{render_closer(prefix="../")}
  </main>""",
            render_footer(prefix="../"),
        ]
    )
    (ROOT / "artists" / "index.html").write_text(html_doc, encoding="utf-8")


def build_artist_pages():
    base = DATA["siteUrl"].rstrip("/")
    all_work = DATA["portfolio"]["allArtistWorks"]

    for artist in DATA["artists"]:
        url = f"{base}/artists/{artist['slug']}.html"
        person = artist_person_entity(artist)
        graph = [
            shop_entity(),
            website_entity(),
            person,
            {
                "@type": "ProfilePage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": f"{artist['displayName']} ({artist['handle']}) | Tooth & Nail Tattoo Parlour",
                "description": (
                    f"{artist['displayName']} ({artist['handle']}) — {artist['role']} at Tooth & Nail Tattoo Parlour, "
                    f"484 Cherry St, Macon, GA. {artist['bio']}"
                ),
                "isPartOf": {"@id": f"{base}/#website"},
                "mainEntity": {"@id": person["@id"]},
                "breadcrumb": {"@id": f"{url}#breadcrumb"},
            },
            breadcrumb_entity(
                url,
                [("Home", ""), ("Artists", "artists/"), (artist["displayName"], f"artists/{artist['slug']}.html")],
            ),
        ]

        tags_html = "".join(f"<li>{e(s)}</li>" for s in artist["styles"])
        artist_works = [w for w in all_work if w.get("artistSlug") == artist["slug"]]

        if artist.get("bookingUrl"):
            book_primary = f'<a class="btn" href="{e(artist["bookingUrl"])}" rel="noopener" target="_blank">Book Online &#8599;</a>'
            book_secondary = f'<a class="btn btn-ghost" href="../book.html?artist={quote(artist["displayName"])}">Shop Consult Form</a>'
        elif artist.get("bookingEmail"):
            book_primary = f'<a class="btn" href="mailto:{e(artist["bookingEmail"])}">Email {e(artist["bookingEmail"])}</a>'
            book_secondary = f'<a class="btn btn-ghost" href="../book.html?artist={quote(artist["displayName"])}">Shop Consult Form</a>'
        else:
            book_primary = f'<a class="btn" href="../book.html?artist={quote(artist["displayName"])}">Request {e(artist["displayName"])}</a>'
            book_secondary = ""

        booking_note_html = f'<p class="muted" style="margin-top:-0.4rem; margin-bottom:1.35rem;">{e(artist["bookingNote"])}</p>' if artist.get("bookingNote") else ""

        if artist_works:
            cols_cls = " cols-3" if len(artist_works) % 3 == 0 and len(artist_works) != 4 else ""
            work_tiles = "\n".join(
                f"""          <figure class="work-tile">
            <button type="button" class="work-trigger" data-lightbox-src="../{w['path']}.webp" data-lightbox-alt="{e(w['alt'])}" data-lightbox-title="{e(w['title'])}" data-lightbox-sub="{e(artist['displayName'])} · {e(w['categoryLabel'])}">
              <picture>
                <source srcset="../{w['path']}.webp" type="image/webp">
                <img src="../{w['path']}.jpg" alt="{e(w['alt'])}" width="{w['width']}" height="{w['height']}" loading="lazy" decoding="async">
              </picture>
              <span class="tile-overlay">
                <strong>{e(w['title'])}</strong>
                <span>{e(w['categoryLabel'])}</span>
              </span>
            </button>
          </figure>"""
                for w in artist_works
            )
            gallery_section = f"""
    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="kicker">Portfolio</p>
            <h2>Work by {e(artist['displayName'])}.</h2>
          </div>
          <a class="text-link" href="{e(artist['instagram'])}" rel="noopener" target="_blank">More on {e(artist['handle'])} &#8599;</a>
        </div>
        <div class="artist-portfolio-wall{cols_cls}">
{work_tiles}
        </div>
      </div>
    </section>"""
        else:
            gallery_section = f"""
    <section class="section">
      <div class="wrap">
        <p class="kicker">Direct Booking &amp; Portfolio</p>
        <h2>Connect With {e(artist['displayName'])}.</h2>
        <p class="lede">Follow {e(artist['handle'])} on Instagram or email <a href="mailto:{e(artist.get('bookingEmail', ''))}">{e(artist.get('bookingEmail', ''))}</a> directly to discuss custom tattoo concepts and scheduling at 484 Cherry St.</p>
        <div class="cta-row" style="margin-top:1.5rem;">
          <a class="btn" href="{e(artist['instagram'])}" rel="noopener" target="_blank">Instagram {e(artist['handle'])} &#8599;</a>
          <a class="btn btn-ghost" href="../book.html?artist={quote(artist['displayName'])}">Request {e(artist['displayName'])}</a>
        </div>
      </div>
    </section>"""

        html_doc = "\n".join(
            [
                render_head(
                    title=f"{artist['displayName']} ({artist['handle']}) | Tooth & Nail Tattoo Parlour",
                    description=(
                        f"{artist['displayName']} ({artist['handle']}) — {artist['role']} at Tooth & Nail Tattoo Parlour in Macon, GA. "
                        f"{artist['bio']}"
                    ),
                    canonical_url=url,
                    prefix="../",
                    graph=graph,
                ),
                render_header("artists", prefix="../"),
                f"""  <main id="main">
    <section class="page-header">
      <div class="wrap">
        {render_breadcrumbs([("Home", ""), ("Artists", "artists/"), (artist["displayName"], f"artists/{artist['slug']}.html")], prefix="../")}
        <p class="kicker">{e(artist['role'])} · {e(artist['handle'])}</p>
        <h1>{e(artist['displayName'])}</h1>
        <p class="lede">{e(artist['bio'])}</p>
        <ul class="tag-row">{tags_html}</ul>
        {booking_note_html}
        <div class="cta-row">
          {book_primary}
          {book_secondary}
          <a class="btn btn-ghost" href="{e(artist['instagram'])}" rel="noopener" target="_blank">Instagram {e(artist['handle'])}</a>
          <a class="text-link" href="index.html">&larr; All 8 Artists</a>
        </div>
      </div>
    </section>
{gallery_section}
{render_closer(prefix="../")}
  </main>""",
                render_footer(prefix="../", include_lightbox=bool(artist_works)),
            ]
        )
        (ROOT / "artists" / f"{artist['slug']}.html").write_text(html_doc, encoding="utf-8")


def build_book():
    base = DATA["siteUrl"].rstrip("/")
    url = f"{base}/book.html"
    graph = [
        shop_entity(),
        website_entity(),
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": "Book a Tattoo Consult | Tooth & Nail Tattoo Parlour (Macon, GA)",
            "description": (
                "Request a custom tattoo or walk-in consultation at Tooth & Nail Tattoo Parlour, 484 Cherry St, downtown Macon, GA. "
                "Call (478) 259-1829 for same-day chair availability."
            ),
            "isPartOf": {"@id": f"{base}/#website"},
            "about": {"@id": f"{base}/#shop"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        breadcrumb_entity(url, [("Home", ""), ("Book Consult", "book.html")]),
    ]

    artist_options = "\n".join(
        f'                <option value="{e(a["displayName"])}">{e(a["displayName"])}</option>'
        for a in DATA["artists"]
    )

    html_doc = "\n".join(
        [
            render_head(
                title="Book a Tattoo Consult | Tooth & Nail Tattoo Parlour (Macon, GA)",
                description=(
                    "Plan your next custom tattoo or check walk-in availability at Tooth & Nail Tattoo Parlour in downtown Macon, GA. "
                    "484 Cherry St · (478) 259-1829."
                ),
                canonical_url=url,
                prefix="",
                graph=graph,
            ),
            render_header("book", prefix=""),
            f"""  <main id="main">
    <section class="page-header">
      <div class="wrap">
        {render_breadcrumbs([("Home", ""), ("Book Consult", "book.html")], prefix="")}
        <p class="kicker">Consultations &amp; Walk-Ins</p>
        <h1>Tell Us About Your Piece.</h1>
        <p class="lede">Share your concept, placement, approximate size, and preferred artist. Looking for a same-day walk-in or piercing? Call <a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a> while we are open.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap booking-layout">
        <div>
          <form
            id="booking-form"
            name="booking"
            method="POST"
            action="book.html"
            enctype="multipart/form-data"
            data-netlify="true"
            netlify-honeypot="bot-field"
          >
            <input type="hidden" name="form-name" value="booking">
            <p class="hp">
              <label>Leave this field empty: <input name="bot-field" tabindex="-1" autocomplete="off"></label>
            </p>
            <div class="form-grid">
              <div class="field">
                <label for="name">Your Name</label>
                <input id="name" name="name" type="text" autocomplete="name" required>
              </div>
              <div class="field">
                <label for="phone">Phone Number</label>
                <input id="phone" name="phone" type="tel" autocomplete="tel" required>
              </div>
              <div class="field">
                <label for="email">Email Address</label>
                <input id="email" name="email" type="email" autocomplete="email" required>
              </div>
              <div class="field">
                <label for="artist">Artist Preference</label>
                <select id="artist" name="artist">
                  <option value="No preference">No preference — match my style</option>
{artist_options}
                  <option value="First available walk-in">First available walk-in chair</option>
                </select>
              </div>
              <div class="field">
                <label for="service">Service Type</label>
                <select id="service" name="service">
                  <option value="Custom Tattoo">Custom Tattoo</option>
                  <option value="Walk-In / Flash">Walk-In / Flash Tattoo</option>
                  <option value="Cover-Up / Rework">Cover-Up or Rework</option>
                  <option value="Body Piercing">Body Piercing Inquiry</option>
                </select>
              </div>
              <div class="field">
                <label for="size">Approximate Size</label>
                <select id="size" name="size" required>
                  <option value="Not sure yet">Not sure yet — advise me</option>
                  <option value="Small (palm-sized or smaller)">Small (palm-sized or smaller)</option>
                  <option value="Medium (hand to forearm/calf)">Medium (hand to forearm/calf)</option>
                  <option value="Large (half sleeve, back, or bigger)">Large (half sleeve, back, or bigger)</option>
                </select>
              </div>
              <div class="field span-2">
                <label for="placement">Body Placement</label>
                <input id="placement" name="placement" type="text" placeholder="Outer forearm, calf, shoulder, ribs..." required>
              </div>
              <div class="field span-2">
                <label for="description">Concept &amp; Details</label>
                <textarea id="description" name="description" required placeholder="Describe your idea, color vs. black &amp; grey, exact spelling for any lettering, and whether it covers an existing tattoo."></textarea>
              </div>
              <div class="field span-2">
                <label for="reference">Reference Image (Optional)</label>
                <input id="reference" name="reference" type="file" accept="image/*">
                <p class="hint">Bring reference images to your consultation or attach them when messaging your artist.</p>
              </div>
            </div>
            <fieldset class="days">
              <legend class="days-legend">Preferred Days</legend>
              <label><input type="checkbox" name="preferred-days" value="Tuesday"> Tue</label>
              <label><input type="checkbox" name="preferred-days" value="Wednesday"> Wed</label>
              <label><input type="checkbox" name="preferred-days" value="Thursday"> Thu</label>
              <label><input type="checkbox" name="preferred-days" value="Friday"> Fri</label>
              <label><input type="checkbox" name="preferred-days" value="Saturday"> Sat</label>
            </fieldset>
            <button class="btn" type="submit">Prepare Consultation Request</button>
          </form>

          <div id="form-fallback" class="fallback" hidden>
            <h3>Your Consultation Summary Is Ready</h3>
            <p class="muted">Copy your formatted request below to message <a href="{e(DATA['social']['instagram'])}" rel="noopener" target="_blank">@tntparlour</a> on Instagram, open an email draft, or call <a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a>.</p>
            <pre id="form-copy"></pre>
            <div class="cta-row">
              <button type="button" class="btn btn-sm" id="copy-request-btn">Copy Request Summary</button>
              <a class="btn btn-sm btn-ghost" id="mailto-link" href="mailto:">Open Email Draft</a>
              <a class="btn btn-sm btn-ghost" href="tel:{e(DATA['phoneHref'])}">Call {e(DATA['phoneDisplay'])}</a>
            </div>
          </div>
        </div>

        <aside class="editorial-notes" aria-label="Booking Information">
          <div class="note-item">
            <p class="kicker">01 · Walk-Ins</p>
            <h3>Same-Day Flash &amp; Small Pieces</h3>
            <p>Smaller flash, script, and walk-in tattoos are welcomed Tuesday through Saturday as chairs open. Custom sleeves and cover-ups start with a consultation.</p>
          </div>
          <div class="note-item">
            <p class="kicker">02 · Quotes &amp; Deposits</p>
            <h3>Straightforward Pricing</h3>
            <p>Every piece is quoted based on size, placement, and detail. Your artist will confirm session pricing and deposit terms directly—never send deposits to unverified accounts.</p>
          </div>
          <div class="note-item">
            <p class="kicker">03 · Identification</p>
            <h3>18+ &amp; Government Photo ID</h3>
            <p>Plan on being 18 or older with a valid, unexpired government-issued photo ID. Call <a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a> beforehand if you have any ID questions.</p>
          </div>
          <div class="note-item">
            <p class="kicker">04 · Studio Desk</p>
            <h3>484 Cherry St, Macon</h3>
            <p>Tue–Thu 1–8 PM · Fri–Sat 1–10 PM<br><a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a> · <a href="{e(DATA['social']['instagram'])}" rel="noopener" target="_blank">@tntparlour</a></p>
          </div>
        </aside>
      </div>
    </section>
  </main>""",
            render_footer(prefix=""),
        ]
    )
    (ROOT / "book.html").write_text(html_doc, encoding="utf-8")


def build_aftercare():
    base = DATA["siteUrl"].rstrip("/")
    url = f"{base}/aftercare.html"

    def howto_node(key, routine):
        return {
            "@type": "HowTo",
            "@id": f"{url}#{key}",
            "name": routine["title"],
            "description": routine["summary"],
            "step": [
                {
                    "@type": "HowToStep",
                    "position": idx + 1,
                    "name": step["name"],
                    "text": step["text"],
                }
                for idx, step in enumerate(routine["steps"])
            ],
        }

    graph = [
        shop_entity(),
        website_entity(),
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": "Tattoo Aftercare Guide | Tooth & Nail Tattoo Parlour (Macon, GA)",
            "description": (
                "Official tattoo healing and aftercare instructions from Tooth & Nail Tattoo Parlour in Macon, GA—covering both Soku second-skin wraps and traditional bandage care."
            ),
            "isPartOf": {"@id": f"{base}/#website"},
            "about": {"@id": f"{base}/#shop"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        breadcrumb_entity(url, [("Home", ""), ("Tattoo Aftercare", "aftercare.html")]),
        howto_node("soku-aftercare", DATA["aftercare"]["soku"]),
        howto_node("traditional-aftercare", DATA["aftercare"]["traditional"]),
    ]

    def render_steps(steps):
        return "\n".join(
            f'            <li><strong>{e(s["name"])}</strong>{e(s["text"])}</li>'
            for s in steps
        )

    soku = DATA["aftercare"]["soku"]
    trad = DATA["aftercare"]["traditional"]

    html_doc = "\n".join(
        [
            render_head(
                title="Tattoo Aftercare Guide | Tooth & Nail Tattoo Parlour (Macon, GA)",
                description=(
                    "Step-by-step tattoo healing instructions from Tooth & Nail Tattoo Parlour in downtown Macon, GA: "
                    "Soku wrap removal, Dial Gold washing, Aquaphor, and unscented lotion."
                ),
                canonical_url=url,
                prefix="",
                graph=graph,
            ),
            render_header("aftercare", prefix=""),
            f"""  <main id="main">
    <section class="page-header">
      <div class="wrap">
        {render_breadcrumbs([("Home", ""), ("Tattoo Aftercare", "aftercare.html")], prefix="")}
        <p class="kicker">Healing &amp; Care</p>
        <h1>Tattoo Aftercare Guide.</h1>
        <p class="lede">Proper healing keeps lines crisp and color saturated for decades. Always prioritize any custom care instructions your artist gives you before leaving 484 Cherry St.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap routine-split">
        <article class="routine-col">
          <p class="kicker">Second-Skin Film</p>
          <h2>{e(soku['title'])}</h2>
          <p class="muted">{e(soku['summary'])}</p>
          <ol class="steps">
{render_steps(soku['steps'])}
          </ol>
        </article>

        <article class="routine-col">
          <p class="kicker">Standard Bandage</p>
          <h2>{e(trad['title'])}</h2>
          <p class="muted">{e(trad['summary'])}</p>
          <ol class="steps">
{render_steps(trad['steps'])}
          </ol>
        </article>
      </div>
    </section>

    <section class="section visit-band">
      <div class="wrap visit-open-grid">
        <div>
          <p class="kicker">Questions During Healing</p>
          <h3>Unsure How Something Is Healing?</h3>
          <p class="muted">Cloudy plasma under a wrap, light flaking, and mild itching are normal in the first week. If a wrap leaks early or redness spreads, call us at <a href="tel:{e(DATA['phoneHref'])}">{e(DATA['phoneDisplay'])}</a> or review our <a href="faq.html">Healing FAQ</a>.</p>
        </div>
        <div class="visit-col-right">
          <p class="kicker">Health &amp; Licensing</p>
          <h3>{e(DATA['healthBoard']['authority'])}</h3>
          <p class="muted">{e(DATA['healthBoard']['address'])} · <a href="tel:{e(DATA['healthBoard']['phoneHref'])}">{e(DATA['healthBoard']['phoneDisplay'])}</a>.</p>
        </div>
      </div>
    </section>

{render_closer(prefix="")}
  </main>""",
            render_footer(prefix=""),
        ]
    )
    (ROOT / "aftercare.html").write_text(html_doc, encoding="utf-8")


def build_faq():
    base = DATA["siteUrl"].rstrip("/")
    url = f"{base}/faq.html"
    faq_entities = [
        {
            "@type": "Question",
            "name": f["question"],
            "acceptedAnswer": {"@type": "Answer", "text": f["answer"]},
        }
        for f in DATA["faqs"]
    ]
    graph = [
        shop_entity(),
        website_entity(),
        {
            "@type": "FAQPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": "FAQ | Tooth & Nail Tattoo Parlour (Macon, GA)",
            "description": (
                "Answers to common questions about walk-in tattoos, shop hours, downtown Macon parking, pricing, deposits, ID rules, body piercing, and healing at Tooth & Nail Tattoo Parlour."
            ),
            "isPartOf": {"@id": f"{base}/#website"},
            "about": {"@id": f"{base}/#shop"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
            "mainEntity": faq_entities,
        },
        breadcrumb_entity(url, [("Home", ""), ("FAQ", "faq.html")]),
    ]

    categories = []
    grouped = {}
    for item in DATA["faqs"]:
        cat = item["category"]
        if cat not in grouped:
            categories.append(cat)
            grouped[cat] = []
        grouped[cat].append(item)

    groups_html = []
    for cat in categories:
        items_html = "\n".join(
            f"""          <details class="faq-item"{" open" if q["openByDefault"] else ""}>
            <summary>{e(q["question"])}</summary>
            <div class="faq-answer">
              <p>{e(q["answer"])}</p>
            </div>
          </details>"""
            for q in grouped[cat]
        )
        groups_html.append(
            f"""      <div class="faq-group">
        <h2 class="faq-group-title">{e(cat)}</h2>
        <div class="faq-list">
{items_html}
        </div>
      </div>"""
        )

    html_doc = "\n".join(
        [
            render_head(
                title="FAQ | Tooth & Nail Tattoo Parlour (Macon, GA)",
                description=(
                    "Hours, walk-ins, downtown Macon parking, pricing, deposits, ID rules, body piercings, and healing answers for Tooth & Nail Tattoo Parlour."
                ),
                canonical_url=url,
                prefix="",
                graph=graph,
            ),
            render_header("faq", prefix=""),
            f"""  <main id="main">
    <section class="page-header">
      <div class="wrap">
        {render_breadcrumbs([("Home", ""), ("FAQ", "faq.html")], prefix="")}
        <p class="kicker">Frequently Asked Questions</p>
        <h1>Straight Answers Before You Sit.</h1>
        <p class="lede">Everything you need to know about walk-ins, consultations, pricing, Cherry Street parking, body piercings, and tattoo healing.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
{chr(10).join(groups_html)}
      </div>
    </section>

{render_closer(prefix="")}
  </main>""",
            render_footer(prefix=""),
        ]
    )
    (ROOT / "faq.html").write_text(html_doc, encoding="utf-8")


def build_404():
    base = DATA["siteUrl"].rstrip("/")
    url = f"{base}/404.html"
    html_doc = "\n".join(
        [
            render_head(
                title="Page Not Found | Tooth & Nail Tattoo Parlour",
                description="The page you requested could not be found. Visit Tooth & Nail Tattoo Parlour at 484 Cherry St in downtown Macon, GA.",
                canonical_url=url,
                prefix="",
                graph=None,
                noindex=True,
            ),
            render_header("", prefix=""),
            """  <main id="main">
    <section class="page-header">
      <div class="wrap">
        <p class="kicker">404 · Page Not Found</p>
        <h1>Wrong Door on Cherry Street.</h1>
        <p class="lede">That link doesn't lead anywhere, but our chairs are still at 484 Cherry St in downtown Macon. Head back to the parlour or book a consult below.</p>
        <div class="cta-row" style="margin-top:1.75rem;">
          <a class="btn" href="index.html">Back to Home</a>
          <a class="btn btn-ghost" href="artists/index.html">Meet the Artists</a>
          <a class="btn btn-ghost" href="book.html">Book a Consult</a>
        </div>
      </div>
    </section>
  </main>""",
            render_footer(prefix=""),
        ]
    )
    (ROOT / "404.html").write_text(html_doc, encoding="utf-8")


def build_sitemap():
    base = DATA["siteUrl"].rstrip("/")
    urls = [
        f"{base}/",
        f"{base}/artists/",
    ] + [f"{base}/artists/{a['slug']}.html" for a in DATA["artists"]] + [
        f"{base}/book.html",
        f"{base}/aftercare.html",
        f"{base}/faq.html",
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{e(u)}</loc><lastmod>{TODAY}</lastmod></url>")
    lines.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def build_robots():
    base = DATA["siteUrl"].rstrip("/")
    content = f"""User-agent: *
Allow: /

# AI Search & Answer Engine Crawlers
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: {base}/sitemap.xml
# LLMs manifest: {base}/llms.txt
"""
    (ROOT / "robots.txt").write_text(content, encoding="utf-8")


def build_llms_txt():
    base = DATA["siteUrl"].rstrip("/")
    artists_md = "\n".join(
        f"- [{a['displayName']}]({base}/artists/{a['slug']}.html): {a['role']} ({', '.join(a['styles'])}) — Instagram: {a['instagram']}"
        for a in DATA["artists"]
    )
    concise = f"""# {DATA['name']}

> Custom tattoo and body piercing parlour at 484 Cherry St in downtown Macon, Georgia. Operating for over a decade with eight resident artists, walk-in availability Tuesday–Saturday, and Macon-Bibb County Board of Health licensing.

## Studio Details
- **Address**: 484 Cherry St, Macon, GA 31201 (Downtown Macon)
- **Phone**: (478) 259-1829
- **Co-Owners**: Kevin Dixon (@kevin_dtattoos) & Ricky Lester (@greasy.dreams)
- **Hours**: Tue–Thu 1:00 PM – 8:00 PM; Fri–Sat 1:00 PM – 10:00 PM; Closed Sun–Mon
- **Walk-Ins**: Welcome Tuesday through Saturday while chairs are open
- **Services**: Custom tattoos, walk-in flash tattoos, cover-ups & reworks, body piercing
- **Health Licensing**: {DATA['healthBoard']['authority']}, {DATA['healthBoard']['address']}, {DATA['healthBoard']['phoneDisplay']}
- **Social**: [Instagram]({DATA['social']['instagram']}) · [Facebook]({DATA['social']['facebook']})

## Key Pages
- [Home & Studio Overview]({base}/)
- [Resident Artists Directory]({base}/artists/)
- [Book a Consultation]({base}/book.html)
- [Tattoo Aftercare Guide]({base}/aftercare.html)
- [Frequently Asked Questions]({base}/faq.html)
- [Full Knowledge Base (llms-full.txt)]({base}/llms-full.txt)

## Resident Artists
{artists_md}
"""
    (ROOT / "llms.txt").write_text(concise, encoding="utf-8")

    services_md = "\n".join(
        f"- **{s['name']}** ({s['availability']}): {s['summary']}"
        for s in DATA["services"]
    )
    faqs_md = "\n".join(
        f"### {q['question']}\n{q['answer']}\n"
        for q in DATA["faqs"]
    )
    soku_md = "\n".join(
        f"{idx + 1}. **{s['name']}**: {s['text']}"
        for idx, s in enumerate(DATA["aftercare"]["soku"]["steps"])
    )
    trad_md = "\n".join(
        f"{idx + 1}. **{s['name']}**: {s['text']}"
        for idx, s in enumerate(DATA["aftercare"]["traditional"]["steps"])
    )

    full = f"""# {DATA['name']} — Full Knowledge Base

> {DATA['tagline']}. Located at 484 Cherry St, Macon, GA 31201. Call (478) 259-1829.

## Overview & NAP
- **Business Name**: {DATA['name']}
- **Owner**: {DATA['owner']}
- **Street Address**: 484 Cherry St, Macon, GA 31201 (Downtown Macon / Cherry Street corridor)
- **Telephone**: +1-478-259-1829
- **Hours**:
  - Tuesday, Wednesday, Thursday: 1:00 PM – 8:00 PM
  - Friday, Saturday: 1:00 PM – 10:00 PM
  - Sunday, Monday: Closed
- **Areas Served**: {', '.join(DATA['areasServed'])}
- **Health Licensing**: {DATA['healthBoard']['authority']} ({DATA['healthBoard']['address']}, {DATA['healthBoard']['phoneDisplay']})
- **Google Maps**: {DATA['mapsUrl']}
- **Instagram**: {DATA['social']['instagram']}
- **Facebook**: {DATA['social']['facebook']}

## Services
{services_md}

## Resident Artists (8 Chairs)
{artists_md}

## Frequently Asked Questions
{faqs_md}
## Tattoo Aftercare Guide

### {DATA['aftercare']['soku']['title']}
{soku_md}

### {DATA['aftercare']['traditional']['title']}
{trad_md}
"""
    (ROOT / "llms-full.txt").write_text(full, encoding="utf-8")


def main():
    build_index()
    build_artists_index()
    build_artist_pages()
    build_book()
    build_aftercare()
    build_faq()
    build_404()
    build_sitemap()
    build_robots()
    build_llms_txt()
    print("Built all 14 HTML pages, sitemap.xml, robots.txt, llms.txt, and llms-full.txt.")


if __name__ == "__main__":
    main()
