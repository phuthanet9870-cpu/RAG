from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,cv2,json,base64,io,hashlib
R=Path('/workspace/RAG');A=R/'assets/npcs-v55';spec=json.loads((A/'design.json').read_text());(A/'sprites').mkdir(exist_ok=True);(A/'masters').mkdir(exist_ok=True)
sources=['a7185b3a-1cb2-48c4-9ffa-19bced28682e','9420f376-44f7-4269-bcfa-cdd1bd7e6b79','843badc8-1879-466b-a8f8-c37b29516dcf','74f3a2e1-05ef-49b1-b91d-0bd6ead49847'];override={'arena':'c577460b-eb69-4324-8db6-32eac2961f93'};out={};audit=[]
for group,key in enumerate(sources):
 path=Path('/workspace/generated_images/exec-'+key+'.png');arr=np.array(Image.open(path).convert('RGBA'));n,labels,stats,cents=cv2.connectedComponentsWithStats((arr[:,:,3]>100).astype('uint8'));big=sorted([i for i in range(1,n)if stats[i,4]>10000],key=lambda i:cents[i,0]);assert len(big)==5,(group,len(big))
 for col,c in enumerate(big):
  item=spec['roles'][group*5+col];id=item['id'];srcpath=path;srcarr=arr;lab=labels;st=stats;cn=cents
  if id in override:
   srcpath=Path('/workspace/generated_images/exec-'+override[id]+'.png');srcarr=np.array(Image.open(srcpath).convert('RGBA'));nn,lab,st,cn=cv2.connectedComponentsWithStats((srcarr[:,:,3]>100).astype('uint8'));c=max(range(1,nn),key=lambda v:st[v,4]);selected=[c]
  else:
   selected=[c]
   for i in range(1,n):
    if i in big or stats[i,4]<8:continue
    near=min(big,key=lambda v:abs(cents[v,0]-cents[i,0]));x,y,w,h,_=stats[c]
    if near==c and x-12<=cents[i,0]<=x+w+12 and y-12<=cents[i,1]<=y+h+12:selected.append(i)
  mask=np.isin(lab,selected);yy,xx=np.where(mask);x0,x1,y0,y1=int(xx.min()),int(xx.max()+1),int(yy.min()),int(yy.max()+1)
  assert x0>0 and y0>0 and x1<srcarr.shape[1] and y1<srcarr.shape[0],(id,'clipped source',x0,y0,x1,y1)
  crop=srcarr[y0:y1,x0:x1].copy();cm=mask[y0:y1,x0:x1];crop[:,:,3]=np.where(cm,255,0);crop[~cm]=0
  master=Image.fromarray(crop);master.save(A/'masters'/(id+'.png'),optimize=True)
  rows=cm.sum(1);footy=int(np.where(rows>=max(6,(x1-x0)*.05))[0][-1]);strip=cm[max(0,footy-round((y1-y0)*.04)):footy+1].astype('uint8');nc,ll,ss,cc=cv2.connectedComponentsWithStats(strip);parts=sorted([i for i in range(1,nc)if ss[i,4]>12],key=lambda i:ss[i,4],reverse=True)[:2];footx=float(np.mean([cc[i,0]for i in parts]))if parts else float(np.median(np.where(strip)[1]))
  target=134 if id in ['smith','guild','merc','arena']else 130 if id in ['stable','storage','market','tower','training','mail','token','collector']else 126;scale=min(target/max(1,footy),160/(x1-x0));w,h=round((x1-x0)*scale),round((y1-y0)*scale);small=master.resize((w,h),Image.Resampling.NEAREST);small=small.quantize(colors=128,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE).convert('RGBA');frame=Image.new('RGBA',(192,160));tx=round(96-footx*scale);ty=round(144-footy*scale);assert tx>=4 and ty>=4 and tx+w<=188 and ty+h<=156,(id,'native frame clips',tx,ty,w,h);frame.alpha_composite(small,(tx,ty));frame.save(A/'sprites'/(id+'.png'),optimize=True);bb=frame.getbbox();assert bb and bb[1]>=4 and bb[3]<=156
  b=io.BytesIO();frame.save(b,format='PNG',optimize=True);out[id]={**item,'src':'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode(),'frameSize':[192,160],'anchor':[96,144],'frames':1,'direction':'S','action':'idle','static':True,'noVfx':True,'rect':[0,0,192,160],'inkBounds':bb};audit.append({'id':id,'source':srcpath.name,'sourceBounds':[x0,y0,x1,y1],'sourceNotClipped':True,'masterSize':[x1-x0,y1-y0],'nativeSize':[192,160],'nativeInkBounds':bb,'anchor':[96,144],'footSource':[round(footx,2),footy],'scale':scale,'direction':'front','pose':'standing','frames':1,'sha256':hashlib.sha256(frame.tobytes()).hexdigest()})
(A/'embedded.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')));(A/'audit.json').write_text(json.dumps({'npcRoles':20,'nativeFrames':20,'frontViewOnly':True,'staticNoAnimation':True,'sprites':audit},ensure_ascii=False,indent=2))
review=Image.new('RGB',(960,800),'#ece5d5');d=ImageDraw.Draw(review)
for i,role in enumerate(spec['roles']):
 xx=i%5*192;yy=i//5*200;f=Image.open(A/'sprites'/(role['id']+'.png'));review.paste(f,(xx,yy+24),f);d.text((xx+12,yy+4),role['id'],fill='#34342a')
review.save(A/'review.jpg',quality=94);print('Normalized20 front-facing static NPCs',flush=True)
