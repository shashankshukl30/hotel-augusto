"""Focused route, disclosure, arrival and dining checks; never sends a message."""
import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "evidence/hospitality-revision"


async def main(base):
    OUT.mkdir(parents=True, exist_ok=True)
    records, interactions = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        try:
            for width in [390, 1440]:
                context = await browser.new_context(
                    viewport={"width": width, "height": 1000},
                    reduced_motion="reduce",
                    permissions=["clipboard-read", "clipboard-write"],
                )
                for route in ["hotel", "dining"]:
                    page = await context.new_page()
                    errors, console_errors, maps = [], [], []
                    page.on("pageerror", lambda err: errors.append(str(err)))
                    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
                    page.on("request", lambda req: maps.append(req.url) if "google.com/maps" in req.url else None)
                    response = await page.goto(base + "/" + route, wait_until="networkidle")
                    await page.evaluate("document.fonts.ready")
                    for image in await page.locator("main img").all():
                        await image.scroll_into_view_if_needed()
                        await image.evaluate("(img)=>img.decode()")
                    await page.locator("footer").scroll_into_view_if_needed()
                    await page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
                    await page.wait_for_timeout(300)
                    await page.screenshot(path=str(OUT / f"{route}-{width}.png"), full_page=True)
                    metrics = await page.evaluate("""()=>({
                      width:document.documentElement.clientWidth,scrollWidth:document.body.scrollWidth,
                      title:document.title,h1:document.querySelector('h1').innerText,
                      headline:{font:getComputedStyle(document.querySelector('h1')).fontFamily,size:getComputedStyle(document.querySelector('h1')).fontSize},
                      images:[...document.querySelectorAll('main img')].map(e=>({alt:e.alt,loaded:e.complete&&e.naturalWidth>0})),
                      duplicateIds:[...document.querySelectorAll('[id]')].map(e=>e.id).filter((id,i,a)=>a.indexOf(id)!==i)
                    })""")
                    records.append({"route": route, "viewport": width, "status": response.status, **metrics, "errors": errors, "consoleErrors": console_errors})
                    details = page.locator(".hospitality-service-detail").first
                    await details.locator("summary").focus()
                    await page.keyboard.press("Enter")
                    interactions.append({"test": f"{route} disclosure keyboard at {width}", "passed": await details.get_attribute("open") is not None})
                    if route == "hotel":
                        guide = page.locator(".arrival-guide")
                        before = await guide.locator("iframe").count()
                        tab = guide.get_by_role("tab", name="By air")
                        await tab.focus()
                        await page.keyboard.press("ArrowRight")
                        selected = guide.get_by_role("tab", name="By rail")
                        href = await guide.locator(".arrival-guide-enquire").get_attribute("href")
                        message = parse_qs(urlparse(href).query)["text"][0]
                        interactions.append({"test": f"arrival keyboard and rail enquiry at {width}", "passed": await selected.get_attribute("aria-selected") == "true" and "train" in message and urlparse(href).path == "/918081709146"})
                        await page.keyboard.press("End")
                        interactions.append({"test": f"arrival End key at {width}", "passed": await guide.get_by_role("tab", name="By road").get_attribute("aria-selected") == "true"})
                        await guide.get_by_role("button", name="Copy address").click()
                        clipboard = await page.evaluate("navigator.clipboard.readText()")
                        interactions.append({"test": f"copy address at {width}", "passed": "Hotel Augusto" in clipboard and "D 36/1" in clipboard and "221001" in clipboard})
                        interactions.append({"test": f"no map before activation at {width}", "passed": before == 0 and not maps})
                        await page.evaluate("document.activeElement?.blur()")
                        await guide.scroll_into_view_if_needed()
                        await page.screenshot(path=str(OUT / f"arrival-{width}.png"))
                        await guide.get_by_role("button", name="Load Google map").click()
                        frame = guide.locator("iframe")
                        await frame.wait_for(state="visible")
                        await page.wait_for_timeout(6000)
                        frame_object = await frame.element_handle()
                        map_frame = await frame_object.content_frame()
                        map_text = await map_frame.locator("body").inner_text()
                        interactions.append({"test": f"map activation at {width}", "passed": await frame.count() == 1 and "Hotel" in (await frame.get_attribute("src")), "mapRequests": maps, "visibleMapText": map_text})
                        await guide.locator(".arrival-guide-map").screenshot(path=str(OUT / f"map-{width}.png"))
                    else:
                        links = await page.locator(".hospitality-dining-enquiry a").evaluate_all("es=>es.map(e=>({text:e.textContent,href:e.href}))")
                        interactions.append({"test": f"three distinct meal enquiries at {width}", "passed": len(links) == 3 and len({link["href"] for link in links}) == 3 and all(urlparse(link["href"]).path == "/918081709146" for link in links), "links": links})
                    await page.close()
                await context.close()
        finally:
            await browser.close()
    passed = all(r["status"] == 200 and r["width"] == r["scrollWidth"] and not r["errors"] and not r["duplicateIds"] and all(i["loaded"] for i in r["images"]) for r in records) and all(i["passed"] for i in interactions)
    report = {"completed": datetime.now(timezone.utc).isoformat(), "base_url": base, "pages": records, "interactions": interactions, "passed": passed, "messagesSent": 0, "visuallyInspected": False}
    (OUT / "hotel-dining-review.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"pages": len(records), "interactions": len(interactions), "passed": passed, "failures": [i for i in interactions if not i["passed"]]}, indent=2))
    assert passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:3082")
    asyncio.run(main(parser.parse_args().base_url.rstrip("/")))
