# Shop Confirmation Checklist

This internal checklist tracks details that can be refined in `data/shop.json` (followed by `python3 build.py`) whenever the shop confirms updates. Nothing from this file is linked or exposed on the public website.

## Optional Updates in `data/shop.json`

1. **Custom Domain (`siteUrl`)**: Currently set to `https://thegenuinegeek.github.io/tntparlour`. Update `siteUrl` in `data/shop.json` to `https://tntparlour.com` (and re-run `python3 build.py`) before switching DNS so canonicals, Open Graph URLs, `sitemap.xml`, `robots.txt`, and `llms.txt` point to the live domain.
2. **Consult Form Backend / Email**: `book.html` is pre-configured with `data-netlify="true"` for Netlify Forms and includes a client-side summary + clipboard/email/Instagram workflow for GitHub Pages. Add a shop booking email or Formspree/Web3Forms endpoint when ready.
3. **Co-Owner Info (Ricky) + Artist Bios, Styles & Portfolio Photos**: Add co-owner **Ricky**'s full name, role/bio, and details alongside Kevin Dixon once confirmed. Only Kevin Dixon's archive work is currently included locally; swap in individual style specialties, bios, and high-res photos for the other seven resident artists (`@greasy.dreams`, `@baza_stormtattoos`, `@c.lo.qween`, `@inkyleetattoos`, `@jordyn_tatts`, `@hol3_punch3r`, `@lilskythetatguy`) as they provide them.
4. **Verified Google Review Count & Map Pin**: `aggregateRating` and `geo` coordinates are intentionally omitted from JSON-LD until exact Google Business Profile review count and rooftop pin coordinates are confirmed.
5. **Exact Deposit & Piercing Menu**: Update the FAQ/Booking policy copy if the shop wants to publish specific deposit dollar amounts, minimum age exceptions, or a piercing price menu.
