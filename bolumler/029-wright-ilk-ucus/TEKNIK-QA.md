# B029 — Final teknik ve görsel QA

**PASS.** Ölçümler final MP4 üzerinden alındı; 10 kritik final kare ayrıca görsel olarak incelendi.

- Dosya `uzun/merakli-029-uzun-wright-ilk-ucus.mp4`.
- Süre **683.67 sn (11:24)**, boyut **53,563,827 bayt**, 100MB GitHub sınırının altında.
- 1920×1080, 30fps, H.264/yuv420p; AAC48kHz stereo.
- `moov` atomu `mdat` önünde: faststart PASS.
- Baştan sona video ve ses FFmpeg decode: çıkış0, hata çıktısı boş.
- Final ses **-14.07 LUFS / -1.40 dBTP / LRA 3.20 LU**. Teknik ölçüm, baştan sona insan gibi dinleme iddiası değil.
- 20 voice-03/tr MP3 ham toplam727,224sn; bütün kaynak MP3ler de tam decode PASS. Sessizlik düzenleme694,85sn; anlatım **×1,031**, miks683,50sn.
- 20 sahne / 25 görsel; çiftler04/08/12/15/19 sahne ortasında, süre/senkron değişmeden. Caption katmanı yok, altyazıfalse.
- 20 tarih bandı, ayrı giriş/kapanış/abone stilleri. Tüm tarih metinleri40px fontla1840px güvenli alan içinde ölçüldü.
- Son abone **KANALIMA ABONE OLMAYI UNUTMAYIN!** yaklaşık **5.68sn** görünür. Son sahne ek5sn kart okunabilirliği için.
- 63 efekt + müzik / 10 benzersiz kaynak: tamamı mevcut, baştan sona decode kontrolünden geçti ve kaynak/lisans tablosu var. Modern analoji etiketleri açık.
- Tüm25 görselde min3 karakter; s07 Taylor ile4, s15 Daniels ile4. İki Wright kardeş eksik değil. Meraklı'nın gerçek tanık olduğu ileri sürülmüyor.
- Her figür 2kol/2AYRI el/2bacak/2ayak kontrolünden geçti. Birleşik eller yok. s13/s15 geniş kadraj ve eller/palalar son hâlde düzeltildi.
- Final birleştirmede vignette ve gren kapalı; temiz kaynak çizim korunur. İki filtre threadiyle mevcut5sahnegrubu yeniden birleştirildi; anlatım/süre/geçişler değişmedi. Eski bölümlerin vignette/gren varsayılanları korundu.
- Kamera hareketi zoom0,015/pan6px: çok figürlü kadrajı korur. Renderer eski varsayılan0,11/40px korunmuştur; diğer bölümler etkilenmez.
- Kapak1280×720v4, büyük **12 SANİYE! / İLK UÇUŞ**, kırmızı **1903 · WRIGHT**. Üç kanonik beyaz çöp adam, kırmızı fular yalnız Meraklı. Metin yüzlere/ellere taşmıyor. Gerçekçi yan figürlü aday reddedildi; finalde kullanılmadı.

## Kritik final kareler
| Kare | Zaman(sn) | Sonuç |
|---|---:|---|
| 01-giris | 1.50 | PASS |
| 07-taylor-motor | 223.35 | PASS |
| 12b-hava-yer-hizi | 403.53 | PASS |
| 13-orville-hazirlik | 430.51 | PASS |
| 14-orville-ilk-ucus | 461.21 | PASS |
| 15-daniels-fotograf | 487.26 | PASS |
| 16-wilbur-dorduncu | 529.11 | PASS |
| 17-yerde-hasar | 560.73 | PASS |
| 19b-temsil-belge | 638.39 | PASS |
| 20-kapanis-abone | 682.67 | PASS |

## Tarih / kurgu / görsel kilitleri
- Ana yer Kill Devil Hills, Kitty Hawk yakınları. 14Aralık başarısızlık ve17Aralık dört uçuş ayrı tarih bandıyla.
- İlk uçuş Orville/gri pantolon:12sn/120feet≈37m. Dördüncü Wilbur/kahverengi:59sn/852feet≈260m. Pilotlar yer değiştirdi; tek uçuşmuş gibi birleştirilmedi.
- 1901 rüzgâr tüneli,1902 planör geçmişi, Taylor motor katkısı ve1904–1905 sonraki gelişmeler ayrı bağlamlarda.
- İlk olma bağlamı insan taşıyan motorlu/kontrollü/sürdürülebilir havadan ağır uçuş; önceki balon/planörler yok sayılmadı.
- Flyer ön canard, arka dikey dümen, iki iki-palalı itici pervane, kızaklar ve tek ray ile temsil edildi. Yakın mekanik görüntüler ölçülü mühendislik planı değildir; yapım/uçuş talimatı yok.
- Son hasar YERDE rüzgârla; yangın/ölüm/airborne infilak yok.
- Bütün görüntüler AI TEMSİLÎ. Çerçevedeki siyah-beyaz resimler de arşiv fotoğrafı değil. s19b yanlış minyatür uçak onaylı canard/kızak çizimiyle düzeltildi.
- Meraklı kurgu gözlemci, belgeli altıncı tanık/pilot/fotoğrafçı değil. Gerçek kişilerle gösterilen yorum sahneleri belgeli toplantı/konuşma iddiası değil.
- Gerçek1903 motor sesi iddiası yok; modern motor/jet/flaş eklenmedi. Doğa ve foley modern gerçek kayıtlardır; kaynak/lisans künyesi verildi.
- Yalnız uzun video; Shorts üretilmedi.
