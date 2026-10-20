"""Production headers, share image and repeatable local browser performance samples."""
from pathlib import Path
from datetime import datetime, timezone
from io import BytesIO
import argparse
import json
import urllib.request
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base-url', default='http://127.0.0.1:3081')
parser.add_argument('--output-dir', default='evidence/apple-premium')
args = parser.parse_args()
base = args.base_url.rstrip('/')
report = {'generated': datetime.now(timezone.utc).isoformat(), 'base_url': base,
          'scope': 'Local synthetic samples, not field Core Web Vitals or a Lighthouse score.'}
with urllib.request.urlopen(base) as response:
    report['headers'] = dict(response.headers)
required = ['x-content-type-options', 'x-frame-options', 'referrer-policy',
            'permissions-policy', 'content-security-policy', 'strict-transport-security']
lower = {k.lower(): v for k, v in report['headers'].items()}
assert all(key in lower for key in required)
assert 'x-powered-by' not in lower
with urllib.request.urlopen(base + '/opengraph-image') as response:
    og = response.read()
with Image.open(BytesIO(og)) as photo:
    photo.load()
    report['og'] = {'size': list(photo.size), 'bytes': len(og), 'format': photo.format}
    assert photo.size == (1200, 630)
output_dir = ROOT / args.output_dir
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / 'opengraph-image.png').write_bytes(og)
with urllib.request.urlopen(base + '/robots.txt') as response:
    report['robots'] = response.read().decode()
assert 'Disallow: /' in report['robots']
samples = []
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    for width, throttled in [(1440, False), (390, True), (390, True)]:
        context = browser.new_context(viewport={'width': width, 'height': 844}, device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        cdp = context.new_cdp_session(page)
        cdp.send('Network.enable')
        cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
        if throttled:
            cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 150,
                     'downloadThroughput': 1_600_000 / 8, 'uploadThroughput': 750_000 / 8})
            cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        page.add_init_script("""
          window.__metrics = {lcp:0, cls:0, longTasks:[]};
          new PerformanceObserver(list => { for(const e of list.getEntries()) window.__metrics.lcp=e.startTime; }).observe({type:'largest-contentful-paint', buffered:true});
          new PerformanceObserver(list => { for(const e of list.getEntries()) if(!e.hadRecentInput) window.__metrics.cls+=e.value; }).observe({type:'layout-shift', buffered:true});
          new PerformanceObserver(list => { for(const e of list.getEntries()) window.__metrics.longTasks.push(e.duration); }).observe({type:'longtask', buffered:true});
        """)
        page.goto(base, wait_until='networkidle', timeout=60000)
        page.wait_for_timeout(1600)
        sample = page.evaluate("""()=>({ ...window.__metrics,
          fcp:performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
          resources:performance.getEntriesByType('resource').map(r=>({name:r.name.split('/').pop(),type:r.initiatorType,encodedBytes:r.encodedBodySize,transferBytes:r.transferSize})),
          fontsReady:document.fonts.status,
          imageLoaded:document.querySelector('.hero-scene-image img').complete && document.querySelector('.hero-scene-image img').naturalWidth>0
        })""")
        sample.update({'width':width,'throttled':throttled,'errors':errors})
        assert not errors and sample['imageLoaded']
        samples.append(sample)
        context.close()
    browser.close()
report['performance'] = {'method':'Cold browser cache; mobile: 1.6 Mbps downstream, 150ms latency, 4x CPU slowdown. Local server and machine affect timings.', 'samples': samples}
(ROOT / 'evidence' / 'production-audit.json').write_text(json.dumps(report, indent=2),encoding='utf-8')
print(json.dumps({'headers':'pass','og':report['og'],'samples':[{'width':s['width'],'lcpMs':round(s['lcp']),'cls':s['cls'],'fcpMs':round(s['fcp']),'errors':s['errors']} for s in samples]}))
