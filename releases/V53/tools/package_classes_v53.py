from pathlib import Path
import json,hashlib,zipfile,html
R=Path('/workspace/RAG');E=R/'evidence/classes-v53';O=R/'build/Runevale-Recast-V53';A=R/'assets/classes-v53';v=json.loads((E/'validation.json').read_text());assert not v['browserErrors'];assert v['rankFactionCases']==600 and len(v['ownClassAI'])==24;assert not json.loads((E/'combat-regression/validation.json').read_text())['browserErrors'];sha=hashlib.sha256((O/'index.html').read_bytes()).hexdigest();assert sha==v['htmlSha256']==json.loads((E/'build.json').read_text())['htmlSha256']
# Materials, character sheets, costumes and previous FX stay byte-for-byte identical.
s=(O/'index.html').read_text();base=(R/'build/Runevale-Recast-V52/index.html').read_text();preserved=[]
for m in ['const WORLD33_MATERIALS=','const WORLD33_PLANS=','const WORLD33_PLACEMENTS=','window.SHEET_DATA=','window.COSTUME36_DATA=','window.MONSTER_DATA=']:
 def get(t):return json.JSONDecoder().raw_decode(t[t.index(m)+len(m):])[0]
 assert get(s)==get(base),m;preserved.append(m)
(E/'preservation.json').write_text(json.dumps({'base':52,'unchanged':preserved},indent=2))
guide=json.loads((E/'skill-guide.json').read_text());lines=['Runevale V53 — คู่มือ12คลาสขั้นสูง / 72สกิลต้นฉบับ','ทุกคลาสต้อง Base Lv.90 และ Job Lv.70 ของอาชีพก่อนหน้า','สกิลใหม่เป็นของคลาสนั้น สืบทอดสกิลพื้นฐานตามระบบสายเดิม','ค่าร่ายในคำอธิบายเป็นค่าก่อนโบนัสDEX/INT ส่วนท่าไม้ตายมีเวลาร่ายคงที่เพิ่ม0.15วิ','ดาเมจจริงผ่านเกราะ ธาตุ และการลดดาเมจPvPตามเกม','']
for c in guide:
 lines += [c['name']+' ['+c['id']+']',c['blurb']]
 for sk in c['skills']:
  lines += ['  '+sk['name']+' ('+sk['type']+')','  ก่อนเรียน: '+str(sk['requirements'])]+['  Lv.'+str(i+1)+': '+d for i,d in enumerate(sk['ranks'])]
 lines+=['']
(O/'คู่มือสกิลใหม่.txt').write_text('\n'.join(lines));(A/'คู่มือสกิลใหม่.txt').write_text('\n'.join(lines))
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale V53 — เปิดคลาสขั้นสูงครบ
แตกZIP แล้วเปิด index.html ภาพฝังครบในเกม
เพิ่ม12คลาสที่เคยล็อก รวมเล่นได้33คลาส
คลาสละ6สกิลต้นฉบับ: ติดตัว1 ใช้งาน5 รวม72สกิลใหม่ (รวมทั้งเกม218สกิล)
สกิลใหม่ทุกสกิลมีไอคอนและแอนิเมชัน12เฟรม
เปลี่ยนได้ที่NPCเปลี่ยนอาชีพในปราสาท เมื่อเป็นอาชีพก่อนหน้า Base90 / Job70
ดูแผนผังและเงื่อนไขสกิลจริงในหน้าทักษะ ดูคู่มือในหน้าเปลี่ยนอาชีพ
G > stefan-gm > คลาสเปิดใหม่V53 เพื่อทดลองเต็ม จ้างฟรี เสกเงา และดูVFXทีละเฟรม
ทหารรับจ้างและเงานักสู้ใช้สกิลของ12คลาสใหม่ได้จริง พร้อมอุปกรณ์สุ่มของตนเอง
คงพื้นผิวเดิมก่อนV49 ตามV52 ไม่ใส่Texture ResourceV49/V51กลับมา
ทดสอบสกิลใหม่600กรณี ครบ5ระดับทั้ง2ฝ่าย และAIใช้สกิลเฉพาะคลาส24กรณี
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่มือถือจริง
''')
d=json.loads((A/'design.json').read_text());preview='''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Runevale V53 Skill Atlas Preview</title><style>body{background:#ede7d7;color:#34302a;font:16px system-ui;max-width:1400px;margin:20px auto;padding:16px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}article{border:1px solid #bba777;background:#faf7ef;padding:10px;border-radius:12px}canvas{width:100%;image-rendering:pixelated;background:#2b3038;border-radius:8px}h2{margin-top:40px}</style><h1>V53 · 12คลาส / 72สกิล / 12เฟรม</h1><p>ภาพเคลื่อนไหวจากPNGชีตจริง แยกไฟล์พื้นหลังโปร่งใส เฟรมละ128×128 เรียง12เฟรมแนวนอน</p><main id="main"></main><script>const design='''+json.dumps(d,ensure_ascii=False)+''';const images={};for(const c of design.classes){let h=document.createElement('h2');h.textContent=c.name;main.append(h);let g=document.createElement('div');g.className='grid';main.append(g);for(const s of design.skills.filter(s=>s.cls===c.id)){let a=document.createElement('article'),name=document.createElement('b'),cv=document.createElement('canvas');name.textContent=s.name;cv.width=cv.height=128;cv.dataset.id=s.id;a.append(name,cv);g.append(a);let im=images[s.id]=new Image;im.src=s.id+'.png';}}function tick(t){let f=Math.floor(t/80)%12;for(let cv of document.querySelectorAll('canvas')){let im=images[cv.dataset.id];if(im?.naturalWidth){let g=cv.getContext('2d');g.clearRect(0,0,128,128);g.drawImage(im,f*128,0,128,128,0,0,128,128);}}requestAnimationFrame(tick)}requestAnimationFrame(tick)</script></html>'''
(A/'preview.html').write_text(preview);(A/'manifest.json').write_text(json.dumps({'version':53,'classes':12,'skills':72,'framesPerSkill':12,'frameSize':[128,128],'atlasSize':[1536,128],'transparent':True,'runtimeRendering':'baked PNG frames; no runtime shape drawing','originalDesign':True},indent=2))
packs=[]
for name,root in [('Runevale-Recast-V53.zip',O),('Runevale-Classes-Skills-V53.zip',A)]:
 p=R/'dist'/name
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for f in root.iterdir():
   if f.is_file()and f.name!='vfx.json':z.write(f,str(f.relative_to(root.parent)))
 with zipfile.ZipFile(p)as z:
  assert z.testzip()is None
  if root==O:assert hashlib.sha256(z.read(O.name+'/index.html')).hexdigest()==sha
 packs.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(E/'packages.json').write_text(json.dumps(packs,indent=2));print(packs,flush=True)
