"""Exercise real calendar interaction and booking state; never send enquiries."""
import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode, urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ["/", "/hotel", "/rooms", "/rooms/compare", "/rooms/deluxe-room",
          "/rooms/deluxe-twin-room", "/rooms/family-room", "/dining", "/varanasi",
          "/gallery", "/guides", "/guides/first-visit-to-kashi",
          "/guides/arriving-in-godowlia", "/guides/choosing-your-room",
          "/group-stays", "/contact", "/privacy"]
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="http://127.0.0.1:3082")
parser.add_argument("--output", default="evidence/mobile-dates/date-qa.json")
parser.add_argument("--engines", nargs="+", default=["chromium"],
                    help="Use chromium locally; run chromium webkit against the HTTPS preview.")
args = parser.parse_args()
engines = [engine for item in args.engines for engine in item.split(",")]
base = args.base_url.rstrip("/")
output = ROOT / args.output
output.parent.mkdir(parents=True, exist_ok=True)
report = {
    "date": datetime.now(timezone.utc).isoformat(), "base_url": base,
    "engines": engines, "checks": [], "runtime_errors": [], "console_errors": [],
    "screenshots": [], "external_messages_sent": 0, "network_events": [],
    "limitations": [
        "WebKit on Windows is browser-engine coverage, not a physical iPhone test.",
        "Windows WebKit may expose native date inputs as text controls; the shared "
        "calendar is tested through rendered dialog, day buttons and submitted ISO values.",
    ],
}
scope = {"engine": "", "case": ""}
RUNTIME_PATTERN = re.compile(
    r"maximum (?:update depth|call stack)|too much recursion|ResizeObserver|"
    r"uncaught|unhandled|hydration|Minified React error", re.I)


def check(name, passed, detail=None):
    full = f"{scope['engine']} / {scope['case']} / {name}"
    report["checks"].append({"name": full, "passed": bool(passed), "detail": detail})
    print(("PASS " if passed else "FAIL ") + full, flush=True)
    if not passed and detail:
        print(str(detail), flush=True)


def run(name, action):
    scope["case"] = name
    try:
        action()
    except Exception as error:
        check("Case completes", False, str(error))


def watch(page):
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(60000)
    page.on("pageerror", lambda error: report["runtime_errors"].append({
        **scope, "url": page.url, "message": str(error), "name": error.name,
        "stack": error.stack, "time": datetime.now(timezone.utc).isoformat()}))

    def network(kind, request, **detail):
        if "_rsc=" in request.url or kind == "failed":
            report["network_events"].append({
                **scope, "kind": kind, "url": request.url,
                "frame_url": page.url, "resource": request.resource_type,
                "time": datetime.now(timezone.utc).isoformat(), **detail})

    page.on("request", lambda request: network("start", request))
    page.on("response", lambda response: network(
        "response", response.request, status=response.status))
    page.on("requestfailed", lambda request: network(
        "failed", request, failure=request.failure))

    def console(message):
        if message.type == "error":
            report["console_errors"].append({**scope, "url": page.url, "message": message.text})
        if RUNTIME_PATTERN.search(message.text):
            report["runtime_errors"].append({**scope, "url": page.url, "message": message.text})
    page.on("console", console)
    return page


def goto(page, route="/"):
    report["network_events"].append({
        **scope, "kind": "navigation-start", "from": page.url, "to": base + route,
        "time": datetime.now(timezone.utc).isoformat()})
    response = page.goto(base + route, wait_until="networkidle")
    if not response or response.status != 200:
        raise AssertionError(f"Route failed: {route}, status {response.status if response else None}")
    page.locator("main").wait_for()
    report["network_events"].append({
        **scope, "kind": "navigation-end", "url": page.url,
        "time": datetime.now(timezone.utc).isoformat()})


def shot(page, name):
    path = output.parent / f"{scope['engine']}-{name}.png"
    page.screenshot(path=str(path), animations="disabled")
    report["screenshots"].append(str(path))


def visible_dialog(page):
    dialog = page.locator("dialog.date-picker-dialog[open]")
    dialog.wait_for(state="visible")
    dialog.get_by_role("grid").wait_for(state="visible")
    return dialog


