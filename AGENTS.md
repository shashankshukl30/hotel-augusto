# Hotel Augusto

Private client project. Work only within this folder. Parent workspace rules apply.

## Project constraints
- Genuine Hotel Augusto, Varanasi photography only for the property. Destination photos must be labelled as Varanasi, never represented as room views.
- Verify website facts against `research/`. Do not invent rates, reviews, star classification, distances, policies, room capacity, river views, or facilities.
- Centralize contact/booking settings in `content/hotel.ts`; leave the booking-engine adapter replaceable.
- Next.js 16, strict TypeScript, Tailwind v4, Framer Motion. Static server-rendered pages, small client interaction components. No backend or database needed for WhatsApp enquiries.
- Latest correction (20 October): the user wants most Hotel Vagmi elements in Augusto's own style and UI/UX. The fuller hotel journey supersedes the previous Apple product-like composition. Use Bodoni Moda display at400 with selective italics, Manrope body, warm ivory, deep ink blue and bronze OKLCH tokens. Preserve clarity, large readable controls and generous imagery. Lead with genuine Augusto room/lounge/restaurant photography. Home includes welcome, all three room categories, dining, city itinerary, review source links, gallery, arrival guidance, FAQs, guides and a dated enquiry close. Keep16contentroutes including room comparison and three practical guide articles. Borrow no Vagmi-specific rates, offers, policies, reviews, branding or facilities. Motion must enrich the experience, respect reduced motion and preserve native scrolling. Google profile and MakeMyTrip hotelId201909301024364424 remain primary hotel evidence; preserve source-to-page/photo mapping.
- Read `docs/plans/2026-10-19-website.md` and research notes before revising the design.
- Browser verification at mobile and desktop sizes is mandatory. Verify keyboard, reduced motion, navigation, image gallery, enquiry validation, and WhatsApp destination.
- Preserve image provenance, editable source, lockfile, evidence and task-owned cleanup audit.
- Current release browser suite is `scripts/qa_hospitality_revision.py`; older Apple-specific suites remain historical evidence. Run browsers sequentially to avoid memory pressure.

<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
