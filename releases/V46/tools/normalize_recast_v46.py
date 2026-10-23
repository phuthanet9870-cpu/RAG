from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,cv2,json,base64,sys,hashlib
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).parent));from bake_motion_v43 import Blend,pack
R=Path('/workspace/RAG');A=R/'assets/recast-v46';(A/'atlases').mkdir(exist_ok=True);(A/'reviews').mkdir(exist_ok=True)
sheets={
'elemental':('607eeea7-36ea-4366-be3c-b1fa10f3a1d3',['fireball','icebolt','lightning','spirit','firenova','firepillar','meteor','icespikes','iceburst','blizzard','tornado','earthspikes']),
'combat':('d13c54f4-a694-4a8f-8ba9-46a69913f5ba',['slash','pierce','crossslash','arrow','shock','block','backstab','poisonclaw','poisoncloud','vines','explosion','snare']),
'support':('ce19336b-54d7-4159-be8b-47fc5eac170d',['heal','holycross','holybeam','shield','cast_fire','cast_ice','cast_holy','cast_arcane','buff','notes','coins','orbs']),
'special':('da722ac2-a414-44bb-a90a-4f2a154a95ac',['acidflask','healflask','falcon','boomerang','mud','water','wind','earth','teleport','dragonfire','shadow','fist'])}
flying={'fireball','icebolt','spirit','pierce','arrow','backstab','acidflask','healflask','falcon','boomerang','dragonfire','fist'}
grounded={'firenova','firepillar','meteor','icespikes','blizzard','tornado','earthspikes','shock','vines','snare','heal','holybeam','shield','cast_fire','cast_ice','cast_holy','cast_arcane','buff','coins','mud','water','wind','earth','teleport','poisoncloud'}
tasks=[];sources={}
for name,(key,ids)in sheets.items():
 path=next(Path('/workspace/generated_images').glob('exec-'+key+'*.png'));src=np.array(Image.open(path).convert('RGBA'));alpha=src[:,:,3];density=(alpha>150).sum(1).astype(float);density=np.convolve(density,np.ones(7)/7,'same');bounds=[0]
 bounds={'elemental':[0,122,220,363,460,568,704,829,954,1083,1215,1373,1536],'combat':[0,128,253,376,492,590,735,849,985,1122,1263,1398,1536],'support':[0,128,252,384,512,640,768,898,1024,1152,1280,1408,1536],'special':[0,128,239,371,489,605,733,855,984,1110,1239,1362,1536]}[name];sources[name]={'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rowBounds':bounds}
 for r,id in enumerate(ids):
  row=src[bounds[r]:bounds[r+1]].copy();row[:,:,3][row[:,:,3]<10]=0;rh=row.shape[0];tiles=[row[:,i*128:(i+1)*128].copy()for i in range(8)];
  for tile in tiles:
   ey,ex=np.mgrid[:rh,:128];edge=np.minimum(np.minimum(ex,127-ex)/12,np.minimum(ey,rh-1-ey)/8);tile[:,:,3]=np.rint(tile[:,:,3]*np.sin(np.clip(edge,0,1)*np.pi/2)**2).astype(np.uint8)
  yy,xx=np.where(row[:,:,3]>100);miny,maxy=int(yy.min()),int(yy.max());scale=min(.80,94/max(1,maxy-miny+1));anchor=[96,64]if id in flying else[64,108]if id in grounded else[64,64];normalized=[]
  for tile in tiles:
   im=Image.fromarray(tile);im=im.resize((round(128*scale),round(rh*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(128,128));tx=round(64-64*scale);ty=round((108-maxy*scale)if id in grounded else(64-(miny+maxy)/2*scale));out.alpha_composite(im,(tx,ty));arr=np.array(out);arr[:3]=0;arr[-3:]=0;arr[:,:3]=0;arr[:,-3:]=0;arr[arr[:,:,3]==0]=0;normalized.append(arr)
  tasks.append((id,normalized,anchor))
# Four roomy repaint strips replace the mist/cloud/cone rows after visual review.
path=Path('/workspace/generated_images/exec-d1df5d21-9fc8-4442-90c6-cf64a3b1ddca.png');src=np.array(Image.open(path).convert('RGBA'));sources['isolated']={'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rowBounds':[0,256,512,768,1024]}
for row,id in enumerate(['blizzard','poisoncloud','dragonfire','shadow']):
 tiles=[src[row*256:(row+1)*256,i*192:(i+1)*192].copy()for i in range(8)];core=[]
 for tile in tiles:
  tile[:,:,3][tile[:,:,3]<10]=0;ys,xs=np.where(tile[:,:,3]>100);core.extend(ys.tolist());ey,ex=np.mgrid[:256,:192];edge=np.minimum(np.minimum(ex,191-ex)/18,np.minimum(ey,255-ey)/12);tile[:,:,3]=np.rint(tile[:,:,3]*np.sin(np.clip(edge,0,1)*np.pi/2)**2).astype(np.uint8)
 miny,maxy=min(core),max(core);scale=min(.56,94/max(1,maxy-miny+1));normalized=[]
 for tile in tiles:
  im=Image.fromarray(tile).resize((round(192*scale),round(256*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(128,128));tx=round(64-96*scale);ty=round((108-maxy*scale)if id in grounded else(64-(miny+maxy)/2*scale));out.alpha_composite(im,(tx,ty));arr=np.array(out);arr[:3]=0;arr[-3:]=0;arr[:,:3]=0;arr[:,-3:]=0;arr[arr[:,:,3]==0]=0;normalized.append(arr)
 anchor=[96,64]if id in flying else[64,108]if id in grounded else[64,64];tasks=[t for t in tasks if t[0]!=id];tasks.append((id,normalized,anchor))
def process(id,keys,anchor):
 eng=Blend();frames=[]
 for i in range(7):
  frames.append(keys[i])
  for j in range(1,4):frames.append(eng.between(keys[i],keys[i+1],j/4,pixel=False))
 frames.append(keys[-1]);atlas,rects=pack(frames);p=A/'atlases'/(id+'.webp');atlas.save(p,lossless=True,method=5)
 cv=Image.new('RGBA',(128*8,128*4),'#474f4b')
 for i,f in enumerate(frames):cv.alpha_composite(Image.fromarray(f),((i%8)*128,(i//8)*128))
 cv.convert('RGB').save(A/'reviews'/(id+'.jpg'),quality=92)
 return id,{'src':'data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode(),'frameSize':128,'frameCount':29,'sourceFrameCount':8,'subframes':4,'anchor':anchor,'grounded':id in grounded,'frameRects':[[*rect,*offset]for rect,offset in rects],'packed':True,'version':46}, {'id':id,'frames':29,'sourceFrames':8,'atlas':list(atlas.size),'bytes':p.stat().st_size,'unique':len({hashlib.sha1(a.tobytes()).hexdigest()for a in frames})}
result={};audit=[]
with ThreadPoolExecutor(max_workers=3)as pool:
 for job in as_completed([pool.submit(process,*args)for args in tasks]):
  id,d,proof=job.result();result[id]=d;audit.append(proof);print(id,proof['bytes'],flush=True)
(A/'library.json').write_text(json.dumps(result,separators=(',',':')));(A/'audit.json').write_text(json.dumps({'families':audit,'sources':sources},indent=2))
