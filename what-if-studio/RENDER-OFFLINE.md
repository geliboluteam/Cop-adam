# Rendering this studio offline (sandbox notes)

The skill assumes a normal machine: Chrome downloads itself, and Google Fonts is reachable at render time. Neither is
true in a locked-down sandbox, so the CLI render needs three things. All of them are already set up in this checkout;
this file is what it took, so it can be redone anywhere.

```bash
# 1. A browser Remotion can drive. remotion.media is unreachable, so Remotion cannot fetch its own Chrome.
#    npm's copy of Chromium works if you give it the shared libraries it ships with.
npm i --no-save @sparticuz/chromium
node --input-type=module -e "import c from '@sparticuz/chromium'; console.log(await c.executablePath())"  # -> /tmp/chromium
node -e "const fs=require('fs'),z=require('zlib');for(const n of ['al2023','fonts','swiftshader']){fs.writeFileSync('/tmp/'+n+'.tar',z.brotliDecompressSync(fs.readFileSync('node_modules/@sparticuz/chromium/bin/'+n+'.tar.br')))}"
mkdir -p /tmp/al2023x && tar xf /tmp/al2023.tar -C /tmp/al2023x

# 2. Fonts from public/ instead of Google: STUDIO.localFonts = true in src/studio.config.ts.
#    The woff2 files are in public/fonts/ (Fontsource builds of the same three OFL faces).

# 3. Render.
export LD_LIBRARY_PATH=/tmp/al2023x/lib:/tmp/al2023x/lib64
npx remotion render src/index.ts SesTesti out/ses-testi/ses-testi.mp4 --browser-executable=/tmp/chromium
```

Notes:

- `out/` is git-ignored: renders land there, and `demo/` holds the one committed clip.
- Remotion's bundled ffmpeg is minimal (no `ebur128`), so the skill's `master.py` loudness pass can't run here; the
  stems are levelled in `audio.json` instead (see `scripts/gen-audio.py`).
- The studio (`npm run studio`) never needs any of this: it renders frames and plays audio in the browser.
