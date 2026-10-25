# Remotion: neyi, nasıl çalıştırıyorsun

İki ayrı dünya var, karıştırmamak gerekiyor:

| | Ne yapar | Chrome gerekir mi | Ne zaman |
|---|---|---|---|
| **Stüdyo** (tarayıcı) | kareleri tarayıcıda çizer, sesi çalar | hayır | tasarlarken, bakarken |
| **CLI** (`still` / `render`) | kareleri Chrome'da çizip ffmpeg ile mp4/png yazar | **evet** | dosya üretirken |

Bu sandbox'ta CLI tarafı için iki şey gerekiyor, ikisi de `scripts/remotion-offline.sh` içinde otomatik:

1. **Chrome**: Remotion kendi Chrome'unu `remotion.media`'dan indirir, o host buradan kapalı → `npm run setup:offline` npm'in Chromium'unu `/tmp/chromium`'a çıkarır.
2. **Kütüphaneler**: o Chromium sistem kütüphaneleri eksik olduğu için yanında gelen `al2023` yığınıyla çalışır → `LD_LIBRARY_PATH=/tmp/al2023x/lib`.

## Komutlar

Hepsi `what-if-studio/` içinden çalışır.

```bash
npm install                 # bir kez
npm run setup:offline       # bir kez (Chrome + kütüphaneler, sadece CLI için)
```

### Bakmak

```bash
npm run studio              # → http://localhost:3430  (Remotion Studio: kompozisyonlar, kare kare)
npm run lab                 # → http://localhost:3440  (Ses Laboratuvarı: canlı miks)
```

Stüdyoda soldaki listede ne varsa onu açıp oynatıyorsun; sağdaki panelden kare kare geziniyorsun. Ses, zaman çizelgesinde
görünür. **Bunun için Chrome indirmeye gerek yok.**

### Neyin var olduğunu görmek

```bash
npm run comps
```

Çıktısı (şu an):

```
Rewind            30      1920x1080      560 (18.67 sec)     ← tam bölüm (tersine oynayan çekimler)
RewindBoard       30      1920x1080       12 (0.40 sec)      ← storyboard: çekim başına bir kare
CopyPaste         30      1920x1080      693 (23.10 sec)
CopyPasteBoard    30      1920x1080       15 (0.50 sec)
SesTesti          30      1920x1080      180 (6.00 sec)      ← ses testi (kodla üretilen ses)
SesTestiBoard     30      1920x1080        3 (0.10 sec)
Cast                      1920x1080      Still                ← kadro sayfası (kostümleri yan yana gör)
```

### Tek kare almak (en hızlı kontrol)

```bash
npm run still -- SesTesti out/kontrol.png --frame=26
npm run still -- Cast out/cast.png                       # kadro sayfası
npm run still -- Rewind out/rew.png --frame=330 --scale=0.5
```

`--frame` o kompozisyonun kare numarası (`fps = 30`, yani kare 26 ≈ 0.87 s). Kare numarasını stüdyoda alttaki
zaman çizelgesinden okuyabilirsin.

### Video render etmek

```bash
npm run render -- SesTesti out/ses-testi/ses-testi.mp4
```

Yararlı bayraklar (hepsi `npm run render -- <kompozisyon> <çıktı> <bayrak>` biçiminde sona eklenir):

| Bayrak | Ne yapar |
|---|---|
| `--frames=0-20` | sadece o aralığı render eder (denemek için: 6 s yerine 1 s) |
| `--scale=0.5` | yarı çözünürlük (hızlı deneme) |
| `--muted` | sessiz render (sesi sonradan ekleyeceksen) |
| `--concurrency=4` | paralel kare sayısı (makine zorlanıyorsa düşür) |
| `--crf=18` | kalite (küçük sayı = daha iyi/daha büyük dosya) |
| `--log=error` | sadece hataları yazdır |

Örnek: `npm run render -- SesTesti out/deneme.mp4 --frames=110-140 --scale=0.5`

Render süresi bu makinede yaklaşık **30 kare/saniye-in** (180 karelik `SesTesti` ≈ 3 dakika). Çıktı `out/` altına gider
(git'e girmez); teslim edilecek dosya `demo/` içinde duruyor.

### Sesi yeniden üretmek

Ses bir dosya değil, kod: `src/episodes/ses-testi/audio.json` + `scripts/gen-audio.py`.

```bash
npm run audio -- ses-testi        # public/ses-testi/{voice,sfx,music}.wav yeniden yazılır
```

Sonra render. Sıra önemli: **önce ses, sonra render** — `Audio` etiketleri render sırasında bu WAV'ları okur.
Ayarı labda bulduysan: lab → "Dosyaya yaz" → `audio.json`'daki `mix` bloğuna yapıştır → `npm run audio` → `npm run render`.

### Tip kontrolü

```bash
npm run typecheck
```

Editörde dosya kaydederken zaten hata görürsün; commit öncesi bir kez çalıştırmak yeterli.

## Sorun giderme

| Hata | Sebep / çözüm |
|---|---|
| `ECONNRESET ... remotion.media` | Chrome indirilemiyor → `npm run setup:offline`, sonra `npm run render` (sarmalayıcı `--browser-executable` verir) |
| `no usable browser at /tmp/chromium` | `/tmp` temizlenmiş → `npm run setup:offline` tekrar |
| `Failed to fetch ... fonts.gstatic.com` | Google Fonts kapalı → `src/studio.config.ts` içinde `localFonts: true` olmalı (öyle) |
| `Could not find composition "X"` | adı yanlış → `npm run comps` ile tam adı al (`SesTesti`, `SesTestiBoard`…) |
| Ses yok ama video var | `public/<slug>/` altında üç WAV var mı, `timeline.json`'daki `audio` yolları doğru mu |
| Render çok yavaş | `--scale=0.5 --concurrency=4`; ya da önce `--frames` ile küçük aralık dene |

## Nerede ne var

| Yol | Ne |
|---|---|
| `src/index.ts` → `src/Root.tsx` | kompozisyon kaydı: her bölüm `Root`'ta `<Composition>` olarak tanımlanır |
| `src/episodes/<slug>/` | bölümün kendisi: `episode.json`, `shots.tsx`, `index.tsx`, `timeline.json`, `audio.json` |
| `src/engine/` | rig, mekânlar, ışık, UI — bütün çizim |
| `public/<slug>/` | voice/sfx/music WAV'ları (render bunları okur) |
| `scripts/` | `gen-audio.py` (ses), `remotion-offline.sh` (CLI sarmalayıcı), `setup-offline.sh` |
| `out/` | üretilen png/mp4 (git dışı) |
| `demo/` | teslim edilen örnek mp4 |
