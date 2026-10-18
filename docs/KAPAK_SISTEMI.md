# KAPAK (THUMBNAIL) SİSTEMİ — v2 KANONİK (2026-10-17'den itibaren)

## İlke

**Kapak hiç değişmez.** Tüm bölümlerin kapağı aynı "Meraklı düşünüyor"
temel sanatını, aynı "EĞER OLSAYDIM" rozetini ve aynı MERAKLI bandını
kullanır. Konu başına YALNIZCA başlık metni değişir. Başlıklar PIL ile
programatik basılır → Türkçe karakterler kusursuz, tipografi her kapakta
birebir aynı (piksel testiyle doğrulanır).

## Sabitler (asla değişmez)

| Öğe | Değer |
|---|---|
| Temel sanat | `kapaklar/temel/merakli-dusunuyor-16x9.png` (uzun video) / `...-9x16.png` (Shorts) |
| Poz | Meraklı taş üzerinde, çenesi elinde "düşünüyor" pozu, nötr kılıksız (zamansız) |
| Rozet | Sol üst kırmızı "EĞER OLSAYDIM" (sabit seri markası) |
| Başlık | Rozet altında 2 satır beyaz + siyah kontur (satır 1: konu, satır 2: yıl/mekân) |
| Marka bandı | Sol alt kırmızı "MERAKLI" + "EĞER OLSAYDIM SERİSİ" |
| Boyutlar | 1280x720 (uzun video) ve 1080x1920 (Shorts) |

## Üretim

```bash
# tek kapak
python3 araclar/kapak_yap2.py kapaklar/bolum-XXX.png "BAŞLIK 1" "BAŞLIK 2" [--dikey]
# tüm konular (55 konu x 2 format)
python3 araclar/kapak_yap2.py --tumu
```

Başlık eşlemesi `araclar/kapak_yap2.py` içindeki `BASLIKLAR` sözlüğündedir
(yeni konu eklendiğinde sözlüğe satır eklenir).

## Kalite Kontrol

- Piksel testi: her kapakta rozet bölgesi (40,30,600,140) ve bant bölgesi
  (40,620,700,720) tüm kapaklarla BİREBİR aynı olmalı (doğrulandı: 5 örnekte
  rozet=True, bant=True).
- Başlık en fazla 2 satır; satır 2'de yıl/mekân (örn. "1453 · İSTANBUL").
- Eski eylem-pozlu kapaklar `kapaklar/arsiv-v1/` klasöründe arşivlidir.

## Durum

- ✅ 55 konunun tamamı için 16:9 + 9:16 kapak üretildi
  (`kapaklar/bolum-001..055.png` + `kapaklar/shorts/bolum-001..055.png`).

---

# YouTube KÜÇÜK RESİM (THUMBNAIL) STANDARDI — v3 (2026-10-17'den itibaren)

Kullanıcı talimatı: YouTube örnek tarzı kapak — **dramatik sahne + sağ önde
BÜYÜK abartılı ifadeli Meraklı + büyük punto başlık (beyaz + kanal kırmızısı)**.
YouTube yüklemelerinde bu sistem kullanılır; video-içi künye kartları
(video_yap.py giriş/tarih/kapanış kartları) olduğu gibi kalır.

## Üretim

```
python3 araclar/thumbnail_yap.py 006    # tek bölüm
python3 araclar/thumbnail_yap.py        # sahnesi olan tüm bölümler
```

- Çıktı: `kapaklar/thumbnail/bolum-XXX.png` (1280×720) + `ONIZLEME.png` (kontak sayfası)
- Sahne: `kapaklar/thumbnail/sahne/bolum-XXX.jpg` — metinsiz AI sahnesi
  (karakter referansı ile üretilir; başlık PIL ile üstüne basılır)
- Tipografi (PIL, piksel keskin): Montserrat Black beyaz ana başlık + siyah
  kontur; kanonik kırmızı **(217,54,54)** vurgu satırı; kırmızı MERAKLI
  rozeti; alt bant "EĞER ORADA OLSAYDIM — BÖLÜM N"
- Bölüm başlıkları script içindeki `BOLUMLER` sözlüğünde tutulur
- **KALICI KURAL (kullanıcı talimatı, 2026-10-17): Shorts videolar için kapak
  fotoğrafı ÜRETİLMEZ.** Küçük resim yalnızca uzun/ana videoya yapılır
  (Shorts'ta YouTube özel küçük resim de desteklemez; ilk kare esas alınır).
- Yeni paketlerde Tur D standart adımıdır (B006+); B001-B006 retrofit edildi

---

## v4 — YÜRÜRLÜKTEKİ KAPAK STANDARDI (2026-10-18, kullanıcı talimatı)

Örnek referans: `docs/kapak-ornek/youtube-ornek-1.jpg` (kullanıcı yüklemesi;
piksel analizi: kırmızı vurgu #C03030 ≈ kanal kırmızısı, kalın koyu
kontur kütleleri, yüksek kontrast/parlaklık).

Kurallar (yalnız uzun/ana videolara; Shorts'a kapak YOK — v3 sürer):
1. **SAHNE GÖRSELİ** (AI, metinsiz, `sahne/bolum-XXX.jpg`): Meraklı
   BÜYÜK — tuvalin sağ ~%40'ı, kafa ~%30 yükseklik; bölümün konusuna
   özgü KIYAFET (gladyatör miğferi, fırıncı önlüğü, halatçı kuşağı...);
   ABARTILI ifade (şok/hayranlık/kararlılık); arka planda dramatik konu
   sahnesi; sol %55 yazı için temiz.
2. **BÜYÜK BAŞLIK** ("buyuk", 2-4 kelime konuya özel çengel):
   Montserrat-Black ~150 px, beyaz + 14 px siyah kontur, sol blok.
   Sözlük: "SURLAR ÇÖKÜYOR!" (001), "DEV ŞAHİ GELİYOR!" (002),
   "GEMİLER KARADAN!" (003), "SON HÜCUM!" (004), "TARİH DÖNDÜ!" (005),
   "KARA VEBÂ!" (006), "18 SAATİN VAR!" (007), "4 DAKİKA!" (008),
   "DÜNYA DUYDU!" (009), "ŞEHİR SİLİNDİ!" (010), "4 GÜN ATEŞ!" (012),
   "ÖLÜM KALIM!" (013), "KÖLE DEĞİLDİK!" (014).
3. **VURGU satırı** ("vurgu"): yıl/anahtar kelime, kırmızı
   RGB(217,54,54) ~110 px + siyah kontur.
4. MERAKLI rozeti sol üst (kırmızı); "EĞER ORADA OLSAYDIM — BÖLÜM N"
   etiketi sol alt.
5. Eski (v3) sahne görselleri v4 kompozisyonu içermez; bölüm kapakları
   YENİLENECEKSE sahne görseli de v4 kompozisyonuyla yeniden üretilir
   (kullanıcı onayına bağlı).
