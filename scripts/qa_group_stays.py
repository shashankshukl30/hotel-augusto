"""Focused group-enquiry, menu and shared booking-dock review. No outbound click."""
import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:3082")
    parser.add_argument("--output", type=Path, default=ROOT / "evidence/apple-dominant-revision/group-review")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    checks, errors, console_errors, captures, audits = [], [], [], [], []

    def check(name, passed, details=None):
        checks.append({"name": name, "passed": bool(passed), "details": details})

    def settle(page):
        page.evaluate("""async () => {
          await document.fonts.ready;
          for (const image of document.images) image.loading='eager';
          await Promise.race([
            Promise.allSettled([...document.images].map(i => i.decode())),
            new Promise(resolve=>setTimeout(resolve,8000))
          ]);
        }""")
        page.wait_for_timeout(800)

    def centre(locator):
        locator.evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})")

    def capture(page, name):
        page.screenshot(path=str(args.output / f"{name}.png"))
        captures.append(f"{name}.png")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        try:
            for width, height in [(390, 844), (1440, 1000)]:
                for motion in ["no-preference", "reduce"]:
                    tag = f"{width}-{motion}"
                    context = browser.new_context(
                        viewport={"width": width, "height": height},
                        reduced_motion=motion, timezone_id="Asia/Kolkata",
                    )
                    try:
                        page = context.new_page()
                        page.on("pageerror", lambda error, tag=tag: errors.append({"context": tag, "error": str(error)}))
                        page.on("console", lambda msg, tag=tag: console_errors.append({"context": tag, "error": msg.text}) if msg.type == "error" else None)
                        page.goto(args.base_url.rstrip("/") + "/group-stays", wait_until="networkidle", timeout=90000)
                        settle(page)
                        dimensions = page.evaluate("""() => ({
                          viewport:innerWidth,body:document.body.scrollWidth,
                          client:document.documentElement.clientWidth,
                          paddingBottom:parseFloat(getComputedStyle(document.body).paddingBottom),
                          dock:(()=>{const r=document.querySelector('.booking-dock').getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,height:r.height}})(),
                          brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)
                        })""")
                        check(f"{tag}: no horizontal overflow", dimensions["body"] == dimensions["client"] == width, dimensions)
                        dock = dimensions["dock"]
                        check(f"{tag}: dock fits viewport and reserves page space", dock["x"] >= 0 and dock["right"] <= width + 1 and abs(dock["bottom"] - height) < 1 and dimensions["paddingBottom"] >= dock["height"] - 1)
                        check(f"{tag}: photographs and logo decode", not dimensions["brokenImages"], dimensions["brokenImages"])
                        check(f"{tag}: group page metadata", 50 <= len(page.title()) <= 60, page.title())
                        if motion == "no-preference":
                            capture(page, f"group-{width}-intro")

                        form = page.locator("form.group-enquiry")
                        form.evaluate("e=>scrollTo({top:scrollY+e.getBoundingClientRect().top-100,behavior:'instant'})")
                        page.wait_for_timeout(300)
                        if motion == "no-preference":
                            capture(page, f"group-{width}-form")
                        submit = form.locator(".group-submit")
                        centre(submit)
                        submit.click()
                        check(f"{tag}: empty dates rejected", form.locator('[name="arrival"]').get_attribute("aria-invalid") == "true" and form.locator(".group-form-alert").is_visible())

                        today = date.fromisoformat(page.evaluate("()=>{const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`}"))
                        arrival, departure = (today + timedelta(days=30)).isoformat(), (today + timedelta(days=33)).isoformat()
                        form.locator('[name="arrival"]').fill((today - timedelta(days=1)).isoformat())
                        form.locator('[name="departure"]').fill(arrival)
                        centre(submit)
                        submit.click()
                        check(f"{tag}: past arrival rejected", form.locator('[name="arrival"]').get_attribute("aria-invalid") == "true")
                        form.locator('[name="arrival"]').fill(arrival)
                        form.locator('[name="departure"]').fill(arrival)
                        centre(submit)
                        submit.click()
                        check(f"{tag}: same-day departure rejected", form.locator('[name="departure"]').get_attribute("aria-invalid") == "true")

                        form.locator('[name="departure"]').fill(departure)
                        form.locator('[name="adults"]').fill("51")
                        form.locator('[name="children"]').fill("31")
                        centre(submit)
                        submit.click()
                        check(f"{tag}: out-of-range party rejected", form.locator('[name="adults"]').get_attribute("aria-invalid") == "true" and form.locator('[name="children"]').get_attribute("aria-invalid") == "true")
                        form.locator('[name="adults"]').fill("12")
                        form.locator('[name="children"]').fill("4")
                        form.locator('[name="roomCount"]').select_option("5")
                        form.locator('[name="room"]').select_option("A mix of room types")
                        form.locator('[name="name"]').fill("QA review")
                        form.locator('[name="company"]').fill("Digiocular")
                        form.locator('[name="notes"]').fill("Separate beds where possible. Please confirm meal inclusions.")
                        check(f"{tag}: nights summary correct", "3 nights" in form.locator(".group-nights").inner_text())
                        centre(submit)
                        submit.click()
                        draft = form.locator(".group-draft a")
                        draft.wait_for(state="visible")
                        destination = urlparse(draft.get_attribute("href"))
                        message = parse_qs(destination.query).get("text", [""])[0]
                        check(f"{tag}: correct reviewed WhatsApp draft",
                              destination.netloc == "wa.me" and destination.path == "/918081709146"
                              and all(text in message for text in ["12 adults, 4 children", "Rooms requested: 5", "A mix of room types", "Company or group: Digiocular", "Separate beds where possible."]))
                        check(f"{tag}: draft receives focus", draft.evaluate("e=>e===document.activeElement"))
                        check(f"{tag}: no external window opened", len(context.pages) == 1)
                        check(f"{tag}: displayed draft matches destination", form.locator(".group-draft-message").inner_text() == message)
                        if motion == "no-preference":
                            centre(draft)
                            capture(page, f"group-{width}-draft")
                        form.locator('[name="company"]').fill("Updated group")
                        check(f"{tag}: editing clears stale draft", form.locator(".group-draft").count() == 0 and submit.is_visible())

                        page.add_script_tag(path=str(ROOT / "node_modules/axe-core/axe.min.js"))
                        result = page.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','best-practice']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),passes:r.passes.length}}""")
                        audits.append({"context": tag, **result})
                        check(f"{tag}: group accessibility audit", not result["violations"], result["violations"])
                        if width == 390:
                            page.evaluate("scrollTo({top:0,behavior:'instant'})")
                            trigger = page.get_by_role("button", name="Open navigation", exact=True)
                            trigger.click()
                            page.wait_for_timeout(800)
                            menu = page.get_by_role("dialog", name="Hotel Augusto navigation")
                            check(f"{tag}: menu has group route", menu.get_by_role("link", name="Group stays", exact=False).count() == 1)
                            check(f"{tag}: menu has no horizontal overflow", menu.evaluate("e=>e.scrollWidth===e.clientWidth"))
                            check(f"{tag}: menu links finish visible", page.locator(".navigation-menu-entry").evaluate_all("es=>es.every(e=>parseFloat(getComputedStyle(e).opacity)>.99)"))
                            if motion == "no-preference":
                                capture(page, "mobile-navigation")
                            page.keyboard.press("Escape")
                            check(f"{tag}: Escape returns menu focus", trigger.evaluate("e=>e===document.activeElement"))
                            trigger.click()
                            menu.get_by_role("link", name="Group stays", exact=False).click()
                            check(f"{tag}: same-route menu selection closes", not menu.is_visible())

                        page.goto(args.base_url.rstrip("/") + "/", wait_until="networkidle")
                        settle(page)
                        check(f"{tag}: home has no horizontal overflow", page.evaluate("document.body.scrollWidth===document.documentElement.clientWidth"))
                        check(f"{tag}: shared logo decodes", page.locator(".site-header .brand-artwork img").evaluate("e=>e.complete&&e.naturalWidth>0"))
                        if motion == "no-preference":
                            capture(page, f"home-{width}-hero-dock")
                    finally:
                        context.close()
        finally:
            browser.close()
    check("No page errors", not errors, errors)
    check("No console errors", not console_errors, console_errors)
    failed = [item for item in checks if not item["passed"]]
    report = {
        "date": datetime.now(timezone.utc).isoformat(), "baseUrl": args.base_url,
        "browserClosed": True, "status": "fail" if failed else "pass",
        "checks": checks, "audits": audits, "captures": captures,
        "pageErrors": errors, "consoleErrors": console_errors,
        "summary": {"checks": len(checks), "failed": len(failed), "audits": len(audits), "captures": len(captures)},
    }
    (args.output / "qa.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"summary": report["summary"], "failures": failed, "browserClosed": True}))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
