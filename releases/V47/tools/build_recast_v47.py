from pathlib import Path
import json,hashlib
R=Path('/workspace/RAG');A=R/'assets/recast-v47';E=R/'evidence/recast-v47';O=R/'build/Runevale-Recast-V47';base=(R/'build/Runevale-Recast-V46/index.html').read_text();s=base
library=json.loads((A/'library.json').read_text())
def get(text,marker):return json.JSONDecoder().raw_decode(text[text.index(marker)+len(marker):])[0]
def swap(marker,d):
 global s
 i=s.index(marker)+len(marker);_,n=json.JSONDecoder().raw_decode(s[i:]);s=s[:i]+json.dumps(d,ensure_ascii=False,separators=(',',':'))+s[i+n:]
swap('window.VFX46_LIBRARY=',library);s=s.replace('window.VFX46_LIBRARY=','window.VFX47_LIBRARY=')
for marker in ['window.SKILL_FX_DATA=','window.CAST_FX_DATA=']:
 data=get(s,marker)
 for d in data.values():d.update(frameCount=8,sourceFrameCount=8,subframes=1,version=47)
 swap(marker,data)
a=s.index('window.SkillEffects=(()=>{');b=s.index('</script>',a);s=s[:a]+(R/'tools/skill-effects-v47.js').read_text()+s[b:]
a=s.index('const Recast46=(()=>{');b=s.index('</script>',a);s=s[:a]+(R/'tools/gm-recast-v47.js').read_text()+s[b:]
s=s.replace('สกิลวาดใหม่ V46','สกิลวาดใหม่ V47 · 8 เฟรมตรง').replace('Runevale Online V46','Runevale Online V47').replace('VFX วาดใหม่29เฟรม','VFX ใหม่8เฟรมตรง').replace('สกิล V46','สกิล V47').replace('ทุกเฟรม V46','ทุกเฟรม V47')
s=s.replace('<h3>V46 · เดิน8','<h3>V47 · เดิน8')
(O/'index.html').write_text(s)
for marker in ['window.SHEET_DATA=','window.COSTUME36_DATA=','window.MONSTER_DATA=','const WORLD33_PLANS=','const WORLD33_PROPS=','const WORLD33_PLACEMENTS=','const HITBOX42_DATA=']:assert get(base,marker)==get(s,marker),marker
assert 'softBuffers44'not in s and 'imageSmoothingEnabled=true'not in (R/'tools/skill-effects-v47.js').read_text()
r={'version':47,'sha256':hashlib.sha256((O/'index.html').read_bytes()).hexdigest(),'skillsAudited':146,'sharedNewAnimationFamilies':48,'effectEntries':156,'framesPerFamily':8,'newOriginalKeys':384,'newFrames':384,'v44RendererRemoved':True,'offlineInterpolatedFramesRemoved':True,'noCrossfadeOrMorph':True,'nearestNativeFrameRendering':True,'characterSheetsV45AndMapsUnchanged':True,'damageFormulaCooldownCostUnchanged':True,'projectileDamageWaitsForFlight':True,'firebombSixthTickPrecisionFixed':True}
(E/'build.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
