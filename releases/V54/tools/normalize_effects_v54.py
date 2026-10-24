from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,cv2,json,base64,io,hashlib
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
R=Path('/workspace/RAG');A=R/'assets/effects-v54';(A/'atlases').mkdir(exist_ok=True);(A/'reviews').mkdir(exist_ok=True)
groups=[('martial','123c6ebe-b0af-49bc-9f22-3481fea3d451',['lance','solar_slash','spirit_fist','forge_impact']),('magic','ee6e4d37-2cae-4d19-8e24-b27198ca3586',['lightning','cyclone','ice_spikes','blizzard']),('support','5bc323be-cb84-4cca-961a-dabf19af6cb3',['aegis','restoration','resurrection','forge']),('nature','6ba9a640-1619-4e7c-a11e-1555418022ab',['acid','venom','vines','bloom']),('shadow','3a8b095e-ded3-4b4f-9048-605ce9c10e45',['soul_reap','soul_chain','cross_blade','eclipse']),('ranged','5d807b01-462f-427e-b4c1-947cd5bb8f34',['arrow','arrow_rain','tailwind','shadow_web']),('fixes','258263ca-3bd7-4d54-a494-b4a8be777b64',['forge_impact','holy_judgement','frost_ward','soul_ward'])]
fly={'lance','spirit_fist','lightning','acid','arrow','tailwind'};library={};audit=[]
for group,key,ids in groups:
 path=Path('/workspace/generated_images/exec-'+key+'.png');arr=np.array(Image.open(path).convert('RGBA'));H,W=arr.shape[:2];density=np.convolve((arr[:,:,3]>120).sum(1),np.ones(9)/9,'same');bounds=[0]
 for row in range(1,4):
  a=int(H*row/4)-57;b=int(H*row/4)+57;bounds.append(a+int(np.argmin(density[a:b])))
 bounds.append(H)
 for row,id in enumerate(ids):
  if group=='martial'and id=='forge_impact':continue
  data=arr[bounds[row]:bounds[row+1]].copy();data[:,:,3][data[:,:,3]<64]=0;rh=data.shape[0]
  # Recover the actually drawn sprite centres, rather than assuming the generated grid is exact.
  lum=data[:,:,:3].max(2).astype(float)/255;energy=(data[:,:,3].astype(float)/255*lum**2).sum(0);energy=gaussian_filter1d(energy,5)
  peaks,_=find_peaks(energy,distance=82,prominence=max(1,energy.max()*.018))
  if len(peaks)<8:peaks,_=find_peaks(energy,distance=74,prominence=max(.2,energy.max()*.004))
  if group=='fixes':peaks=np.array([round(W*(i+.5)/8)for i in range(8)])
  assert len(peaks)>=8,(id,'fewer than8 native sprites',peaks.tolist())
  centers=list(map(float,peaks));count=len(centers);edges=[0]
  for j in range(1,count):
   lo=round(centers[j-1]+(centers[j]-centers[j-1])*.35);hi=round(centers[j-1]+(centers[j]-centers[j-1])*.65);edges.append(lo+int(np.argmin(energy[lo:hi])))
  edges.append(W);peak=int(np.argmax(energy[peaks]));selected=sorted(set([0,round(peak*.45),max(1,peak-1),peak,min(count-1,peak+1),round(peak+(count-1-peak)*.55),count-2,count-1]));
  while len(selected)<8:
   k=max((k for k in range(count)if k not in selected),key=lambda k:min(abs(k-v)for v in selected));selected=sorted(selected+[k])
  n,lab,stats,cents=cv2.connectedComponentsWithStats((data[:,:,3]>0).astype('uint8'));owner=np.full(n,-1,dtype=int)
  for c in range(1,n):
   if stats[c,4]<2:continue
   inside=[j for j,v in enumerate(centers)if stats[c,0]<=v<stats[c,0]+stats[c,2]]
   if len(inside)==1:owner[c]=inside[0]
   elif not inside:owner[c]=int(np.argmin(np.abs(np.array(centers)-cents[c,0])))
  tiles=[];boxes=[];cw=320
  for j in selected:
   left=round(centers[j]-cw/2);right=left+cw;lo=max(0,left);hi=min(W,right);part=data[:,lo:hi].copy();labels=lab[:,lo:hi];own=owner[labels];xx=np.arange(lo,hi)[None,:];belongs=(own==j)|((own==-1)&(xx>=edges[j])&(xx<edges[j+1]));part[:,:,3][~belongs]=0;tile=np.zeros((rh,cw,4),dtype='uint8');tile[:,lo-left:hi-left]=part
   yy,xx2=np.where(tile[:,:,3]>64);assert len(xx2)>15,(id,j,'blank');boxes.append((int(xx2.min()),int(yy.min()),int(xx2.max()+1),int(yy.max()+1)));tiles.append(tile)
  # One scale and one vertical baseline for the entire clip. Never rescale individual frames.
  xmin=min(b[0]for b in boxes);xmax=max(b[2]for b in boxes);maxw=xmax-xmin;ymin=min(b[1]for b in boxes);ymax=max(b[3]for b in boxes);scale=min(100/maxw,98/(ymax-ymin),.85);grounded=id not in fly;anchor=[64,108]if grounded else[64,64];frames=[];hashes=[]
  for tile in tiles:
   p=Image.fromarray(tile).resize((round(cw*scale),round(rh*scale)),Image.Resampling.NEAREST);f=Image.new('RGBA',(128,128));tx=round(64-(xmin+xmax)/2*scale);ty=round(108-ymax*scale)if grounded else round(64-(ymin+ymax)/2*scale);f.alpha_composite(p,(tx,ty));a=np.array(f);a[:3]=0;a[-3:]=0;a[:,:3]=0;a[:,-3:]=0;a[a[:,:,3]==0]=0;f=Image.fromarray(a);assert f.getbbox();frames.append(f);hashes.append(hashlib.sha256(f.tobytes()).hexdigest())
  assert len(set(hashes))==8,(id,'duplicate');atlas=Image.new('RGBA',(1024,128));review=Image.new('RGBA',(1024,160),'#e4ddcb');ImageDraw.Draw(review).text((5,3),id,fill='#292e29')
  for j,f in enumerate(frames):atlas.alpha_composite(f,(j*128,0));review.alpha_composite(f,(j*128,25))
  atlas.save(A/'atlases'/(id+'.png'),optimize=True);review.convert('RGB').save(A/'reviews'/(id+'.jpg'),quality=93);b=io.BytesIO();atlas.save(b,format='PNG',optimize=True);library['u54_'+id]={'src':'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode(),'frameSize':128,'frameCount':8,'sourceFrameCount':8,'subframes':1,'anchor':anchor,'grounded':grounded,'frameRects':[[j*128,0,128,128,0,0]for j in range(8)],'packed':True,'version':54};audit.append({'family':id,'source':path.name,'sourceRow':row,'rowBounds':bounds[row:row+2],'gutters':edges,'scale':scale,'sourceDetectedFrames':count,'selectedSourceSlots':selected,'sourcePeaks':centers,'frames':8,'uniqueFrames':len(set(hashes)),'anchor':anchor,'maxSourceFrameWidth':maxw,'nativeFramesOnly':True,'edgePixelsRemoved':True})
(A/'library.json').write_text(json.dumps(library,separators=(',',':')));(A/'audit.json').write_text(json.dumps({'families':audit,'totalFamilies':27,'nativeFrames':216,'noOpticalFlowOrCrossfade':True},indent=2));print('Normalized27 sheets /216 native frames',flush=True)
# Compact clip overview at useful display scale, checker-free neutral ground.
review=Image.new('RGB',(1024,27*96),'#e4ddcb');d=ImageDraw.Draw(review)
for i,q in enumerate(audit):
 d.text((4,i*96+3),q['family'],fill='#292e29');im=Image.open(A/'atlases'/(q['family']+'.png'))
 for j,k in enumerate([0,1,3,4,6,7]):
  f=im.crop((k*128,0,(k+1)*128,128)).resize((96,96),Image.Resampling.NEAREST);review.paste(f,(170+j*140,i*96),f)
review.save(A/'overview.jpg',quality=91)
