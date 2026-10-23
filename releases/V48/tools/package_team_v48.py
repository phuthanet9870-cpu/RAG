from pathlib import Path
import json,hashlib,zipfile
R=Path('/workspace/RAG');O=R/'build/Runevale-Recast-V48';E=R/'evidence/team-v48'
assert not json.loads((E/'validation.json').read_text())['browserErrors']
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale Online V48 — ทีม / ทหารรับจ้าง / ประลอง
แตก ZIP ก่อน แล้วเปิด index.html ทุกภาพฝังในไฟล์เกม
เข้าเกม > NPC ทหารรับจ้าง: จ้างได้ทุก21อาชีพ สูงสุด10คนในรายชื่อ
ปาร์ตี้ในสนามรวมผู้เล่นสูงสุด10คน = ผู้เล่น1 + ทหาร9 อีกคนเป็นสำรอง
กดสลับเข้าทีมเพื่อเปลี่ยนตัวสำรอง
NPC ลานประลอง > เลือก1vs1 / 3vs3 / 5vs5 / 10vs10 > เลือกทหารก่อนเริ่ม
จำนวนทีมรวมผู้เล่น เช่น3vs3ใช้ผู้เล่น1+ทหาร2 ฝ่ายตรงข้ามเป็นทีมเงานักสู้
ทั้งสองฝ่ายใช้ตัวดำเนินสกิลจริงของเกม มีSP คูลดาวน์ ร่าย ฮีล บัฟและชุบชีวิตแยกฝ่าย
เลเวลและงบสเตตัสเท่าผู้เล่น จัดค่าสเตตัสตามอาชีพและอุปกรณ์ระดับเดียวกัน
เพื่อนล้มไม่จบทันที ต้องแพ้ทั้งทีม ไม่มีฟื้นอัตโนมัติในประลอง จำกัด5นาที
ชนะ +25คะแนน +2โทเคน แพ้หรือยอมแพ้ −15 ออกจากรอบคืนปาร์ตี้เดิม
G > stefan-gm > ทีม10คน / ทหารทุกคลาส / เงานักสู้ / ประลอง V48
GMจ้างฟรี เสกเงาทุกคลาส ฟื้นฟูทีม และเปิดหน้าเลือกโหมด
คงภาพตัวละคร แผนที่และVFXจากV47
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง390/844 ไม่ใช่การทดสอบมือถือจริง
''')
z=R/'dist/Runevale-Recast-V48.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as f:
 for p in O.iterdir():f.write(p,str(p.relative_to(O.parent)))
with zipfile.ZipFile(z)as f:
 assert f.testzip()is None
 assert hashlib.sha256(f.read(O.name+'/index.html')).hexdigest()==json.loads((E/'build.json').read_text())['sha256']
report={'name':z.name,'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'crcVerified':True,'htmlMatchesTestedBuild':True};(E/'package.json').write_text(json.dumps(report,indent=2));print(report,flush=True)
