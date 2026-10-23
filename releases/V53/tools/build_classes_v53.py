from pathlib import Path
import json,hashlib,re
R=Path('/workspace/RAG');s=(R/'build/Runevale-Recast-V52/index.html').read_text();A=R/'assets/classes-v53';d=json.loads((A/'design.json').read_text());v=json.loads((A/'vfx.json').read_text())
def patch(a,b):
 global s
 assert a in s,a[:80];s=s.replace(a,b)
def update(marker,extra):
 global s
 i=s.index(marker)+len(marker);obj,n=json.JSONDecoder().raw_decode(s[i:]);obj.update(extra);s=s[:i]+json.dumps(obj,separators=(',',':'))+s[i+n:]
update('window.VFX47_LIBRARY=',v['library']);update('window.SKILL_FX_DATA=',v['fx'])
a=s.index('const LOCKED_JOBS =');b=s.index(';',a)+1;s=s[:a]+'const LOCKED_JOBS = [];'+s[b:]
insert='const Unlock53Design='+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n'+(R/'tools/classes-v53-definitions.js').read_text()+'\n'
patch('const SKILL_COUNT = Object.keys(SK).length;',insert+'const SKILL_COUNT = Object.keys(SK).length;')
patch("lineRoot(x) === root && CLS[x].tier <= tier)","lineRoot(x) === root && CLS[x].tier <= tier && (!UNLOCK53_IDS.includes(x)||jobChain(c).includes(x)))")
# Role and preferred weapon selection lives inside Team48.config; add the new classes there.
patch("const magical=['mage','wizard','sage','acolyte','priest'].includes(cls),ranged=['archer','hunter','bard','dancer'].includes(cls);", "const design53=Unlock53Design.classes.find(c=>c.id===cls);const magical=design53?['caster','healer'].includes(design53.role):['mage','wizard','sage','acolyte','priest'].includes(cls),ranged=design53?design53.role==='ranged':['archer','hunter','bard','dancer'].includes(cls);")
patch("role:cls==='priest'||cls==='acolyte'?'healer'", "role:design53?.role==='healer'||cls==='priest'||cls==='acolyte'?'healer'")
patch("wt:({knight:'sword2'", "wt:design53?.weapon||({knight:'sword2'")
patch("skills:Object.fromEntries(skillsFor(cls).map(id=>[id,SK[id].max])),falcon:cls==='hunter'", "skills:Object.fromEntries(skillsFor(cls).map(id=>[id,SK[id].max])),falcon:cls==='hunter'||cls==='sniper'")
# The new damage-leech option heals only after a successful hit, capped by remaining HP.
patch("  applyDmgMon(t, dmg, u, { crit, el, k: o.k, idx, em, src: c.s ? c.s.id : 'basic' });", "  const leech53=Math.max(0,t.hp);applyDmgMon(t, dmg, u, { crit, el, k: o.k, idx, em, src: c.s ? c.s.id : 'basic' });")
patch('  if (dmg > 0) {\n    if (d.a.leechHp', '  if (dmg > 0) {\n    if(o.leech&&leech53>0)healUnit(u,Math.round(Math.max(0,leech53-Math.max(0,t.hp))*o.leech),u);\n    if (d.a.leechHp')
patch('  if (dmg > 0) {\n    if(o.leech', '  if (dmg > 0) {\n    if(o.effect53&&idx===0&&t.hp<leech53)Unlock53Rules.onHit(c,t);\n    if(o.leech')
patch("  if (u.buffs.weak) dmg *= .8;", "  if (u.buffs.weak) dmg *= .8;if(u.st?.weaken53?.until>clock)dmg*=1-u.st.weaken53.v;")
patch("  let dmg = m.atk * mul * (.9 + rnd() * .2);", "  let dmg = m.atk * mul * (.9 + rnd() * .2);if(m.st?.weaken53?.until>clock)dmg*=1-m.st.weaken53.v;")
patch('d.move = 5 * T * Math.max(.3, 1 + a.move / 100)', 'd.move = 5 * T * (u.st?.slow>0?.5:1) * Math.max(.3, 1 + a.move / 100)')
patch("else emit(id,u.x,u.y,{sprite:'heal',size:80,life:.55})", "else emit(id,u.x,u.y,{sprite:data[id].version===53?data[id].family:'heal',size:80,life:.55})")
# Own class support skills should be tried before inherited support buffs.
patch("const supports=skills.filter(s=>!s.k", "skills.sort((a,b)=>(b.cls===a.cls)-(a.cls===b.cls));const supports=skills.filter(s=>!s.k") if False else None
# Keep existing AI order stable; prioritize new own-class support and healing without changing attacks.
patch("for(const s of skills){if(s.tgt==='dead'", "skills.sort((x,y)=>(y.cls===a.cls)-(x.cls===a.cls));for(const s of skills){if(s.tgt==='dead'")
# Existing GM effect previews must expose all12 frames for the new skills.
patch(' const active=()=>SkillEffects.data[id];',' const active=()=>SkillEffects.data[id];const nativeFrames=()=>SkillEffects.library[active().family]?.frameCount||8;')
patch('Math.floor(phase)%8:selectedFrame','Math.floor(phase)%nativeFrames():selectedFrame')
patch("label.textContent='เฟรม '+(k+1)+' / 8'", "label.textContent='เฟรม '+(k+1)+' / '+nativeFrames()")
patch('Math.floor(phase):selectedFrame)+1)%8','Math.floor(phase):selectedFrame)+1)%nativeFrames()')
patch('ครบ146สกิล · ภาพใหม่48ตระกูล','ครบ218สกิล · สกิลใหม่72ชุด12เฟรม')
patch('ตรวจ146สกิล / ระดับสกิล / สาธิตจังหวะ','ตรวจ218สกิล / ระดับสกิล / สาธิตจังหวะ')
patch('สกิลและวงร่าย156ชุด','สกิลและวงร่าย228ชุด')
patch("document.createTextNode(' · V52 · คืนพื้นผิวเดิม')", "document.createTextNode(' · V53 · คลาสขั้นสูงครบ')")
patch("document.title='Runevale Online V52 · คืนพื้นผิวเดิม'", "document.title='Runevale Online V53 · คลาสขั้นสูงครบ'")
s=s.replace('</script></body></html>','\nconst UNLOCK53_ICONS='+json.dumps(v['icons'],separators=(',',':'))+';\n'+(R/'tools/classes-v53-ui.js').read_text()+'\n</script></body></html>')
O=R/'build/Runevale-Recast-V53';O.mkdir(exist_ok=True);(O/'index.html').write_text(s);E=R/'evidence/classes-v53';E.mkdir(exist_ok=True);(E/'build.json').write_text(json.dumps({'version':53,'base':52,'classesAdded':12,'skillsAdded':72,'activeSkillsAdded':60,'passivesAdded':12,'totalClasses':33,'totalSkills':218,'framesPerSkill':12,'htmlSha256':hashlib.sha256(s.encode()).hexdigest()},indent=2));print('Built V53',flush=True)
