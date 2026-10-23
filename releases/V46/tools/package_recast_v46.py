from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path('/workspace/RAG');A=R/'assets/recast-v46';E=R/'evidence/recast-v46';O=R/'build/Runevale-Recast-V46';S=R/'build/Runevale-Skill-VFX-Sheets-V46';S.mkdir(exist_ok=True);(S/'atlases').mkdir(exist_ok=True)
v=json.loads((E/'runtime/validation.json').read_text());build=json.loads((E/'build.json').read_text());timing=json.loads((E/'timing-validation.json').read_text());assert v['sha256']==build['sha256']==hashlib.sha256((O/'index.html').read_bytes()).hexdigest();assert v['activeSkillsExecuted']==105 and v['passiveSkillsObserved']==41 and v['vfxMainSceneCoverage']==156 and not v['browserErrors'];assert len(timing['realExecutions'])==54 and not timing['errors']
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale Online V46 — สกิลและเอฟเฟกต์วาดใหม่
แตก ZIP แล้วเปิด index.html ภาพทั้งหมดฝังในเกม

แทนภาพสกิลและตัวแสดงผลชุด V44 ด้วยภาพวาดใหม่ครบ146สกิล
ใช้ส่วนประกอบใหม่ร่วมกัน48ตระกูล แต่จัดตำแหน่ง จำนวนครั้ง และจังหวะตามความสามารถจริง
มีภาพหลัก8ภาพและเฟรมคั่น รวม29ภาพต่อชุด (ภาพโปร่งใสทั้งหมด)
ศรเพลิง/น้ำแข็ง/สายฟ้า1–10ลูกตามเลเวล ลูกแก้ว/เหยี่ยว/แทงหอกมีจำนวนฮิตของตัวเอง
ลูกยิงเดินทางก่อนขึ้นดาเมจ จำนวนฮิต ดาเมจ SP และคูลดาวน์ตามความสามารถเดิม
วงร่ายธาตุ วงพื้น กับดัก ฮีล บัฟ พิษ และสกิลบอสใช้ภาพวาดใหม่
แก้ความคลาดเคลื่อนทศนิยมที่ทำให้ขวดไฟบางครั้งขาดฮิตสุดท้าย ให้ครบ6ครั้งตามคำอธิบาย
ท่าเดินและคอสตูม V45 กับแผนที่และการแก้มอนสเตอร์ติดฉากยังอยู่

GM: กด G → stefan-gm → ตรวจ146สกิล / ระดับสกิล / สาธิตจังหวะ
ปุ่มสาธิตในเมนูนี้แสดงภาพเท่านั้น ไม่เปลี่ยน HP/SP/สกิลของตัวละคร

