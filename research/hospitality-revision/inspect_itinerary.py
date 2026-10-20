import json
from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path(__file__).resolve().parent / "qa-editorial"
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge",headless=True)
    c = b.new_context(viewport={"width":390,"height":844}, reduced_motion="reduce")
    page = c.new_page()
    errors = []
    page.on("console",lambda message: errors.append({"type":message.type,"text":message.text}) if message.type in ["error","warning"] else None)
    page.goto("http://127.0.0.1:3082/varanasi",wait_until="networkidle")
    page.get_by_role("tab",name="The temple",exact=True).click()
    page.wait_for_timeout(800)
    data = page.locator(".itinerary-copy").evaluate_all("nodes=>nodes.map(n=>({html:n.outerHTML.slice(0,650),inert:n.inert,hidden:n.getAttribute('aria-hidden'),visibility:getComputedStyle(n).visibility}))")
    result = {"nodes":data,"console":errors}
    (out/"itinerary-dom-debug.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
    c.close()
    b.close()
