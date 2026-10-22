"""B030 son grup: uzuvları doğru kaynak sahnelerle temsili kompozitler.
AI taslaklarında s15b/s20 kesik ayak, s17 gizli kol, s19 örtüşen eller,
s19b eksik yüz çizgileri vardı. Bu taslakları kullanmak yerine PASS kaynak
s14/s15/s12b/s16 yeniden kullanılır. Tüm ek şemalar bu betikte çizilir;
NASA arşivi/ölçülü mühendislik çizimi değildir. Hiçbir figür rötuşlanmaz.
Çalıştırma: python <bu_dosya>. Kaynak PNG'ler önce 1920x1080 olmalıdır.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math, json, hashlib
ROOT=Path(__file__).resolve().parents[4]
G=ROOT/'bolumler/030-apollo11-gorev-kontrol/uzun/gorseller'
S=3
records=[]

def start(source):
    im=Image.open(G/f'{source}.png').convert('RGBA')
    assert im.size==(1920,1080)
    layer=Image.new('RGBA',(1920*S,1080*S));d=ImageDraw.Draw(layer)
    return im,layer,d

def poly(d,pts,fill='#e3e1c9',outline='#42483f',width=2):
    pp=[(round(x*S),round(y*S)) for x,y in pts];d.polygon(pp,fill=fill)
    if outline:d.line(pp+[pp[0]],fill=outline,width=width*S,joint='curve')

def line(d,pts,fill='#42483f',width=2):
    d.line([(round(x*S),round(y*S)) for x,y in pts],fill=fill,width=width*S,joint='curve')

def ellipse(d,box,fill=None,outline='#42483f',width=2):
    d.ellipse(tuple(round(v*S) for v in box),fill=fill,outline=outline,width=width*S)

def finish(id,source,im,layer,operation):
    im=Image.alpha_composite(im,layer.resize(im.size,Image.Resampling.LANCZOS)).convert('RGB')
    im.save(G/f'{id}.png')
    records.append({'id':id,'source':f'{source}.png','source_sha256':hashlib.sha256((G/f'{source}.png').read_bytes()).hexdigest(),'operation':operation,'final_sha256':hashlib.sha256((G/f'{id}.png').read_bytes()).hexdigest()})

# s15b: source s14 has four fully visible people. Recorder on upper-left wall
# is our schematic illustration, not evidence of an actual recorder location.
im,layer,d=start('s14')
poly(d,[(72,221),(338,221),(345,232),(66,232)],'#868c7d')
poly(d,[(85,77),(325,77),(325,219),(85,219)],'#9fa598')
poly(d,[(93,85),(317,85),(317,211),(93,211)],'#c7cbbd')
for cx in (151,258):
    ellipse(d,(cx-40,86,cx+40,166),'#dadbc9')
    ellipse(d,(cx-11,115,cx+11,137),'#626b61')
    for angle in (0,120,240):
        a=math.radians(angle);x=cx+25*math.cos(a);y=126+25*math.sin(a)
        ellipse(d,(x-6,y-6,x+6,y+6),'#777f73',width=1)
line(d,[(151,161),(180,179),(228,179),(258,161)],width=2)
poly(d,[(107,180),(147,180),(147,194),(107,194)],'#6e7a70')
for x in (190,224,258,292):ellipse(d,(x-6,185,x+6,197),'#778174',width=1)
finish('s15b','s14',im,layer,'Dört tam boy PASS figürlü s14 tabanı + kendi çizdiğimiz temsili makaralı kayıt aygıtı; s15b kesik ayaklı AI taslağı kullanılmadı.')

# s17: source s15 already has four front-facing, fully clothed figures.
im,layer,d=start('s15')
for i in range(4):
    dx=i*3;dy=-i*4
    poly(d,[(697+dx,641+dy),(774+dx,636+dy),(802+dx,657+dy),(720+dx,665+dy)],'#e8e6d0',width=1)
for y in (641,646,651):line(d,[(728,y),(768,y-3)],'#8e9282',1)
finish('s17','s15',im,layer,'s15 tam boy/dört açık kollu figür tabanı + kendi kontrol kâğıdı çizimimiz; arkası dönük/gizli kollu s17 AI taslağı kullanılmadı.')

# s19: source s12b has separated hands. Explanatory paper is deliberately
# tiny; no claim that this schematic is telemetry or an engineering plan.
im,layer,d=start('s12b')
poly(d,[(75,604),(161,597),(238,700),(128,719)],'#dedec5',None)
ellipse(d,(133,671,166,696),None,width=1)
# Angular ascent-stage symbol and conical command/cylindrical service stage.
poly(d,[(130,640),(146,634),(156,644),(151,656),(134,655)],'#b2b8a9',width=1)
line(d,[(134,654),(130,664),(151,656),(157,664)],width=1)
poly(d,[(178,630),(188,622),(198,630),(192,637)],'#b9c0b2',width=1)
poly(d,[(188,622),(199,617),(209,626),(198,630)],'#a1aea0',width=1)
line(d,[(149,674),(146,660),(148,665)],width=1)
line(d,[(155,645),(170,637),(178,632)],width=1)
finish('s19','s12b',im,layer,'El örtüşmesi olmayan s12b tabanındaki kâğıda kendi temsili yükseliş/buluşma şemamız; örtüşen elli s19 taslağı kullanılmadı.')

# s19b: source s16 has canonical faces and open limbs. Replace only the
# paper interior, safely far to the right of all people.
im,layer,d=start('s16')
poly(d,[(1686,500),(1892,507),(1878,790),(1661,773)],'#e8e5cf',None)
for cx,cy,r in [(1711,571,30),(1777,552,37),(1840,576,30)]:
    pts=[]
    for i in range(21):
        a=math.pi+i*math.pi/20;pts.append((cx+r*math.cos(a),cy+r*.65*math.sin(a)))
    pts.extend([(cx+r,cy+3),(cx-r,cy+3)])
    poly(d,pts,'#e4e2cb',width=1)
    for frac in (-.6,0,.6):line(d,[(cx+r*frac,cy-r*.52),(cx+r*frac*.65,cy+3)],'#7a7d6c',1)
    for x in (cx-r+3,cx,cx+r-3):line(d,[(x,cy+3),(1780,699)],'#6b7568',1)
poly(d,[(1777,692),(1806,732),(1756,732)],'#bcc4b3',width=2)
poly(d,[(1756,732),(1806,732),(1800,740),(1762,740)],'#929f90',width=1)
poly(d,[(1777,710),(1787,719),(1777,725),(1768,718)],'#586e64',width=1)
for y in (744,758):
    pts=[]
    for x in range(1680,1870,3):pts.append((x,y+3*math.sin((x-1680)/11)))
    line(d,pts,'#6b796c',1)
finish('s19b','s16',im,layer,'Kanonik yüzlü/dört tam boy s16 tabanı + kendi paraşüt/kapsül/deniz şemamız; eksik yüzlü s19b taslağı kullanılmadı. Tarih bandı 24 Temmuz olacak.')

# s20: full-body s14 reuse, open EMPTY hands rather than a cropped wave.
# Only extra checklists on the rear console; closing/subscribe cards are
# separate video cards, never painted over the figures here.
im,layer,d=start('s14')
for i in range(3):
    dx=i*2;dy=i*3
    poly(d,[(902+dx,596+dy),(963+dx,594+dy),(976+dx,614+dy),(914+dx,618+dy)],'#e4e2cf',width=1)
for y in (601,607):line(d,[(919,y),(956,y-2)],'#909781',1)
finish('s20','s14',im,layer,'Tam boy s14 tabanı ve kontrol kâğıdı çizimleri. Meraklı iki eli açık/aşağıda kapanış yapar, el sallama iddiası yok; kesik ayaklı s20 taslağı kullanılmadı.')
(Path(__file__).parent/'SON-GRUP-KOMPOZITLER.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print('5 kompozit yazıldı; görsel QA hâlâ gereklidir.')
