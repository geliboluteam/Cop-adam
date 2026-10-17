#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MERAKLI serisi — YouTube küçük resim (thumbnail) üreticisi.

Kullanım:
  python3 araclar/thumbnail_yap.py          → sahne görseli olan tüm bölümler
  python3 araclar/thumbnail_yap.py 006      → sadece bölüm 006

Tasarım standardı (kullanıcı talimatı, 2026-10-17 — YouTube örneği tarzı):
  - 1280×720 (YouTube önerilen boyut)
  - dramatik sahne + sağ önde BÜYÜK abartılı ifadeli Meraklı (AI sahnesi)
  - sol üst: kırmızı MERAKLI rozeti + beyaz kalın ana başlık (siyah kontur)
    + kanal kırmızısı vurgu satırı (KIRMIZI = 217,54,54 — kapak_yap.py ile
    birebir aynı kanonik "fular kırmızısı")
  - sol alt: "EĞER ORADA OLSAYDIM — BÖLÜM N" seri etiketi
  - Shorts'lar YouTube'da özel küçük resim almadığı için yalnız uzun/ana
    videolara üretilir.

Sahneler: kapaklar/thumbnail/sahne/bolum-XXX.jpg (metinsiz üretilir)
Çıktı:    kapaklar/thumbnail/bolum-XXX.png + ONIZLEME.png (kontak sayfası)
Yeni bölüm paketlerinde Tur D'de standart adımdır (B006'dan itibaren).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAHNE_KLASOR = os.path.join(KOK, "kapaklar", "thumbnail", "sahne")
CIKTI_KLASOR = os.path.join(KOK, "kapaklar", "thumbnail")
F_BLACK = os.path.join(KOK, "araclar", "fonts", "Montserrat-Black.ttf")
F_XBOLD = os.path.join(KOK, "araclar", "fonts", "Montserrat-ExtraBold.ttf")
F_BOLD = os.path.join(KOK, "araclar", "fonts", "Montserrat-Bold.ttf")

W, H = 1280, 720
KIRMIZI = (217, 54, 54)  # kanonik fular kırmızısı (kapak_yap.py ile aynı)
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)

# beyaz başlık satırları "\n" ile bölünebilir; kirmizi = vurgu satırı
BOLUMLER = {
    "001": dict(beyaz="FETİH'İN\nİZCİSİ", kirmizi="1453"),
    "002": dict(beyaz="ŞAHİ\nTOPÇUSU", kirmizi="1453"),
    "003": dict(beyaz="FIRTINADA\nDENCİ", kirmizi="1453"),
    "004": dict(beyaz="SON\nNÖBETÇİ", kirmizi="1453"),
    "005": dict(beyaz="MALAZGİRT", kirmizi="1071"),
    "006": dict(beyaz="KARA\nVEBA", kirmizi="1348"),
    "007": dict(beyaz="POMPEII", kirmizi="MS 79"),
}


def yazi_sigdir(cizim, metin, font_yolu, max_genislik, baslangic_boyutu, kontur):
    """Metni max_genislik'e sığdıran en büyük puntoyu bulur."""
    boyut = baslangic_boyutu
    while boyut > 28:
        font = ImageFont.truetype(font_yolu, boyut)
        kutu = cizim.textbbox((0, 0), metin, font=font)
        if kutu[2] - kutu[0] + 2 * kontur <= max_genislik:
            return font, kutu
        boyut -= 3
    font = ImageFont.truetype(font_yolu, boyut)
    return font, cizim.textbbox((0, 0), metin, font=font)


