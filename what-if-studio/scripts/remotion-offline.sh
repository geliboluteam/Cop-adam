#!/usr/bin/env bash
# Runs any Remotion CLI command on a machine where Remotion can't fetch its own Chrome.
#
#   npm run comps | still | render   (they all come through here)
#   bash scripts/remotion-offline.sh compositions src/index.ts
#   bash scripts/remotion-offline.sh still src/index.ts SesTesti out/x.png --frame=26
#
# It does two things: points Remotion at the browser npm gave us, and puts that browser's shared libraries on the
# loader path. Everything else (entry point, composition, flags) is passed straight through.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIB=/tmp/al2023x/lib
BROWSER="${REMOTION_BROWSER:-/tmp/chromium}"

if [ ! -x "$BROWSER" ] || [ ! -d "$LIB" ]; then
  echo "remotion-offline: no usable browser at $BROWSER (or $LIB is missing)." >&2
  echo "                  run: npm run setup:offline" >&2
  exit 1
fi

export LD_LIBRARY_PATH="$LIB:/tmp/al2023x/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
cd "$ROOT"
exec npx remotion "$@" --browser-executable="$BROWSER"
