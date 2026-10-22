# B030 Apollo 11 — Nihai teknik ve görsel kontrol

**SONUÇ: PASS · 22 Ekim 2026 · 11:38 uzun video.**

## Ölçülmüş dosya
- Video: `uzun/merakli-030-uzun-apollo11-gorev-kontrol.mp4`
- 33,023,221 bayt; MP4 kapsayıcı süresi 698.000 sn; kare takvimi 697.933333 sn (20938 kare). Kapsayıcı/örnek yuvarlaması farkı 0,067 sn. 5–12 dakika şartı sağlandı.
- H.264 High / yuv420p / 1920×1080 / 30 fps; AAC-LC / 48000 Hz / stereo. `moov` atomu `mdat` önünde: faststart PASS.
- Tam ses+görüntü decode: FFmpeg dönüş kodu 0, hata çıktısı boş. Birkaç kare açmanın yerine tam decode da yapıldı.
- Final ses: **-14.01 LUFS / -1.36 dBTP / LRA 3.10 LU**. Hedef −14 LUFS/−1,5 dBTP; kabul −15…−13 LUFS, TP≤−1 dBTP.
- SHA256: `2222978930f657e08f3126c416f2af6a0cd7109fd54b06ce63f0c1a42de2ffd3`

## İçerik / senkron / kaynak testleri
- 20 sahne, 25 PNG, 4 ayrı kart = 29 klip. Her klibin ortasından final videodan kare alınıp gerçek kaynakla karşılaştırıldı: **29/29 PASS**. Başlık alanı dışındaki RGB mutlak fark eşiği <9; ayrıntı JSON içinde. Bu, yalnız dosya varlığı kontrolü değildir.
- 25 PNG 1920×1080 ve kaynak SHA256 kontrolü PASS. Kullanıcının onayladığı s01 değişmedi.
- 20 voice-03 kaynak MP3 SHA256 ve kaynak anlatı metni SHA256 eşleşmesi PASS; yeni TTS yok. İlk üretimdeki tam decode kayıtları `ANLATIM-SURE-OLCUMU.json` içinde. Anlatım finalde 1,06×; 660,743354 sn PCM.
- NASA/JSC kökenli işlenmiş mirror alıntısı kaynak SHA256 eşleşmesi PASS; normal **1,0×** hız, **517,674417–527,224458 sn**, decode PCM **9,550042 sn**. MP3 kapsayıcıdaki 9,613061 sn encoder padding farkıdır.
- Ölçülmüş konuşma aralıkları birbiriyle çakışmıyor. Arşiv boyunca Türkçe anlatı ve foley yok. “GERÇEK KAYIT” etiketi yalnız o aralıkta; görsel aynı anda da “AI TEMSİLÎ”. Önce/içinde/sonra üç kare açıldı.
- 7 modern foley yerleşimi, 3 CC0 kaynak dosya: ayrıca tam decode PASS (`uzun/FOLEY-QA.json`). Her modern sesin sırasında MODERN ANALOJİ etiketi; ilk örnek 7,3 sn karesinde görüldü. Bu sesler NASA oda kaydı veya 1202 alarmı değildir.
- Altyazı yok; yalnız bağlam/tarih/kaynak etiketleri. Müzik yok. 04/08/12/15/19 ikinci görselleri anlatı süresini uzatmadan yaklaşık ortada değişir; ayrı tarih gerekli s19b 24 Temmuz bandı.
- Statik tam kadraj, 0,4 sn xfade. Dört ayrı giriş/tarih/kapanış/abone kartı. Abone metni iki satırda: **KANALIMA ABONE OLMAYI UNUTMAYIN!**

## Görsel kontrolün kapsamı
Aşağıdaki **16 kritik kare gerçekten açılıp incelendi**. Kartlar okunur; tarih ve kaynak başlıkları yüz/ellerden ayrı. Kritik anlatı karelerinde giyinik beyaz çöp adamlar, Meraklı'nın kırmızı fuları ve ayrık iki el/kol kontrol edildi. Kaynak 25 görselin önceki anatomi kontrolü ayrıca manifestte; beş yerel kompozitin kaynağı ve hashleri açıkça kaydedildi. s20 el sallamaz, iki eli açık/aşağıdadır. Kapak v4 ayrıca açılıp kontrol edildi; kaynak s14'ün yüzü değil, yalnız kapak kopyasının yüzü rötuşlandı.

| Kritik kare | Saniye | İnceleme |
|---|---:|---|
| 01-giris.jpg | 1.300 | PASS |
| 02-tarih.jpg | 4.100 | PASS |
| 03-s01-modern.jpg | 7.300 | PASS |
| 04-s04b.jpg | 132.000 | PASS |
| 05-s09.jpg | 294.000 | PASS |
| 06-s12b.jpg | 407.000 | PASS |
| 07-s14.jpg | 464.000 | PASS |
| 08-kayit-oncesi.jpg | 517.424 | PASS |
| 09-gercek-kayit.jpg | 520.000 | PASS |
| 10-kayit-sonrasi.jpg | 527.474 | PASS |
| 11-ilk-adim.jpg | 610.000 | PASS |
| 12-yukselis.jpg | 636.000 | PASS |
| 13-donus24temmuz.jpg | 650.000 | PASS |
| 14-s20.jpg | 678.000 | PASS |
| 15-kapanis.jpg | 692.400 | PASS |
| 16-abone.jpg | 696.000 | PASS |

## Sınırlamalar / doğrulamadığımız şeyler
Bu teknik ve kare bazlı görsel kontroldür; bütün videoyu gerçek zamanda izleme veya insan dinlemesi yapıldığı iddia edilmez. Arşiv içeriği belgeli edinim zinciri, yayıncı caption eşlemesi ve ALSJ bağlamına dayanır. Caption tam kelimekelime transkript değildir. PocketSphinx radio ASR denemesi düşük güvenliydi ve doğrulanmış transkript olarak kullanılmadı. Whisper modeli ağ kısıtı nedeniyle alınamadı; Whisper çalıştırıldı denmez. Public Domain Mark yeni lisans izni değil durum işaretidir. İşlenmiş mirror kesiti kesintisiz ham kayıt diye sunulmaz.

## Yeniden kontrol / üretim
- `python bolumler/030-apollo11-gorev-kontrol/uzun/render_b030.py` (uzun render, Python/Pillow ve depodaki FFmpeg/fontlar)
- `python bolumler/030-apollo11-gorev-kontrol/uzun/qa_b030.py` (teknik raporu yeniden üretir; insan/model kare inceleme bayrağını kendiliğinden PASS yapmaz)
- Yeni render sonrası teknik rapor ve kritik kareler yeniden kontrol edilmeli; önceki görsel onayı otomatik taşınmamalı. Teslim manifesti, plan ve yayın belgelerindeki SHA/süreler yeni dosyayla yeniden eşleştirilmelidir.
- `.cache/b030-render` çalışma önbelleğidir, depoya dahil değil. Kaynak görselleri değiştirirsen önbelleği kaldırarak yeniden üret; kliplerin gerçek kaynakla eşleşmesini QA tekrar kontrol eder.
