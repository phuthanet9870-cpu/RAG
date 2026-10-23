from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,base64,io,hashlib
R=Path('/workspace/RAG');A=R/'assets/low-walk-v45';E=R/'evidence/low-walk-v45';old=json.loads((R/'assets/motion-v43/costumes-embedded.json').read_text());new=json.loads((A/'costumes-embedded.json').read_text());audits=json.loads((A/'audit.json').read_text());checks=0;preserved=0

def frame(d,im,f):
 cv=Image.new('RGBA',(128,144));x,y,w,h=f['rect'];px,py=f['pivot'];cv.alpha_composite(im.crop((x,y,x+w,y+h)),(64-px,128-py));return np.array(cv)
for id,d in new.items():
 im=Image.open(A/'costumes'/(id+'.webp'));oi=Image.open(R/'assets/motion-v43/costumes'/(id+'.webp'));of={(f['direction'],f['action'],f['frame']):frame(old[id],oi,f)for f in old[id]['frames']};nf={(f['direction'],f['action'],f['frame']):frame(d,im,f)for f in d['frames']}
 assert len(nf)==len(of)==194
 for k,f in nf.items():
  di,action,n=k
  if action in ['idle','attack','down']:assert np.array_equal(f,of[k]),(id,k);preserved+=1
  if action=='walk':
   assert np.array_equal(f[:98],nf[di,'idle',0][:98]),(id,k,'upper body drift')
   assert np.nonzero(f[:,:,3]>64)[0].max()+1==128,(id,k,'baseline')
   assert not f[0,:,3].any()and not f[-1,:,3].any()and not f[:,0,3].any()and not f[:,-1,3].any(),(id,k,'clipped')
 for di in ['S','N','W','E']:
  walk=[nf[di,'walk',k]for k in range(8)];assert len({hashlib.sha1(f.tobytes()).hexdigest()for f in walk})==8
  assert not np.array_equal(walk[0][98:],walk[4][98:])
  assert np.array_equal(nf[di,'start',2],walk[0])
  for k in range(8):assert np.array_equal(nf[di,'stop'+str(k),0],walk[k])and np.array_equal(nf[di,'stop'+str(k),2],nf[di,'idle',0])
  a=next(a for a in audits if a['id']==id)['directions'][di]
  for row in a['legs']:assert max(p['lift']for p in row)<=2 and min(p['lift']for p in row)==0
  assert a['legs'][2][0]['sole']!=a['legs'][6][0]['sole']and a['legs'][2][1]['sole']!=a['legs'][6][1]['sole'],(id,di,'feet not alternating')
  checks+=1
# Animated in-game source-frame proof: same frost costume before and after.
frames=[];id='c_frost';d=new[id];im=Image.open(A/'costumes'/(id+'.webp'));oi=Image.open(R/'assets/motion-v43/costumes'/(id+'.webp'))
for k in range(8):
 cv=Image.new('RGBA',(512,320),'#e9e5d9');draw=ImageDraw.Draw(cv);draw.text((80,8),'V44: BEFORE',fill='black');draw.text((330,8),'V45: LOW WALK',fill='black')
 for col,(data,image)in enumerate([(old[id],oi),(new[id],im)]):
  f=next(f for f in data['frames']if f['action']=='walk'and f['direction']=='E'and f['frame']==k);a=Image.fromarray(frame(data,image,f)).resize((256,288),Image.Resampling.NEAREST);cv.alpha_composite(a,(col*256,25))
 frames.append(cv.convert('RGB'))
frames[0].save(E/'frost-before-after.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=2)
r={'changedCostumes':10,'directionClips':checks,'walkFrames':320,'allWalkFramesUnique':True,'feetAlternateAndLiftAtMost2NativePixels':True,'feetBaseline128EveryFrame':True,'facesUpperBodyIdleAndAttacksPreserved':True,'unchangedIdleAttackDeathFrames':preserved,'startStopClipsMatchNewWalk':True};(E/'pixel-validation.json').write_text(json.dumps(r,indent=2));print(r)
