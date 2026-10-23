from pathlib import Path
import hashlib,json
R=Path('/workspace/RAG');s=(R/'build/Runevale-Recast-V49/index.html').read_text()
def patch(a,b):
 global s
 assert a in s,a[:100]
 s=s.replace(a,b)
a=s.index('  a.equip=JSON.parse(JSON.stringify(P.equip||{}));',s.index('const Team48='));b=s.index('  a.wt=M.wt;',a);s=s[:a]+'  Gear50.equip(a,M);\n'+s[b:]
patch('const budget=Math.max(6,STAT_KEYS.reduce', 'const weights=Gear50.weights(a,M.stats);const budget=Math.max(6,STAT_KEYS.reduce')
patch('(budget-6)*M.stats[k]','(budget-6)*weights[k]')
patch('function make(kind){const cls=clsOf(kind);','function make(kind,load){const cls=clsOf(kind);')
patch('};sync(a);a.hp=derive(a).maxHP;',"};if(load&&load.cls===cls&&load.equip?.weapon&&Object.values(load.equip).every(it=>ITEM[it.id])){a.equip=JSON.parse(JSON.stringify(load.equip));a._equipLevel50=load.level;a.seed50=load.seed;a.kit50=true;}sync(a);a.hp=derive(a).maxHP;")
patch('.slice(0,10).map(make).filter(Boolean)', '.slice(0,10).map((kind,i)=>make(kind,P.mercGear50?.[i])).filter(Boolean)')
patch("if(chosen.length!==mode-1){note('เลือกทหารรับจ้าง '+(mode-1)+' คนก่อนเข้า');return false;}","if(![1,3,5,10].includes(mode)||chosen.length>mode-1){note('เลือกทหารได้สูงสุด '+(mode-1)+' คน');return false;}")
patch("${selected.size!==mode-1?'disabled':''}","${selected.size>mode-1?'disabled':''}")
patch('เลือกทหารรับจ้าง ${selected.size}/${mode-1} คน','เลือกทหาร ${selected.size}/${mode-1} คน · เข้าได้ตั้งแต่0คน ไม่ต้องครบทีม')
patch('ฝ่ายละจำนวนที่เลือก รวมตัวคุณ · ต่อสู้กับทีมเงานักสู้ที่ใช้สกิลจริง', 'โหมดกำหนดจำนวนเงาฝ่ายตรงข้ามและเพดานทีมคุณ เลือกทหาร0–จำนวนสูงสุดได้ · เงาสุ่มอุปกรณ์และใช้สกิลจริง')
patch('อุปกรณ์ระดับเดียวกัน ใช้สกิลจริงตามอาชีพ', 'อุปกรณ์สุ่มส่วนตัวตามเลเวล ไม่คัดลอกชุดผู้เล่น ใช้สกิลจริงตามอาชีพ')
patch('${selecting?`<button data-act="team48Pick"', '${`<button data-act="kit50" data-a="${i}">ดูอุปกรณ์</button>`}${selecting?`<button data-act="team48Pick"')
patch('size:mode,done:false','size:mode,playerCount50:chosen.length+1,done:false')
patch("banner(mode+' vs '+mode,", "banner((chosen.length+1)+' vs '+mode,")
patch('กำลังประลอง ${W.arena.size}v${W.arena.size}', 'กำลังประลอง ${W.allies.length+1}vs${W.arena.size} · โหมด${W.arena.size}v${W.arena.size}')
# More deliberate target selection, with a minimum lock interval to avoid flicker.
patch('const d=derive(a);let t=a.target', "const d=derive(a);if(a.fighter48&&a.st.taunt>0&&a.aggroOn&&Team48.enemy(a,a.aggroOn)&&a.aggroOn.hp>0)a.target=a.aggroOn;if(a.fighter48&&!a.queued&&!(a.st.taunt>0)&&clock>(a.nextFocus50||0)){a.nextFocus50=clock+1.6;const options=foes(a).filter(x=>!x.dead&&x.hp>0&&dist(a,x)<16*T);const score=x=>dist(a,x)/T+x.hp/derive(x).maxHP*4-(['priest','acolyte'].includes(x.cls)?2:0)-(x.cast?1:0);if(options.length)a.target=options.sort((x,y)=>score(x)-score(y))[0];}let t=a.target")
patch("document.createTextNode(' · V49 · เมือง / คอสตูม')","document.createTextNode(' · V50 · นักสู้สุ่มอุปกรณ์')")
patch("document.title='Runevale Online V49 · เมือง / คอสตูม'","document.title='Runevale Online V50 · นักสู้สุ่มอุปกรณ์'")
s=s.replace('</script></body></html>',(R/'tools/gear-combat-v50.js').read_text()+'\n</script></body></html>')
O=R/'build/Runevale-Recast-V50';O.mkdir(exist_ok=True);(O/'index.html').write_text(s);E=R/'evidence/gear-v50';E.mkdir(exist_ok=True);(E/'build.json').write_text(json.dumps({'version':50,'sha256':hashlib.sha256(s.encode()).hexdigest(),'randomIndependentKits':True,'underfilledModes':[1,3,5,10],'persistentMercenaryKits':True},indent=2));print('Built V50')
