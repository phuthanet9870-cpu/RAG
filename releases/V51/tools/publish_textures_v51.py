from pathlib import Path
import json,hashlib
exec(Path('/workspace/RAG/tools/publish_recast_v47.py').read_text().split('z=D/')[0])
E=R/'evidence/textures-v51';P=R/'tools/download-v51';P.mkdir(exist_ok=True);D=R/'dist';packs=json.loads((E/'packages.json').read_text());pack=packs[0];data=(D/pack['name']).read_bytes();assert hashlib.sha256(data).hexdigest()==pack['sha256'];files={};parts=[]
for i,start in enumerate(range(0,len(data),80*1024*1024)):
 p=D/('Runevale-V51.part'+str(i+1));p.write_bytes(data[start:start+80*1024*1024]);parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});files['downloads/V51/'+p.name]=p
files['downloads/V51/'+packs[1]['name']]=D/packs[1]['name']
for n in ['build.json','validation.json','art-validation.json','packages.json']:files['releases/V51/'+n]=E/n
files['releases/V51/README.txt']=R/'build/Runevale-Recast-V51/อ่านก่อนเล่น.txt'
for n in ['art_textures_v51.py','build_textures_v51.py','test_textures_v51.py','test_city_regression_v51.py','package_textures_v51.py','publish_textures_v51.py']:files['releases/V51/tools/'+n]=R/'tools'/n
c=push('runevale-game-download',files,'Publish V51 original fantasy terrain textures and transparent resource art')
for p in parts:p['url']='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V51/'+p['name']
(P/'config.json').write_text(json.dumps({**pack,'parts':parts}));old=(R/'tools/download-v50/index.html').read_text();script=old[old.index('<script>'):].replace('V50','V51');head=old[:old.index('<main>')].replace('V50','V51');art='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V51/'+packs[1]['name']
(P/'index.html').write_text(head+'''<main><small>RUNEVALE ONLINE · V51</small><h1>Texture Resource ใหม่</h1><p>งานภาพต้นฉบับแนวแฟนตาซี MMORPG ได้แรงบันดาลใจจาก Ragnarok Classic</p><img src="preview.jpg" alt="ตัวอย่างพื้นผิวและทรัพยากรใหม่" style="width:100%;border-radius:12px"><ul><li>พื้นผิวใหม่32แบบ แยกตามธีมเมือง ป่า ภูเขา ทะเล ทะเลทราย น้ำแข็ง สุสาน และภูเขาไฟ</li><li>ทรัพยากรโปร่งใส6แบบ: แร่เหล็ก แร่ทอง ผลึก สมุนไพร ไม้ และเปลือกหอย</li><li>ติดตั้งในเกมแล้ว คงผังเมือง ตัวละคร สกิล และระบบทหาร/เงาจากV50</li><li>เปิด G → stefan-gm → Texture Resource V51 เพื่อดูภาพและเสกทรัพยากรตกแต่ง</li></ul><button id="get" disabled>กำลังเตรียมดาวน์โหลด…</button><p id="status" role="status"></p><p>แตกZIP แล้วเปิด <b>index.html</b></p><p><a href="'''+art+'''">ดาวน์โหลดชุดภาพ PNG แยก</a></p><small>ทดสอบChromiumและขนาดจอมือถือจำลอง · ภาพทรัพยากรเป็นของตกแต่ง ไม่ใช่ระบบเก็บเกี่ยว</small></main>'''+script)
(P/'sw.js').write_text((R/'tools/download-v50/sw.js').read_text().replace('V50','V51'))
from PIL import Image
im=Image.open(R/'assets/textures-v51/review.jpg');im.thumbnail((768,1344));im.save(P/'preview.jpg',quality=85)
c2=push('gh-pages',{'v51/'+n:P/n for n in ['index.html','sw.js','config.json','preview.jpg']},'Publish V51 terrain and resource art download page');(E/'publish.json').write_text(json.dumps({'partsCommit':c,'pagesCommit':c2,'page':'https://phuthanet9870-cpu.github.io/RAG/v51/'},indent=2));print('PARTS',c,'PAGES',c2,flush=True)
