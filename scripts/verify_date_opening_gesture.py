"""Verify touch retargeting, deliberate selection and virtual calendar clicks."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument("--base-url", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--engines", nargs="+", default=["chromium"])
args = parser.parse_args()
report = {"date": datetime.now(timezone.utc).isoformat(), "checks": [], "runtime_errors": []}
scope = {"engine": "", "case": ""}


def check(name, passed):
    entry = {**scope, "name": name, "passed": bool(passed)}
    report["checks"].append(entry)
    print(("PASS " if passed else "FAIL ") + str(entry), flush=True)
    assert passed, name


with sync_playwright() as p:
    for engine in args.engines:
        scope["engine"] = engine
        browser = getattr(p, engine).launch(
            headless=True, **({"channel": "msedge"} if engine == "chromium" else {}))
        context = browser.new_context(viewport={"width": 390, "height": 844},
                                      is_mobile=True, has_touch=True, reduced_motion="reduce")
        page = context.new_page()
        page.set_default_timeout(10000)
        page.on("pageerror", lambda error: report["runtime_errors"].append(
            {**scope, "name": error.name, "message": str(error)}))
        try:
            for route, selector in [
                ("/", "#dock-arrival"), ("/", "#dock-departure"),
                ("/", ".stay-bar input[name=arrival]"), ("/contact", ".booking-form #arrival"),
                ("/group-stays", ".group-enquiry input[name=arrival]"),
                ("/dining", ".dining-enquiry-form input[type=date]"),
            ]:
                scope["case"] = route + " " + selector
                page.goto(args.base_url.rstrip("/") + route, wait_until="networkidle")
                field = page.locator(selector)
                for attempt in range(3):
                    previous = field.input_value()
                    field.tap()
                    dialog = page.locator("dialog.date-picker-dialog[open]")
                    dialog.get_by_role("grid").wait_for(state="visible")
                    check(f"Opening tap {attempt} keeps the calendar open", dialog.is_visible())
                    check(f"Opening tap {attempt} never selects a day", field.input_value() == previous)
                    day = dialog.locator('[role="grid"] [data-day] button:not([disabled])').first
                    expected = day.evaluate("e=>e.closest('[data-day]').dataset.day")
                    if attempt == 1:
                        # Screen-reader/virtual activation may have no pointer or key event.
                        day.evaluate("e=>e.click()")
                    else:
                        day.tap()
                    dialog.wait_for(state="hidden")
                    check(f"Intentional selection {attempt} stores its date",
                          field.input_value() == expected)
                    check(f"Selection {attempt} restores focus",
                          field.evaluate("e=>document.activeElement===e"))
                check("No horizontal overflow", page.evaluate(
                    "document.body.scrollWidth===document.documentElement.clientWidth"))
        except Exception as error:
            report["checks"].append({**scope, "name": "Cases complete", "passed": False,
                                      "detail": str(error)})
        finally:
            context.close()
            browser.close()
report["passed"] = all(c["passed"] for c in report["checks"]) and not report["runtime_errors"]
output = Path(args.output)
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"passed": report["passed"], "checks": len(report["checks"]),
                  "failures": [c for c in report["checks"] if not c["passed"]],
                  "runtime_errors": report["runtime_errors"]}, indent=2))
raise SystemExit(0 if report["passed"] else 1)
