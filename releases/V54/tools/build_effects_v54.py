from pathlib import Path
import json,hashlib
R=Path('/workspace/RAG');A=R/'assets/effects-v54';s=(R/'build/Runevale-Recast-V53/index.html').read_text();lib=json.loads((A/'library.json').read_text())
shape={'crest':'aegis','strike':'lance','crescent':'solar_slash','reaper':'soul_reap','chain':'soul_chain','shield':'aegis','banner':'aegis','fortress':'aegis','sanctum':'aegis','mist':'venom','skull':'eclipse','eclipse':'eclipse','cross':'holy_judgement','lightning':'lightning','tornado':'cyclone','wind':'tailwind','storm':'lightning','ice':'ice_spikes','sigil':'blizzard','blizzard':'blizzard','arrow':'arrow','arrowrain':'arrow_rain','eye':'bloom','vine':'vines','heal':'restoration','rainheal':'restoration','angel':'resurrection','fist':'spirit_fist','fissure':'forge_impact','orbit':'tailwind','hammer':'forge_impact','forge':'forge','anvil':'forge','flask':'acid','spore':'venom','bloom':'bloom','garden':'bloom','crossslash':'cross_blade','shadow':'soul_reap','web':'shadow_web'}
overrides={'ice_scholar_53_mastery':'frost_ward','i53_coat':'frost_ward','death_knight_53_mastery':'soul_ward','d53_armor':'soul_ward','twilight_knight_53_mastery':'soul_ward','t53_ward':'aegis','t53_dusk':'eclipse','c53_step':'soul_reap','r53_hunt':'cross_blade','cross_assassin_53_mastery':'cross_blade','shadow_stalker_53_mastery':'shadow_web','sniper_53_mastery':'arrow','storm_weaver_53_mastery':'cyclone','fist_champion_53_mastery':'spirit_fist','white_smith_53_mastery':'forge','life_creator_53_mastery':'bloom','high_priest_53_mastery':'holy_judgement'}
design=json.loads((R/'assets/classes-v53/design.json').read_text());mapping={};directions={'lance','solar_slash','spirit_fist','soul_reap','cross_blade','arrow','tailwind'}
def get(m):return json.JSONDecoder().raw_decode(s[s.index(m)+len(m):])[0]
def put(m,v):
 global s
 i=s.index(m)+len(m);_,n=json.JSONDecoder().raw_decode(s[i:]);s=s[:i]+json.dumps(v,separators=(',',':'))+s[i+n:]
def patch(a,b):
 global s
 assert a in s,a[:80];s=s.replace(a,b)
oldlib=get('window.VFX47_LIBRARY=');oldlib={k:v for k,v in oldlib.items()if not k.startswith('u53_')};oldlib.update(lib);put('window.VFX47_LIBRARY=',oldlib)
fx=get('window.SKILL_FX_DATA=')
for m in design['skills']:
 family=overrides.get(m['id'],shape[m['shape']]);k='u54_'+family;d=fx[m['id']];d.update({'family':k,'impact':k,'version':54,'frameCount':8,'sourceFrameCount':8,'subframes':1,'frameSize':128,'anchor':lib[k]['anchor'],'grounded':lib[k]['grounded'],'directional':family in directions,'projectileSize':90 if family in ['arrow','lightning']else 56 if family=='acid'else 48});mapping[m['id']]={'name':m['name'],'class':m['cls'],'family':family,'frames':8,'file':'atlases/'+family+'.png'}
