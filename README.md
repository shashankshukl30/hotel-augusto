# Hotel Augusto, Varanasi

An independent Digiocular client website in `D:\Digiocular\Websites\Hotel Augusto`.

The latest 20 October brief puts Lando Norris first for bold composition and memorable motion, with Apple and Linear informing clear controls and precise interaction. The shared system uses local Inter, near-white/cool-gray surfaces, charcoal and cobalt actions. The site has 17 hospitality routes, three room categories, comparison, vegetarian dining, group accommodation enquiries, city planning, galleries, arrival guidance and persistent date controls. The supplied `logo.jpeg` appears in the header, footer, favicon, OG image and dining guide.

The homepage opens with nearly full-viewport genuine property photography and the large left-aligned “Your place / in Kashi.” headline. Scene and pause controls sit inside the photograph; scene changes wait for image readiness. Spring-driven pointer drift and native scroll scaling provide motion, with independent hover/focus pause and reduced-motion support. The ink-blue city chapter combines oversized decorative KASHI lettering, genuine river imagery and manual tabs. The [implementation plan](docs/plans/2026-10-19-website.md) records this frozen composition; [Linear source notes](research/apple-dominant-revision/linear-reference.json), the [hotel reference study](research/hospitality-revision/reference-study.md) and [Casa Angelina study](research/apple-dominant-revision/casa-angelina-reference.json) retain source context. Release acceptance follows the current source's production evidence.

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

- `/` — property-led hero, dated enquiry, all three room categories, dining, city itinerary, review links, gallery, arrival, FAQs and stay guides
- `/hotel` — genuine hotel spaces, detailed facilities and arrival planning
- `/dining` — vegetarian restaurant, room service, specific dining enquiry and downloadable planning guide
- `/group-stays` — family, friends and business accommodation requests; requested rooms, total party size and optional company/billing details
- `/rooms` — all room categories and real photographic introductions
- `/rooms/compare` — factual bed-layout and feature comparison, including a two-room mobile selector
- `/rooms/deluxe-room`, `/rooms/deluxe-twin-room`, `/rooms/family-room`
- `/varanasi` — destination guide and a self-directed four-stage city itinerary
- `/gallery` — filterable gallery with keyboard and swipe support
- `/guides` — practical stay-guide index
- `/guides/first-visit-to-kashi`, `/guides/arriving-in-godowlia`, `/guides/choosing-your-room`
- `/contact` — date/guest/room enquiry, phone, arrival tabs, address copy, optional Google map and FAQs
- `/privacy` — enquiry privacy and licensed destination photograph credits

## Content and booking

`content/hotel.ts` owns core hotel facts, rooms and the booking phone number. `content/hospitality.ts` adds sourced facilities, arrival guidance, practical FAQs and review-profile links; `content/guides.ts` contains the three stay guides. `content/social-proof.ts` holds the dated Google snapshot and proximity links. Room image mappings are in `content/room-images.ts`. Photo provenance and retained originals are in `research/assets/` and `research/ota-revision/`; licensed destination photography also has records in `research/awwwards-revision/`. The source ledger includes Google and MakeMyTrip; the supplied MMT hotel ID is `201909301024364424`. Research documents include DOCX twins.

The exact dated MakeMyTrip route returned a browser transport error; its indexed canonical property page corroborated stable facts. Google property photos were opened and mapped to the site. These distinctions and individual asset sources are recorded in `research/ota-revision/`; no live MMT availability was established.

The client confirmed **+91 80817 09146** for WhatsApp and **aromaofkashi@gmail.com** for email enquiries on 21 October. Both are centralized in `content/hotel.ts`. The navbar, mobile menu and rightmost booking-dock chat link use that WhatsApp number. Chat has its own space beside availability and never floats over the hero photograph. No enquiry is sent during automated testing.

The universal `BookingDock` keeps dates and “Check availability” accessible across routes. Its measured height reserves bottom space so the footer remains reachable. Dated `StayBar` and enquiry forms support 1–8 requested rooms and night summaries. Validated dates, party size, room count and room preference travel to contact through the URL and may remain in browser history. Names and private notes stay off that URL. `lib/stay-query.ts` validates those preferences; `lib/booking.ts` prepares the explicit WhatsApp handoff. Availability is confirmed by the hotel, not a live inventory engine.

