#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MERAKLI — KAPAK SİSTEMİ v2 (2026-10 sonrası kanonik)

KURAL: Kapak ASLA değişmez — sabit "Meraklı düşünüyor" temel sanatı, sabit
"EĞER OLSAYDIM" rozeti, sabit MERAKLI bandı. Konu başına YALNIZCA başlık
metni değişir. Başlıklar PIL ile basılır (yapay zekâ metni yok → Türkçe
karakter hatasız, tipografi her kapakta birebir aynı).

Kullanım (tek kapak):
  python3 araclar/kapak_yap2.py <cikti.png> "BAŞLIK SATIRI 1" "BAŞLIK SATIRI 2" [--dikey]

Toplu üretim (tüm konular):
  python3 araclar/kapak_yap2.py --tumu

Temel sanatlar:
  kapaklar/temel/merakli-dusunuyor-16x9.png  (uzun video kapakları)
  kapaklar/temel/merakli-dusunuyor-9x16.png  (Shorts kapakları)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(KOK, "araclar", "fonts", "Montserrat-ExtraBold.ttf")
TEMEL_G = os.path.join(KOK, "kapaklar", "temel", "merakli-dusunuyor-16x9.png")
TEMEL_D = os.path.join(KOK, "kapaklar", "temel", "merakli-dusunuyor-9x16.png")

KIRMIZI = (217, 54, 54)
BEYAZ = (255, 255, 255)
SIYAH = (12, 12, 12)

# Konu başlıkları (bolum no -> (satir1, satir2)) — satir2'de yıl/mekân
BASLIKLAR = {
    "001": ("FETİH ORDUSUNDA İZCİ", "1453 · İSTANBUL"),
    "002": ("ŞAHİ TOPUNUN USTASI", "1453 · EDİRNE"),
    "003": ("FIRTINADA BİR DENİCİ", "1453 · HALİÇ"),
    "004": ("SURLARDA SON NÖBETÇİ", "1453 · 29 MAYIS"),
    "005": ("MALAZGİRT'TE HABERCİ", "1071"),
    "006": ("KARA VEBA ŞEHRİNDE", "1347 · AVRUPA"),
    "007": ("POMPEII'DE KAÇABİLİR MİYİM?", "79 · VEZÜV"),
    "008": ("HERCULANEUM: SON 30 DAKİKA", "79 · VEZÜV"),
    "009": ("KRAKATOA PATLAMASI", "1883"),
    "010": ("DEPREM ANINDA ANTİK ŞEHİR", "ANTİK ÇAĞ"),
    "011": ("BÜYÜK ŞEHİR YANGININDA", "MAHSUR KALSAM"),
    "012": ("LONDRA'NIN BÜYÜK YANGINI", "1666"),
    "013": ("ARENEYA ÇIKAN GLADYATÖR", "80 · ROMA"),
    "014": ("PİRAMİT İŞÇİSİ", "MÖ 2560 · GİZA"),
    "015": ("İLK OLİMPİYAT", "MÖ 776 · OLİMPIA"),
    "016": ("KARTACA KUŞATMASINDA", "MÖ 149"),
    "017": ("LEJYONER KARAKOLDA", "MS 120 · LİMES"),
    "018": ("SOKRATES'İN DURUŞMASI", "MÖ 399 · ATİNA"),
    "019": ("TİYATRONUN SAHNE ARKASI", "ANTİK YUNAN"),
    "020": ("İSKENDERİYE KÜTÜPHANESİ", "YANGIN GECESİ"),
    "021": ("İSKENDER'İN HARİTACISI", "MÖ 334"),
    "022": ("TAÇ GİYME TÖRENİNDE", "SARAY GÖREVLİSİ"),
    "023": ("TRUVA ATI SOKAĞINDA", "O GECE"),
    "024": ("VİKİNG BASKININDA", "793"),
    "025": ("KALE KUŞATMASINDA", "ORTA ÇAĞ"),
    "026": ("CADILIK SUÇLAMASIYLA", "ORTA ÇAĞ"),
    "027": ("ŞÖVALYE TURNUVASINDA", "ORTA ÇAĞ"),
    "028": ("ÇİN SEDDİ'NDE NÖBETÇİ", "GECE GÖZETİMİ"),
    "029": ("PANAYIRDA TÜCCAR", "ORTA ÇAĞ"),
    "030": ("MANASTIRDA KEŞİŞ", "YAZMA ODASI"),
    "031": ("KALEDE AŞÇI", "KUŞATMA GÜNÜ"),
    "032": ("KALEYE SIZAN CASUS", "GECE GÖREVİ"),
    "033": ("SAMURAY: KALE SAVUNMASI", "JAPONYA"),
    "034": ("NİL TAŞKININDA ÇİFTÇİ", "ESKİ MISIR"),
    "035": ("AZTEK BAŞKENTİNDE TÜCCAR", "1519 · TENOCHTITLAN"),
    "036": ("İNKA YOLUNDA ULAK", "AND DAĞLARI"),
    "037": ("KERVANSARAYDA BİR GECE", "ANADOLU"),
    "038": ("İPEK YOLU'NDA KERVAN", "ÇÖL GÜZERGÂHI"),
    "039": ("İLK TREN YOLCULUĞU", "1830 · LIVERPOOL"),
    "040": ("SOKAKTA İLK OTOMOBİLLER", "1886"),
    "041": ("İLK BALONDA YÜKSELDİM", "1783 · PARİS"),
    "042": ("İLK DENİZALTI MÜRETTEBATI", "SU ALTINDA"),
    "043": ("İLK FOTOĞRAFIN ÇIRAĞI", "1839"),
    "044": ("İLK UÇUŞA TANIK OLDUM", "1903 · KITTY HAWK"),
    "045": ("APOLLO 11 KONTROL ODASI", "1969 · HOUSTON"),
    "046": ("TİTANİC'İN SON GECESİ", "1912 · ATLANTİK"),
    "047": ("KUTUPTA KIZAKÇIYDIM", "1911"),
    "048": ("BİLİNMEYEN ADADA", "KEŞİF GÜNÜ"),
    "049": ("GRÖNLAND'A DOĞRU", "985 · VİKİNG"),
    "050": ("KORSAN GEMİSİNDE İSYAN", "ALTIN ÇAĞ"),
    "051": ("İLK MATBAADA ÇIRAK", "1450 · MAINZ"),
    "052": ("SAAT KULESİNİN ÇIRAĞI", "ORTA ÇAĞ"),
    "053": ("DEVRİMDE FIRINCI ÇIRAĞI", "1789 · PARİS"),
    "054": ("SİPERLERDE BİR GÜN", "1915"),
    "055": ("TUTANKHAMUN'UN MEZARINDA", "1922"),
}

