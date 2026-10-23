from pathlib import Path
import zipfile,hashlib,json
R=Path('/workspace/RAG');E=R/'evidence/restore-v52';O=R/'build/Runevale-Recast-V52';v=json.loads((E/'validation.json').read_text());restore=json.loads((E/'restoration.json').read_text());assert not v['browserErrors']and not restore['browserErrors'];assert v['htmlSha256']==restore['htmlSha256']==hashlib.sha256((O/'index.html').read_bytes()).hexdigest()
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale V52 — คืนพื้นผิวเดิม
แตกZIP แล้วเปิด index.html ภาพทั้งหมดฝังในเกม
ถอดชุดTexture ResourceของV49และV51ออก
คืนชุดพื้นผิวเดิมจากV48 ไม่ได้เอาพื้นผิวทั้งหมดออกจนแมพว่าง
ถอดวัตถุทรัพยากรตกแต่ง6แบบและเมนูเสกของชุดดังกล่าว
คงผังเมือง NPC คอสตูม ระบบเดิน สกิล อุปกรณ์สุ่มของเงา/ทหาร และเข้าได้ทุกโหมดแม้ทีมไม่ครบ
GM: G > stefan-gm
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง
''')
p=R/'dist/Runevale-Recast-V52.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in O.iterdir():
  if f.is_file():z.write(f,str(f.relative_to(O.parent)))
with zipfile.ZipFile(p)as z:
 assert z.testzip()is None;assert hashlib.sha256(z.read(O.name+'/index.html')).hexdigest()==v['htmlSha256']
r={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(E/'packages.json').write_text(json.dumps([r],indent=2));print(r,flush=True)
