#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MERAKLI serisi — YouTube küçük resim (thumbnail) üreticisi — v4.

Kullanım:
  python3 araclar/thumbnail_yap.py          → sahne görseli olan tüm bölümler
  python3 araclar/thumbnail_yap.py 014      → sadece bölüm 014

v4 STANDARDI (2026-10-18, kullanıcı talimatı — örnek: docs/kapak-ornek/):
  - 1280×720; Shorts'a kapak ÜRETİLMEZ (yalnız uzun/ana video).
  - SAHNE GÖRSELİ (AI, metinsiz, bolum-XXX.jpg): Meraklı BÜYÜK — tuvalin
    sağ ~%40'ını kaplar, kafa yüksekliği tuvalin ~%30'u; o bölümün
    konusuna özgü KIYAFET ve abartılı İFADE (şok/hayranlık/kararlılık);
    arka planda dramatik konu sahnesi; SOL TARAF yazı için temiz.
  - BÜYÜK İLGİ ÇEKİCİ BAŞLIK (2-4 kelime, konuya özel "buyuk"):
    beyaz, Montserrat-Black, ~150 px, kalın siyah kontur; sol blok.
  - VURGU SATIRI ("vurgu"): kanal kırmızısı RGB(217,54,54), ~110 px,
    siyah kontur (yıl / anahtar kelime).
  - MERAKLI rozeti (kırmızı) sol üst; seri etiketi sol alt.

Sahneler: kapaklar/thumbnail/sahne/bolum-XXX.jpg (metinsiz üretilir)
Çıktı:    kapaklar/thumbnail/bolum-XXX.png + ONIZLEME.png (kontak sayfası)
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
KIRMIZI = (217, 54, 54)  # kanonik fular kırmızısı
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)

# buyuk: 2-4 kelimelik, konuya özel İLGİ ÇEKİCİ büyük başlık ("\n" ile satır)
# vurgu: kırmızı vurgu satırı (yıl / anahtar kelime)
BOLUMLER = {
    "001": dict(buyuk="SURLAR\nÇÖKÜYOR!", vurgu="1453"),
    "002": dict(buyuk="DEV ŞAHİ\nGELİYOR!", vurgu="1453"),
    "003": dict(buyuk="GEMİLER\nKARADAN!", vurgu="1453"),
    "004": dict(buyuk="SON\nHÜCUM!", vurgu="29 MAYIS 1453"),
    "005": dict(buyuk="TARİH\nDÖNDÜ!", vurgu="1071"),
    "006": dict(buyuk="KARA\nVEBÂ!", vurgu="1348"),
    "007": dict(buyuk="18 SAATİN\nVAR!", vurgu="MS 79"),
    "008": dict(buyuk="4\nDAKİKA!", vurgu="MS 79"),
    "009": dict(buyuk="DÜNYA\nDUYDU!", vurgu="1883"),
    "010": dict(buyuk="ŞEHİR\nSİLİNDİ!", vurgu="MS 526"),
    "012": dict(buyuk="4 GÜN\nATEŞ!", vurgu="1666"),
    "013": dict(buyuk="ÖLÜM\nKALIM!", vurgu="MS 80"),
    "014": dict(buyuk="KÖLE\nDEĞİLDİK!", vurgu="MÖ 2560"),
    "015": dict(buyuk="ÇIPLAK\nDEĞİLDİK!", vurgu="MÖ 776"),
    "016": dict(buyuk="Kartaca\nYIKILMALI!", vurgu="MÖ 149"),
    "017": dict(buyuk="80 MİL\nDUVAR!", vurgu="MS 122"),
    "018": dict(buyuk="FİLOZOFA\nÖLÜM!", vurgu="MÖ 399"),
    "019": dict(buyuk="BULUT\nOLDUM!", vurgu="MÖ 423"),
    "020": dict(buyuk="KÜTÜPHANE\nYANIYOR!", vurgu="MÖ 48"),
    "021": dict(buyuk="HARİTANIN\nUCU!", vurgu="MÖ 334"),
    "022": dict(buyuk="TACI KİM\nVERDİ?", vurgu="MS 457"),
    "023": dict(buyuk="ATIN İÇİNDE\nNE VAR?", vurgu="MÖ 1180"),
    "024": dict(buyuk="İLK TREN\n48 KM KORKUSU", vurgu="1830"),
}