def wrapper(field):
    return field.locator(
        "xpath=ancestor::*[contains(concat(' ',normalize-space(@class),' '),' date-control ')][1]")


def open_calendar(page, field, label, by_input=False):
    opener = field if by_input else wrapper(field).get_by_role(
        "button", name=re.compile("^Open " + re.escape(label) + " calendar$", re.I))
    opener.scroll_into_view_if_needed()
    if page.evaluate("navigator.maxTouchPoints > 0"):
        opener.tap()
    else:
        opener.click()
    dialog = visible_dialog(page)
    check("Calendar has its field heading", dialog.get_by_role(
        "heading", name=label, exact=True).count() == 1)
    bounds = dialog.evaluate("""e=>{const r=e.getBoundingClientRect();return {
      left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:innerWidth,height:innerHeight,
      scroll:e.scrollWidth,client:e.clientWidth}}""")
    check("Calendar stays inside the viewport", bounds["left"] >= -1
          and bounds["right"] <= bounds["width"] + 1 and bounds["top"] >= -1
          and bounds["bottom"] <= bounds["height"] + 1
          and bounds["scroll"] <= bounds["client"] + 1, bounds)
    return dialog, opener


def days(dialog):
    return dialog.locator('[role="grid"] [data-day] button').evaluate_all("""buttons=>buttons.map(b=>{
      const cell=b.closest('[data-day]');
      return {iso:cell.dataset.day,disabled:b.disabled||b.getAttribute('aria-disabled')==='true',
        outside:cell.hasAttribute('data-outside'),label:b.getAttribute('aria-label')};
    })""")


def pick_next_month(page, field, label, by_input=False, screenshot=None):
    dialog, opener = open_calendar(page, field, label, by_input)
    before = days(dialog)
    check("Calendar contains actual day buttons", len(before) >= 28, {"days": len(before)})
    dialog.get_by_role("button", name=re.compile("next month", re.I)).click()
    after = days(dialog)
    check("Next month changes the available dates", before != after)
    enabled = [day for day in after if not day["disabled"] and not day["outside"]]
    if not enabled:
        raise AssertionError("No enabled day in the next month")
    chosen = enabled[min(9, len(enabled) - 1)]["iso"]
    if screenshot:
        shot(page, screenshot)
    dialog.locator(f'[data-day="{chosen}"] button').first.click()
    dialog.wait_for(state="hidden")
    check("Selection stores ISO date", field.input_value() == chosen, field.input_value())
    check("Calendar returns focus to opener", opener.evaluate("e=>document.activeElement===e"))
    check("Selected date hides empty prompt",
          not wrapper(field).locator(".date-field-placeholder").is_visible())
    submitted = field.evaluate("e=>new FormData(e.form).get(e.name)")
    check("FormData contains the selected date", submitted == chosen, submitted)
    return chosen


def dock_case(page, width):
    page.set_viewport_size({"width": width, "height": 900 if width > 600 else 844})
    goto(page)
    for ident in ["dock-arrival", "dock-departure"]:
        field = page.locator("#" + ident)
        prompt = wrapper(field).locator(".date-field-placeholder")
        check(ident + " has a visible empty prompt", prompt.is_visible()
              and "Choose date" in prompt.inner_text())
    shot(page, f"dock-empty-{width}")
    arrival = page.locator("#dock-arrival")
    chosen = pick_next_month(page, arrival, "Check-in date", by_input=True,
                             screenshot=f"checkin-calendar-{width}")
    departure = page.locator("#dock-departure")
    minimum = (datetime.fromisoformat(chosen) + timedelta(days=1)).date().isoformat()
    check("Checkout minimum follows check-in", departure.get_attribute("min") == minimum)
    dialog, opener = open_calendar(page, departure, "Check-out date")
    previous = [day for day in days(dialog) if day["iso"] < minimum]
    check("Checkout disables dates before its minimum",
          bool(previous) and all(day["disabled"] for day in previous), previous)
    page.keyboard.press("Escape")
    dialog.wait_for(state="hidden")
    check("Escape returns focus", opener.evaluate("e=>document.activeElement===e"))
    pick_next_month(page, departure, "Check-out date", screenshot=f"checkout-calendar-{width}")
    for _ in range(3):
        dialog, opener = open_calendar(page, departure, "Check-out date")
        dialog.get_by_role("button", name="Close calendar", exact=True).click()
        dialog.wait_for(state="hidden")
    check("Repeated open and close restores focus", opener.evaluate("e=>document.activeElement===e"))
    check("Page fits viewport after calendar interactions",
          page.evaluate("document.body.scrollWidth===document.documentElement.clientWidth"))


