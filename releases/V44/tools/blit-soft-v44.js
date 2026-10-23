const softBuffers44=new Map();
 function blit(c,id,phase,x,y,o={}){
  id=idOf(id);const d=data[id],im=images[id];if(!d||!im?.naturalWidth)return false;
  const fc=d.sourceFrameCount||d.frameCount||9,fs=d.frameSize||(im.naturalWidth/fc),factor=d.subframes||1,slots=(o.slots||Array.from({length:fc},(_,i)=>i)).filter(i=>i>=0&&i<fc);if(!slots.length)return false;
  const p=Math.min(.999999,Math.max(0,phase))*(o.loop?slots.length:Math.max(0,slots.length-1)),index=Math.min(slots.length-1,Math.floor(p)),next=o.loop?(index+1)%slots.length:Math.min(slots.length-1,index+1),logical=slots[index]+(slots[next]-slots[index])*(p-index);
  const position=Math.max(0,Math.min((d.frameCount||fc)-1,o.nativeSlot??((o.slot??logical)*factor))),i=Math.floor(position),j=Math.min((d.frameCount||fc)-1,i+1),blend=position-i,w=o.width||o.size||92,h=o.height||w,anchor=d.anchor||[fs/2,fs/2];
  c.save();c.translate(x,y);if(o.angle)c.rotate(o.angle);c.globalAlpha=1;c.globalCompositeOperation='source-over';c.imageSmoothingEnabled=true;c.imageSmoothingQuality='high';
  if(blend>1e-5&&i!==j){
   // Interpolate premultiplied RGBA in a transparent buffer. Add weighted frames,
   // never source-over two translucent copies (which would dim the core).
   let buffer=softBuffers44.get(fs);if(!buffer){const canvas=document.createElement('canvas');canvas.width=canvas.height=fs;buffer={canvas,context:canvas.getContext('2d')};softBuffers44.set(fs,buffer)}
   const softFrame44=buffer.canvas,z=buffer.context;z.clearRect(0,0,fs,fs);z.globalCompositeOperation='lighter';z.imageSmoothingEnabled=false;
   for(const [slot,weight]of[[i,1-blend],[j,blend]]){const r=d.frameRects?.[slot]||[slot*fs,0,fs,fs,0,0];z.globalAlpha=weight;z.drawImage(im,r[0],r[1],r[2],r[3],r[4],r[5],r[2],r[3])}
   z.globalAlpha=1;z.globalCompositeOperation='source-over';c.drawImage(softFrame44,-anchor[0]*w/fs,-anchor[1]*h/fs,w,h);
  }else{const r=d.frameRects?.[i]||[i*fs,0,fs,fs,0,0];c.drawImage(im,r[0],r[1],r[2],r[3],w*(r[4]-anchor[0])/fs,h*(r[5]-anchor[1])/fs,r[2]*w/fs,r[3]*h/fs)}
  c.restore();if(c.canvas?.id==='cv'){renderStats.mainDraws++;renderStats.byId[id]=(renderStats.byId[id]||0)+1}return true;
 }
