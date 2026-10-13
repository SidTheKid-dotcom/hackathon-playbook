#!/usr/bin/env python3
"""timeline.json -> captions file (.srt) for YouTube or any player.
  python3 srt.py [timeline.json] [captions.srt] [--max 38]
Cues break at sentence ends, at commas past 24 characters, or at --max characters. Upload it as a subtitle file.
"""
import json, sys

argv = [x for x in sys.argv[1:] if not x.startswith("--")]
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 38
argv = [x for x in argv if not x.isdigit()]
tl = argv[0] if argv else "timeline.json"; out = argv[1] if len(argv) > 1 else "captions.srt"
TL = json.load(open(tl))


def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


cues = []
for seg in TL["segments"]:
    cur = []
    for w in seg["words"]:
        cur.append(w); text = " ".join(x["w"] for x in cur)
        if len(text) >= MAX or w["w"][-1] in ".?!:" or (w["w"][-1] == "," and len(text) > 24):
            cues.append(cur); cur = []
    if cur:
        cues.append(cur)
lines = []
for i, c in enumerate(cues, 1):
    end = c[-1]["e"] + .25
    if i < len(cues):
        end = min(end, cues[i][0]["t"] - .02)
    lines.append(f"{i}\n{ts(c[0]['t'])} --> {ts(end)}\n{' '.join(x['w'] for x in c)}\n")
open(out, "w").write("\n".join(lines))
print(f"{out}: {len(cues)} cues, film {TL['total']} s")