def fnt(b):
    return ImageFont.truetype(FONT, b)

def kapla(im, W, H):
    olcek = max(W/im.width, H/im.height)
    im = im.resize((int(im.width*olcek)+1, int(im.height*olcek)+1), Image.LANCZOS)
    x = (im.width - W)//2
    y = (im.height - H)//2
    return im.crop((x, y, x+W, y+H))

def sol_gradyan(taban, W, H, dikey=False):
    siyah = Image.new("RGB", (W, H), SIYAH)
    katman = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(katman)
    if dikey:  # ustten koyulasan (dikeyde baslik ustte)
        for y in range(int(H*0.62)):
            oran = y / (H*0.62)
            d.line([(0, y), (W, y)], fill=int(170*(1-oran)**1.2))
    else:      # soldan koyulasan
        for x in range(int(W*0.66)):
            oran = x / (W*0.66)
            d.line([(x, 0), (x, H)], fill=int(185*(1-oran)**1.3))
    taban.paste(siyah, (0, 0), katman)
    return taban

def kapak_uret(cikti, s1, s2, dikey=False):
    if dikey:
        W, H = 1080, 1920
        taban = kapla(Image.open(TEMEL_D).convert("RGB"), W, H)
        taban = sol_gradyan(taban, W, H, dikey=True)
        dr = ImageDraw.Draw(taban)
        # rozet (sabit metin)
        f = fnt(44); metin = "EĞER OLSAYDIM"
        kutu = dr.textbbox((0, 0), metin, font=f)
        dr.rounded_rectangle([50, 120, 50+kutu[2]-kutu[0]+52, 120+kutu[3]-kutu[1]+40],
                             radius=14, fill=KIRMIZI, outline=BEYAZ, width=3)
        dr.text((76-kutu[0], 140-kutu[1]), metin, font=f, fill=BEYAZ)
        # baslik (2 satir, otomatik boyut)
        boy = 96
        while boy > 44:
            fb = fnt(boy)
            if max(dr.textbbox((0,0), s, font=fb)[2] for s in (s1, s2)) <= 900:
                break
            boy -= 4
        fb = fnt(boy)
        y = 300
        for s in (s1, s2):
            kutu = dr.textbbox((0, 0), s, font=fb)
            dr.text((57, y-kutu[1]+7), s, font=fb, fill=(0, 0, 0))
            dr.text((50, y-kutu[1]), s, font=fb, fill=BEYAZ,
                    stroke_width=6, stroke_fill=SIYAH)
            y += (kutu[3]-kutu[1]) + 26
        # MERAKLI bandi (sabit)
        f2 = fnt(46); metin2 = "MERAKLI"
        kutu2 = dr.textbbox((0, 0), metin2, font=f2)
        y0 = H-140
        dr.rounded_rectangle([50, y0, 50+kutu2[2]-kutu2[0]+48, y0+kutu2[3]-kutu2[1]+28],
                             radius=20, fill=KIRMIZI, outline=BEYAZ, width=3)
        dr.text((74-kutu2[0], y0+14-kutu2[1]), metin2, font=f2, fill=BEYAZ)
        f3 = fnt(28)
        dr.text((120+kutu2[2]-kutu2[0]+40, y0+22), "EĞER OLSAYDIM SERİSİ",
                font=f3, fill=BEYAZ, stroke_width=4, stroke_fill=SIYAH)
    else:
        W, H = 1280, 720
        taban = kapla(Image.open(TEMEL_G).convert("RGB"), W, H)
        taban = sol_gradyan(taban, W, H, dikey=False)
        dr = ImageDraw.Draw(taban)
        # rozet (sabit metin)
        f = fnt(42); metin = "EĞER OLSAYDIM"
        kutu = dr.textbbox((0, 0), metin, font=f)
        dr.rounded_rectangle([46, 42, 46+kutu[2]-kutu[0]+52, 42+kutu[3]-kutu[1]+38],
                             radius=14, fill=KIRMIZI, outline=BEYAZ, width=3)
        dr.text((72-kutu[0], 61-kutu[1]), metin, font=f, fill=BEYAZ)
        # baslik
        boy = 92
        while boy > 40:
            fb = fnt(boy)
            if max(dr.textbbox((0,0), s, font=fb)[2] for s in (s1, s2)) <= 700:
                break
            boy -= 4
        fb = fnt(boy)
        y = 170
        for s in (s1, s2):
            kutu = dr.textbbox((0, 0), s, font=fb)
            dr.text((53, y-kutu[1]+7), s, font=fb, fill=(0, 0, 0))
            dr.text((46, y-kutu[1]), s, font=fb, fill=BEYAZ,
                    stroke_width=7, stroke_fill=SIYAH)
            y += (kutu[3]-kutu[1]) + 24
        # MERAKLI bandi (sabit)
        f2 = fnt(40); metin2 = "MERAKLI"
        kutu2 = dr.textbbox((0, 0), metin2, font=f2)
        y0 = H-100
        dr.rounded_rectangle([46, y0, 46+kutu2[2]-kutu2[0]+44, y0+kutu2[3]-kutu2[1]+26],
                             radius=20, fill=KIRMIZI, outline=BEYAZ, width=3)
        dr.text((68-kutu2[0], y0+13-kutu2[1]), metin2, font=f2, fill=BEYAZ)
        f3 = fnt(26)
        dr.text((110+kutu2[2]-kutu2[0]+40, y0+16), "EĞER OLSAYDIM SERİSİ",
                font=f3, fill=BEYAZ, stroke_width=4, stroke_fill=SIYAH)
    os.makedirs(os.path.dirname(cikti), exist_ok=True)
    taban.save(cikti, "PNG", optimize=True)
    return cikti

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--tumu":
        os.makedirs(os.path.join(KOK, "kapaklar"), exist_ok=True)
        os.makedirs(os.path.join(KOK, "kapaklar", "shorts"), exist_ok=True)
        for no, (s1, s2) in sorted(BASLIKLAR.items()):
            kapak_uret(os.path.join(KOK, "kapaklar", f"bolum-{no}.png"), s1, s2)
            kapak_uret(os.path.join(KOK, "kapaklar", "shorts", f"bolum-{no}.png"),
                       s1, s2, dikey=True)
        print(f"TOPLAM {len(BASLIKLAR)} konu x 2 format kapak üretildi.")
    else:
        if len(sys.argv) < 4:
            print(__doc__); sys.exit(1)
        cikti, s1, s2 = sys.argv[1], sys.argv[2], sys.argv[3]
        dikey = "--dikey" in sys.argv
        kapak_uret(cikti, s1, s2, dikey)
        print(f"KAPAK: {cikti}")

if __name__ == "__main__":
    main()
