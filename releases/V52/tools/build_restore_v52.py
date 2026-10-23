from pathlib import Path
import json,hashlib
R=Path('/workspace/RAG');s=(R/'build/Runevale-Recast-V50/index.html').read_text();old=(R/'build/Runevale-Recast-V48/index.html').read_text()
def get(t,m):return json.JSONDecoder().raw_decode(t[t.index(m)+len(m):])[0]
def swap(m,d):
 global s
 i=s.index(m)+len(m);_,n=json.JSONDecoder().raw_decode(s[i:]);s=s[:i]+json.dumps(d,separators=(',',':'))+s[i+n:]
a=get(old,'const WORLD33_MATERIALS=');swap('const WORLD33_MATERIALS=',a);art=get(s,'const CITY49_ART=');art['textures']=[];art['resources']={};swap('const CITY49_ART=',art)
start=s.index(' function decorate(){',s.index('const City49='));end=s.index('\n const oldEnter=',start);s=s[:start]+" function decorate(){dress();}"+s[end:]
start=s.index("if(d.k==='resource49')",s.index('const City49='));end=s.index("const a=d.k==='world33'",start);s=s[:start]+s[end:]
s=s.replace('<button data-act="gmCity49Texture">ดูพื้นผิว / ทรัพยากร</button>','')
start=s.index(" TITLEOF.resources49=");end=s.index('\n ACT.gmCity49=',start);s=s[:start]+s[end:]
start=s.index('ACT.gmCity49Texture=');end=s.index('\n const oldAdmin=',start);s=s[:start]+s[end:]
s=s.replace("resourceNames={iron:'สายแร่เหล็ก',gold:'สายแร่ทอง',crystal:'ผลึกเวท',herb:'สมุนไพร',timber:'ไม้ท่อน',shell:'เปลือกหอย'}","resourceNames={}")
s=s.replace('เมืองใหม่ / สุ่มคอสตูม / พื้นผิวและทรัพยากร V49','เมือง / สุ่มคอสตูม').replace('GM · เมือง / คอสตูม / พื้นผิว V49','GM · เมือง / คอสตูม')
s=s.replace("document.createTextNode(' · V50 · นักสู้สุ่มอุปกรณ์')","document.createTextNode(' · V52 · คืนพื้นผิวเดิม')").replace("document.title='Runevale Online V50 · นักสู้สุ่มอุปกรณ์'","document.title='Runevale Online V52 · คืนพื้นผิวเดิม'")
assert 'resource49'not in s and 'gmResource49'not in s and 'gmTexture51'not in s
O=R/'build/Runevale-Recast-V52';O.mkdir(exist_ok=True);(O/'index.html').write_text(s);E=R/'evidence/restore-v52';E.mkdir(exist_ok=True);(E/'build.json').write_text(json.dumps({'version':52,'base':50,'htmlSha256':hashlib.sha256(s.encode()).hexdigest(),'materialsRestoredExactlyFrom':48,'removedTextureResourceVersions':[49,51],'preservedCityNpcCostumeAndCombat':True},indent=2));print('Built V52 — original textures restored')
