# B030 — SES KÜNYESİ / EDİNİM TAMAM, HENÜZ MİKS DEĞİL

**Durum:**20/20 voice-03 Türkçe anlatım hazır; NASA/JSC kökenli işlenmiş radyo alıntısı edinildi, provenans ve teknik decode kontrol edildi. Arşiv son içerik/kesit denetimi, foley yerleşimi ve final miks/video henüz yok. Aşağıdaki liste bir finalde kullanılmış ses listesi değildir.

## 1. Anlatım

- Aynı seçilmiş **voice-03**, Türkçe; s01–s20. Anlatıcı gerçek astronot veya NASA görevlisinin taklidi değildir.
- Ham734,136sn; sessizlik düzenlemesi1×700,18sn. Klip süreleri/SHA256/metinSHA256/decode `ANLATIM-SURE-OLCUMU.json` içinde. Final hız ve video süresi henüz belirlenmedi.
- Teknik20/20 tamdecode PASS; insan gibi tam dinleme veya bağımsızASR yapıldığı iddia edilmez.

## 2. Tarihî radyo kaydı — edinilen işlenmiş kısa alıntı

| Alan | Kayıt |
|---|---|
| Yerel dosya | `uzun/arsiv-sesleri/eagle-has-landed-islenmis.mp3` |
| Asıl kayıt | NASA / Johnson Space Center, Apollo11 air-to-ground /20Temmuz1969 iniş bildirimi |
| Kaynak reel beyanı | NASA/JSC **Apollo11 Audio Highlights**, https://archive.org/details/Apollo11AudioHighlights |
| Edinim | https://github.com/seankd3/orbital-mechanics/blob/5f0ad6b09eca781416cc333bed557004499766da/public/audio/apollo11/eagle-has-landed.mp3 |
| Mirror commit / blob | `5f0ad6b09eca781416cc333bed557004499766da` / `5bca917fb5b34158626b9a690d345102a779c54c` |
| Boyut / süre / biçim |58023bayt / **9,613061sn** /22050Hz mono MP3, nominal48kbps |
| SHA256 | `ba45c8de4e9f22ccc0e05b818642eec0775175081413da622a1b82e252d064d3` |
| Teknik kontrol | Baştan sona FFmpeg decode çıkış0/hata yok |
| Yerel işlem | Dosya baytları değiştirilmedi. Henüz kesme/miks/hız değiştirme yok |

### Kaynak ve hak/işlem açıklaması

- Mirror README, kaynağı NASAJSC federal kayıt ve **Public Domain Mark** taşıyan reel olarak tanımlıyor. PDM kamu malı durum işaretidir, yeni bir lisans izni değildir. NASA kaydı ve basit sinyal/kesit işlemleri için kaynak zinciri açıkça korunur; üçüncü taraf malzemelerine sınırsız izin veya NASA onayı varsayılmaz.
- README: https://github.com/seankd3/orbital-mechanics/blob/5f0ad6b09eca781416cc333bed557004499766da/scripts/mission-audio/README.md
- Kesitler: aynı commit `scripts/mission-audio/clips.json`; kaynak reel **1335.1–1337.95sn** + **1338.3–1345.0sn**.
- İşlem betiği: aynı commit `scripts/mission-audio/cut.py`.250–3600Hz bandpass;−18LUFS/−2dBTP hedefi;22.05kHzmono48kbps MP3; giriş/çıkış fade; parçalar birleştirilerek sessizlik atılmış. Reel de zaten highlight derlemesi. İşlem/kesit hazırlığı için **seankd3/orbital-mechanics** kredisi verilir.
- Bu dosya **kesintisiz ham olay kaydı değildir**. İşlenmiş tarihî konuşma alıntısıdır; yeni üretilmiş/sentetik astronot sesi değildir.
- NASA resmî bağlam: https://www.nasa.gov/historical-sounds/ ; kullanım rehberi: https://www.nasa.gov/nasa-brand-center/images-and-media/ . Eğitim/editoryal atıf yapılır; NASA destek/onay/işbirliği ima edilmez.
- NASA resmî kısa `569462main_eagle_has_landed.mp3` ve extended `590333main_ringtone_eagleHasLanded_extended.mp3` bağlantıları araştırıldı; **bu dosyalar indirilmedi**. Edindiğimiz dosya yukarıdaki belgeli mirror kopyasıdır; resmî kısa dosyayla bayt eşitliği iddia edilmez.

