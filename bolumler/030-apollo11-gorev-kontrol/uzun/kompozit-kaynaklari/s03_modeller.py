"""s03: Onaylı dört figürlü s01 üzerine kendi çizdiğimiz TEMSİLÎ iki araç modeli.
Bunlar NASA çizimi, arşiv fotoğrafı veya ölçülü mühendislik planı değildir.
Önceki AI modelleri yan figürlerin ayaklarını örtüyordu. Bu kompozitte tablo
ve modeller bütün figürlerin açık sağ koridorunda, uzuvların dışındadır.
Çalıştırma: python bolumler/030-apollo11-gorev-kontrol/uzun/kompozit-kaynaklari/s03_modeller.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[4]
G = ROOT / 'bolumler/030-apollo11-gorev-kontrol/uzun/gorseller'
im = Image.open(G / 's01.png').convert('RGBA')
S = 3
layer = Image.new('RGBA', (1920*S, 1080*S))
d = ImageDraw.Draw(layer)
ink = '#3e3e36'
def line(points, fill=ink, width=2):
    d.line([(round(x*S), round(y*S)) for x,y in points], fill=fill, width=round(width*S), joint='curve')
def poly(points, fill, outline=ink, width=2):
    pts=[(round(x*S),round(y*S)) for x,y in points]
    d.polygon(pts, fill=fill)
    if outline: d.line(pts+[pts[0]], fill=outline, width=round(width*S), joint='curve')
def ellipse(box, fill, outline=ink, width=2):
    d.ellipse(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=round(width*S))
# Low display table, entirely to the right of all three colleagues and left of Merakli.
poly([(1105,961),(1120,961),(1117,1048),(1108,1048)], '#7e7c6b')
poly([(1405,961),(1417,961),(1420,1048),(1410,1048)], '#7e7c6b')
poly([(1100,938),(1408,938),(1431,962),(1081,962)], '#d1cfb8')
poly([(1081,962),(1431,962),(1431,972),(1081,972)], '#aaa995')
# Eagle: four spindly landing legs with four pads; gold descent stage, angular ascent stage.
for points in [[(1150,865),(1128,910),(1130,925)],[(1209,865),(1235,909),(1239,925)]]:
    line(points, '#b39a68', 4); line(points, ink, 1)
for x,y in [(1130,926),(1239,926)]: ellipse((x-10,y-3,x+10,y+3), '#c3ad79', width=1)
poly([(1146,840),(1209,840),(1223,864),(1214,904),(1148,904),(1131,866)], '#bba06b')
poly([(1146,840),(1179,848),(1174,900),(1148,904),(1131,866)], '#d0b77c')
poly([(1179,848),(1209,840),(1223,864),(1214,904),(1174,900)], '#8c774c')
line([(1147,854),(1164,875),(1153,895)], '#e1cc91', 1)
line([(1204,852),(1191,872),(1206,895)], '#c2aa71', 1)
poly([(1151,780),(1192,770),(1215,794),(1211,841),(1149,840),(1139,808)], '#a7aaa1')
poly([(1151,780),(1173,793),(1167,834),(1149,840),(1139,808)], '#62655e')
poly([(1173,793),(1192,770),(1215,794),(1211,841),(1167,834)], '#b7bbb2')
poly([(1150,798),(1168,792),(1165,812)], '#303d3d', '#d1d2c1', 1)
poly([(1182,793),(1204,799),(1185,812)], '#303d3d', '#d1d2c1', 1)
poly([(1170,818),(1184,818),(1185,838),(1169,838)], '#515751')
line([(1148,780),(1141,757)], width=2)
ellipse((1133,747,1149,759), '#bfc3b8', width=1)
line([(1205,785),(1220,760)], width=2)
ellipse((1215,752,1226,762), '#c5c5b7', width=1)
# Two visible front legs and triangulated supports.
for points in [[(1141,875),(1103,940)],[(1209,874),(1254,940)]]:
    line(points, '#c5ad73', 5); line(points, ink, 1)
line([(1141,875),(1129,925),(1103,940)], '#8f7e56', 2)
line([(1209,874),(1238,925),(1254,940)], '#8f7e56', 2)
for x in [1103,1254]: ellipse((x-13,938,x+13,944), '#baa16b', width=1)
# Separate Columbia command/service module, supported on a miniature display cradle.
poly([(1322,835),(1388,835),(1388,886),(1322,886)], '#b9bdb7')
ellipse((1380,834,1397,887), '#929a95')
poly([(1391,848),(1413,840),(1413,881),(1391,872)], '#686e68')
line([(1408,842),(1408,880)], '#a5aaa0', 1)
ellipse((1316,834,1331,887), '#c7cbc3')
poly([(1274,859),(1319,834),(1319,886)], '#c4c9c0')
poly([(1274,859),(1319,868),(1319,886)], '#9ba59e')
line([(1283,853),(1316,840)], '#e2e3d6', 2)
poly([(1294,853),(1305,848),(1305,858),(1294,861)], '#455753', '#6c7770', 1)
line([(1342,838),(1342,884)], '#7b8580', 1)
line([(1371,838),(1371,884)], '#7b8580', 1)
for x,y in [(1357,855),(1357,866),(1350,860),(1364,860)]: ellipse((x-2,y-2,x+2,y+2), '#707a72', width=1)
for x in [1334,1378]:
    line([(x,887),(x,930)], '#777d72', 4)
poly([(1325,930),(1393,930),(1403,938),(1315,938)], '#969d90')
# Subtle common contact shadow; drawing contours retain the scene's muted palette.
shadow=Image.new('RGBA',layer.size);sd=ImageDraw.Draw(shadow)
for box in [(1091,938,1269,949),(1310,934,1409,947)]:
    sd.ellipse(tuple(v*S for v in box), fill=(46,44,36,45))
shadow=shadow.filter(ImageFilter.GaussianBlur(3*S))
# Objects drawn at 3x resolution for smooth clean ink edges, not harsh pixelated vector edges.
layer=Image.alpha_composite(layer,shadow).resize(im.size,Image.Resampling.LANCZOS)
im=Image.alpha_composite(im,layer)
im.convert('RGB').save(G / 's03.png')
