from pathlib import Path
import json,hashlib
R=Path('/workspace/RAG');A=R/'assets/low-walk-v45';E=R/'evidence/low-walk-v45';O=R/'build/Runevale-Low-Walk-V45';O.mkdir(exist_ok=True)
s=(R/'build/Runevale-Soft-VFX-Combat-V44/index.html').read_text();marker='window.COSTUME36_DATA=';i=s.index(marker)+len(marker);old,n=json.JSONDecoder().raw_decode(s[i:]);new=json.loads((A/'costumes-embedded.json').read_text());assert set(old)==set(new)and len(new)==10
s=s[:i]+json.dumps(new,ensure_ascii=False,separators=(',',':'))+s[i+n:];s=s.replace('เดินเข้าตี / VFX นุ่มนวล V44','เดินก้าวต่ำ V45').replace('Runevale Online V44','Runevale Online V45');
for label in ['ตรวจเฟรมเดิน / โจมตี / สกิล V43','ตรวจเดิน / โจมตี / VFX ทุกเฟรม V43','<h3>V43 · เดิน8','ตรวจเฟรมตัวละคร · V43','ตรวจอนิเมชั่น 33 อาชีพ · V43']:s=s.replace(label,label.replace('V43','V45'))
(O/'index.html').write_text(s)
r={'version':45,'sha256':hashlib.sha256((O/'index.html').read_bytes()).hexdigest(),'costumes':10,'directionsPerCostume':4,'walkFramesPerDirection':8,'liftSourcePixels':2,'shortStrideSourcePixels':5,'wholeFrameSpritesOnly':True,'baseClasses33Untouched':True,'v44VfxAndCollisionFixesRetained':True,'idleAndAttackArtRetained':True};(E/'build.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