def keyboard_case(page):
    goto(page)
    field = page.locator("#dock-arrival")
    opener = wrapper(field).get_by_role("button", name="Open check-in date calendar", exact=True)
    opener.focus()
    page.keyboard.press("Enter")
    dialog = visible_dialog(page)
    dialog.get_by_role("button", name=re.compile("next month", re.I)).click()
    enabled = [day for day in days(dialog) if not day["disabled"] and not day["outside"]]
    start = enabled[5]["iso"]
    dialog.locator(f'[data-day="{start}"] button').first.focus()
    page.keyboard.press("ArrowRight")
    focused = page.evaluate("document.activeElement.closest('[data-day]')?.dataset.day")
    expected = (datetime.fromisoformat(start) + timedelta(days=1)).date().isoformat()
    check("ArrowRight moves one calendar day", focused == expected, {"before": start, "after": focused})
    page.keyboard.press("Enter")
    dialog.wait_for(state="hidden")
    check("Keyboard selection updates input", field.input_value() == expected)
    check("Keyboard selection returns focus", opener.evaluate("e=>document.activeElement===e"))


def contact_case(page):
    today = page.evaluate("""()=>{const d=new Date();return [
      d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')}""")
    initial = datetime.fromisoformat(today) + timedelta(days=45)
    arrival, departure = initial.date().isoformat(), (initial + timedelta(days=3)).date().isoformat()
    query = urlencode({"arrival": arrival, "departure": departure, "adults": "2",
                       "children": "1", "room": "family-room", "roomCount": "3"})
    goto(page, "/contact?" + query)
    page.wait_for_function("value=>document.querySelector('#arrival').value===value", arg=arrival)
    form = page.locator(".booking-form")
    check("Query hydrates controlled dates", page.locator("#arrival").input_value() == arrival
          and page.locator("#departure").input_value() == departure)
    check("Prefilled date has no blank prompt",
          not wrapper(page.locator("#arrival")).locator(".date-field-placeholder").is_visible())
    form.locator("#name").fill("Calendar QA")
    form.locator("#notes").fill("Keep this unfinished note private.")
    form.locator("#room").select_option(label="Deluxe Twin Room")
    form.locator("#roomCount").select_option("4")
    form.locator("#children").select_option("2")
    form.get_by_role("button", name="Prepare WhatsApp enquiry").click()
    form.locator("#whatsapp-draft").wait_for()
    for index in range(4):
        new_arrival = (initial + timedelta(days=7 * (index + 1))).date().isoformat()
        new_departure = (initial + timedelta(days=7 * (index + 1) + 2)).date().isoformat()
        page.locator("#dock-arrival").fill(new_arrival)
        page.locator("#dock-departure").fill(new_departure)
        page.locator("#dock-adults").select_option("4")
        page.locator(".booking-dock").get_by_role("button", name="Check availability").click()
        page.wait_for_function("value=>document.querySelector('#arrival').value===value", arg=new_arrival)
        values = form.evaluate("e=>Object.fromEntries(new FormData(e))")
        check(f"Dock handoff {index + 1} preserves travel and private fields",
              values.get("arrival") == new_arrival and values.get("departure") == new_departure
              and values.get("adults") == "4" and values.get("room") == "Deluxe Twin Room"
              and values.get("children") == "2" and values.get("roomCount") == "4"
              and values.get("name") == "Calendar QA"
              and values.get("notes") == "Keep this unfinished note private.", values)
        check(f"Dock handoff {index + 1} invalidates stale feedback",
              form.locator("#whatsapp-draft").count() == 0
              and form.locator('[aria-invalid="true"]').count() == 0)
        check(f"Dock handoff {index + 1} keeps private fields out of URL",
              "Calendar" not in page.url and "notes=" not in page.url and "name=" not in page.url)
        if index == 0:
            form.locator("#departure").fill("")
            form.get_by_role("button", name="Prepare WhatsApp enquiry").click()
            check("Invalid date is reported", form.locator('[aria-invalid="true"]').count() > 0)
        elif index < 3:
            form.get_by_role("button", name="Prepare WhatsApp enquiry").click()
            form.locator("#whatsapp-draft").wait_for()
    shot(page, "contact-dates")


