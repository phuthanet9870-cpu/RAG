from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib,base64,io
R=Path('/workspace/RAG');A=R/'assets/recast-v47';E=R/'evidence/recast-v47';lib=json.loads((A/'library.json').read_text());design=json.loads((A/'design.json').read_text());count=0;edges=[];sample=[]
for id,d in lib.items():
 im=Image.open(A/'atlases'/(id+'.webp')).convert('RGBA');assert base64.b64decode(d['src'].split(',')[1])==(A/'atlases'/(id+'.webp')).read_bytes();assert d['frameCount']==8;hashes=set()
 for k,r in enumerate(d['frameRects']):
  x,y,w,h,ox,oy=r;assert min(x,y)>=0 and x+w<=im.width and y+h<=im.height;cv=Image.new('RGBA',(128,128));cv.alpha_composite(im.crop((x,y,x+w,y+h)),(ox,oy));a=np.array(cv);assert a[:,:,3].max()>32,(id,k,'blank');hashes.add(hashlib.sha1(a.tobytes()).hexdigest());count+=1
  border=np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])
  if border.max()>16:edges.append((id,k,int(border.max())))
  assert not a[0,0,3]and not a[-1,-1,3],(id,k,'opaque corner')
  if k==4:sample.append((id,cv))
 assert len(hashes)==8,(id,'duplicate frames')
assert not edges,edges
cv=Image.new('RGBA',(8*144,6*158),'#d8d5ca');dr=ImageDraw.Draw(cv)
for i,(id,im)in enumerate(sample):cv.alpha_composite(im,(i%8*144+8,i//8*158+22));dr.text((i%8*144+4,i//8*158+2),id,fill='black')
cv.convert('RGB').save(E/'new-families-contact.jpg',quality=95)
r={'newPaintedFamilies':len(lib),'transparentNativeFrames':count,'all8FramesUniquePerFamily':True,'noBlankFramesOrOpaqueCorners':True,'allSpriteRectsValid':True,'all146SkillDesignsMapped':len(design)==146};(E/'pixel-validation.json').write_text(json.dumps(r,indent=2));print(r)
