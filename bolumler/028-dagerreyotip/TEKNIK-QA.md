# B028 — Final teknik ve görsel QA

**PASS.** Ölçümler final MP4 üzerinden alındı.

- Dosya: `uzun/merakli-028-uzun-dagerreyotip.mp4`.
- Süre: **575.03 sn (9:35)**, boyut: **55,257,114 bayt**, GitHub 100 MB sınırının altında.
- 1920×1080, 30 fps, H.264/yuv420p; AAC 48 kHz stereo.
- MP4 atomları kontrol edildi: `moov`, `mdat` öncesinde; **faststart PASS**.
- Tüm video/ses akışları baştan sona FFmpeg ile çözüldü: dönüş kodu 0, hata çıktısı boş.
- 20 sahne, beş çift görsel (04/08/12/15/19), toplam 25. İkinci görüntüler sahne ortasında, süre/senkron korunuyor.
- 20 tarih bandı; giriş/kapanış/ayrı abone satırı mevcut. Caption katmanı yok, altyazı kapalı.
- 61 efekt yerleşimi + müzik; 10 benzersiz kaynak dosyasının tamamı mevcut ve `SFX-KUNYE.md` ile `YAYIN.md` içinde lisanslı.
- Ham anlatım 595,18 sn; sessizlik sıkıştırma sonrası 565,5 sn. Anlatım ×1,000, hızlandırma yok. Miks 575,00 sn.
- Kapanışta abone satırı finalde yaklaşık **5.60 sn** görünür; s20 ek süre 5,0 sn yalnız kart okunabilirliği içindir.
- Final ses ölçümü: integrated **-14.05 LUFS**, true peak **-1.44 dBTP**, LRA **3.00 LU**. Bunlar final dosyanın teknik ölçümleridir; tüm video insan gibi baştan sona dinlendi iddiası değildir.

## Sekiz kritik örnek kare
| Kare | Zaman (sn) | Sonuç |
|---|---:|---|
| giris | 1.50 | PASS — Tarih/giriş yazıları ayrı, dönem kıyafeti ve sade beyaz karakter sistemi korunmuş. |
| s04-temsili-kesit | 98.90 | PASS — Açık yan panel/optik görüntü TEMSİLÎ KESİT bandıyla ayrılmış, özgün çalışma şeması iddiası yok. |
| s07-koruksuz-kamera | 185.12 | PASS — İki kapalı sert sürgülü ahşap kutu, körük/film/flaş yok; iki ayrı el ve kol. |
| s12-iki-ayri-el | 320.01 | PASS — Bir el dış ahşap çerçeve kenarında, öteki el aşağıda; ek el/kol yok, cam/metal yüzeyine dokunma yok. |
| s13-sag-sol | 351.85 | PASS — Oda: pencere solda/sandalye sağda; metal görüntüde ters yerleşim gerçekten görülüyor. |
| s15-ayri-kagit-yolu | 407.21 | PASS — Mat kâğıt negatif/pozitif ve ayrı metal görüntü; 1841 kalotip bandıyla dönem ayrımı. |
| s17-yuzeye-dokunmadan | 461.09 | PASS — Açık avuç resimden uzakta, diğer el aşağıda; cam altındaki görüntü silinmiyor. |
| kapanis-abone | 574.03 | PASS — Soru/seçenek/abone ayrı satırlar, taşma/üst üste yazı yok; tek Meraklı ve iki ayrı el. |

## İçerik ve anatomi kilitleri
- Üretim sırasında bütün figürlerde tam 2 kol/2 ayrı el/2 bacak/2 ayak sayımı yapıldı. Birleşik eller yok; s05/s07/s10/s12 reddedilen eski örnekleri finalde kullanılmadı.
- Meraklı kahverengi yelek/gri önlük/kırmızı fularlı, beyaz yuvarlak kafa ve beyaz ince uzuvlu. Ziyaretçi giyinik beyaz çöp adam, fularsız; gerçekçi insan yok.
- Meraklı hayalî çırak, eğitim makinesi boş; gerçek fotoğraf ürettiği veya Daguerre'nin belgelenmiş yardımcısı olduğu söylenmiyor.
- Niépce'nin önceki çalışmaları, 7 Ocak/19 Ağustos 1839 ve 1841 kalotip ayrılıyor. Fotoğrafın bütünü için 1839 mutlak başlangıç sayılmıyor.
- Aktif kimyasal uygulama veya tarif yok, cıva buharı tehlikesi belirtiliyor. Bitmiş görüntü yüzeyine dokunma/silme yok.
- Metal tekil görüntü, mat kâğıt negatif/pozitif ve kâğıt çizim aynı nesne/yöntem sayılmıyor. Cam altındaki temsili görüntüler özgün arşiv fotoğrafı diye sunulmuyor.
- s09 temsili sokak, s10 esinli mimari, s15/s15b sonradan kurulmuş karşılaştırma; özgün olay mekânı/fotoğrafı iddiası yok.
- Modern kayıt/foley analojileri etiketli; filmli makine deklanşörü, flaş, kimyasal ısıtma/buhar efekti yok.
- Kapak v4: 1280×720, konu kıyafetli büyük Meraklı, ayrı büyük başlık/yıl etiketi; 2 kol/2 ayrı el, iki sert kutu kamera, körük yok. Yalnız uzun video; Shorts üretilmedi.
