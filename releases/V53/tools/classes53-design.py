from pathlib import Path
import json
R=Path('/workspace/RAG');O=R/'assets/classes-v53';O.mkdir(exist_ok=True)
# All six-skill kits are original Runevale designs. Values are rank1 + step per rank.
rows=[
('honor_guardian','ผู้พิทักษ์เกียรติยศ','knight','spear1','tank','#d4ba73','เกราะแห่งคำสัตย์','DEF',4,'ยืนแนวหน้า ลดความเสียหายและปกป้องทีม',[
('h53_lance','หอกตราสัตย์','strike',6,0,'p',0,'single','hit',2.2,.35,1,0,'stun',1),
('h53_call','บัญชาการแนวโล่','banner',12,0,None,0,'self','taunt',0,0,1,3,'weak',8),
('h53_wall','กำแพงเกียรติยศ','shield',20,.4,None,6,'party','guard',0,0,1,0,None,0),
('h53_sweep','กวาดหอกราชองครักษ์','crescent',9,0,'p',0,'self','cone',1.8,.3,1,4,'root',1.2),
('h53_oath','ป้อมปราการคำสัตย์','fortress',32,.8,'p',6,'self','fortress',2.5,.4,2,4,None,0)]),
('twilight_knight','อัศวินพลบค่ำ','crusader','sword2','fighter','#b798d1','สมดุลสนธยา','ATK',5,'สลับคมดาบเงาและเกราะแสง ดูดพลังคืนจากการโจมตี',[
('t53_edge','คมดาบสนธยา','crescent',5,0,'p',7,'single','drain',2.1,.35,1,0,None,0),
('t53_dusk','หมอกพลบค่ำ','mist',13,.5,'m',7,'ground','area',.8,.16,3,3,'slow',3),
('t53_ward','ม่านแสงสุดท้าย','shield',22,.3,None,6,'party','mguard',0,0,1,0,None,0),
('t53_cross','กางเขนจันทร์เสี้ยว','cross',10,.4,'m',6,'single','hit',2.4,.45,1,0,'weak',5),
('t53_eclipse','สุริยันลับฟ้า','eclipse',34,1,'m',7,'ground','area',1.1,.18,4,4,'slow',4)]),
('death_knight','อัศวินเงามรณะ','crusader','spear2','fighter','#8c78ae','เกราะวิญญาณ','HPpct',2,'อัศวินดูดชีวิต ควบคุมพื้นที่ด้วยพันธนาการเงา',[
('d53_reap','เคียวเก็บวิญญาณ','reaper',6,0,'p',7,'single','drain',2.3,.4,1,0,None,0),
('d53_chain','โซ่สุสาน','chain',12,.4,'m',7,'single','hit',1.8,.3,1,0,'root',2),
('d53_armor','เกราะวิญญาณทมิฬ','shield',24,.3,None,7,'self','selfguard',0,0,1,0,None,0),
('d53_dread','เสียงคร่ำครวญ','skull',13,.6,'m',7,'self','area',1.2,.2,2,3,'weak',6),
('d53_requiem','พิธีคืนชีพเงา','reaper',36,1,'p',7,'self','harvest',1.7,.28,3,4,None,0)]),
('storm_weaver','ผู้ทอพายุ','wizard','staff','caster','#81bedb','เส้นใยมรสุม','MATK',6,'ถักสายฟ้าเป็นชุด สร้างพายุและลมผลักศัตรู',[
('s53_threads','ด้ายอสนี','lightning',5,.4,'m',4,'single','hit',.75,.12,3,0,None,0),
('s53_vortex','วังวนเมฆคราม','tornado',12,.7,'m',4,'ground','area',.65,.13,4,3,'slow',3),
('s53_tailwind','ลมหนุนผู้ร่าย','wind',23,.4,None,4,'party','hastecast',0,0,1,0,None,0),
('s53_gale','กรรโชกฟ้าคะนอง','wind',9,.3,'m',4,'self','cone',1.8,.3,1,5,None,0),
('s53_tempest','ผืนฟ้ามหาพายุ','storm',35,1.2,'m',4,'ground','area',.75,.14,6,4,'stun',.6)]),
('ice_scholar','ปราชญ์น้ำแข็ง','sage','book','caster','#a7d4d7','ศาสตร์ผลึกเหมันต์','MATK',5,'ผลึกเยือกแข็งตรึงศัตรูและเกราะเหมันต์ปกป้องทีม',[
('i53_shards','บทผลึกสามแฉก','ice',5,.4,'m',1,'single','hit',.85,.14,3,0,'slow',2),
('i53_seal','อักขระธารตรึง','sigil',12,.6,'m',1,'ground','area',1.6,.25,1,3,'root',2),
('i53_coat','อาภรณ์น้ำค้าง','shield',24,.4,None,1,'party','mguard',0,0,1,0,None,0),
('i53_prison','คุกแก้วเยือกแข็ง','ice',11,.6,'m',1,'single','hit',2,.35,1,0,'freeze',1.5),
('i53_zero','ตำราเหมันต์นิรันดร์','blizzard',36,1.2,'m',1,'ground','area',.8,.14,5,4,'freeze',1)]),
('sniper','พลซุ่มยิง','hunter','bow','ranged','#b1c786','วิถีศรเงียบ','DEX',2,'นักแม่นธนู ยิงต่อเนื่อง ตรึงเป้าและเร่งความแม่นยำ',[
('n53_pierce','ศรเจาะขอบฟ้า','arrow',5,.2,'p',0,'single','hit',2.6,.45,1,0,None,0),
('n53_rain','ฝนศรดาวตก','arrowrain',12,.5,'p',0,'ground','area',.55,.1,5,3,None,0),
('n53_focus','สายตาเหยี่ยวราตรี','eye',22,.2,None,0,'self','focus',0,0,1,0,None,0),
('n53_tether','ศรพันธนาการป่า','vine',10,.3,'p',2,'single','hit',1.6,.25,1,0,'root',2),
('n53_horizon','หกศรทะลวงสุริยา','arrow',32,.8,'p',0,'single','hit',.8,.15,6,0,None,0)]),
('high_priest','นักบวชสูงสุด','priest','staff','healer','#e3d3a0','เมตตาแห่งรุ่งอรุณ','healPct',3,'นักบวชฟื้นพลัง ชำระสถานะและเรียกแสงชุบชีวิตทั้งทีม',[
('p53_heal','พรน้ำตารุ่งอรุณ','heal',6,.4,None,6,'ally','heal',0,0,1,0,None,0),
('p53_sanctum','วิหารแสงพิทักษ์','sanctum',22,.6,None,6,'party','guard',0,0,1,0,None,0),
('p53_judge','ตราชั่งเทวทูต','cross',10,.5,'m',6,'ground','holy',1.3,.25,2,3,None,0),
('p53_cleanse','ฝนชำระมลทิน','rainheal',18,.5,None,6,'party','cleanse',0,0,1,0,None,0),
('p53_return','ปีกแห่งวันใหม่','angel',55,1.8,None,6,'dead','revive',0,0,1,0,None,0)]),
('fist_champion','แชมเปี้ยนหมัด','monk','knuckle','fighter','#e1ab76','ลมหายใจยุทธ์','ASPD',2,'หมัดหลายจังหวะ ทำลายเกราะและระเบิดพลังประชิด',[
('f53_combo','หมัดสามประสาน','fist',5,0,'p',0,'single','hit',.7,.13,3,0,None,0),
('f53_crack','หมัดร้าวพสุธา','fissure',11,.2,'p',2,'single','break',2,.35,1,0,None,0),
('f53_breath','ลมหายใจมังกรขาว','orbit',23,.2,None,0,'self','fury',0,0,1,0,None,0),
('f53_roar','คำรามฝ่าคลื่น','fist',10,.2,'p',0,'self','cone',1.6,.3,1,4,'stun',.8),
('f53_infinity','แปดหมัดไร้ขอบเขต','fist',34,.8,'p',0,'single','hit',.55,.1,8,0,None,0)]),
('white_smith','ช่างเหล็กขาว','blacksmith','axe2','fighter','#ddbe88','ศาสตร์เหล็กกล้าขาว','ATK',6,'ค้อนหนักทำลายเกราะ หลอมอาวุธและคุ้มกันทั้งทีม',[
('w53_hammer','ค้อนประกายเงิน','hammer',6,.2,'p',0,'self','area',1.6,.3,1,2.5,'stun',1),
('w53_forge','เพลิงหลอมคมศึก','forge',24,.5,None,3,'party','warcry',0,0,1,0,None,0),
('w53_rivet','ตอกหมุดแยกเกราะ','fissure',10,.2,'p',0,'single','break',2.3,.35,1,0,None,0),
('w53_temper','ชุบเกราะผลึกเงิน','shield',25,.5,None,0,'party','mguard',0,0,1,0,None,0),
('w53_anvil','ทั่งพิพากษาอุกกาบาต','anvil',35,1,'p',3,'ground','area',1.2,.23,3,4,'stun',1)]),
('life_creator','ผู้สร้างชีวิต','alchemist','axe1','healer','#a7c882','ชีววิทยาเวท','SPpct',3,'ปรุงกรด ฟื้นชีวิตและสร้างพื้นที่ชีวพิษที่แยกมิตรศัตรู',[
('l53_acid','ขวดกรดผลึกชีวะ','flask',6,.3,'m',5,'single','break',1.9,.3,1,0,None,0),
('l53_heal','สารสกัดคืนชีวิต','heal',8,.4,None,0,'ally','healclean',0,0,1,0,None,0),
('l53_spore','สปอร์พันธนาการ','spore',13,.6,'m',5,'ground','area',.7,.12,3,3,'poison',8),
('l53_bloom','เยื่อหุ้มชีวะ','bloom',25,.5,None,0,'party','vital',0,0,1,0,None,0),
('l53_genesis','สวนกำเนิดชีวิต','garden',38,1.2,'m',5,'ground','garden',.65,.12,5,4,'poison',10)]),
('cross_assassin','มือสังหารกากบาท','assassin','katar','fighter','#b89bc9','จังหวะคมกากบาท','CRIT',2,'กากบาทพิษ จู่โจมประชิดและพรางพื้นที่ด้วยหมอกอ่อนแรง',[
('c53_cross','คมกากบาทพิษ','crossslash',5,0,'p',5,'single','hit',.6,.12,4,0,'poison',6),
('c53_step','ก้าวเงาเฉือนจันทร์','shadow',10,.2,'p',7,'single','dash',2,.35,1,0,None,0),
('c53_focus','สมาธิคมสังหาร','eye',23,.2,None,0,'self','focus',0,0,1,0,None,0),
('c53_smoke','หมอกพิษบังจิต','mist',13,.3,'p',5,'self','area',1.1,.2,1,3,'weak',5),
('c53_final','สิบทัณฑ์กากบาทราตรี','crossslash',35,.8,'p',7,'single','hit',.45,.08,10,0,None,0)]),
('shadow_stalker','นักติดตามเงา','rogue','bow','ranged','#aa9bc4','รอยเท้าไร้เสียง','FLEE',4,'จับรอยเงา ตรึงศัตรูและขยายความได้เปรียบจากพันธนาการ',[
('r53_echo','ศรสะท้อนเงา','arrow',5,.2,'p',7,'single','hit',1,.18,2,0,None,0),
('r53_web','ตาข่ายรอยเงา','web',12,.5,'m',7,'ground','area',1.3,.2,1,3,'root',2),
('r53_veil','ย่างเท้าจันทร์ดับ','wind',24,.3,None,7,'party','evasion',0,0,1,0,None,0),
('r53_sever','ตัดรอยชะตา','crossslash',10,.3,'p',7,'single','execute',2,.3,1,0,None,0),
('r53_hunt','ล่าเงาห้าทิศ','shadow',34,.9,'p',7,'ground','area',.8,.15,5,4,'weak',4)])]
classes=[];skills=[]
for ci,(id,name,parent,wt,role,color,pname,stat,bonus,blurb,acts)in enumerate(rows):
 p={'id':id,'name':name,'parent':parent,'weapon':wt,'role':role,'color':color,'blurb':blurb};classes.append(p)
 passive={'id':id+'_53_mastery','name':pname,'cls':id,'passive':True,'stat':stat,'bonus':bonus,'shape':'crest','color':color,'max':5};skills.append(passive)
 for i,row in enumerate(acts):
  sid,n,shape,cd,cast,k,el,target,mechanic,mul,step,hits,r,status,duration=row
  req=[[passive['id'],2]]if i==0 else[[acts[0][0],3]]if i==1 else[[passive['id'],3]]if i==2 else[[acts[1][0],3]]if i==3 else[[acts[0][0],5],[acts[1][0],5]]
  skills.append({'id':sid,'name':n,'cls':id,'shape':shape,'color':color,'cd':cd,'cast':cast,'k':k,'el':el,'target':target,'mechanic':mechanic,'mul':mul,'step':step,'hits':hits,'radius':r,'status':status,'statusDuration':duration,'req':req,'max':5,'sp':(45 if i==4 else 16+i*3),'spStep':(4 if i==4 else 2),'range':(10 if role=='ranged'else 9 if role in ['caster','healer']else 3 if i in [0,4]else 7),'ultimate':i==4})
(O/'design.json').write_text(json.dumps({'classes':classes,'skills':skills},ensure_ascii=False,indent=2));print(len(classes),'classes',len(skills),'skills')
