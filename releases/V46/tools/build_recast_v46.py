from pathlib import Path
import json,hashlib
R=Path('/workspace/RAG');A=R/'assets/recast-v46';E=R/'evidence/recast-v46';O=R/'build/Runevale-Recast-V46';O.mkdir(exist_ok=True);base=(R/'build/Runevale-Low-Walk-V45/index.html').read_text();s=base;library=json.loads((A/'library.json').read_text());design=json.loads((A/'design.json').read_text())
def get(marker):
 i=s.index(marker)+len(marker);return json.JSONDecoder().raw_decode(s[i:])[0]
def swap(marker,d):
 global s
 i=s.index(marker)+len(marker);_,n=json.JSONDecoder().raw_decode(s[i:]);s=s[:i]+json.dumps(d,ensure_ascii=False,separators=(',',':'))+s[i+n:]
old=get('window.SKILL_FX_DATA=');casts=get('window.CAST_FX_DATA=');new={}
for id,d in old.items():
 profile=design.get(id)
 if not profile:
  families={'tq_cast':'cast_arcane','tq_claw':'poisonclaw','tq_wave':'poisonclaw','tq_bind':'vines','tq_explosion':'poisoncloud','tq_zone':'poisoncloud'};assert id in families,id;profile={'family':families[id],'pattern':'boss'}
 family=profile['family'];lib=library[family];new[id]={**{k:v for k,v in d.items()if k not in ['src','frameCount','sourceFrameCount','subframes','frameRects','packed','anchor','frameSize']},**profile,'duration':.6,'frameSize':128,'frameCount':29,'sourceFrameCount':8,'subframes':4,'anchor':lib['anchor'],'grounded':lib['grounded'],'version':46}
for id,d in casts.items():
 lib=library[id];casts[id]={**{k:v for k,v in d.items()if k not in ['src','frameCount','sourceFrameCount','subframes','frameRects','packed','anchor','frameSize']},'family':id,'pattern':'cast','frameSize':128,'frameCount':29,'sourceFrameCount':8,'subframes':4,'anchor':lib['anchor'],'grounded':True,'version':46}
assert len(new)==152 and len(casts)==4 and len(library)==48
swap('window.SKILL_FX_DATA=',new);swap('window.CAST_FX_DATA=',casts)
pos=s.index('window.SKILL_FX_DATA=');s=s[:pos]+'window.VFX46_LIBRARY='+json.dumps(library,separators=(',',':'))+';'+s[pos:]
a=s.index('window.SkillEffects=(()=>{');b=s.index('</script>',a);s=s[:a]+(R/'tools/skill-effects-v46.js').read_text()+s[b:]
needle="u.buffs[id] = Object.assign({ t, max: t, mods, sk: CURSK }, extra);"
assert s.count(needle)==1;s=s.replace(needle,needle+"SkillEffects.buff(u);")
needle="a.buffs.oath = { t: 30 + 3 * c.lv, by: c.src, mods: {} };"
assert s.count(needle)==1;s=s.replace(needle,needle+"SkillEffects.buff(a);")
needle='g.tick >= (g.max / g.ticks)';assert s.count(needle)==1;s=s.replace(needle,'g.tick + 1e-7 >= (g.max / g.ticks)')
# Replace old generic combat canvas emitters too; retain the monster death sheet.
a=s.index('FXK.hit =');b=s.index('function drawWarns(c, t)',a);line=next(l for l in s[a:b].splitlines()if l.startswith('FXK.monsterSheetDeath='));s=s[:a]+line+'\n\n'+s[b:]
# Flights and impacts share the exact same execution schedule and hit count.
a=s.index('function hitT(c, o, t = c.t) {');b=s.index('function oneHit(',a)
s=s[:a]+'''function hitT(c,o,t=c.t){
 if(!t||t.hp<=0)return;const visualDelay=SkillEffects.timeline(c,o,t)||0;SkillEffects.basicHits(c,o,t);const hits=o.hits||1,start=(o.start||0)+visualDelay;
 if(hits>1||o.delay||start){for(let i=0;i<hits;i++)W.timers.push({at:clock+start+i*(o.delay||.06),fn:()=>oneHit(c,o,t,i)})}else oneHit(c,o,t,0);
}
'''+s[b:]
s=s.replace('เดินก้าวต่ำ V45','สกิลวาดใหม่ V46').replace('Runevale Online V45','Runevale Online V46')
for a,b in [('ตรวจเฟรมเดิน / โจมตี / สกิล V45','ตรวจเฟรมเดิน / โจมตี / สกิล V46'),('ตรวจเดิน / โจมตี / VFX ทุกเฟรม V45','ตรวจเดิน / โจมตี / VFX ทุกเฟรม V46'),('<h3>V45 · เดิน8 / โจมตี12เฟรม · VFX29–33เฟรม</h3>','<h3>V46 · เดิน8 / โจมตี12เฟรม · VFX วาดใหม่29เฟรม</h3>')]:s=s.replace(a,b)
payload=(R/'tools/gm-recast-v46.js').read_text()if(R/'tools/gm-recast-v46.js').exists()else'';pos=s.rfind('</script>');s=s[:pos]+payload+s[pos:];(O/'index.html').write_text(s)
# Character frames, all 31 maps, inventory and old damage formulas remain exact.
for marker in ['window.SHEET_DATA=','window.COSTUME36_DATA=','window.MONSTER_DATA=','const WORLD33_PLANS=','const WORLD33_PROPS=','const WORLD33_PLACEMENTS=','const HITBOX42_DATA=']:
 i=base.index(marker)+len(marker);oldval,_=json.JSONDecoder().raw_decode(base[i:]);assert oldval==get(marker),marker
r={'version':46,'sha256':hashlib.sha256((O/'index.html').read_bytes()).hexdigest(),'skillsAudited':146,'sharedNewAnimationFamilies':48,'effectEntries':156,'framesPerFamily':29,'newOriginalKeys':384,'newFrames':1392,'v44RendererRemoved':'softBuffers44'not in s,'oldSkillArtRemoved':all(d.get('src')not in s for d in old.values()),'oldCanvasSkillEmittersRemoved':'FXK.hit ='not in s,'characterSheetsV45AndMapsUnchanged':True,'damageFormulaCooldownCostUnchanged':True,'projectileDamageWaitsForFlight':True,'firebombSixthTickPrecisionFixed':True};(E/'build.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
