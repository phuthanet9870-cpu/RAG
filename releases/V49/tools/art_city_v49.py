from pathlib import Path
from PIL import Image,ImageDraw
import random,math,json,base64,io
R=Path('/workspace/RAG');O=R/'assets/city-v49';O.mkdir(exist_ok=True)
def save(im,name):
 im.save(O/(name+'.png'));b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
icons={};colors={'c_phoenix':('#a53e28','#f6b34f'),'c_frost':('#4f92ad','#d9f5ed'),'c_moon':('#596f9b','#e1d4a4'),'c_shadow':('#342a48','#a277bf'),'c_sakura':('#a35c83','#f5c3d6'),'c_knight':('#ac8342','#f0de9c'),'c_jungle':('#426842','#b5c67a'),'c_aurora':('#4a8f88','#b6dbd9'),'c_beach':('#438baf','#f4d59a'),'c_lava':('#3b3b43','#e89368')}
for idx,(id,(coat,trim))in enumerate(colors.items()):
 im=Image.new('RGBA',(64,64));d=ImageDraw.Draw(im);d.rounded_rectangle((1,1,62,62),9,fill='#f1e8d5',outline='#705735',width=2);d.rounded_rectangle((4,4,59,59),7,fill='#30333a',outline=trim);d.polygon([(20,14),(27,11),(32,17),(37,11),(44,14),(54,29),(45,34),(40,27),(44,53),(20,53),(24,27),(19,34),(10,29)],fill=coat,outline='#171d25');d.line([(27,12),(32,20),(37,12)],fill=trim,width=3);d.line([(32,20),(32,51)],fill=trim,width=2);d.line([(21,48),(42,48)],fill=trim,width=2);d.rectangle((26,33,38,36),fill='#422f26');d.rectangle((30,32,34,37),fill=trim)
 if idx==0:d.polygon([(27,30),(25,24),(30,26),(32,20),(37,26),(35,31)],fill=trim)
 elif idx==1:
  for a in range(0,360,60):x,y=32+8*math.cos(math.radians(a)),26+8*math.sin(math.radians(a));d.line((32,26,x,y),fill=trim,width=2)
 elif idx==2:d.ellipse((25,19,39,32),fill=trim);d.ellipse((29,17,41,29),fill=coat)
 elif idx==3:d.polygon([(32,19),(39,26),(32,32),(25,26)],fill=trim);d.ellipse((30,24,34,28),fill='#30223b')
 elif idx==4:
  for a in range(0,360,72):x,y=32+5*math.cos(math.radians(a)),26+5*math.sin(math.radians(a));d.ellipse((x-3,y-3,x+3,y+3),fill=trim)
 elif idx==5:d.polygon([(25,20),(39,20),(38,29),(32,33),(26,29)],fill=trim);d.line((32,22,32,29),fill=coat,width=2)
 elif idx==6:d.ellipse((26,19,37,32),fill=trim);d.line((27,31,36,20),fill=coat,width=2)
 elif idx==7:
  for q in range(3):d.line([(23,23+q*3),(31,20+q*3),(40,24+q*3)],fill=trim,width=2)
 elif idx==8:
  d.rectangle((8,10,56,56),fill='#30333a');d.polygon([(24,14),(29,12),(32,20),(35,12),(40,14),(42,36),(22,36)],fill=coat,outline='#17212c');d.polygon([(22,38),(42,38),(41,50),(34,50),(32,43),(30,50),(23,50)],fill=trim,outline='#17212c');d.line([(24,28),(29,25),(34,28),(40,25)],fill='#e5ece7',width=2);d.ellipse((27,17,30,21),fill='#e5ece7');d.ellipse((34,17,37,21),fill='#e5ece7')
 else:d.polygon([(32,19),(39,28),(34,32),(31,27),(26,30)],fill=trim)
 icons[id]=save(im.resize((128,128),Image.Resampling.NEAREST),'icon-'+id)
