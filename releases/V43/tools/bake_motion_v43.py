from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,cv2,json,base64,io,hashlib,math,os,time
from concurrent.futures import ThreadPoolExecutor,as_completed
cv2.setNumThreads(1)
R=Path('/workspace/RAG');A=R/'assets/motion-v43';E=R/'evidence/motion-v43';BASE=R/'build/Runevale-Angel-Hitbox-V42/index.html'
for d in ['characters','costumes','fx','reviews']:(A/d).mkdir(exist_ok=True)
def parse(s,marker):
 a=s.index(marker)+len(marker);return json.JSONDecoder().raw_decode(s[a:])[0]
def rgba(src):return np.array(Image.open(io.BytesIO(base64.b64decode(src.split(',')[1]))).convert('RGBA'))
def gray(a):
 x=a.astype(np.float32);aa=x[:,:,3]/255;return np.uint8(np.clip((cv2.cvtColor(x[:,:,:3],cv2.COLOR_RGB2GRAY)*.62+96)*aa,0,255))
class Blend:
 def __init__(self):self.cache={}
 def between(self,a,b,t,pixel=True):
  if t<=0:return a.copy()
  if t>=1:return b.copy()
  ka=hashlib.sha1(a.tobytes()).digest();kb=hashlib.sha1(b.tobytes()).digest();key=(ka,kb)
  if key not in self.cache:
   dis=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM);dis.setFinestScale(0);dis.setGradientDescentIterations(16);dis.setVariationalRefinementIterations(4)
   ga,gb=gray(a),gray(b);f=dis.calc(ga,gb,None);z=dis.calc(gb,ga,None);limit=max(a.shape[:2])*.42;f=np.clip(f,-limit,limit);z=np.clip(z,-limit,limit)
   if pixel:
    # Both endpoint sprites share the same sole anchor. Suppress erroneous vertical flow at that anchor.
    yy=np.arange(a.shape[0],dtype=np.float32)[:,None];weight=np.clip((a.shape[0]-16-yy)/18,0,1);f[:,:,1]*=weight;z[:,:,1]*=weight
   self.cache[key]=(f,z)
  f,z=self.cache[key];h,w=a.shape[:2];yy,xx=np.mgrid[:h,:w].astype(np.float32)
  def warp(x,flow,weight):
   y=x.astype(np.float32)/255;pa=np.concatenate([y[:,:,:3]*y[:,:,3:4],y[:,:,3:4]],axis=2)
   return cv2.remap(pa,xx-flow[:,:,0]*weight,yy-flow[:,:,1]*weight,cv2.INTER_NEAREST if pixel else cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
  aa=warp(a,f,t);bb=warp(b,z,1-t);out=aa*(1-t)+bb*t;alpha=out[:,:,3:4];rgb=np.divide(out[:,:,:3],alpha,out=np.zeros_like(out[:,:,:3]),where=alpha>1e-6);
  if pixel:
   # Keep one coherent opaque silhouette; crossfading unaligned limbs creates visible extra feet.
   primary=aa if t<.5 else bb;secondary=bb if t<.5 else aa;alpha=primary[:,:,3:4];own=np.divide(primary[:,:,:3],alpha,out=np.zeros_like(primary[:,:,:3]),where=alpha>1e-6);rgb=np.where((primary[:,:,3:4]>.85)&(secondary[:,:,3:4]>.85),rgb,own)
  out=np.concatenate([rgb,alpha],axis=2);out=np.uint8(np.clip(np.rint(out*255),0,255));out[:,:,3][out[:,:,3]<32]=0;out[:,:,3][out[:,:,3]>=224]=255;out[:,:,:3][out[:,:,3]==0]=0;return out
 def clear(self):self.cache.clear()
def baseline(a,pivot):
 aa=a[:,:,3]>64;yy,xx=np.nonzero(aa)
 if not len(yy):return a
 dy=int(pivot[1])-int(yy.max()+1)
 if abs(dy)<=16 and dy:
  out=np.zeros_like(a)
  if dy>0:out[dy:]=a[:-dy]
  else:out[:dy]=a[-dy:]
  return out
 return a
def footwidth(a,pivot):
 h,w=a.shape[:2];lo=int(pivot[1]-max(10,(pivot[1]-np.nonzero(a[:,:,3]>64)[0].min())*.22));yy,xx=np.nonzero(a[lo:pivot[1],:,3]>64);return int(np.ptp(xx)+1)if len(xx)else 0
def pack(images,width=1024):
 # Deduplicate identical whole frames, trim transparent padding, preserve each original pivot mathematically.
 atlas=Image.new('RGBA',(width,4096));rects=[];keys={};x=y=3;rowh=0
 for im in images:
  if not isinstance(im,Image.Image):im=Image.fromarray(im)
  box=im.getchannel('A').getbbox()or(0,0,1,1);box=(max(0,box[0]-2),max(0,box[1]-2),min(im.width,box[2]+2),min(im.height,box[3]+2));tile=im.crop(box);key=hashlib.sha1(tile.tobytes()+str(tile.size).encode()).hexdigest()
  if key in keys:rect=keys[key]
  else:
   if x+tile.width+3>width:x=3;y+=rowh+3;rowh=0
   assert y+tile.height+3<=4096
   atlas.alpha_composite(tile,(x,y));rect=[x,y,tile.width,tile.height];keys[key]=rect;x+=tile.width+3;rowh=max(rowh,tile.height)
  rects.append((rect,box[:2]))
 height=math.ceil((y+rowh+3)/4)*4;return atlas.crop((0,0,width,height)),rects
DIRS=['S','N','W','E']
def char_task(id,d,kind):
 original=rgba(d['src']);W,H=d.get('frameSize',[192,160]);pivot=d.get('anchor',[96,144]);engine=Blend();frames=[];images=[];review=[];audit=[]
 def src(action,di):
  fs=sorted([f for f in d['frames']if f['action']==action and f['direction']==di],key=lambda f:f['frame']);out=[]
  for f in fs:
   x,y,w,h=f['rect'];out.append(original[y:y+h,x:x+w].copy())
  return out
 def add(action,di,tiles,poses=None):
  for n,tile in enumerate(tiles):
   images.append(tile);frames.append({'action':action,'direction':di,'frame':n,'pivot':pivot.copy(),'sourceSlot':len(images)-1,'pose':poses[n]if poses else action})
 for di in DIRS:
  idle=src('idle',di)[0];walk=src('walk',di);attack=src('attack',di);keys=[]
  for j in range(4):
   if j%2==0:
    # Intermediate full poses shorten the extreme extension; no limb is cut, rigged or warped in the runtime.
    target=walk[(j-1)%4]
    if footwidth(target,pivot)>footwidth(walk[j],pivot):target=idle
    key=baseline(engine.between(walk[j],target,.55),pivot)
   else:key=walk[j]
   keys.append(key)
  newwalk=[]
  for j in range(4):newwalk.extend([keys[j],baseline(engine.between(keys[j],keys[(j+1)%4],.5),pivot)])
  antic,strike=attack[:2]
  newattack=[idle,engine.between(idle,antic,.5),antic,engine.between(antic,strike,.5),strike]+[engine.between(strike,idle,t/7)for t in range(1,7)]+[idle]
  assert len(newattack)==12
  add('idle',di,[idle]);add('walk',di,newwalk,['left-contact','left-release','right-pass','right-load','right-contact','right-release','left-pass','left-load']);add('attack',di,newattack)
  add('start',di,[idle,engine.between(idle,newwalk[0],.5),newwalk[0]])
  for j in range(8):add('stop'+str(j),di,[newwalk[j],engine.between(newwalk[j],idle,.5),idle])
  audit.append({'direction':di,'walkFrames':8,'attackFrames':12,'uniqueWalk':len({hashlib.sha1(a.tobytes()).hexdigest()for a in newwalk}),'uniqueAttack':len({hashlib.sha1(a.tobytes()).hexdigest()for a in newattack}),'oldContactWidths':[footwidth(walk[j],pivot)for j in[0,2]],'newContactWidths':[footwidth(newwalk[j],pivot)for j in[0,4]],'feet':[int(np.nonzero(a[:,:,3]>64)[0].max()+1)for a in newwalk]})
  review.append((di,walk,newwalk,newattack));engine.clear()
 add('down','S',src('down','S'));atlas,rects=pack(images)
 for f,(rect,offset)in zip(frames,rects):f['rect']=rect;f['pivot']=[pivot[0]-offset[0],pivot[1]-offset[1]]
 outpath=A/kind/(id+'.webp');atlas.save(outpath,lossless=True,method=5)
 result={**{k:v for k,v in d.items()if k not in ['src','frames']},'src':'data:image/webp;base64,'+base64.b64encode(outpath.read_bytes()).decode(),'frames':frames,'version':43,'walkCycleDistance':80,'packed':True}
 # Native anchor review: original vs short contact, followed by all eight authored/baked walk poses.
 cv=Image.new('RGBA',(W*10,H*4),'#d9e1dc');draw=ImageDraw.Draw(cv)
 for row,(di,old,walk,attack)in enumerate(review):
  for col,tile in enumerate([old[0],walk[0],*walk]):cv.alpha_composite(Image.fromarray(tile),(col*W,row*H))
  draw.text((4,row*H+4),di+' old / short / 8-frame cycle',fill='black')
 cv.convert('RGB').save(A/'reviews'/(id+'-walk.jpg'),quality=94)
 # Proof actual full frames, not runtime deformations.
 record={'id':id,'kind':kind,'atlas':list(atlas.size),'logicalFrames':len(frames),'bytes':outpath.stat().st_size,'directions':audit}
 return id,result,record,review

def fx_task(id,d):
 original=rgba(d['src']);fc=d['frameCount'];fs=d['frameSize'];engine=Blend();frames=[];factor=4
 originals=[original[:,i*fs:(i+1)*fs]for i in range(fc)]
 for i in range(fc-1):
  frames.append(originals[i])
  for k in range(1,factor):frames.append(engine.between(originals[i],originals[i+1],k/factor,pixel=False))
 frames.append(originals[-1]);atlas,rects=pack(frames);path=A/'fx'/(id+'.webp');atlas.save(path,lossless=True,method=5)
 result={**d,'src':'data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode(),'frameCount':len(frames),'sourceFrameCount':fc,'subframes':factor,'frameRects':[[*rect,*offset]for rect,offset in rects],'packed':True}
 if id in ['sw_bash','mg_fire','ar_double','ac_heal','as_cloud','me_smash']:
  canvas=Image.new('RGBA',(fs*8,fs*4),'#354947')
  for j,f in enumerate(frames[:32]):canvas.alpha_composite(Image.fromarray(f),((j%8)*fs,(j//8)*fs))
  canvas.convert('RGB').save(A/'reviews'/(id+'-fx.jpg'),quality=94)
 return id,result,{'id':id,'oldFrames':fc,'frames':len(frames),'atlas':list(atlas.size),'bytes':path.stat().st_size,'durationUnchanged':True}

def main():
 s=BASE.read_text();chars=parse(s,'window.SHEET_DATA=');costumes=parse(s,'window.COSTUME36_DATA=');skills=parse(s,'window.SKILL_FX_DATA=');casts=parse(s,'window.CAST_FX_DATA=');partial=os.environ.get('MOTION_SAMPLE');data={};audits=[]
 tasks=[(id,d,'characters')for id,d in chars.items()]+[(id,d,'costumes')for id,d in costumes.items()]
 if partial:tasks=[t for t in tasks if t[0]in ['novice','knight','c_phoenix']]
 with ThreadPoolExecutor(max_workers=3)as pool:
  jobs=[pool.submit(char_task,*t)for t in tasks]
  for job in as_completed(jobs):
   id,result,record,review=job.result();data[id]=result;audits.append(record);print('character',id,record['atlas'],record['bytes'],flush=True)
 (A/'characters-embedded.json').write_text(json.dumps({id:d for id,d in data.items()if id in chars},separators=(',',':')));(A/'costumes-embedded.json').write_text(json.dumps({id:d for id,d in data.items()if id in costumes},separators=(',',':')));(A/'characters-audit.json').write_text(json.dumps(audits,indent=2))
 if os.environ.get('BODY_ONLY'):print('DONE body only',len(data),flush=True);return
 allfx={**skills,**casts}
 if partial:allfx={id:d for id,d in allfx.items()if id in ['sw_bash','mg_fire']}
 fx={};audits=[]
 with ThreadPoolExecutor(max_workers=3)as pool:
  jobs=[pool.submit(fx_task,id,d)for id,d in allfx.items()]
  for job in as_completed(jobs):id,result,record=job.result();fx[id]=result;audits.append(record);print('fx',id,record['frames'],flush=True)
 (A/'skills-embedded.json').write_text(json.dumps({id:d for id,d in fx.items()if id in skills},separators=(',',':')));(A/'casts-embedded.json').write_text(json.dumps({id:d for id,d in fx.items()if id in casts},separators=(',',':')));(A/'fx-audit.json').write_text(json.dumps(audits,indent=2));print('DONE',len(data),'bodies',len(fx),'effects')
if __name__=='__main__':main()
