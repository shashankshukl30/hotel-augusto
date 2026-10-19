# Hotel Augusto — cinematic hospitality direction

Reviewed 19 October 2026. This study responds to the user's correction: use creative judgment and Awwwards alongside Apple's clarity. The result should be a distinctive, unmistakably multipage hotel website. The former literal Apple treatment is no longer the visual brief.

## Three live references

### The Drake: identity inside the photograph

[Awwwards, Site of the Day, 2 September 2025](https://www.awwwards.com/sites/the-drake-hotel) · [Live site](https://thedrake.ca/) · [Designer case study](https://locomotive.ca/en/work/the-drake-hotel)

Desktop and mobile were opened and captured in fresh Edge contexts. Its full-bleed media creates atmosphere immediately. The large title sits low and left; the navigation occupies a deliberate separate layer. The mobile composition changes the navigation and keeps the main identity readable. Take the confidence of scale and the connection between brand and photography. Augusto should not imitate the boxed word treatment, dense navigation geometry, or nightlife positioning.

Evidence: drake-1440-hero.png, drake-390-hero.png, drake-1440-section.png.

### Kaskady: a hotel with visible destinations

[Awwwards, Honorable Mention, 1 September 2023](https://www.awwwards.com/sites/hotel-spa-resort-kaskady) · [Live site](https://www.resortkaskady.com/)

The current desktop header exposes Rooms, Gallery, Contact, and other actual destinations. Booking remains separate and visible. On mobile, Menu and Booking remain understandable while the hero becomes a portrait composition. Take this clarity of information architecture, persistent booking access, and contrast between immersive media and quieter content. Do not borrow its serif headings, badges, chapter numerals, or hotel-specific amenities and claims.

Evidence: kaskady-1440-hero.png, kaskady-390-hero.png, kaskady-1440-section.png.

### Casa Cook: the location provides the atmosphere

[Awwwards, Honorable Mention, 16 May 2019](https://www.awwwards.com/sites/casa-cook-hotels) · [Live site](https://casacook.com/)

The current site was inspected after dismissing its consent dialog. Large environmental media carries the first impression, followed by restrained pale surfaces and photographic property previews. Mobile keeps a direct booking action available. Take the visual relationship between landscape and a place to stay, and the calm transition after an immersive opening. Augusto needs more visible desktop page links than Casa Cook's collapsed navigation. The award is historical; these captures document today's site, not a claim that its current implementation is the 2019 award version.

Evidence: casa-cook-1440-hero.png, casa-cook-390-hero.png, casa-cook-1440-section.png. Initial consent-obscured captures were replaced with the inspected page.

## The hero photograph

Selected: /images/varanasi-hero.webp, a real Varanasi riverfront photograph by Martijn Vonk. [Source photograph](https://unsplash.com/photos/a-group-of-boats-floating-on-top-of-a-river-wloNuC7qKf8) · [Unsplash License](https://unsplash.com/license).

The primary photo page identifies Varanasi and free use under the Unsplash License. The license permits commercial use. Credit the photographer in the site's photo credits. The delivered image is 2800 × 1867, 888,608 bytes, converted to WebP without altering photographic content. Original and file hashes are retained in hero-asset.json. It is destination photography, not a hotel view.

This frame has sunlit architecture rising on the right, a strong orange boat, and open river on the left. It gives the left headline space while making Varanasi recognizable. It replaces the initial hero recommendation: the existing varanasi-ghats.webp has a large foreground advertisement and hazy empty sky that become distracting at full-screen scale. The new photograph was visually inspected before delivery.

## Original composition for Augusto

- Desktop: full-bleed image at approximately 1440 × 850–900; object-position 50% 55%. Place text on the left within a 6% gutter and retain the architecture on the right. Use a localized dark ink veil for white text, fading toward the image subject. Keep the river's natural color and detail visible rather than placing a uniform opaque wash over it.
- Typography: Manrope display, Inter body. A 104–136px desktop headline with approximately 1.0 line-height and tight, deliberate tracking creates the main gesture. Keep it to two or three short lines. Mobile display is approximately 60–72px, selected against the actual copy and 342px content width. Keep body text at 16–18px.
- Property anchor: a small real Deluxe Room inset at the lower right, around 264px wide, labelled At Hotel Augusto and linked to /rooms. Place it below the boat's main silhouette. On mobile, move it into a short horizontal room-preview strip beneath the photograph; do not float a second photograph over the headline or booking action.
- Mobile: object-position approximately 63% 55% retains the architecture and boat. Use a deliberate portrait crop, a compact readable header, and a visible booking action. The composition study verifies 390px with zero horizontal overflow. Judge the final crop against the final headline, not these coordinates alone.
- Color: bone backgrounds, deep green-black ink, restrained verdigris actions. The city photograph supplies warmth. Use small 4–8px photo corners or square edges, not a page of identical oversized rounded panels.
- Motion: one composed entrance, with the photograph settling from scale 1.035 to 1 and the title moving about 16–24px. Keep navigation and booking immediately usable. Reduced motion shows the final state without travel. Do not add simulated video, generated hotel scenes, compulsory loaders, or scroll hijacking.

hero-crop-1440.png and hero-crop-390.png are browser-rendered composition studies with the actual new asset; crop-preview.html is research only. The headline in that study is a placement test, not approved production copy.

## Make the multiple pages obvious

Keep Rooms, Varanasi, Gallery, and Contact visible in the desktop navigation. Use actual route links, an active-page state, and a clearly separate booking action. The mobile menu should expose the same page names in a readable list rather than forcing guests to infer icon meanings.

The homepage should preview the property, room choices, and location, then link into their complete pages. Each destination needs its own opening composition and purpose: Rooms for room selection, Gallery for visual inspection, Varanasi for a city guide, Contact for the address and booking inquiry. Avoid reproducing every page's full content on the homepage; this makes a real multipage build feel like a long single-page template.

## Verification and provenance

All three references were captured at 1440px and 390px; live-inspection.json records landed URLs and page titles. The two crop studies loaded both real photographs and returned equal body/client widths. Search used agent-reach via Exa; pages were read through Jina with a web-reader fallback for blocked Unsplash pages, and visually inspected in fresh Edge. Agent Reach v1.5.0 reported current. No application code was changed for this study; the only public addition was the explicitly authorized new hero asset.
