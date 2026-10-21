# B027 — Final teknik ve görsel QA

- Durum: **PASS**. Ölçümler final MP4 üzerinden alındı.
- Dosya: `uzun/merakli-027-uzun-turtle-denizalti.mp4`.
- Süre: **613.77 saniye (10:14)**; boyut: **57,729,087 bayt** (<100 MB).
- 1920×1080, 30 fps, H.264/yuv420p; AAC, 48 kHz stereo; MP4 faststart.
- Tüm video ve ses akışları FFmpeg ile baştan sona çözüldü: dönüş kodu 0, hata çıktısı boş.
- 20 anlatım sahnesi; 5 sahnede ikinci görsel (04/08/12/15/19), toplam 25. Ses/görüntü süresini değiştirmeyen orta nokta geçişi.
- 20/20 tarih bandı; giriş/kapanış/ayrı abone satırı mevcut. Caption katmanı yok; altyazı kapalı.
- 66 efekt yerleşimi + müzik; 12 benzersiz kaynak dosyanın tamamı `SFX-KUNYE.md` ve `YAYIN.md` içinde lisanslı.
- İşitsel ölçüm: integrated **-14.02 LUFS**, true peak **-1.46 dBTP**, LRA **3.10 LU**. Bunlar final dosyanın ölçümleridir; anlatıcı her an dinlenerek denetlendi iddiası değildir.

## Kritik örnek kare denetimi
| Kare | Zaman (sn) | Sonuç |
|---|---:|---|
| giris | 1.50 | PASS — Giriş ve tarih yazıları ayrı; sahne korunmuş. |
| s09-kurgu | 258.72 | PASS — Karada açık kapak, tek Meraklı; 2 kol/2 ayrı el/2 bacak/2 ayak. Yeni ses “dizlerime” ile uyumlu. |
| s12-lee | 344.04 | PASS — Görevde yalnız Lee; gri yelek, fular yok, 2 kol/2 el/2 bacak/2 ayak. |
| s17-kiyi | 497.42 | PASS — Meraklı kıyıda, düz pirinç kapak; kraliyet tacı hatası yok. |
| s20-soru | 589.37 | PASS — Meraklı tek figür; iki ayrı el, tam uzuv sayısı. |
| kapanis-abone | 613.32 | PASS — Soru, seçenekler ve KANALIMA ABONE OLMAYI UNUTMAYIN! ayrı satırlar; taşma/çakışma yok. |

## İçerik ve dürüstlük kilitleri
- AI temsili rekonstrüksiyonlar; özgün kamera kaydı veya mühendislik çizimi iddiası yok.
- Meraklı'nın çıraklığı/testi/yorumu kurgu; gerçek görevde ikinci kişi eklenmez.
- Görev ayrıntıları Lee'nin sonradan aktarımı olarak ayrılır; bakır kesin neden sayılmaz.
- Drebbel/Turtle/Hunley/Holland aynı tarihe sıkıştırılmaz; s18 yalnız temsili model sergisi.
- Sonraki model/çizimler özgün Turtle diye sunulmaz; s19 Smithsonian'ın 1986 modelini birebir gösterme iddiası taşımaz.
- Özgün 1776 sesi yok; modern kayıt/foley analojileri künye ile etiketli; patlama/motor/sonar yok.
- Kapak v4, 1280×720: onaylı s09'dan yakınlaştırma/aynalama, konu kıyafeti, büyük başlık, ayrı yıl etiketi. Shorts yok.
