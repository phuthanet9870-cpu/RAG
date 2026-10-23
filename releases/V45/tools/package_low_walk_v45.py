from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path('/workspace/RAG');O=R/'build/Runevale-Low-Walk-V45';E=R/'evidence/low-walk-v45';v=json.loads((E/'runtime/validation.json').read_text());sha=hashlib.sha256((O/'index.html').read_bytes()).hexdigest();assert sha==v['sha256']==json.loads((E/'build.json').read_text())['sha256'];assert v['classCostumeCombinations']==330 and not v['browserErrors']
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale Online V45 — ลดท่ายกเข่าสูง
แตก ZIP แล้วเปิด index.html ภาพทั้งหมดฝังในไฟล์เกม
แก้คอสตูมทั้ง10ชุด ครบ4ทิศ ให้ยกเท้าใกล้พื้น ก้าวสั้น และสลับขาซ้ายขวา
เดิน8เฟรมต่อทิศ จุดยึดเท้าคงที่ พร้อมแก้เฟรมเริ่มเดินและหยุดเดิน
หน้าตา เสื้อผ้า ท่ายืนและท่าโจมตีเดิมยังคงอยู่
เกมใช้ภาพเต็มเฟรมจากชีต ไม่มีระบบบิดขาขณะเล่น
คงเอฟเฟกต์นุ่มนวลและการแก้มอนสเตอร์ติดฉากจากV44
GM: กด G → stefan-gm → ตรวจเดิน / โจมตี / VFX ทุกเฟรมV45
ทดสอบChromium เดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่มือถือจริง
''')
for n in ['build.json','pixel-validation.json','preservation.json']:shutil.copy(E/n,O/n)
shutil.copy(E/'runtime/validation.json',O/'runtime-validation.json');p=R/'dist/Runevale-Low-Walk-V45.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in sorted(O.iterdir()):
  if f.is_file():z.write(f,O.name+'/'+f.name)
with zipfile.ZipFile(p)as z:assert z.testzip()is None
r={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(E/'package.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
