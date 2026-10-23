# B032 — Görsel QA Grup 1 (s01–s09)

23 Ekim 2026, Fetih tarzı. Kullanıcı s01 tarzını onayladı; toplu üretim aynı dilde.

## PASS (7)
- s01 (onaylı), s02, s03, s05, s06, s08, s09 — 1920×1080 normalize edildi.
- s03 yakın kontrol: eller ayrı, parşömen boş/yazısız. s09 yakın kontrol: eller ayrı, yemeni, arka plan mutfak eşyası/çadır direği (tüfek değil).

## FAIL → yeniden üretim (4)
- **s04:** dikey 768×1376 geldi + kubbe silüeti. Yatay 16:9, kubbesiz yeniden.
- **s04b:** ikinci figürde de kırmızı fular. Tek fularla yeniden.
- **s07:** 6 figür (5 istendi) + iki kırmızı fular. Tam 5 figür, tek fularla yeniden.
- **s08b:** iki figür keseyi iki elle kenetli tutuyor (kullanıcı kuralı: kenetli el FAIL). Eller boş/ayrı yeniden.
