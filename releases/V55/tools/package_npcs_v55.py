from pathlib import Path
from PIL import Image
import json,hashlib,zipfile,html
R=Path('/workspace/RAG');E=R/'evidence/npcs-v55';A=R/'assets/npcs-v55';O=R/'build/Runevale-Recast-V55';v=json.loads((E/'validation.json').read_text());assert not v['browserErrors'];assert v['npcRoles']==20 and len(v['npcLocations'])==30;sha=hashlib.sha256((O/'index.html').read_bytes()).hexdigest();assert sha==v['htmlSha256']==json.loads((E/'build.json').read_text())['htmlSha256']
s=(O/'index.html').read_bytes().decode('latin1');base=(R/'build/Runevale-Recast-V54/index.html').read_bytes().decode('latin1');preserved=[]
for m in ['const WORLD33_MATERIALS=','const WORLD33_PLANS=','const WORLD33_PLACEMENTS=','window.SHEET_DATA=','window.COSTUME36_DATA=','window.MONSTER_DATA=','const Unlock53Design=','window.VFX47_LIBRARY=','window.SKILL_FX_DATA=']:
 def get(t):return json.JSONDecoder().raw_decode(t,t.index(m)+len(m))[0]
 assert get(s)==get(base),m;preserved.append(m)
a='const NPCS =';b='const SHOP_LIST';assert s[s.index(a):s.index(b)]==base[base.index(a):base.index(b)]
(E/'preservation.json').write_text(json.dumps({'base':54,'unchangedData':preserved,'npcLocationsAndServicesUnchanged':True,'newRenderingOnly':True},indent=2))
roles=json.loads((A/'design.json').read_text())['roles'];atlas=Image.new('RGBA',(960,640));meta=[]
for i,d in enumerate(roles):
 f=Image.open(A/'sprites'/(d['id']+'.png'));x=i%5*192;y=i//5*160;atlas.alpha_composite(f,(x,y));meta.append({**d,'sprite':'sprites/'+d['id']+'.png','master':'masters/'+d['id']+'.png','rect':[x,y,192,160],'pivot':[96,144],'direction':'front','action':'standing','frames':1,'fps':0,'loop':False})
atlas.save(A/'npc-front-atlas.png',optimize=True);(A/'manifest.json').write_text(json.dumps({'version':55,'npcRoles':20,'spawnLocations':v['npcLocations'],'atlas':'npc-front-atlas.png','atlasSize':[960,640],'frameSize':[192,160],'transparent':True,'actions':['standing'],'directions':['front'],'framesPerNpc':1,'records':meta},ensure_ascii=False,indent=2))
preview='''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Runevale NPC V55</title><style>body{background:#ece5d5;color:#302e25;font:16px system-ui;margin:20px;padding:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}article{background:#faf7ef;border:1px solid #b49e70;border-radius:12px;padding:14px}img{image-rendering:pixelated;max-width:100%;height:auto}a{display:block;color:#6e542c;margin-top:10px}</style><h1>NPC20บทบาท · ยืนด้านหน้า1เฟรม</h1><p>PNGโปร่งใส เฟรม192×160 จุดยึดเท้า96,144 · ไม่มีอนิเมชันและไม่มีทิศอื่น</p><div class="grid">'''
for d in roles:preview+='<article><img src="sprites/'+d['id']+'.png" width="192" height="160" alt="'+html.escape(d['name'])+'"><h2>'+html.escape(d['name'])+'</h2><p>'+html.escape(d['service'])+'</p><a href="sprites/'+d['id']+'.png">PNG · '+d['id']+'</a><a href="masters/'+d['id']+'.png">ภาพต้นฉบับแยกตัว</a></article>'
preview+='</div></html>';(A/'preview.html').write_text(preview)
(O/'อ่านก่อนเล่น.txt').write_text('''Runevale V55 — NPCใหม่ยืนด้านหน้า
แตกZIP แล้วเปิด index.html ภาพทั้งหมดฝังในเกม
ออกแบบNPC20บทบาท รวม30จุดในเมืองหลัก เมืองคาราวาน และโถงปราสาท
NPCทุกคนยืนหันหน้าตรง1เฟรม ไม่หันตามผู้เล่น ไม่เดิน ไม่ใช้ท่าต่อสู้และไม่มีเอฟเฟกต์บนตัว
รูปลักษณ์แยกตามหน้าที่และชื่อเดิม เช่นช่างตีเหล็ก พ่อค้า ผู้ดูแลคลัง อาจารย์อาชีพ และผู้สุ่มคอสตูม
GM: G > stefan-gm > NPCใหม่V55 เพื่อดูภาพ ไปจุดบริการ ทดสอบบริการ และวางตัวอย่างใกล้ตัว
ปุ่มลบNPCตัวอย่างจะลบเฉพาะตัวที่GMวางเพิ่ม ไม่ลบจุดบริการจริง
คงชื่อ บริการ ผังเมือง ตำแหน่ง สกิล VFX ตัวละครผู้เล่น ทหาร และมอนสเตอร์จากV54
ทดสอบNPCทุก20บทบาท 30จุด เดินถึงได้และเปิดบริการได้ครบ
ทดสอบเปลี่ยนมุมfaceและเวลา8แบบต่อNPCแล้วยังคงภาพเดิมทุกครั้ง
ทดสอบChromiumเดสก์ท็อปและขนาดจอมือถือจำลอง ไม่ใช่มือถือจริง
''')
(A/'อ่านก่อนใช้งาน.txt').write_text('''เปิดpreview.htmlเพื่อดูNPC20บทบาทพร้อมชื่อและหน้าที่
sprites/ มีPNGโปร่งใส20ไฟล์ ไฟล์ละ1เฟรม192×160
masters/ มีภาพต้นฉบับแยกตัวละคร ไม่ใช่ภาพขยายจากเฟรมขนาดเล็ก
npc-front-atlas.png รวม20ตัวในกริด5คอลัมน์4แถว ขนาด960×640 ไม่มีข้อความทับภาพ
ดูตำแหน่งrectและจุดยึดเท้า96,144จากmanifest.json
ทุกตัวมีเฉพาะท่ายืนหันหน้าตรง ไม่มีอนิเมชัน ไม่มีทิศอื่น ไม่มีVFX
''')
packs=[]
for name,root in [('Runevale-Recast-V55.zip',O),('Runevale-NPC-Front-Sprites-V55.zip',A)]:
 p=R/'dist'/name
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for f in root.rglob('*'):
   if f.is_file()and f.name!='embedded.json':z.write(f,str(f.relative_to(root.parent)))
 with zipfile.ZipFile(p)as z:
  assert z.testzip()is None
  if root==O:assert hashlib.sha256(z.read(O.name+'/index.html')).hexdigest()==sha
 packs.append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(E/'packages.json').write_text(json.dumps(packs,indent=2));print(packs,flush=True)
