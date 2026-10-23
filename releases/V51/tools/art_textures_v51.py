from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,random,math,json,base64,io,hashlib
R=Path('/workspace/RAG');O=R/'assets/textures-v51';O.mkdir(exist_ok=True)
S=128;y,x=np.mgrid[:S,:S];tex=[];meta=[]
names=['Capital limestone','Meadow clover','Sunlit pasture','Granite trail','Wildflower field','Dry grassland','Amber meadow','Forest moss','Deep woodland','Highland shale','Fern forest','Mountain scree','Slate ridge','Ancient grove','Glacial frost','Garden lawn','Seaside sand','Crypt flagstone','Forgotten catacomb','Poisoned earth','Basalt vault','Withered marsh','Golden dunes','Red sandstone','Volcanic crust','Eclipse marble','Tomb sandstone','Tower mosaic','Training turf','Arena ochre','Clear river','Venom mire']
grass={1:(116,142,83),2:(139,151,91),4:(123,148,88),5:(150,145,94),6:(151,143,79),7:(84,119,75),8:(71,103,73),10:(91,126,79),13:(91,117,76),15:(124,150,91),28:(118,137,85)}
stone={0:(183,176,153),3:(142,140,126),9:(133,132,122),11:(128,130,127),12:(113,121,123),17:(113,112,115),18:(106,111,107),20:(91,99,108),25:(111,110,131),27:(151,146,128)}
sand={16:(204,188,146),22:(204,176,122),23:(188,144,103),26:(178,155,114),29:(183,155,112)}
def noise(seed):
 rng=random.Random(seed);a=np.zeros((S,S),float)
 for freq,amp in [(1,5),(2,4),(4,2.4),(8,1.1),(16,.6)]:
  for k in range(4):
   ax=rng.randint(-freq,freq);ay=rng.randint(-freq,freq);a+=amp*np.sin(2*np.pi*(ax*x+ay*y)/S+rng.random()*6.28)/4
 return a

def save(im,name):
 im.save(O/(name+'.png'),optimize=True);b=io.BytesIO();im.save(b,format='PNG',optimize=True);return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
