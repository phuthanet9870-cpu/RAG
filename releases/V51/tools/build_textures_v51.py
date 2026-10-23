from pathlib import Path
import json,hashlib
R=Path('/workspace/RAG');s=(R/'build/Runevale-Recast-V50/index.html').read_text();a=json.loads((R/'assets/textures-v51/data.json').read_text())
def replace_json(marker,obj):
 global s
 start=s.index(marker)+len(marker);old,end=json.JSONDecoder().raw_decode(s[start:]);s=s[:start]+json.dumps(obj,separators=(',',':'))+s[start+end:];return old
replace_json('const WORLD33_MATERIALS=',a['textures'])
start=s.index('const CITY49_ART=')+len('const CITY49_ART=');old,end=json.JSONDecoder().raw_decode(s[start:]);old.update(a);s=s[:start]+json.dumps(old,separators=(',',':'))+s[start+end:]
s=s.replace("document.createTextNode(' · V50 · นักสู้สุ่มอุปกรณ์')","document.createTextNode(' · V51 · พื้นผิวแฟนตาซี')").replace("document.title='Runevale Online V50 · นักสู้สุ่มอุปกรณ์'","document.title='Runevale Online V51 · พื้นผิวแฟนตาซี'")
code='''
const Texture51=(()=>{
 const names=NAMES51;
 TITLEOF.resources49='GM · Texture Resource V51';
 WIN.resources49.render=function(){if(!ADM.ok)return '';return `<p>พื้นผิววาดใหม่32แบบ · ทรัพยากรโปร่งใส6แบบ · ติดตั้งในทุกแผนที่แล้ว</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(138px,1fr));gap:10px">${CITY49_ART.textures.map((src,i)=>`<figure style="margin:0;padding:6px;background:#f4eddd;border:1px solid #baa87d;border-radius:8px"><img src="${src}" width="128" height="128" style="max-width:100%;height:auto"><figcaption>${i} · ${esc(names[i])}</figcaption></figure>`).join('')}</div><h3>วางทรัพยากรตกแต่ง</h3><p>ใช้ตกแต่งฉาก ไม่มีการเปลี่ยนระบบดรอปหรือเก็บเกี่ยว</p>${Object.keys(City49.resourceNames).map(id=>`<button data-act="gmResource49" data-a="${id}"><img src="${CITY49_ART.resources[id]}" width="64" height="64">${City49.resourceNames[id]}</button>`).join('')}`;};
 ACT.gmTexture51=()=>{if(ADM.ok)openWindow('resources49');};
 const admin=WIN.admin.render;WIN.admin.render=function(...a){return admin.apply(this,a)+(ADM.ok?'<button data-act="gmTexture51">Texture Resource V51 · พื้นผิว / แร่ / สมุนไพร</button>':'');};
 return {version:51,names};
})();
'''.replace('NAMES51',json.dumps([v['name']for v in json.loads((R/'assets/textures-v51/manifest.json').read_text())['textures']]))
s=s.replace('</script></body></html>',code+'\n</script></body></html>');O=R/'build/Runevale-Recast-V51';O.mkdir(exist_ok=True);(O/'index.html').write_text(s);E=R/'evidence/textures-v51';E.mkdir(exist_ok=True);(E/'build.json').write_text(json.dumps({'version':51,'base':50,'htmlSha256':hashlib.sha256(s.encode()).hexdigest(),'textures':32,'resources':6,'embedded':True},indent=2));print('Built V51')