textures=[]
# All grain is periodic; motifs wrap at tile edges rather than producing seams.
for n in range(32):
 kind='grass' if n in [1,2,4,5,6,7,8,10,13,15,28] else 'ice' if n==14 else 'sand' if n in [16,22,23,26,29] else 'lava' if n==24 else 'water' if n==30 else 'toxic' if n in [19,21,31] else 'stone' if n in [0,3,9,11,12,17,18,20,25,27] else 'grass'
 pal={'grass':(102,125,77),'stone':(172,164,141)if n==0 else (111,112,109),'sand':(194,166,119),'ice':(168,195,199),'lava':(87,70,66),'water':(53,123,148),'toxic':(78,100,74)};rng=random.Random(4900+n);im=Image.new('RGB',(64,64));pix=im.load();r,g,b=pal[kind]
 for y in range(64):
  for x in range(64):
   q=rng.uniform(-4,4)+3*math.sin(2*math.pi*x/64)*math.cos(2*math.pi*y/64);pix[x,y]=tuple(max(0,min(255,round(c+q)))for c in(r,g,b))
 d=ImageDraw.Draw(im)
 for i in range(80):
  x,y=rng.randrange(64),rng.randrange(64);v=rng.choice([-12,9,16]);col=tuple(max(0,min(255,c+v))for c in(r,g,b))
  for ox in [-64,0,64]:
   for oy in [-64,0,64]:
    if kind=='grass':d.line((x+ox,y+oy,x+ox+1,y+oy-3),fill=col)
    elif kind in ['water','sand','ice']:d.line((x+ox,y+oy,x+ox+5,y+oy+1),fill=col)
    else:d.point((x+ox,y+oy),fill=col)
 if kind=='stone':
  for y in range(-16,80,16):
   for x in range(-32,96,32):
    xx=x+(16 if y//16%2 else 0);d.rounded_rectangle((xx+1,y+1,xx+30,y+14),3,outline=tuple(max(0,c-15)for c in(r,g,b)));d.line((xx+5,y+2,xx+25,y+2),fill=tuple(min(255,c+11)for c in(r,g,b)))
 textures.append(save(im,'texture-'+str(n)))
resources={}
for kind in ['iron','gold','crystal','herb','timber','shell']:
 im=Image.new('RGBA',(64,64));d=ImageDraw.Draw(im);d.ellipse((7,49,59,60),fill=(25,32,27,45))
 if kind in ['iron','gold','crystal']:
  for j in range(3):
   x=10+j*15;y=28-j%2*10;col={'iron':'#7c8793','gold':'#c6a04c','crystal':'#67bbc4'}[kind];d.polygon([(x,y+25),(x-3,y+8),(x+7,y-5),(x+17,y+5),(x+18,y+24)],fill=col,outline='#35454a');d.line((x+7,y-3,x+7,y+22),fill='#dce5cb',width=2);d.polygon([(x+8,y),(x+16,y+6),(x+16,y+22),(x+8,y+22)],fill={'iron':'#536478','gold':'#8f7133','crystal':'#3e858f'}[kind])
 elif kind=='herb':
  for x,y in [(18,36),(28,28),(42,34),(34,43)]:d.line((32,54,x,y),fill='#405e31',width=3);d.ellipse((x-8,y-5,x+8,y+5),fill='#6b9855',outline='#375b37');d.ellipse((x-2,y-8,x+3,y-3),fill='#d0b8dc')
 elif kind=='timber':
  for y,x in [(48,10),(39,20),(29,13)]:d.rounded_rectangle((x,y-6,x+35,y+6),4,fill='#796047',outline='#413f31');d.ellipse((x+27,y-6,x+39,y+6),fill='#ba9769',outline='#6c5038');d.ellipse((x+31,y-3,x+36,y+3),outline='#8e6a45');d.line((x+4,y-2,x+25,y-2),fill='#ad8660')
 else:
  d.pieslice((12,18,55,59),180,360,fill='#c4aa98',outline='#7c7471',width=2)
  for x in range(18,52,6):d.line((33,56,x,29),fill='#e4d1b2',width=2)
 resources[kind]=save(im,'resource-'+kind)
(O/'data.json').write_text(json.dumps({'icons':icons,'textures':textures,'resources':resources},separators=(',',':')))
# Review contact sheet.
cv=Image.new('RGB',(640,360),'#e9e2d3');dr=ImageDraw.Draw(cv)
for i,(id,src)in enumerate(icons.items()):cv.paste(Image.open(O/('icon-'+id+'.png')).resize((64,64)),((i%10)*64,0),Image.open(O/('icon-'+id+'.png')).resize((64,64)));dr.text(((i%10)*64,66),id[2:10],fill='#302c28')
for n in range(32):cv.paste(Image.open(O/('texture-'+str(n)+'.png')),((n%10)*64,88+(n//10)*64))
cv.save(O/'review.jpg');print('10 icons / 32 materials / 6 resource sprites')
