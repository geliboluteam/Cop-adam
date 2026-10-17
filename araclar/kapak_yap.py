#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MERAKLI — Seri kapak (thumbnail) üretici.
TÜM BÖLÜMLER İÇİN DEĞİŞMEYEN ŞABLON: yerleşim, renkler, font, rozet ve MERAKLI
bandı sabittir; bölüm başına yalnızca sanat + yıl rozeti + iki satır başlık
değişir. Başlıklar PIL ile basılır (yapay zekâ metni yok -> Türkçe karakter
hatasız, her bölümde aynı tipografi).

Kullanım:
  python3 araclar/kapak_yap.py <sanat.png> "<yil_rozeti>" "<satir1>" "<satir2>" <cikti.png>
Örnek:
  python3 araclar/kapak_yap.py kapaklar/sanat/bolum-001.png \
      "EĞER 1453'TE OLSAYDIM" "FETİH ORDUSUNDA" "BİR İZCİ" kapaklar/bolum-001.png

Şablon kuralları (docs/KAPAK_SISTEMI.md):
  - 1280x720, sanat sağa yaslı kaplama (karakter sağ üçte birde)
  - soldan koyulaşan gradyan (metin okunurluğu)
  - sol üst: kırmızı (#D93636) yıl rozeti, beyaz Montserrat ExtraBold
  - rozetin altında: 2 satır büyük beyaz başlık, siyah kontur + gölge
  - sol alt: kırmızı MERAKLI bandı + "EĞER OLSAYDIM SERİSİ" alt yazısı
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(KOK, "araclar", "fonts", "Montserrat-ExtraBold.ttf")

# --- Sabit şablon değerleri (ASLA değişmez) ---
W, H = 1280, 720
KIRMIZI = (217, 54, 54)        # fular kırmızısı
BEYAZ = (255, 255, 255)
SIYAH = (12, 12, 12)
ROZET_BOY = 42
BASLIK_MAX_GEN = 640
BASLIK_BOY_MAX = 104
BASLIK_BOY_MIN = 56
BANT_BOY = 40

def font_boyut(boy):
    return ImageFont.truetype(FONT, boy)

def kapla(sanat):
    """Sanatı 1280x720'ye kaplayarak yerleştir (dikeyde %45'e hizalı kırpma)."""
    im = Image.open(sanat).convert("RGB")
    olcek = max(W/im.width, H/im.height)
    im = im.resize((int(im.width*olcek)+1, int(im.height*olcek)+1), Image.LANCZOS)
    x = (im.width - W)//2
    y = int((im.height - H)*0.45)
    return im.crop((x, y, x+W, y+H))

def sol_gradyan(taban):
    """Soldan koyulaşan siyah gradyan + hafif alt karartma."""
    katman = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(katman)
    for x in range(W):
        oran = x / W
        if oran < 0.62:
            alfa = int(190 * (1 - oran/0.62)**1.35)
        else:
            alfa = 0
        d.line([(x, 0), (x, H)], fill=alfa)
    # alt karartma
    alt = Image.new("L", (W, H), 0)
    da = ImageDraw.Draw(alt)
    for y in range(H):
        if y > H*0.72:
            da.line([(0, y), (W, y)], fill=int(90*((y-H*0.72)/(H*0.28))))
    siyah = Image.new("RGB", (W, H), SIYAH)
    taban.paste(siyah, (0, 0), katman)
    taban.paste(siyah, (0, 0), alt)
    return taban

def rozet_ciz(dr, metin):
    f = font_boyut(ROZET_BOY)
    kutu = dr.textbbox((0, 0), metin, font=f)
    tw, th = kutu[2]-kutu[0], kutu[3]-kutu[1]
    pad_x, pad_y = 26, 14
    x0, y0 = 46, 42
    dr.rounded_rectangle([x0, y0, x0+tw+2*pad_x, y0+th+2*pad_y+8],
                         radius=14, fill=KIRMIZI, outline=BEYAZ, width=3)
    dr.text((x0+pad_x-kutu[0], y0+pad_y-kutu[1]), metin, font=f, fill=BEYAZ)
    return y0+th+2*pad_y+8

def baslik_boyutu_bul(dr, satirlar):
    boy = BASLIK_BOY_MAX
    while boy > BASLIK_BOY_MIN:
        f = font_boyut(boy)
        genis = max(dr.textbbox((0, 0), s, font=f)[2] for s in satirlar)
        if genis <= BASLIK_MAX_GEN:
            return boy
        boy -= 4
    return BASLIK_BOY_MIN

def baslik_ciz(dr, satirlar, ust_y):
    boy = baslik_boyutu_bul(dr, satirlar)
    f = font_boyut(boy)
    y = ust_y + 34
    for s in satirlar:
        kutu = dr.textbbox((0, 0), s, font=f)
        # gölge
        dr.text((50+7, y-kutu[1]+7), s, font=f, fill=(0, 0, 0))
        dr.text((50, y-kutu[1]), s, font=f, fill=BEYAZ,
                stroke_width=7, stroke_fill=SIYAH)
        y += (kutu[3]-kutu[1]) + 18

def bant_ciz(dr):
    f = font_boyut(BANT_BOY)
    metin = "MERAKLI"
    kutu = dr.textbbox((0, 0), metin, font=f)
    tw, th = kutu[2]-kutu[0], kutu[3]-kutu[1]
    x0, y0 = 46, H-92
    dr.rounded_rectangle([x0, y0, x0+tw+44, y0+th+26], radius=20,
                         fill=KIRMIZI, outline=BEYAZ, width=3)
    dr.text((x0+22-kutu[0], y0+13-kutu[1]), metin, font=f, fill=BEYAZ)
    # yanında ince seri yazısı
    f2 = font_boyut(26)
    dr.text((x0+tw+60, y0+16), "EĞER OLSAYDIM SERİSİ", font=f2, fill=BEYAZ,
            stroke_width=4, stroke_fill=SIYAH)

def main():
    if len(sys.argv) != 6:
        print(__doc__); sys.exit(1)
    sanat, rozet, s1, s2, cikti = sys.argv[1:6]
    taban = kapla(sanat)
    taban = sol_gradyan(taban)
    dr = ImageDraw.Draw(taban)
    alt_y = rozet_ciz(dr, rozet)
    baslik_ciz(dr, [s1, s2], alt_y)
    bant_ciz(dr)
    taban.save(cikti, "PNG", optimize=True)
    print(f"KAPAK: {cikti}  ({os.path.getsize(cikti)/1024:.0f} KB)")

if __name__ == "__main__":
    main()
