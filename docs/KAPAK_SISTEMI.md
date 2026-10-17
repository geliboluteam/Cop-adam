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
