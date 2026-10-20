# Hotel Augusto

Website handoff · Digiocular · Varanasi

Generated 20 October 2026, 05:25 UTC. Regenerate after final verification or deployment changes.

## Current delivery

Independent project: `D:\Digiocular\Websites\Hotel Augusto`. Next.js 16.4.2, strict TypeScript, Tailwind v4 and Framer Motion. The website provides room information and WhatsApp enquiries; there is no live booking engine, payment flow or enquiry database.

No production domain has been changed. This handoff records the local implementation and the available evidence; it does not assert a public launch.

Git origin at generation: `https://github.com/shashankshukl30/hotel-augusto.git`.

## Visual system

The 20 October correction restores the Apple-inspired foundation the user explicitly liked, now larger and more animated. Local Manrope display at weight 650 and Inter body, pearl surfaces, charcoal text and a restrained blue accent support large real photographs, generous spacing and rounded panels. Interior titles reach roughly 80–104px on desktop and 52–64px on mobile, with 18px desktop / 17px mobile body copy and readable labels. All 11 pages and the improved Varanasi hero remain.

Hotel and dining retain their distinct compositions. Photography and form panels use soft 24–32px corners; primary actions and enquiry controls are approximately 56px desktop / 50px mobile. Contact fields stay at 17px or larger on mobile. Visible entrance and scroll motion respect reduced-motion preferences and native scrolling. See [current Apple premium contract](../research/apple-premium-direction.md) and [implementation plan](plans/2026-10-19-website.md). The previous verdigris and smaller Apple revisions remain historical references.

## Pages and editing locations

- `/` — hotel introduction, room selection, dining and Varanasi photography.

- `/hotel` — the property, reception, facilities and arrival guidance; `/dining` — vegetarian restaurant, room service and meal-plan enquiries.

- `/rooms` and `/rooms/deluxe-room`, `/rooms/deluxe-twin-room`, `/rooms/family-room` — comparison and individual room pages.

- `/varanasi` — destination guide; `/gallery` — filters and keyboard/touch image viewer.

- `/contact` — enquiry, phone, directions and FAQs; `/privacy` — actual data handling and destination photo credits.

Edit facts and the contact number in `content/hotel.ts`; room photographs in `content/room-images.ts`; visual tokens in `app/globals.css`. Booking validation and WhatsApp URL generation live in `lib/booking.ts`, with the form in `components/booking-form.tsx`. Replace that handoff deliberately when integrating an approved booking engine.

## Content, photographs and owner confirmations

Research retains 22 source entries covering Google, OTAs, destination authorities and contact verification. The public image set contains 22 WebP files. Property photographs show Hotel Augusto; destination photographs are separately identified. No generated hotel photographs or unrelated room stand-ins are used.

- Confirm that +91 80817 09146 is the hotel's active WhatsApp booking account. It is the Google-listed telephone and its public WhatsApp link resolves, which does not establish registration or account ownership. Testing sent no enquiry.

- Confirm permission to reuse property photographs collected from public hotel listings. Public visibility alone is not a reuse licence. Preserve originals, hashes and provenance in `research/assets/` and `research/ota-revision/`; Google uploader display names alone do not establish copyright ownership.

- Destination images use Unsplash licences and a CC BY 4.0 temple photo by Pradum Shukla. Keep the visible temple attribution and `/privacy` credits. The Augusto wordmark is an original typographic treatment, not a recovered official logo.

- Confirm current check-in/out, guest identification, parking, meal inclusions and cancellation/payment terms with the hotel. Conflicting published policies, room areas/capacities, live rates and availability have not been promoted as established facts.

Evidence: [fact sheet](../research/hotel-fact-sheet.md), [source ledger](../research/source-ledger.md), [asset manifest](../research/assets/asset-manifest.json), [Maps verification](../research/map-link-verification.json), [WhatsApp verification](../research/whatsapp-public-check.json). Research documents also have DOCX twins.

The user-supplied MakeMyTrip dated route was tried in a fresh browser and returned an HTTP/2 transport error. The canonical indexed MMT property page corroborates the address, room categories and vegetarian dining; it does not verify live dated availability. Google’s rendered profile and eight accessible still-photo entries were inspected, and three additional real property photographs were collected. See [OTA revision record](../research/ota-revision/SOURCE-REVIEW.md), [source-to-page mapping](../research/ota-revision/source-to-page-mapping.json) and [new asset ledger](../research/ota-revision/asset-candidates.json).

## Run, deploy and configure

