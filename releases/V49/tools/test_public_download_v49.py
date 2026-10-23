from pathlib import Path
from playwright.sync_api import sync_playwright
import hashlib,json
R=Path('/workspace/RAG');E=R/'evidence/city-v49';expected=json.loads((E/'packages.json').read_text())[0]
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);q=b.new_page(accept_downloads=True);q.goto('https://phuthanet9870-cpu.github.io/RAG/v49/',timeout=90000);q.wait_for_function('!document.querySelector("#get").disabled',timeout=30000);q.wait_for_function('!!navigator.serviceWorker.controller',timeout=30000)
 with q.expect_download(timeout=180000)as event:q.locator('#get').click()
 d=event.value;assert not d.failure(),d.failure();got=Path(d.path());assert got.stat().st_size==expected['bytes'];sha=hashlib.sha256(got.read_bytes()).hexdigest();assert sha==expected['sha256'];b.close()
(E/'public-browser-download.json').write_text(json.dumps({'page':'https://phuthanet9870-cpu.github.io/RAG/v49/','singleClickDownload':True,'suggestedFilename':expected['name'],'sha256':sha,'bytes':expected['bytes']},indent=2));print('Public page: one click downloads the exact full ZIP',flush=True)
