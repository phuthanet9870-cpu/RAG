from pathlib import Path
import json,hashlib
exec(Path('/workspace/RAG/tools/publish_recast_v47.py').read_text().split('z=D/')[0])
E=R/'evidence/effects-v54';P=R/'tools/download-v54';P.mkdir(exist_ok=True);D=R/'dist';packs=json.loads((E/'packages.json').read_text());pack=packs[0];data=(D/pack['name']).read_bytes();assert hashlib.sha256(data).hexdigest()==pack['sha256'];files={};parts=[]
for i,start in enumerate(range(0,len(data),80*1024*1024)):
 p=D/('Runevale-V54.part'+str(i+1));p.write_bytes(data[start:start+80*1024*1024]);parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});files['downloads/V54/'+p.name]=p
files['downloads/V54/'+packs[1]['name']]=D/packs[1]['name']
for n in ['build.json','validation.json','preservation.json','packages.json']:files['releases/V54/'+n]=E/n
files['releases/V54/README.txt']=R/'build/Runevale-Recast-V54/อ่านก่อนเล่น.txt';files['releases/V54/art-audit.json']=R/'assets/effects-v54/audit.json';files['releases/V54/skill-map.json']=R/'assets/effects-v54/skill-map.json'
for n in ['normalize_effects_v54.py','build_effects_v54.py','test_effects_v54.py','package_effects_v54.py','publish_effects_v54.py']:files['releases/V54/tools/'+n]=R/'tools'/n
c=push('runevale-game-download',files,'Publish V54 classic painted sprite-sheet effects for all72 advanced class skills')
for p in parts:p['url']='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V54/'+p['name']
(P/'config.json').write_text(json.dumps({**pack,'parts':parts}));old=(R/'tools/download-v53/index.html').read_text();script=old[old.index('<script>'):].replace('V53','V54');head=old[:old.index('<main>')].replace('V53','V54');art='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V54/'+packs[1]['name']
(P/'index.html').write_text(head+'''<main><small>RUNEVALE ONLINE · V54</small><h1>Sprite Sheet เอฟเฟกต์สกิลเข้าชุดเดิม</h1><p>ภาพแสงเงา ประกาย ควัน และพลังเวทวาดใหม่ สำหรับ72สกิลของ12คลาสขั้นสูง</p><img src="preview.jpg" alt="ตัวอย่างSprite Sheet เอฟเฟกต์ใหม่" style="width:100%;border-radius:12px"><ul><li>27รูปแบบพลัง ใช้ร่วมกันเมื่อความสามารถเป็นชนิดเดียวกัน</li><li>8เฟรมวาดจริงต่อชีต ขนาดเฟรม128×128 PNGโปร่งใส ไม่มีเฟรมคั่นจากการบิดภาพ</li><li>แทนภาพเอฟเฟกต์V53แล้ว ความสามารถ ดาเมจ SP และคูลดาวน์เดิม</li><li>คงคลาส33อาชีพ สกิล218สกิล เมือง และพื้นผิวเดิมของV52</li><li>G → stefan-gm → Sprite Sheet เอฟเฟกต์ใหม่V54 เพื่อดูทั้งชีตและตรวจทีละเฟรม</li></ul><button id="get" disabled>กำลังเตรียมดาวน์โหลด…</button><p id="status" role="status"></p><p>แตกZIP แล้วเปิด <b>index.html</b></p><p><a href="'''+art+'''">ดาวน์โหลดSprite Sheet PNGแยก72สกิล พร้อมหน้าPreview</a></p><small>ทดสอบสกิลใช้งาน600กรณี ทั้ง5ระดับและ2ฝ่าย · Chromiumและขนาดจอมือถือจำลอง</small></main>'''+script)
(P/'sw.js').write_text((R/'tools/download-v53/sw.js').read_text().replace('V53','V54'))
from PIL import Image
im=Image.open(R/'assets/effects-v54/overview.jpg');im.thumbnail((768,2000));im.save(P/'preview.jpg',quality=87)
c2=push('gh-pages',{'v54/'+n:P/n for n in ['index.html','sw.js','config.json','preview.jpg']},'Publish V54 native effect sheets and playable game download page');(E/'publish.json').write_text(json.dumps({'partsCommit':c,'pagesCommit':c2,'page':'https://phuthanet9870-cpu.github.io/RAG/v54/'},indent=2));print('PARTS',c,'PAGES',c2,flush=True)
