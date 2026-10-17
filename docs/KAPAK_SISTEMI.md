# KAPAK (THUMBNAIL) SİSTEMİ — TÜM BÖLÜMLER

## İlke

Her bölümün kapağı **aynı değişmeyen şablondan** üretilir: yerleşim, renkler,
tipografi, yıl rozeti ve MERAKLI bandı hiç değişmez. Bölümden bölüme yalnızca
şunlar değişir: **arka plan sanatı**, **yıl rozeti metni** ve **iki satırlık
bölüm başlığı**. Böylece kanal sayfasında seri bütünlüğü oluşur.

## Sabit Şablon Öğeleri (asla değişmez)

| Öğe | Değer |
|---|---|
| Boyut | 1280x720 PNG |
| Yerleşim | Sanat sağa yaslı; karakter sağ üçte birde |
| Okunurluk | Soldan koyulaşan gradyan + hafif alt karartma |
| Yıl rozeti | Sol üst, kırmızı (#D93636) yuvarlatılmış kutu, beyaz kontur, Montserrat ExtraBold 42 |
| Başlık | Rozet altında 2 satır, beyaz, siyah kontur + gölge, Montserrat ExtraBold (otomatik boyut 56–104) |
| Marka bandı | Sol alt kırmızı "MERAKLI" bandı + "EĞER OLSAYDIM SERİSİ" alt yazısı |
| Renk dili | Fular kırmızısı vurgu + beyaz/siyah tipografi |

## Üretim Komutu

```bash
python3 araclar/kapak_yap.py kapaklar/sanat/bolum-XXX.png \
  "EĞER [YIL]'TE OLSAYDIM" "BAŞLIK SATIRI 1" "BAŞLIK SATIRI 2" kapaklar/bolum-XXX.png
```

Sanat üretim kuralı: `karakter/merakli-referans.png` referansı ile, **yatay
16:9**, karakter sağ üçte birde, sol üçte ikisi sakin (metin alanı), metinsiz.

## Bölüm Başlık Eşlemesi (56 bölüm)

| Bölüm | Yıl rozeti | Başlık (satır 1 / satır 2) | Kapak sanatı fikri | Durum |
|---|---|---|---|---|
| 001 | EĞER 1453'TE OLSAYDIM | FETİH ORDUSUNDA / BİR İZCİ | Alacakaranlıkta surlar önünde izci | ✅ |
| 002 | EĞER 1453'TE OLSAYDIM | ŞAHİ TOPUNUN / USTASI OLSAM | Meraklı + dev Şahi topu | ✅ |
| 003 | EĞER 1453'TE OLSAYDIM | FIRTINADA / BİR DENİCİ | Gece fırtınasında kadırga güvertesi | ✅ |
| 004 | EĞER 1453'TE OLSAYDIM | SURLARDA SON / NÖBETÇİ | Bizans nöbetçi, gelen ordu | ✅ |
| 005 | EĞER 1071'DE OLSAYDIM | MALAZGİRT'TE / HABERCİ | Atlı haberci, altın ova | ✅ |
| 006 | EĞER 1347'DE OLSAYDIM | KARA VEBA / ŞEHRİNDE | Karanlık sokak, işaretli kapılar | ⬜ |
| 007 | EĞER 79'DA OLSAYDIM | POMPEII'DE / KAÇABİLİR MİYİM? | Vezüv patlaması, kül yağmuru | ⬜ |
| 008 | EĞER 79'DA OLSAYDIM | HERCULANEUM'DA / SON 30 DAKİKA | Gelen püroklastik bulut | ⬜ |
| 009 | EĞER 1883'TE OLSAYDIM | KRAKATOA / PATLAMASI | Denizden dev patlama | ⬜ |
| 010 | EĞER ANTİK ÇAĞ'DA OLSAYDIM | DEPREM ANINDA / ANTİK ŞEHİR | Yıkılan sütunlar, toz bulutu | ⬜ |
| 011 | EĞER O GÜN OLSAYDIM | BÜYÜK ŞEHİR / YANGININDA | Alevler arasındaki sokak | ⬜ |
| 012 | EĞER 1666'DA OLSAYDIM | LONDRA'NIN / BÜYÜK YANGINI | Alevler içinde katedral | ⬜ |
| 013 | EĞER 80'DE OLSAYDIM | ARENAYA ÇIKAN / GLADYATÖR | Kolezyum kumu, ilk bakış | ⬜ |
| 014 | EĞER MÖ 2560'TA OLSAYDIM | PİRAMİT / İŞÇİSİ | Giza rampası, kireç blokları | ⬜ |
| 015 | EĞER MÖ 776'DA OLSAYDIM | İLK / OLİMPİYAT | Stadyum pisti, başlama çizgisi | ⬜ |
| 016 | EĞER MÖ 149'DA OLSAYDIM | KARTACA / KUŞATMASINDA | Yıkımdan önceki son gün | ⬜ |
| 017 | EĞER MS 120'DE OLSAYDIM | LEJYONER / KARAKOLDA | Sınır kalesi, rutin devriye | ⬜ |
| 018 | EĞER MÖ 399'DA OLSAYDIM | SOKRATES'İN / DURUŞMASI | Agora, mahkeme halkası | ⬜ |
| 019 | EĞER ANTİK ÇAĞ'DA OLSAYDIM | TİYATRONUN / SAHNE ARKASI | Maskeler, son hazırlık | ⬜ |
| 020 | EĞER O GÜN OLSAYDIM | İSKENDERİYE / KÜTÜPHANESİNDE | Tomarlar ve tehlike | ⬜ |
| 021 | EĞER MÖ 334'TE OLSAYDIM | İSKENDER'İN / HARİTACISI | Pergament haritası, ordu kampı | ⬜ |
| 022 | EĞER O GÜN OLSAYDIM | TAÇ GİYME / TÖRENİNDE | Saltanat salonu, taç | ⬜ |
| 023 | EĞER O GECE OLSAYDIM | TRUVA ATI / SOKAĞINDA | Atın şehre girişi, kalabalık | ⬜ |
| 024 | EĞER 793'TE OLSAYDIM | VİKİNG / BASKININDA | Kıyıya yanaşan drakkar | ⬜ |
| 025 | EĞER ORTA ÇAĞ'DA OLSAYDIM | KALE / KUŞATMASINDA | Mancınıklar, uçan taşlar | ⬜ |
| 026 | EĞER ORTA ÇAĞ'DA OLSAYDIM | CADILIK / SUÇLAMASIYLA | Karanlık mahkeme, zincirler | ⬜ |
| 027 | EĞER ORTA ÇAĞ'DA OLSAYDIM | ŞÖVALYE / TURNUVASINDA | Mızrak düellosu, tribün | ⬜ |
| 028 | EĞER O GECE OLSAYDIM | ÇİN SEDDİ'NDE / NÖBETÇİ | Duvar, duman sinyal kulesi | ⬜ |
| 029 | EĞER ORTA ÇAĞ'DA OLSAYDIM | PANAYIRDA / TÜCCAR | Renkli tezgâhlar, kalabalık | ⬜ |
| 030 | EĞER ORTA ÇAĞ'DA OLSAYDIM | MANASTIRDA / KEŞİŞ | Yazma odayı, mürekkep | ⬜ |
| 031 | EĞER ORTA ÇAĞ'DA OLSAYDIM | KALEDE / AŞÇI | Dev kazanlar, buhar | ⬜ |
| 032 | EĞER ORTA ÇAĞ'DA OLSAYDIM | KALEYE SIZAN / CASUS | Gece, halat, gölgeler | ⬜ |
| 033 | EĞER O GECE OLSAYDIM | SAMURAY: / KALE SAVUNMASI | Japon kalesi, yağmur | ⬜ |
| 034 | EĞER O YIL OLSAYDIM | NIL TAŞKININDA / ÇİFTÇİ | Yükselen sular, sandal | ⬜ |
| 035 | EĞER 1519'DA OLSAYDIM | AZTEK / BAŞKENTİNDE | Kanallar üzerinde şehir, piramit | ⬜ |
| 036 | EĞER O GÜN OLSAYDIM | İNKA YOLUNDA / BİR ULAK | And dağ yolu, koşan ulak | ⬜ |
| 037 | EĞER O GECE OLSAYDIM | KERVANSARAYDA / BİR GECE | Avlu, ateş başı diller | ⬜ |
| 038 | EĞER O GÜN OLSAYDIM | İPEK YOLU'NDA / KERVAN | Develer, çöl ufkunda karakol | ⬜ |
| 039 | EĞER 1830'DA OLSAYDIM | İLK TREN / YOLCULUĞU | Buharlı lokomotif, kömür dumanı | ⬜ |
| 040 | EĞER 1886'DA OLSAYDIM | SOKAKTA İLK / OTOMOBİLLER | Atlı arabalarla karışık trafik | ⬜ |
| 041 | EĞER 1783'TE OLSAYDIM | İLK BALONDA / YÜKSELDİM | Paris çatıları üzerinde balon | ⬜ |
| 042 | EĞER 1776'DA OLSAYDIM | İLK DENİZALTI / MÜRETTEBATI | Su altı gövdesi, mum ışığı | ⬜ |
| 043 | EĞER 1839'DA OLSAYDIM | İLK FOTOĞRAFIN / ÇIRAĞI | Stüdyo, kimyasal banyo | ⬜ |
| 044 | EĞER 1903'TE OLSAYDIM | İLK UÇUŞA / TANIK OLDUM | Kitty Hawk kum tepeleri | ⬜ |
| 045 | EĞER 1969'DA OLSAYDIM | APOLLO 11 / KONTROL ODASI | Yıldız dolu ekranlar, gerilim | ⬜ |
| 046 | EĞER 1912'DE OLSAYDIM | TİTANİC'İN / SON GECESİ | Buzdağı, güverte kalabalığı | ⬜ |
| 047 | EĞER 1911'DE OLSAYDIM | KUTUPTA / KIZAKÇIYDIM | Beyaz sonsuzluk, köpek takımı | ⬜ |
| 048 | EĞER O GÜN OLSAYDIM | BİLİNMEYEN / ADADA | Tropik kıyı, sisli iç kesim | ⬜ |
| 049 | EĞER 985'TE OLSAYDIM | GRÖNLAND'A / DOĞRU | Buz denizinde viking gemisi | ⬜ |
| 050 | EĞER O GECE OLSAYDIM | KORSAN GEMİSİNDE / İSYAN | Güverte isyanı, kılıçlar | ⬜ |
| 051 | EĞER 1450'DE OLSAYDIM | İLK MATBAADA / ÇIRAĞIM | Gutenberg presi, harf kalıpları | ⬜ |
| 052 | EĞER ORTA ÇAĞ'DA OLSAYDIM | SAAT KULESİNİN / ÇIRAĞI | Dev dişliler, kule içi | ⬜ |
| 053 | EĞER 1789'DA OLSAYDIM | DEVRİMDE / FIRINCI ÇIRAĞI | Barikatlar, ekmek kuyruğu | ⬜ |
| 054 | EĞER 1915'TE OLSAYDIM | SİPERLERDE / BİR GÜN | Çamur, tel örgüler, sis | ⬜ |
| 055 | EĞER 1922'DE OLSAYDIM | TUTANKHAMUN'UN / MEZARINDA | Altın lahit, mezar odası | ⬜ |
| 056 | (yedek konu) | — | — | ⬜ |

Not: Ek çekimler sonrası ayrıntılı tarih düzeltmesi yapılır (örn. 016 → MÖ 149,
017 → MS 122 vb. bölüm araştırmasında netleştirilir). Rozetlerdeki Türkçe
ek uyumu (–de/–da/–te/–ta) bölüm araştırması sırasında son kez kontrol edilir.

## Kalite Kontrol

- Kapak üretildikten sonra piksel kontrolü: rozet ve MERAKLI bandı tüm
  kapaklarda **birebir aynı** olmalı (şablon testi bu yüzden piksel sayısını
  karşılaştırır: rozet 30.389 px, bant 7.998 px).
- Başlık en fazla 2 satır, satır başına ~18 karakter hedefi.
- Kapak, video içeriğinin ilk sahnesiyle ton uyumunda olmalı.
