"""Check calendar contrast, viewport bounds and native modal focus behavior."""
import argparse
import json
from datetime import date, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="http://127.0.0.1:3082")
parser.add_argument("--output", default="evidence/mobile-date-fix/accessibility-geometry.json")
args = parser.parse_args()
out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
checks = []
arrival = date.today() + timedelta(days=30)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in [(320, 568), (390, 844), (480, 320), (1440, 900)]:
        context = browser.new_context(viewport={"width": width, "height": height},
                                      has_touch=True, reduced_motion="reduce")
        page = context.new_page()
        page.goto(args.base_url, wait_until="networkidle")
        page.locator("#dock-arrival").fill(arrival.isoformat())
        page.locator("#dock-departure").fill((arrival + timedelta(days=2)).isoformat())
        page.locator("#dock-adults").focus()
        page.screenshot(path=str(out.parent / f"selected-{width}.png"))
        fits = page.locator(".dock-date input").evaluate_all(
            "es=>es.every(e=>e.scrollWidth<=e.clientWidth)")
        checks.append({"name": f"Selected dates fit at {width}", "passed": fits})
        page.locator("#dock-arrival").tap()
        dialog = page.locator("dialog[open]")
        dialog.get_by_role("grid").wait_for()
        page.screenshot(path=str(out.parent / f"calendar-{width}.png"))
        page.add_script_tag(path="node_modules/axe-core/axe.min.js")
        violations = page.evaluate("""async()=>{
          const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});
          return r.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.html)}))
        }""")
        checks.append({"name": f"Calendar accessibility at {width}",
                       "passed": not violations, "violations": violations})
        protected = True
        for _ in range(12):
            page.keyboard.press("Tab")
            # Native dialogs permit moving to browser chrome; while the document
            # has focus, no underlying page control may receive that focus.
            protected = protected and dialog.evaluate(
                "e=>!document.hasFocus()||e.contains(document.activeElement)")
        checks.append({"name": f"Tab never reaches background controls at {width}",
                       "passed": protected})
        page.mouse.click(2, 2)
        checks.append({"name": f"Intentional backdrop tap dismisses at {width}",
                       "passed": dialog.count() == 0})
        context.close()
    browser.close()
result = {"base_url": args.base_url, "checks": checks,
          "passed": all(c["passed"] for c in checks)}
out.write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["passed"] else 1)
