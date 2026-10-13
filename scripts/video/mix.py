#!/usr/bin/env python3
"""Mix narration, word-locked sound cues and an optional ducked music bed into out/mix.wav (48 kHz stereo).

  python3 mix.py [--timeline timeline.json] [--vo vo_fit] [--cues out/cues.json] [--sfx sfx] [--bed sfx/bed.wav]
                 [--fx-gain 0.30] [--bed-gain 0.16] [--duck 0.09]
Cues come from the composition (window.CUES = [{t, name, gain}]), written by render.mjs.
The bed sits at bed-gain in pauses and drops by `duck` under speech (120 ms attack, 600 ms release).
Final loudness is set later by finish.sh (-14 LUFS). Needs numpy.
"""
import argparse, json, os, sys, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--timeline", default="timeline.json"); ap.add_argument("--vo", default="vo_fit")
ap.add_argument("--cues", default="out/cues.json"); ap.add_argument("--sfx", default="sfx")
ap.add_argument("--bed", default=""); ap.add_argument("--out", default="out/mix.wav")
ap.add_argument("--fx-gain", type=float, default=0.30); ap.add_argument("--bed-gain", type=float, default=0.16)
ap.add_argument("--duck", type=float, default=0.09)
a = ap.parse_args()
SR = 48000


def rd(f):
    with wave.open(f) as w:
        if w.getframerate() != SR or w.getsampwidth() != 2:
            sys.exit(f"{f}: needs 16-bit {SR} Hz wav (timeline.py and sfx.py write that)")
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        x = x.reshape(-1, w.getnchannels())
    return np.repeat(x, 2, 1) if x.shape[1] == 1 else x


TL = json.load(open(a.timeline)); N = int((TL["total"] + .5) * SR)
vo = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32)


def put(buf, x, t, g=1.0):
    i = max(0, int(t * SR)); x = x[: max(0, N - i)]; buf[i:i + len(x)] += x * g


for s in TL["segments"]:
    put(vo, rd(os.path.join(a.vo, f"{s['id']}.wav")), s["t"])
cues = json.load(open(a.cues)) if os.path.exists(a.cues) else []
cache = {}
for c in cues:
    if c["name"] not in cache:
        cache[c["name"]] = rd(os.path.join(a.sfx, f"{c['name']}.wav"))
    put(fx, cache[c["name"]], c["t"], c.get("gain", 1.0))
vo *= 0.70 / (np.abs(vo).max() + 1e-9)          # voice peak about -3 dBFS before loudness normalisation
mix = vo + fx * a.fx_gain
if a.bed and os.path.exists(a.bed):
    bed = rd(a.bed)[:N]; bed = np.pad(bed, ((0, N - len(bed)), (0, 0)))
    win = int(.05 * SR); env = np.convolve(np.abs(vo[:, 0]), np.ones(win) / win, "same")
    talk = (env > 0.01).astype(np.float32)
    g = np.empty(N, np.float32); up = 1 - np.exp(-1 / (.12 * SR)); dn = 1 - np.exp(-1 / (.6 * SR)); s = 0.0
    for i in range(0, N, 48):
        tgt = talk[i]; s += (tgt - s) * (1 - (1 - (up if tgt > s else dn)) ** 48); g[i:i + 48] = s
    tt = np.arange(N) / SR
    level = (a.bed_gain - a.duck * g) * np.clip(tt / 1.5, 0, 1) * np.clip((TL["total"] + .3 - tt) / 2.5, 0, 1)
    mix += bed * level[:, None]
mix /= max(1.0, np.abs(mix).max() / 0.95)
os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
with wave.open(a.out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print(f"{a.out}: {N / SR:.2f} s, {len(TL['segments'])} lines, {len(cues)} cues, bed {'on' if a.bed else 'off'}")