def yazi_sigdir(cizim, metin, font_yolu, max_genislik, baslangic_boyutu, kontur):
    """Metni max_genislik'e sığdıran en büyük puntoyu bulur."""
    boyut = baslangic_boyutu
    while boyut > 30:
        font = ImageFont.truetype(font_yolu, boyut)
        kutu = cizim.textbbox((0, 0), metin, font=font)
        if kutu[2] - kutu[0] + 2 * kontur <= max_genislik:
            return font, kutu
        boyut -= 4
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

    # 0) sol taraf yumuşak siyah perdah — örnek kapaklardaki ağır siyah
    #    kütleler + metin kontrastı (soldan %60 genişliğe kademeli solar)
    for x in range(W):
        pay = 1.0 - x / (W * 0.60)
        if pay > 0:
            d.line([(x, 0), (x, H)], fill=(0, 0, 0, int(95 * pay)))

    # 1) MERAKLI rozeti (kırmızı) — sol üst, v4'te biraz küçük (başlık yer açar)
    y = 26
    f_rozet = ImageFont.truetype(F_XBOLD, 36)
    kutu = d.textbbox((0, 0), "MERAKLI", font=f_rozet)
    rw, rh = kutu[2] - kutu[0] + 42, kutu[3] - kutu[1] + 24
    d.rounded_rectangle([34, y, 34 + rw, y + rh], radius=12, fill=KIRMIZI + (255,))
    d.text((34 + 21, y + 12 - kutu[1]), "MERAKLI", font=f_rozet, fill=BEYAZ + (255,))
    y += rh + 18

    # 2) BÜYÜK İLGİ ÇEKİCİ BAŞLIK — beyaz, dev, kalın siyah kontur (sol blok)
    x0 = 40
    for satir in ayar["buyuk"].split("\n"):
        font, kutu = yazi_sigdir(d, satir, F_BLACK, 660, 156, 16)
        d.text((x0 + 8, y + 10), satir, font=font, fill=SIYAH + (140,),
               stroke_width=16, stroke_fill=SIYAH + (140,))
        d.text((x0, y), satir, font=font, fill=BEYAZ + (255,),
               stroke_width=16, stroke_fill=SIYAH + (255,))
        y += (kutu[3] - kutu[1]) + 26

    # 3) VURGU — KIRMIZI KUTU içinde beyaz yazı (örnek kapak imzası:
    #    kırmızı %15-24 blok vurgular; her kapakta düzgün kırmızı varlık)
    y += 4
    font, kutu = yazi_sigdir(d, ayar["vurgu"], F_BLACK, 560, 108, 0)
    tw, th = kutu[2] - kutu[0], kutu[3] - kutu[1]
    px_, py_ = 34, 16
    d.rounded_rectangle([x0, y, x0 + tw + 2 * px_, y + th + 2 * py_],
                        radius=14, fill=KIRMIZI + (255,),
                        outline=SIYAH + (255,), width=5)
    d.text((x0 + px_ - kutu[0], y + py_ - kutu[1]), ayar["vurgu"],
           font=font, fill=BEYAZ + (255,))

    # 4) sol alt seri etiketi
    etiket = f"EĞER ORADA OLSAYDIM — BÖLÜM {int(no)}"
    f_etiket = ImageFont.truetype(F_XBOLD, 28)
    d.text((x0 + 4, H - 52 + 4), etiket, font=f_etiket, fill=SIYAH + (150,),
           stroke_width=6, stroke_fill=SIYAH + (150,))
    d.text((x0, H - 52), etiket, font=f_etiket, fill=BEYAZ + (255,),
           stroke_width=6, stroke_fill=SIYAH + (255,))

    im = Image.alpha_composite(im, katman).convert("RGB")
    cikti_yolu = os.path.join(CIKTI_KLASOR, f"bolum-{no}.png")
    im.save(cikti_yolu)
    print(f"  ✓ bolum-{no}.png  ({ayar['buyuk'].replace(chr(10), ' ')} / {ayar['vurgu']})")
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
        metin = f"BÖLÜM {int(no)} · {BOLUMLER[no]['buyuk'].replace(chr(10), ' ')} · {BOLUMLER[no]['vurgu']}"
        kutu = d.textbbox((0, 0), metin, font=f)
        d.text((x + (tw - (kutu[2] - kutu[0])) // 2, y + th + 9), metin,
               font=f, fill=BEYAZ)
    yol = os.path.join(CIKTI_KLASOR, "ONIZLEME.png")
    sayfa.save(yol)
    print(f"  ✓ ONIZLEME.png ({len(ciktilar)} kapak)")


def main():
    secilen = sys.argv[1:] if len(sys.argv) > 1 else sorted(BOLUMLER)
    print(f"Kanal kırmızısı: RGB{KIRMIZI} · v4: büyük başlık + konu-kıyafetli Meraklı")
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
        # ONIZLEME her zaman TÜM mevcut kapaklarla (glob)
        import glob
        hepsi = [(os.path.basename(p)[6:9], p) for p in
                 sorted(glob.glob(os.path.join(CIKTI_KLASOR, "bolum-*.png")))]
        onizleme(hepsi)


if __name__ == "__main__":
    main()
