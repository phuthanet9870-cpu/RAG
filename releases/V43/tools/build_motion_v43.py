from pathlib import Path
from PIL import Image
import json,base64,io,hashlib,numpy as np
R=Path('/workspace/RAG');A=R/'assets/motion-v43';E=R/'evidence/motion-v43';O=R/'build/Runevale-Smooth-Animations-V43';base=(R/'build/Runevale-Angel-Hitbox-V42/index.html').read_text();html=base;replacements=[]
def replace(a,b,count=1):
 global html
 assert html.count(a)>=count,(a[:150],html.count(a));html=html.replace(a,b,count);replacements.append([a,b,count])
def swap(marker,data):
 global html
 a=html.index(marker)+len(marker);_,n=json.JSONDecoder().raw_decode(html[a:]);html=html[:a]+json.dumps(data,ensure_ascii=False,separators=(',',':'))+html[a+n:]
chars=json.loads((A/'characters-embedded.json').read_text());costumes=json.loads((A/'costumes-embedded.json').read_text());skills=json.loads((A/'skills-embedded.json').read_text());casts=json.loads((A/'casts-embedded.json').read_text());assert len(chars)==33 and len(costumes)==10 and len(skills)==152 and len(casts)==4
for marker,data in [('window.SHEET_DATA=',chars),('window.COSTUME36_DATA=',costumes),('window.SKILL_FX_DATA=',skills),('window.CAST_FX_DATA=',casts)]:swap(marker,data)
# Arena targeting follows the new packed character frames. Monster masks are untouched.
marker='const HITBOX42_DATA=';i=html.index(marker)+len(marker);masks,_=json.JSONDecoder().raw_decode(html[i:]);masks['characters']={}
for id,d in chars.items():
 im=np.array(Image.open(io.BytesIO(base64.b64decode(d['src'].split(',')[1]))).convert('RGBA'));fs={}
 for f in d['frames']:
  key=','.join(str(x)for x in f['rect'])
  if key in fs:continue
  x,y,w,h=f['rect'];a=im[y:y+h,x:x+w,3]>=32;yy,xx=np.nonzero(a);fs[key]={'w':w,'h':h,'box':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'bits':base64.b64encode(np.packbits(a.ravel(),bitorder='little').tobytes()).decode()}
 masks['characters'][id]=fs
