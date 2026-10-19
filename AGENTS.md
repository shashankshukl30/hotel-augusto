# Hotel Augusto

Private client project. Work only within this folder. Parent workspace rules apply.

## Project constraints
- Genuine Hotel Augusto, Varanasi photography only for the property. Destination photos must be labelled as Varanasi, never represented as room views.
- Verify website facts against `research/`. Do not invent rates, reviews, star classification, distances, policies, room capacity, river views, or facilities.
- Centralize contact/booking settings in `content/hotel.ts`; leave the booking-engine adapter replaceable.
- Next.js 16, strict TypeScript, Tailwind v4, Framer Motion. Static server-rendered pages, small client interaction components. No backend or database needed for WhatsApp enquiries.
- Latest client correction overrides the initial design: use Apple design, Awwwards-level execution. The client rejected the serif, terracotta and editorial layout as AI slop. Use crisp Inter variable typography, almost-white/gray/ink surfaces, a single blue accent, precise rounded photography, capsule CTAs and purposeful motion. No ornamental serif identity, tiny tracked caps, section numbering or generic poetic copy. Rebuild the composition, not merely the colors.
- Read `docs/plans/2026-10-19-website.md` and research notes before revising the design.
- Browser verification at mobile and desktop sizes is mandatory. Verify keyboard, reduced motion, navigation, image gallery, enquiry validation, and WhatsApp destination.
- Preserve image provenance, editable source, lockfile, evidence and task-owned cleanup audit.

<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
