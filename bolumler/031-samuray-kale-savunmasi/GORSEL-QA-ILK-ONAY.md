# B031 — İlk kostüm/sahne kontrolü

22 Ekim 2026. **Teknik/anatomi kontrolü: PASS. Kullanıcı stil/kostüm onayı: BEKLENİYOR.**

`uzun/gorseller/s01.png` hem ilk model çıktısı hem 1920×1080 RGB normalizasyonu sonrasında ayrı ayrı açılıp görüldü. Tam görüntü ölçeklendi; kadraj kırpılmadı, anatomik parça eklenmedi. Kaynak hashleri `uzun/ILK-GORSEL-KAYNAK.json` içinde.

## Her figürü ayrı kontrol

| Figür / konum | Kol | Ayrı görünen el | Bacak | Ayak | Not |
|---|---:|---:|---:|---:|---|
| Meraklı, ön sağ | 2 | 2 | 2 | 2 | Eller boş ve birbirinden uzak; kın/tutamak beyaz el diye sayılmadı; kırmızı fular yalnız onda |
| Deneyimli görevli, en sol | 2 | 2 | 2 | 2 | İki yandaki beyaz eller ayrı; kıyafetli |
| Ashigaru, soldan ikinci | 2 | 2 | 2 | 2 | Jingasa ve sade zırh; eller bel bağından ayrı |
| Ashigaru, ortada | 2 | 2 | 2 | 2 | İki beyaz el gövdeden ayrı; figürler örtüşmüyor |
| Haberci, orta sağ | 2 | 2 | 2 | 2 | İki el boş; alt bacağın koyu bölümü kumaş, beyaz ayaklar görünür |

Toplam **5 figür, 10 el, 10 ayak**. Birleşik/kenetli el veya saklı kol PASS sayılmadı. Fazla/eksik uzuv görülmedi. Başlar/miğferler ve ayaklar çerçeve içinde. Yüzler beyaz ve sade; gerçekçi insan yok. Yan figürlerde kırmızı fular yok.

## Stil ve temsil

- Kanonik yüzde küçük siyah gözler, basit burun/ağız; Meraklı'nın görünür beyaz yüzü, elleri ve alt bacak/ayakları; rolüne uygun giysi/zırh.
- Koyu kol korumaları zırh/giysidir. Yüzü örten menpō yok. Miğfer ve zırhın görünüşü/oranı kullanıcı kabulünü bekler.
- Fetih referansından ayrıntılı boyanmış tarihî çevre ve derinlik; Japon ahşap kapısı, çatıları, toprak seti ve küçük doğal taş örgüsü. İlk kare sakin/gergin bir başlangıç; kanlı çatışma değil.
- Uzaktaki kale silueti dönem çağrışımıdır; 1614 Osaka'nın birebir planı değildir. Modern müze kulesi veya kesin bir Sanada Maru rekonstrüksiyonu diye sunulmaz.
- Meraklı ve yanındaki dört kişi kurgu. Tarihî komutanların belgelenmiş bir buluşması diye etiketlenmez.
- AI TEMSİLÎ görsel. Görselin teknik PASS olması, kostümün kullanıcı tarafından onaylandığı veya tüm tarihî parçaların birebir belgelendiği anlamına gelmez.

## Onay kapısı

Kullanıcı görseli gördükten sonra onay/düzeltme verir. Bu turdaki “Devam” Apollo 11'den samuray hazırlığına geçiştir; **henüz görmediği bu yeni kostüm için önceden verilmiş onay sayılmaz.** Kalan 24 görsel, TTS ve render başlatılmadı.