ตรวจสกิลจริง105สกิลใช้งานและ41สกิลติดตัว ตรวจ911ระดับสกิลจากตัวสั่งงานเดิม
ทดสอบ54กรณีเลเวล/เป้าหมาย จำนวนลูกและเวลาฮิตตรงกัน
Chromium เดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่มือถือจริง
อ้างอิงคลิปเมจ20วินาทีที่มีในโปรเจกต์ ไฟล์วิดีโอแนบใหม่ใหญ่เกินขีดจำกัดรับไฟล์32MiB จึงไม่ได้เปิดไฟล์แนบใหม่โดยตรง
''')
for n in ['build.json','pixel-validation.json','timing-validation.json','field-validation.json']:shutil.copy(E/n,O/n)
shutil.copy(E/'runtime/validation.json',O/'runtime-validation.json')
lib=json.loads((A/'library.json').read_text());design=json.loads((A/'design.json').read_text());meta={id:{**{k:v for k,v in d.items()if k!='src'},'file':'atlases/'+id+'.webp'}for id,d in lib.items()}
manifest={'version':46,'library':meta,'skills':design};(S/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for id in lib:shutil.copy(A/'atlases'/(id+'.webp'),S/'atlases'/(id+'.webp'))
viewer='''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Runevale V46 Skill VFX</title><style>body{font:16px/1.6 system-ui;background:#f2eee3;color:#292b31;margin:20px}main{max-width:900px;margin:auto}button,select{font:inherit;padding:8px;margin:5px}canvas{display:block;max-width:100%;background:#c6c5b9;border-radius:16px}small{display:block}</style><main><h1>ชีตเอฟเฟกต์วาดใหม่ V46</h1><p>ภาพ48ตระกูล ใช้ประกอบสกิล146สกิล · ดูจังหวะสกิลจริงได้ในเมนูGMของเกม</p><select id="skill"></select><select id="family"></select><button id="play">หยุด</button><button id="next">เฟรมถัดไป</button><p id="desc"></p><canvas width="600" height="420" id="view"></canvas><small id="phase"></small></main><script>const M=META46,cache={},s=document.getElementById('skill'),f=document.getElementById('family'),cv=document.getElementById('view'),g=cv.getContext('2d');let selected='fireball',k=0,last=0,playing=true;s.innerHTML=Object.values(M.skills).map(d=>'<option value="'+d.id+'">'+d.name+'</option>').join('');f.innerHTML=Object.keys(M.library).sort().map(id=>'<option>'+id+'</option>').join('');function load(id){selected=id;f.value=id;k=0;if(!cache[id]){let im=cache[id]=new Image;im.src=M.library[id].file}}s.onchange=()=>{let d=M.skills[s.value];document.getElementById('desc').textContent=d.descriptions[d.max-1];load(d.family)};f.onchange=()=>load(f.value);document.getElementById('play').onclick=()=>{playing=!playing;document.getElementById('play').textContent=playing?'หยุด':'เล่น';last=0};document.getElementById('next').onclick=()=>{playing=false;k=(Math.floor(k)+1)%29};function tick(t){if(playing&&last)k+=Math.min(.1,(t-last)/1000)/.026;last=t;let d=M.library[selected],im=cache[selected],i=Math.floor(k)%29,r=d.frameRects[i],a=d.anchor,scale=2.1;g.clearRect(0,0,600,420);if(im?.naturalWidth)g.drawImage(im,r[0],r[1],r[2],r[3],300+(r[4]-a[0])*scale,310+(r[5]-a[1])*scale,r[2]*scale,r[3]*scale);document.getElementById('phase').textContent=selected+' · '+(i+1)+' / 29';requestAnimationFrame(tick)}s.value='mg_fire';s.onchange();requestAnimationFrame(tick)</script></html>'''
(S/'Viewer.html').write_text(viewer.replace('META46',json.dumps(manifest,ensure_ascii=False,separators=(',',':'))))
(S/'อ่านก่อนใช้.txt').write_text('''Runevale V46 — ภาพวาดเอฟเฟกต์ใหม่
เปิด Viewer.html ดูภาพทั้ง48ตระกูลและการเชื่อมโยง146สกิล
atlases/*.webp เป็นภาพlosslessพื้นหลังโปร่งใส รวม1392เฟรม
manifest.json library ระบุ frameRects=[x,y,w,h,offsetX,offsetY], frameSize128, anchor, frameCount29
วาดส่วนrectที่ตำแหน่งโลก+(offset-anchor)*scale ไม่ใช่กริดช่องเท่ากัน
skills ระบุตระกูลภาพ รูปแบบการปล่อย จังหวะและจำนวนฮิตที่ตรวจจากสกิลจริง
ภาพวงร่าย/กระสุน/กระแทก/วงพื้นถูกประกอบเป็นเอฟเฟกต์ตามความสามารถในไฟล์เกม
Viewerดูองค์ประกอบภาพ ส่วนสาธิตสกิลเต็มรูปแบบอยู่ในเมนูGMของเกมV46
''')
packages=[]
for root in [O,S]:
 path=R/'dist'/(root.name+'.zip')
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for p in sorted(root.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(root.parent)))
 with zipfile.ZipFile(path)as z:assert z.testzip()is None
 row={'name':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};packages.append(row);print(row,flush=True)
(E/'packages.json').write_text(json.dumps(packages,indent=2))
