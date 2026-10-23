from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,cv2,json,base64,io,hashlib,sys
sys.path.insert(0,str(Path(__file__).parent))
from bake_motion_v43 import pack,Blend
R=Path('/workspace/RAG');A=R/'assets/low-walk-v45';A.mkdir(exist_ok=True);(A/'costumes').mkdir(exist_ok=True);(A/'reviews').mkdir(exist_ok=True)
data=json.loads((R/'assets/motion-v43/costumes-embedded.json').read_text());rows=[];results={};audits=[]
def unpack(d,im,f):
 tile=Image.new('RGBA',tuple(d.get('frameSize',[128,144])));x,y,w,h=f['rect'];px,py=f['pivot'];a=d.get('anchor',[64,128]);tile.alpha_composite(im.crop((x,y,x+w,y+h)),(a[0]-px,a[1]-py));return np.array(tile)
def lowwalk(idle,di,pivot):
 h,w=idle.shape[:2];yy,xx=np.mgrid[:h,:w].astype(np.float32);bottom=pivot[1]-1
 # Author grounded leg motion offline from the shipped idle art. No body part
 # transform or rig is shipped to the game, only transparent whole-frame images.
 foot=(idle[:,:,3]>64)&(yy>=bottom-10);xs=np.where(foot)[1];xmin,xmax=int(xs.min()),int(xs.max());split=(xmin+xmax)/2
 # Keep the cape, hands, face and chest unchanged. A three-pixel hip overlap
 # holds the legs attached; only pants/boots below this line articulate.
 hip=bottom-29;left=max(xmin-3,0);right=min(xmax+4,w);region=(yy>=hip)&(xx>=left)&(xx<right);masks=[region&(xx<split),region&(xx>=split)]
 layers=[]
 for mask in masks:
  layer=idle.copy();layer[~mask]=0;ys=np.where(layer[:,:,3]>64)[0];end=int(ys.max())if len(ys)else bottom
  layers.append((layer,end))
 static=idle.copy();static[region]=0;frames=[];legaudit=[]
 for k in range(8):
  phase=k*np.pi/4;legs=[];infos=[]
  for j,(layer,end)in enumerate(layers):
   stride=np.cos(phase+j*np.pi);lift=2.0*max(0,np.sin(phase+j*np.pi)*(1 if di in ['W','N']else -1));depth=bottom-hip;weight=np.clip((yy-hip)/depth,0,1)
   # Stretch the original rear foot to the same ground plane once, then use a
   # two-pixel swing clearance. This is NOT the previous raised-knee pose.
   correction=bottom-end;motionx=(5.0 if di in ['E','W']else 1.25)*stride;motiony=0
   srcx=xx-motionx*weight**1.5;srcy=hip+(yy-hip+lift*weight**2-motiony*weight**2)*(max(1,end-hip)/depth)
   moved=cv2.remap(layer,srcx.astype(np.float32),srcy.astype(np.float32),cv2.INTER_NEAREST,borderMode=cv2.BORDER_CONSTANT);legs.append(moved)
   ys2=np.where(moved[:,:,3]>64)[0];infos.append({'leg':j,'sole':int(ys2.max()+1)if len(ys2)else None,'lift':round(lift,3),'stride':round(motionx,3)})
  cv=Image.new('RGBA',(w,h))
  # Far leg before near leg; use lower first for front/back perspective.
  order=[1,0]if di=='E'else[0,1]
  for j in order:cv.alpha_composite(Image.fromarray(legs[j]))
  cv.alpha_composite(Image.fromarray(static));a=np.array(cv);a[a[:,:,3]==0]=0;frames.append(a);legaudit.append(infos)
 return frames,legaudit,{'hip':hip,'split':split,'bounds':[left,right]}
for id,d in data.items():
 im=Image.open(R/'assets/motion-v43/costumes'/(id+'.webp')).convert('RGBA');pivot=d.get('anchor',[64,128]);allframes=[];frames=[];proof=[];engine=Blend();audit={'id':id,'directions':{}}
 old={}
 for f in d['frames']:old[(f['direction'],f['action'],f['frame'])]=unpack(d,im,f)
 replacements={}
 for di in ['S','N','W','E']:
  idle=old[di,'idle',0];walk,legs,roi=lowwalk(idle,di,pivot)
  for k,tile in enumerate(walk):replacements[(di,'walk',k)]=tile
  replacements[(di,'start',0)]=idle;replacements[(di,'start',1)]=engine.between(idle,walk[0],.5);replacements[(di,'start',2)]=walk[0]
  for k in range(8):
   replacements[(di,'stop'+str(k),0)]=walk[k];replacements[(di,'stop'+str(k),1)]=engine.between(walk[k],idle,.5);replacements[(di,'stop'+str(k),2)]=idle
  proof.append((di,[old[di,'walk',k]for k in range(8)],walk));audit['directions'][di]={'legs':legs,'roi':roi,'unique':len({hashlib.sha1(x.tobytes()).hexdigest()for x in walk}),'baseline':[int(np.where(x[:,:,3]>64)[0].max()+1)for x in walk]};engine.clear()
 for f in d['frames']:
  k=(f['direction'],f['action'],f['frame']);allframes.append(replacements.get(k,old[k]));frames.append({a:b for a,b in f.items()if a not in ['rect','pivot']})
 atlas,rects=pack(allframes)
 for f,(rect,offset)in zip(frames,rects):f['rect']=rect;f['pivot']=[pivot[0]-offset[0],pivot[1]-offset[1]]
 p=A/'costumes'/(id+'.webp');atlas.save(p,lossless=True,method=5);results[id]={**d,'src':'data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode(),'frames':frames,'version':45};audits.append(audit)
 cv=Image.new('RGBA',(128*8,144*8),'#e0e3df');dr=ImageDraw.Draw(cv)
 for i,(di,oldwalk,newwalk)in enumerate(proof):
  for j in range(8):cv.alpha_composite(Image.fromarray(oldwalk[j]),(j*128,i*288));cv.alpha_composite(Image.fromarray(newwalk[j]),(j*128,i*288+144))
  dr.text((2,i*288+2),di+' OLD',fill='black');dr.text((2,i*288+146),di+' LOW WALK',fill='black')
 cv.convert('RGB').save(A/'reviews'/(id+'.jpg'),quality=95);print(id,audit['directions']['E']['roi'],flush=True)
 if '--sample'in sys.argv:break
(A/'costumes-embedded.json').write_text(json.dumps(results,separators=(',',':')));(A/'audit.json').write_text(json.dumps(audits,indent=2))
