from pathlib import Path
import json,hashlib
exec((Path('/workspace/RAG/tools/publish_recast_v47.py')).read_text().split('z=D/')[0])
P=R/'tools/download-v48';P.mkdir(exist_ok=True);E=R/'evidence/team-v48';D=R/'dist'
old=(R/'tools/download-v47/index.html').read_text();script=old[old.index('<script>'):].replace('V47','V48')
head=old[:old.index('<main>')].replace('V47','V48')
(P/'index.html').write_text(head+'''<main><small>RUNEVALE ONLINE · V48</small><h1>ทีม10คนและสังเวียนประลอง</h1><ul><li>โหมด1v1 / 3v3 / 5v5 / 10v10 เลือกทหารก่อนเริ่ม</li><li>ทหารรับจ้างครบ21อาชีพ จ้างได้10คน มีตัวสำรอง</li><li>เงานักสู้และทหารใช้สกิลจริงของอาชีพ ฮีลและบัฟแยกทีม</li><li>เลเวลและงบสเตตัสเท่าผู้เล่น อุปกรณ์ระดับเดียวกัน</li><li>ชนะเมื่อฝ่ายตรงข้ามล้มครบทีม คืนปาร์ตี้เดิมเมื่อออก</li></ul><button id="get" disabled>กำลังเตรียมดาวน์โหลด…</button><p id="status" role="status"></p><p>แตกZIP แล้วเปิด <b>index.html</b><br>ปาร์ตี้สนามรวมผู้เล่น10คน: ผู้เล่น1+ทหาร9 อีกคนเป็นสำรอง<br>เมนูแอดมิน <b>G → stefan-gm</b><br>เลือก “ทีม10คน / ทหารทุกคลาส / เงานักสู้ / ประลอง V48”</p><small>ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง · ภาพตัวละคร แผนที่ และVFXเดิมจากV47</small></main>'''+script)
(P/'sw.js').write_text((R/'tools/download-v47/sw.js').read_text().replace('V47','V48'))
pack=json.loads((E/'package.json').read_text());z=D/pack['name'];data=z.read_bytes();assert hashlib.sha256(data).hexdigest()==pack['sha256'];parts=[];files={}
for i,start in enumerate(range(0,len(data),80*1024*1024)):
 p=D/('Runevale-V48.part'+str(i+1));p.write_bytes(data[start:start+80*1024*1024]);parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});files['downloads/V48/'+p.name]=p
for n in ['build.json','validation.json','package.json']:files['releases/V48/'+n]=E/n
for n in ['team-combat-v48.js','build_team_combat_v48.py','test_team_v48.py','package_team_v48.py','publish_team_v48.py']:files['releases/V48/tools/'+n]=R/'tools'/n
files['releases/V48/README.txt']=R/'build/Runevale-Recast-V48/อ่านก่อนเล่น.txt'
c=push('runevale-game-download',files,'Publish V48 class-skilled teams, mercenary roster and four arena modes')
for p in parts:p['url']='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V48/'+p['name']
(P/'config.json').write_text(json.dumps({**pack,'parts':parts}));print('PARTS',c,flush=True)
c2=push('gh-pages',{'v48/'+n:P/n for n in ['index.html','sw.js','config.json']},'Publish V48 tested game download page');print('PAGES',c2,flush=True)
(E/'publish.json').write_text(json.dumps({'partsCommit':c,'pagesCommit':c2,'page':'https://phuthanet9870-cpu.github.io/RAG/v48/'},indent=2))
