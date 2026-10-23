from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path('/workspace/RAG');E=R/'evidence/city-v49';O=R/'build/Runevale-Recast-V49';A=R/'assets/city-v49'
v=json.loads((E/'validation.json').read_text());assert not v['browserErrors'];assert not json.loads((E/'team-regression/validation.json').read_text())['browserErrors'];assert v['htmlSha256']==hashlib.sha256((O/'index.html').read_bytes()).hexdigest()
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale Online V49 — เมือง / คอสตูม / ทรัพยากร
แตกZIP แล้วเปิด index.html ทุกภาพฝังในไฟล์เกม
เมืองหลัก80×80ช่อง จากเดิม96×96 พร้อมปราสาทใหญ่และน้ำพุกลางเมือง
NPCในเมือง19จุด มีชื่อและรูปลักษณ์ต่างกัน อยู่หน้าบ้านแต่ละหลัง
ออโรรา สุ่มคอสตูม อยู่หน้าบ้านหลังคาฟ้าฝั่งซ้ายล่างเมือง
สุ่ม1ครั้ง100,000z / 10ครั้ง1,000,000z ทุกชุด10% สุ่มซ้ำได้ ชุดซ้ำรับ1โทเคน
คอสตูม10ชุดมีไอคอนใหม่ สวมได้ทุกอาชีพโดยไม่เปลี่ยนค่าสเตตัส
เดินพื้นฐาน5ช่อง/วินาที เร็วเป็น2เท่าจากเดิม2.5ช่อง/วินาที บัฟและGMยังมีผล
แก้การเข้าประชิด: หยุดที่ระยะโจมตี ระยะมีช่วงเผื่อ ไม่เดินเข้ากลางมอนสเตอร์
การดันแยกมอนสเตอร์ตรวจสิ่งกีดขวาง จึงไม่ดันทะลุแล้วกระโดดกลับ
วัตถุสูงที่บังตัวละครจะแสดงทึบ28% กลับทึบปกติเมื่อเดินพ้น
พื้นผิวใหม่32แบบ ใช้ตามธีมแมพ และวัตถุทรัพยากรตกแต่ง6แบบ (ไม่มีระบบเก็บเกี่ยว)
ไฟล์PNGแยกอยู่ในแพ็กRunevale-City-Assets-V49.zip
G > stefan-gm > เมืองใหม่ / สุ่มคอสตูม / พื้นผิวและทรัพยากร V49
GMไปหาNPC เปิดสุ่ม มอบคอสตูม เปิด/ปิดการโปร่งแสง และวางทรัพยากรได้
คงตัวละคร คอสตูม แอนิเมชันสกิล และทีมประลองจากV48
ตรวจ76มอนสเตอร์/บอส การหยุดเข้าตี การชนกำแพง และระบบสกิล42ชุดอาชีพ/ทีม
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่มือถือจริง
''')
# Keep the separately reusable native art small and complete.
artZip=R/'dist/Runevale-City-Assets-V49.zip'
with zipfile.ZipFile(artZip,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(A.iterdir()):
  if p.suffix=='.png':z.write(p,'Runevale-City-Assets-V49/'+p.name)
 z.writestr('Runevale-City-Assets-V49/README.txt','V49 original pixel assets: 10 costume icons128x128; 32 terrain materials64x64; 6 transparent resource sprites64x64. Native PNG files. All are embedded in index.html. Resource sprites are decorative, not harvestable. Costume IDs match the wardrobe. Material indices match WORLD33_MATERIALS.\n')
packages=[]
zpath=R/'dist/Runevale-Recast-V49.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(O.iterdir()):
  if p.is_file():z.write(p,str(p.relative_to(O.parent)))
for zp in [zpath,artZip]:
 with zipfile.ZipFile(zp)as z:
  assert z.testzip()is None
  if zp==zpath:assert hashlib.sha256(z.read(O.name+'/index.html')).hexdigest()==v['htmlSha256']
 row={'name':zp.name,'bytes':zp.stat().st_size,'sha256':hashlib.sha256(zp.read_bytes()).hexdigest()};packages.append(row);print(row,flush=True)
(E/'packages.json').write_text(json.dumps(packages,indent=2))