### İçerik ve kullanım kapısı

- Yayıncının `src/game/voice.ts` caption eşlemesi: **“TRANQUILITY BASE HERE. THE EAGLE HAS LANDED. — ROGER, TRANQUILITY, WE COPY YOU ON THE GROUND.”** https://github.com/seankd3/orbital-mechanics/blob/main/src/game/voice.ts
- Caption, bağımsız dinleme veya bizim ASR sonucumuz değildir. İniş konuşmasının olay/rol bağlamı araştırmadaki ALSJ birincil transkriptiyle uyumludur; **dosyanın son içerik/kesit incelemesi henüz bekliyor**. Duyulmayan ek sözcük veya yanıt duyulmuş gibi yazılmayacak.
- Planlanan yer s15: Türkçe anlatım biter, kısa boşluk, özgün alıntı **normal hızında ve ayrı ses katmanında**. Anlatıcı/başka söz/foley radyo alıntısını bastırmaz. Gerçek başlangıç/bitiş ve `ek_sure` nihai yerleşimde ölçülecek.
- **GERÇEK KAYIT** etiketi yalnız alıntı süresince. Çöp adamlı görsel hep **AI TEMSİLÎ**; NASA arşiv görüntüsü diye etiketlenmez. Genel Türkçe anlatı gerçek NASA sesi gibi etiketlenmez.
- Ayrıntılı makine kaydı: `uzun/arsiv-sesleri/KAYNAK.json`. Henüz videoda kullanıldığı veya miks tamamlandığı iddia edilmez.

## 3. Modern gerçek kayıt adayları — MODERN ANALOJİ

| Depodaki dosya | Kaynak / lisans | Kullanım niyeti |
|---|---|---|
| `sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pageturn1.opus` | OwlishMedia / CC0 / https://opengameart.org/content/sound-effects-pack | Kâğıt çevirme;1969belgesel oda sesi iddiası yok |
| `sfx/free-sfx/Owlish/Sound Effects Pack/Paper/pencil-scratch-1.opus` | OwlishMedia / CC0 / aynı kaynak | Hayalî gözlemcinin defteri; modern foley |
| `sfx/free-sfx/Owlish/Sound Effects Pack/Cloth, Rustle/320137__owlstorm__blanket-movement-1.opus` | OwlishMedia / CC0 / aynı kaynak | Kumaş hareketi; modern foley |

Bu üç dosya depoda var. B030 için tamdecode/süre ve yerleşim henüz yapılmadı. NASA oda uğultusu, arşiv alkışı, motor sesi veya1202alarmı diye yeniden adlandırılmazlar. Ay dış boşluğunda mikrofonla duyulmuş motor/rüzgâr sesi iddiası yok. Sentetik bip/cızırtı sahte tarihî kayıt yerine konmaz.

## 4. Finalde doldurulacak

- Kullanılan dosyaların TAM listesi, süreleri, lisans/atıf ve gerçek yerleşim sayısı; kullanılmayan adaylar ayrılacak.
- Arşiv son içerik/kesit denetimi ve gerçek yerleşim zamanları; kayıt normal hızda/anlatı susuyor kontrolü.
- Müzik kullanılacaksa ayrı kaynak/lisans ve MODERN BESTE açıklaması.
- Final MP4 LUFS/truepeak/tamAVdecode/faststart, etiketin doğru başlangıç/bitişi ve5–12dk uyumu. Final MP4 henüz yok.
