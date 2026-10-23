from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageColor
import json,math,random,io,base64,hashlib
R=Path('/workspace/RAG');O=R/'assets/classes-v53';design=json.loads((O/'design.json').read_text());lib={};fx={};icons={};thumbs=[]
def src(im):
 b=io.BytesIO();im.save(b,format='PNG',optimize=True);return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def render(s,j):
 im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im);p=j/11;ease=math.sin(p*math.pi)**.55;rr=12+39*ease;shape=s['shape'];seed=sum(map(ord,s['id']));rng=random.Random(seed);col=ImageColor.getrgb(s['color']);el=s.get('el');colors={1:(148,204,218),2:(182,153,98),3:(233,157,83),4:(143,190,219),5:(155,191,91),6:(229,209,143),7:(170,135,200)};col=colors.get(el,col);hi=tuple(min(255,int(v*.3+177))for v in col);dark=tuple(int(v*.55)for v in col);cx,cy=64,70
 def line(pts,w=3,c=col):d.line(pts,fill=c,width=w,joint='curve')
 def orb(x,y,r,c=col):
  d.ellipse((x-r,y-r,x+r,y+r),fill=c);d.ellipse((x-r*.6,y-r*.7,x+r*.3,y+r*.2),fill=hi)
 def star(x,y,r):d.polygon([(x,y-r),(x+r*.23,y-r*.23),(x+r,y),(x+r*.23,y+r*.23),(x,y+r),(x-r*.23,y+r*.23),(x-r,y),(x-r*.23,y-r*.23)],fill=hi)
 def ring(rad,yy=78):
  d.ellipse((cx-rad,yy-rad*.38,cx+rad,yy+rad*.38),outline=col,width=2)
  for a in range(0,360,45):
   ang=math.radians(a)+p*.7;px=cx+math.cos(ang)*rad;py=yy+math.sin(ang)*rad*.38;line([(px-2,py-2),(px+2,py+2)],2,hi)
 if shape in ['crest','shield','fortress','sanctum','banner']:
  ring(rr,99);w=18+ease*12;h=30+ease*12;yy=57
  d.polygon([(cx-w,yy-h*.5),(cx,yy-h),(cx+w,yy-h*.5),(cx+w*.8,yy+h*.5),(cx,yy+h),(cx-w*.8,yy+h*.5)],fill=(*dark,230),outline=col);line([(cx-w+3,yy-h*.5),(cx,yy-h+4),(cx+w-3,yy-h*.5)],3,hi);line([(cx,yy-h+8),(cx,yy+h-7)],3);line([(cx-12,yy),(cx+12,yy)],3)
  if shape in ['fortress','sanctum']:
   for xx in [22,42,86,106]:line([(xx,102),(xx,60-15*ease)],4);d.rectangle((xx-4,52-15*ease,xx+4,61-15*ease),fill=hi)
  if shape=='banner':line([(29,108),(29,24)],3,hi);d.polygon([(30,25),(58,30),(58,55),(45,49),(30,53)],fill=col)
 elif shape in ['crescent','reaper','crossslash','strike','shadow']:
  a=-120+p*190;rx=18+37*ease
  for offs,w,c in [(0,10,col),(-3,4,hi),(6,2,dark)]:d.arc((64-rx,64-rx*.78+offs,64+rx,64+rx*.78+offs),a,a+125,fill=c,width=w)
  if shape=='crossslash':
   d.arc((21,15,109,106),180-a,310-a,fill=hi,width=5)
  if shape=='strike':line([(28,92),(93,28),(84,49)],5,hi)
  if shape=='reaper':line([(44,111),(83,31)],4,col);d.arc((43,16,115,70),185,350,fill=hi,width=8)
  if shape=='shadow':
   for q in range(3):d.arc((17+q*13,34,54+q*13,97),110,255,fill=(*col,100+q*45),width=7)
 elif shape in ['lightning','storm']:
  ring(rr,103)
  for q in range(1 if shape=='lightning'else 4):
   xx=64 if q==0 else 25+q*22;offs=math.sin(j*1.6+q)*7;pts=[(xx+8,12),(xx-7+offs,40),(xx+4,43),(xx-9-offs,70),(xx+2,70),(xx-5,101)];line(pts,7,col);line(pts,3,hi)
 elif shape in ['tornado','wind']:
  for q in range(5):
   yy=103-q*15;w=(18+q*7)*(.5+ease*.5);offs=math.sin(p*9+q)*8;d.arc((64-w+offs,yy-8,64+w+offs,yy+8),int(p*250+q*22),int(p*250+q*22+250),fill=col,width=4);d.arc((64-w+offs,yy-8,64+w+offs,yy+8),int(p*250+q*22),int(p*250+q*22+120),fill=hi,width=2)
 elif shape in ['ice','blizzard']:
  ring(rr,104)
  for q in range(3 if shape=='ice'else 7):
   xx=64+(q-(1 if shape=='ice'else 3))*13;hh=(25+22*ease)*(1 if q%2 else 1.4);base=99+(q%2)*7;d.polygon([(xx-7,base-5),(xx-7,base-hh*.65),(xx,base-hh),(xx+8,base-hh*.65),(xx+8,base-6),(xx,base+1)],fill=col,outline=dark);d.polygon([(xx,base-hh),(xx+8,base-hh*.65),(xx+8,base-6),(xx,base+1)],fill=hi)
 elif shape in ['arrow','arrowrain']:
  for q in range(1 if shape=='arrow'else 5):
   xx=22+q*18 if shape=='arrowrain'else 64;yy=22+q%2*12 if shape=='arrowrain'else 64;ang=1.2 if shape=='arrowrain'else 0;dx=math.cos(ang);dy=math.sin(ang);length=26+ease*25;line([(xx-dx*length,yy-dy*length),(xx+dx*length*.65,yy+dy*length*.65)],3,col);tip=(xx+dx*length*.85,yy+dy*length*.85);d.polygon([tip,(tip[0]-dx*14+dy*7,tip[1]-dy*14-dx*7),(tip[0]-dx*10,tip[1]-dy*10),(tip[0]-dx*14-dy*7,tip[1]-dy*14+dx*7)],fill=hi)
 elif shape in ['heal','rainheal','cross']:
  ring(rr,105)
  for q in range(1 if shape=='cross'else 4):
   xx=64 if q==0 else 28+(q-1)*32;yy=55 if q==0 else 50+math.sin(p*5+q)*18;sz=15 if q==0 else 6;d.rectangle((xx-3,yy-sz,xx+3,yy+sz),fill=hi);d.rectangle((xx-sz,yy-3,xx+sz,yy+3),fill=hi)
  if shape in ['heal','rainheal']:
   for xx in [25,49,78,101]:line([(xx,96),(xx,48-20*ease)],2,(*col,190))
 elif shape=='angel':
  ring(rr,105);d.ellipse((54,17,74,25),outline=hi,width=2);d.ellipse((59,31,69,42),fill=hi);d.polygon([(64,43),(52,78),(76,78)],fill=col)
  for side in [-1,1]:
   for q in range(5):line([(64+side*9,48+q*3),(64+side*(37+q*3)*ease,23+q*9)],5-q//2,hi)
 elif shape in ['fist','hammer','anvil','fissure','forge']:
  ring(rr,105)
  if shape=='fist':
   xx=61+math.sin(p*3.14)*12;d.rounded_rectangle((xx-20,42,xx+19,80),7,fill=col,outline=hi,width=2)
   for q in range(4):d.rounded_rectangle((xx-18+q*9,33,xx-10+q*9,56),3,fill=hi,outline=col)
   d.rounded_rectangle((xx+8,56,xx+26,70),4,fill=col,outline=hi)
  elif shape in ['hammer','anvil']:
   yy=25+ease*38;d.polygon([(40,yy-8),(89,yy-8),(100,yy+2),(83,yy+8),(80,yy+25),(45,yy+25),(44,yy+9),(30,yy+4)],fill=dark,outline=col);line([(40,yy-8),(89,yy-8),(100,yy+2)],3,hi);line([(62,yy+8),(62,yy+23)],3,col)
  for q in range(7):
   a=q*2.399;rrr=15+35*p;xx=64+math.cos(a)*rrr;yy=98+math.sin(a)*rrr*.4;line([(64,98),(xx,yy)],2,col);d.polygon([(xx,yy-4),(xx+4,yy),(xx,yy+3),(xx-3,yy)],fill=hi)
 elif shape in ['mist','spore','skull','eclipse']:
  for q in range(9):
   a=q*2.399+p*1.8;rad=12+ease*22;xx=64+math.cos(a)*rad;yy=73+math.sin(a)*rad*.6-15*p;rrr=9+5*ease;d.ellipse((xx-rrr,yy-rrr,xx+rrr,yy+rrr),fill=(*dark,170),outline=(*col,210))
  if shape=='skull':
   d.ellipse((47,35,81,70),fill=col);d.rectangle((54,61,75,77),fill=col);d.ellipse((53,48,61,59),fill=dark);d.ellipse((67,48,75,59),fill=dark)
  elif shape=='eclipse':d.ellipse((37,25,91,79),fill=col);d.ellipse((48,18,96,70),fill=(*dark,255));d.arc((33,20,95,84),80,310,fill=hi,width=3)
 elif shape in ['chain','vine','web','garden','bloom']:
  ring(rr,104)
  for q in range(5):
   xx=27+q*18;pts=[(xx,105),(xx+math.sin(q+p*7)*10,83),(xx-8,62),(xx+4,43+12*(1-ease))];line(pts,3,col)
   if shape in ['garden','bloom','vine']:
    for yy in [65,85]:d.polygon([(xx,yy),(xx-12,yy-12),(xx-5,yy-14),(xx+2,yy-4)],fill=col);line([(xx,yy),(xx-8,yy-10)],1,hi)
   else:
    for yy in [65,80,95]:d.ellipse((xx-4,yy-6,xx+4,yy+6),outline=hi,width=2)
  if shape=='web':
   for yy in [52,74,96]:d.arc((20,yy-10,108,yy+10),0,180,fill=hi,width=2)
  if shape=='garden':
   for xx in [35,64,92]:star(xx,48,6)
 elif shape in ['eye','orbit','sigil']:
  ring(rr,90);d.ellipse((25,36,103,83),outline=col,width=3);orb(64,59,12+4*ease)
  if shape=='eye':d.polygon([(27,59),(48,42),(80,42),(101,59),(80,76),(48,76)],outline=hi);d.rectangle((62,50,66,68),fill=dark)
  else:
   for q in range(6):a=q*math.pi/3+p*2;orb(64+math.cos(a)*38,59+math.sin(a)*27,4)
 elif shape=='flask':
  yy=60+math.sin(p*math.pi)*-12;d.polygon([(57,yy-27),(72,yy-27),(72,yy-11),(88,yy+7),(84,yy+25),(44,yy+25),(40,yy+7),(57,yy-11)],fill=(*col,220),outline=hi);d.rectangle((56,yy-31,74,yy-23),fill=dark);d.ellipse((49,yy+3,79,yy+22),fill=col);line([(49,yy+5),(59,yy-4)],3,hi)
 else:ring(rr);star(64,60,20*ease+6)
 # Consistent sparks; positions and silhouettes progress in each native frame.
 for q in range(7):
  a=rng.random()*math.pi*2;rad=18+p*42;xx=64+math.cos(a)*rad;yy=70+math.sin(a)*rad*.7;star(xx,yy,max(.7,2.5*(1-p)))
 glow=im.filter(ImageFilter.GaussianBlur(2));glow.putalpha(glow.getchannel('A').point(lambda v:v//4));return Image.alpha_composite(glow,im)
for si,s in enumerate(design['skills']):
 atlas=Image.new('RGBA',(1536,128));frames=[]
 for j in range(12):
  im=render(s,j);atlas.paste(im,(j*128,0));frames.append(im)
 atlas.save(O/(s['id']+'.png'),optimize=True);family='u53_'+s['id'];grounded=s.get('radius',0)>0 or s.get('target')in ['party','ally','self','dead']or s.get('passive');anchor=[64,108]if grounded else[64,64]
 lib[family]={'src':src(atlas),'frameSize':128,'frameCount':12,'sourceFrameCount':12,'subframes':1,'anchor':anchor,'grounded':bool(grounded),'frameRects':[[j*128,0,128,128,0,0]for j in range(12)],'packed':True,'version':53}
 m=s.get('mechanic');target=s.get('target');pattern='passive'if s.get('passive')else'projectile'if target=='single'and s['shape']in ['arrow','flask','lightning']else'heal'if m in ['heal','healclean']else'party'if target=='party'else'revive'if m=='revive'else'taunt'if m=='taunt'else'area'if s.get('radius')else'shield'if target=='self'else'strike'
 fx[s['id']]={'id':s['id'],'name':s['name'],'cls':s['cls'],'type':'passive'if s.get('passive')else'active','element':s.get('el'),'family':family,'impact':family,'grounded':bool(grounded),'pattern':pattern,'duration':1 if s.get('ultimate')else .65,'frameCount':12,'version':53}
 icon=Image.new('RGBA',(64,64),'#292d36');d=ImageDraw.Draw(icon);d.rounded_rectangle((1,1,62,62),9,outline=s['color'],width=2);f=frames[5].resize((60,60),Image.Resampling.LANCZOS);icon.alpha_composite(f,(2,2));d.rectangle((5,53,5+si%12*3,56),fill=s['color']);icons[s['id']]=src(icon);icon.save(O/(s['id']+'-icon.png'));thumbs.append((s,icon))
review=Image.new('RGB',(960,720),'#ece5d3');d=ImageDraw.Draw(review)
for i,(s,im)in enumerate(thumbs):
 xx=i%12*80;yy=i//12*120;review.paste(im,(xx+8,yy+8),im);d.text((xx+4,yy+80),s['id'][:12],fill='#333333')
review.save(O/'review.jpg',quality=90);(O/'vfx.json').write_text(json.dumps({'library':lib,'fx':fx,'icons':icons},separators=(',',':')));print('72 unique atlases / 864 native frames + 72 icons',flush=True)
