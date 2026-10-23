window.SkillEffects=(()=>{
 const data={...window.SKILL_FX_DATA,...window.CAST_FX_DATA},library=window.VFX46_LIBRARY,atlasImages={},images={},events=[],stats={},learned=new WeakMap(),stack=[];let current=null,sequence=0;
 const renderStats={mainDraws:0,byId:{}};
 const alias={hn_mine_x:'hn_mine',hn_mine_t:'hn_mine',hn_ankle_t:'hn_ankle',hn_clay_t:'hn_clay',hn_clay_z:'hn_clay',al_bomb_z:'al_bomb',sg_seal_z:'sg_seal',st_poison:'as_cloud'};
 const idOf=id=>data[id]?id:alias[id];
 const body=u=>u.y-(u.isMon&&window.MonsterSheets?MonsterSheets.height(u)*.5:34);
 function log(id,phase,extra={}){if(!data[id])return;const s=stats[id]||(stats[id]={});s[phase]=(s[phase]||0)+1;events.push({id,phase,at:typeof clock==='number'?clock:0,...extra});if(events.length>4096)events.shift()}
 function blit(c,id,phase,x,y,o={}){
  id=idOf(id);const d=data[id];if(!d)return false;const family=o.sprite||d.family,a=library[family],im=atlasImages[family];if(!a||!im?.naturalWidth)return false;
  let position=Math.max(0,Math.min(.999999,phase))*(a.frameCount-1);
  if(o.slots?.length){const p=Math.max(0,Math.min(.999999,phase))*(o.loop?o.slots.length:o.slots.length-1),i=Math.floor(p),j=o.loop?(i+1)%o.slots.length:Math.min(o.slots.length-1,i+1);position=(o.slots[i]+(o.slots[j]-o.slots[i])*(p-i))*a.subframes}
  const k=Math.max(0,Math.min(a.frameCount-1,Math.round(o.nativeSlot??(o.slot!=null?o.slot*a.subframes:position)))),r=a.frameRects[k],w=o.width||o.size||84,h=o.height||w,anchor=o.anchor||a.anchor;
  c.save();c.translate(x,y);if(o.angle)c.rotate(o.angle);c.globalAlpha=o.alpha??1;c.globalCompositeOperation='source-over';c.imageSmoothingEnabled=true;c.imageSmoothingQuality='high';c.drawImage(im,r[0],r[1],r[2],r[3],(r[4]-anchor[0])*w/128,(r[5]-anchor[1])*h/128,r[2]*w/128,r[3]*h/128);c.restore();
  if(c.canvas?.id==='cv'){renderStats.mainDraws++;renderStats.byId[id]=(renderStats.byId[id]||0)+1}return true;
 }
 function emit(id,x,y,o={}){id=idOf(id);if(!data[id]||typeof W==='undefined'||!W?.fx||W.fx.length>=500)return null;const f={kind:'skillV19',id,x,y,t:-(o.delay||0),life:o.life||data[id].duration||.6,...o};delete f.delay;f.animationDuration=f.life;W.fx.push(f);return f}
 function projectile(id,from,target,o={}){const d=data[idOf(id)];if(!d||!target)return null;const sx=from.x,sy=body(from),tx=target.x,ty=body(target),life=o.life||Math.max(.08,Math.min(.28,Math.hypot(tx-sx,ty-sy)/950));log(d.id,'flight',{target:target.id||target.name,delay:o.delay||0,travel:life,index:o.index??0});return emit(id,sx,sy,{projectile:true,target,tx,ty,size:36,life,...o})}
 function draw(c,f){if(f.t<0)return false;const d=data[f.id];if(!d)return false;let p=Math.max(0,Math.min(.999,f.t/(f.animationDuration||f.life))),x=f.x,y=f.y,o={...f};
  if(f.follow&&f.target){x=f.target.x;y=library[f.sprite||d.family]?.grounded?f.target.y:body(f.target)}
  if(f.projectile){const tx=f.target?.x??f.tx,ty=f.target?body(f.target):f.ty;
   if(f.hover){const travel=f.travel,span=f.span,back=f.t>travel+span;if(f.t<travel){const q=f.t/travel;x=f.x+(tx-f.x)*q;y=f.y+(ty-f.y)*q}else if(!back){x=tx+Math.sin((f.t-travel)*25)*10;y=ty+Math.cos((f.t-travel)*25)*5}else{const q=Math.min(1,(f.t-travel-span)/travel);x=tx+(f.x-tx)*q;y=ty+(f.y-ty)*q}o.angle=Math.atan2(ty-f.y,tx-f.x);p=.25+(f.t*3%1)*.4}
   else if(f.drop){x=tx;y=ty-150*(1-p);o.angle=d.family==='arrow'?Math.PI/2:0;p=.15+.6*p}
   else{x=f.x+(tx-f.x)*p;y=f.y+(ty-f.y)*p-(f.arc||0)*Math.sin(p*Math.PI);o.angle=d.family==='meteor'?0:Math.atan2(ty-f.y,tx-f.x);if(f.spin)o.angle+=p*Math.PI*2;p=d.family==='meteor'?.08+.28*p:.18+.48*p}
  }
  if(f.orbit){const a=p*Math.PI*2+(f.orbitOffset||0),r=f.orbitR||28;x=f.x+Math.cos(a)*r;y=f.y+Math.sin(a)*r*.6;o.angle=a+Math.PI/2;p=.2+p*.4}
  if(f.link){const sx=f.src.x,sy=body(f.src),tx=f.target.x,ty=body(f.target);x=(sx+tx)/2;y=(sy+ty)/2;o.width=18;o.height=Math.hypot(tx-sx,ty-sy)*1.2;o.anchor=[64,64];o.angle=Math.atan2(ty-sy,tx-sx)+Math.PI/2;o.sprite='holybeam'}
  if(f.cone){const a=f.angle||0,len=f.r||6*T;x=f.x+Math.cos(a)*len*.12;y=f.y-24+Math.sin(a)*len*.12;o.width=len;o.height=2*len*Math.sin(f.halfAngle||35*Math.PI/180);o.anchor=[8,64];o.angle=a}
  return blit(c,f.id,p,x,y,o);
 }
 function begin(c){stack.push(current);current=c;c._v46={cast:++sequence,origin:{x:c.src.x,y:c.src.y},schedules:[],visuals:0,recipients:[],beforeStolen:!!c.t?.stolen};c.v8Origin=c._v46.origin;c.v8Duration=data[c.s.id]?.duration||.6;c.v8Hit=false;c.v8Heal=false}
 function end(){current=stack.pop()||null}
 function buff(u){if(current?._v46&&!current._v46.recipients.includes(u))current._v46.recipients.push(u)}
 function timeline(c,o,t){const d=data[c?.s?.id];if(!d||!t)return 0;const v=c._v46||(c._v46={cast:++sequence,origin:{x:c.src.x,y:c.src.y},schedules:[],visuals:0,recipients:[],beforeStolen:!!c.t?.stolen});const n=o.hits||1,start=o.start||0,delay=o.delay||.06;v.schedules.push({target:t.id,hits:n,start,delay});log(d.id,'timeline',{hits:n,start,delay,target:t.id,cast:v.cast});
  if(['projectile','drop'].includes(d.pattern)){
   const travel=d.pattern==='drop'?.14:Math.max(.08,Math.min(.28,Math.hypot(t.x-c.src.x,t.y-c.src.y)/950));
   for(let i=0;i<n;i++){projectile(d.id,c.src,t,{delay:start+i*delay,life:travel,drop:d.pattern==='drop',size:d.pattern==='drop'?70:d.family==='arrow'?48:d.family==='acidflask'?30:36,arc:d.family==='acidflask'?28:0,spin:d.family==='acidflask',index:i});v.visuals++}
   return travel;
  }
  if(['boomerang','falcon'].includes(d.pattern)){
   if(!v.visuals){const travel=.16,span=Math.max(.05,(n-1)*delay);projectile(d.id,c.src,t,{delay:start,life:travel*2+span,hover:true,travel,span,size:d.pattern==='falcon'?64:50});v.visuals++}return .16;
  }
  if(d.pattern==='strike')for(let i=0;i<n;i++){const a=Math.atan2(t.y-c.src.y,t.x-c.src.x);emit(d.id,t.x,library[d.family].grounded?t.y:body(t),{size:d.id==='mo_asura'?130:78,delay:start+i*delay,angle:['slash','pierce','backstab','fist'].includes(d.family)?a+(i%2?.18:-.18):0,life:.3});log(d.id,'strike',{index:i,delay:start+i*delay})}
  return 0;
 }
 function impact(t,info,u){if(info.src==='basic'){const family=u.wt==='knuckle'?'fist':u.wt==='dagger'||u.wt==='katar'?'backstab':u.wt==='bow'?'pierce':u.wt==='staff'?'spirit':'slash';return!!emit('sw_bash',t.x,body(t),{sprite:family,size:40,angle:Math.atan2(t.y-u.y,t.x-u.x),life:.25})}const id=idOf(info.src),d=data[id];if(!d)return false;log(id,'hit',{target:t.id||null,index:info.idx});if(current?.s?.id===id)current.v8Hit=true;
  const angle=Math.atan2(t.y-u.y,t.x-u.x),family=d.family==='heal'?'holycross':d.impact||(['projectile','falcon','strike'].includes(d.pattern)?'pierce':d.family);emit(id,t.x,library[family]?.grounded?t.y:body(t),{sprite:family,size:d.pattern==='strike'?(['mo_asura','mo_palm'].includes(id)?118:76):['area','rain','meteor','cone','ground'].includes(d.pattern)?40:49,angle:['slash','pierce','backstab','fist','poisonclaw'].includes(family)?angle:0,life:.28+(d.pattern==='strike'?.12:0)});if(d.secondary)emit(id,t.x,t.y,{sprite:d.secondary,size:64,life:.55});return true;
 }
 function center(c,d){return c.s.tgt==='self'?c.src:c.s.tgt==='ground'?{x:c.x??c.t?.x??c.src.x,y:c.y??c.t?.y??c.src.y}:c.t||{x:c.x??c.src.x,y:c.y??c.src.y}}
 const circleId=d=>d.element===3?'cast_fire':d.element===1?'cast_ice':d.element===6||d.cls==='priest'||d.cls==='acolyte'?'cast_holy':'cast_arcane';
 function areaCast(c,d){const p=center(c,d),r=(typeof c.s.r==='number'?c.s.r:2)*T,schedule=c._v46?.schedules?.[0],n=schedule?.hits||1,gap=schedule?.delay||.12,start=schedule?.start||0;
  if(d.pattern==='cone'){emit(d.id,c.src.x,c.src.y,{cone:true,r:6*T,halfAngle:35*Math.PI/180,angle:c.t?Math.atan2(c.t.y-c.src.y,c.t.x-c.src.x):c.src.face||0,life:.85,layer:'ground'});return}
  emit(d.id,p.x,p.y,{sprite:circleId(d),size:r*2,life:Math.min(2,.55+(n-1)*gap),layer:'ground'});
  if(d.pattern==='rain'){for(let i=0;i<12;i++){const a=i*2.39996,rr=r*Math.sqrt((i+.5)/12),x=p.x+Math.cos(a)*rr,y=p.y+Math.sin(a)*rr;emit(d.id,x-35,y-170,{projectile:true,tx:x,ty:y,drop:true,delay:start+i*.024,life:.22,size:48,angle:Math.PI/2,layer:'ground'})}return}
  for(let i=0;i<n;i++){const a=i*2.39996,rr=n===1?0:r*.4,x=p.x+Math.cos(a)*rr,y=p.y+Math.sin(a)*rr;
   if(d.pattern==='meteor'){emit(d.id,x-60,y-190,{projectile:true,tx:x,ty:y,delay:Math.max(0,start-.25)+i*gap,life:.25,size:90,layer:'ground',sprite:'meteor'});emit(d.id,x,y,{sprite:'explosion',size:r*.9,delay:start+i*gap,life:.45,layer:'ground'});log(d.id,'meteor',{index:i,delay:start+i*gap})}
   else emit(d.id,x,y,{size:d.family==='lightning'?r*.65:Math.max(78,Math.min(r*1.4,260)),delay:start+i*gap,life:.42,layer:'ground'})
  }
 }
 function cast(c){const d=data[c.s.id];if(!d||d.type==='passive')return false;log(d.id,'cast',{level:c.lv,cast:c._v46?.cast});const src=c.src,ally=c.ally||src,p=c.t||src;switch(d.pattern){
  case'projectile':case'drop':case'boomerang':case'falcon':return true;
  case'potion':if(c.v8Heal)return true;return false;
  case'heal':if(c.v8Heal||c.t?.isMon)return true;emit(d.id,ally.x,ally.y,{size:76,life:.6});return true;
  case'area':case'meteor':case'rain':case'cone':areaCast(c,d);return true;
  case'ground':return true;
  case'trap':return true;
  case'teleport':{let o=c._v46?.origin||src;emit(d.id,o.x,o.y,{size:70,life:.4});emit(d.id,src.x,src.y,{size:75,life:.5});return true}
  case'strike':if(!c._v46?.schedules?.length&&c.t)emit(d.id,c.t.x,body(c.t),{size:76,life:.45});if(['kn_charge','ro_back'].includes(d.id)){let o=c._v46?.origin||src;emit(d.id,o.x,o.y,{sprite:d.id==='kn_charge'?'wind':'shadow',size:66,life:.4})}return true;
  case'party':for(const a of c._v46?.recipients||[]){emit(d.id,a.x,library[d.family].grounded?a.y:body(a),{target:a,follow:true,size:73,life:.65});if(d.id==='cr_oath'&&a!==src)emit(d.id,src.x,body(src),{link:true,src,target:a,life:.6})}return true;
  case'enchant':emit(d.id,ally.x,body(ally),{size:60,life:.6,target:ally,follow:true});return true;
  case'shield':emit(d.id,ally.x,ally.y,{target:ally,follow:true,size:86,life:.55});return true;
  case'revive':emit(d.id,ally.x,ally.y,{size:110,life:1});emit(d.id,ally.x,ally.y,{sprite:'holybeam',size:100,life:1});return true;
  case'debuff':{const stolen=d.id==='th_steal'&&p.stolen&&!c._v46?.beforeStolen;emit(d.id,p.x,body(p),{sprite:d.id==='th_steal'&&!stolen?'shadow':d.family,size:60,life:.5});if(stolen)projectile(d.id,p,src,{sprite:'coins',size:30,life:.3});return true;}
  case'orbit':if(d.id==='hn_detect'){const x=c.x??src.x,y=c.y??src.y;emit(d.id,x,y-30,{orbit:true,orbitR:6*T,size:65,life:1.2});emit(d.id,x,y,{sprite:'cast_arcane',size:12*T,life:1.2,layer:'ground'})}else emit(d.id,src.x,src.y,{sprite:d.id==='mg_sight'?'cast_fire':'cast_holy',size:76,life:.55});return true;
  case'taunt':emit(d.id,src.x,src.y,{size:95,life:.55});return true;
  default:emit(d.id,src.x,library[d.family].grounded?src.y:body(src),{size:70,life:.55,target:src,follow:true});return true;
 }}
 function heal(u,value,src){const c=current,id=c?.s?.id;if(!c||!data[id])return;c.v8Heal=true;log(id,'heal');if(id==='al_potion'){projectile(id,src||c.src,u,{sprite:'healflask',size:30,arc:24,spin:true,life:.22});emit(id,u.x,u.y,{sprite:'heal',size:80,life:.55,delay:.22})}else emit(id,u.x,u.y,{sprite:'heal',size:80,life:.55})}
 function learn(u,id){if(data[id]?.type!=='passive')return false;log(id,'learn');return!!emit(id,u.x,body(u),{size:44,life:.4})}
 function observe(u){if(!u.skills)return;let old=learned.get(u);if(!old){learned.set(u,{...u.skills});return}for(const[id,lv]of Object.entries(u.skills)){if(data[id]?.type==='passive'&&lv>(old[id]||0))learn(u,id);old[id]=lv}}
 function passive(u,id,t){if(!data[id]||data[id].type!=='passive'||!u.skills?.[id])return false;log(id,'proc');if(['mo_triple','th_double','hn_auto'].includes(id))return true;return!!emit(id,t?.x??u.x,t?body(t):body(u),{size:44,life:.3})}
 function basicHits(c,o,t){if(c.s)return;if(o.hits===3&&c.src.skills?.mo_triple)passive(c.src,'mo_triple',t);else if(o.hits===2&&c.src.wt==='dagger')passive(c.src,'th_double',t)}
 function regen(u,hp,sp){if(hp>0&&u.skills?.sw_regen)passive(u,'sw_regen');if(sp>0&&u.skills?.mg_sp)passive(u,'mg_sp')}
 function drawBuffs(c,u,t){observe(u);if(u.dead)return;if(u.buffs?.mg_sight){for(let i=0;i<3;i++){const a=t*2+i*Math.PI*2/3;blit(c,'mg_sight',.3+(t%1)*.2,u.x+Math.cos(a)*31,body(u)+Math.sin(a)*12,{size:22,angle:a+Math.PI/2})}}if(u.buffs?.mo_orbs){const n=u.buffs.mo_orbs.orbs||1;for(let i=0;i<n;i++){const a=t+i*Math.PI*2/n;blit(c,'mo_orbs',.28,u.x+Math.cos(a)*29,body(u)+Math.sin(a)*12,{sprite:'spirit',size:17,anchor:[64,64]})}}}
 const zoneFallback={pneuma:'wz_pneuma',quag:'wz_quag',blizzard:'wz_storm',magnus:'pr_magnus',sanct:'pr_sanct',safety:'pr_safety',seal:'sg_seal',firebomb:'al_bomb',burn:'hn_clay',water:'sg_water',toxicQueenZone:'tq_zone'};
 function ground(c,g,t){const id=idOf(g.sk)||zoneFallback[g.kind],d=data[id];if(!d)return false;const age=g.max!=null?g.max-g.t:t;const phase=(age*.9)%1;
  blit(c,id,(age*.5)%1,g.x,g.y,{sprite:circleId(d),size:g.r*2});
  if(['wz_pneuma','pr_pneuma','sg_seal','pr_safety'].includes(id))return blit(c,id,.18+phase*.42,g.x,g.y,{size:g.r*2});
  const n=g.r>140?5:3;for(let i=0;i<n;i++){const a=i*2.39996,rr=i?g.r*.45:0;blit(c,id,.18+((phase+i/n)%1)*.5,g.x+Math.cos(a)*rr,g.y+Math.sin(a)*rr*.65,{size:Math.min(150,g.r*1.1),sprite:g.kind==='burn'?'firepillar':d.family})}return true;
 }
 function trap(c,tr,t,mine){const id=tr.c?.s?.id||({mine:'hn_mine',ankle:'hn_ankle',clay:'hn_clay'}[tr.kind]);return blit(c,id,.16,tr.x,tr.y,{sprite:'snare',size:40,alpha:mine?1:.65})}
 function trapTriggered(tr){const id=tr.c?.s?.id||({mine:'hn_mine',ankle:'hn_ankle',clay:'hn_clay'}[tr.kind]);log(id,'trigger');return emit(id,tr.x,tr.y,{size:Math.max(70,tr.r*1.6),life:.55,layer:'ground'})}
 function drawGrounds(c,t){for(const g of W.grounds)ground(c,g,t);for(const tr of W.traps)trap(c,tr,t,tr.owner===P);for(const f of W.fx)if(f.kind==='skillV19'&&f.layer==='ground')draw(c,f)}
 function legacy(kind,x,y,o={},curId){if(kind==='monsterSheetDeath')return false;if(['castStart','trapSet','falcon','pickup'].includes(kind))return true;if(kind==='flask'&&o.acid)return true;if(current&&curId)return true;
  if(kind==='arrow'&&o.t){for(let i=0;i<(o.n||1);i++)projectile('ar_double',{x,y},o.t,{delay:i*.08,life:o.life||.22,size:42});return true}
  if(kind==='mbolt'&&o.t){projectile(o.el===1?'mg_cold':o.el===4?'mg_light':'mg_fire',{x,y},o.t,{life:o.life||.22,size:30});return true}
  if(kind==='flask'){projectile('al_acid',{x,y},{x:o.tx,y:o.ty},{sprite:'acidflask',size:27,life:.24,arc:28,spin:true});return true}
  if(kind==='swing'||kind==='slash'){const sprite=o.wt==='knuckle'?'fist':o.wt==='dagger'||o.wt==='katar'?'backstab':'slash';emit('sw_bash',x,y-24,{sprite,size:58,angle:o.a||0,life:.28});return true}
  const map={hit:'sw_bash',swing:'sw_bash',slash:'as_sonic',block:'cr_guard',buffUp:'ac_bless',heal:'ac_heal',revive:'pr_resu',nova:'mg_wave',impact:'bs_hammer',dash:'th_back',falconCircle:'hn_detect',coins:'me_wit',death:'as_cloak',monDeath:'as_cloak',link:'cr_oath'};const id=map[kind];if(!id)return false;emit(id,x,library[data[id].family].grounded?y:y-22,{size:kind==='impact'?Math.max(70,Math.min(320,(o.r||40)*1.6)):kind==='nova'?110:kind==='hit'?38:65,life:.42,angle:['hit','swing','slash','dash'].includes(kind)?o.a||0:0});return true;
 }
 function depth(f){if(f.target&&f.follow)return f.target.y;if(f.projectile){const p=Math.max(0,Math.min(1,f.t/f.life)),ty=f.target?body(f.target):f.ty;return f.y+(ty-f.y)*p+34}return f.y+(data[f.id]?.grounded?0:34)}
 function compat(id,x,y,size,o={}){return emit(id,x,y,{size:size||72,...o})}
 function status(c,m,t,kind){const id=({poison:'as_cloud',freeze:'mg_frost',root:'hn_ankle',reflect:'cr_reflect',enrage:'al_berserk'})[kind];return id?blit(c,id,.2+(t%1)*.4,0,kind==='root'?0:-(m.r||14)*.6,{size:Math.max(28,(m.r||14)*2.6),alpha:kind==='freeze'?.75:.55}):false}
 function castId(id){return circleId(data[id]||{})}
 function casting(c,u,t){if(!u.cast?.c?.s||u.dead)return false;const id=castId(u.cast.c.s.id),progress=Math.max(0,Math.min(.999,u.cast.t/u.cast.total));return blit(c,id,.14+progress*.5,u.x,u.y,{size:94})}
 async function preload(){await SafeImages.group(library,atlasImages,'skill-v46');for(const[id,d]of Object.entries(data))images[id]=atlasImages[d.family]}
 return{version:46,depth,renderStats,casting,castId,blit,emit,draw,begin,end,buff,timeline,cast,projectile,impact,heal,learn,observe,passive,basicHits,regen,drawBuffs,ground,trap,trapTriggered,drawGrounds,legacy,compat,status,preload,images,atlasImages,library,data,events,stats};
})();
