# Unconfirmed details

This is a static prototype. Nothing here was sent to the shop. Replace every item below before treating the site as live.

## Artist roster — placeholders

Instagram would not return the bio at `https://instagram.com/tntparlour`.

- A normal browser request was redirected to the Instagram login page and then answered **429**.
- `i.instagram.com/api/v1/users/web_profile_info/?username=tntparlour` returned **404**.
- Facebook `https://facebook.com/105780602271555` redirected to a login page, so current work photos could not be downloaded from there either.

The pages `artists/placeholder-1.html`, `placeholder-2.html`, and `placeholder-3.html` use these stand-in names:

- Placeholder Artist 1
- Placeholder Artist 2
- Placeholder Artist 3

They are **not** real artists. Bios, style tags, and personal Instagram links are empty on purpose. Each page links to the shop Instagram and says the personal handle is unconfirmed.

Do not publish those names as the roster. When the bio is available, replace the names, bios, style tags, handles, photos, the booking-form options, and the URLs. Remove the placeholder seats that are not real people.

### Names that were seen elsewhere and not used

The old site (https://github.com/drewclem/tooth-n-nail) listed Kevin Dixon, Jonathan Kirby, Micah Freeman, and Ricky Lester. The task said that roster is outdated, so it was not copied onto this site.

Public posts and reviews have also mentioned Lee (Instagram discussed as inkyleetattoos), Nicolle, Storm, Amber, Micah, Ricky, and Kevin. Those mentions were not treated as the current Instagram bio, so they are not listed as artists here.

Kevin Dixon is named only as **owner**, which was given in the project brief, not as a confirmed chair on today's roster.

## Photos

- Owner-approved Facebook photos were not fetched (login wall).
- Gallery and artist-page images are from the public repo `drewclem/tooth-n-nail`.
- Several frames are watermarked or signed **Kevin D Tattoos**. The gallery says so. Artist pages label every sample as archive work, not a confirmed portfolio for that seat.
- The small archive thumbs were cropped to remove an Instagram heart icon. They are low resolution (about 220px).
- Logo: `images/logo.png` from that same repo (`static/images/tnn_logo.jpg`). Confirm the shop still uses it.
- `images/og.jpg` is a generated share image using that logo.

## Policies written as placeholders

Marked **PLACEHOLDER** on the booking page and in the FAQ:

- **Deposit.** No amount, no rule about whether it applies to the final price, and no payment method. The page tells people not to send money until the shop states the terms.
- **Age and ID.** The page says to plan on 18+ with a valid photo ID. Guardian rules and any exceptions are explicitly unconfirmed.

## Aftercare and older FAQ answers

`aftercare.html` follows the previous site's two routines (Soku wrap, and a bandage plus Dial Gold / Aquaphor / unscented lotion). Wording was cleaned up. Product names were kept. A banner tells the client to confirm the routine with their artist.

The health-board line was copied and not re-verified:

> Licensed by the Macon Bibb County Board of Health. 171 Emory Highway. 478-745-0411.

FAQ answers on pain, swimming, price, and "leaking ink" started from that site (`pages/Q&A.vue`), edited for clarity. The price answer still says the old site did not quote over the phone or social media, and it tells the reader to confirm that. The pain answer still mentions piercing. Whether the shop still pierces was not reconfirmed.

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
