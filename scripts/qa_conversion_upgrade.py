"""Focused release QA. One Edge browser; every enquiry stops at its draft URL."""

import argparse
import asyncio
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import fitz
from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
ROUTES = [
    "/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
    "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
    "/gallery", "/guides", "/guides/first-visit-to-kashi",
    "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
    "/contact", "/privacy", "/group-stays", "/does-not-exist",
]
ROOMS = {"deluxe-room": "Deluxe Room", "deluxe-twin-room": "Deluxe Twin Room",
         "family-room": "Family Room"}
WIDTH_CASES = ("dock_validation", "dock_handoff", "multiple_rooms", "social_proof",
               "dining", "group", "image_delivery", "room_preview")
CASE_NAMES = (*WIDTH_CASES, "layout", "hero_focus_pause", "hero_deferred_scene",
              "room_preview_reduced", "static_export")


class ExportPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.preloads = [], []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == "img":
            self.images.append(attributes)
        if tag == "link" and attributes.get("imagesrcset"):
            self.preloads.append(attributes)


class QA:
    def __init__(self, args):
        self.base = args.base_url.rstrip("/")
        self.output = (ROOT / args.output).resolve()
        self.output.mkdir(parents=True, exist_ok=True)
        self.export = (ROOT / args.export_dir).resolve()
        self.cases = list(dict.fromkeys(args.case or []))
        baseline = self.output / "conversion-upgrade-qa.json"
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        self.report_path = self.output / (
            f"conversion-{'-'.join(self.cases)}-retest-{stamp}.json"
            if self.cases else baseline.name)
        self.report = {
            "started": datetime.now(timezone.utc).isoformat(),
            "baseUrl": self.base, "browser": "One fresh headless Microsoft Edge process",
            "runType": "supplemental-retest" if self.cases else "full",
            "requestedCases": self.cases or list(CASE_NAMES),
            "externalMessagesSent": 0, "externalNavigationAttempts": [],
            "checks": [], "runtimeErrors": [], "consoleErrors": [],
            "failedResponses": [], "staticPages": [], "browserClosed": False,
        }
        if self.cases and baseline.is_file():
            payload = baseline.read_bytes()
            previous = json.loads(payload)
            self.report["baselineReport"] = {
                "path": str(baseline), "sha256": hashlib.sha256(payload).hexdigest(),
                "finished": previous.get("finished"), "summary": previous.get("summary"),
                "preservedUnchanged": True,
            }
        self.save()

    def selected(self, name):
        return not self.cases or name in self.cases

    def save(self):
        checks = self.report["checks"]
        self.report["summary"] = {
            "checks": len(checks), "passed": sum(c["passed"] for c in checks),
            "failed": sum(not c["passed"] for c in checks),
        }
        self.report["status"] = "fail" if self.report["summary"]["failed"] else "in-progress"
        self.report_path.write_text(
            json.dumps(self.report, indent=2) + "\n", encoding="utf8")

    def check(self, name, passed, evidence=None):
        self.report["checks"].append({"name": name, "passed": bool(passed), "evidence": evidence})
        self.save()

    async def case(self, name, operation):
        try:
            await operation()
        except Exception as error:
            self.check(name, False, {"exception": str(error)})

    async def context(self, browser, width, reduced="no-preference"):
        context = await browser.new_context(
            viewport={"width": width, "height": 844 if width == 390 else 1000},
            device_scale_factor=1, reduced_motion=reduced, accept_downloads=True,
            timezone_id="Asia/Kolkata",
        )

        async def block_whatsapp(route):
            self.report["externalNavigationAttempts"].append(route.request.url)
            await route.abort()

        await context.route("**://wa.me/**", block_whatsapp)
        page = await context.new_page()
        page.set_default_timeout(12000)
        page.on("pageerror", lambda error: self.report["runtimeErrors"].append(
            {"width": width, "url": page.url, "message": str(error)}))
        page.on("console", lambda message: self.report["consoleErrors"].append(
            {"width": width, "url": page.url, "message": message.text})
            if message.type == "error" and not (
                urlsplit(page.url).path == "/does-not-exist" and "404" in message.text) else None)
        page.on("response", lambda response: self.report["failedResponses"].append(
            {"url": response.url, "status": response.status})
            if response.status >= 400 and urlsplit(response.url).path != "/does-not-exist" else None)
        return context, page

    async def ready(self, page, path):
        response = await page.goto(self.base + path, wait_until="domcontentloaded", timeout=60000)
        await expect(page.locator("h1")).to_be_visible()
        await expect(page.locator(".booking-dock")).to_be_visible()
        await page.evaluate("""async () => {
          document.documentElement.style.scrollBehavior='auto';
          await document.fonts.ready;
          await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
        }""")
        return response

    async def layout(self, page, path, width):
        response = await self.ready(page, path)
        await page.evaluate("""async () => {
          const logos=[...document.querySelectorAll('.brand-artwork img')];
          logos.forEach(image=>image.loading='eager');
          await Promise.allSettled(logos.map(image=>image.decode()));
        }""")
        state = await page.evaluate("""() => {
          const dock=document.querySelector('.booking-dock'),rect=dock.getBoundingClientRect();
          const controls=[...dock.querySelectorAll('input:not([type=hidden]),select,button')];
          const bounds=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,
            top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
          return {dock:bounds(dock),position:getComputedStyle(dock).position,
            innerWidth,clientWidth:document.documentElement.clientWidth,
            bodyWidth:document.body.scrollWidth,padding:parseFloat(getComputedStyle(document.body).paddingBottom),
            visible:getComputedStyle(dock).visibility==='visible'&&getComputedStyle(dock).display!=='none',
            controls:controls.map(e=>({id:e.id,text:e.innerText,...bounds(e)})),
            logos:[...document.querySelectorAll('.brand-artwork img')].map(e=>({
              source:e.currentSrc,width:e.naturalWidth,height:e.naturalHeight,complete:e.complete})),
            count:document.querySelectorAll('.booking-dock').length};
        }""")
        expected = 404 if path == "/does-not-exist" else 200
        controls_fit = all(c["left"] >= 0 and c["right"] <= width + 1 and
                           c["height"] >= 43 and c["width"] >= 43 for c in state["controls"])
        self.check(f"{width} {path}: persistent dock, reserved space and controls", (
            response.status == expected and state["count"] == 1 and state["visible"] and
            state["position"] == "fixed" and state["dock"]["bottom"] <= (844 if width == 390 else 1000) + 1 and
            state["padding"] >= state["dock"]["height"] - 1 and
            state["bodyWidth"] == state["clientWidth"] == width and controls_fit), state)
        self.check(f"{width} {path}: genuine supplied logo decodes in header and footer",
                   len(state["logos"]) >= 2 and all(
                       item["complete"] and item["width"] == item["height"] == 1254 and
                       urlsplit(item["source"]).path == "/brand/logo.jpeg" for item in state["logos"]),
                   state["logos"])
        await page.evaluate("scrollTo(0,document.documentElement.scrollHeight)")
        await page.wait_for_function("""() => {
          const f=document.querySelector('.site-footer').getBoundingClientRect();
          const d=document.querySelector('.booking-dock').getBoundingClientRect();
          return f.bottom<=d.top+1;
        }""")
        footer = await page.evaluate("""() => ({
          footerBottom:document.querySelector('.site-footer').getBoundingClientRect().bottom,
          dockTop:document.querySelector('.booking-dock').getBoundingClientRect().top})""")
        self.check(f"{width} {path}: footer remains reachable above dock",
                   footer["footerBottom"] <= footer["dockTop"] + 1, footer)

    async def dock_validation(self, page, width):
        await self.ready(page, "/")
        dock = page.locator(".booking-dock")
        await dock.locator("button[type=submit]").click()
        await expect(page.locator("#dock-arrival")).to_be_focused()
        self.check(f"{width}: missing dock dates focus the first error",
                   await page.locator("#dock-arrival").get_attribute("aria-invalid") == "true" and
                   await dock.locator("[role=alert]").count() == 1)
        for previous, next_id in [("dock-arrival", "dock-departure"), ("dock-departure", "dock-adults")]:
            await page.locator("#" + previous).focus()
            # Native date controls may expose multiple internal keyboard segments.
            for _ in range(8):
                await page.keyboard.press("Tab")
                if await page.locator("#" + next_id).evaluate("e=>e===document.activeElement"):
                    break
            await expect(page.locator("#" + next_id)).to_be_focused()
        self.check(f"{width}: dock keyboard order follows dates then adults", True)
        await page.locator("#dock-arrival").fill((date.today() - timedelta(days=2)).isoformat())
        await dock.locator("button[type=submit]").click()
        await expect(page.locator("#dock-arrival")).to_be_focused()
        self.check(f"{width}: past dock arrival is rejected",
                   "today or later" in await dock.inner_text())
        arrival = (date.today() + timedelta(days=45)).isoformat()
        await page.locator("#dock-arrival").fill(arrival)
        departure = (date.fromisoformat(arrival) + timedelta(days=1)).isoformat()
        await expect(page.locator("#dock-departure")).to_have_value(departure)
        self.check(f"{width}: check-in automatically provides the following checkout day", True)
        await page.locator("#dock-departure").fill(arrival)
        await dock.locator("button[type=submit]").click()
        await expect(page.locator("#dock-departure")).to_be_focused()
        self.check(f"{width}: reversed or zero-night stay focuses checkout",
                   "after your arrival" in await dock.inner_text())

    async def dock_handoff(self, page, width):
        arrival = (date.today() + timedelta(days=50)).isoformat()
        departure = (date.today() + timedelta(days=53)).isoformat()
        for slug, label in reversed(list(ROOMS.items())):
            await self.ready(page, "/rooms/" + slug)
            await page.locator("#dock-arrival").fill(arrival)
            await page.locator("#dock-departure").fill(departure)
            await page.locator("#dock-adults").select_option("4")
            await page.locator(".dock-submit").click()
            await page.wait_for_url("**/contact?**#enquire")
            await expect(page.locator("#room")).to_have_value(label)
            restored = {key: await page.locator("#" + key).input_value()
                        for key in ["arrival", "departure", "adults", "room"]}
            query = parse_qs(urlsplit(page.url).query)
            self.check(f"{width}: {slug} dock handoff retains dates, adults and room", (
                restored == {"arrival": arrival, "departure": departure, "adults": "4", "room": label} and
                query.get("room") == [slug] and query.get("adults") == ["4"]), {"fields": restored, "query": query})
        updated_arrival = (date.today() + timedelta(days=70)).isoformat()
        updated_departure = (date.today() + timedelta(days=74)).isoformat()
        # These are unsent edits, intentionally newer than the current URL.
        await page.locator("#room").select_option("Family Room")
        await page.locator("#roomCount").select_option("3")
        await page.locator("#children").select_option("2")
        await page.locator("#name").fill("QA & returning guest")
        await page.locator("#notes").fill("Keep our family room request & arrival notes.")
        await page.locator(".booking-form").evaluate("form=>{window.__enquiryBeforeUpdate=form}")
        await page.locator(".booking-submit").click()
        await expect(page.locator("#whatsapp-draft")).to_be_visible()
        await page.locator("#dock-arrival").fill(updated_arrival)
        await page.locator("#dock-departure").fill(updated_departure)
        await page.locator("#dock-adults").select_option("3")
        await page.locator(".dock-submit").click()
        await expect(page.locator("#arrival")).to_have_value(updated_arrival)
        await expect(page.locator("#departure")).to_have_value(updated_departure)
        await expect(page.locator("#adults")).to_have_value("3")
        await expect(page.locator("#whatsapp-draft")).to_have_count(0)
        retained = {key: await page.locator("#" + key).input_value()
                    for key in ["room", "roomCount", "children", "name", "notes"]}
        query = parse_qs(urlsplit(page.url).query)
        self.check(f"{width}: dock update preserves unsent enquiry details without remount", (
            retained == {"room": "Family Room", "roomCount": "3", "children": "2",
                         "name": "QA & returning guest",
                         "notes": "Keep our family room request & arrival notes."} and
            await page.locator(".booking-form").evaluate("form=>form===window.__enquiryBeforeUpdate") and
            query.get("room") == ["family-room"] and query.get("roomCount") == ["3"] and
            query.get("children") == ["2"] and "name" not in query and "notes" not in query),
            {"fields": retained, "query": query})
        self.check(f"{width}: repeated submit on contact refreshes the enquiry fields", True,
                   {"url": page.url, "arrival": updated_arrival, "departure": updated_departure})
        await page.locator(".booking-submit").click()
        draft = page.locator("#whatsapp-draft")
        await expect(draft).to_be_visible()
        message = parse_qs(urlsplit(await draft.get_attribute("href")).query).get("text", [""])[0]
        self.check(f"{width}: regenerated draft includes retained details and updated stay", all(
            value in message for value in ["Family Room", "Rooms requested: 3", "3 adults",
                "2 children", "QA & returning guest", "Keep our family room request & arrival notes."]),
            {"message": message})

    async def multiple_rooms(self, page, width):
        await self.ready(page, "/rooms/family-room")
        bar = page.locator(".stay-bar")
        arrival = (date.today() + timedelta(days=80)).isoformat()
        departure = (date.today() + timedelta(days=83)).isoformat()
        await bar.locator("[name=arrival]").fill(arrival)
        await bar.locator("[name=departure]").fill(departure)
        await bar.locator("[name=roomCount]").select_option("3")
        await bar.locator("[name=adults]").select_option("6")
        await bar.locator("button[type=submit]").click()
        await page.wait_for_url("**/contact?**#enquire")
        await expect(page.locator("#roomCount")).to_have_value("3")
        await page.locator("#name").fill("QA group request")
        await page.locator(".booking-submit").click()
        draft = page.locator("#whatsapp-draft")
        await expect(draft).to_be_visible()
        href = await draft.get_attribute("href")
        parsed = urlsplit(href)
        text = parse_qs(parsed.query).get("text", [""])[0]
        self.check(f"{width}: three-room request survives handoff and WhatsApp draft",
                   parsed.hostname == "wa.me" and parsed.path == "/918081709146" and
                   all(item in text for item in ["Rooms requested: 3", "Family Room", "6 adults"]) and
                   parse_qs(urlsplit(page.url).query).get("roomCount") == ["3"], {"href": href, "message": text})

    async def social_proof(self, page, width):
        await self.ready(page, "/")
        badge = page.locator(".google-review-badge")
        await badge.scroll_into_view_if_needed()
        text, href = await badge.inner_text(), await badge.get_attribute("href")
        self.check(f"{width}: Google badge is dated and links to the property",
                   all(value in text for value in ["3.7", "1,628", "Checked 20 October 2026"]) and
                   urlsplit(href).hostname == "www.google.com" and "HOTEL+AUGUSTO" in href and
                   await badge.get_attribute("target") == "_blank", {"text": text, "href": href})
        await badge.focus()
        self.check(f"{width}: review source is keyboard reachable", await badge.evaluate(
            "e=>e===document.activeElement&&getComputedStyle(e).outlineStyle!=='none'"))

    async def dining(self, page, width):
        await self.ready(page, "/dining")
        form = page.get_by_role("form", name="Dining enquiry", exact=True)
        await form.locator("button[type=submit]").click()
        await expect(page.locator("#dining-date")).to_be_focused()
        self.check(f"{width}: dining date is required and first error receives focus",
                   await page.locator("#dining-date").get_attribute("aria-invalid") == "true")
        future = (date.today() + timedelta(days=30)).isoformat()
        await page.locator("#dining-date").fill(future)
        await page.locator("#dining-guests").fill("0")
        await form.locator("button[type=submit]").click()
        await expect(page.locator("#dining-guests")).to_be_focused()
        self.check(f"{width}: dining rejects an invalid party count",
                   await page.locator("#dining-guests").get_attribute("aria-invalid") == "true")
        await page.locator("#dining-guests").fill("5")
        await page.locator("#dining-interest").select_option("Breakfast")
        await page.locator("#dining-name").fill("QA & dining guest")
        await page.locator("#dining-notes").fill("Please confirm serving times & meal inclusions.")
        await form.locator("button[type=submit]").click()
        draft = form.locator(".dining-form-draft a")
        await expect(draft).to_be_visible()
        href = await draft.get_attribute("href")
        parsed = urlsplit(href)
        text = parse_qs(parsed.query).get("text", [""])[0]
        self.check(f"{width}: dining prepares an encoded, unsent WhatsApp draft",
                   parsed.hostname == "wa.me" and parsed.path == "/918081709146" and
                   all(value in text for value in ["Breakfast", "People in our party: 5",
                       "QA & dining guest", "serving times & meal inclusions."]),
                   {"href": href, "message": text})
        await page.locator("#dining-notes").fill("Updated dining request.")
        self.check(f"{width}: editing dining details invalidates the previous draft",
                   await form.locator(".dining-form-draft a").count() == 0)
        link = page.locator(".hospitality-dining-download")
        async with page.expect_download() as pending:
            await link.click()
        download = await pending.value
        file = Path(await download.path())
        payload = file.read_bytes()
        with fitz.open(stream=payload, filetype="pdf") as document:
            pdf = {"pages": len(document), "text": "".join(page.get_text() for page in document)}
        normalized_text = " ".join(pdf["text"].split()).casefold()
        source = ROOT / "public/downloads/hotel-augusto-dining-guide.pdf"
        self.check(f"{width}: dining guide downloads as the valid one-page PDF",
                   payload.startswith(b"%PDF-") and pdf["pages"] == 1 and
                   "dining, around your day." in normalized_text and
                   "hotel augusto" in normalized_text and
                   hashlib.sha256(payload).digest() == hashlib.sha256(source.read_bytes()).digest(),
                   {"filename": download.suggested_filename, "bytes": len(payload),
                    "pages": pdf["pages"], "normalizedText": normalized_text,
                    "sha256": hashlib.sha256(payload).hexdigest()})

    async def image_delivery(self, page, width):
        await self.ready(page, "/")
        photo = page.locator(".hero-photo img").first
        await photo.evaluate("image=>image.decode()")
        source = await photo.evaluate("image=>image.currentSrc")
        response = await page.context.request.get(source, headers={
            "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
        })
        mime = response.headers.get("content-type", "").split(";")[0]
        body = await response.body()
        self.check(f"{width}: normal deployment negotiates AVIF through Next",
                   urlsplit(source).path == "/_next/image" and response.status == 200 and
                   mime == "image/avif" and b"ftypavif" in body[:32],
                   {"currentSrc": source, "requestAccept": "image/avif,image/webp,image/*,*/*;q=0.8",
                    "responseContentType": mime, "bytes": len(body), "vary": response.headers.get("vary")})

    async def group(self, page, width):
        await self.ready(page, "/group-stays")
        form = page.locator("form.group-enquiry")
        field = lambda name: form.locator(f"[name={name}]")
        await form.locator(".group-submit").click()
        await expect(field("arrival")).to_be_focused()
        self.check(f"{width}: group dates are required with first-error focus",
                   await field("arrival").get_attribute("aria-invalid") == "true" and
                   await form.locator(".group-form-alert").count() == 1)
        future = date.today() + timedelta(days=40)
        await field("arrival").fill((date.today() - timedelta(days=1)).isoformat())
        await field("departure").fill(future.isoformat())
        await form.locator(".group-submit").click()
        await expect(field("arrival")).to_be_focused()
        self.check(f"{width}: group request rejects a past arrival",
                   "today or later" in await form.inner_text())
        await field("arrival").fill(future.isoformat())
        await form.locator(".group-submit").click()
        await expect(field("departure")).to_be_focused()
        self.check(f"{width}: group request rejects a zero-night stay",
                   "after your arrival" in await form.inner_text())
        await field("departure").fill((future + timedelta(days=3)).isoformat())
        await field("adults").fill("0")
        await form.locator(".group-submit").click()
        await expect(field("adults")).to_be_focused()
        self.check(f"{width}: group request rejects invalid adult totals",
                   await field("adults").get_attribute("aria-invalid") == "true")
        await field("adults").fill("12")
        await field("children").fill("4")
        await field("roomCount").select_option("5")
        await field("room").select_option("A mix of room types")
        await field("name").fill("QA group coordinator")
        await field("company").fill("Digiocular & guests")
        await field("notes").fill("Please confirm separate beds and meal options.")
        await form.locator(".group-submit").click()
        draft = form.locator(".group-draft a")
        await expect(draft).to_be_visible()
        await expect(draft).to_be_focused()
        href = await draft.get_attribute("href")
        parsed = urlsplit(href)
        text = parse_qs(parsed.query).get("text", [""])[0]
        expected = ["12 adults, 4 children", "Rooms requested: 5", "A mix of room types",
                    "Digiocular & guests", "separate beds and meal options."]
        self.check(f"{width}: group draft retains exact requested totals and text",
                   parsed.hostname == "wa.me" and parsed.path == "/918081709146" and
                   all(value in text for value in expected) and
                   (await form.locator(".group-draft-message").inner_text()).strip() == text.strip(),
                   {"href": href, "message": text})
        await field("company").fill("Revised group name")
        self.check(f"{width}: editing a group request clears its previous draft",
                   await form.locator(".group-draft").count() == 0 and
                   await form.locator(".group-submit").is_visible())

    async def room_preview(self, page, width, reduced=False):
        for route in ("/", "/rooms"):
            await page.mouse.move(0, 0)
            await self.ready(page, route)
            link = page.locator(".room-photo-link").first
            await link.scroll_into_view_if_needed()
            self.check(f"{width} {route}: alternate room photo is deferred until interaction",
                       await link.locator(".room-photo-preview").count() == 0)
            if width == 1440 and not reduced:
                await link.hover()
            else:
                await link.focus()
            preview = link.locator(".room-photo-preview")
            await expect(preview).to_be_attached()
            await preview.locator("img").evaluate("image=>image.decode()")
            if reduced:
                await page.evaluate("()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
            else:
                await page.wait_for_function(
                    "()=>Number(getComputedStyle(document.querySelector('.room-photo-preview')).opacity)>=.99")
            self.check(f"{width} {route}: {'reduced-motion' if reduced else 'interactive'} alternate photo loads",
                       await preview.locator("img").evaluate("e=>e.complete&&e.naturalWidth>0") and
                       await preview.get_attribute("aria-hidden") == "true")
            if reduced:
                samples = await preview.evaluate("""async element=>{
                  const values=[];for(let i=0;i<4;i++){await new Promise(requestAnimationFrame);
                    values.push(Number(getComputedStyle(element).opacity));}return values;
                }""")
                self.check(f"{width} {route}: reduced-motion photo remains stable", all(v >= .99 for v in samples), samples)
            await page.mouse.move(0, 0)
            await link.evaluate("element=>element.blur()")
            await page.wait_for_function(
                "()=>Number(getComputedStyle(document.querySelector('.room-photo-preview')).opacity)<=.01")
            await link.focus()
            await page.wait_for_function(
                "()=>Number(getComputedStyle(document.querySelector('.room-photo-preview')).opacity)>=.99")
            self.check(f"{width} {route}: keyboard focus reveals a usable room preview",
                       await link.evaluate("e=>e===document.activeElement&&getComputedStyle(e).outlineStyle!=='none'"))
            href = await link.get_attribute("href")
            await page.keyboard.press("Enter")
            await page.wait_for_url("**" + href)
            self.check(f"{width} {route}: Enter opens the room detail", urlsplit(page.url).path == href)

    async def hero_deferred_scene(self, page):
        requested, release = asyncio.Event(), asyncio.Event()
        delayed_urls = []

        async def delay_lounge(route):
            delayed_urls.append(route.request.url)
            requested.set()
            await release.wait()
            await route.continue_()

        pattern = "**/*hotel-lounge*"
        await page.route(pattern, delay_lounge)
        try:
            await self.ready(page, "/")
            await expect(page.locator(".hero-pause")).to_be_disabled()
            photos = page.locator(".hero-photo")
            await photos.nth(0).locator("img").evaluate("image=>image.decode()")
            rooms = page.get_by_role("button", name="Show guest rooms", exact=True)
            lounge = page.get_by_role("button", name="Show the hotel lounge", exact=True)
            await lounge.click()
            await asyncio.wait_for(requested.wait(), timeout=12)
            await expect(page.locator(".hero-scene-buttons")).to_have_attribute("aria-busy", "true")
            before = await photos.evaluate_all("""elements=>elements.map(element=>({
              hidden:element.getAttribute('aria-hidden'),
              opacity:Number(getComputedStyle(element).opacity),
              decoded:!!element.querySelector('img')?.naturalWidth
            }))""")
            self.check("Reduced motion: a delayed lounge image keeps the current room visible", (
                await rooms.get_attribute("aria-pressed") == "true" and
                await lounge.get_attribute("aria-pressed") == "false" and
                before[0]["hidden"] == "false" and before[0]["opacity"] >= .99 and
                before[0]["decoded"] and before[1]["hidden"] == "true" and
                before[1]["opacity"] <= .01 and not before[1]["decoded"]),
                {"delayedRequests": delayed_urls, "photos": before})
            release.set()
            await expect(lounge).to_have_attribute("aria-pressed", "true", timeout=30000)
            await expect(page.locator(".hero-scene-buttons")).to_have_attribute("aria-busy", "false")
            await photos.nth(1).locator("img").evaluate("image=>image.decode()")
            await page.evaluate("()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
            after = await photos.evaluate_all("""elements=>elements.map(element=>({
              hidden:element.getAttribute('aria-hidden'),
              opacity:Number(getComputedStyle(element).opacity),
              decoded:!!element.querySelector('img')?.naturalWidth
            }))""")
            self.check("Reduced motion: the lounge is selected only after its photo loads", (
                after[0]["hidden"] == "true" and after[0]["opacity"] <= .01 and
                after[1]["hidden"] == "false" and after[1]["opacity"] >= .99 and
                after[1]["decoded"]), after)
        finally:
            release.set()
            await page.unroute(pattern, delay_lounge)

    async def hero_focus_pause(self, page):
        await page.mouse.move(0, 0)
        await self.ready(page, "/")
        await page.wait_for_function("()=>document.querySelectorAll('.hero-photo img').length===3")
        await page.locator(".hero-photo img").evaluate_all(
            "images=>Promise.all(images.map(image=>image.decode()))")
        rooms = page.get_by_role("button", name="Show guest rooms", exact=True)
        await rooms.focus()
        await rooms.hover()
        await page.mouse.move(0, 0)
        await expect(rooms).to_be_focused()
        # Longer than the actual eight-second carousel interval: mouseleave
        # must not clear the independent keyboard-focus pause.
        await page.wait_for_timeout(8500)
        self.check("Hero autoplay remains paused after pointer leaves a focused control", (
            await rooms.get_attribute("aria-pressed") == "true" and
            await rooms.evaluate("element=>element===document.activeElement") and
            await page.locator(".hero-pause").get_attribute("aria-pressed") == "false"))
        await page.locator("#dock-arrival").focus()
        lounge = page.get_by_role("button", name="Show the hotel lounge", exact=True)
        await expect(lounge).to_have_attribute("aria-pressed", "true", timeout=12000)
        self.check("Hero autoplay resumes when focus and pointer both leave", True)

    def static_export(self):
        for route in ROUTES:
            relative = "index.html" if route == "/" else "404.html" if route == "/does-not-exist" else route.lstrip("/") + ".html"
            path = self.export / relative
            if not path.is_file():
                self.check(f"Static {route}: exported HTML exists", False, str(path))
                continue
            parsed = ExportPage()
            parsed.feed(path.read_text(encoding="utf8"))
            photographs = [image for image in parsed.images
                           if urlsplit(image.get("src", "")).path.startswith("/images/") or
                           urlsplit(image.get("src", "")).path == "/_next/image"]
            missing, optimizer_urls, no_srcset = [], [], []
            for image in photographs:
                if not image.get("srcset"):
                    no_srcset.append(image.get("src"))
            for image in photographs + parsed.preloads:
                sources = [image.get("src", "")]
                candidates = image.get("srcset", image.get("imagesrcset", ""))
                sources += [candidate.strip().split()[0] for candidate in candidates.split(",") if candidate.strip()]
                for source in filter(None, sources):
                    url = urlsplit(source)
                    if url.path == "/_next/image":
                        optimizer_urls.append(source)
                    if url.scheme or url.netloc or source.startswith("data:"):
                        continue
                    target = (self.export / unquote(url.path).lstrip("/")).resolve()
                    if not target.is_relative_to(self.export) or not target.is_file():
                        missing.append(source)
            item = {"route": route, "photographs": len(photographs),
                    "srcsets": [image.get("srcset") for image in photographs],
                    "missing": missing, "optimizerUrls": optimizer_urls, "missingSrcsets": no_srcset}
            self.report["staticPages"].append(item)
            self.check(f"Static {route}: responsive sources resolve without image API",
                       not missing and not optimizer_urls and not no_srcset, item)
        manifest = json.loads((ROOT / "content/responsive-images.json").read_text(encoding="utf8"))
        missing = [item["src"] for variants in manifest.values() for item in variants
                   if not (self.export / item["src"].lstrip("/")).is_file()]
        self.check("Static export contains every responsive image candidate", not missing, missing)

    async def run(self, static_only=False):
        if not static_only and (not self.cases or set(self.cases) != {"static_export"}):
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(channel="msedge", headless=True)
                try:
                    for width in (390, 1440):
                        context, page = await self.context(browser, width)
                        try:
                            if self.selected("layout"):
                                for route in ROUTES:
                                    await self.case(f"{width} {route}: layout exception",
                                                    lambda r=route: self.layout(page, r, width))
                            for name in WIDTH_CASES:
                                if self.selected(name):
                                    await self.case(f"{width}: {name} exception",
                                                    lambda n=name: getattr(self, n)(page, width))
                            if width == 1440 and self.selected("hero_focus_pause"):
                                await self.case("Hero mixed pointer and keyboard pause exception",
                                                lambda: self.hero_focus_pause(page))
                            print(f"Completed {width}px conversion checks", flush=True)
                        finally:
                            await context.close()
                    if self.selected("hero_deferred_scene") or self.selected("room_preview_reduced"):
                        context, page = await self.context(browser, 390, reduced="reduce")
                        try:
                            if self.selected("hero_deferred_scene"):
                                await self.case("Reduced-motion delayed hero photo exception",
                                                lambda: self.hero_deferred_scene(page))
                            if self.selected("room_preview_reduced"):
                                await self.case("Reduced-motion room preview exception",
                                                lambda: self.room_preview(page, 390, reduced=True))
                        finally:
                            await context.close()
                finally:
                    await browser.close()
                    self.report["browserClosed"] = True
            self.check("No JavaScript, console or unexpected HTTP errors", not (
                self.report["runtimeErrors"] or self.report["consoleErrors"] or self.report["failedResponses"]),
                {key: self.report[key] for key in ["runtimeErrors", "consoleErrors", "failedResponses"]})
            self.check("No WhatsApp link was opened or sent", not self.report["externalNavigationAttempts"])
        if static_only or self.selected("static_export"):
            self.static_export()
        baseline = self.report.get("baselineReport")
        if baseline:
            unchanged = hashlib.sha256(Path(baseline["path"]).read_bytes()).hexdigest() == baseline["sha256"]
            baseline["preservedUnchanged"] = unchanged
            self.check("Original full-run report remains byte-identical", unchanged, baseline)
        self.report["finished"] = datetime.now(timezone.utc).isoformat()
        self.save()
        self.report["status"] = "fail" if self.report["summary"]["failed"] else "pass"
        self.report_path.write_text(json.dumps(self.report, indent=2) + "\n", encoding="utf8")
        print(json.dumps({"status": self.report["status"], **self.report["summary"],
                          "report": str(self.report_path)}), flush=True)
        return 1 if self.report["summary"]["failed"] else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:3080")
    parser.add_argument("--output", default="evidence/apple-dominant-revision")
    parser.add_argument("--export-dir", default="out")
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--case", action="append", choices=CASE_NAMES,
                        help="Run only this suite at its supported widths; repeat for several. "
                             "Writes a dated supplemental report and preserves the full run.")
    options = parser.parse_args()
    raise SystemExit(asyncio.run(QA(options).run(options.static_only)))