When the dock is used on `/contact`, it keeps the form's current room preference, room count and children while applying the dock's dates/adults. `ContactEnquiry` updates query preferences in the existing `BookingForm` without remounting it, preserving unfinished name and notes fields. Changed preferences clear stale errors and prepared WhatsApp drafts; the guest prepares a fresh draft before opening WhatsApp.

`/group-stays` requests accommodation, with total adults and children, requested rooms and optional company information. Input limits are enquiry limits, not hotel capacity promises. No weddings, banquet facilities or conference services are advertised. The dining form uses `lib/dining-enquiry.ts` to validate the desired date, meal interest and party size.

Stay, dining and group forms send email through FormSubmit when the guest selects **Send enquiry**. `lib/enquiry-email.ts` validates reply details and builds the payload; `components/use-email-enquiry.ts` manages pending requests, a 20-second timeout and failure recovery. The hotel recipient is fixed by configuration. Forms preserve values on failure and prevent repeated pending or unchanged successful submissions. An explicit WhatsApp alternative still prepares a message locally and requires the guest to send it in WhatsApp. The website has no enquiry database; submitted email details are processed by FormSubmit and the recipient's email provider.

FormSubmit requires the recipient to activate the form through its confirmation email. Provider acceptance does not prove inbox delivery. Record activation and a real approved inbox test separately from the mocked browser checks in `evidence/client-handoff-20261021/`. Run `python -B scripts/verify_client_contacts.py --base <URL> --browser chromium` and then `--browser webkit` against HTTPS. Every FormSubmit POST in this suite is intercepted; it never sends an email.

The guest-facing [dining planning PDF](public/downloads/hotel-augusto-dining-guide.pdf) and [editable DOCX](docs/hotel-augusto-dining-guide.docx) are generated together by `python -B scripts/generate_dining_guide.py`. They use the supplied logo and genuine dining photograph, with planning information rather than an invented menu. Both one-page outputs were rendered and inspected; see `evidence/apple-dominant-revision/dining-guide/verification.json`.

The arrival guide loads its Google Maps iframe only after the visitor selects “Load Google map”. Temple and ghat proximity use qualitative walking guidance and direct walking-route links, without fixed travel-time promises. No analytics or social-media feed is installed. A source-specific Google badge records **3.7/5 from 1,628 reviews, checked 20 October 2026**. MakeMyTrip scores conflict across indexed pages and are not displayed. The existing exact Tripadvisor excerpt remains attributed. Evidence is in `research/apple-dominant-revision/conversion-evidence/findings.json` and `research/hospitality-revision/guest-review-evidence.json`. No new guest-photo reuse licence was established; property images are not relabelled as guest portraits.

## Checks

```powershell
npm run lint
npm run typecheck
npm test
npm run build
npm run qa -- --base-url http://127.0.0.1:3080 --output evidence/apple-dominant-revision
python -B scripts/qa_conversion_upgrade.py --base-url http://127.0.0.1:3080 --output evidence/apple-dominant-revision
```

Browser QA uses a fresh Microsoft Edge context through Python Playwright and axe-core. Run the production server separately and browser suites sequentially; the focused conversion suite also inspects the prepared static export in `out/`. This revision's results are recorded in `evidence/apple-dominant-revision/production-qa.json`, `conversion-upgrade-qa.json`, `production-audit.json` and `static-export-audit.json`. Read each report's scope, completion time and subsequent-fix notes before treating it as release evidence. Earlier passes do not certify the expanded 17-route source. Tests do not send WhatsApp messages.

The final broad report passed 108 viewport checks, 36 axe audits and 40 interactions. The original conversion report remains 209/211 because two PDF checks expected the wrong title; the separate [dining retest](evidence/apple-dominant-revision/conversion-dining-retest-20261020T073017878694Z.json) passed 13/13 with actual brochure text and download/source hash verification, retaining the original report's SHA256. The handoff keeps these results separate. The room review passed 21 layouts, 10 axe audits and 29 interactions; static-export validation passed 64/64 checks.

