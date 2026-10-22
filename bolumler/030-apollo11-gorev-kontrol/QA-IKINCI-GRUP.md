# B030 — İkinci üretim grubu QA / 22 Ekim 2026

> TARİHÎ ARA KAYIT: s12b/s14 sonraki grupta düzeltildi; güncel25görselPASS. Final durum URETIM-DURUMU.json / TEKNIK-QA.md içinde.

**Güncel: 17/25 PNG mevcut; 15 PASS, 2 DÜZELTME; 8 yeni görsel eksik. 20/20 voice-03 Türkçe anlatım hazır. Final video yok.**

Kostüm kullanıcı tarafından önceki s01 sunumundan sonra **Devam** ile onaylandı; tekrar onay beklenmiyor. Bu grupta 10 görsel çağrısı = 9 yeni dosya + 1 s04b AI düzeltmesi; 10 anlatım çağrısı = s11–s20. Yerel çizim/kompozit düzeltmeleri ayrıca yapıldı.

## Görsel denetim

Her sahne ayrı `read_file` ile incelendi. Her ana figürde ve üç yan figürde kol sayısı, **ayrı el sayısı**, bacak ve ayak sayısı ayrı denetlendi. Dosyanın teknik olarak açılması anatomi veya kostüm PASS anlamına gelmez.

| Görsel | Kişi | Sonuç | Not |
|---|---:|---|---|
| s01/s02/s03/s04/s05/s06/s07 | her biri4 | Önceki7 PASS korundu | Dosyaları değiştirilmedi; s01 kullanıcı onaylı |
| s04b |4| PASS — düzeltildi | Yan figürler AI ile ayrıldı. Meraklı sol elde tek kalem tutar, sağ eli aşağıda ayrı. İlk AI düzeltmesindeki top biçimli sağ el, önceki çizimden alfa maskeli el/önkol ile değiştirildi; büyütülmüş el ayrıntısı tekrar incelendi. Diğer6el boş/ayrı. Uzun çizim kolu krem figürün önünden geçer ama uzuv veya el birleşmesi yok |
| s08 |4| PASS | Guidance/flight/CAPCOM rol temsilleri, tüm2kol/2ayrıel/2bacak/2ayak açık; uyarı sayıları sonradan bantta |
| s08b |4| PASS — yerel çizim/renk | Ayrı destek odası. İki küçük yüzde eksik kaş/burun/ağız tamamlandı; Meraklı yeleğinin ana yüzeyi petrol tonuna çevrildi, kenar/rib gölgeleri muted. Tüm uzuvlar/eller açık |
| s09 |4| PASS — yerel yüz çizgileri | MIT geriye bakış. Hamilton rolü zeytin hırka/lacivert etekli beyaz çöp figür, iki yazılım uzmanı ve Meraklı. Üç yüzde eksik küçük çizgiler tamamlandı. Tüm uzuvlar açık. Meraklı bu MIT ziyaret çiziminde kulaklık takmıyor; fular/kıyafet kimliği korunuyor |
| s10 |4| PASS | Ayrı figürlerle değerlendirme; kenetlenmiş el yok |
| s11 |4| PASS | Ayrı levhada iki küçük kabin figürlü temsili araç şeması; bunlar odaya ek kontrolörler değil. Kumanda/joystick yok. Fular bir yan figür gövdesi önünden geçer ama elleri örtmez |
| s12 |4| PASS | Veri/irtifa grafikleri, ayrı eller ve ayaklar; kesin sıfır kronometresi veya canlı iniş videosu yok |
| **s12b** |4| **DÜZELTME / PASS sayılmadı** | Uzuvlar ayrı; ancak Meraklı baş oranı kanonik büyük baş kimliğine göre küçük, ana figür ayrımı zayıf. Baş/kadraj düzeltmesi gerekiyor |
| s13 |4| PASS | Veri ekranları, ayrı kâğıt krater şeması; canlı Ay iniş videosu yok. Tüm uzuvlar açık |
| **s14** |4| **DÜZELTME / PASS sayılmadı** | Eller/ayaklar ayrı, fakat üç yan figürde dönem pantolonu eksik. Giyinik rol/dönem kostümü şartı nedeniyle düzeltilecek |

