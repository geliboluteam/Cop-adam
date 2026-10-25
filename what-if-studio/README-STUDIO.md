# what-if-studio — hazır

Bu klasör çalışır durumda: bağımlılıklar kurulu, sesler üretilmiş, üç bölüm render edilmiş. Tek komut her şeyi
tazeler:

```bash
npm run ready          # kurulum + ses + render + demo/ kopyaları   (~9 dk)
npm run ready -- --no-render --boards   # sadece experiment: pano (storyboard) üret
```

## Şu an elinde ne var

| Dosya | Ne | Süre / boyut |
|---|---|---|
| `demo/rewind.mp4` | **Rewind** — "What if you could rewind 10 seconds?" (kanıt bölümü: çekimler tersine oynuyor) | 18,7 s · 16 MB |
| `demo/copy-paste.mp4` | **CopyPaste** — "What if you could copy and paste anything?" | 23,1 s · 17 MB |
| `demo/ses-testi.mp4` | **SesTesti** — 6 s'lik ses testi: kareler ve ses kodla üretilmiş | 6,1 s · 4,5 MB |
| `demo/rewind-storyboard.png` | 12 çekimlik pano | 1992×948 |
| `demo/copy-paste-storyboard.png` | 15 çekimlik pano | 1992×1256 |
| `demo/ses-testi-storyboard.png` | 3 çekimlik pano | 1500×332 |

Hepsi 1920×1080, 30 fps, h264 + AAC stereo. Ham çıktılar `out/<slug>/` altında (git dışı).

## Açmak (tarayıcı, Chrome indirmesi gerekmez)

```bash
npm run studio      # → http://localhost:3430   Remotion Studio: kompozisyonlar, kare kare, sesli önizleme
npm run lab         # → http://localhost:3440   Ses Laboratuvarı: animasyon + canlı miks, efekt pedleri
```

Studio'da sol listede: `Rewind`, `RewindBoard`, `CopyPaste`, `CopyPasteBoard`, `SesTesti`, `SesTestiBoard`, `Cast`.
`Cast` kadro sayfasıdır — kostümleri yan yana görürsün.

## Kendi üretimini yapmak

```bash
npm run audio -- ses-testi                    # sesi yeniden üret (audio.json'daki mix'e göre)
npm run still -- SesTesti out/x.png --frame=26  # tek kare
npm run render -- Rewind out/rewind.mp4         # video
npm run comps                                   # kompozisyon listesi + süreler
npm run typecheck                               # tip kontrolü
```

Ses ayarı labda bulunur: lab → "Dosyaya yaz" → `src/episodes/ses-testi/audio.json` içindeki `mix` bloğuna yapıştır →
`npm run audio` → `npm run render`. Ayrıntılı komut rehberi: **`REMOTION.md`**.

## Nerede ne var

```
src/episodes/<slug>/     bölümün kendisi (episode.json, shots.tsx, index.tsx, timeline.json, audio.json)
src/engine/              rig, mekânlar (study/stairwell/classroom/rooftop/kitchen/schematic), ışık, UI
src/Root.tsx             kompozisyon kaydı
public/<slug>/           voice/sfx/music (ses)
public/fonts/            üç yazı tipi (çevrimdışı render için)
lab/                     Ses Laboratuvarı (Vite + Web Audio)
scripts/                 gen-audio.py, ready.sh, remotion-offline.sh, setup-offline.sh, sheet.py
demo/                    teslim edilen dosyalar
```

## Bu makineye özgü iki not

- **Render için Chrome**: normalde Remotion kendi Chrome'unu indirir; burada `remotion.media` kapalı. `npm run
  setup:offline` bir kez `/tmp/chromium`'ı kurar, `npm run render` onu kullanır. `/tmp` silinirse tekrar çalıştır.
- **Yazı tipleri**: Google Fonts kapalı olduğu için `public/fonts/`'tan yükleniyor (`src/studio.config.ts` →
  `localFonts: true`). İnternetli bir makinede `false` yaparsan aynı üç fontu Google'dan çeker.
- **Ses**: `ses-testi` dışındaki iki bölümün sesi pakette hazır geliyor (ElevenLabs, örnek dosyalar). Yeni ses üretmek
  için `ELEVENLABS_API_KEY` gerekir; `ses-testi` ise anahtarsız, kodla üretiliyor.