Generate matching Markdown and Word handoffs after final verification with `python -B scripts/generate_handoff.py`. The generator reads only this revision's final report, creates both files through the same content blocks, and reopens the DOCX. Final documents must also be rendered and visually checked.

## Launch settings

1. The client confirmed WhatsApp `+91 80817 09146` and enquiry email `aromaofkashi@gmail.com`. FormSubmit recipient activation and a real inbox test remain separate launch checks.
2. The approved production origin is `https://hotelaugusto.in`. Set `NEXT_PUBLIC_SITE_URL` to that origin.
3. Keep `SITE_INDEXABLE=false` for previews; set it to `true` only for approved production. This controls robots and sitemap output.
4. Push this independent Git repository before any Vercel deployment. The owner authorized public visibility on 21 October 2026 for the client import; `main` contains the current approved application. The Vercel region is configured as `sin1`.
5. Run the browser checks on the deployed host and verify its canonical/OG URLs before connecting a domain.

The client production project is in Vercel team `sahil-5aa6`, with a public fallback URL at https://hotel-augusto-brown.vercel.app. The local Vercel link targets that client project. Both `hotelaugusto.in` and `www.hotelaugusto.in` are attached, with www redirecting to the apex. Namecheap DNS and custom-domain HTTPS must be verified separately; attaching an alias is not a completed DNS cutover. Current release and handoff evidence is in `evidence/client-handoff-20261021/`.

The client updated Namecheap on 21 October: apex A `76.76.21.21`, www CNAME `a2ab83b9e7357c0b.vercel-dns-017.com`. Vercel accepts both records; validated certificates now serve the apex with HTTP 200 and www with a 308 redirect to the apex. Some DNS resolvers may retain the earlier parking records until their cached TTL expires. Evidence is in `domain-tls-diagnostic.json` and `domain-vercel-confirmation.json`. Mail/MX/TXT records were not changed. Reinspect Vercel's current recommendation before any later DNS change. The client's GitHub Login Connection is not configured, so releases are pushed to GitHub and then deployed through the authenticated Vercel CLI; automatic Git deployments remain unconnected.

## Private preview

An owner-private Sites preview is configured for [Hotel Augusto](https://hotel-augusto.candy-okapi-4696.chatgpt.site). Current publication status is recorded in `evidence/apple-dominant-revision/private-deployment.json`; the public hotel launch remains separate. Earlier deployment records remain historical. The existing Sites project is recorded in `.openai/hosting.json`; reuse it rather than creating a new site.

Normal Next.js/Vercel operation remains the default. To produce the optional static preview bundle:

```powershell
$env:SITE_STATIC_EXPORT = "true"
npm run build
Remove-Item Env:\SITE_STATIC_EXPORT
```

This writes `out/` and uses `lib/static-image-loader.ts` with generated local WebP sizes for responsive static delivery. Normal Next deployments retain AVIF/WebP image optimization. After adding or replacing a photograph, run `python -B scripts/generate-responsive-images.py` to refresh `content/responsive-images.json` and its provenance report; originals are retained and never upscaled. The static host supplies HTTP response headers. Keep preview indexing disabled and verify deployed behavior before sharing. Public launch and domain connection remain separate.

## Security and maintenance

The retained 19 October dependency review reported no production vulnerabilities and an unresolved development-only `braces` advisory; see `evidence/security-review.json`. Treat that as a dated review and recheck upstream during release verification. Do not force-downgrade Next.js to silence the report.

Security headers, hotel JSON-LD, a 1200×630 OG image, local fonts and responsive images are implemented. Their recorded release checks are in this revision's verification reports. Keep the lockfile and licensed photograph credits. All source and working dependencies remain in this one project folder. Scoped cleanup is recorded in `evidence/apple-dominant-revision/cleanup-final.json`; preserve historical evidence and known retained artifacts.

Tailwind uses `source(none)` with explicit `@source` paths for app, components and content. Preserve this boundary: a previous broad scan encountered a transient Word file and panicked during hot development. Generated documents and research remain outside the source scan.
