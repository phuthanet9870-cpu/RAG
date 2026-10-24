from pathlib import Path
import json,hashlib
exec(Path('/workspace/RAG/tools/publish_recast_v47.py').read_text().split('z=D/')[0])
E=R/'evidence/npcs-v55';P=R/'tools/download-v55';P.mkdir(exist_ok=True);D=R/'dist';packs=json.loads((E/'packages.json').read_text());pack=packs[0];data=(D/pack['name']).read_bytes();assert hashlib.sha256(data).hexdigest()==pack['sha256'];files={};parts=[]
for i,start in enumerate(range(0,len(data),80*1024*1024)):
 p=D/('Runevale-V55.part'+str(i+1));p.write_bytes(data[start:start+80*1024*1024]);parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});files['downloads/V55/'+p.name]=p
files['downloads/V55/'+packs[1]['name']]=D/packs[1]['name']
for n in ['build.json','validation.json','preservation.json','packages.json']:files['releases/V55/'+n]=E/n
files['releases/V55/README.txt']=R/'build/Runevale-Recast-V55/อ่านก่อนเล่น.txt';files['releases/V55/art-audit.json']=R/'assets/npcs-v55/audit.json';files['releases/V55/manifest.json']=R/'assets/npcs-v55/manifest.json'
for n in ['normalize_npcs_v55.py','npcs-v55.js','build_npcs_v55.py','test_npcs_v55.py','package_npcs_v55.py','publish_npcs_v55.py']:files['releases/V55/tools/'+n]=R/'tools'/n
c=push('runevale-game-download',files,'Publish V55 all20 service NPC roles as static front-facing pixel sprites at30 locations')
for p in parts:p['url']='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V55/'+p['name']
(P/'config.json').write_text(json.dumps({**pack,'parts':parts}));old=(R/'tools/download-v54/index.html').read_text();script=old[old.index('<script>'):].replace('V54','V55');head=old[:old.index('<main>')].replace('V54','V55');art='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V55/'+packs[1]['name']
(P/'index.html').write_text(head+'''<main><small>RUNEVALE ONLINE · V55</small><h1>NPCใหม่ · ยืนหันหน้าตรง</h1><img src="preview.jpg" alt="NPCใหม่ครบ20บทบาท" style="width:100%;border-radius:12px"><ul><li>ออกแบบ20บทบาทให้ตรงชื่อและหน้าที่ รวม30จุดในเมืองหลัก คาราวาน และปราสาท</li><li>Pixel art2Dสีสดใส หัวสมส่วน ภาพโปร่งใส ยืนด้านหน้าเพียง1เฟรม</li><li>ไม่หมุนตามผู้เล่น ไม่เดิน ไม่โจมตี และไม่มีเอฟเฟกต์บนตัว</li><li>คงตำแหน่งNPC บริการ เมือง และระบบอื่นจากV54</li><li>G → stefan-gm → NPCใหม่V55 ดูภาพ ไปจุดบริการ หรือวางตัวอย่างได้</li></ul><button id="get" disabled>กำลังเตรียมดาวน์โหลด…</button><p id="status" role="status"></p><p>แตกZIP แล้วเปิด <b>index.html</b></p><p><a href="'''+art+'''">ดาวน์โหลดPNGแยก20ตัว ชีตรวม ภาพต้นฉบับ และหน้าPreview</a></p><small>ตรวจครบ30จุดและ20เมนูบริการ · ภาพคงเดิมทุกมุมและเวลา · Chromiumและขนาดจอมือถือจำลอง</small></main>'''+script)
(P/'sw.js').write_text((R/'tools/download-v54/sw.js').read_text().replace('V54','V55'))
from PIL import Image
im=Image.open(R/'assets/npcs-v55/review.jpg');im.thumbnail((960,800));im.save(P/'preview.jpg',quality=92)
c2=push('gh-pages',{'v55/'+n:P/n for n in ['index.html','sw.js','config.json','preview.jpg']},'Publish V55 front-facing NPC sprites and playable game download page');(E/'publish.json').write_text(json.dumps({'partsCommit':c,'pagesCommit':c2,'page':'https://phuthanet9870-cpu.github.io/RAG/v55/'},indent=2));print('PARTS',c,'PAGES',c2,flush=True)
