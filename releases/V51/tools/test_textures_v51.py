from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
from playwright.sync_api import sync_playwright
R=Path('/workspace/RAG');E=R/'evidence/textures-v51';A=R/'assets/textures-v51';errors=[]
# Confirm exact preservation of maps, characters, VFX, costumes and kit code.
a=(R/'build/Runevale-Recast-V50/index.html').read_text();b=(R/'build/Runevale-Recast-V51/index.html').read_text();preserved=[]
for marker in ['const WORLD33_PLANS=','const WORLD33_PLACEMENTS=','window.SHEET_DATA=','window.COSTUME36_DATA=','window.MONSTER_DATA=','const HITBOX42_DATA=','window.VFX47_LIBRARY=','window.SKILL_FX_DATA=','window.CAST_FX_DATA=']:
 va,_=json.JSONDecoder().raw_decode(a[a.index(marker)+len(marker):]);vb,_=json.JSONDecoder().raw_decode(b[b.index(marker)+len(marker):]);assert va==vb,marker;preserved.append(marker)
assert (R/'tools/gear-combat-v50.js').read_text()in b
seams=[]
for n in range(32):
 im=np.array(Image.open(A/f'texture-{n}.png')).astype(float);assert im.shape==(128,128,3)
 interior=np.abs(np.diff(im,axis=1)).mean();edge=np.abs(im[:,-1]-im[:,0]).mean();vertical=np.abs(im[-1]-im[0]).mean();assert max(edge,vertical)<max(13,interior*4),(n,edge,vertical,interior);seams.append({'index':n,'edgeHorizontal':round(edge,2),'edgeVertical':round(vertical,2)})
for id in ['iron','gold','crystal','herb','timber','shell']:
 im=np.array(Image.open(A/f'resource-{id}.png'));assert im.shape==(128,128,4);assert im[0,:,3].max()==0;assert(im[:,:,3]==0).sum()>5000;assert(im[:,:,3]==255).sum()>1000
with sync_playwright()as p:
 br=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage']);q=br.new_page(viewport={'width':1440,'height':1000});q.on('pageerror',lambda e:errors.append(str(e)))
 q.goto('http://127.0.0.1:8767/RAG/build/Runevale-Recast-V51/index.html',timeout=180000);q.locator('#aUser').fill('texture51');q.locator('#aPass').fill('texture51123');q.locator('#aPass2').fill('texture51123');q.get_by_role('button',name='สมัครและเริ่มเล่น').click();q.locator('#cName').fill('TextureHero');q.locator('#cGo').click();q.wait_for_timeout(1200);q.evaluate('running=false;closeWindow();ADM.god=true')
 dims=q.evaluate('''async()=>{const src=[...WORLD33_MATERIALS,...Object.values(CITY49_ART.resources)];return await Promise.all(src.map(s=>new Promise((resolve,reject)=>{let i=new Image;i.onload=()=>resolve([i.naturalWidth,i.naturalHeight]);i.onerror=reject;i.src=s})));}''');assert dims==[[128,128]]*38
 maps=q.evaluate('''()=>{let out=[];for(let p of World33.plans){enterZone(p.zone,p.room,'gm');let cv=document.createElement('canvas');cv.width=cv.height=256;let g=cv.getContext('2d');g.scale(256/Wpx(),256/Hpx());World33.terrain(g,p);let ink=cv.getContext('2d').getImageData(0,0,256,256).data;let count=0;for(let i=3;i<ink.length;i+=4)if(ink[i])count++;if(count<50000)throw Error('empty terrain '+p.key);out.push({key:p.key,material:p.material,paintedPixels:count,spawnFree:!blockedFeet(P.x,P.y)});}return out}''');assert all(v['spawnFree']for v in maps)
 for zone,name in [(0,'capital'),(7,'forest'),(14,'ice'),(16,'coast'),(17,'crypt'),(22,'desert'),(24,'volcano'),(21,'toxic')]:
  q.evaluate(f'''enterZone({zone},null,'gm');P.x=Wpx()*.5;P.y=Hpx()*.5;W.fade=0;W.zoneCard=null;updateCam(10);draw(performance.now()/1000)''');q.wait_for_timeout(120);q.evaluate('draw(performance.now()/1000)');q.screenshot(path=str(E/(name+'.png')))
 q.evaluate('enterZone(1,null,"gm");closeWindow();document.activeElement?.blur()');q.keyboard.press('g');q.locator('#admCode').fill('stefan-gm');q.locator('[data-act=admLogin]').click();q.locator('[data-act=gmTexture51]').click();assert q.locator('figure').count()==32;assert q.locator('[data-act=gmResource49]').count()==6;q.screenshot(path=str(E/'gm-textures.png'))
 for id in ['iron','gold','crystal','herb','timber','shell']:
  q.evaluate('openWindow("resources49")');q.locator(f'[data-act=gmResource49][data-a={id}]').click();assert q.evaluate(f'W.decor.some(d=>d.k==="resource49"&&d.asset==="{id}")')
 # Real render of all new resource sprites at gameplay size, not a static asset montage.
 q.evaluate('''()=>{closeWindow();let cv=document.createElement('canvas');cv.id='props51';cv.width=600;cv.height=180;cv.style='position:fixed;left:20px;top:180px;z-index:99999;width:600px;height:180px';document.body.append(cv);let g=cv.getContext('2d');g.fillStyle='#c1c8a0';g.fillRect(0,0,600,180);Object.keys(CITY49_ART.resources).forEach((asset,i)=>drawDecor(g,{k:'resource49',asset,x:50+i*98,y:125},clock));}''');q.locator('#props51').screenshot(path=str(E/'resources-in-runtime.png'));q.evaluate('document.querySelector("#props51").remove()')
 for w,h in [(390,844),(844,390)]:
  q.set_viewport_size({'width':w,'height':h});q.evaluate('resize();openWindow("resources49")');assert q.evaluate('document.documentElement.scrollWidth<=innerWidth+2');q.screenshot(path=str(E/f'gm-{w}.png'))
 assert not errors,errors;br.close()
(E/'art-validation.json').write_text(json.dumps({'texturesDecoded':len(dims),'all128Pixels':True,'transparentResources':6,'seamMeasurements':seams,'mapsRendered':maps,'preservedData':preserved,'gear50Unchanged':True,'gmAuthenticatedAllSixSpawned':True,'mobileViewports':[390,844],'browserErrors':errors},indent=2));print('Art + integration PASS',flush=True)
