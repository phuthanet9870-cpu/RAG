from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright
R=Path('/workspace/RAG');E=R/'evidence/restore-v52';s=(R/'build/Runevale-Recast-V52/index.html').read_text();v48=(R/'build/Runevale-Recast-V48/index.html').read_text();v50=(R/'build/Runevale-Recast-V50/index.html').read_text()
def get(t,m):return json.JSONDecoder().raw_decode(t[t.index(m)+len(m):])[0]
assert get(s,'const WORLD33_MATERIALS=')==get(v48,'const WORLD33_MATERIALS=')
for m in ['const WORLD33_PLANS=','const WORLD33_PLACEMENTS=','window.SHEET_DATA=','window.COSTUME36_DATA=','window.MONSTER_DATA=','window.VFX47_LIBRARY=']:
 assert get(s,m)==get(v50,m),m
assert get(s,'const CITY49_ART=')['icons']==get(v50,'const CITY49_ART=')['icons'];assert not get(s,'const CITY49_ART=')['resources'];assert 'resource49'not in s
errors=[]
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage']);q=b.new_page(viewport={'width':1440,'height':1000});q.on('pageerror',lambda e:errors.append(str(e)))
 q.goto('http://127.0.0.1:8767/RAG/build/Runevale-Recast-V52/index.html',timeout=180000);q.locator('#aUser').fill('restore52');q.locator('#aPass').fill('restore52123');q.locator('#aPass2').fill('restore52123');q.get_by_role('button',name='สมัครและเริ่มเล่น').click();q.locator('#cName').fill('RestoreHero');q.locator('#cGo').click();q.wait_for_timeout(1200);q.evaluate('running=false;closeWindow();ADM.god=true');assert 'V52'in q.title()
 decoded=q.evaluate('''async()=>await Promise.all(WORLD33_MATERIALS.map(src=>new Promise((resolve,reject)=>{let im=new Image;im.onload=()=>resolve([im.naturalWidth,im.naturalHeight]);im.onerror=reject;im.src=src})))''');assert all(w>0 and h>0 for w,h in decoded)
 maps=q.evaluate('''()=>{let a=[];for(let p of World33.plans){enterZone(p.zone,p.room,'gm');if(W.decor.some(d=>d.k==='resource49'))throw Error('old resources');a.push({key:p.key,spawnFree:!blockedFeet(P.x,P.y)});}return a}''');assert all(x['spawnFree']for x in maps)
 q.evaluate('enterZone(0,null,"gm");P.x=Wpx()/2;P.y=Hpx()/2+300;updateCam(10);W.fade=0;W.zoneCard=null;draw(performance.now()/1000)');q.screenshot(path=str(E/'restored-capital.png'));assert q.evaluate('W.npcs.length===19&&!!WIN.costumegacha&&!!Gear50')
 q.evaluate('closeWindow();document.activeElement?.blur()');q.keyboard.press('g');q.locator('#admCode').fill('stefan-gm');q.locator('[data-act=admLogin]').click();assert q.locator('[data-act=gmCity49]').count()==1;assert q.locator('[data-act=gmTexture51]').count()==0;q.locator('[data-act=gmCity49]').click();assert q.locator('[data-act=gmCity49Texture]').count()==0;q.screenshot(path=str(E/'gm-no-textures.png'))
 for w,h in [(390,844),(844,390)]:
  q.set_viewport_size({'width':w,'height':h});q.evaluate('resize();closeWindow();draw(performance.now()/1000)');q.screenshot(path=str(E/f'restored-{w}.png'));assert q.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
 assert not errors,errors;b.close()
(E/'restoration.json').write_text(json.dumps({'htmlSha256':hashlib.sha256(s.encode()).hexdigest(),'exactOriginalMaterialSet':True,'v49AndV51ResourceSpritesRemoved':True,'gmTextureControlsRemoved':True,'maps':maps,'decodedOriginalMaterials':len(decoded),'preservedCityCostumesNpcsGear':True,'browserErrors':errors},indent=2));print('Restoration PASS',flush=True)
