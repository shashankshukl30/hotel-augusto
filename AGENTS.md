# Hotel Augusto

Private client project. Work only within this folder. Parent workspace rules apply.

## Project constraints
- Genuine Hotel Augusto, Varanasi photography only for the property. Destination photos must be labelled as Varanasi, never represented as room views.
- Verify website facts against `research/`. Do not invent rates, reviews, star classification, distances, policies, room capacity, river views, or facilities.
- Centralize contact/booking settings in `content/hotel.ts`; leave the booking-engine adapter replaceable.
- Next.js 16, strict TypeScript, Tailwind v4, Framer Motion. Static server-rendered pages, small client interaction components. No backend or database needed for WhatsApp enquiries.
- Latest correction: combine Apple clarity with original Awwwards-inspired hospitality art direction, rather than an Apple replica. Build a visibly multi-page hotel website with a cinematic, photographic hero. Use Manrope display and Inter body, bone/ink/verdigris, confident asymmetric compositions and purposeful accessible motion. The earlier serif/terracotta and literal Apple layouts were rejected. Dedicated /hotel and /dining pages join rooms/details, Varanasi, gallery and contact. Every navigation destination is a real route. Inspect both the Google profile and MakeMyTrip hotelId 201909301024364424 supplied by the user; preserve source-to-page/photo mapping.
- Read `docs/plans/2026-10-19-website.md` and research notes before revising the design.
- Browser verification at mobile and desktop sizes is mandatory. Verify keyboard, reduced motion, navigation, image gallery, enquiry validation, and WhatsApp destination.
- Preserve image provenance, editable source, lockfile, evidence and task-owned cleanup audit.

<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