def kapak_yap(no, ayar):
    kaynak_yolu = os.path.join(SAHNE_KLASOR, f"bolum-{no}.jpg")
    if not os.path.exists(kaynak_yolu):
        print(f"  ! bolum-{no}: sahne yok, atlandı ({kaynak_yolu})")
        return None
    kaynak = Image.open(kaynak_yolu).convert("RGB")
    ow, oh = kaynak.size
    olcek = max(W / ow, H / oh)
    kaynak = kaynak.resize((round(ow * olcek), round(oh * olcek)), Image.LANCZOS)
    ow, oh = kaynak.size
    sol, ust = (ow - W) // 2, (oh - H) // 2
    im = kaynak.crop((sol, ust, sol + W, ust + H)).convert("RGBA")
    katman = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(katman)
    x0 = 52

    # 1) MERAKLI rozeti
    y = 34
    f_rozet = ImageFont.truetype(F_XBOLD, 40)
    kutu = d.textbbox((0, 0), "MERAKLI", font=f_rozet)
    rw, rh = kutu[2] - kutu[0] + 46, kutu[3] - kutu[1] + 28
    d.rounded_rectangle([x0, y, x0 + rw, y + rh], radius=14, fill=KIRMIZI + (255,))
    d.text((x0 + 23, y + 14 - kutu[1]), "MERAKLI", font=f_rozet, fill=BEYAZ + (255,))
    y += rh + 22

    # 2) beyaz ana başlık (satırlar halinde)
    for satir in ayar["beyaz"].split("\n"):
        font, kutu = yazi_sigdir(d, satir, F_BLACK, 620, 112, 11)
        d.text((x0 + 6, y + 8), satir, font=font, fill=SIYAH + (130,),
               stroke_width=11, stroke_fill=SIYAH + (130,))
        d.text((x0, y), satir, font=font, fill=BEYAZ + (255,),
               stroke_width=11, stroke_fill=SIYAH + (255,))
        y += (kutu[3] - kutu[1]) + 30

    # 3) kanal kırmızısı vurgu satırı
    y += 6
    font, kutu = yazi_sigdir(d, ayar["kirmizi"], F_BLACK, 420, 122, 11)
    d.text((x0 + 6, y + 8), ayar["kirmizi"], font=font, fill=SIYAH + (130,),
           stroke_width=11, stroke_fill=SIYAH + (130,))
    d.text((x0, y), ayar["kirmizi"], font=font, fill=KIRMIZI + (255,),
           stroke_width=11, stroke_fill=SIYAH + (255,))

    # 4) sol alt seri etiketi
    etiket = f"EĞER ORADA OLSAYDIM — BÖLÜM {int(no)}"
    f_etiket = ImageFont.truetype(F_XBOLD, 30)
    d.text((x0 + 4, H - 56 + 4), etiket, font=f_etiket, fill=SIYAH + (150,),
           stroke_width=6, stroke_fill=SIYAH + (150,))
    d.text((x0, H - 56), etiket, font=f_etiket, fill=BEYAZ + (255,),
           stroke_width=6, stroke_fill=SIYAH + (255,))

    im = Image.alpha_composite(im, katman).convert("RGB")
    cikti_yolu = os.path.join(CIKTI_KLASOR, f"bolum-{no}.png")
    im.save(cikti_yolu)
    print(f"  ✓ bolum-{no}.png  ({ayar['beyaz'].replace(chr(10), ' ')} / {ayar['kirmizi']})")
    return cikti_yolu


def onizleme(ciktilar):
    """3 sütunlu dinamik kontak sayfası: kapaklar/thumbnail/ONIZLEME.png"""
    kol, tw, th, bosluk, etiket_h = 3, 416, 234, 12, 36
    satir = (len(ciktilar) + kol - 1) // kol
    sayfa_w = kol * tw + (kol + 1) * bosluk
    sayfa_h = satir * (th + etiket_h) + (satir + 1) * bosluk
    sayfa = Image.new("RGB", (sayfa_w, sayfa_h), (18, 18, 22))
    d = ImageDraw.Draw(sayfa)
    f = ImageFont.truetype(F_BOLD, 21)
    for i, (no, yol) in enumerate(ciktilar):
        r, s = i % kol, i // kol
        x = bosluk + r * (tw + bosluk)
        y = bosluk + s * (th + etiket_h + bosluk)
        gorsel = Image.open(yol).resize((tw, th), Image.LANCZOS)
        sayfa.paste(gorsel, (x, y))
        d.rectangle([x, y + th, x + tw, y + th + etiket_h], fill=KIRMIZI)
        metin = f"BÖLÜM {int(no)} · {BOLUMLER[no]['beyaz'].replace(chr(10), ' ')}"
        kutu = d.textbbox((0, 0), metin, font=f)
        d.text((x + (tw - (kutu[2] - kutu[0])) // 2, y + th + 9), metin,
               font=f, fill=BEYAZ)
    yol = os.path.join(CIKTI_KLASOR, "ONIZLEME.png")
    sayfa.save(yol)
    print(f"  ✓ ONIZLEME.png ({len(ciktilar)} kapak)")


def main():
    secilen = [sys.argv[1]] if len(sys.argv) > 1 else sorted(BOLUMLER)
    print(f"Kanal kırmızısı: RGB{KIRMIZI} (kanonik fular kırmızısı)")
    os.makedirs(CIKTI_KLASOR, exist_ok=True)
    ciktilar = []
    for no in secilen:
        if no not in BOLUMLER:
            print(f"  ! bilinmeyen bölüm: {no}")
            continue
        yol = kapak_yap(no, BOLUMLER[no])
        if yol:
            ciktilar.append((no, yol))
    if ciktilar:
        onizleme(ciktilar)


if __name__ == "__main__":
    main()
