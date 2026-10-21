"""Client contact release QA. Every FormSubmit request is intercepted; no email is sent."""
import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
RECIPIENT = "aromaofkashi@gmail.com"
PHONE = "918081709146"
ROUTES = ["/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
          "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
          "/gallery", "/guides", "/guides/first-visit-to-kashi",
          "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
          "/group-stays", "/contact", "/privacy"]
FORMS = [("/contact", ".booking-form", "Stay enquiry"),
         ("/dining", ".dining-enquiry-form", "Dining enquiry"),
         ("/group-stays", ".group-enquiry", "Group stay enquiry")]
RUNTIME = re.compile(r"maximum (?:update depth|call stack)|too much recursion|hydration|Minified React error", re.I)
GEOMETRY = """selectors=>Object.fromEntries(selectors.map(selector=>{const e=document.querySelector(selector);
 if(!e)return [selector,null];const r=e.getBoundingClientRect(),s=getComputedStyle(e);
 return [selector,{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height,
 visible:!!r.width&&!!r.height&&s.visibility!=='hidden'&&s.display!=='none'}]}))"""


def overlaps(a, b):
    return min(a["right"], b["right"]) - max(a["left"], b["left"]) > 1 and min(a["bottom"], b["bottom"]) - max(a["top"], b["top"]) > 1


