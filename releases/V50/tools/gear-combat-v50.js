const Gear50=(()=>{
 function equip(a,M){if(a._equipLevel50===P.lv&&a.equip?.weapon)return;
  const held=Object.values(P.equip||{}).filter(i=>ITEM[i?.id]?.t==='wpn'||ITEM[i?.id]?.t==='arm'||ITEM[i?.id]?.t==='acc'),avg=(k)=>held.length?held.reduce((s,i)=>s+(i[k]||0),0)/held.length:0;
  const tier=Math.max(0,TIERS.findLastIndex(t=>t.lv<=P.lv)),baseR=Math.max(Math.floor(P.lv/60),Math.round(avg('r'))),baseRef=Math.max(Math.floor(P.lv/35),Math.round(avg('ref'))),choose=arr=>arr[Math.floor(rnd()*arr.length)];
  function item(pool,weapon=false){if(!pool.length)return null;const wanted=Math.max(0,tier-(rnd()<.25?1:0)),near=pool.filter(b=>b.tier===wanted),b=choose(near.length?near:pool.filter(b=>(b.lv||1)<=P.lv));if(!b)return null;const pr=weapon?P.equip?.weapon:null,r=clamp(Math.max(baseR,pr?.r||0)+Math.floor(rnd()*3)-1,0,4),ref=clamp(Math.max(baseRef,pr?.ref||0)+Math.floor(rnd()*4)-1,0,15);return mkItem(b.id,{rarity:r,ref});}
  a.equip={};const weapon=item(Object.values(ITEM).filter(b=>b.t==='wpn'&&b.wt===M.wt&&(b.lv||1)<=P.lv),true);if(weapon)a.equip.weapon=weapon;
  for(const slot of ['head','mid','low','armor','gloves','garment','pants','shoes','acc1','acc2']){const type=slot.startsWith('acc')?'acc':slot,it=item(Object.values(ITEM).filter(b=>(b.t==='arm'||b.t==='acc')&&b.slot===type&&(b.lv||1)<=P.lv));if(it)a.equip[slot]=it;}
  if(a.cls==='crusader'){const it=item(Object.values(ITEM).filter(b=>b.slot==='shield'&&(b.lv||1)<=P.lv));if(it)a.equip.offhand=it;}
  if(WT[M.wt]?.ranged){const ammo=Object.values(ITEM).filter(b=>b.slot==='ammo');if(ammo.length)a.equip.ammo=mkItem(choose(ammo).id,{n:9999});}
  a.kit50=true;a._equipLevel50=P.lv;a._dvf=-1;
 }
 function weights(a,weights){a.seed50??=Math.floor(rnd()*0x7fffffff)+1;let seed=a.seed50;const out={};let sum=0;for(const k of STAT_KEYS){seed=(Math.imul(seed,1664525)+1013904223)>>>0;out[k]=weights[k]*(.85+seed/4294967296*.3);sum+=out[k];}for(const k of STAT_KEYS)out[k]/=sum;return out;}
 function capture(){if(!P||!W)return;P.mercGear50=Team48.roster.map(a=>({cls:a.cls,level:a._equipLevel50,seed:a.seed50,equip:JSON.parse(JSON.stringify(a.equip))}));}
 const save0=saveGame;saveGame=function(...a){capture();return save0(...a);};
 let viewed=null;
 function show(a){if(a){viewed=a;openWindow('kit50');}}
 TITLEOF.kit50='สเตตัส / อุปกรณ์ส่วนตัว';WIN.kit50={render(){const a=viewed;if(!a)return'<p>เลือกตัวละครก่อน</p>';const d=derive(a);return `<h3>${esc(a.name)} · Lv.${a.lv}</h3><p>ชุดสุ่มส่วนตัวตามอาชีพและเลเวล · อุปกรณ์นี้เป็นของตัวละคร ไม่ใช้ไอเทมจากกระเป๋าผู้เล่น</p><p>HP ${fmt(d.maxHP)} · SP ${fmt(d.maxSP)} · ATK ${fmt(d.ATK)} · MATK ${fmt(d.MATK)} · DEF ${fmt(d.DEF)} · MDEF ${fmt(d.MDEF)}</p><p>${STAT_KEYS.map(k=>k+' '+d.s[k]).join(' · ')}</p><div class="list">${Object.entries(a.equip).map(([slot,it])=>`<div class="li">${im(it.id)}<div style="flex:1"><small>${SLOT_N[slot]||slot}</small><b style="display:block;color:${['#655d4d','#3d7b38','#316eab','#80569a','#a65e25'][it.r||0]}">${esc(itemName(it))}</b><small>${(it.opts||[]).map(optLabel).join(' · ')}</small></div></div>`).join('')}</div>${ADM.ok?'<button data-act="gmReroll50">GM · สุ่มอุปกรณ์ชุดใหม่</button>':''}`;}};
 ACT.kit50=el=>show(Team48.roster[+el.dataset.a]);ACT.gmReroll50=()=>{if(!ADM.ok||!viewed)return;const hp=viewed.hp/derive(viewed).maxHP,sp=viewed.sp/derive(viewed).maxSP;viewed._equipLevel50=-1;syncAllyLevel(viewed);viewed.hp=derive(viewed).maxHP*hp;viewed.sp=derive(viewed).maxSP*sp;capture();saveSoon();renderWin();};
 TITLEOF.gear50='GM · อุปกรณ์และนักสู้ V50';WIN.gear50={render(){if(!ADM.ok)return'<p>เข้าสู่ระบบ GM ก่อน</p>';return `<button data-act="gmGear50Arena">เลือกโหมด / เข้าได้แม้ทีมไม่ครบ</button><p>อุปกรณ์และค่าสเตตัสของนักสู้จริงในปัจจุบัน</p>${[...Team48.roster,...W.mons.filter(m=>m.fighter48)].map((a,i)=>`<div class="li"><span style="flex:1">${esc(a.name)} · Lv.${a.lv}</span><button data-act="gmGear50View" data-a="${i}">ดู / สุ่มชุดใหม่</button></div>`).join('')}`;}};
 ACT.gmGear50=()=>{if(ADM.ok)openWindow('gear50');};ACT.gmGear50Arena=()=>{if(ADM.ok)openWindow('arena');};ACT.gmGear50View=el=>{if(ADM.ok)show([...Team48.roster,...W.mons.filter(m=>m.fighter48)][+el.dataset.a]);};
 const oldAdmin=WIN.admin.render;WIN.admin.render=function(...a){return oldAdmin.apply(this,a)+(ADM.ok?'<button data-act="gmGear50">อุปกรณ์สุ่ม / สเตตัสนักสู้ / ทีมไม่ครบ V50</button>':'');};
 return{version:50,equip,weights,capture,show};
})();
