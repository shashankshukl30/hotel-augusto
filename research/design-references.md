# Hotel Augusto: design reference study

**Superseded:** The user rejected the serif/terracotta direction. The current design contract is [apple-direction.md](apple-direction.md). This file remains as a record of the initial Awwwards research only.

Research date: 19 October 2026. Direction is original; references supply principles, not reusable designs, copy, or hotel imagery.

## References actually inspected

### Masia Mont Rural — editorial hierarchy and mobile composition

- Awwwards Honorable Mention, 21 September 2026: https://www.awwwards.com/sites/masia-mont-rural
- Live site identified: https://mont-rural.emblematica.agency/
- Award hero: https://www.awwwards.com/inspiration/hero-block-masia-mont-rural
- Award mobile example: https://www.awwwards.com/inspiration/mobile-masia-mont-rural
- Visually inspected the award's supplied desktop and mobile images. A live visit reached a loading screen; a later network-idle attempt timed out, so live animations were not validated.
- Useful principle: a large serif headline can work as a composition across the page, with small factual text placed on a different axis. Large photographs follow actual content hierarchy. The mobile layout changes text placement and image proportions instead of shrinking the desktop.
- Apply to Augusto: a deliberate headline and location note on warm paper, followed by a generous actual property photograph. Retain hospitality warmth without importing Catalan vineyard illustrations or exaggerated ornamental typography.

### Grand Hotel Miramare — booking visibility and room storytelling

- Awwwards Honorable Mention, 20 March 2024: https://www.awwwards.com/sites/grand-hotel-miramare
- Live website: https://www.grandhotelmiramare.it/en/
- Room reference: https://www.awwwards.com/inspiration/informative-room-presentation-grand-hotel-miramare
- Visually inspected the live desktop and mobile first viewport and the award's room-page image. The live page title identifies Grand Hotel Miramare; main heading reads “Celebrate the Estate Italiana.”
- Useful principle: highly memorable photography and typography coexist with an always discoverable booking action. The room page is a photographic chapter with meaningful room information beneath it, rather than a product-card grid.
- Apply to Augusto: strong full-width or asymmetric real room photographs, crisp editorial headings, clear category labels and room-specific WhatsApp enquiry actions. Do not imitate Miramare's script font, seaside imagery, five-star status, or hospitality claims.

### Vesper Hotel — useful structural reference, with age caveat

- Awwwards nominee, 12 November 2014: https://www.awwwards.com/sites/vesper-hotel
- Current live website: https://www.vesperhotel.com/
- Read current content and inspected computed type styles. Current display face is Domaine Display and body is Proxima Nova. The captured hero media had not resolved, so it is not a reliable visual-quality benchmark for the current build.
- Useful principle: rooms, dining, and the local destination can share an editorial rhythm with distinct photography. An old award entry does not establish that the current website is the originally awarded design.

## Augusto direction

Recommended direction: a well-made address in old Varanasi. Warm ivory, dark ink, and one restrained terracotta accent; Libre Bodoni display typography paired with Public Sans. Let the real property photography and city context carry the atmosphere. The website's premium craft must not imply that Augusto is a palace, riverfront estate, or five-star resort.

The location is a real strength: current Google Hotels and Booking.com listings place the property in Jangambari/Godowlia and discuss access to the temple and ghats. Exact walking times, river views, facilities, and room benefits must come from the separate property fact-check. Do not turn destination images into apparent hotel views.

- Desktop: broad margins, asymmetric title/photo relationships, an identifiable image cadence, fine rules and small section numbers. Make each section composition purposeful; avoid repeating the same two-column block six times.
- Mobile: shorter headline measures, portrait crops selected for their subject, condensed navigation, and a reachable WhatsApp action. Room facts and booking actions should remain together. Gallery becomes a considered two-column photographic index with occasional full-width moments.
- Motion: one composed entrance with a short image reveal and slight headline rise; soft opacity/translate entrances for sections; deliberate gallery transitions. No scroll hijacking, compulsory loader, cursor replacement, continuously moving text, or animation that delays booking. Honor reduced motion.
- Booking now: label the action honestly as “Book on WhatsApp” or “Enquire on WhatsApp.” Pre-fill room/date information only when supplied by the guest. A date selector may compose an enquiry but must never pretend to return availability. Keep the phone destination in one configuration field for later engine integration.
- Photographs: use real hotel photographs locally optimized, with provenance retained. Use wide images where image quality supports it; avoid enlarging small OTA thumbnails to full screen. Show city photography inside an explicitly labeled Varanasi section.
- Information architecture: Home, Rooms, Gallery, Varanasi, Contact. Each page answers a distinct booking question; leave detailed policies to verified information. Provide direct room enquiry links, directions, and accessible telephone contact.

## Traps to avoid

1. Decorative “luxury” vocabulary unsupported by the actual property: sanctuary, palace, bespoke experience, riverfront, spa, award-winning.
2. A centered stock-photo hero with four trust counters and three identical amenity cards.
3. Fabricated reviews, inflated stars, unverified prices, permanently displayed scarcity, or copied OTA marketing paragraphs.
4. Giant typography that hides the property name, crops unpredictably, or wraps tracked labels into two lines.
5. A green floating WhatsApp bubble as the only understandable booking path; the intent belongs in the main navigation and page content too.
6. Empty visual polish: redundant rounded containers, ornamental gradients, excessive grain, or low-contrast beige text.
7. Misusing destination imagery as an implied room view, or replacing real hotel assets with generated architecture.

## Property context sources used for design positioning

- Google Hotels: https://www.google.co.in/travel/hotels/entity/ChkI9IOdtNaKmJZrGg0vZy8xMWI2ZGc2bWszEAE
- Booking.com: https://www.booking.com/hotel/in/augusto-varanasi1.en-gb.html
- MakeMyTrip: https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html

Property data, booking numbers, room naming and policy conflicts are owned by the parallel hotel research work. This document does not override those findings.

## Evidence files

Kept locally in research: masia-hero-reference.jpg, masia-mobile-reference.jpg, miramare-room-reference.jpg, miramare-desktop.png, miramare-mobile.png. These are design research only and must not be shipped as Augusto customer-facing assets. Failed/partial loading screenshots are disposable and are removed during task cleanup.

Agent Reach check: installed version 1.5.0 reported current on 19 October 2026.