# Paint all motifs on a 3x3 canvas then crop: features wrap exactly at texture borders.
for n in range(32):
 rng=random.Random(51000+n);a=noise(n+510);base=grass.get(n,stone.get(n,sand.get(n,(168,191,196)if n==14 else (82,70,68)if n==24 else (69,131,149)if n==30 else (89,111,72))))
 rgb=np.clip(np.array(base)[None,None,:]+a[:,:,None],0,255).astype('uint8');im=Image.fromarray(rgb);large=Image.new('RGB',(S*3,S*3));
 for iy in range(3):
  for ix in range(3):large.paste(im,(ix*S,iy*S))
 d=ImageDraw.Draw(large)
 def motif(fn,*args):
  for yy in [-S,0,S]:
   for xx in [-S,0,S]:fn(xx+S,yy+S,*args)
 if n in grass or n in [19,21]:
  # Broad clumps of blades with warm tips, cool undergrowth, scattered earth.
  for k in range(210):
   cx,cy=rng.randrange(S),rng.randrange(S);h=rng.randint(2,5);w=rng.randint(2,5);shade=rng.choice([-18,-9,8,14]);c=tuple(max(0,min(255,v+shade))for v in base)
   def tuft(ox,oy):
    px,py=cx+ox,cy+oy;d.line([(px-2,py+1),(px+w,py+1)],fill=tuple(max(0,v-18)for v in c));d.line([(px,py),(px-1,py-h)],fill=c);d.line([(px+1,py),(px+3,py-h+1)],fill=c);d.point((px-1,py-h),fill=tuple(min(255,v+10)for v in c))
   motif(tuft)
  for k in range(17):
   cx,cy=rng.randrange(S),rng.randrange(S);rr=rng.randint(1,3)
   def peb(ox,oy):
    px,py=cx+ox,cy+oy;d.ellipse((px,py,px+rr*2,py+rr),fill=(114,111,88));d.line((px+1,py,px+rr,py),fill=(165,157,118))
   motif(peb)
  if n in [2,4,7,10,13,15]:
   for k in range(7):
    cx,cy=rng.randrange(S),rng.randrange(S)
    def flower(ox,oy):
     px,py=cx+ox,cy+oy;d.line((px,py,px,py+3),fill=(69,106,62));d.ellipse((px-1,py-1,px+1,py+1),fill=(222,204,143)if k%2 else(185,178,191));d.point((px,py),fill=(238,215,151))
    motif(flower)
 elif n in stone:
  # Irregular toroidal Voronoi slabs, bevel shading and hairline mortar.
  sites=[]
  for attempt in range(4000):
   sx,sy=rng.uniform(0,S),rng.uniform(0,S)
   if all(((sx-a+S/2)%S-S/2)**2+((sy-b+S/2)%S-S/2)**2>13**2 for a,b in sites):sites.append((sx,sy))
   if len(sites)>=38:break
  ds=[]
  for sx,sy in sites:
   dx=(x-sx+S/2)%S-S/2;dy=(y-sy+S/2)%S-S/2;ds.append(dx*dx+dy*dy)
  ds=np.array(ds);order=np.argsort(ds,axis=0);dist=np.take_along_axis(ds,order,axis=0);idx=order[0];edge=(np.sqrt(dist[1])-np.sqrt(dist[0]));out=np.zeros((S,S,3),float)
  for k in range(len(sites)):
   m=idx==k;variation=rng.uniform(-16,16);out[m]=np.array(base)+variation+a[m,None]*.65
  # Directional raised top-left edges versus lower-right recesses.
  highlight=(np.roll(idx,1,axis=0)!=idx)|(np.roll(idx,1,axis=1)!=idx);out[edge<.65]=np.array(base)*.70;out[(edge>=.65)&(edge<2.5)]+=6;out[highlight& (edge>1.2)]+=8
  # Raised worn surfaces, porous grain, broad cloudy inclusions.
  for k,(sx,sy) in enumerate(sites):
   dx=(x-sx+S/2)%S-S/2;dy=(y-sy+S/2)%S-S/2;m=idx==k;relief=np.clip((18-np.sqrt(ds[k]))*.35,-5,5)-(dx+dy)*.12;out[m]+=relief[m,None]
  out+=noise(n+810)[:,:,None]*1.4;out+=np.random.default_rng(n).normal(0,1.4,(S,S,1));im=Image.fromarray(np.clip(out,0,255).astype('uint8'));large=Image.new('RGB',(S*3,S*3))
  for iy in range(3):
   for ix in range(3):large.paste(im,(ix*S,iy*S))
  d=ImageDraw.Draw(large)
  for k in range(100):
   cx,cy=rng.randrange(S),rng.randrange(S)
   def fleck(ox,oy):d.line((cx+ox,cy+oy,cx+ox+2,cy+oy),fill=tuple(min(255,v+15)for v in base))
   motif(fleck)
 elif n in sand:
  # Low relief wind-shaped ripples, warm mineral flecks and individual pebbles.
  wave=2.3*np.sin(2*np.pi*(y*6/S+.13*np.sin(x*2*np.pi/S)))
  im=Image.fromarray(np.clip(rgb.astype(float)+wave[:,:,None],0,255).astype('uint8'))
  for iy in range(3):
   for ix in range(3):large.paste(im,(ix*S,iy*S))
  d=ImageDraw.Draw(large)
  for k in range(110):
   cx,cy=rng.randrange(S),rng.randrange(S);v=rng.choice([-15,10,18]);c=tuple(max(0,min(255,q+v))for q in base)
   def grit(ox,oy):d.point((cx+ox,cy+oy),fill=c)
   motif(grit)
  for k in range(7):
   cx,cy=rng.randrange(S),rng.randrange(S)
   def pebble(ox,oy):
    px,py=cx+ox,cy+oy;d.ellipse((px,py,px+4,py+2),fill=(148,129,98));d.line((px,py,px+2,py),fill=(220,198,154))
   motif(pebble)
 elif n==14:
  for k in range(18):
   cx,cy=rng.randrange(S),rng.randrange(S);length=rng.randrange(10,35)
   def ice(ox,oy):
    px,py=cx+ox,cy+oy;d.line([(px,py),(px+length*.4,py+4),(px+length,py+1)],fill=(136,169,181));d.line([(px,py-1),(px+length*.4,py+3),(px+length,py)],fill=(203,220,216))
   motif(ice)
 elif n==24:
  for k in range(14):
   cx,cy=rng.randrange(S),rng.randrange(S)
   def crack(ox,oy):
    pts=[(cx+ox,cy+oy),(cx+ox+6,cy+oy+9),(cx+ox+3,cy+oy+17),(cx+ox+15,cy+oy+25)];d.line(pts,fill=(48,43,45),width=4);d.line(pts,fill=(168,85,47),width=1);d.point(pts[1],fill=(219,139,65))
   motif(crack)
 elif n in [30,31]:
  for k in range(32):
   cx,cy=rng.randrange(S),rng.randrange(S);length=rng.randrange(5,19)
   def ripple(ox,oy):
    col=(106,161,170)if n==30 else(116,144,84);d.arc((cx+ox,cy+oy,cx+ox+length,cy+oy+5),0,130,fill=col)
   motif(ripple)
 im=large.crop((S,S,2*S,2*S));tex.append(save(im,'texture-'+str(n)));meta.append({'index':n,'name':names[n],'size':[S,S],'seamless':True})
