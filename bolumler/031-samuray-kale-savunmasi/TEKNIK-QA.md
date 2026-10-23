# B031 — Teknik QA

23 Ekim 2026. **Sonuç: PASS.**

- Video: `uzun/merakli-031-uzun-samuray-kale-savunmasi.mp4` — 11:18 (678,2 sn), 1920×1080, 30 fps, 36296805 bayt, SHA-256 `8f976d025ae79a26a553d5d5ae1afd6c72a03a675c2fa400f77841e6a7e19d52`.
- Tam AV decode PASS; faststart (moov önde) PASS. Ses: -14.01 LUFS, -1.26 dBTP, LRA 4.0.
- 20 sahne / 25 görsel / 20 anlatım; çift sahneler s04,s08,s12,s15,s19 sahne ortasında ikinci görsele geçer, süre/senkron değişmez (`ZAMAN-CIZELGESI.json`).
- Anlatım hızı 1,18x; üst üste binen anlatım yok (render assert). Altyazı yok; yalnız tarih bandı + "ÇİZİM: AI TEMSİLÎ" etiketi.
- 4 ayrı kart: giriş / tarih / kapanış / abone (`uzun/kartlar/`). Açılan QA kareleri: giriş, s01, s04b, s19b, kapanış, abone — yazı/yüz çakışması yok.
- Görsel anatomi: 25/25 PASS (her figür 2 kol, 2 ayrı el, 2 bacak, 2 ayak). Reddedilip yenilenenler: s02 (×2), s04b, s10 (×2), s12b (×2), s17; gerekçeler QA-GRUP1/2/3 dosyalarında. s04b kompoziti tamamen kaldırıldı.
- Kapsam notu: Tam decode ve kare incelemesi teknik kontroldür; bağımsız insan dinlemesi/kelime kelime ASR yapılmadı.
