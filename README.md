# Hotel Augusto, Varanasi

An independent Digiocular client website in `D:\Digiocular\Websites\Hotel Augusto`.

The current direction follows the user's latest 20 October brief: bring most Hotel Vagmi elements into Augusto's own hotel identity and experience. Genuine Augusto photographs lead a 16-page hospitality website, with Bodoni Moda display at weight 400, Manrope body, ivory surfaces, ink-blue text and bronze details. All three room categories are visible, alongside restaurant information, city planning, arrival guidance and dated stay enquiries. Motion includes controlled photo transitions and reveals, with reduced-motion support and native scrolling. See the [reference study](research/hospitality-revision/reference-study.md), [feature and fact plan](research/hospitality-revision/content-journey-plan.json) and [implementation plan](docs/plans/2026-10-19-website.md).

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
- `/dining` — vegetarian restaurant, room service and three meal-enquiry choices
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

`content/hotel.ts` owns core hotel facts, rooms and the booking phone number. `content/hospitality.ts` adds sourced facilities, arrival guidance, practical FAQs and review-profile links; `content/guides.ts` contains the three stay guides. Room image mappings are in `content/room-images.ts`. Photo provenance and retained originals are in `research/assets/` and `research/ota-revision/`; licensed destination photography also has records in `research/awwwards-revision/`. The source ledger includes Google and MakeMyTrip; the supplied MMT hotel ID is `201909301024364424`. Research documents include DOCX twins.

The exact dated MakeMyTrip route returned a browser transport error; its indexed canonical property page corroborated stable facts. Google property photos were opened and mapped to the site. These distinctions and individual asset sources are recorded in `research/ota-revision/`; no live MMT availability was established.

The current WhatsApp destination is the hotel's Google-listed telephone, **+91 80817 09146**. The public WhatsApp link resolves to that number. The hotel must confirm it is the desired, active booking account before public launch. No enquiry was sent during testing.

The dated StayBar validates dates and guest counts, then carries only dates, party size and room preference to the contact page through its URL. Those preferences may remain in browser history. Names and private notes stay off the URL. The enquiry form prepares an encoded message for the visitor to review and explicitly open in WhatsApp. It does not check live inventory, confirm a reservation, process payments or save enquiries to a database. `lib/stay-query.ts` validates the page-to-page preferences; `lib/booking.ts` is the integration point for a future booking engine.

The arrival guide loads its Google Maps iframe only after the visitor selects “Load Google map”. No analytics or social-media feed is installed. Review-profile links and one short, exact Tripadvisor guest excerpt are backed by retained source evidence; no numerical ratings are promoted. The excerpt, attribution and individual review link are recorded in `research/hospitality-revision/guest-review-evidence.json`. Services, meal inclusions, access requirements and policies should be confirmed with the hotel when relevant.

## Checks

```powershell
npm run lint
npm run typecheck
npm test
npm run build
python scripts/qa_hospitality_revision.py --base-url http://127.0.0.1:3080
```

Browser QA uses a fresh Microsoft Edge context through Python Playwright and axe-core. The completed [production report](evidence/hospitality-revision/production-qa.json) records 102 viewport checks, 34 axe audits and 40 interaction checks with zero failures. Lint, typecheck, four booking unit cases, static export and the normal production build also passed. Current evidence belongs in `evidence/hospitality-revision/`. Earlier Apple and cinematic reports remain historical and do not certify this revision. Tests do not send WhatsApp messages.

Generate matching Markdown and Word handoffs after final verification with `python scripts/generate_handoff.py`. The generator reads only this revision's final report, creates both files through the same content blocks, and reopens the DOCX.

## Launch settings

1. Confirm the WhatsApp booking number, current guest policies and permission to reuse the hotel photographs collected from public listings.
2. Supply the approved production domain. Set `NEXT_PUBLIC_SITE_URL` to its HTTPS origin.
3. Keep `SITE_INDEXABLE=false` for previews; set it to `true` only for approved production. This controls robots and sitemap output.
4. Push this independent private Git repository before any Vercel deployment. The Vercel region is configured as `sin1`.
5. Run the browser checks on the deployed host and verify its canonical/OG URLs before connecting a domain.

No production domain has been changed. Old hotel domains were not assumed to be authoritative: one no longer resolves, and another redirects through an affiliate.

## Private preview

An owner-private Sites preview is configured for [Hotel Augusto](https://hotel-augusto.candy-okapi-4696.chatgpt.site). Current publication status is recorded in [the deployment record](evidence/hospitality-revision/private-deployment.json); the public hotel launch remains separate. The existing Sites project is recorded in `.openai/hosting.json`.

Normal Next.js/Vercel operation remains the default. To produce the optional static preview bundle:

```powershell
$env:SITE_STATIC_EXPORT = "true"
npm run build
Remove-Item Env:\SITE_STATIC_EXPORT
```

This writes `out/`, disables server image optimization for that export, and leaves HTTP response-header configuration to the static host. Keep preview indexing disabled and verify the deployed host before sharing it. A public launch and domain connection remain separate from this private preview.

## Security and maintenance

Production dependencies have no reported npm audit findings as of this build. The development ESLint dependency chain has an upstream `braces` advisory without an available patched release; see `evidence/security-review.json`. Do not force-downgrade Next.js to silence that report.

Security headers, hotel JSON-LD, a 1200×630 OG image, local fonts and responsive images are included. Keep the lockfile and licensed photograph credits. All source and working dependencies remain in this one project folder.
