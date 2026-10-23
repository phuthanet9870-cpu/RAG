from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path('/workspace/RAG');E=R/'evidence/recast-v46';E.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage']);q=b.new_page();q.goto('http://127.0.0.1:8767/RAG/build/Runevale-Low-Walk-V45/index.html',timeout=180000)
 rows=q.evaluate("""()=>Object.values(SK).map(s=>{let r={id:s.id,name:s.n,cls:s.cls,type:s.type||'active',target:s.tgt,max:s.max,oldMode:SkillEffects.data[s.id]?.mode,run:s.run?.toString()};for(let key of ['hits','sp','cast','fixed','cd','rng','r','desc'])r[key]=typeof s[key]==='function'?Array.from({length:s.max},(_,i)=>s[key](i+1)):s[key];return r})""");b.close()
(E/'skill-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(E/'skill-audit.txt').write_text('\n'.join(r['id']+' | '+r['name']+' | '+r['type']+' | '+str(r['desc'][-1]if isinstance(r['desc'],list)else r['desc'])for r in rows));print(len(rows))
