from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,base64,hashlib,cv2
R=Path('/workspace/RAG');A=R/'assets/recast-v47';sources=json.loads((A/'sources.json').read_text());old=json.loads((R/'assets/recast-v46/library.json').read_text());library={};proof=[]
lastSource={id:i for i,g in enumerate(sources)for id in g['ids']}
for groupIndex,group in enumerate(sources):
 path=Path(group['path']);im=Image.open(path).convert('RGBA');src=np.array(im);H,W=src.shape[:2];density=np.convolve((src[:,:,3]>150).sum(1).astype(float),np.ones(5)/5,'same');bounds=[0]+[int(j+np.argmin(density[j:k]))for i in range(1,6)for j,k in[(round(H*i/6)-40,round(H*i/6)+40)]]+[H];bounds=group.get('bounds',bounds);group['bounds']=bounds
 for row,id in enumerate(group['ids']):
  if lastSource[id]!=groupIndex:continue
  tiles=[];boxes=[];rowData=src[bounds[row]:bounds[row+1]].copy();rowData[:,:,3][rowData[:,:,3]<64]=0
  n,labels,stats,centroids=cv2.connectedComponentsWithStats((rowData[:,:,3]>0).astype('uint8'));owners=np.full(n,-1,dtype=int)
  for component in range(1,n):
   if stats[component,4]>=2:owners[component]=min(7,max(0,int(centroids[component,0]/(W/8))))
  for col in range(8):
   # Capture the whole connected sprite across nominal cell boundaries, excluding neighbors.
   center=round(W*(col+.5)/8);left=center-144;right=center+144;tile=np.zeros((rowData.shape[0],288,4),dtype=np.uint8);lo=max(0,left);hi=min(W,right);part=rowData[:,lo:hi].copy();part[:,:,3][owners[labels[:,lo:hi]]!=col]=0;tile[:,lo-left:hi-left]=part
   ys,xs=np.where(tile[:,:,3]>64);assert len(xs)>15,(id,col,'blank source');boxes.append((xs.min(),ys.min(),xs.max()+1,ys.max()+1));tiles.append(tile)
  minY=min(b[1]for b in boxes);maxY=max(b[3]for b in boxes);maxW=max(b[2]-b[0]for b in boxes);scale=min(1,100/maxW,96/(maxY-minY));cw=tiles[0].shape[1];anchor=old[id]['anchor'];grounded=old[id]['grounded'];frames=[]
  # One scale and vertical anchor across each strip. No per-frame bounding-box recentering.
  for tile in tiles:
   th,tw=tile.shape[:2];frame=Image.new('RGBA',(128,128));part=Image.fromarray(tile).resize((round(tw*scale),round(th*scale)),Image.Resampling.NEAREST);x=round(64-cw*.5*scale);y=round(108-maxY*scale)if grounded else round(64-(minY+maxY)*.5*scale);frame.alpha_composite(part,(x,y));a=np.array(frame);a[:3]=0;a[-3:]=0;a[:,:3]=0;a[:,-3:]=0;a[a[:,:,3]==0]=0;frames.append(Image.fromarray(a))
  atlas=Image.new('RGBA',(1024,128));rects=[]
  for k,f in enumerate(frames):atlas.alpha_composite(f,(128*k,0));rects.append([128*k,0,128,128,0,0])
  dest=A/'atlases'/(id+'.webp');atlas.save(dest,lossless=True,method=5)
  library[id]={'src':'data:image/webp;base64,'+base64.b64encode(dest.read_bytes()).decode(),'frameSize':128,'frameCount':8,'sourceFrameCount':8,'subframes':1,'anchor':anchor,'grounded':grounded,'frameRects':rects,'packed':True,'version':47}
  review=Image.new('RGBA',(1024,150),'#dedbcf');review.alpha_composite(atlas,(0,22));ImageDraw.Draw(review).text((4,3),id,fill='black');review.convert('RGB').save(A/'reviews'/(id+'.jpg'),quality=94)
  unique=len({hashlib.sha256(f.tobytes()).hexdigest()for f in frames});assert unique==8,(id,unique);proof.append({'id':id,'frames':8,'unique':unique,'source':path.name,'scale':scale,'bytes':dest.stat().st_size})
assert len(library)==48
(A/'library.json').write_text(json.dumps(library,separators=(',',':')));(A/'audit.json').write_text(json.dumps({'frames':384,'nativeFramesOnly':True,'noOpticalFlow':True,'families':proof,'sources':sources},indent=2));print('48 fresh native strips, 384 unique keyframes; zero interpolated frames',flush=True)
