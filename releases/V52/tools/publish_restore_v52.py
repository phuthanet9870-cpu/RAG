from pathlib import Path
import json,hashlib
exec(Path('/workspace/RAG/tools/publish_recast_v47.py').read_text().split('z=D/')[0])
E=R/'evidence/restore-v52';P=R/'tools/download-v52';P.mkdir(exist_ok=True);D=R/'dist';pack=json.loads((E/'packages.json').read_text())[0];data=(D/pack['name']).read_bytes();assert hashlib.sha256(data).hexdigest()==pack['sha256'];files={};parts=[]
for i,start in enumerate(range(0,len(data),80*1024*1024)):
 p=D/('Runevale-V52.part'+str(i+1));p.write_bytes(data[start:start+80*1024*1024]);parts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});files['downloads/V52/'+p.name]=p
for n in ['build.json','validation.json','restoration.json','packages.json']:files['releases/V52/'+n]=E/n
files['releases/V52/README.txt']=R/'build/Runevale-Recast-V52/อ่านก่อนเล่น.txt'
for n in ['build_restore_v52.py','test_restore_v52.py','test_gear_regression_v52.py','package_restore_v52.py','publish_restore_v52.py']:files['releases/V52/tools/'+n]=R/'tools'/n
c=push('runevale-game-download',files,'Restore pre-V49 materials and remove V49/V51 resource texture additions in V52')
for p in parts:p['url']='https://raw.githubusercontent.com/phuthanet9870-cpu/RAG/'+c+'/downloads/V52/'+p['name']
(P/'config.json').write_text(json.dumps({**pack,'parts':parts}));old=(R/'tools/download-v50/index.html').read_text();script=old[old.index('<script>'):].replace('V50','V52');head=old[:old.index('<main>')].replace('V50','V52')
(P/'index.html').write_text(head+'''<main><small>RUNEVALE ONLINE · V52</small><h1>กลับไปใช้พื้นผิวเดิม</h1><ul><li>คืนพื้นผิวชุดก่อนV49 ถอดTexture Resourceที่เพิ่มในV49และV51</li><li>ถอดทรัพยากรตกแต่ง6แบบและเมนูเสกชุดดังกล่าว</li><li>คงผังเมือง NPC คอสตูม และระบบต่อสู้/อุปกรณ์สุ่มจากV50</li></ul><button id="get" disabled>กำลังเตรียมดาวน์โหลด…</button><p id="status" role="status"></p><p>แตกZIP แล้วเปิด <b>index.html</b><br>GM: <b>G → stefan-gm</b></p><small>ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลองแล้ว</small></main>'''+script)
(P/'sw.js').write_text((R/'tools/download-v50/sw.js').read_text().replace('V50','V52'))
c2=push('gh-pages',{'v52/'+n:P/n for n in ['index.html','sw.js','config.json']},'Publish V52 restored original textures download page');(E/'publish.json').write_text(json.dumps({'partsCommit':c,'pagesCommit':c2,'page':'https://phuthanet9870-cpu.github.io/RAG/v52/'},indent=2));print('PARTS',c,'PAGES',c2,flush=True)
