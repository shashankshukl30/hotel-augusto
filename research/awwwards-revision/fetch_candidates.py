import concurrent.futures
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent
CANDIDATES = {
    "varsha-ghats": "https://images.unsplash.com/photo-1752733904669-8a2af6d349f3?fm=jpg&q=85&w=2800&fit=max",
    "varsha-riverfront": "https://images.unsplash.com/photo-1752733904517-e8b987add6b1?fm=jpg&q=85&w=2800&fit=max",
    "martijn-ghats": "https://images.unsplash.com/photo-1706186839147-0d708602587b?fm=jpg&q=85&w=2800&fit=max",
    "vizag-riverfront": "https://images.unsplash.com/photo-1762513839526-c596f5e99a9a?fm=jpg&q=85&w=2800&fit=max",
}

def fetch(item):
    name,url=item
    response=requests.get(url,timeout=40)
    response.raise_for_status()
    (ROOT/f"{name}.jpg").write_bytes(response.content)
    return name,len(response.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(fetch,CANDIDATES.items())))
