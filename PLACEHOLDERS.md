# Unconfirmed details

This is a static prototype. Nothing here was sent to the shop. Replace every item below before treating the site as live.

## Artist roster

James supplied the current artists from the Instagram bio. Display names are the handle with `@`, except Kevin Dixon. No other real names were invented.

| Page | Display name | Instagram |
| --- | --- | --- |
| `artists/kevin-dixon.html` | Kevin Dixon (owner) | https://instagram.com/kevin_dtattoos |
| `artists/greasy-dreams.html` | @greasy.dreams | https://instagram.com/greasy.dreams |
| `artists/baza-stormtattoos.html` | @baza_stormtattoos | https://instagram.com/baza_stormtattoos |
| `artists/c-lo-qween.html` | @c.lo.qween | https://instagram.com/c.lo.qween |
| `artists/inkyleetattoos.html` | @inkyleetattoos | https://instagram.com/inkyleetattoos |
| `artists/jordyn-tatts.html` | @jordyn_tatts | https://instagram.com/jordyn_tatts |
| `artists/hol3-punch3r.html` | @hol3_punch3r | https://instagram.com/hol3_punch3r |
| `artists/lilskythetatguy.html` | @lilskythetatguy | https://instagram.com/lilskythetatguy |

### Bios and styles — still placeholders

Every artist page has:

- A **Placeholder** bio: not confirmed. No experience, specialties, or limits are stated.
- A style tag: **Styles unconfirmed — placeholder**.

Replace both after the shop writes them. Do not treat the handles as full legal names.

## Photos

- Facebook photos were not fetched (login wall).
- Kevin D Tattoos watermarked or signed archive frames from `drewclem/tooth-n-nail` are used only on the home gallery and on Kevin Dixon's page.
- The other seven artist pages have a "See their work on Instagram" card and no borrowed photos.
- Logo: `images/logo.png` from that same repo. Confirm the shop still uses it.
- `images/og.jpg` is a generated share image using that logo.

## Piercing

The bio calls the shop a tattoo and piercing shop. The homepage, the FAQ, and the `TattooParlor` description say piercing is a service. The FAQ answer is a **placeholder**. No piercing price, jewelry list, or menu was invented.

## Policies written as placeholders

Marked **PLACEHOLDER** on the booking page and in the FAQ:

- **Deposit.** No amount, no rule about whether it applies to the final price, and no payment method. The page tells people not to send money until the shop states the terms.
- **Age and ID.** The page says to plan on 18+ with a valid photo ID. Guardian rules and any exceptions are explicitly unconfirmed.

## Aftercare and older FAQ answers

`aftercare.html` follows the previous site's two routines (Soku wrap, and a bandage plus Dial Gold / Aquaphor / unscented lotion). Wording was cleaned up. Product names were kept. A banner tells the client to confirm the routine with their artist.

The health-board line was copied and not re-verified:

> Licensed by the Macon Bibb County Board of Health. 171 Emory Highway. 478-745-0411.

FAQ answers on pain, swimming, price, and "leaking ink" started from that site (`pages/Q&A.vue`), edited for clarity. The price answer still says the old site did not quote over the phone or social media, and it tells the reader to confirm that. A separate piercing question is a placeholder and does not list a price.

Hours and walk-ins in the FAQ match the facts supplied for this prototype.

## Facts used, and what was left out of schema

Used as given:

- Tooth & Nail Tattoo Parlour, 484 Cherry St, Macon, GA 31201
- (478) 259-1829
- Tue–Thu 1–8 PM, Fri–Sat 1–10 PM, closed Sun–Mon
- Walk-ins welcome
- Over a decade in business
- Instagram https://instagram.com/tntparlour
- Facebook https://facebook.com/105780602271555
- Owner Kevin Dixon

**Google rating.** The page shows "4.9 stars / on Google". The brief said *about* 4.9 from *roughly* 121 reviews. Another public listing showed 4.9 from 77. `aggregateRating` is **omitted** from JSON-LD. Confirm the live count before adding it.

**Map pin.** JSON-LD has the street address and a Google Maps search link. It does **not** include `geo`. A public listing showed 32.83526, -83.62724. The old site's map embed centered near 32.83527, -83.62944. Those are far enough apart to put a pin on the wrong block. Add coordinates only after the shop confirms the pin.

**Email.** No shop email was supplied. The consult form's fallback opens a `mailto:` with no recipient.

**Old homepage claims not reused as current copy:** "35 years of combined experience," and the sterile / quality / professional blurbs. The tagline "Lowbrow with Know How" was not reused.

**http://tntparlour.com/** showed up on a listing and was not linked.

## Form

`book.html` includes `data-netlify="true"`, `netlify-honeypot="bot-field"`, a honeypot field, and `enctype="multipart/form-data"` so a later Netlify deploy can accept it, including the reference file field.

GitHub Pages cannot receive that POST. The page says so and offers a phone call plus a mailto built from the fields. The file itself is not attached in that fallback.

Netlify's file-upload feature may require a paid form add-on. This prototype does not turn that on.
