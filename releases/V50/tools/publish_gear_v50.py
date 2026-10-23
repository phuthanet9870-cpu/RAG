from pathlib import Path
import json,hashlib
exec(Path('/workspace/RAG/tools/publish_recast_v47.py').read_text().split('z=D/')[0])
E=R/'evidence/gear-v50';P=R/'tools/download-v50';P.mkdir(exist_ok=True);D=R/'dist';pack=json.loads((E/'packages.json').read_text())[0];data=(D/pack['name']).read_bytes();assert hashlib.sha256(data).hexdigest()==pack['sha256'];files={};parts=[]
for i,start in enumerate(range(0,len(data),80*1024*1024)):
 p=D/('Runevale-V50.part'+str(i+1));p.write_bytes(data[start:start+80*1024*1024]);parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});files['downloads/V50/'+p.name]=p
for n in ['build.json','validation.json','packages.json']:files['releases/V50/'+n]=E/n
files['releases/V50/combat-regression.json']=E/'combat-regression/validation.json';files['releases/V50/README.txt']=R/'build/Runevale-Recast-V50/อ่านก่อนเล่น.txt'
for n in ['gear-combat-v50.js','build_gear_v50.py','test_gear_v50.py','test_combat_regression_v50.py','package_gear_v50.py','publish_gear_v50.py']:files['releases/V50/tools/'+n]=R/'tools'/n
c=push('runevale-game-download',files,'Publish V50 independent fighter gear, persistent mercenary kits and underfilled arena modes')
for p in parts:p['url']='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V50/'+p['name']
(P/'config.json').write_text(json.dumps({**pack,'parts':parts}));old=(R/'tools/download-v48/index.html').read_text();script=old[old.index('<script>'):].replace('V48','V50');head=old[:old.index('<main>')].replace('V48','V50')
(P/'index.html').write_text(head+'''<main><small>RUNEVALE ONLINE · V50</small><h1>นักสู้ชุดสุ่ม และเข้าได้แม้ทีมไม่ครบ</h1><ul><li>เงานักสู้และทหารครบ21อาชีพมีอุปกรณ์สุ่มส่วนตัว ไม่คัดลอกชุดผู้เล่น</li><li>สเตตัสอิงเลเวลและงบแต้มผู้เล่น อุปกรณ์มีความหายาก ตีบวก และออปชัน</li><li>เงาเลือกเป้าหมายฮีลเลอร์ ผู้ร่าย และเป้าหมายอ่อนแอ ใช้สกิลจริง</li><li>ทุกโหมดเข้าได้ตั้งแต่0ทหาร ถึงเพดานทีม เช่นลงโหมด10v10คนเดียวสู้เงา10ตัวได้</li><li>ทหารบันทึกชุดเดิมหลังโหลดและเข้าประลอง มีหน้าดูสเตตัส/อุปกรณ์</li></ul><button id="get" disabled>กำลังเตรียมดาวน์โหลด…</button><p id="status" role="status"></p><p>แตกZIP แล้วเปิด <b>index.html</b><br>เลือก “ดูอุปกรณ์” ในหน้าทหารหรือหน้าเลือกทีม<br>เมนูแอดมิน <b>G → stefan-gm</b><br>“อุปกรณ์สุ่ม / สเตตัสนักสู้ / ทีมไม่ครบ V50” ใช้ตรวจและสุ่มชุดใหม่รายตัว</p><small>ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง · เมืองและคอสตูมจากV49</small></main>'''+script)
(P/'sw.js').write_text((R/'tools/download-v48/sw.js').read_text().replace('V48','V50'))
c2=push('gh-pages',{'v50/'+n:P/n for n in ['index.html','sw.js','config.json']},'Publish V50 tested game download page');(E/'publish.json').write_text(json.dumps({'partsCommit':c,'pagesCommit':c2,'page':'https://phuthanet9870-cpu.github.io/RAG/v50/'},indent=2));print('PARTS',c,'PAGES',c2,flush=True)
