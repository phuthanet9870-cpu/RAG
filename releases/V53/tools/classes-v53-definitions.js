const UNLOCK53_IDS=Unlock53Design.classes.map(c=>c.id);
const Unlock53Rules=(()=>{
 const models=Object.fromEntries(Unlock53Design.skills.map(s=>[s.id,s]));
 function healValue(u,l){const d=derive(u);return Math.round((d.maxHP*(.08+.02*l)+d.MATK*(.4+.15*l))*(1+d.a.healPct/100));}
 const mods=(m,l)=>m==='guard'||m==='fortress'?{DEF:10+4*l,red:6+2*l}:m==='mguard'?{MDEF:12+5*l,red:4+l}:m==='selfguard'?{DEF:15+5*l,MDEF:10+3*l,red:8+l}:m==='hastecast'?{castPct:8+2*l,move:5+2*l}:m==='focus'?{HIT:15+5*l,CRIT:5+2*l}:m==='fury'?{ASPD:6+2*l,ATK:10+4*l}:m==='warcry'?{ATKp:5+2*l,HIT:10+3*l}:m==='vital'?{HPpct:4+2*l,red:3+l}:m==='evasion'?{FLEE:10+4*l,move:5+2*l}:{};
 const modNames={DEF:'DEF',MDEF:'MDEF',red:'ลดดาเมจ%',castPct:'ลดเวลาร่าย%',move:'ความเร็วเดิน%',HIT:'HIT',CRIT:'คริ%',ASPD:'ความเร็วโจมตี%',ATK:'ATK',ATKp:'ATK%',HPpct:'HPสูงสุด%',FLEE:'FLEE'};
 function desc(s,l){if(s.passive)return `${s.stat} +${s.bonus*l}${['HPpct','SPpct','ASPD','CRIT','healPct'].includes(s.stat)?'%':''} (ติดตัว)`;
  const m=s.mechanic,r=s.radius||0,v=Math.round((s.mul+s.step*(l-1))*100),where=s.target==='self'?'รอบตัว':s.target==='ground'?'รอบจุดเลือก':'เป้าหมาย',tail=` · SP ${s.sp+s.spStep*l} · CD ${s.cd}วิ · ร่าย ${s.cast}วิ`;
  let d='';if(['guard','mguard','selfguard','hastecast','focus','fury','warcry','vital','evasion'].includes(m))d=`${s.target==='party'?'ทีมในระยะ8ช่อง':'ตนเอง'}: ${Object.entries(mods(m,l)).map(([k,v])=>(modNames[k]||k)+' +'+v).join(' / ')} นาน ${12+2*l}วิ`;
  else if(['heal','healclean'].includes(m))d=`ฟื้น HP เพื่อนหรือตนเอง ${8+2*l}% HPสูงสุดผู้ร่าย + MATK ${Math.round((.4+.15*l)*100)}% (เพิ่มตามโบนัสฮีล)`+(m==='healclean'?' และล้างพิษ/อ่อนแรง':'');
  else if(m==='cleanse')d=`ล้างพิษ มึนงง แช่แข็ง ตรึง ช้า และอ่อนแรง ให้ทีมใน8ช่อง พร้อมฟื้น HP ${4+l}% ของHPสูงสุดผู้ร่าย`;
  else if(m==='revive')d=`ชุบเพื่อนที่ล้มทุกคนใน7ช่องด้วยHP ${25+5*l}% · ต้องมีเพื่อนล้มอยู่ใกล้`;
  else if(m==='taunt')d='ยั่วยุศัตรูใน3ช่อง4วิ และลดดาเมจโจมตีและเวทที่ศัตรูทำ20% นาน8วิ';
  else {d=`${s.k==='m'?'MATK':'ATK'} ${v}% ×${s.hits} จังหวะ ธาตุ${['ปกติ','น้ำ','ดิน','ไฟ','ลม','พิษ','แสง','มืด'][s.el]} · ${where}${r?' รัศมี'+r+'ช่อง':''}`;
   if(m==='cone')d+=` · กรวย70° ผลัก1ช่อง`;
   if(m==='drain'||m==='harvest')d+=` · คืนHP ${m==='drain'?20+2*l:15}% ของดาเมจจริง`;
   if(m==='break')d+=` · ลดDEF ${10+3*l}% นาน8วิ`;
   if(m==='dash')d+=' · พุ่งประชิดโดยตรวจสิ่งกีดขวาง';
   if(m==='execute')d+=' · แรงขึ้น50% เมื่อเป้าถูกตรึง';
   if(m==='holy')d+=' · แรงขึ้น50% ต่อผีดิบ/ปีศาจ';
   if(m==='garden')d+=` · ฟื้นHPทีมในวง ${4+l}% ของHPสูงสุดผู้ร่ายหนึ่งครั้ง`;
   if(m==='fortress')d+=` · ทีมใน8ช่องรับDEF +${10+4*l} ลดดาเมจ${6+2*l}% นาน${8+l}วิ`;
   if(s.status)d+=` · ${s.status==='weak'?'ลดดาเมจโจมตีและเวทที่ทำ20%':s.status==='poison'?'พิษ':s.status==='freeze'?'แช่แข็ง':s.status==='root'?'ตรึง':s.status==='stun'?'มึนงง':'ช้า50%'} ${s.statusDuration}วิ (บอสต้านตรึง/แข็ง/มึนงง)`;
  }return d+tail;
 }
 function weaken(t,duration){t.st||={};t.st.weaken53={until:clock+duration,v:.2};}
 function run(c){const s=models[c.s.id],l=c.lv,m=s.mechanic,u=c.src,at=s.target==='self'?u:{x:c.x,y:c.y},extra={label:s.name};
  if(['guard','mguard','hastecast','warcry','vital','evasion'].includes(m))return partyBuff(c,s.id,12+2*l,mods(m,l),8,extra);
  if(['selfguard','focus','fury'].includes(m))return buffU(u,s.id,12+2*l,mods(m,l),extra);
  if(m==='heal'||m==='healclean'){const a=c.ally||u;healUnit(a,healValue(u,l),u);if(m==='healclean'){delete a.st?.poison;delete a.st?.weaken53;}return;}
  if(m==='cleanse'){for(const a of allyList(u))if(dist(a,u)<=8*T){for(const k of ['poison','stun','freeze','root','slow','weaken53'])delete a.st?.[k];healUnit(a,derive(u).maxHP*(.04+.01*l),u);}return;}
  if(m==='revive'){for(const a of Team48.members(u,true))if(a.dead&&dist(a,u)<=7*T){reviveUnit(a,.25+.05*l);SkillEffects.emit(s.id,a.x,a.y,{size:115,life:1.1});}return;}
  if(m==='taunt'){area(c,u.x,u.y,3*T,t=>{t.st.taunt=4;t.aggroOn=u;t.aggro=1;weaken(t,8);});return;}
  if(m==='dash'&&c.t)dashTo(u,c.t);
  const hit=t=>{let mul=s.mul+s.step*(l-1);if(m==='execute'&&t.st.root>0)mul*=1.5;if(m==='holy'&&['undead','demon'].includes(t.race))mul*=1.5;
   hitT(c,{k:s.k,el:s.el,mul,hits:s.hits,delay:.11,ranged:s.range>=8,effect53:true,leech:m==='drain'?(.2+.02*l):m==='harvest'?.15:0},t);

  };
  if(m==='cone')cone(c,c.t?Math.atan2(c.t.y-u.y,c.t.x-u.x):u.face,s.radius*T,70,hit);
  else if(s.radius)area(c,at.x,at.y,s.radius*T,hit);else if(c.t)hit(c.t);
  if(m==='fortress')partyBuff(c,s.id,8+l,mods(m,l),8,extra);
  if(m==='garden')for(const a of allyList(u))if(Math.hypot(a.x-at.x,a.y-at.y)<=s.radius*T)healUnit(a,derive(u).maxHP*(.04+.01*l),u);
 }
 function onHit(c,t){const s=models[c.s?.id];if(!s)return;const m=s.mechanic,l=c.lv,u=c.src;
   if(m==='break')t.st.defdown={t:8,v:(10+3*l)/100};
   if(s.status==='weak')weaken(t,s.statusDuration);else if(s.status)status(t,s.status,s.statusDuration,1,u);
   if(m==='cone')knock(t,u,1);
 }
 for(const c of Unlock53Design.classes){const p=CLS[c.parent];cls(c.id,{n:c.name,from:c.parent,tier:3,jobMax:70,hp:[p.hp[0]*1.08,p.hp[1]*1.08],sp:p.sp*1.12,wpns:[...new Set([c.weapon,...p.wpns])],c:c.color,blurb:c.blurb,melee:['tank','fighter'].includes(c.role)?1:0,rangedCls:c.role==='ranged'?1:0});RP[c.id]={...RP[c.parent]};}
 for(const s of Unlock53Design.skills){if(s.passive){sk(s.cls,s.id,s.name,{type:'passive',max:5,desc:l=>desc(s,l),pas:(l,a)=>{a[s.stat]+=s.bonus*l;}});continue;}
  sk(s.cls,s.id,s.name,{max:5,tgt:s.target==='single'?'enemy':s.target,rng:s.range,r:s.radius,sp:l=>s.sp+s.spStep*l,cd:s.cd,cast:s.cast,fixed:s.ultimate?.15:0,k:s.k||undefined,el:s.el,mul:l=>s.mul+s.step*(l-1),hits:()=>s.hits,req:s.req,desc:l=>desc(s,l),run,ai:['heal','healclean'].includes(s.mechanic)?'heal':s.radius?'aoe':s.k?'single':'buff'});
 }
 return{models,desc,run,onHit,healValue,mods};
})();
