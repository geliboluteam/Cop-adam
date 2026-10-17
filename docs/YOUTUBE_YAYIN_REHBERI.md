# YOUTUBE YAYIN REHBERİ (SHORTS)

## Teknik Gereksinimler

- Dosya: 1080x1920 (9:16), MP4 (H.264 + AAC), 30 fps, ≤ 60 sn
- Ses: -14 LUFS hedefli miks (betik zaten `loudnorm` uygular)
- Yüklemede başlık/açıklama/etiketler `bolumler/NNN-*/YAYIN.md` dosyasından
  kopyalanır.

## Başlık Şablonları (A/B test edilebilir)

1. `EĞER 1453'TE OLSAYDIM 😱 #shorts #tarih`
2. `İstanbul'un Fethinde İZCİ Olsaydım Neler Yazardım? | 1453`
3. `Fatih'in Ordusunda Bir İzci: 53 Günün Hikâyesi #1453`
- Kural: **"EĞER [YIL]"** kalıbı + duygusal/emotion kelime + yıl. ≤ 60 karakter.

## Açıklama İskeleti

```
[YILDIZLI HOOK - 1-2 cümle, görünür ilk satır]

Bu videoda: [1 cümle içerik özeti].

⚠️ DÜRÜST TARİH NOTU: [efsane/kaynak notu; örn. Ulubatlı Hasan için]

🔊 SES KÜNYESİ — bu videodaki ses efektleri gerçek kayıtlardır; tarihsel
olayın çağdaş kaydı yoktur, dönem sesleri modern benzer kayıtlarla
(analojiyle) temsil edilmiştir:
• [efekt] — [sanatçı/kaynak], [lisans], [URL]
• ...
 Müzik: [parça] — [besteci/kaynak], [lisans], [URL]

🎨 Görseller ve seslendirme yapay zekâ ile üretilmiştir. Karakter ve senaryo
özgündür.

#tarih #1453 #istanbul #shorts #keşfet #[dönem etiketi]

Sıradaki bölümü sen seç: yorumlara tarih+yer yaz!
```

## Etiket Havuzu (örnek bölüm 01)

tarih, istanbulun fethi, 1453, fatih sultan mehmet, osmanlı, tarihte bugün,
keşfet, shorts, eğlence, eğitim, animasyon, çöp adam, eğer olsaydım,
what if, history shorts, ottoman empire, constantinople

## Shorts Yükleme Kontrol Listesi

- [ ] Video 9:16 ve ≤ 60 sn
- [ ] Altyazı yok (Bölüm 04+; ekran temiz) — sessiz izleyici için YouTube otomatik altyazıyı (CC) etkinleştir
- [ ] İlk 2 saniyede kanca görünüyor mu?
- [ ] Başlıkta yıl + anahtar kelime var mı?
- [ ] Açıklamada SES KÜNYESİ tam mı?
- [ ] Kanal markası (fular) kapak karesinde görünür mü?
- [ ] Sabit yorum: "Sıradaki durak neresi? 👇" (ilk yorumu kendimiz atarız)
- [ ] Çalma listesi: "EĞER OLSAYDIM — TÜM BÖLÜMLER"

## KAPANIŞ KARTI STANDARDI (2026-10-17'den itibaren — kalıcı)

Her videonun kapanış kartı ÜÇ satırdır ve kademeli olarak belirir:

1. **"SIRADA NERE?"** — büyük beyaz (Kapanis stili)
2. **"YORUMLARA YAZ"** — mavi vurgu (KapanisAlt stili)
3. **"KANALIMA ABONE OLMAYI UNUTMAYIN!"** — kanal kırmızısı (Abone stili)

- `video_yap.py` içinde varsayılan olarak AÇIKTIR; planda
  `kapanis_karti.abone = ""` yazılarak tek video için kapatılabilir.
- Satırlar PIL ile ölçülüp garantili %4.5H boşlukla istiflenir —
  üst üste binme olamaz (kart istif düzeltmesi ile aynı sistem).
