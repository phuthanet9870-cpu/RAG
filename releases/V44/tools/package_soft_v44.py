from pathlib import Path
import zipfile,json,hashlib,shutil
R=Path('/workspace/RAG');O=R/'build/Runevale-Soft-VFX-Combat-V44';E=R/'evidence/soft-vfx-v44';v=json.loads((E/'validation.json').read_text());full=json.loads((E/'full-runtime/validation.json').read_text());assert not v['errors']and not full['browserErrors'];assert full['sha256']==json.loads((E/'build.json').read_text())['sha256'];assert full['activeSkillsExecuted']==105 and full['vfxMainSceneCoverage']==156
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale Online V44 — เอฟเฟกต์นุ่มนวล / เดินเข้าตีไม่ติดฉาก
แตก ZIP แล้วเปิด index.html ภาพทั้งหมดฝังอยู่ในไฟล์เกม

เอฟเฟกต์สกิลทุกชุดเชื่อมภาพต่อเนื่องระหว่างเฟรม และปรับขอบภาพเวลาแสดงผล
คงสี ความเข้ม ระยะเวลาสกิล และดาเมจเดิม ไม่มีการลดความทึบทั้งเอฟเฟกต์
แก้การเดินเลยจุดเลี้ยวจนวนอยู่กับที่
มอนสเตอร์เดินหลบสิ่งกีดขวางและไม่ถูกผลักทะลุเข้าไปในวัตถุ
ตัวที่ติดในวัตถุจะกลับสู่พื้นที่เดินได้
ตัวละครไม่แสดงท่าเดินเมื่อขยับไม่ได้ และไม่โจมตีทะลุสิ่งกีดขวาง

GM: กด G → stefan-gm
ตัวละคร/คอสตูม/ปีก/เมือง/ไอเทม/แผนที่คงจาก V43
ทดสอบด้วย Chromium ทั้งเดสก์ท็อปและขนาดจอมือถือจำลอง (ไม่ใช่มือถือจริง)
''')
for src,name in [(E/'validation.json','validation.json'),(E/'full-runtime/validation.json','runtime-validation.json'),(E/'build.json','build.json')]:shutil.copy(src,O/name)
p=R/'dist/Runevale-Soft-VFX-Combat-V44.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in sorted(O.iterdir()):
  if f.is_file():z.write(f,O.name+'/'+f.name)
with zipfile.ZipFile(p)as z:assert z.testzip()is None
r={'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(E/'package.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