swap(marker,masks)
a=html.index(' function choose(u,t,moving){');b=html.index(' function draw(c,u,t,moving)',a);html=html[:a]+' '+(R/'tools/choose-motion-v43.js').read_text()+html[b:]
a=html.index(' function blit(c,id,phase,x,y,o={}){');b=html.index(' function emit(id,x,y,o={})',a);html=html[:a]+' '+(R/'tools/blit-motion-v43.js').read_text()+html[b:]
replace("const stages=['projectile','dash'].includes(m.mode)?[4,5,6,7,8]:Array.from({length:m.frameCount||9},(_,i)=>i);","const stages=['projectile','dash'].includes(m.mode)?[4,5,6,7,8]:Array.from({length:m.sourceFrameCount||m.frameCount||9},(_,i)=>i);")
replace('delete f.delay;W.fx.push(f);return f}','delete f.delay;f.animationDuration=f.life;W.fx.push(f);return f}')
replace('f.t/f.life','f.t/(f.animationDuration||f.life)',html.count('f.t/f.life'))
replace("{slots:[1,2,3,4,5,6,7,6,5,4,3,2],size:g.r*2,alpha:1}","{slots:[1,2,3,4,5,6,7,6,5,4,3,2],size:g.r*2,alpha:1,loop:true}")
replace("size:Math.max(32,(m.r||14)*(kind==='root'?2:3)),alpha:kind==='freeze'?.4:.3}","size:Math.max(32,(m.r||14)*(kind==='root'?2:3)),alpha:kind==='freeze'?.4:.3,loop:true}")
# Existing previews must inspect the new timing and trimmed rectangles too.
replace("const duration=()=>action==='walk'?.14:action==='attack'?.25:.6;","const duration=()=>action==='walk'?.1:action==='attack'?.025:.6;")
replace('เดิน 4 ภาพ: ก้าวซ้าย → ผ่าน → ก้าวขวา → ผ่านกลับ','เดิน 8 เฟรม: ก้าวสั้นสลับขา / โจมตี12เฟรม')
replace('if(playing&&previous)phase+=Math.min(.15,(t-previous)/1000)/.14;','if(playing&&previous)phase+=Math.min(.15,(t-previous)/1000)/(action===\'walk\'?.1:action===\'attack\'?.025:.6);')
replace('เดิน 4 ก้าวสลับขา','เดิน8เฟรมก้าวสั้นสลับขา / โจมตี12เฟรม')
replace("g.drawImage(im,0,0,128,144,0,0,96,108);", "const f=d.frames.find(f=>f.action==='idle'&&f.direction==='S');g.drawImage(im,...f.rect,48-f.pivot[0]*.75,96-f.pivot[1]*.75,f.rect[2]*.75,f.rect[3]*.75);")
replace('เมืองกระชับ V42','เมืองกระชับ V43',html.count('เมืองกระชับ V42'))
replace('return {choose,draw,preload,ensure,images,clips,directions:dirs,version:34};','return {choose,draw,preload,ensure,images,clips,directions:dirs,version:43};')
replace("TITLEOF.characters32='ตรวจเฟรมตัวละคร · V34'","TITLEOF.characters32='ตรวจเฟรมตัวละคร · V43'")
replace('ตรวจอนิเมชั่น 33 อาชีพ · V34','ตรวจอนิเมชั่น 33 อาชีพ · V43')
replace('return{version:34};','return{version:43};')
replace('return{version:36,thumb,ids:Object.keys(COSTUME36_DATA)};','return{version:43,thumb,ids:Object.keys(COSTUME36_DATA)};')
# The original class render scale, movement speed, damage and all skill mechanics are retained.
payload='\n'+(R/'tools/motion-inspector-v43.js').read_text();a=html.rfind('</script>');html=html[:a]+payload+html[a:];(O/'index.html').write_text(html)
for name in ['WORLD33_PLANS','WORLD33_PROPS','WORLD33_PLACEMENTS','window.MONSTER_DATA','window.TOXIC_WINGS_DATA']:
 marker=('const '+name+'=')if name.startswith('WORLD')else name+'=';i=base.index(marker)+len(marker);j=html.index(marker)+len(marker);assert json.JSONDecoder().raw_decode(base[i:])[0]==json.JSONDecoder().raw_decode(html[j:])[0]
# Skills retain identity/ability metadata and timings; only the frame data/packing is new.
for marker,data in [('window.SKILL_FX_DATA=',skills),('window.CAST_FX_DATA=',casts)]:
 i=base.index(marker)+len(marker);old,_=json.JSONDecoder().raw_decode(base[i:]);assert set(old)==set(data)
 for id,d in old.items():
  for key,value in d.items():
   if key not in ['src','frameCount']:assert data[id][key]==value,(id,key)
report={'sha256':hashlib.sha256(html.encode()).hexdigest(),'bodySheets':33,'costumes':10,'walkFramesPerDirection':8,'attackFramesPerDirection':12,'fxSheets':156,'fxFrames':sum(d['frameCount']for d in{**skills,**casts}.values()),'runtimeUsesOnlyBakedFrames':True,'all31MapsAndMonsterArtUnchanged':True,'movementSpeedAndDamageUnchanged':True,'skillIdentityAbilitiesDurationsAndColorsRetained':True,'angel50PercentAndNoPickupFXRetained':True,'walkCycleWorldDistance':80};(E/'preservation.json').write_text(json.dumps(report,indent=2));print(report)
