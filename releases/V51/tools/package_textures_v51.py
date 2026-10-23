from pathlib import Path
import zipfile,json,hashlib
R=Path('/workspace/RAG');E=R/'evidence/textures-v51';O=R/'build/Runevale-Recast-V51';v=json.loads((E/'art-validation.json').read_text());assert not v['browserErrors'];assert not json.loads((E/'validation.json').read_text())['browserErrors'];sha=hashlib.sha256((O/'index.html').read_bytes()).hexdigest();assert sha==json.loads((E/'build.json').read_text())['htmlSha256']
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale V51 — Texture Resource ใหม่
แตก ZIP แล้วเปิด index.html ภาพทั้งหมดฝังในเกมแล้ว ไม่ต้องโหลดภาพจากเว็บ
พื้นผิว32แบบ: หินปูเมือง ทุ่งหญ้า ป่ามอส ภูเขา ทราย น้ำแข็ง สุสาน ลาวา น้ำ และบึงพิษ
ภาพทรัพยากรใหม่6แบบ: สายแร่เหล็ก สายแร่ทอง ผลึกเวท สมุนไพร ไม้ท่อน และเปลือกหอย
งานภาพต้นฉบับแนวแฟนตาซี MMORPG pixel art ได้แรงบันดาลใจจากบรรยากาศ Ragnarok Classic
ไม่ได้ใช้ภาพที่ดึงจากเกม Ragnarok โดยตรง
ทรัพยากรเหล่านี้ใช้ตกแต่งฉาก ยังไม่ได้เพิ่มระบบเก็บเกี่ยว
G > stefan-gm > Texture Resource V51 เพื่อดูภาพและวางทรัพยากรใกล้ตัว
คงผังเมือง ตำแหน่ง NPC การเดิน คอสตูม สกิล และระบบทหาร/เงานักสู้จากV50
ทดสอบทุก31แผนที่ ตรวจภาพโปร่งใสและขอบพื้นผิว ตรวจGMเสกครบ6แบบ
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่โทรศัพท์จริง
''')
packs=[]
for name,root in [('Runevale-Recast-V51.zip',O),('Runevale-Texture-Resource-V51.zip',R/'assets/textures-v51')]:
 p=R/'dist'/name
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for f in root.iterdir():
   if f.is_file():z.write(f,str(f.relative_to(root.parent)))
 with zipfile.ZipFile(p)as z:
  assert z.testzip()is None
  if root==O:assert hashlib.sha256(z.read(O.name+'/index.html')).hexdigest()==sha
 packs.append({'name':name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(E/'packages.json').write_text(json.dumps(packs,indent=2));print(packs,flush=True)
