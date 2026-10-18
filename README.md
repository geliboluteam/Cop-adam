# ÇÖP ADAM — "Eğer Orada Olsaydım" Tarih Serisi

Karakterimiz **MERAKLI**: kırmızı fularlı, burunlu-ağızlı, beyaz insansı çöp
adam. Tarihin en büyük anlarının **tam ortasına** düşer — YouTube Shorts
serisinin üretim deposu.

> Karakter hiç değişmez: hep aynı beyaz çöp adam (nokta gözler, küçük burun,
> ifadeli ağız), boynunda hep aynı kırmızı fular. Değişen tek şey kıyafetleri
> ve içinde bulunduğu tarihtir.

## Depo Yapısı

```
README.md                  -> bu dosya
docs/
  KANAL_KIMLIK.md          -> kanal/seri kimliği, format kuralları, ton
  KARAKTER.md              -> Çöp Adam karakter kitabı (değişmez kurallar)
  SES_POLITIKASI.md        -> ses efekti + lisans politikası
  YOL_HARITASI.md          -> 56 bölüm konusunun planı ve durumu
  YOUTUBE_YAYIN_REHBERI.md -> başlık/açıklama/etiket şablonları, yükleme listesi
karakter/                  -> karakter referans görselleri
arastirma/                 -> bölüm başına kaynaklı tarih araştırması
senaryo/                   -> bölüm senaryoları (sahne + ses + efekt planı)
sfx/                       -> ses efekti arşivi + SFX_KAYITLARI.md (lisanslar)
bolumler/                  -> üretilen bölümler (görsel, ses, video, yayin metni)
kapaklar/thumbnail/        -> GÜNCEL bölüm kapakları — v4 standardı
                              (üretici: araclar/thumbnail_yap.py; sahne/ altında
                              hero görüntüleri + ONIZLEME.png kontak sayfası)
kapaklar/                   -> yalnızca thumbnail/ alt klasörü vardır
                              (eski arşivler 2026-10-18'de silindi; gerekirse git geçmişinde)
araclar/                   -> ffmpeg, fontlar, video üretim betikleri
```

## Bölüm Üretim Akışı

1. **Araştırma** — `arastirma/NNN-*.md` (tarih, kaynaklar, çelişkiler, "efsane mi gerçek mi" notları)
2. **Senaryo** — `senaryo/NNN-*.md` (~57 sn, en az 10 sahne, sahne başına efekt işaretleri)
3. **Seslendirme** — seçilmiş Türkçe anlatıcı sesi, sahne sahne kayıt
4. **Görseller** — karakter referansı ile 9:16 sahne görselleri (dönem kıyafetli)
5. **Ses efektleri** — `sfx/` arşivinden, lisanslar `SFX_KAYITLARI.md`'de belgeli
6. **Kurgu** — `python3 araclar/video_yap.py <plan.json> <cikti>.mp4`
   (Ken Burns + xfade + miks + loudnorm; Shorts 1080x1920 ~55 sn, uzun video
   1920x1080 5-10 dk `hedef_sure` ile; altyazı yalnızca ilk 3 bölümde)
7. **Yayın** — `bolumler/NNN-*/YAYIN.md` (başlık, açıklama, etiketler, künye)
8. **Git** — her bölüm kendi commit'i olarak bu depoya işlenir

## Ses ve Görsel Künye Politikası (Özet)

- Ses efektleri **gerçek kayıtlardır**; kaynak URL + lisans her ses için
  `sfx/SFX_KAYITLARI.md` dosyasında ve video açıklamasında belgelenir.
- Sadece **CC0 / CC-BY / CC-BY-SA / kamu malı** lisanslı sesler kullanılır.
- Tarihsel olayın çağdaş kaydı yoksa (ör. 1453 top sesi) **modern analoji**
  kullanılır ve asla "özgün dönem sesi" gibi sunulmaz. Doğa sesleri (rüzgâr,
  dalga, ateş, cırcır böceği) türdeş gerçek kayıtlardır.
- Görseller yapay zekâ ile üretilir; videoda ve açıklamada belirtilir.
