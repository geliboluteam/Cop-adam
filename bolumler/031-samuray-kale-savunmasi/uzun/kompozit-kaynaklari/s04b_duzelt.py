#!/usr/bin/env python3
"""s04b: üçyanfigürlüAIv1tabanına s03'ün bağımsıztamgövdeaskerini ekler.
AIv2'de Meraklıkolu habercigövdesine taşıyordu; onu kullanmayız.
YeniAIgörseli gibi sunulmaz. Meraklı veonaylıs01değişmez.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import hashlib,json
ROOT=Path(__file__).resolve().parents[4];B=Path(__file__).resolve().parents[2]
base_path=Path(__file__).with_name('s04b-temel.png');source=B/'uzun/gorseller/s03.png';out=B/'uzun/gorseller/s04b.png'
base=Image.open(base_path).convert('RGBA').resize((1376,768),Image.Resampling.LANCZOS)
im=Image.open(source).convert('RGBA').resize((1376,768),Image.Resampling.LANCZOS)
poly=[(580,266),(629,296),(627,305),(611,310),(611,317),(608,326),(603,334),(594,340),(595,345),(606,348),(617,376),(624,403),(624,438),(629,450),(627,460),(621,465),(614,464),(612,447),(611,470),(615,500),(610,512),(603,518),(603,545),(621,557),(625,564),(622,569),(613,570),(591,564),(587,559),(589,518),(583,506),(578,496),(572,508),(560,520),(558,549),(560,569),(557,575),(549,578),(538,576),(535,570),(538,560),(543,550),(543,516),(535,506),(532,499),(536,473),(537,466),(532,466),(527,462),(524,454),(525,443),(521,421),(517,405),(518,397),(525,374),(538,352),(551,346),(559,340),(555,333),(551,320),(548,311),(533,312),(527,309),(527,304)]
mask=Image.new('L',(1376*4,768*4));ImageDraw.Draw(mask).polygon([(x*4,y*4) for x,y in poly],fill=255);mask=mask.resize((1376,768),Image.Resampling.LANCZOS)
box=(515,263,632,580);cut=im.crop(box);cut.putalpha(mask.crop(box));cut=cut.resize((88,238),Image.Resampling.LANCZOS)
# Empty far-right courtyard: no scarf, hand, torso or foot overlapped.
pos=(1250,420);shadow=Image.new('RGBA',base.size);ImageDraw.Draw(shadow).ellipse((1240,646,1345,666),fill=(35,30,25,60));shadow=shadow.filter(ImageFilter.GaussianBlur(4));base=Image.alpha_composite(base,shadow);base.alpha_composite(cut,pos)
base.convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(out)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meta={'output':str(out.relative_to(ROOT)),'method':'local composite, not a fresh independent AI scene','base':str(base_path.relative_to(ROOT)),'base_sha256':sha(base_path),'figure_source':str(source.relative_to(ROOT)),'figure_source_sha256':sha(source),'source_coordinate_system':[1376,768],'mask_polygon':poly,'crop_box':box,'placement':pos,'cutout_size':[88,238],'final_sha256':sha(out),'purpose':'Add missing fourth companion without covering hands; avoid AIv2 foreground-arm/companion-torso overlap. Five full figures, ten distinct hands. Final visual review separate.'}
out.with_name('s04b-KOMPOZIT.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('S04B_COMPOSITE',sha(out))