put('window.SKILL_FX_DATA=',fx)
# Keep damage schedules unchanged. Only paint orientation and draw size change.
patch("size:d.pattern==='drop'?70:d.family==='arrow'?48:d.family==='acidflask'?30:36", "size:d.projectileSize||(d.pattern==='drop'?70:d.family==='arrow'?48:d.family==='acidflask'?30:36)")
patch("angle:['slash','pierce','backstab','fist'].includes(d.family)?a+(i%2?.18:-.18):0", "angle:(d.directional||['slash','pierce','backstab','fist'].includes(d.family))?a+(i%2?.18:-.18):0")
patch("angle:['slash','pierce','backstab','fist','poisonclaw'].includes(family)?angle:0", "angle:(d.directional||['slash','pierce','backstab','fist','poisonclaw'].includes(family))?angle:0")
patch("life:.42,layer:'ground'})", "life:.42,layer:'ground',angle:d.directional?(c.src.face||0):0})")
patch("if(f.projectile&&['acidflask','healflask'].includes(sf))", "if(f.projectile&&(['acidflask','healflask'].includes(sf)||sf==='u54_acid'))")
patch("arc:d.family==='acidflask'?28:0,spin:d.family==='acidflask'", "arc:(d.family==='acidflask'||d.family==='u54_acid')?28:0,spin:d.family==='acidflask'||d.family==='u54_acid'")
patch("data[id].version===53?data[id].family:'heal'", "data[id].version>=53?data[id].family:'heal'")
patch('เปิดครบ12คลาสขั้นสูง · 72สกิลต้นฉบับ · สกิลใช้งานมี12เฟรมต่อแอนิเมชัน','เปิดครบ12คลาสขั้นสูง · 72สกิลต้นฉบับ · เอฟเฟกต์วาดใหม่8เฟรมเข้าชุดเดิม')
patch('สกิลใหม่72ชุด12เฟรม','สกิลใหม่72ชุด8เฟรม')
patch("document.createTextNode(' · V53 · คลาสขั้นสูงครบ')","document.createTextNode(' · V54 · ชีตเอฟเฟกต์ชุดใหม่')")
patch("document.title='Runevale Online V53 · คลาสขั้นสูงครบ'","document.title='Runevale Online V54 · ชีตเอฟเฟกต์ชุดใหม่'")
# Add a read-only native-sheet gallery to GM; the existing per-frame preview is retained.
code='''
const Sheets54=(()=>{const map=MAP54;
 TITLEOF.sheets54='GM · Sprite Sheet เอฟเฟกต์ V54';WIN.sheets54={render(){if(!ADM.ok)return '';return `<p>สกิลใหม่72สกิลใช้ชีตวาดใหม่27ตระกูล · 8เฟรมวาดจริง · เฟรม128×128 · พื้นหลังโปร่งใส</p><p>กดชื่อสกิลเพื่อเปิดดูทีละเฟรมและสาธิตในฉาก · ใช้ภาพร่วมกันเมื่อเป็นพลังประเภทเดียวกัน</p>${Object.keys(SkillEffects.library).filter(k=>k.startsWith('u54_')).map(k=>`<section class="card" style="margin:12px 0;min-width:0"><b>${k.slice(4)}</b><div style="overflow:auto"><img src="${SkillEffects.library[k].src}" width="1024" height="128" style="max-width:none;image-rendering:pixelated" alt="${k.slice(4)} 8เฟรม"></div><div class="acts wrap">${Object.entries(map).filter(([id,m])=>'u54_'+m.family===k).map(([id,m])=>`<button data-act="u53Preview" data-a="${id}">${esc(m.name)}</button>`).join('')}</div></section>`).join('')}`;}};ACT.gmSheets54=()=>{if(ADM.ok)openWindow('sheets54');};const old=WIN.admin.render;WIN.admin.render=function(...a){return old.apply(this,a)+(ADM.ok?'<button data-act="gmSheets54">Sprite Sheet เอฟเฟกต์ใหม่ V54 · 27ชีต / 72สกิล</button>':'');};return{version:54,map};})();
'''.replace('MAP54',json.dumps(mapping,ensure_ascii=False,separators=(',',':')))
s=s.replace('</script></body></html>',code+'\n</script></body></html>');assert '"u53_'not in s
O=R/'build/Runevale-Recast-V54';O.mkdir(exist_ok=True);(O/'index.html').write_text(s);(A/'skill-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2));E=R/'evidence/effects-v54';E.mkdir(exist_ok=True);(E/'build.json').write_text(json.dumps({'version':54,'base':53,'replacedSkillEffects':72,'newFamilies':27,'framesPerFamily':8,'nativeFrames':216,'htmlSha256':hashlib.sha256(s.encode()).hexdigest(),'damageAndSkillsUnchanged':True},indent=2));print('Built V54',flush=True)