class Audit:
    def __init__(self, args):
        self.args, self.scope = args, {}
        self.output = ROOT / "evidence/client-handoff-20261021" / f"contact-{args.browser}.json"
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.report = {"recorded_at_utc": datetime.now(timezone.utc).isoformat(), "base": args.base,
                       "browser": args.browser, "checks": [], "runtime_errors": [], "console_errors": [],
                       "requests": [], "blocked_external_writes": [], "blocked_whatsapp": [], "screenshots": [],
                       "external_emails_sent": 0, "limitations": [
                           "FormSubmit responses are mocked. This does not prove mailbox activation or delivery.",
                           "WebKit emulation is not a physical iPhone test."]}

    def check(self, name, passed, detail=None):
        self.report["checks"].append({**self.scope, "name": name, "passed": bool(passed), "detail": detail})
        print(f"{'PASS' if passed else 'FAIL'} {self.scope} {name}", flush=True)

    def save(self):
        self.report["summary"] = {"passed": sum(c["passed"] for c in self.report["checks"]),
                                  "failed": sum(not c["passed"] for c in self.report["checks"]),
                                  "runtime_errors": len(self.report["runtime_errors"]),
                                  "mocked_posts": len(self.report["requests"])}
        self.output.write_text(json.dumps(self.report, indent=2), encoding="utf-8")

    def context(self, browser, width, height, reduced=False):
        context = browser.new_context(viewport={"width": width, "height": height},
            timezone_id="Asia/Kolkata", is_mobile=width < 900, has_touch=width < 900,
            reduced_motion="reduce" if reduced else "no-preference", service_workers="block")
        pending = []
        origin = urlsplit(self.args.base)

        def intercept(route):
            request, url = route.request, urlsplit(route.request.url)
            host = (url.hostname or "").lower()
            if host == "formsubmit.co" or host.endswith(".formsubmit.co"):
                if request.method == "OPTIONS":
                    route.fulfill(status=204, headers={"Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "content-type,accept"})
                elif request.method == "POST":
                    try:
                        payload = json.loads(request.post_data or "{}")
                    except ValueError:
                        payload = {"invalid_json": True}
                    self.report["requests"].append({**self.scope, "url": request.url, "payload": payload, "mocked": True})
                    pending.append(route)
                else:
                    route.abort()
                return
            if host in {"wa.me", "api.whatsapp.com", "web.whatsapp.com"}:
                self.report["blocked_whatsapp"].append(request.url)
                route.abort()
                return
            if request.method in {"POST", "PUT", "PATCH", "DELETE"} and (url.scheme, url.netloc) != (origin.scheme, origin.netloc):
                self.report["blocked_external_writes"].append({"url": request.url, "method": request.method})
                route.abort()
                return
            route.continue_()

        context.route("**/*", intercept)
        page = context.new_page()
        page.set_default_timeout(15000)
        page.set_default_navigation_timeout(60000)
        page.on("pageerror", lambda error: self.report["runtime_errors"].append({**self.scope, "message": str(error)}))

        def console(message):
            if message.type == "error":
                self.report["console_errors"].append({**self.scope, "message": message.text})
                if RUNTIME.search(message.text):
                    self.report["runtime_errors"].append({**self.scope, "message": message.text})
        page.on("console", console)
        return context, page, pending

    def goto(self, page, route):
        self.scope["route"] = route
        response = page.goto(self.args.base + route, wait_until="domcontentloaded")
        self.check("Page responds successfully", bool(response and response.ok), response.status if response else None)
        page.locator("main").wait_for()
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(900)

    def overflow(self, page, state):
        size = page.evaluate("({body:document.body.scrollWidth,document:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth})")
        self.check(f"{state}: no horizontal overflow", max(size["body"], size["document"]) <= size["viewport"] + 1, size)

    def screenshot(self, page, name):
        suffix = "-reduced" if self.scope.get("reduced_motion") else ""
        path = self.output.parent / f"contact-{self.args.browser}-{name}{suffix}.png"
        page.screenshot(path=str(path), animations="allow")
        self.report["screenshots"].append(str(path.relative_to(ROOT)))

    def position(self, locator):
        locator.evaluate("e=>scrollTo({top:Math.max(0,e.getBoundingClientRect().top+scrollY-innerHeight*.25),behavior:'instant'})")

    def whatsapp(self, locator, label):
        self.check(f"{label}: one link exists", locator.count() == 1)
        if locator.count() != 1:
            return
        url = urlsplit(locator.get_attribute("href") or "")
        self.check(f"{label}: correct WhatsApp destination", url.scheme == "https" and url.hostname == "wa.me"
                   and url.path == f"/{PHONE}" and bool(parse_qs(url.query).get("text")), locator.get_attribute("href"))
        self.check(f"{label}: accessible external-link semantics", bool(locator.get_attribute("aria-label"))
                   and locator.get_attribute("target") == "_blank" and "noopener" in (locator.get_attribute("rel") or ""))

    def dock_chat_layout(self, page, state):
        boxes = page.evaluate(GEOMETRY, [".whatsapp-chat", ".booking-dock", ".booking-dock-fields"])
        controls = page.locator(".booking-dock-fields :is(.dock-date,.dock-guests,.dock-submit)").evaluate_all("""elements=>elements.map(e=>{
          const r=e.getBoundingClientRect();return {class:e.className,left:r.left,right:r.right,top:r.top,bottom:r.bottom}})""")
        boxes["booking_controls"] = controls
        chat, dock, fields = [boxes[s] for s in [".whatsapp-chat", ".booking-dock", ".booking-dock-fields"]]
        in_grid = page.locator(".whatsapp-chat").evaluate("""e=>e.parentElement.matches('.dock-actions')
          && !!e.closest('.booking-dock-fields')
          && !['absolute','fixed'].includes(getComputedStyle(e).position)""")
        contained = bool(chat and dock and fields and chat["visible"]
                         and chat["left"] >= dock["left"] - 1 and chat["right"] <= dock["right"] + 1
                         and chat["top"] >= dock["top"] - 1 and chat["bottom"] <= dock["bottom"] + 1)
        self.check(f"{state}: chat occupies the rightmost booking dock cell", in_grid and contained
                   and abs(chat["right"] - fields["right"]) <= 1, boxes)
        self.check(f"{state}: chat is separate from both dates, guests and availability button", bool(chat)
                   and len(controls) == 4 and all(not overlaps(chat, control) for control in controls), boxes)

    def chrome(self, page, width, height):
        self.goto(page, "/")
        for selector, label in [(".header-whatsapp", "Navbar"), (".whatsapp-chat", "Dock chat")]:
            link = page.locator(selector)
            self.whatsapp(link, label)
            box = link.bounding_box()
            self.check(f"{label}: visible 44px target inside viewport", link.is_visible() and box is not None
                       and box["width"] >= 44 and box["height"] >= 44 and box["x"] >= 0
                       and box["x"] + box["width"] <= width + 1, box)
        boxes = page.evaluate(GEOMETRY, [".site-header", ".whatsapp-chat", ".hero-scene-controls", ".hero-actions", ".booking-dock"])
        actions = page.locator(".hero-actions a, .hero-actions button").evaluate_all("""elements=>elements.map(e=>{
          const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {tag:e.tagName,label:e.getAttribute('aria-label')||e.textContent.trim(),
          left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height,
          visible:!!r.width&&!!r.height&&s.visibility!=='hidden'&&s.display!=='none'}}).filter(e=>e.visible)""")
        boxes["actionable_children"] = actions
        chat, scene, dock = [boxes[s] for s in [".whatsapp-chat", ".hero-scene-controls", ".booking-dock"]]
        self.dock_chat_layout(page, "Homepage")
        self.check("Dock chat clears hero controls", not overlaps(chat, scene)
                   and bool(actions) and all(not overlaps(chat, action) for action in actions), boxes)
        self.check("Hero actions and scene controls stay above booking dock", scene["bottom"] <= dock["top"] + 1
                   and bool(actions) and all(action["bottom"] <= dock["top"] + 1 for action in actions)
                   and scene["top"] >= boxes[".site-header"]["bottom"] - 1, boxes)
        self.overflow(page, "Homepage")
        scenes = page.locator(".hero-scene-buttons button")
        scenes.nth(1).click()
        page.wait_for_function("document.querySelectorAll('.hero-scene-buttons button')[1].getAttribute('aria-pressed')==='true'")
        self.check("Hero scene remains operable beside chat", scenes.nth(1).get_attribute("aria-pressed") == "true")
        page.wait_for_timeout(900)
        self.screenshot(page, f"home-{width}x{height}")
        if page.locator(".menu-trigger").is_visible():
            page.locator(".menu-trigger").click()
            page.locator(".navigation-dialog[open]").wait_for()
            self.whatsapp(page.locator('.navigation-contact a[href^="https://wa.me/"]'), "Mobile menu")
            self.check("Dock chat hides behind navigation dialog", page.locator(".whatsapp-chat").is_hidden())
            self.overflow(page, "Navigation open")
            page.get_by_role("button", name="Close navigation", exact=True).click()
            self.check("Dock chat returns after navigation closes", page.locator(".whatsapp-chat").is_visible())
        calendar_trigger = page.locator(".booking-dock .date-picker-trigger").first
        if calendar_trigger.is_visible():
            calendar_trigger.click()
        else:
            page.locator("#dock-arrival").click()
        page.locator(".date-picker-dialog[open]").wait_for()
        self.check("Dock chat hides while calendar is open", page.locator(".whatsapp-chat").is_hidden())
        page.get_by_role("button", name="Close calendar", exact=True).click()
        self.check("Calendar opening does not select a date", page.locator("#dock-arrival").input_value() == "")
        self.check("Dock chat returns after calendar closes", page.locator(".whatsapp-chat").is_visible())
        if width in {390, 1440}:
            self.goto(page, "/gallery")
            page.locator(".gallery-tile").first.click()
            page.locator(".gallery-dialog[open]").wait_for()
            self.check("Dock chat hides behind gallery dialog", page.locator(".whatsapp-chat").is_hidden())
            page.get_by_role("button", name="Close photograph viewer", exact=True).click()
            self.check("Dock chat returns after gallery closes", page.locator(".whatsapp-chat").is_visible())

    def set_field(self, form, name, value):
        field = form.locator(f'[name="{name}"]')
        if field.evaluate("e=>e.tagName") == "SELECT":
            field.select_option(str(value))
        else:
            field.fill(str(value))
        field.evaluate("e=>e.blur()")

    def submit(self, page, form):
        button = form.locator('button[type="submit"]').first
        self.position(button)
        button.click()
        page.wait_for_timeout(150)

    def await_post(self, page, pending):
        deadline = time.monotonic() + 12
        while not pending and time.monotonic() < deadline:
            page.wait_for_timeout(30)
        if not pending:
            raise AssertionError("Expected an intercepted FormSubmit POST; none arrived")

    def respond(self, pending, status=200, body=None):
        pending.pop(0).fulfill(status=status, content_type="application/json", headers={"Access-Control-Allow-Origin": "*"},
                               body=json.dumps(body if body is not None else {"success": "true", "message": "Test enquiry accepted"}))

    def values(self, form):
        return form.evaluate("e=>Object.fromEntries([...e.elements].filter(x=>x.name&&x.name!=='channel').map(x=>[x.name,x.value]))")

    def form_case(self, page, pending, route, selector, subject, width):
        self.goto(page, route)
        form = page.locator(selector)
        form.wait_for()
        primary = form.locator('button[type="submit"]').first
        baseline = len(self.report["requests"])
        self.submit(page, form)
        self.check("Empty submission validates without sending", form.locator('[role="alert"]').count() > 0 and len(self.report["requests"]) == baseline)
        dates = page.evaluate("()=>[30,32].map(n=>{const d=new Date();d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')})")
        dining = route == "/dining"
        values = {"name": "Digiocular verification", "email": "digiocular@gmail.com", "phone": "+91 9999991234", "notes": "QA only - intercepted locally; never delivered."}
        values.update({"date": dates[0], "guests": "0"} if dining else {"arrival": dates[0], "departure": dates[0], "adults": "2", "children": "0", "roomCount": "2"})
        for name, value in values.items():
            self.set_field(form, name, value)
        self.submit(page, form)
        self.check("Invalid dates or guest count prevent sending", form.locator('[aria-invalid="true"]').count() > 0 and len(self.report["requests"]) == baseline)
        self.set_field(form, "guests" if dining else "departure", "2" if dining else dates[1])
        self.set_field(form, "email", "invalid-email")
        self.set_field(form, "phone", "not-a-number")
        self.submit(page, form)
        self.check("Reply email and phone are validated", form.locator('[name="email"]').get_attribute("aria-invalid") == "true"
                   and form.locator('[name="phone"]').get_attribute("aria-invalid") == "true" and len(self.report["requests"]) == baseline)
        for name in ["email", "phone"]:
            self.set_field(form, name, values[name])
        expected = self.values(form)
        self.submit(page, form)
        self.await_post(page, pending)
        self.check("Pending state disables submission and inputs", form.get_attribute("aria-busy") == "true" and primary.is_disabled()
                   and form.locator('[name="email"]').is_disabled() and form.locator('[value="whatsapp"]').is_disabled())
        form.evaluate("e=>{e.requestSubmit();e.requestSubmit()}")
        page.wait_for_timeout(200)
        self.check("Repeated pending submits create only one request", len(self.report["requests"]) == baseline + 1 and len(pending) == 1)
        request = self.report["requests"][-1]
        url, body = urlsplit(request["url"]), request["payload"]
        self.check("Request uses exact hotel email destination", url.scheme == "https" and url.hostname == "formsubmit.co"
                   and unquote(url.path) == f"/ajax/{RECIPIENT}", request["url"])
        self.check("Request preserves reply and enquiry details", body.get("email") == values["email"] and body.get("phone") == values["phone"]
                   and body.get("Name") == values["name"] and body.get("Notes") == values["notes"]
                   and body.get("_subject", "").endswith(subject) and body.get("_template") == "table", body)
        self.check("Requested dates and party survive serialization",
                   (body.get("Preferred date") == dates[0] and body.get("Guests") == "2") if dining else
                   (body.get("Arrival") == dates[0] and body.get("Departure") == dates[1]
                    and body.get("Adults") == "2" and body.get("Children") == "0" and body.get("Rooms requested") == "2"), body)
        self.respond(pending, status=503, body={"success": False, "message": "Mock service failure"})
        form.locator(".enquiry-email-error").wait_for()
        self.check("Failed delivery keeps values and enables retry", self.values(form) == expected and primary.is_enabled()
                   and form.get_attribute("aria-busy") == "false")
        self.overflow(page, "Email failure")
        if width == 390:
            self.position(form.locator(".enquiry-email-error"))
            self.screenshot(page, f"{route.strip('/')}-error-{width}")
        self.submit(page, form)
        self.await_post(page, pending)
        self.check("Retry sends unchanged details exactly once", len(self.report["requests"]) == baseline + 2
                   and self.report["requests"][-1]["payload"] == body)
        self.respond(pending)
        accepted = form.locator(".enquiry-email-accepted")
        accepted.wait_for()
        self.check("Successful forwarding is clear and values remain", "accepted for forwarding" in accepted.inner_text()
                   and primary.is_disabled() and self.values(form) == expected)
        form.evaluate("e=>e.requestSubmit()")
        page.wait_for_timeout(150)
        self.check("Unchanged successful enquiry cannot be resent", len(self.report["requests"]) == baseline + 2)
        self.overflow(page, "Email accepted")
        if width == 390:
            self.position(accepted)
            self.screenshot(page, f"{route.strip('/')}-accepted-{width}")
        self.set_field(form, "notes", "Edited QA enquiry; delivery remains mocked.")
        self.check("Editing enables a fresh enquiry", primary.is_enabled() and accepted.count() == 0)
        self.submit(page, form)
        self.await_post(page, pending)
        self.respond(pending, body={"success": "true", "message": "Please activate the email address by checking your inbox"})
        activation = form.locator(".enquiry-email-activation")
        activation.wait_for()
        self.check("Activation response is not presented as delivery", form.locator(".enquiry-email-accepted").count() == 0
                   and activation.locator(f'a[href="mailto:{RECIPIENT}"]').count() == 1 and primary.is_enabled())
        self.set_field(form, "email", "")
        alternative = form.locator('button[value="whatsapp"]')
        self.position(alternative)
        alternative.click()
        draft = form.locator('a[href^="https://wa.me/"]')
        draft.wait_for()
        self.check("WhatsApp alternative works without email and sends nothing", urlsplit(draft.get_attribute("href")).path == f"/{PHONE}"
                   and len(self.report["requests"]) == baseline + 3 and not pending)

    def route_sweep(self, page):
        for route in ROUTES:
            self.goto(page, route)
            for fraction in [0, .25, .5, .75, 1]:
                page.evaluate("f=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*f,behavior:'instant'})", fraction)
                page.wait_for_timeout(160)
                self.overflow(page, f"Route scroll {fraction}")
            self.whatsapp(page.locator(".header-whatsapp"), "Navbar")
            self.whatsapp(page.locator(".whatsapp-chat"), "Dock chat")
            self.dock_chat_layout(page, "Page end")
            self.save()

    def run_case(self, browser, width, height, action, reduced=False):
        self.scope = {"width": width, "height": height, "reduced_motion": reduced}
        context, page, pending = self.context(browser, width, height, reduced)
        try:
            action(page, pending)
        except Exception as error:
            self.check("Case completes", False, {"type": type(error).__name__, "message": str(error)})
        finally:
            for route in pending:
                try:
                    route.abort()
                except Exception:
                    pass
            context.close()
            self.save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://127.0.0.1:3080")
    parser.add_argument("--browser", choices=["chromium", "webkit"], default="chromium")
    args = parser.parse_args()
    args.base = args.base.rstrip("/")
    if args.browser == "webkit" and urlsplit(args.base).scheme != "https":
        parser.error("Use HTTPS for WebKit: the site CSP upgrades insecure requests.")
    audit = Audit(args)
    try:
        with sync_playwright() as playwright:
            browser = getattr(playwright, args.browser).launch(headless=True, **({"channel": "msedge"} if args.browser == "chromium" else {}))
            try:
                for width, height in [(320, 844), (390, 844), (844, 390), (1440, 1000)]:
                    audit.run_case(browser, width, height, lambda page, pending, w=width, h=height: audit.chrome(page, w, h))
                for width in [320, 390, 1440]:
                    for route, selector, subject in FORMS:
                        audit.run_case(browser, width, 844 if width < 900 else 1000,
                            lambda page, pending, r=route, s=selector, t=subject, w=width: audit.form_case(page, pending, r, s, t, w))
                audit.run_case(browser, 390, 844, lambda page, pending: audit.route_sweep(page))
                audit.run_case(browser, 390, 844, lambda page, pending: audit.chrome(page, 390, 844), reduced=True)
            finally:
                browser.close()
    except Exception as error:
        audit.check("Browser launch and suite complete", False, str(error))
    audit.check("No runtime or recursion errors", not audit.report["runtime_errors"], audit.report["runtime_errors"])
    audit.check("No WhatsApp navigation attempted", not audit.report["blocked_whatsapp"], audit.report["blocked_whatsapp"])
    audit.check("No unexpected external write attempted", not audit.report["blocked_external_writes"], audit.report["blocked_external_writes"])
    audit.save()
    return int(bool(audit.report["summary"]["failed"]))


if __name__ == "__main__":
    raise SystemExit(main())
