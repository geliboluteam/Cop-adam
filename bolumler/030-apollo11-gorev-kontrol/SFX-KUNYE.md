# B030 — NİHAİ SES KÜNYESİ

**20 anlatım + 1 tarihî radyo alıntısı + 7 modern foley yerleşimi. Müzik yok.** Video 11:38. Zamanlar final videonun başlangıcına göre saniye.

## Anlatım
Aynı Türkçe **voice-03**, s01–s20. Ham 734,136 sn; sessizlik düzenlemesi 1× hızda 700,18 sn; final 1,06× hızda 660,743354 sn PCM anlatım. 20 MP3/metin SHA256 ve decode `ANLATIM-SURE-OLCUMU.json` içinde. Arşiv/anlatıcı taklidi yapılmadı. Konuşma aralıkları birbirine binmez.

## Gerçek tarihî kayıt — NASA/JSC kökenli İŞLENMİŞ ALINTI
- Dosya: `uzun/arsiv-sesleri/eagle-has-landed-islenmis.mp3`; 58023 bayt, 22050 Hz mono / 48 kbps MP3; konteyner 9,613061 sn. MP3 encoder padding sonrası decode PCM **9,550042 sn**; videoda bu PCM süresi kullanıldı, yeni kelime/süre kesilmedi.
- Konum: **517.674417–527.224458 sn** (08:37–08:47), s15. **Hız 1,0×**; Türkçe anlatıcı susar ve foley yok. Göreli gain +3 dB, ardından bütün miks iki-pass loudness; kaynak MP3 baytları değişmedi.
- SHA256 `ba45c8de4e9f22ccc0e05b818642eec0775175081413da622a1b82e252d064d3`; GitHub blob `5bca917fb5b34158626b9a690d345102a779c54c`.
- Kaynak beyanı: NASA/Johnson Space Center **Apollo 11 Audio Highlights**, https://archive.org/details/Apollo11AudioHighlights / **Public Domain Mark**. PDM bir durum işaretidir, yeni lisans izni değildir. Federal kayıt atfı korunur; NASA onayı veya sınırsız üçüncü taraf izni ima edilmez.
- Edinim/işlem kredisi: **seankd3/orbital-mechanics**, commit `5f0ad6b09eca781416cc333bed557004499766da`: https://github.com/seankd3/orbital-mechanics/blob/5f0ad6b09eca781416cc333bed557004499766da/public/audio/apollo11/eagle-has-landed.mp3 . README/clip JSON/cut.py aynı committen okundu.
- Mirror işlem zinciri: kaynak reel 1335.1–1337.95 ve 1338.3–1345.0 sn birleştirme/sessizlik atma; 250–3600 Hz bandpass; −18 LUFS / −2 dBTP hedefi; fade; 22.05 kHz mono / 48 kbps MP3. Reel de highlight derlemesi. **Kesintisiz ham olay kaydı denmez.**
- İçerik dayanağı: yayıncının caption eşlemesi ve ALSJ iniş konuşması bağlamı. Caption çekirdek “Tranquility Base / Eagle has landed / copy you on the ground” sözlerini listeler; tam kelime kelime transkript değildir. Bağımsız insan dinlemesi yapılmadı. PocketSphinx ASR düşük güvenli çıktı verdi ve doğrulama/altyazı olarak kullanılmadı; Whisper model indirmesi ağ kısıtıyla başarısız, Whisper çalıştı denmez. Bu sınırlamalar `KAYNAK.json` içinde.
- Kaynak bağlamı: https://www.nasa.gov/historical-sounds/ ; hak rehberi https://www.nasa.gov/nasa-brand-center/images-and-media/ . Resmî NASA kısa/extended MP3 dosyaları indirilmedi; edinilen mirror onlarla bayt eşit diye sunulmaz.
- **GERÇEK KAYIT** etiketi yalnız alıntı süresince. Çizim aynı anda da **AI TEMSİLÎ**. Genel Türkçe anlatım NASA sesi diye etiketlenmez.

## Modern gerçek kayıtlar — MODERN ANALOJİ
Üç kaynak: **OwlishMedia / Sound Effects Pack / CC0**; https://opengameart.org/content/sound-effects-pack . Sayfadaki paket künyesi depodaki free-sfx/Owlish kaynağıyla birlikte tutulur. Üç dosya tam decode kontrol edildi. Kâğıt kaynağı 0,60 sn; kalem 30,42 sn; kumaş 9,95 sn. Yalnız aşağıdaki kısa başlangıç kesitleri, düşük gain ve kısa fade ile kullanıldı; NASA oda sesi/alkış/motor/1202 alarmı değildir.

| Sahne | Final aralık (sn) | Kaynak dosya | Göreli gain | Etiket/hak |
|---|---|---|---|---|
| s01 | 6.700–8.100 | `sfx/free-sfx/Owlish/Sound Effects Pack/Cloth, Rustle/320137__owlstorm__blanket-movement-1.opus` | -27 dB | MODERN ANALOJİ / OwlishMedia / CC0 |
| s03 | 84.867–85.467 | `sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pageturn1.opus` | -27 dB | MODERN ANALOJİ / OwlishMedia / CC0 |
| s05 | 150.300–150.900 | `sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pageturn1.opus` | -27 dB | MODERN ANALOJİ / OwlishMedia / CC0 |
| s07 | 225.233–226.733 | `sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pencil-scratch-1.opus` | -27 dB | MODERN ANALOJİ / OwlishMedia / CC0 |
| s10 | 332.833–333.433 | `sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pageturn1.opus` | -27 dB | MODERN ANALOJİ / OwlishMedia / CC0 |
| s17 | 573.133–573.733 | `sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pageturn1.opus` | -27 dB | MODERN ANALOJİ / OwlishMedia / CC0 |
| s20 | 661.733–662.933 | `sfx/free-sfx/Owlish/Sound Effects Pack/Cloth, Rustle/320137__owlstorm__blanket-movement-1.opus` | -27 dB | MODERN ANALOJİ / OwlishMedia / CC0 |

## Miks / ölçüm
48 kHz stereo AAC / hedef 160 kbps; iki-pass loudnorm hedef −14 LUFS / −1,5 dBTP. Final ölçüm **−14,01 LUFS / −1,36 dBTP / LRA 3,10 LU**. Tam AV decode PASS. Radyo normal hızda, anlatıcı ve foley ile çakışmıyor; bu aralık kontrolü ölçülmüş zamanlara dayanır. Modern sesler 1969 görev kaydı diye sunulmaz. Ay boşluğunda duyulan motor/rüzgâr iddiası veya sentetik “tarihî alarm” yok.
