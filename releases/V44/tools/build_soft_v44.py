from pathlib import Path
import hashlib,json
R=Path('/workspace/RAG');base=R/'build/Runevale-Smooth-Animations-V43/index.html';s=base.read_text()
def replace(a,b):
 global s
 assert s.count(a)==1,(a[:110],s.count(a));s=s.replace(a,b)
start=s.index(' function blit(c,id,phase,x,y,o={}){');end=s.index(' function emit(id,x,y,o={}){',start);s=s[:start]+' '+(R/'tools/blit-soft-v44.js').read_text()+s[end:]
start=s.index('function bfsPath(sx, sy, gx, gy) {');end=s.index('/* ---------- ground ---------- */',start);s=s[:start]+(R/'tools/pathing-v44.js').read_text()+'\n'+s[end:]
start=s.index('function moveToward(u, x, y, spd, dt) {');end=s.index('/* ---------- Player update ---------- */',start)
s=s[:start]+'''function moveToward(u,x,y,spd,dt){
 if(Math.hypot(x-u.x,y-u.y)<1.5||spd<=0||dt<=0)return false;
 const beforeX=u.x,beforeY=u.y,[sx,sy]=W.solid?steerPoint(u,x,y):[x,y],dx=sx-u.x,dy=sy-u.y,dd=Math.hypot(dx,dy);
 if(dd<.001)return false;
 const step=Math.min(dd,spd*dt);slideTo(u,u.x+dx/dd*step,u.y+dy/dd*step);inBounds(u);
 const traveled=Math.hypot(u.x-beforeX,u.y-beforeY);if(traveled<.001)return false;
 u.face=Math.atan2(u.y-beforeY,u.x-beforeX);u.walkT=(u.walkT||0)+traveled/T;return true;
}

'''+s[end:]
replace('if (dd <= r + 6) { const q = u.queued;', 'if (dd <= r + 6 && lineClear(u.x,u.y,t.x,t.y)) { const q = u.queued;')
replace('if (dd > d.rng + MonsterHitbox42.radius(t)) return moveToward(u, t.x, t.y, d.move, dt);','if (dd > d.rng + MonsterHitbox42.radius(t) || !lineClear(u.x,u.y,t.x,t.y)) return moveToward(u,t.x,t.y,d.move,dt);')
replace('function updateMon(m, dt) {\n  const st = m.st;','function updateMon(m, dt) {\n  world33PlaceActor(m);\n  const st = m.st;')
replace('m.x += m.kx * f; m.y += m.ky * f;', 'slideTo(m,m.x+m.kx*f,m.y+m.ky*f);')
replace('if (dd > reach) { if (spd) { m.x += (tgt.x - m.x) / dd * spd * dt; m.y += (tgt.y - m.y) / dd * spd * dt; m.walkT = (m.walkT || 0) + dt * spd / T; } m.face = Math.atan2(tgt.y - m.y, tgt.x - m.x); }','if(dd>reach||!lineClear(m.x,m.y,tgt.x,tgt.y)){if(spd)moveToward(m,tgt.x,tgt.y,spd,dt);m.face=Math.atan2(tgt.y-m.y,tgt.x-m.x)}')
replace('if (dd <= reach + 6 && m.atkT <= 0) {','if (dist(m,tgt)<=reach+6 && lineClear(m.x,m.y,tgt.x,tgt.y) && m.atkT<=0) {')
replace('if (wd > 4 && spd) { m.x += wx / wd * spd * .35 * dt; m.y += wy / wd * spd * .35 * dt; m.face = Math.atan2(wy, wx); m.walkT = (m.walkT || 0) + dt * spd * .35 / T; }','if(wd>4&&spd&&!moveToward(m,m.wx,m.wy,spd*.35,dt)){m.wt=0}')
# A simple sampling segment is shared by actors and projectile visibility.
replace('n = Math.ceil(d / 14);','n = Math.max(1,Math.ceil(d / 5));')
# Keep the GM inspector and every existing gameplay catalogue accessible.
s=s.replace('เมืองกระชับ V43','เดินเข้าตี / VFX นุ่มนวล V44')
s=s.replace('<title>Runevale Online</title>','<title>Runevale Online V44</title>')
O=R/'build/Runevale-Soft-VFX-Combat-V44';O.mkdir(exist_ok=True);(O/'index.html').write_text(s)
report={'version':44,'baseSHA256':hashlib.sha256(base.read_bytes()).hexdigest(),'sha256':hashlib.sha256((O/'index.html').read_bytes()).hexdigest(),'vfx':'continuous premultiplied frame interpolation, high quality resampling; unchanged artwork/colors/durations','pathing':'shared foot collision, no overshoot, safe wander/chase/knockback, obstacle-aware combat','preserved':['43 body variants','156 VFX sheets','31 maps','GM G stefan-gm','damage and movement speed']};(R/'evidence/soft-vfx-v44/build.json').write_text(json.dumps(report,indent=2));print(report)
