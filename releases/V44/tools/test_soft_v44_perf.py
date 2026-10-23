from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path('/workspace/RAG');results={}
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for version,path in [(43,'Runevale-Smooth-Animations-V43'),(44,'Runevale-Soft-VFX-Combat-V44')]:
  q=b.new_page(viewport={'width':1280,'height':800});q.goto('http://127.0.0.1:8767/RAG/build/'+path+'/index.html',timeout=180000);q.locator('#aUser').fill('perf'+str(version));q.locator('#aPass').fill('perf123456');q.locator('#aPass2').fill('perf123456');q.get_by_role('button',name='สมัครและเริ่มเล่น').click();q.locator('#cName').fill('PerfHero');q.locator('#cGo').click();q.wait_for_timeout(700)
  results[version]=q.evaluate("""()=>{running=false;closeWindow();enterZone(0,'training','gm');W.mons=[];W.allies=[];W.npcs=[];W.fx=[];W.fade=0;W.zoneCard=null;updateCam(10);let ids=Object.keys(SkillEffects.data);for(let i=0;i<40;i++){let d=SkillEffects.data[ids[i]],f=SkillEffects.emit(ids[i],P.x-180+(i%8)*50,P.y-80+Math.floor(i/8)*45,{size:92,life:1});f.t=.413+i*.001}let timings=[];for(let i=0;i<100;i++){let start=performance.now();for(let f of W.fx)f.t=.31+(i%30)*.004;draw(performance.now()/1000);timings.push(performance.now()-start)}timings=timings.slice(10).sort((a,b)=>a-b);return{medianMs:timings[45],p95Ms:timings[85],effects:40}}""");print(version,results[version],flush=True);q.close()
 b.close()
(R/'evidence/soft-vfx-v44/performance.json').write_text(json.dumps(results,indent=2))
