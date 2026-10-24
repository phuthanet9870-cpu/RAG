from pathlib import Path
from PIL import Image
import json,hashlib,zipfile,shutil
R=Path('/workspace/RAG');E=R/'evidence/effects-v54';A=R/'assets/effects-v54';O=R/'build/Runevale-Recast-V54';v=json.loads((E/'validation.json').read_text());assert not v['browserErrors'];assert v['rankFactionCases']==600;sha=hashlib.sha256((O/'index.html').read_bytes()).hexdigest();assert sha==v['htmlSha256']==json.loads((E/'build.json').read_text())['htmlSha256']
s=(O/'index.html').read_text();base=(R/'build/Runevale-Recast-V53/index.html').read_text();preserved=[]
def get(t,m):return json.JSONDecoder().raw_decode(t[t.index(m)+len(m):])[0]
for m in ['const WORLD33_MATERIALS=','const WORLD33_PLANS=','const WORLD33_PLACEMENTS=','window.SHEET_DATA=','window.COSTUME36_DATA=','window.MONSTER_DATA=','const Unlock53Design=','const UNLOCK53_ICONS=']:
 assert get(s,m)==get(base,m),m;preserved.append(m)
for marker,end in [('const Unlock53Rules=','const SKILL_COUNT ='),('const Team48=','window.Team48=Team48;'),('const Gear50=','const UNLOCK53_ICONS=')]:
 def chunk(t):return t[t.index(marker):t.index(end,t.index(marker))]
 assert chunk(s)==chunk(base),marker
old=get(base,'window.VFX47_LIBRARY=');new=get(s,'window.VFX47_LIBRARY=');assert not any(k.startswith('u53_')for k in new)
for k,d in old.items():
 if not k.startswith('u53_'):assert new[k]==d,k
