# Alignment revision - 21 October 2026

This revision preserves the approved visual direction and fixes the supplied Safari screenshot concerns across the shared layout system.

## Changes

- One content width and responsive gutter scale for the main, room and hospitality wrappers.
- Stable photo frame edges with native-scroll motion inside the image; amenities meet the lounge photograph edges.
- Matching itinerary heading/detail columns and a top alpha mask that blends KASHI into the photograph, including reduced-motion mode.
- Matching dining introduction, enquiry and FAQ columns.
- Compact forms respond to their own available width. The homepage enquiry section becomes one column at 800px; 601-768px date text no longer overlaps calendar triggers.
- Consistent date prompt/native-value insets and wrapping prepared group enquiry buttons.
- Deployment-safe photo credits: the privacy page reads generated `content/photo-credits.json`. Research remains outside deployment uploads. `npm run credits:sync` regenerates the five published credits; its `--check` mode detects drift. The previous CLI packaging failure is retained in `deploy-packaging-failure.txt`, and exact field/order/source-hash preservation is verified in `photo-credits-validation.json`.

## Local verification

- Production build and ESLint succeeded; all 18 unit tests passed.
- `local-alignment.json`: all 17 routes at 320, 390, 768, 1024, 1440 and 1920px. No horizontal overflow, suspicious content overflow or JavaScript runtime errors. The initial harness reported 19 false positives; `audit-notes.json` preserves and explains every flag. The harness was then corrected to distinguish intentional hero/centred layouts and different stacked control rows.
- `visual-review.json`: 34 full-page captures visually inspected (17 routes at 390 and 1440px), plus the supplied problem areas. Narrow homepage states were investigated separately.
- `home-compact-before.json` and `home-compact-after.json`: the additional real date-label regression failed 8 checks before the fix and passed all 34 afterwards.
- `production-states.json`: empty, invalid and prepared contact/group/dining enquiries, compact home forms and tablet room forms. Its 3 dining-column failures led to the final dining alignment fix. Two 1100px room assertions incorrectly assumed the container was below 400px; the harness now tests actual available width. `production-states-rerun.json` reruns both affected routes on the final build: 85 passed, zero failures/runtime errors.
- `production-motion.json`: 41 checks passed, including actual photo movement within fixed frames, hero/gallery/city motion, keyboard/touch navigation, all 17 mobile routes, reduced motion, failed image fallback and no-JavaScript content.
- `calendar-chromium.json`: 78 touch-opening, deliberate selection, dismissal and virtual-click checks passed, with no runtime errors.

No enquiry was sent and no WhatsApp link was opened. Browser engine emulation does not constitute a physical Mac/iPhone test.

The first hosted sweep (`hosted-webkit.json`) completed all 17 mobile routes without a layout/runtime finding, then timed out on `/hotel` at 1024px while waiting for `networkidle`. A separate HTTP request returned the hotel page with status 200 in 424ms. This did not establish a cause or replace browser verification. The alignment harness now waits for DOM content, the main element and fonts, then performs its existing scroll, geometry and interactive checks. Tablet and desktop are rerun in separate browser processes; `hosted-webkit-tablet.json` completed all 17 routes with 139 passing checks and zero failures/runtime errors. The original timeout report is preserved.

Motion prompt library references reviewed: `cipherwrk-451155` and `deeprajo1-623150`. Existing Framer Motion/native scrolling retained; no reference artwork, copy or external animation engine was added.

## Hosted verification and release

- All 17 routes passed hosted WebKit geometry checks at 390, 1024 and 1440px. The complete tablet and desktop reports each contain 139 passing checks, zero failures, zero suspicious overflow and zero runtime errors. Mobile results are preserved in the initial hosted report described above.
- `hosted-states-webkit.json`: 234 checks passed. The first 320px contact navigation timed out before form assertions; `hosted-contact-rerun.json` independently repeated the contact route at all five widths with request diagnostics: 67 passed, no failed requests or runtime errors. The initial timeout remains recorded; its cause was not established.
- `calendar-webkit.json`: all 78 calendar opening, intentional selection, dismissal and virtual-click checks passed. Together with Chromium, the two engines passed 156 calendar checks.
- `client-access.json`: 58 checks passed in an anonymous browser context, without access-bypass credentials or custom headers. All 17 routes opened publicly; the preview remains noindex.
- `visual-review.json`: hosted WebKit screenshots were visually reviewed for all 17 mobile routes, 12 desktop routes and three tablet homepage sections. No actionable alignment defects remained in those captures. Local Chromium visual review covered all 17 routes at both 390 and 1440px.
- Published application source: `01e057ef3acfc23049e0bf102a25d717efaa5dfb`, following alignment commit `f2381541e75adc6190b51b1f8b935472064f8d72`.
- READY Vercel deployment: `dpl_6wb3TiM77vMpn6s6udQC9VJHE4TT`; runtime region `sin1`. Stable public preview: https://hotel-augusto-git-preview-vercel-omvitys-projects.vercel.app .
- The final commit contains verification reports and test-harness diagnostics only; application files are identical to the deployed source above. The deployment receipt and machine-readable release record are retained beside this file.
- `cleanup.json` records drive measurements and the task-owned evidence inventory. No files were positively identified as disposable; no files were deleted. Source, dependencies, imagery and reproducible QA evidence were retained.
