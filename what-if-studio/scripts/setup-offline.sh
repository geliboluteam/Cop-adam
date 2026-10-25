#!/usr/bin/env bash
# Sets up a browser Remotion can drive, for machines that can't reach remotion.media (which is how Remotion normally
# fetches Chrome). Downloads npm's Chromium build and unpacks the shared libraries it needs into /tmp.
#
#   npm run setup:offline
#
# Nothing in the repo is changed except node_modules; the studio itself doesn't need this (the browser renders).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "→ installing @sparticuz/chromium (no-save)"
npm i --no-save --no-audit --no-fund --legacy-peer-deps @sparticuz/chromium

echo "→ unpacking the browser and its libraries into /tmp"
node --input-type=module -e "
import c from '@sparticuz/chromium';
const p = await c.executablePath();
console.log('   browser:', p);
"
node -e "
const fs = require('fs'), z = require('zlib');
for (const n of ['al2023', 'fonts', 'swiftshader']) {
  const src = 'node_modules/@sparticuz/chromium/bin/' + n + '.tar.br';
  if (!fs.existsSync(src)) continue;
  fs.writeFileSync('/tmp/' + n + '.tar', z.brotliDecompressSync(fs.readFileSync(src)));
}
"
mkdir -p /tmp/al2023x
tar xf /tmp/al2023.tar -C /tmp/al2023x

echo "→ checking it runs"
LD_LIBRARY_PATH=/tmp/al2023x/lib:/tmp/al2023x/lib64 /tmp/chromium --version

echo
echo "ready. Now:"
echo "  npm run comps                      list the compositions"
echo "  npm run still -- SesTesti out/x.png --frame=26"
echo "  npm run render -- SesTesti out/ses-testi/ses-testi.mp4"