- Tüm17 sahne PNG'si **1920×1080**. Ham çıktılar çok küçük merkez kırpma/ölçekleme ile16:9 normalize edildi; bütün ayaklar kadraj içinde.
- Yan figürler de beyaz yuvarlak başlı, sade yüzlü, beyaz uzuvlu çöp adamlar. Gerçekçi insan/ten rengi gövde yok. Kırmızı fular yalnız Meraklı'da. s14'ün eksik pantolonları özellikle başarısız sayıldı.
- `uzun/kompozit-kaynaklari/IKINCI-GRUP-DUZELTMELER.json`: yerel müdahaleler ve final PNG SHA256. `s04b-ayri-el-kaynagi.png`: önceki çizimden çıkarılmış alfa maskeli el/önkol kaynağı. Bu yerel çizim/kompozit işlemleri NASA arşiv görüntüsü değildir.
- İlk grubun raporu tarihî checkpoint olarak `QA-ILK-GRUP.md` içinde korunur; eski s04b FAIL kaydı artık güncel durum değildir.

## Anlatım teknik QA

- **s01–s20 / voice-03 / Türkçe**. İlk10 ses tekrar üretilmedi.
- 20/20 MP3 tam FFmpeg decode; kaynak metin SHA256 ve dosya SHA256 kayıtlı.
- Ham toplam **734,136sn**. `video_yap.narr_isle(...,1.0)` sessizlik düzenlemesi sonrası **700,18sn**.
- Her iki toplam alanı da20 klibi kapsar; ilk yarının357,57sn değeri artık toplam değildir.
- Bu bir final video süresi değildir. Arşiv, geçişler ve ayrı giriş/kapanış/abone kartları yerleştirilince nihai hız ve5–12dk denetimi yapılacak. Henüz final hız seçilmedi.
- Teknik decode ve üretime verilen metnin eşleşmesi denetlendi; insan gibi tam dinleme veya bağımsız ASR yapılmış gibi iddia edilmez.

## Tarihî ses edinimi

- `uzun/arsiv-sesleri/eagle-has-landed-islenmis.mp3`: **58023bayt / 9,613061sn / 22050Hz / mono / tamdecode PASS**.
- NASA/JSC Apollo11 Audio Highlights kökenli **işlenmiş** kopya. Edinim commit'i `seankd3/orbital-mechanics@5f0ad6b09eca781416cc333bed557004499766da`; GitHub blob `5bca917fb5b34158626b9a690d345102a779c54c`.
- Dosya SHA256 `ba45c8de4e9f22ccc0e05b818642eec0775175081413da622a1b82e252d064d3`.
- Aynı commit'teki README/clipJSON/cut.py okundu: kaynak reel1335.1–1337.95 ve1338.3–1345.0sn birleştirilmiş, sessizlik atılmış;250–3600Hz bandpass,−18LUFS hedefi, fade ve22.05kHzmono48kbps MP3 işlemleri açıklanıyor. **Kesintisiz ham olay kaydı denmez.**
- Kaynak beyanı NASA/JSC federal kayıt / Public Domain Mark; bu bir NASA onayı veya sınırsız üçüncü taraf lisansı değildir. Ayrıntı `KAYNAK.json` ve `SFX-KUNYE.md` içinde.
- Yayıncının eşlediği caption ve gerçek iniş konuşmasının tarih/rol bağlamı kontrol edildi. **Bu bizim bağımsız işitsel transkript doğrulamamız değildir. Son içerik/kesit incelemesi henüz bekliyor.** Duyulmayan sözleri duyulmuş gibi raporlama yok.
- Yerel ek işlem yapılmadı, miks yok. s15 Türkçe girişinden sonra anlatıcı susacak; arşiv ayrı katmanda normal hızda çalacak. GERÇEK KAYIT yalnız o aralıkta; çizimler hep TEMSİLÎ.

## Sonraki kabul kapıları

1. s12b baş oranı ve s14 üç yan figürün dönem pantolonları. Düzeltmelerden sonra tüm elleri/ayakları yeniden incele.
2. Eksik8PNG: **s15/s15b/s16/s17/s18/s19/s19b/s20**. Minimum4 kanonik giyinik figür;25/25 PASS olmadan render yok.
3. Anlatımlar TAMAM, tekrar üretme. Arşiv son içerik/kesit denetimi, CC0 foley teknik kontrolü/yerleşim ve ayrı miks.
4. s15 yalnız alıntı aralığında GERÇEK KAYIT; s19b24Temmuz ayrı tarih bandı. Bütün çizimler TEMSİLÎ; altyazı yok.
5. Kartlar yüzleri örtmeden, birbirinden ayrı. Kapanışta **KANALIMA ABONE OLMAYI UNUTMAYIN!**
6. Nihai plan/hız/süre, video render, kapakv4, YAYIN, loudness/truepeak/tamAVdecode/faststart ve kritik kare QA. Henüz final video veya kapak yok.
7. Commit→hemen push→uzak HEAD/blob doğrulama. B018 kullanıcı dosyalarına dokunma.
