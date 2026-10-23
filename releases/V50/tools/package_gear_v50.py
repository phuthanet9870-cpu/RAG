from pathlib import Path
import json,hashlib,zipfile
R=Path('/workspace/RAG');E=R/'evidence/gear-v50';O=R/'build/Runevale-Recast-V50';v=json.loads((E/'validation.json').read_text());assert not v['browserErrors'];assert not json.loads((E/'combat-regression/validation.json').read_text())['browserErrors'];assert hashlib.sha256((O/'index.html').read_bytes()).hexdigest()==v['htmlSha256']
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale V50 — เงานักสู้และอุปกรณ์สุ่ม
แตกZIP เปิด index.html ภาพทั้งหมดอยู่ในไฟล์เกม
เงานักสู้และทหารมีชุดอุปกรณ์สุ่มส่วนตัว: อาวุธ เกราะ หมวก ผ้าคลุม รองเท้า ถุงมือ กางเกง และเครื่องประดับ
สุ่มประเภทที่ใช้ได้ตามอาชีพ ระดับตามเลเวล มีความหายาก ตีบวก และออปชัน
เลเวลและงบแต้มสเตตัสอิงผู้เล่น แต่จัดสรรแต้มตามสายอาชีพและรูปแบบเฉพาะตัว
ไม่ได้คัดลอกชุดผู้เล่น เงาแต่ละตัวสุ่มใหม่เมื่อเกิด
ทหารที่จ้างแล้วบันทึกชุดเดิมเมื่อโหลดเกมหรือเข้าประลอง ปรับชุดตามเลเวลที่เปลี่ยน
เงาเลือกเป้าหมายจากระยะ HP ผู้ร่ายและฮีลเลอร์ พร้อมเคารพการยั่วยุ ใช้สกิลอาชีพจริง
ลานประลองเข้าได้แม้ไม่เลือกทหารเลย ฝ่ายเงายังคงครบตามโหมด:
1v1: ผู้เล่น1 ไม่มีทหาร
3v3: ผู้เล่น1 + ทหาร0ถึง2
5v5: ผู้เล่น1 + ทหาร0ถึง4
10v10: ผู้เล่น1 + ทหาร0ถึง9
รายชื่อจ้างยังสูงสุด10คน มีสำรอง ปาร์ตี้สนามรวมผู้เล่นสูงสุด10คน
ดูอุปกรณ์และสเตตัสทหารได้จากหน้าจ้างหรือหน้าเลือกทีม
G > stefan-gm > อุปกรณ์สุ่ม / สเตตัสนักสู้ / ทีมไม่ครบ V50
GMตรวจทหารและเงาทุกตัวในสนาม และสุ่มชุดใหม่ให้ตัวที่เลือกได้
คงเมือง คอสตูม แผนที่ พื้นผิว และการเดิน V49
ทดสอบครบ21อาชีพ ชุดไม่ซ้ำ20ครั้ง เซฟและโหลดชุด โหมดทีมไม่ครบ และสกิล42ชุดฝ่าย/อาชีพ
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่มือถือจริง
''')
p=R/'dist/Runevale-Recast-V50.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in O.iterdir():
  if f.is_file():z.write(f,str(f.relative_to(O.parent)))
with zipfile.ZipFile(p)as z:
 assert z.testzip()is None
 assert hashlib.sha256(z.read(O.name+'/index.html')).hexdigest()==v['htmlSha256']
r={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(E/'packages.json').write_text(json.dumps([r],indent=2));print(r,flush=True)
