from pathlib import Path
import json,hashlib
exec(Path('/workspace/RAG/tools/publish_recast_v47.py').read_text().split('z=D/')[0])
E=R/'evidence/city-v49';P=R/'tools/download-v49';P.mkdir(exist_ok=True);D=R/'dist';packages=json.loads((E/'packages.json').read_text());pack=packages[0];data=(D/pack['name']).read_bytes();assert hashlib.sha256(data).hexdigest()==pack['sha256'];assert json.loads((E/'validation.json').read_text())['htmlSha256']==json.loads((E/'build.json').read_text())['sha256'];files={};parts=[]
for i,start in enumerate(range(0,len(data),80*1024*1024)):
 p=D/('Runevale-V49.part'+str(i+1));p.write_bytes(data[start:start+80*1024*1024]);parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});files['downloads/V49/'+p.name]=p
art=D/packages[1]['name'];files[art.name]=art
for n in ['build.json','validation.json','packages.json']:files['releases/V49/'+n]=E/n
files['releases/V49/team-regression.json']=E/'team-regression/validation.json';files['releases/V49/README.txt']=R/'build/Runevale-Recast-V49/อ่านก่อนเล่น.txt'
for n in ['art_city_v49.py','build_city_v49.py','city-v49.js','test_city_v49.py','test_team_regression_v49.py','package_city_v49.py','publish_city_v49.py']:files['releases/V49/tools/'+n]=R/'tools'/n
c=push('runevale-game-download',files,'Publish V49 compact town, unique service NPCs, costume gacha, icons and resource materials')
for p in parts:p['url']='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V49/'+p['name']
(P/'config.json').write_text(json.dumps({**pack,'parts':parts}));old=(R/'tools/download-v48/index.html').read_text();script=old[old.index('<script>'):].replace('V48','V49');head=old[:old.index('<main>')].replace('V48','V49')
(P/'index.html').write_text(head+'''<main><small>RUNEVALE ONLINE · V49</small><h1>เมืองกระชับ คอสตูม และพื้นผิวใหม่</h1><ul><li>NPCสุ่มคอสตูม: 1ครั้ง100,000z / 10ครั้ง1,000,000z</li><li>ไอคอนใหม่10ชุด โอกาสชุดละ10% ชุดซ้ำรับ1โทเคน</li><li>เมือง80×80ช่อง NPC19จุดมีรูปลักษณ์เฉพาะและอยู่หน้าบ้าน</li><li>เดินเร็ว2เท่า แก้การเข้าประชิดและการดันมอนสเตอร์ชนกำแพง</li><li>วัตถุบังตัวละครจะโปร่งแสง พื้นผิว32แบบและทรัพยากรตกแต่ง6แบบ</li></ul><button id="get" disabled>กำลังเตรียมดาวน์โหลด…</button><p id="status" role="status"></p><p>แตกZIP แล้วเปิด <b>index.html</b><br>NPCออโรราอยู่หน้าบ้านหลังคาฟ้าฝั่งซ้ายล่างเมือง<br>เมนูแอดมิน <b>G → stefan-gm</b><br>เลือก “เมืองใหม่ / สุ่มคอสตูม / พื้นผิวและทรัพยากร V49”</p><img src="town-overview.jpg" width="640" height="640" style="max-width:100%;height:auto;border-radius:12px" alt="เมืองV49และNPCประจำบ้าน"><p><a class="secondary" href="https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/COMMIT49/ARTFILE49">ดาวน์โหลดไอคอน พื้นผิว และทรัพยากรPNGแยก</a></p><small>ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง · ทรัพยากรเป็นของตกแต่งฉาก ไม่มีระบบเก็บเกี่ยว</small></main>'''.replace('COMMIT49',c).replace('ARTFILE49',art.name)+script)
(P/'sw.js').write_text((R/'tools/download-v48/sw.js').read_text().replace('V48','V49'))
from PIL import Image
Image.open(E/'town-overview.png').convert('RGB').resize((640,640)).save(P/'town-overview.jpg',quality=87)
c2=push('gh-pages',{'v49/'+n:P/n for n in ['index.html','sw.js','config.json','town-overview.jpg']},'Publish V49 tested game, compact town preview and native pixel assets');print('PARTS',c,'PAGES',c2,flush=True)
(E/'publish.json').write_text(json.dumps({'partsCommit':c,'pagesCommit':c2,'page':'https://phuthanet9870-cpu.github.io/RAG/v49/'},indent=2))
