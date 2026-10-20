"""Reuse the editorial acceptance suite and verify the enlarged type and motion."""
from pathlib import Path

BASE_CHECK = Path(__file__).with_name("verify_editorial.py")
source = BASE_CHECK.read_text(encoding="utf-8")
source = source.replace('"cinematic-redesign"', '"apple-large"')

layout_marker = '            assert metrics["inner"] == width, metrics'
layout_checks = r'''            metrics["typography"] = page.evaluate("""() => {
                const style = selector => {
                    const element = document.querySelector(selector);
                    if (!element) return null;
                    const computed = getComputedStyle(element);
                    return {fontSize:parseFloat(computed.fontSize),fontWeight:computed.fontWeight,
                        radius:computed.borderRadius,height:element.getBoundingClientRect().height};
                };
                return {title:style("h1"),body:style(".river-feature-copy p:not(.feature-context)"),
                    caption:style(".gallery-caption"),metadata:style(".gallery-count"),
                    filter:style(".gallery-filters button"),photo:style(".gallery-image-wrap"),
                    guideControl:style(".destination-guide-nav a")};
            }""")
            typography = metrics["typography"]
            assert typography["title"]["fontSize"] >= (60 if width <= 760 else 80), typography
            assert typography["title"]["fontWeight"] == "650", typography
            if route == "gallery":
                assert typography["filter"]["height"] >= 44, typography
                assert typography["metadata"]["fontSize"] >= 14, typography
                assert typography["caption"]["fontSize"] >= 18, typography
            else:
                assert typography["guideControl"]["height"] >= 44, typography
                assert typography["body"]["fontSize"] >= (17 if width <= 760 else 18), typography
            assert metrics["inner"] == width, metrics'''
assert layout_marker in source
source = source.replace(layout_marker, layout_checks)

motion_marker = "    context.close()\n    browser.close()"
motion_checks = r'''    context.close()
    motion_context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="no-preference")
    motion_page = motion_context.new_page()
    motion_page.on("pageerror", lambda error: report["errors"].append({"message": str(error), "stack": error.stack, "step": "Motion review"}))
    motion_page.goto(f"{BASE}/varanasi", wait_until="networkidle")
    motion_page.evaluate("document.querySelector('#temple').scrollIntoView({behavior:'instant',block:'center'})")
    motion_page.wait_for_timeout(100)
    start = motion_page.locator("#temple .destination-card-copy").evaluate("element => ({transform:getComputedStyle(element).transform,opacity:getComputedStyle(element).opacity})")
    motion_page.screenshot(path=str(OUT / "varanasi-motion-start.png"))
    motion_page.wait_for_timeout(1100)
    finish = motion_page.locator("#temple .destination-card-copy").evaluate("element => ({transform:getComputedStyle(element).transform,opacity:getComputedStyle(element).opacity})")
    motion_page.screenshot(path=str(OUT / "varanasi-motion-finish.png"))
    report["motion"] = {"start":start,"finish":finish,"reducedMotionLayoutChecks":8}
    assert start != finish, report["motion"]
    assert float(finish["opacity"]) == 1, report["motion"]
    motion_context.close()
    browser.close()'''
assert motion_marker in source
source = source.replace(motion_marker, motion_checks)
exec(compile(source, str(BASE_CHECK), "exec"), {"__file__": str(BASE_CHECK.resolve())})
