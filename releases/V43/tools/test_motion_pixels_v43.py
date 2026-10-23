from pathlib import Path
from PIL import Image
import json,base64,io,hashlib,numpy as np
R=Path('/workspace/RAG');A=R/'assets/motion-v43';E=R/'evidence/motion-v43';base=(R/'build/Runevale-Angel-Hitbox-V42/index.html').read_text()
def old(marker):
 i=base.index(marker)+len(marker);return json.JSONDecoder().raw_decode(base[i:])[0]
def image(d):return Image.open(io.BytesIO(base64.b64decode(d['src'].split(',')[1]))).convert('RGBA')
def native(im,f,pivot,size):
 x,y,w,h=f['rect'];c=Image.new('RGBA',tuple(size));c.alpha_composite(im.crop((x,y,x+w,y+h)),(pivot[0]-f['pivot'][0],pivot[1]-f['pivot'][1]));return np.array(c)
def delta(frames):
 a=[np.array(f).astype(float)for f in frames];return float(np.mean([np.abs(x-y).mean()for x,y in zip(a,a[1:]+a[:1])]))
rows=[];feet=[];margins=[]
for file,marker in [('characters-embedded.json','window.SHEET_DATA='),('costumes-embedded.json','window.COSTUME36_DATA=')]:
 data=json.loads((A/file).read_text());previous=old(marker)
 for id,d in data.items():
  im=image(d);prev=image(previous[id]);pivot=d['anchor'];size=d['frameSize'];clips={}
  for f in d['frames']:clips.setdefault((f['direction'],f['action']),[]).append(f)
  for key,fs in clips.items():fs.sort(key=lambda f:f['frame'])
  for di in ['S','N','W','E']:
   walk=[native(im,f,pivot,size)for f in clips[di,'walk']];attack=[native(im,f,pivot,size)for f in clips[di,'attack']];assert len(walk)==8 and len(attack)==12
   assert len({hashlib.sha1(f.tobytes()).hexdigest()for f in walk})==8,(id,di,'walk duplicates')
   idle=native(im,clips[di,'idle'][0],pivot,size);assert np.array_equal(attack[-1],idle),(id,di,'recovery jump')
   for k,f in enumerate(walk):
    yy,xx=np.nonzero(f[:,:,3]>64);feet.append(int(yy.max()+1));assert yy.max()+1==pivot[1],(id,di,k,'foot baseline');assert xx.min()>0 and xx.max()<size[0]-1 and yy.min()>0,(id,di,k,'clipped')
   oldwalk=[native(prev,f,pivot,size)for f in previous[id]['frames']if f['direction']==di and f['action']=='walk'];rows.append({'id':id,'direction':di,'oldWalkFrameDelta':delta(oldwalk),'newWalkFrameDelta':delta(walk),'walkFrames':8,'attackFrames':12})
assert len(rows)==172
fxrows=[];total=0
for file,marker in [('skills-embedded.json','window.SKILL_FX_DATA='),('casts-embedded.json','window.CAST_FX_DATA=')]:
 data=json.loads((A/file).read_text());previous=old(marker)
 for id,d in data.items():
  im=image(d);prev=image(previous[id]);fs=d['frameSize'];assert d['frameCount']in[29,33]and len(d['frameRects'])==d['frameCount'];frames=[]
  for k,r in enumerate(d['frameRects']):
   x,y,w,h,ox,oy=r;canvas=Image.new('RGBA',(fs,fs));canvas.alpha_composite(im.crop((x,y,x+w,y+h)),(ox,oy));f=np.array(canvas);frames.append(f)
   if k%d['subframes']==0:
    i=k//d['subframes'];original=np.array(prev.crop((i*fs,0,(i+1)*fs,fs)));assert np.array_equal(f[:,:,3],original[:,:,3]),(id,i,'alpha keyframe');visible=original[:,:,3]>0;assert np.array_equal(f[:,:,:3][visible],original[:,:,:3][visible]),(id,i,'color keyframe')
  assert d['duration']==previous[id]['duration'];total+=len(frames);fxrows.append({'id':id,'frames':len(frames),'originalKeyframesExact':True,'newFrameDelta':delta(frames)})
assert len(fxrows)==156 and total==5092
improved=sum(r['newWalkFrameDelta']<r['oldWalkFrameDelta']for r in rows);assert improved>=160,(improved,len(rows))
r={'bodyDirections':172,'all43BodiesHave8Walk12Attack':True,'feetAnchoredEveryWalkFrame':True,'walkDirectionsWithLowerFrameDelta':improved,'walkRows':rows,'fxSheets':156,'fxFrames':total,'allFXOriginalKeyframesExact':True,'allFXDurationsUnchanged':True};(E/'pixel-validation.json').write_text(json.dumps(r,indent=2));print({k:v for k,v in r.items()if k!='walkRows'})
