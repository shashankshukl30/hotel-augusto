"""Focused browser review for the hospitality room revision; never sends an enquiry."""
import argparse
import asyncio
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "evidence" / "hospitality-premium"
ROUTES = ["/rooms", "/rooms/deluxe-room", "/rooms/deluxe-twin-room", "/rooms/family-room", "/rooms/compare"]
AXE = ROOT / "node_modules" / "axe-core" / "axe.min.js"


async def settle(page):
    await page.evaluate("document.fonts.ready")
    await page.wait_for_timeout(650)
    await page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    height = await page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, height, 650):
        await page.evaluate("(y)=>window.scrollTo({top:y,behavior:'instant'})", y)
        await page.wait_for_timeout(100)
    await page.wait_for_timeout(650)
    await page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    await page.wait_for_timeout(700)


async def main(base):
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"started": datetime.now(timezone.utc).isoformat(), "base": base, "layouts": [], "axe": [], "interactions": [], "runtimeErrors": [], "externalMessagesSent": 0}

    def check(name, passed, evidence=None):
        report["interactions"].append({"name": name, "passed": bool(passed), "evidence": evidence})

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        try:
            for width in [360, 390, 768, 1024, 1440]:
                context = await browser.new_context(viewport={"width": width, "height": 900 if width > 600 else 844}, device_scale_factor=1)
                page = await context.new_page()
                page.on("pageerror", lambda e: report["runtimeErrors"].append(str(e)))
                page.on("console", lambda m: report["runtimeErrors"].append(m.text) if m.type == "error" else None)
                for route in ROUTES if width != 360 else ["/rooms/compare"]:
                    response = await page.goto(base + route, wait_until="domcontentloaded")
                    await settle(page)
                    data = await page.evaluate("""() => ({
                      inner: innerWidth, client: document.documentElement.clientWidth,
                      body: document.body.scrollWidth,
                      h1: [...document.querySelectorAll('main h1')].map(e=>e.textContent),
                      title: document.title,
                      imageFailures: [...document.querySelectorAll('main img')].filter(e=>{
                        if(e.closest('dialog:not([open]),[aria-hidden="true"]')) return false;
                        const r=e.getBoundingClientRect(); return r.width&&r.height&&(!e.complete||!e.naturalWidth);
                      }).map(e=>e.getAttribute('src')),
                      type: [...document.querySelectorAll('main h1')].map(e=>({font:getComputedStyle(e).fontFamily,size:getComputedStyle(e).fontSize,weight:getComputedStyle(e).fontWeight})),
                      controls: [...document.querySelectorAll('.stay-bar input,.stay-bar select')].map(e=>({name:e.name,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height,font:getComputedStyle(e).fontSize}))
                    })""")
                    passed = response.status == 200 and data["inner"] == width and data["body"] <= data["client"] and len(data["h1"]) == 1 and not data["imageFailures"] and 50 <= len(data["title"]) <= 60
                    report["layouts"].append({"route": route, "width": width, "passed": passed, **data})
                    if width in [390, 1440]:
                        await page.add_script_tag(path=str(AXE))
                        result = await page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}});return r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}));}")
                        report["axe"].append({"route": route, "width": width, "passed": not result, "violations": result})
                        if route in ["/rooms", "/rooms/deluxe-twin-room", "/rooms/compare"]:
                            await page.screenshot(path=str(OUT / f"rooms-{route.split('/')[-1]}-{width}.png"), full_page=True)
                    print("Layout", width, route, "PASS" if passed else "FAIL", flush=True)
                await context.close()

            context = await browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1)
            page = await context.new_page()
            page.on("pageerror", lambda e: report["runtimeErrors"].append(str(e)))
            page.on("console", lambda m: report["runtimeErrors"].append(m.text) if m.type == "error" else None)
            await page.goto(base + "/rooms/compare")
            await page.locator("#compare-first").select_option("family-room")
            names = await page.locator(".comparison-mobile-room h2").all_text_contents()
            check("Mobile compare changes first room", names == ["Family Room", "Deluxe Twin Room"], names)
            await page.locator("#compare-second").select_option("family-room")
            names = await page.locator(".comparison-mobile-room h2").all_text_contents()
            check("Choosing the same comparison room swaps the other selection", names == ["Deluxe Twin Room", "Family Room"], names)
            await page.locator(".comparison-mobile-room").nth(1).get_by_role("link", name="Choose room", exact=True).click()
            await page.wait_for_url("**/contact?room=family-room#enquire")
            await page.wait_for_timeout(400)
            check("Comparison choice preselects enquiry", await page.locator("#room").input_value() == "Family Room")

            for route in ROUTES[1:4]:
                await page.goto(base + route)
                stage = page.locator(".room-photo-main")
                first = await page.locator(".room-photo-caption").inner_text()
                await page.get_by_role("button", name="Next room photograph", exact=True).click()
                second = await page.locator(".room-photo-caption").inner_text()
                check(route + " next photograph changes caption", first != second, second)
                await page.locator(".room-photo-thumbnails button").nth(2).click()
                check(route + " thumbnail selection", await page.locator(".room-photo-thumbnails button").nth(2).get_attribute("aria-pressed") == "true")
                await stage.click()
                dialog = page.locator(".room-photo-dialog")
                check(route + " opens larger photograph", await dialog.is_visible())
                await page.keyboard.press("ArrowRight")
                enlarged = await page.locator(".room-viewer-bottom>p").inner_text()
                check(route + " enlarged viewer arrow wraps", enlarged == first, enlarged)
                await page.keyboard.press("Tab")
                await page.keyboard.press("Tab")
                await page.keyboard.press("Tab")
                check(route + " dialog contains keyboard focus", await page.evaluate("document.activeElement.closest('dialog')!==null"))
                await page.keyboard.press("Escape")
                check(route + " Escape closes and restores focus", not await dialog.is_visible() and await stage.evaluate("(e)=>e===document.activeElement"))
                check(route + " selected room reaches stay bar", await page.locator(".stay-bar select[name=room]").input_value() == route.split("/")[-1])

            form = page.locator(".stay-bar")
            await form.get_by_role("button", name="Plan my stay").click()
            check("Room stay bar rejects empty dates", await form.locator(".stay-error").is_visible() and page.url.endswith("/rooms/family-room"))
            arrival = (date.today() + timedelta(days=11)).isoformat()
            departure = (date.today() + timedelta(days=14)).isoformat()
            await form.locator("input[name=arrival]").fill(arrival)
            await form.locator("input[name=departure]").fill(arrival)
            await form.get_by_role("button", name="Plan my stay").click()
            check("Room stay bar rejects same-day departure", await form.locator(".stay-error").is_visible() and page.url.endswith("/rooms/family-room"))
            await form.locator("input[name=departure]").fill(departure)
            await form.locator("select[name=adults]").select_option("3")
            await form.locator("select[name=children]").select_option("1")
            await form.get_by_role("button", name="Plan my stay").click()
            await page.wait_for_url("**/contact?**#enquire")
            await page.wait_for_timeout(450)
            carried = {name: await page.locator("#" + name).input_value() for name in ["arrival", "departure", "adults", "children", "room"]}
            check("Room dates guests and preference reach contact", carried == {"arrival": arrival, "departure": departure, "adults": "3", "children": "1", "room": "Family Room"}, carried)
            await page.locator(".booking-form button[type=submit]").click()
            href = await page.locator("#whatsapp-draft").get_attribute("href")
            check("Contact prepares encoded WhatsApp draft without sending", href.startswith("https://wa.me/918081709146?text=") and "Family%20Room" in href, href)
            await context.close()

            reduced = await browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
            page = await reduced.new_page()
            page.on("pageerror", lambda e: report["runtimeErrors"].append(str(e)))
            page.on("console", lambda m: report["runtimeErrors"].append(m.text) if m.type == "error" else None)
            await page.goto(base + "/rooms/deluxe-room")
            await page.wait_for_timeout(800)
            await page.get_by_role("button", name="Next room photograph", exact=True).click()
            value = await page.locator(".room-photo-layer").nth(1).evaluate("(e)=>({opacity:getComputedStyle(e).opacity,transition:getComputedStyle(e).transitionDuration})")
            check("Reduced motion keeps photo selection immediate", value["opacity"] == "1" and value["transition"] in ["0s", "1e-05s"], value)
            await reduced.close()
        finally:
            await browser.close()
    report["completed"] = datetime.now(timezone.utc).isoformat()
    report["summary"] = {"layouts": len(report["layouts"]), "axeAudits": len(report["axe"]), "interactions": len(report["interactions"]), "failed": sum(not x["passed"] for key in ["layouts", "axe", "interactions"] for x in report[key]), "runtimeErrors": len(report["runtimeErrors"])}
    report["browserClosed"] = True
    (OUT / "rooms-review.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:3082")
    asyncio.run(main(parser.parse_args().base))