Use Node.js 22.9+; this workspace used Node 24. From the project folder:

```powershell
npm ci
npm run dev
```

Local preview: `http://localhost:3080`. Before release, run the following. Stop the dev server before starting production on the same port.

```powershell
npm run lint
npm run typecheck
npm test
npm run build
npm run start
python scripts/browser_qa.py --base-url http://127.0.0.1:3080
```

- Set `NEXT_PUBLIC_SITE_URL` to the approved HTTPS origin. Keep `SITE_INDEXABLE=false` on previews; set it to `true` only for approved production. These settings control absolute metadata URLs, robots and sitemap behavior. `.env.example` documents the values.

- Push the independent private repository before the first deployment. Import it into Vercel as Next.js; `vercel.json` pins region `sin1`. Run the browser checks against the deployed URL and check canonical/OG output before connecting the approved domain.

- Do not infer ownership from old hotel domains: research found a failed domain and an affiliate redirect. Obtain the client's intended domain and access separately.

## Verification snapshot

Latest completed shared report: [evidence/qa-apple-premium-production.json](../evidence/qa-apple-premium-production.json), completed 2026-10-20T05:23:43.863633+00:00 against `http://127.0.0.1:3080`. Status: PASS. It records 72 viewport checks, 24 axe audits, 76 interaction checks and 0 failures. These are report counts, not a claim that an unrecorded final run passed.

The initial report recorded 1 failed automated check. The final report includes 3 targeted keyboard-link retests using a 1px outer-edge rounding tolerance and fully visible text bounds. The original run, retest evidence and timestamps remain preserved in that report; no application change was required between those runs.

Focused hotel, dining, contact and privacy review: 8 route/viewport records at 390, 1440px; layout/image/runtime checks pass. The rendered screenshots were inspected for type scale, image framing and control alignment. Evidence: [page review](../evidence/apple-premium/hospitality-review.json).

Current revision evidence is in `evidence/apple-premium/`; the intended final report is `evidence/qa-apple-premium-production.json`. Earlier Apple/cinematic reports and `research/awwwards-revision/` remain reference history. Use the latest completed report and its remaining failures; earlier passes do not certify later edits. Browser checks do not establish hotel policy accuracy or photo rights.

Release evidence: [production audit](../evidence/production-audit.json), [scoped storage cleanup](../evidence/storage-cleanup.json), and [inactive development output cleanup](../evidence/dev-output-cleanup.json). The development cleanup records 240,653,234 bytes removed after stopping the dev session; production was verified afterwards. The local preview remains noindex. An approved public domain and route canonical configuration still require launch verification.

Render-cleanup limitation: automatic approval review rejected removal of the verified OTA-document render scratch with the reason 'blocked by policy'. Its 447,116 bytes remain under `research/ota-revision/.document-review/`; no further removal was attempted. The retained source twins and scratch hashes are recorded in `research/ota-revision/source-review-verification.json`. Final handoff render evidence is retained with `docs/handoff-verification.json`.

## Security and maintenance

The recorded production dependency audit has 0 vulnerabilities. The full audit records 5 high findings from one development-only ESLint chain ending in braces 3.0.3. [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) had no official patched release at the 19 October 2026 review. Keep the lockfile, recheck upstream and do not force-downgrade Next.js to silence it. Details: [security review](../evidence/security-review.json).

The enquiry stays in browser memory until the visitor opens the encoded WhatsApp link. No silent message sending, payment collection, analytics or enquiry persistence is installed. Security headers, Hotel JSON-LD, local fonts and a 1200×630 OG image are included. Revisit privacy and security when a booking engine or analytics is added.

## Primary reference links

Design: [The Drake on Awwwards](https://www.awwwards.com/sites/the-drake-hotel), [Kaskady on Awwwards](https://www.awwwards.com/sites/hotel-spa-resort-kaskady), [Casa Cook on Awwwards](https://www.awwwards.com/sites/casa-cook-hotels), [Apple typography](https://developer.apple.com/design/human-interface-guidelines/typography). Property: [MakeMyTrip Hotel Augusto](https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html). Destination: [Kashi Vishwanath](https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/), [Dashashwamedh Ghat](https://kashi.gov.in/listing-details/dashashwamedh-ghat). Credits: [Pradum Shukla temple photo](https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [Unsplash licence](https://unsplash.com/license).

Regenerate both handoff files with: python scripts/generate_handoff.py. The generator uses python-docx and verifies that its DOCX can be reopened.
