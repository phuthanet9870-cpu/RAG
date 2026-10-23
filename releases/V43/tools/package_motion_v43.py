from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path('/workspace/RAG');E=R/'evidence/motion-v43';A=R/'assets/motion-v43';O=R/'build/Runevale-Smooth-Animations-V43';S=R/'build/Runevale-Animation-Sheets-V43';S.mkdir(exist_ok=True)
v=json.loads((E/'validation.json').read_text());p=json.loads((E/'preservation.json').read_text());px=json.loads((E/'pixel-validation.json').read_text());sha=hashlib.sha256((O/'index.html').read_bytes()).hexdigest();assert sha==v['sha256']==p['sha256'];assert v['bodyDirectionCases']==172 and v['vfxMainSceneCoverage']==156 and v['activeSkillsExecuted']==105 and v['passiveSkillsObserved']==41 and not v['browserErrors'];assert px['feetAnchoredEveryWalkFrame']and px['allFXOriginalKeyframesExact']
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale Online V43 — Smooth Character & Skill Animations
แตก ZIP แล้วเปิด index.html ทุกภาพฝังในไฟล์เกม
ตัวละคร33แบบและคอสตูม10ชุดปรับการเคลื่อนไหวครบ4ทิศ
เดิน8เฟรมต่อทิศ ใช้ท่าก้าวสั้น ลดการกางขาและจังหวะถี่เกินไป
เพิ่มภาพเริ่มเดินและหยุดเดิน จุดยึดเท้าอยู่บนพื้นทุกเฟรม
โจมตี12เฟรมต่อทิศ รวมเตรียมโจมตี ออกท่า และคืนท่ายืน
สร้างเฟรมกลางจากชีตเดิมและบันทึกลงภาพจริง ไม่มีริกหรือโค้ดบิดขาขณะเล่น
ยังคงรูปลักษณ์เดิม ใช้ทุกอาชีพและคอสตูมที่มีอยู่แล้วในบัญชี
VFXครบ156ชีต: สกิล146สกิล เอฟเฟกต์ToxicQueen6ชุด และวงร่าย4ชุด
เพิ่มเป็น29–33เฟรมต่อชีต รวม5092เฟรม โดยคงภาพหลัก สี และระยะเวลาเดิม
บัฟติดตัวไม่แสดงออร่าค้างตามเดิม กลไกสกิลและดาเมจไม่เปลี่ยน
GM กดG → stefan-gm → ตรวจเดิน / โจมตี / VFX ทุกเฟรมV43
เลือกครบ33ตัวละคร/10คอสตูมและ156VFX หยุดภาพและเลื่อนดูทีละเฟรมได้
เมืองและแมพ31พื้นที่จากV42คงเดิม นางฟ้าเลเวลอัปความทึบ50% และเก็บของไม่มีVFXยังคงเดิม
Hitboxมอนสเตอร์จากV42คงเดิม ตัวประลองปรับmaskให้ตรงชีตใหม่
ทดสอบChromiumผ่านHTTPในเครื่อง รวมขนาดจอมือถือจำลอง ไม่ใช่โทรศัพท์จริง
''')
for name in ['validation.json','pixel-validation.json','preservation.json']:shutil.copy2(E/name,O/name)
meta={'bodies':{},'fx':{}}
for file,folder,kind in [('characters-embedded.json','characters','bodies'),('costumes-embedded.json','costumes','bodies'),('skills-embedded.json','fx','fx'),('casts-embedded.json','fx','fx')]:
 data=json.loads((A/file).read_text());(S/folder).mkdir(exist_ok=True)
 for id,d in data.items():
  shutil.copy2(A/folder/(id+'.webp'),S/folder/(id+'.webp'));meta[kind][id]={k:v for k,v in d.items()if k!='src'};meta[kind][id]['file']=folder+'/'+id+'.webp'
(S/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
viewer='''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Runevale Animation Sheets V43</title><style>body{margin:0;background:#f5f1e7;color:#292b2d;font:16px system-ui}header{padding:18px;background:#292b2d;color:#f5ead0;border-bottom:3px solid #b49a60}main{max-width:1180px;margin:auto;padding:20px}select,button{padding:10px;margin:5px;background:#fffdf6;border:1px solid #b9a77e;border-radius:8px}#grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}figure{margin:0;border:1px solid #b9a77e;border-radius:8px;padding:10px;text-align:center;background:#fffdf6}canvas{width:100%;max-width:256px;background:conic-gradient(#ecece6 25%,#fff 0 50%,#ecece6 0 75%,#fff 0);background-size:20px 20px}small{display:block}a{color:#8a682a}</style><header>Runevale V43 · ตัวละคร33 / คอสตูม10 / VFX156</header><main><select id="tab"><option value="bodies">ตัวละครและคอสตูม</option><option value="fx">สกิลและวงร่าย</option></select><select id="pick"></select><select id="action"><option value="walk">เดิน8เฟรม</option><option value="attack">โจมตี12เฟรม</option><option value="idle">ยืน</option><option value="start">เริ่มเดิน</option><option value="stop0">หยุดเดิน</option><option value="down">ตาย</option></select><button id="play">หยุด</button><button id="next">เฟรมถัดไป</button><p id="info"></p><a id="download" download>ดาวน์โหลดชีต WebP โปร่งใส</a><div id="grid"></div></main><script>const data=META43,cache={};let phase=0,playing=true,last=0;function selected(){return data[tab.value][pick.value]}function count(){let d=selected();return tab.value==='fx'?d.frameCount:d.frames.filter(f=>f.action===action.value&&f.direction==='S').length}function render(){grid.innerHTML=(tab.value==='fx'?['FX']:action.value==='down'?['S']:['S','N','W','E']).map(d=>'<figure>'+d+'<canvas width="256" height="288" data-dir="'+d+'"></canvas><small></small></figure>').join('');phase=0;const d=selected();action.hidden=tab.value==='fx';download.href=d.file;info.textContent=pick.value+' · '+count()+' เฟรม · ภาพโปร่งใส / ชีตแพ็กพร้อมจุดยึดในmanifest.json';if(!cache[d.file]){let im=new Image();im.src=d.file;cache[d.file]=im}}function options(){pick.innerHTML=Object.keys(data[tab.value]).map(id=>'<option value="'+id+'">'+(data[tab.value][id].name||id)+'</option>').join('');render()}function tick(t){let d=selected(),step=tab.value==='fx'?(d.duration||1)/d.frameCount:action.value==='walk'?.1:action.value==='attack'?.025:action.value==='start'?.03:.6;if(playing&&last)phase+=Math.min(.15,(t-last)/1000)/step;last=t;let k=Math.floor(phase)%count(),im=cache[d.file];for(let c of grid.querySelectorAll('canvas')){let g=c.getContext('2d');g.clearRect(0,0,256,288);g.imageSmoothingEnabled=false;if(im?.naturalWidth){if(tab.value==='bodies'){let f=d.frames.filter(f=>f.direction===c.dataset.dir&&f.action===action.value).sort((a,b)=>a.frame-b.frame)[k];if(f)g.drawImage(im,...f.rect,128-f.pivot[0]*1.6,260-f.pivot[1]*1.6,f.rect[2]*1.6,f.rect[3]*1.6)}else{let r=d.frameRects[k],a=d.anchor,s=224/d.frameSize;g.drawImage(im,r[0],r[1],r[2],r[3],128+(r[4]-a[0])*s,144+(r[5]-a[1])*s,r[2]*s,r[3]*s)}}c.nextElementSibling.textContent='เฟรม '+(k+1)+' / '+count()}requestAnimationFrame(tick)}tab.onchange=options;pick.onchange=action.onchange=render;play.onclick=()=>{playing=!playing;play.textContent=playing?'หยุด':'เล่น';last=0};next.onclick=()=>{playing=false;play.textContent='เล่น';phase=(Math.floor(phase)+1)%count()};options();requestAnimationFrame(tick);</script></html>''';(S/'Viewer.html').write_text(viewer.replace('META43',json.dumps(meta,ensure_ascii=False,separators=(',',':'))))
(S/'อ่านก่อนนำเข้า.txt').write_text('''Runevale Animation Sheets V43
เปิดViewer.htmlดูตัวละคร33แบบ คอสตูม10ชุด และสกิล/วงร่าย156แบบ
characters/ costumes/ fx/ เป็นชีตWebPแบบlosslessโปร่งใส
manifest.json ระบุกรอบภาพและจุดยึด เนื่องจากตัดพื้นที่โปร่งใสออกแล้วจึงไม่ใช้กริดช่องเท่ากัน
ตัวละคร: frames[].rect=[x,y,w,h], pivot=[x,y]ภายในกรอบ ใช้drawImageที่ตำแหน่งโลก-pivot
เดิน8เฟรมต่อทิศ โจมตี12 เริ่มเดิน3 หยุดเดิน3ต่อเฟรมก้าว ยืน1 ตาย2ทิศS
4ทิศS,N,W,E; ท่าตายS; จุดยึดเท้าเดิม ความเร็วรอบเดิน80worldpx
VFX: frameRects=[x,y,w,h,offsetX,offsetY]; frameSize/anchorอ้างอิงช่องต้นฉบับ
วาดที่ตำแหน่งโลก+(offset-anchor)*scale ขนาดw*scale,h*scale
frameCount29หรือ33; sourceFrameCount8หรือ9; subframes4
ภาพหลักเดิมอยู่ที่ดัชนี0,4,8,... สีและalphaที่มองเห็นตรงต้นฉบับ ระยะเวลาเดิม
เฟรมกลางสร้างล่วงหน้าจากภาพเต็มเฟรม ไม่มีระบบริกหรือโค้ดบิดขาในเกม
''')
for name in ['validation.json','pixel-validation.json','preservation.json']:shutil.copy2(E/name,S/name)
packages=[]
for root in [O,S]:
 path=R/'dist'/(root.name+'.zip')
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for f in sorted(root.rglob('*')):
   if f.is_file():z.write(f,root.name+'/'+str(f.relative_to(root)))
 with zipfile.ZipFile(path)as z:assert z.testzip()is None
 packages.append({'name':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(E/'packages.json').write_text(json.dumps(packages,indent=2));print(packages)