# New silhouettes at128px: lit facets, bark rings, serrated leaves, spiral shell.
resources={}
for j,id in enumerate(['iron','gold','crystal','herb','timber','shell']):
 im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im);rng=random.Random(510+j)
 d.ellipse((17,104,113,120),fill=(32,36,31,50));d.ellipse((26,106,105,117),fill=(29,32,30,60))
 if id in ['iron','gold']:
  pts=[(14,104),(20,80),(38,73),(44,49),(73,43),(92,62),(112,83),(116,106),(91,116),(41,116)]
  d.polygon(pts,fill='#686d70',outline='#3e454a');d.polygon([(20,80),(44,49),(73,43),(65,76),(38,94)],fill='#a0a29b');d.polygon([(65,76),(73,43),(92,62),(112,83),(88,87)],fill='#80878a');d.polygon([(38,94),(65,76),(88,87),(91,116),(41,116)],fill='#777d79');d.line([(21,81),(43,50),(72,44)],fill='#c2c0ad',width=2)
  for k in range(17):
   cx=rng.randrange(35,99);cy=rng.randrange(65,104);r=rng.randrange(2,5);gold=id=='gold';d.polygon([(cx-r,cy),(cx,cy-r),(cx+r,cy),(cx+2,cy+r)],fill=('#c8a75c'if gold else'#b5a28a'));d.line((cx-r,cy,cx,cy-r),fill=('#edcf86'if gold else'#ddd0ab'),width=2)
  d.line([(39,94),(55,98),(66,91)],fill='#4b5355',width=2)
 elif id=='crystal':
  d.polygon([(19,109),(34,94),(94,94),(111,110),(82,119),(37,117)],fill='#5e6972')
  for cx,cy,h,w in [(41,103,49,12),(88,104,62,13),(64,108,84,17),(101,110,32,8),(26,111,29,9)]:
   d.polygon([(cx-w,cy-h*.7),(cx,cy-h),(cx+w,cy-h*.7),(cx+w-2,cy-5),(cx,cy+3),(cx-w+2,cy-5)],fill='#638f9c',outline='#384f68');d.polygon([(cx,cy-h),(cx+w,cy-h*.7),(cx+w-2,cy-5),(cx,cy+3)],fill='#547a96');d.polygon([(cx,cy-h),(cx-w,cy-h*.7),(cx-w+2,cy-5),(cx,cy+3)],fill='#a7cfcb');d.line([(cx,cy-h+2),(cx,cy)],fill='#d6e7d9',width=2)
 elif id=='herb':
  d.ellipse((38,103,95,117),fill='#6e7050')
  for k in range(15):
   ang=k*2.4;cx=64+math.cos(ang)*rng.randrange(10,35);cy=87+math.sin(ang)*rng.randrange(12,26);tip=(cx+math.cos(ang)*18,cy-17);d.line((64,111,cx,cy),fill='#495e3e',width=3);d.polygon([(cx-9,cy-3),tip,(cx+7,cy-8),(cx+6,cy+3),(cx,cy+9)],fill=rng.choice(['#759258','#8aa45f','#557747','#637f4a']),outline='#425e3b');d.line((cx,cy+5,*tip),fill='#b1ba78')
  for cx,cy in [(46,70),(74,66),(83,85)]:
   d.line((cx,cy,cx-2,cy+25),fill='#64784a',width=2)
   for a in range(0,360,72):
    px=cx+math.cos(math.radians(a))*4;py=cy+math.sin(math.radians(a))*4;d.ellipse((px-3,py-3,px+3,py+3),fill='#cbb4bf')
   d.ellipse((cx-2,cy-2,cx+2,cy+2),fill='#dbc58b')
 elif id=='timber':
  for cx,cy in [(39,101),(78,105),(58,83)]:
   d.polygon([(cx-21,cy-11),(cx+10,cy-34),(cx+34,cy-20),(cx+7,cy+13)],fill='#705239',outline='#433d30');d.line([(cx-18,cy-9),(cx+11,cy-30)],fill='#aa8152',width=3);d.line([(cx-8,cy-5),(cx+22,cy-25)],fill='#463c30',width=2);d.ellipse((cx-20,cy-14,cx+13,cy+15),fill='#b29a69',outline='#554832',width=2);d.ellipse((cx-14,cy-9,cx+7,cy+10),outline='#8e754e',width=2);d.ellipse((cx-8,cy-4,cx+2,cy+6),outline='#7b6546');d.line((cx-3,cy+1,cx+9,cy+10),fill='#756044')
  d.polygon([(80,69),(96,58),(101,64),(92,72)],fill='#72915a');d.line((81,71,97,61),fill='#b1b77b')
 else:
  d.polygon([(30,106),(27,91),(36,72),(55,58),(79,57),(98,69),(109,89),(101,107),(79,116),(48,115)],fill='#bba98e',outline='#746c61');d.pieslice((33,56,105,118),180,365,fill='#d3c4a4',outline='#96866f',width=2)
  for a in range(195,350,15):
   rad=math.radians(a);d.line((68,109,68+37*math.cos(rad),101+39*math.sin(rad)),fill='#ae967d',width=2);d.line((70,109,70+36*math.cos(rad),99+38*math.sin(rad)),fill='#e7d7b4')
  d.arc((49,73,89,109),170,530,fill='#a98f76',width=3);d.arc((58,80,81,101),0,320,fill='#8e7a67',width=2);d.ellipse((65,87,72,93),fill='#b69b7d')
 resources[id]=save(im,'resource-'+id)
(O/'data.json').write_text(json.dumps({'textures':tex,'resources':resources}));(O/'manifest.json').write_text(json.dumps({'style':'Original painted pixel-art fantasy MMORPG materials; no extracted Ragnarok assets','textures':meta,'resources':list(resources),'resourcePixels':[128,128],'worldFootprint':[64,64]},indent=2))
# 3x3 repeated previews reveal tiled rhythms and edges at actual size.
review=Image.new('RGB',(1024,1792),'#e9e2cc');d=ImageDraw.Draw(review)
for n in range(32):
 px=(n%4)*256;py=(n//4)*192;im=Image.open(O/f'texture-{n}.png');review.paste(im,(px+4,py+22));review.paste(im,(px+132,py+22));d.text((px+5,py+5),str(n)+' '+names[n],fill='#343e37')
for n,id in enumerate(resources):review.paste(Image.open(O/f'resource-{id}.png'),((n%6)*164+18,1570),Image.open(O/f'resource-{id}.png'));d.text(((n%6)*164+20,1710),id,fill='#343e37')
review.save(O/'review.jpg',quality=90);print('32 materials + 6 transparent resources authored')
