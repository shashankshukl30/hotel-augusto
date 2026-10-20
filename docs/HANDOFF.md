# Hotel Augusto

Website handoff · Digiocular · Varanasi

Generated 20 October 2026, 06:06 UTC. Regenerate after final verification or deployment changes.

## Current delivery

Independent project: `D:\Digiocular\Websites\Hotel Augusto`. Next.js 16.4.2, strict TypeScript, Tailwind v4 and Framer Motion. The website provides room information and WhatsApp enquiries; there is no live booking engine, payment flow or enquiry database.

No production domain has been changed. This handoff records the local implementation and the available evidence; it does not assert a public launch.

An owner-private Sites preview is configured at [hotel-augusto.candy-okapi-4696.chatgpt.site](https://hotel-augusto.candy-okapi-4696.chatgpt.site). Current publication status is recorded in [the deployment record](../evidence/hospitality-revision/private-deployment.json); the public hotel launch remains separate. `.openai/hosting.json` records the existing Sites project.

Git origin at generation: `https://github.com/shashankshukl30/hotel-augusto.git`.

## Visual system

The latest 20 October brief brings most Hotel Vagmi elements into Augusto's own hospitality identity. Local Bodoni Moda at weight 400 and Manrope body combine with ivory, ink blue and bronze. Genuine property photographs lead the hero, all three room categories are visible, and detailed dining, arrival and city content give the hotel substance across 16 pages. Asymmetric spreads, fine rules and modest 4–8px corners replace the earlier product-like Apple treatment.

Interior titles reach roughly 76–104px on desktop and 48–58px on mobile; body copy is 18px desktop / 17px mobile. Rectangular actions are approximately 52–54px high. Hero scene controls, a pause action, photo transitions and reveals respect reduced motion and native scrolling. See the [hospitality reference study](../research/hospitality-revision/reference-study.md), [feature and fact plan](../research/hospitality-revision/content-journey-plan.json) and [implementation plan](plans/2026-10-19-website.md). Earlier design documents remain historical.

## Pages and editing locations

- `/` — genuine-property hero, dated StayBar, welcome, all rooms, dining, city itinerary, an attributed guest excerpt and review links, gallery, arrival, FAQs, guides and a final enquiry.

- `/hotel` — the property, reception, facilities and arrival guidance; `/dining` — vegetarian restaurant, room service and meal-plan enquiries.

- `/rooms`, `/rooms/compare` and three room-detail pages — visible categories, factual bed layouts, a mobile two-room selector, photo walkthroughs and room-prefilled enquiries.

- `/varanasi` — destination guide; `/gallery` — filters and keyboard/touch image viewer.

- `/guides` and `/guides/first-visit-to-kashi`, `/guides/arriving-in-godowlia`, `/guides/choosing-your-room` — practical planning articles.

- `/contact` — enquiry, phone, directions and FAQs; `/privacy` — actual data handling and destination photo credits.

Core facts and contact: `content/hotel.ts`. Facilities, review links and arrival: `content/hospitality.ts`. Guides: `content/guides.ts`. Photos: `content/room-images.ts`. Tokens: `app/globals.css`. Booking validation and WhatsApp URLs: `lib/booking.ts`; page-to-page travel preferences: `lib/stay-query.ts`. The reusable `StayBar` and `ArrivalGuide` components serve multiple pages. Adapt the enquiry handoff deliberately when adding an approved booking engine.

## Content, photographs and owner confirmations

Research retains 22 source entries covering Google, OTAs, destination authorities and contact verification. The public image set contains 22 WebP files. Property photographs show Hotel Augusto; destination photographs are separately identified. No generated hotel photographs or unrelated room stand-ins are used.

- Confirm that +91 80817 09146 is the hotel's active WhatsApp booking account. It is the Google-listed telephone and its public WhatsApp link resolves, which does not establish registration or account ownership. Testing sent no enquiry.

- Confirm permission to reuse property photographs collected from public hotel listings. Public visibility alone is not a reuse licence. Preserve originals, hashes and provenance in `research/assets/` and `research/ota-revision/`; Google uploader display names alone do not establish copyright ownership.

- Destination images use Unsplash licences and a CC BY 4.0 temple photo by Pradum Shukla. Keep the visible temple attribution and `/privacy` credits. The Augusto wordmark is an original typographic treatment, not a recovered official logo.

- Confirm current check-in/out, guest identification, parking, meal inclusions and cancellation/payment terms with the hotel. Conflicting published policies, room areas/capacities, live rates and availability have not been promoted as established facts.

Evidence: [fact sheet](../research/hotel-fact-sheet.md), [source ledger](../research/source-ledger.md), [asset manifest](../research/assets/asset-manifest.json), [Maps verification](../research/map-link-verification.json), [WhatsApp verification](../research/whatsapp-public-check.json). Research documents also have DOCX twins.

The user-supplied dated MakeMyTrip route returned a browser HTTP/2 transport error. Its indexed canonical page corroborates stable property facts; a fresh 20 October amenities index supports the expanded service details, not live dated availability. Google's rendered profile and accessible property photos were inspected. See [OTA source record](../research/ota-revision/SOURCE-REVIEW.md), [photo mapping](../research/ota-revision/source-to-page-mapping.json), [new feature evidence](../research/hospitality-revision/content-journey-plan.json), [guest-excerpt evidence](../research/hospitality-revision/guest-review-evidence.json) and [official visitor-link checks](../research/hospitality-revision/additional-source-checks.json).

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
python scripts/qa_hospitality_revision.py --base-url http://127.0.0.1:3080
```

- Set `NEXT_PUBLIC_SITE_URL` to the approved HTTPS origin. Keep `SITE_INDEXABLE=false` on previews; set it to `true` only for approved production. These settings control absolute metadata URLs, robots and sitemap behavior. `.env.example` documents the values.

- Push the independent private repository before the first deployment. Import it into Vercel as Next.js; `vercel.json` pins region `sin1`. Run the browser checks against the deployed URL and check canonical/OG output before connecting the approved domain.

- Normal Next.js/Vercel operation is the default. For the private static preview only, set `SITE_STATIC_EXPORT=true` before `npm run build`; the result is `out/`. Unset the flag for the next normal build. Static export disables server image optimization; the static host must supply response headers. Keep previews noindex and verify their deployed behavior.

- Do not infer ownership from old hotel domains: research found a failed domain and an affiliate redirect. Obtain the client's intended domain and access separately.

## Verification snapshot

Latest completed shared report: [evidence/hospitality-revision/production-qa.json](../evidence/hospitality-revision/production-qa.json), completed 2026-10-20T05:58:42.349172+00:00 against `http://127.0.0.1:3080`. Status: PASS. It records 102 viewport checks, 34 axe audits, 40 interaction checks and 0 failures. These are report counts, not a claim that an unrecorded final run passed.

The refreshed production audit is dated 2026-10-20T06:00:16.943938+00:00; its OG image is 1200 × 630px. Throttled mobile samples: LCP 1780ms / CLS 0.0000; LCP 1728ms / CLS 0.0000. These are local synthetic measurements, not field Core Web Vitals or a Lighthouse score. The audit retains response headers and runtime observations.

Focused hotel/dining review: 4 route/viewport records at 390, 1440px and 16 interactions; checks pass. Screenshots and the activated Hotel Augusto map pin were visually inspected. This focused dev check supplements the production report. Evidence: [page review](../evidence/hospitality-revision/hotel-dining-review.json).

Current revision evidence is in `evidence/hospitality-revision/`; the final report is `evidence/hospitality-revision/production-qa.json`. Earlier Apple/cinematic reports remain history. Browser checks do not establish hotel policy accuracy, live availability or photo rights.

Release evidence: [production audit](../evidence/production-audit.json), [scoped storage cleanup](../evidence/storage-cleanup.json), and [inactive development output cleanup](../evidence/dev-output-cleanup.json). The development cleanup records 290,643,233 bytes removed after stopping the dev session; production was verified afterwards. The local preview remains noindex. An approved public domain and route canonical configuration still require launch verification.

Render-cleanup limitation: automatic approval review rejected removal of the verified OTA-document render scratch with the reason 'blocked by policy'. Its 447,116 bytes remain under `research/ota-revision/.document-review/`; no further removal was attempted. The retained source twins and scratch hashes are recorded in `research/ota-revision/source-review-verification.json`. Final handoff render evidence is retained with `docs/handoff-verification.json`.

A separate 29,539-byte generated handoff bytecode file was also rejected for cleanup by automatic approval review. It remains retained; no retry is part of this revision. Current scoped cleanup records preserve all source, licensed assets and review evidence.

## Security and maintenance

The recorded production dependency audit has 0 vulnerabilities. The full audit records 5 high findings from one development-only ESLint chain ending in braces 3.0.3. [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) had no official patched release at the 19 October 2026 review. Keep the lockfile, recheck upstream and do not force-downgrade Next.js to silence it. Details: [security review](../evidence/security-review.json).

StayBar passes validated dates, party size and room preference through the contact URL; these may remain in browser history. Names and personal notes stay off that URL. The form prepares a WhatsApp draft without saving enquiries or sending silently. The Google map iframe loads only on explicit activation. No payment collection or analytics is installed. Security headers, Hotel JSON-LD, local fonts and a 1200×630 OG image are included. Privacy must be revisited when these features change.

## Primary reference links

Design: [Hotel Vagmi](https://hotelvagmi.com/), [The Drake on Awwwards](https://www.awwwards.com/sites/the-drake-hotel), plus Shree Ganesha Palace and live reference captures in `research/hospitality-revision/`. Property: [MakeMyTrip Hotel Augusto](https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html). Destination: [official temple visitor portal](https://www.shrikashivishwanath.org/), [Kashi Vishwanath government page](https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/), [Dashashwamedh Ghat](https://kashi.gov.in/listing-details/dashashwamedh-ghat). Credits: [Pradum Shukla temple photo](https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [Unsplash licence](https://unsplash.com/license).

Regenerate both handoff files with: python scripts/generate_handoff.py. The generator uses python-docx and verifies that its DOCX can be reopened.