def shared_form_case(page, route, selector, name, label):
    goto(page, route)
    field = page.locator(selector).locator(f'input[name="{name}"]').first
    check("Shared empty prompt is visible", wrapper(field).locator(".date-field-placeholder").is_visible())
    pick_next_month(page, field, label, by_input=True)
    check("Shared form fits viewport",
          page.evaluate("document.body.scrollWidth===document.documentElement.clientWidth"))


def route_case(page, route, width):
    page.set_viewport_size({"width": width, "height": 844 if width == 390 else 568})
    goto(page, route)
    geometry = page.evaluate("""()=>({body:document.body.scrollWidth,
      viewport:document.documentElement.clientWidth,
      dock:document.querySelector('.booking-dock').getBoundingClientRect().height,
      reserved:parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--booking-dock-height'))})""")
    check("No horizontal layout overflow", geometry["body"] == geometry["viewport"], geometry)
    check("Dock reservation matches its height", abs(geometry["dock"] - geometry["reserved"]) <= 1, geometry)
    check("No unexpected open calendar", page.locator("dialog.date-picker-dialog[open]").count() == 0)


with sync_playwright() as playwright:
    for engine in engines:
        scope["engine"] = engine
        scope["case"] = "launch"
        browser = None
        try:
            if engine not in ("chromium", "webkit"):
                raise ValueError("Supported engines are chromium and webkit")
            if engine == "webkit" and urlsplit(base).scheme != "https":
                raise ValueError("Use HTTPS for WebKit: the production CSP upgrades HTTP subresources.")
            launch = {"headless": True}
            if engine == "chromium":
                launch["channel"] = "msedge"
            browser = getattr(playwright, engine).launch(**launch)
            context = browser.new_context(viewport={"width": 390, "height": 844},
                                          has_touch=True, is_mobile=True, reduced_motion="reduce")
            page = watch(context.new_page())
            for width in (320, 390):
                run(f"Dock at {width}px", lambda width=width: dock_case(page, width))
            desktop = browser.new_context(viewport={"width": 1440, "height": 900},
                                          reduced_motion="reduce")
            desktop_page = watch(desktop.new_page())
            run("Dock at desktop 1440px", lambda: dock_case(desktop_page, 1440))
            desktop.close()
            page.set_viewport_size({"width": 390, "height": 844})
            run("Keyboard calendar", lambda: keyboard_case(page))
            run("Contact hydration and repeated handoff", lambda: contact_case(page))
            for route, selector, name, label in [
                ("/", ".stay-bar", "arrival", "Arrival date"),
                ("/rooms/deluxe-room", ".stay-bar", "departure", "Departure date"),
                ("/contact", ".booking-form", "arrival", "Arrival date"),
                ("/group-stays", ".group-enquiry", "arrival", "Arrival date"),
                ("/dining", ".dining-enquiry-form", "date", "Preferred date"),
            ]:
                run(f"Shared calendar {route} {name}", lambda r=route, s=selector, n=name, l=label:
                    shared_form_case(page, r, s, n, l))
            for width in (320, 390):
                for route in ROUTES:
                    run(f"Route {route} at {width}px", lambda r=route, w=width: route_case(page, r, w))
            context.close()
        except Exception as error:
            check("Engine audit completes", False, str(error))
        finally:
            if browser:
                browser.close()
        scope["case"] = "runtime"
        errors = [error for error in report["runtime_errors"] if error["engine"] == engine]
        check("No runtime, recursion or resize-observer errors", not errors, errors)

report["passed"] = bool(report["checks"]) and all(item["passed"] for item in report["checks"])
output.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"passed": report["passed"], "checks": len(report["checks"]),
                  "failures": [item for item in report["checks"] if not item["passed"]],
                  "runtime_errors": report["runtime_errors"]}, indent=2))
raise SystemExit(0 if report["passed"] else 1)
