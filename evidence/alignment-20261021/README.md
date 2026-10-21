# Alignment revision - 21 October 2026

This revision preserves the approved visual direction and fixes the supplied Safari screenshot concerns across the shared layout system.

## Changes

- One content width and responsive gutter scale for the main, room and hospitality wrappers.
- Stable photo frame edges with native-scroll motion inside the image; amenities meet the lounge photograph edges.
- Matching itinerary heading/detail columns and a top alpha mask that blends KASHI into the photograph, including reduced-motion mode.
- Matching dining introduction, enquiry and FAQ columns.
- Compact forms respond to their own available width. The homepage enquiry section becomes one column at 800px; 601-768px date text no longer overlaps calendar triggers.
- Consistent date prompt/native-value insets and wrapping prepared group enquiry buttons.

## Local verification

- Production build and ESLint succeeded; all 18 unit tests passed.
- `local-alignment.json`: all 17 routes at 320, 390, 768, 1024, 1440 and 1920px. No horizontal overflow, suspicious content overflow or JavaScript runtime errors. The initial harness reported 19 false positives; `audit-notes.json` preserves and explains every flag. The harness was then corrected to distinguish intentional hero/centred layouts and different stacked control rows.
- `visual-review.json`: 34 full-page captures visually inspected (17 routes at 390 and 1440px), plus the supplied problem areas. Narrow homepage states were investigated separately.
- `home-compact-before.json` and `home-compact-after.json`: the additional real date-label regression failed 8 checks before the fix and passed all 34 afterwards.
- `production-states.json`: empty, invalid and prepared contact/group/dining enquiries, compact home forms and tablet room forms. Its 3 dining-column failures led to the final dining alignment fix. Two 1100px room assertions incorrectly assumed the container was below 400px; the harness now tests actual available width. `production-states-rerun.json` reruns both affected routes on the final build: 85 passed, zero failures/runtime errors.
- `production-motion.json`: 41 checks passed, including actual photo movement within fixed frames, hero/gallery/city motion, keyboard/touch navigation, all 17 mobile routes, reduced motion, failed image fallback and no-JavaScript content.

No enquiry was sent and no WhatsApp link was opened. Browser engine emulation does not constitute a physical Mac/iPhone test. Hosted WebKit verification and deployment receipts are recorded separately when completed.

Motion prompt library references reviewed: `cipherwrk-451155` and `deeprajo1-623150`. Existing Framer Motion/native scrolling retained; no reference artwork, copy or external animation engine was added.
