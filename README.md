# Cop-adam

Bu repoda **what-if-studio** var: tek satır konudan 15–25 saniyelik animasyon bölüm üreten bir Remotion stüdyosu
(her kare SVG olarak kodla çizilir, ses kodla üretilir). Kurulu ve çalışır durumda: üç bölüm render edilmiş, hikâye
panoları hazır.

Başlamak için: [`what-if-studio/README-STUDIO.md`](what-if-studio/README-STUDIO.md)

```bash
cd what-if-studio
npm run studio     # → http://localhost:3430   Remotion Studio (kompozisyonlar, kare kare)
npm run lab        # → http://localhost:3440   Ses Laboratuvarı (canlı miks)
npm run ready      # her şeyi tazele: ses + render + panolar
```

Hazır dosyalar: `what-if-studio/demo/` — `rewind.mp4`, `copy-paste.mp4`, `ses-testi.mp4` ve üç pano.

| Belge | Ne |
|---|---|
| `what-if-studio/README-STUDIO.md` | ne hazır, nasıl açılır, kendi üretimini nasıl yaparsın |
| `what-if-studio/REMOTION.md` | Remotion komutları: still / render / comps, bayraklar, sorun giderme |
| `what-if-studio/RENDER-OFFLINE.md` | Chrome'suz makinede render kurulumu (elle yol) |
| `what-if-studio/lab/README.md` | ses laboratuvarı ve lab → dosya turu |
