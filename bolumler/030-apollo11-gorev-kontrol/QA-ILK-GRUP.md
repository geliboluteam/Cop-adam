# B030 — İlk üretim grubu QA / 22 Ekim 2026

> TARİHÎ ARA KAYIT: Bu dosya ilk grubun o andaki sonucudur. s04bsonra düzeltildi; güncel durum `QA-IKINCI-GRUP.md` ve `URETIM-DURUMU.json` içinde.

**Ara durum: 8 görsel dosyası / 7 PASS / 1 DÜZELTME; 10 anlatım hazır. Final video değildir.**

## Onay ve kapsam
- Kullanıcı s01kıyafetini **Devam** diyerek onayladı. Krem gömlek/petrol-mavi yelek/antrasit pantolon/beyaz el-ayak/kablolu kulaklık/kırmızı fular kimliği korunuyor.
- Yalnız uzun video; hedef20sahne/25görsel. Çiftler04/08/12/15/19, sahne ortasında. Shorts yok.
- Bu tur10görsel çağrısı:7yeni sahne dosyası +3AIdüzeltme. Önceki s01ile8PNG. İki yerel kompozit/maske düzeltmesi ayrıca yapıldı.
- **17görsel henüz yok**; bunlara ek olarak s04bdüzeltmesi var. Son10anlatım henüz üretilmedi. Kıyafet onayı tekrar beklenmiyor.

## Görsel denetim
| Dosya | Kişi | Sonuç | Ayrı el / ayak ve dönem kontrolü |
|---|---:|---|---|
| s01 |4| PASS + kullanıcı kostüm onayı | Bütün figürler tam boy, tüm eller/ayaklar ayrı; kanonik kimlik |
| s02 |4| PASS | Konsol arkasında kalan ilk figürler yeniden açık koridora alındı; tüm2kol/2ayrıel/2bacak/2ayak |
| s03 |4| PASS — kompozit | İlk model/masa uzuvları örtüyordu. Onaylı s01tabanında şematik iki araç modeli uzuvların dışında sağ açık alana yerleştirildi |
| s04 |4| PASS | Üççeyrek Meraklı yüzü; bir yan figür panoya arkası dönük, ama tüm2kol/2ayrıel/2bacak/2ayak görünür |
| **s04b** |4| **FAIL / DÜZELTME** | **Krem figürün sağ eli ile gri figürün sol eli örtüşüyor. Kol sayısı doğru olması yeterli değil. Ayrı el kontrolü başarısız; PASS sayısına katılmadı** |
| s05 |4| PASS | İlk kesik ayaklar ve beşli kompozisyon yeniden kuruldu; geniş kapı/koridorda4tam boy figür, boş/ayrı eller |
| s06 |4| PASS | CAPCOM/direktör/guidance rol temsilleri; tümeller ve ayaklar açık, modern ekran/canlı iniş filmi yok |
| s07 |4| PASS — yerel baş oranı düzeltmesi | Baş maskeyle büyütülerek kanonik oran güçlendirildi. Bir el boş kâğıt tutuyor, diğer beyaz el kalçada kapalı ama ayrı görünür. Uzuvlar tam; önceden prova bağlamı |

- Her dosya ayrı ayrı `read_file` ile incelendi; s04belleri büyütülmüş ayrıntıda ayrıca incelendi. Sadece otomatik dosya sayımıyla anatomi PASS verilmedi.
- Bütün8PNG1920×1080; ham1376×768çıktılar kenarlardan çok küçük merkez kırpma ile16:9normalleştirildi. Figürlerin ayakları kesilmedi. PNGdecode/okuma denetimi yapılır; s04bdePNGteknik sağlamlığı görselPASSanlamına gelmez.
- s03kendi çizdiğimiz temsili araç modelleri: Eagle'ın açısal üst gövdesi/altın inişkatı/dört ayak-pabuç ve ayrı konik komuta+kısa silindirik hizmetmodülü. Fiziksel ölçülü rekonstrüksiyon değil. Kompozit üretim kaynağı `uzun/kompozit-kaynaklari/s03_modeller.py`; kaynak tabanı s01. NASAarşiv fotoğrafı veya NASAüretimi çizim değil.
- Yan figürler de beyaz çöp adam, muted dönem kıyafetli; kırmızı fular yalnız Meraklı. Gerçekçi insan, ten rengi gövde, siyah uzuv/bot, modern laptop/LED/NASAlogoları yok.
- İniş öncesi ekranlar yalnız temsili çizgisel yörünge/veri panoları. s04bşeması bağımsız kâğıt levha, canlı Ay görüntüsü değil. s07prova odası gerçek iniş arızası diye etiketlenmeyecek.

## Anlatım teknik ölçümü
- **s01–s10: voice-03 / Türkçe**, aynı seçilmiş anlatıcı.10/10MP3baştan sona FFmpegdecode: çıkış0, hata çıktısı boş.
- Ham toplam **374,928sn**. Sessizlik düzenleme ve1×hız sonrası **357,57sn**.
- Bu yalnız ilk10sesin ölçümü; final video süresi veya final anlatım hızı değildir. Kalan sesler ve arşiv kesiti ölçülmeden5–12dkuyumu ilan edilmedi.
- `ANLATIM-SURE-OLCUMU.json`: her dosyanın süre, SHA256, kaynak metin SHA256 ve decode sonucu. İşlenmiş ölçümWAVları geçici, final miks değil.
- s05metnindeki dilbilgisi 'ölçümlerin güvenilirliği üzerine çalışanları' olarak düzeltildi; plan ve anlatım aynı metni kullanıyor.
- Bu kontrol sesin teknik çözülmesi ve kaynak metnin eşleşmesine ilişkindir; insan gibi baştan sona dinleme/bağımsızASRiddiası değildir.

## Henüz yapılmayanlar / sonraki kapı
1. **Önce s04bellerini birbirinden ayırarak düzelt.** Her figürde kol ve el sayısını ayrı say; kenetli/üst üste elleri geçirme.
2. s08/s08b/s09...17eksik yeni görsel, her birinde4+kanonik beyaz figür ve tam görünür uzuvlar.
3. s11–s20anlatımlarını aynıvoice-03ile üret; mevcut ilk10sesi tekrar üretme.
4. NASAgerçek radyo alıntısı henüz edinilmedi/doğrulanmadı. Kaynaklar araştırma veSFXtaslağında. Sesin sonradan edinilmiş/gerçekten çalınmış olduğunu şu aşamada iddia etme.
5. Finalde Türkçe anlatıcı susarken gerçek alıntı normalhızda; GERÇEKKAYITetiketi yalnız alıntı aralığı. Tüm çizimlerTEMSİLÎ. Kaynak/lisans ve dönüşümler açıkça yazılacak.
6. Giriş/kapanış kartlarını yüzlere taşmadan konumlandır; s19b24Temmuzbandı ve s15kayıt-aralığı bandı mevcut renderer'da henüz uygulanmadı, taslak gereksinim olarak kayıtlı.
7. Tüm25görselPASS/20ses ve arşiv/SFXtamam olmadan render yok. Video/kapakv4/finalYAYIN/TEKNIK-QAhenüz yok.
