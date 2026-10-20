# Hotel Augusto

Website handoff · Digiocular · Varanasi

Generated 20 October 2026, 07:32 UTC. Regenerate after final verification or deployment changes.

## Current delivery

Independent project: `D:\Digiocular\Websites\Hotel Augusto`. Next.js 16.4.2, strict TypeScript, Tailwind v4 and Framer Motion. The website provides room information and WhatsApp enquiries; there is no live booking engine, payment flow or enquiry database.

No production domain has been changed. This handoff records the local implementation and the available evidence; it does not assert a public launch.

An owner-private Sites preview is configured at [hotel-augusto.candy-okapi-4696.chatgpt.site](https://hotel-augusto.candy-okapi-4696.chatgpt.site). This revision's publication status is recorded in [the deployment record](../evidence/apple-dominant-revision/private-deployment.json); the public hotel launch remains separate. `.openai/hosting.json` records the existing Sites project.

Git origin at generation: `https://github.com/shashankshukl30/hotel-augusto.git`.

## Visual system

The latest reference hierarchy puts Lando Norris first for bold composition and memorable motion, with Apple and Linear informing control clarity and precision. The shared system uses local Inter, near-white/cool-gray surfaces, charcoal and cobalt actions. Genuine Augusto photography and the supplied hotel logo anchor the 17-route hospitality experience.

The homepage opens with nearly full-viewport property photography, the large left-aligned 'Your place / in Kashi.' headline and scene/pause controls within the photograph. Scene changes wait for image readiness. Spring pointer drift, native scroll scaling and independent hover/focus pause support the interaction. An ink-blue city chapter uses oversized decorative KASHI lettering, genuine river imagery and manual tabs.

Keep substantial headings, readable 18px/17px body copy, clear primary actions and at least 44px interactive targets. Hero motion, room-photo hover/focus feedback, menu transitions and reveals respect reduced motion and native scrolling. The [implementation plan](plans/2026-10-19-website.md) records the frozen design; [Linear source notes](../research/apple-dominant-revision/linear-reference.json), [Casa Angelina notes](../research/apple-dominant-revision/casa-angelina-reference.json) and earlier hotel studies retain research context.

## Pages and editing locations

- `/` — property hero, dated StayBar, all rooms, dining, city itinerary, dated Google badge, attributed guest excerpt, proximity links, gallery, arrival, FAQs and guides.

- `/hotel` — property, facilities and arrival; `/dining` — vegetarian dining, its own enquiry and downloadable planning guide; `/group-stays` — family, friends and business accommodation requests.

- `/rooms`, `/rooms/compare` and three room-detail pages — visible categories, factual bed layouts, a mobile two-room selector, photo walkthroughs and room-prefilled enquiries.

- `/varanasi` — destination guide; `/gallery` — filters and keyboard/touch image viewer.

- `/guides` and `/guides/first-visit-to-kashi`, `/guides/arriving-in-godowlia`, `/guides/choosing-your-room` — practical planning articles.

- `/contact` — enquiry, phone, directions and FAQs; `/privacy` — actual data handling and destination photo credits.

Core facts: `content/hotel.ts`; facilities/arrival: `content/hospitality.ts`; dated proof: `content/social-proof.ts`; guides/photos: `content/guides.ts` and `content/room-images.ts`. Booking: `lib/booking.ts`, `lib/stay-query.ts`, `lib/dining-enquiry.ts`. The universal `BookingDock` reserves its measured height through the footer. Stay requests include 1–8 requested rooms and night summaries; these are not capacity promises.

## Content, photographs and owner confirmations

The base ledger retains 22 source entries, supplemented by later verification records. The public image set retains 22 source WebP files plus generated responsive variants. Hotel and destination photographs are clearly distinguished. No generated hotel photographs or unrelated room stand-ins are used.

- Confirm that +91 80817 09146 is the hotel's active WhatsApp booking account. It is the Google-listed telephone and its public WhatsApp link resolves, which does not establish registration or account ownership. Testing sent no enquiry.

- Confirm permission to reuse property photographs collected from public hotel listings. Public visibility alone is not a reuse licence. Preserve originals, hashes and provenance in `research/assets/` and `research/ota-revision/`; Google uploader display names alone do not establish copyright ownership.

- Destination images use Unsplash licences and a CC BY 4.0 temple photo by Pradum Shukla. Keep temple attribution and `/privacy` credits. The user supplied `logo.jpeg`; its public brand copy now appears in the header, footer, favicon, OG and dining guide.

- Confirm current check-in/out, guest identification, parking, meal inclusions and cancellation/payment terms with the hotel. Conflicting published policies, room areas/capacities, live rates and availability have not been promoted as established facts.

Evidence: [fact sheet](../research/hotel-fact-sheet.md), [source ledger](../research/source-ledger.md), [asset manifest](../research/assets/asset-manifest.json), [Maps verification](../research/map-link-verification.json), [WhatsApp verification](../research/whatsapp-public-check.json). Research documents also have DOCX twins.

The user-supplied dated MakeMyTrip route returned a browser HTTP/2 transport error. Its indexed canonical page corroborates stable property facts; a fresh 20 October amenities index supports the expanded service details, not live dated availability. Google's rendered profile and accessible property photos were inspected. See [OTA source record](../research/ota-revision/SOURCE-REVIEW.md), [photo mapping](../research/ota-revision/source-to-page-mapping.json), [new feature evidence](../research/hospitality-revision/content-journey-plan.json), [guest-excerpt evidence](../research/hospitality-revision/guest-review-evidence.json) and [official visitor-link checks](../research/hospitality-revision/additional-source-checks.json).

Google: 3.7/5 from 1,628 reviews, checked 20 October 2026, displayed with source/date. MMT scores conflict, so its review link carries no numerical badge. No new guest-photo reuse licence was established. Temple/ghat proximity stays qualitative with walking-direction links. [Fresh findings](../research/apple-dominant-revision/conversion-evidence/findings.json) retain these distinctions; no wedding, banquet or conference services are claimed.

The one-page [dining PDF](../public/downloads/hotel-augusto-dining-guide.pdf) and [editable DOCX](hotel-augusto-dining-guide.docx) use genuine imagery and planning information, not an invented menu. Regenerate with `python -B scripts/generate_dining_guide.py`; [render/reopen evidence](../evidence/apple-dominant-revision/dining-guide/verification.json) records both outputs.

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
npm run qa -- --base-url http://127.0.0.1:3080 --output evidence/apple-dominant-revision
```

- Set `NEXT_PUBLIC_SITE_URL` to the approved HTTPS origin. Keep `SITE_INDEXABLE=false` on previews; set it to `true` only for approved production. These settings control absolute metadata URLs, robots and sitemap behavior. `.env.example` documents the values.

- Push the independent private repository before the first deployment. Import it into Vercel as Next.js; `vercel.json` pins region `sin1`. Run the browser checks against the deployed URL and check canonical/OG output before connecting the approved domain.

- Normal Next/Vercel retains AVIF/WebP optimization. Optional `SITE_STATIC_EXPORT=true` writes `out/` using `lib/static-image-loader.ts` and local WebP variants. After changing photographs, run `python -B scripts/generate-responsive-images.py`; preserve originals and the manifest. Unset the export flag for a normal build. The static host supplies response headers; previews remain noindex.

- Do not infer ownership from old hotel domains: research found a failed domain and an affiliate redirect. Obtain the client's intended domain and access separately.

## Verification snapshot

Latest completed shared report: [evidence/apple-dominant-revision/production-qa.json](../evidence/apple-dominant-revision/production-qa.json), completed 2026-10-20T07:25:36.282700+00:00 against `http://127.0.0.1:3080`. Status: PASS. It records 108 viewport checks, 36 axe audits, 40 interaction checks and 0 failures. These are report counts, not a claim that an unrecorded final run passed.

Original focused [conversion QA](../evidence/apple-dominant-revision/conversion-upgrade-qa.json), completed 2026-10-20T07:27:37.930214+00:00: 209 of 211 checks passed; 2 assertions failed. Its scope covers persistent booking access, requested rooms, enquiry drafts, downloads and responsive static media. The original report is retained without rewriting its counts.

Separate [dining retest](../evidence/apple-dominant-revision/conversion-dining-retest-20261020T073017878694Z.json), completed 2026-10-20T07:30:21.949581+00:00: PASS, 13 of 13 checks passed and 0 failed. The original PDF assertions expected the wrong title. The corrected check validates the actual brochure text and downloaded/source SHA256; the brochure did not require a content change. The supplemental report confirms the original report remains byte-identical; its baseline SHA256 is `e461ad27174be77d22045182d937008daa2d90fd65d0b86b797b4ba8fccb76b8`. These targeted results are separate from the original full-run totals.

The separate [room review](../evidence/apple-dominant-revision/rooms-review.json) records 21 layouts, 10 axe audits, 29 interactions and 0 failures. The [static-export audit](../evidence/apple-dominant-revision/static-export-audit.json) records 64/64 checks passed across 17 content routes and the not-found artifact. The [visual capture record](../evidence/apple-dominant-revision/visual-review-captures.json) contains 46 captures and 0 capture errors.

The refreshed production audit is dated 2026-10-20T07:29:12.879370+00:00; its OG image is 1200 × 630px. Throttled mobile samples: LCP 1624ms / CLS 0.0000; LCP 1692ms / CLS 0.0000. These are local synthetic measurements, not field Core Web Vitals or a Lighthouse score. The audit retains response headers and runtime observations.

Current revision evidence is in `evidence/apple-dominant-revision/`; the final report is `production-qa.json`. Earlier hospitality, Apple and cinematic reports and deployment receipts remain historical. Browser checks do not establish hotel policy accuracy, live availability or photo rights.

Release evidence: [production audit](../evidence/apple-dominant-revision/production-audit.json), [static-export audit](../evidence/apple-dominant-revision/static-export-audit.json), [this revision's cleanup](../evidence/apple-dominant-revision/cleanup-final.json) and [private deployment status](../evidence/apple-dominant-revision/private-deployment.json). Historical storage and development-output records remain preserved. The preview stays noindex. An approved public domain and route canonical configuration still require launch verification.

Render-cleanup limitation: automatic approval review rejected removal of the verified OTA-document render scratch with the reason 'blocked by policy'. Its 447,116 bytes remain under `research/ota-revision/.document-review/`; no further removal was attempted. The retained source twins and scratch hashes are recorded in `research/ota-revision/source-review-verification.json`. Final handoff render evidence is retained with `docs/handoff-verification.json`.

A separate 29,539-byte generated handoff bytecode file was also rejected for cleanup by automatic approval review. It remains retained; no retry is part of this revision. Current scoped cleanup records preserve all source, licensed assets and review evidence.

## Security and maintenance

The recorded production dependency audit has 0 vulnerabilities. The full audit records 5 high findings from one development-only ESLint chain ending in braces 3.0.3. [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) had no official patched release at the 19 October 2026 review. Keep the lockfile, recheck upstream and do not force-downgrade Next.js to silence it. Details: [security review](../evidence/security-review.json).

StayBar/dock pass dates, party size, requested room count and preference through the contact URL; these may remain in browser history. Names and personal notes stay off that URL. On contact, dock submission retains current room/count/children and applies the dock's dates/adults. Query changes update the existing form without remounting it, preserve unfinished name/notes and clear stale errors and prepared drafts. Stay/group/dining forms prepare explicit WhatsApp drafts without storage or silent sending. The map loads only on activation. No payments or analytics are installed. Preserve security headers, Hotel JSON-LD, local fonts and OG metadata.

Tailwind uses `source(none)` with explicit app/components/content paths. Preserve that scan boundary: a previous broad scan panicked on a transient Word file during hot development. Generated documents and research are excluded.

## Primary reference links

Visual hierarchy: [Lando Norris](https://landonorris.com/), [Apple](https://www.apple.com/), [Linear](https://linear.app/). Hospitality: [Casa Angelina](https://www.casangelina.com/), [Hotel Vagmi](https://hotelvagmi.com/), [The Drake on Awwwards](https://www.awwwards.com/sites/the-drake-hotel). Facts: [MakeMyTrip](https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html), [temple visitor portal](https://www.shrikashivishwanath.org/). Credits: [Pradum Shukla temple photo](https://commons.wikimedia.org/wiki/File:Kashi_Vishwanath_Temple_in_2025.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [Unsplash licence](https://unsplash.com/license).

Regenerate both handoff files with: python -B scripts/generate_handoff.py. The generator uses python-docx and verifies that its DOCX can be reopened.
