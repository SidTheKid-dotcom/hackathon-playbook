#!/usr/bin/env bash
# Audits on the FINAL file: length vs limit, loudness, near-blank frames, contact sheets, and (optional) every line heard.
# Usage: bash qa.sh final.mp4 <limit_seconds> [lines.json]
# Then LOOK at qa/sheet_*.png yourself, and have a person watch it once with sound.
set -uo pipefail
F="$1"; LIMIT="${2:-180}"; LINES="${3:-}"; HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p qa
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
python3 - "$d" "$LIMIT" <<'PY'
import sys; d, lim = float(sys.argv[1]), float(sys.argv[2])
print(f"length   {int(d//60)}:{d%60:05.2f}  limit {int(lim//60)}:{lim%60:05.2f}  " + ("OVER LIMIT" if d >= lim else f"margin {lim-d:.1f} s" + ("  (thin: keep 1+ s)" if lim-d < 1 else "")))
PY
ffmpeg -hide_banner -nostats -i "$F" -af ebur128=peak=true -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{printf "loudness %s LUFS (target about -14)\n",$2} f&&/Peak:/{printf "peak     %s dBFS (keep under -1)\n",$2; exit}'
# near-blank frames: very low detail for more than 0.2 s (black, white or plain paper)
ffmpeg -v error -i "$F" -vf "fps=10,scale=160:90,format=gray" -f rawvideo - | python3 -c "
import sys, numpy as np
x = np.frombuffer(sys.stdin.buffer.read(), np.uint8).reshape(-1, 90, 160).astype(np.float32)
sd = x.std((1, 2)); low = sd < 6; runs = []; s = None
for i, v in enumerate(low):
    if v and s is None: s = i
    if not v and s is not None: runs.append((s, i)); s = None
if s is not None: runs.append((s, len(low)))
runs = [(a / 10, b / 10) for a, b in runs if b - a > 2]
print('blank    ' + ('none' if not runs else ', '.join(f'{a:.1f}-{b:.1f}s' for a, b in runs) + '  <- look at these (planned fades are fine)'))
"
python3 "$HERE/../contact_sheet.py" qa/sheet.png --video "$F" --every 1 --cols 6 --thumb 320 --per-sheet 60 | sed 's/^/sheet    /'
if [ -n "$LINES" ]; then
  echo "== every line heard (speech-to-text on the final mix)"
  python3 "$HERE/align.py" check "$F" --lines "$LINES"
fi
echo "Now: look at every qa/sheet_*.png, run dwell.mjs on the composition, check claims against FACTS.md, and watch it once with sound."
