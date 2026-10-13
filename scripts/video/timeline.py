#!/usr/bin/env python3
"""Lay the narration lines on one clock -> timeline.json, plus fitted clips in vo_fit/.

Input: lines.json = [{"id", "text", "gap"?}] in film order, vo/<id>.<audio>, vo/<id>.words.json (from align.py words).
Each clip is trimmed to its speech (LEAD s before the first word, TAIL s after the last), resampled to 48 kHz mono,
optionally sped up by TEMPO (pitch kept), and placed after a pause of gap*GAPK seconds (default gap 0.5).

  python3 timeline.py [--tempo 1.0] [--gapk 1.0] [--hold 3.0] [--lead 0.12] [--tail 0.25] [--limit 180]

Prints each line's start time and the total. --limit warns when the film runs over (keep a margin).
Never change --tempo without telling the person whose voice it is.
"""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--lines", default="lines.json"); ap.add_argument("--vo", default="vo"); ap.add_argument("--out", default="vo_fit")
ap.add_argument("--tempo", type=float, default=1.0); ap.add_argument("--gapk", type=float, default=1.0)
ap.add_argument("--hold", type=float, default=3.0, help="seconds after the last line (end card)")
ap.add_argument("--lead", type=float, default=0.12); ap.add_argument("--tail", type=float, default=0.25)
ap.add_argument("--start", type=float, default=0.8, help="silence before the first line")
ap.add_argument("--limit", type=float, default=0.0)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)


def energy_db(path):
    """10 ms RMS loudness in dB, from ffmpeg (needs numpy)."""
    import numpy as np
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32)
    hop = 480; n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)


def speech_bounds(path, t_first, t_last):
    """Whisper's word times can be late at the start (it clipped a soft "P" once) or early at the end.
    Walk outwards from the first/last word through voiced frames, allowing pauses under 0.2 s."""
    import numpy as np
    db = energy_db(path); thr = np.percentile(db, 10) + 10; n = len(db)
    def walk(i, step):
        gap = 0
        while 0 < i < n - 1:
            if db[i + step] > thr:
                gap = 0
            else:
                gap += 1
                if gap > 20:
                    break
            i += step
        return i - step * gap
    on = walk(min(n - 1, int(t_first / .01)), -1) * .01
    off = walk(min(n - 1, int(t_last / .01)), 1) * .01
    return min(on, t_first), max(off, t_last)


def src(i):
    for ext in ("wav", "m4a", "mp3", "flac", "ogg"):
        p = os.path.join(a.vo, f"{i}.{ext}")
        if os.path.exists(p):
            return p
    sys.exit(f"no audio for {i}")


segments, t = [], a.start
for k, L in enumerate(json.load(open(a.lines))):
    wp = os.path.join(a.vo, f"{L['id']}.words.json")
    if not os.path.exists(wp):
        sys.exit(f"missing {wp}: run align.py words first")
    words = json.load(open(wp))
    on, off = speech_bounds(src(L["id"]), words[0]["t"], words[-1]["e"])
    s0 = max(0.0, on - a.lead); s1 = off + a.tail
    af = f"aresample=48000,atempo={a.tempo}" if a.tempo != 1.0 else "aresample=48000"
    dst = os.path.join(a.out, f"{L['id']}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{s0:.3f}", "-to", f"{s1:.3f}", "-i", src(L["id"]),
                    "-af", af, "-ac", "1", "-c:a", "pcm_s16le", dst], check=True)
    if k:
        t += L.get("gap", 0.5) * a.gapk
    sh = lambda x: round(t + (x - s0) / a.tempo, 3)
    ws = [{"w": w["w"], "t": sh(w["t"]), "e": sh(w["e"])} for w in words]
    end = round(t + (s1 - s0) / a.tempo, 3)
    segments.append({"id": L["id"], "t": round(t, 3), "end": end, "text": L["text"], "words": ws})
    print(f"{L['id']:6} {t:7.2f} - {end:7.2f}  {L['text'][:70]}")
    t = end
total = round(t + a.hold, 2)
json.dump({"segments": segments, "total": total, "tempo": a.tempo, "gapk": a.gapk}, open("timeline.json", "w"), indent=1, ensure_ascii=False)
m, s = divmod(total, 60)
print(f"total {total:.2f} s ({int(m)}:{s:05.2f})" + (f"  OVER the {a.limit:.0f} s limit" if a.limit and total > a.limit else
      (f"  margin {a.limit - total:.1f} s" if a.limit else "")))
