#!/usr/bin/env bash
# Gets the studio ready to use, end to end: dependencies, the offline browser, the synthesised audio, and a render of
# every episode into out/ (with a copy in demo/ to hand over).
#
#   npm run ready                 everything
#   npm run ready -- --no-render  only setup + audio (fast)
#   npm run ready -- --boards     also write a still per shot into out/<slug>/board/
#   npm run ready -- --episodes rewind,ses-testi
#
# Safe to run twice: each step is skipped if it is already done.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

RENDER=1
BOARDS=0
ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --no-render) RENDER=0 ;;
    --boards) BOARDS=1 ;;
    --episodes) ONLY="$2"; shift ;;
    *) echo "ready: unknown flag $1" >&2; exit 2 ;;
  esac
  shift
done

say() { printf '\n\033[1;33m▸ %s\033[0m\n' "$1"; }

# 1. dependencies
if [ ! -d node_modules/remotion ] || [ ! -d node_modules/vite ]; then
  say "dependencies"
  npm install --no-audit --no-fund
else
  say "dependencies: already installed"
fi

# 2. a browser for the CLI (the browser preview doesn't need one)
if [ -x /tmp/chromium ] && [ -d /tmp/al2023x/lib ]; then
  say "browser: /tmp/chromium already unpacked"
else
  say "browser: unpacking (one time)"
  bash scripts/setup-offline.sh
fi

# 3. synthesised audio: any episode with an audio.json regenerates its three stems
say "audio"
for cfg in src/episodes/*/audio.json; do
  [ -e "$cfg" ] || continue
  slug="$(basename "$(dirname "$cfg")")"
  python3 scripts/gen-audio.py "$slug" | sed 's/^/  /'
done

# 4. render and boards
# which episodes: any folder with a timeline.json (its composition id comes from its index.tsx)
slugs=""
for dir in src/episodes/*/; do
  s="$(basename "$dir")"
  [ -e "$dir/timeline.json" ] || continue
  slugs="$slugs $s"
done
if [ -n "$ONLY" ]; then
  slugs=" $(echo "$ONLY" | tr ',' ' ')"
fi

if [ "$RENDER" = 1 ] || [ "$BOARDS" = 1 ]; then
  say "typecheck"
  npx tsc --noEmit && echo "  clean"
fi

for s in $slugs; do
  comp="$(grep -o "defineEpisode('[A-Za-z]*'" "src/episodes/$s/index.tsx" | sed "s/defineEpisode('//;s/'//")"
  if [ -z "$comp" ]; then
    echo "  $s: could not read its composition id, skipped"
    continue
  fi
  mkdir -p "out/$s" demo

  if [ "$RENDER" = 1 ]; then
    say "render $comp -> out/$s/$s.mp4"
    bash scripts/remotion-offline.sh render src/index.ts "$comp" "out/$s/$s.mp4" --log=error
    cp "out/$s/$s.mp4" "demo/$s.mp4"
  fi

  if [ "$BOARDS" = 1 ]; then
    n="$(node -e "const t=require('./src/episodes/$s/timeline.json');console.log(t.shots.length)")"
    say "board $comp ($n stills)"
    mkdir -p "out/$s/board"
    rm -f "out/$s/board"/*.png
    for i in $(seq 0 $((n - 1))); do
      id="$(node -e "const t=require('./src/episodes/$s/timeline.json');console.log(t.shots[$i].id)")"
      bash scripts/remotion-offline.sh still src/index.ts "${comp}Board" "out/$s/board/$id.png" --frame="$i" --scale=0.5 --log=error >/dev/null
      printf '  %s' "$id"
    done
    printf '\n'
    python3 scripts/sheet.py "out/$s/board" -o "out/$s/storyboard.png" --cols 4 --width 440 --labels | sed 's/^/  /'
    cp "out/$s/storyboard.png" "demo/$s-storyboard.png"
  fi
done

say "ready"
echo "  preview   npm run studio   -> http://localhost:3430"
echo "  lab       npm run lab      -> http://localhost:3440"
echo "  renders   out/<slug>/<slug>.mp4   (copies in demo/)"
ls -lh demo/*.mp4 2>/dev/null | awk '{print "  " $9 "  " $5}'
