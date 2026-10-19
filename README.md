# Hotel Augusto, Varanasi

An independent Digiocular client website in `D:\Digiocular\Websites\Hotel Augusto`.

The current design combines Apple-like clarity with an original hospitality direction informed by live Awwwards references: Manrope display typography, Inter body text, bone/ink/verdigris surfaces, a full-screen photographic Varanasi hero and asymmetric layouts. The site is multi-page. Earlier serif/terracotta and literal Apple directions are superseded.

## Run locally

Requires Node.js 22.9 or later (built and tested with Node 24).

```powershell
npm ci
npm run dev
```

Open http://localhost:3080. For a production preview:

```powershell
npm run build
npm run start
```

Stop the development server before starting production on the same port.

## Pages

- `/` — hotel introduction, room selector, dining and city photography
- `/hotel` — property story, real hotel spaces, amenities and arrival
- `/dining` — vegetarian dining, restaurant photographs and meal enquiries
- `/rooms` — room comparison
- `/rooms/deluxe-room`, `/rooms/deluxe-twin-room`, `/rooms/family-room`
- `/varanasi` — local destination guide
- `/gallery` — filterable gallery with keyboard and swipe support
- `/contact` — date/guest/room enquiry, phone, directions and FAQs
- `/privacy` — enquiry privacy and licensed destination photograph credits

## Content and booking

`content/hotel.ts` is the single source of hotel facts and the booking phone number. Room image mappings are in `content/room-images.ts`. Photo provenance and retained originals are in `research/assets/`, with the new hero licence and original in `research/awwwards-revision/`. The source ledger includes Google and MakeMyTrip; the supplied MMT hotel ID is `201909301024364424`. Research documents include DOCX twins.

The current WhatsApp destination is the hotel's Google-listed telephone, **+91 80817 09146**. The public WhatsApp link resolves to that number. The hotel must confirm it is the desired, active booking account before public launch. No enquiry was sent during testing.

The form validates dates and guest counts, prepares an encoded message, and lets the visitor explicitly open and send it in WhatsApp. It does not check live inventory, confirm a reservation, process payments, or store personal data. `lib/booking.ts` is the integration point for a future booking engine.

## Checks

```powershell
npm run lint
npm run typecheck
npm test
npm run build
python scripts/browser_qa.py --base-url http://127.0.0.1:3080
```

Browser QA uses a fresh Microsoft Edge context through Python Playwright and axe-core. Reports are in `evidence/`. Tests do not send WhatsApp messages.

## Launch settings

1. Confirm the WhatsApp booking number, current guest policies and permission to reuse the hotel photographs collected from public listings.
2. Supply the approved production domain. Set `NEXT_PUBLIC_SITE_URL` to its HTTPS origin.
3. Keep `SITE_INDEXABLE=false` for previews; set it to `true` only for approved production. This controls robots and sitemap output.
4. Push this independent private Git repository before any Vercel deployment. The Vercel region is configured as `sin1`.
5. Run the browser checks on the deployed host and verify its canonical/OG URLs before connecting a domain.

No production domain has been changed. Old hotel domains were not assumed to be authoritative: one no longer resolves, and another redirects through an affiliate.

## Security and maintenance

Production dependencies have no reported npm audit findings as of this build. The development ESLint dependency chain has an upstream `braces` advisory without an available patched release; see `evidence/security-review.json`. Do not force-downgrade Next.js to silence that report.

Security headers, hotel JSON-LD, a 1200×630 OG image, local fonts and responsive images are included. Keep the lockfile and licensed photograph credits. All source and working dependencies remain in this one project folder.