mapping=json.loads((A/'skill-map.json').read_text());assert len(mapping)==72
(A/'skills').mkdir(exist_ok=True)
for id,m in mapping.items():shutil.copyfile(A/m['file'],A/'skills'/(id+'.png'));m['skillSheet']='skills/'+id+'.png'
(A/'skill-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2));(E/'preservation.json').write_text(json.dumps({'base':53,'unchangedData':preserved,'skillDefinitionsIdentical':True,'teamAndEquipmentSystemsIdentical':True,'all48PreviousVfxFamiliesIdentical':True,'oldFlatV53EffectAtlasesRemoved':True},indent=2))
(A/'manifest.json').write_text(json.dumps({'version':54,'skillSheets':72,'sharedFamilies':27,'nativeFramesPerFamily':8,'nativeFramesTotal':216,'frameSize':[128,128],'atlasSize':[1024,128],'layout':'one horizontal row, 8 slots, left to right','transparent':True,'nativeOnly':True,'interpolatedFrames':0,'runtime':'PNG frame selection, no runtime shape drawing','anchors':'see library.json metadata; [64,108] grounded, [64,64] flying'},indent=2))
# Runtime data URLs are omitted from the asset ZIP; clean metadata references the PNGs.
lib=json.loads((A/'library.json').read_text())
for k,d in lib.items():d['src']='atlases/'+k[4:]+'.png'
(A/'atlas-metadata.json').write_text(json.dumps(lib,indent=2))
preview='''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Runevale V54 Sprite Sheet</title><style>body{background:#e8e0ce;color:#302d25;font:16px system-ui;margin:20px;padding:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}article{background:#faf7ed;border:1px solid #b89c62;border-radius:12px;padding:10px}canvas{background:#393d40;image-rendering:pixelated;width:100%;border-radius:8px}small{display:block;overflow-wrap:anywhere}</style><h1>V54 · Sprite Sheet เอฟเฟกต์ 72สกิล</h1><p>8เฟรมวาดจริงต่อแอนิเมชัน · ภาพ128×128 · 27รูปแบบที่ใช้ร่วมกันตามชนิดพลัง · ไม่มีการสร้างเฟรมคั่น</p><div class="grid" id="grid"></div><script>const map='''+json.dumps(mapping,ensure_ascii=False)+''';const images={};for(const[id,m]of Object.entries(map)){const a=document.createElement('article'),b=document.createElement('b'),cv=document.createElement('canvas'),note=document.createElement('small');b.textContent=m.name;note.textContent=m.skillSheet+' · '+m.family;cv.width=cv.height=128;cv.dataset.id=id;a.append(b,cv,note);grid.append(a);let im=images[id]=new Image;im.src=m.skillSheet;}function tick(t){let k=Math.floor(t/85)%8;for(let cv of document.querySelectorAll('canvas')){let im=images[cv.dataset.id];if(im?.naturalWidth){let g=cv.getContext('2d');g.clearRect(0,0,128,128);g.drawImage(im,k*128,0,128,128,0,0,128,128);}}requestAnimationFrame(tick)}requestAnimationFrame(tick)</script></html>'''
(A/'preview.html').write_text(preview)
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale V54 — Sprite Sheet เอฟเฟกต์เข้าชุดเดิม
แตกZIP แล้วเปิด index.html ภาพทั้งหมดฝังในเกมแล้ว
แทนเอฟเฟกต์สกิลใหม่72สกิลของ12คลาสขั้นสูง ด้วยภาพวาดแบบแสงเงามีรายละเอียดเข้ากับเอฟเฟกต์เดิม
27รูปแบบพลัง ใช้8เฟรมวาดจริงต่อแอนิเมชัน ไม่มีoptical-flow ไม่มีcrossfade และไม่มีรูปทรงVFXแบบเดิมของV53
สกิลที่ใช้พลังประเภทเดียวกันใช้ชีตร่วมกัน แต่ยังมีชื่อ ความสามารถ จำนวนฮิต คูลดาวน์ และSPเดิม
เฟรมแยกเป็นภาพPNGโปร่งใส เฟรม128×128 ชีต1024×128 มี8ช่องแนวนอน
GM: G > stefan-gm > Sprite Sheet เอฟเฟกต์ใหม่V54 เพื่อดูทั้งชีตและเลือกสกิลตรวจทีละเฟรม
คลาส สกิล ดาเมจ ระบบทหาร เงา คอสตูม เมือง และพื้นผิวยังเหมือนV53/V52
ทดสอบสกิลใช้งาน600กรณี ทั้ง5ระดับและ2ฝ่าย ตรวจGMและจอมือถือจำลอง
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่มือถือจริง
''')
(A/'อ่านก่อนใช้งาน.txt').write_text('''เปิดpreview.htmlเพื่อดูภาพเคลื่อนไหวของ72สกิล
skills/ มีชีตPNGแยกตามชื่อIDของทุกสกิล72ไฟล์
atlases/ มี27ตระกูลภาพที่ใช้ร่วมกันตามชนิดเอฟเฟกต์
8เฟรมวาดจริง ขนาดเฟรม128×128 ชีต1024×128 เรียงซ้ายไปขวา
ดูจุดยึดจากatlas-metadata.json และจับคู่ชื่อไทย/อาชีพจากskill-map.json
reviews/ มีภาพสำหรับตรวจเฟรมพร้อมข้อความชื่อ ไม่ใช่ภาพนำเข้าเกม
ภาพต้นฉบับขนาดใหญ่ไม่รวมในแพ็กนี้ เพื่อลดการสับสนกับชีตที่จัดเฟรมเรียบร้อยแล้ว
''')
packs=[]
for name,root in [('Runevale-Recast-V54.zip',O),('Runevale-Skill-Sprite-Sheets-V54.zip',A)]:
 p=R/'dist'/name
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for f in root.rglob('*'):
   if f.is_file()and f.name!='library.json'and not f.name.startswith('reference-'):z.write(f,str(f.relative_to(root.parent)))
 with zipfile.ZipFile(p)as z:
  assert z.testzip()is None
  if root==O:assert hashlib.sha256(z.read(O.name+'/index.html')).hexdigest()==sha
 packs.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(E/'packages.json').write_text(json.dumps(packs,indent=2));print(packs,flush=True)
