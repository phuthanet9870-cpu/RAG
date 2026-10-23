function blit(c,id,phase,x,y,o={}){
  id=idOf(id);const d=data[id],im=images[id];if(!d||!im?.naturalWidth)return false;
  const fc=d.sourceFrameCount||d.frameCount||9,fs=d.frameSize||(im.naturalWidth/fc),factor=d.subframes||1,slots=(o.slots||Array.from({length:fc},(_,i)=>i)).filter(i=>i>=0&&i<fc);if(!slots.length)return false;
  const p=Math.min(.999999,Math.max(0,phase))*(o.loop?slots.length:Math.max(0,slots.length-1)),index=Math.min(slots.length-1,Math.floor(p)),next=o.loop?(index+1)%slots.length:Math.min(slots.length-1,index+1),logical=slots[index]+(slots[next]-slots[index])*(p-index);
  const i=Math.max(0,Math.min((d.frameCount||fc)-1,o.nativeSlot??Math.round((o.slot??logical)*factor))),w=o.width||o.size||92,h=o.height||w;
  const anchor=d.anchor||[fs/2,fs/2],r=d.frameRects?.[i]||[i*fs,0,fs,fs,0,0],dx=w*(r[4]-anchor[0])/fs,dy=h*(r[5]-anchor[1])/fs;
  c.save();c.translate(x,y);if(o.angle)c.rotate(o.angle);c.globalAlpha=1;c.globalCompositeOperation='source-over';c.imageSmoothingEnabled=false;c.drawImage(im,r[0],r[1],r[2],r[3],dx,dy,r[2]*w/fs,r[3]*h/fs);c.restore();
  if(c.canvas?.id==='cv'){renderStats.mainDraws++;renderStats.byId[id]=(renderStats.byId[id]||0)+1}return true;
 }
