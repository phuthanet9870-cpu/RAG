function choose(u,t,moving){
  const id=COSTUME36_DATA[u.costume]?u.costume:SHEET_DATA[u.cls]?u.cls:'novice';let st=tracks.get(u);
  if(!st){st={x:u.x,y:u.y,time:t,distance:0,dir:direction(u.face??Math.PI/2),travel:false,deadAt:null,walkAt:t,stopAt:null,lastWalk:0};tracks.set(u,st)}
  if(t!==st.time){const dx=u.x-st.x,dy=u.y-st.y,dt=t-st.time,ds=Math.hypot(dx,dy),was=st.travel,valid=dt>0&&Number.isFinite(ds)&&ds<=Math.max(24,dt*600);st.travel=valid&&ds>.005;
   if(st.travel){if(!was){st.distance=0;st.walkAt=t;st.stopAt=null}const a=Math.atan2(dy,dx),centre=st.dir*Math.PI/2,error=Math.abs(Math.atan2(Math.sin(a-centre),Math.cos(a-centre)));if(error>Math.PI/4+.08)st.dir=direction(a);st.distance+=ds}
   else{if(was&&valid)st.stopAt=t;if(!valid)st.stopAt=null;if(Number.isFinite(u.face))st.dir=direction(u.face)}st.x=u.x;st.y=u.y;st.time=t;
  }
  let state=u.dead?'down':u.cast?'cast':u.anim?'attack':st.travel?'walk':st.stopAt!==null&&t-st.stopAt<.12?'stop':'idle';
  if(!u.dead)st.deadAt=null;else if(st.deadAt===null)st.deadAt=t;
  if(state==='attack'||state==='cast')st.dir=direction(u.face??Math.PI/2);
  const dir=state==='down'?'S':dirs[st.dir];let action=state==='cast'?'attack':state,phase=0;
  if(state==='walk'){st.lastWalk=Math.floor((st.distance+1e-8)/10)%8;if(t-st.walkAt<.09){action='start';phase=Math.min(2,Math.floor((t-st.walkAt)/.03))}else phase=st.lastWalk}
  else if(state==='stop'){action='stop'+st.lastWalk;phase=Math.min(2,Math.floor((t-st.stopAt)/.04))}
  else if(state==='attack')phase=Math.max(0,Math.min(11,Math.floor((u.anim.t||0)/Math.max(.001,u.anim.d||.3)*12)));
  else if(state==='cast')phase=2;
  else if(state==='down')phase=t-st.deadAt<.16?0:1;
  const frames=clips[id][dir+'/'+action]||clips[id][dir+'/idle'];phase=Math.min(frames.length-1,phase);
  return{id,state,action,dir,phase,frame:frames[phase],distance:st.distance};
 }
