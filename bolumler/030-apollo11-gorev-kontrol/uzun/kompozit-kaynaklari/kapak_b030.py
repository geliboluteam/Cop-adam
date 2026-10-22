"""B030 v4 kapak: s14'ün bölüm kostümlü Meraklı'sı, yerel şaşkın yüz,
büyük v4 başlık. Yeni AI üretimi değildir; s14 kaynaklı kompozit.
Sadece kapak yüz ifadesi değişir, anlatı s14.png değiştirilmez.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'araclar'))
import thumbnail_yap as th
source=ROOT/'bolumler/030-apollo11-gorev-kontrol/uzun/gorseller/s14.png'
im=Image.open(source).convert('RGB')
# Remove only old dark smile/brows, interpolating nearby white head shading.
for box in [(1520,282,1590,312),(1476,173,1515,195),(1586,177,1629,203)]:
    mask=Image.new('L',im.size);mp=mask.load()
    for y in range(box[1],box[3]):
        for x in range(box[0],box[2]):
            if max(im.getpixel((x,y)))<155:mp[x,y]=255
    mask=mask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(.7))
    fill=im.copy();px=fill.load()
    for y in range(box[1]-4,box[3]+4):
        l=im.getpixel((box[0]-5,y));r=im.getpixel((box[2]+5,y))
        for x in range(box[0]-4,box[2]+4):
            t=(x-box[0]+5)/(box[2]-box[0]+10)
            px[x,y]=tuple(round(l[k]*(1-t)+r[k]*t) for k in range(3))
    im=Image.composite(fill,im,mask)
big=im.resize((3840,2160),Image.Resampling.LANCZOS);d=ImageDraw.Draw(big)
d.ellipse((1544*2,282*2,1574*2,326*2),fill='#fffefe',outline='#303936',width=7)
d.arc((1474*2,155*2,1521*2,194*2),195,315,fill='#343d39',width=6)
d.arc((1581*2,156*2,1630*2,200*2),205,322,fill='#343d39',width=6)
im=big.resize((1280,720),Image.Resampling.LANCZOS)
folder=ROOT/'kapaklar/thumbnail/sahne';folder.mkdir(exist_ok=True,parents=True)
scene=folder/'bolum-030.jpg';im.save(scene,quality=94)
th.kapak_yap('030',th.BOLUMLER['030'])
out=ROOT/'kapaklar/thumbnail/bolum-030.png'
record={'version':4,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'s14 reuse + local surprised mouth/brows + v4 PIL typography; no new AI generation','output':str(out.relative_to(ROOT)),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'long_only':True,'shorts':False}
(Path(__file__).parent/'KAPAK-KAYNAK.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
