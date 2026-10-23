from pathlib import Path
import json,math,hashlib
R=Path('/workspace/RAG');s=(R/'build/Runevale-Recast-V48/index.html').read_text();A=json.loads((R/'assets/city-v49/data.json').read_text())
def get(m):return json.JSONDecoder().raw_decode(s[s.index(m)+len(m):])[0]
def swap(m,d):
 global s
 i=s.index(m)+len(m);_,n=json.JSONDecoder().raw_decode(s[i:]);s=s[:i]+json.dumps(d,ensure_ascii=False,separators=(',',':'))+s[i+n:]
def patch(a,b):
 global s
 assert a in s,a[:70]
 s=s.replace(a,b)
plans=get('const WORLD33_PLANS=');places=get('const WORLD33_PLACEMENTS=');p=plans[0];factor=80/p['cols'];p['cols']=p['rows']=80
for lane in p['lanes']:
 for v in lane:v[0]*=factor;v[1]*=factor
for d in places['0']:
 ox,oy=d['x'],d['y'];d['x']=round(ox*factor);d['y']=round(oy*factor)
 if d.get('hit'):
  x,y,w,h=d['hit'];d['hit']=[d['x']+x-ox,d['y']+y-oy,w,h]
 if d['asset']=='town-landmarks-castle':
  sc=min(1,(d['y']-32)/d['height']);d['width']=round(d['width']*sc);d['height']=round(d['height']*sc);d['hit']=[d['x']-d['width']*.425,d['y']-d['height']*.25,d['width']*.85,d['height']*.253]
# One distinct town service per townhouse, plus the costume boutique.
houses=[d for d in places['0']if d['asset'].startswith('town-street-house')];available=houses+[next(d for d in places['0']if d['asset']=='town-civic-bakery')]
roles=list(p['npcs'])+['costumegacha'];p['npcs']['costumegacha']=[.32,.84];assign={}
for role in roles:
 tx,ty=p['npcs'][role];d=min(available,key=lambda d:(d['x']/3200-tx)**2+(d['y']/3200-ty)**2);available.remove(d);d['service49']=role;p['npcs'][role]=[d['x']/3200,(d['y']+54)/3200];assign[role]={'asset':d['asset'],'door':[d['x'],d['y']+54]}
 # Link each doorstep to the nearest existing road, retaining the irregular grass plots.
 best=None
 for a,b in p['roads']:
  ax,ay=a[0]*3200,a[1]*3200;bx,by=b[0]*3200,b[1]*3200;dx,dy=bx-ax,by-ay;t=max(0,min(1,((d['x']-ax)*dx+(d['y']+54-ay)*dy)/(dx*dx+dy*dy or 1)));q=[ax+t*dx,ay+t*dy];dd=math.hypot(q[0]-d['x'],q[1]-d['y']-54)
  if best is None or dd<best[0]:best=(dd,q)
 p['lanes'].append([[d['x'],d['y']+14],[d['x'],d['y']+54],best[1]])
swap('const WORLD33_PLANS=',plans);swap('const WORLD33_PLACEMENTS=',places);swap('const WORLD33_MATERIALS=',A['textures'])
# Walk speed: change the one base formula; preserve buffs and GM multipliers.
patch('d.move = 2.5 * T *', 'd.move = 5 * T *')
# Combat stops at reach instead of walking toward the centre of a moving monster.
patch('if (dd > d.rng + MonsterHitbox42.radius(t) || !lineClear(u.x,u.y,t.x,t.y)) return moveToward(u,t.x,t.y,d.move,dt);', 'if (Combat49.approach(u,t,d.rng+MonsterHitbox42.radius(t),d.move,dt)) return true; if(!lineClear(u.x,u.y,t.x,t.y))return false;')
patch('return moveToward(u, t.x, t.y, d.move, dt);','return Combat49.close(u,t,Math.max(8,r-3),d.move,dt);')
patch('if(dd>reach||!lineClear(m.x,m.y,tgt.x,tgt.y)){if(spd)moveToward(m,tgt.x,tgt.y,spd,dt);m.face=Math.atan2(tgt.y-m.y,tgt.x-m.x)}','if(dd>reach||!lineClear(m.x,m.y,tgt.x,tgt.y)){if(spd)Combat49.close(m,tgt,Math.max(8,reach-3),spd,dt);m.face=Math.atan2(tgt.y-m.y,tgt.x-m.x)}')
patch('if (!a.boss) { a.x -= dx / dd * p; a.y -= dy / dd * p; }','if (!a.boss && a.hp>0) slideTo(a,a.x-dx/dd*p,a.y-dy/dd*p);')
patch('if (!b.boss) { b.x += dx / dd * p; b.y += dy / dd * p; }','if (!b.boss && b.hp>0) slideTo(b,b.x+dx/dd*p,b.y+dy/dd*p);')
patch('ความเร็วพื้นฐาน 2.5 ช่อง/วินาที','ความเร็วพื้นฐาน 5 ช่อง/วินาที')
patch('baseWalkTilesPerSecond:2.5','baseWalkTilesPerSecond:5')
# Substep endpoint interpolation: never let an axis-slide overshoot the requested destination.
old='let x=u.x+(nx-sx)/n,y=u.y+(ny-sy)/n;'
# Retain incremental swept substeps: blocked axes must not jump through a wall.
patch("document.createTextNode(' · V48 · ทีม10คน / ประลอง')", "document.createTextNode(' · V49 · เมือง / คอสตูม')")
patch("document.title='Runevale Online V48 · ทีม10คน / ประลอง'", "document.title='Runevale Online V49 · เมือง / คอสตูม'")
s=s.replace('</script></body></html>','\nconst CITY49_ART='+json.dumps(A,separators=(',',':'))+';\n'+(R/'tools/city-v49.js').read_text()+'\n</script></body></html>')
O=R/'build/Runevale-Recast-V49';O.mkdir(exist_ok=True);(O/'index.html').write_text(s);E=R/'evidence/city-v49';E.mkdir(exist_ok=True)
(E/'build.json').write_text(json.dumps({'version':49,'sha256':hashlib.sha256(s.encode()).hexdigest(),'townBefore':[96,96],'townAfter':[80,80],'npcHomes':assign,'walkBaseTilesPerSecond':5,'costumeIcons':10,'materials':32,'resourceSprites':6},ensure_ascii=False,indent=2));print('Built V49',flush=True)
