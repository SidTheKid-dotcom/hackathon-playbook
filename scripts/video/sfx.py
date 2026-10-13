#!/usr/bin/env python3
"""Soft sound effects and an optional quiet music bed, all synthesized: no licences, nothing to credit but "made in code".

  python3 sfx.py <out_dir> [bed_seconds]
Writes paper, hl (highlighter), stamp, key, tick, tap, whoosh, pop, sent, blocked .wav (48 kHz stereo),
and bed.wav (a warm pad) if bed_seconds is given. Use few effects, softly, on the same words as the motion.
Needs numpy.
"""
import os
import numpy as np, wave, sys
SR = 48000; rng = np.random.default_rng(3)
if len(sys.argv) < 2: sys.exit(__doc__)
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
def save(name, x, peak=0.8):
    x = x / (np.abs(x).max() + 1e-9) * peak
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(f"{OUT}/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
def t(d): return np.arange(int(SR * d)) / SR
def lp(x, a):  # one-pole low-pass, a in (0,1): smaller = darker
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s += a * (v - s); y[i] = s
    return y
def hp(x, a): return x - lp(x, a)
def env(n, att, rel, shape=2.0):
    e = np.ones(n); A = max(1, int(att * SR)); e[:A] = np.linspace(0, 1, A) ** 1.5
    R = max(1, int(rel * SR)); e[-R:] *= np.linspace(1, 0, R) ** shape; return e
# paper slide: brushed noise, rising then falling brightness
d = .42; n = rng.normal(0, 1, int(SR * d)); x = hp(lp(n, .18), .02) * env(len(n), .08, .3)
save("paper", x * np.sin(np.linspace(0, np.pi, len(n))) ** .6, .45)
# highlighter: felt tip dragging, a soft band of noise with gentle wobble
d = .55; n = rng.normal(0, 1, int(SR * d)); wob = 1 + .25 * np.sin(2 * np.pi * 7 * t(d))
x = hp(lp(n, .09), .01) * wob * env(len(n), .04, .18)
save("hl", x, .32)
# stamp: rubber stamp on paper on a desk; low thud + short paper slap
d = .45; tt = t(d); f = 95 * np.exp(-tt * 9) + 48
th = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 13)
sl = hp(rng.normal(0, 1, len(tt)), .3) * np.exp(-tt * 55) * .5
save("stamp", lp(th + sl, .5), .85)
# typewriter-ish key: very short, soft (used sparingly in a light pattern)
d = .07; tt = t(d); k = hp(rng.normal(0, 1, len(tt)), .35) * np.exp(-tt * 140) + np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt * 160) * .4
save("key", k, .35)
# tick: soft wooden tick for list items / check marks
d = .12; tt = t(d); x = np.sin(2 * np.pi * 1250 * tt) * np.exp(-tt * 70) + np.sin(2 * np.pi * 2500 * tt) * np.exp(-tt * 110) * .3
save("tick", x, .35)
# tap: phone tap, a muted click
d = .09; tt = t(d); x = np.sin(2 * np.pi * 620 * tt) * np.exp(-tt * 90) + lp(rng.normal(0, 1, len(tt)), .3) * np.exp(-tt * 120) * .4
save("tap", x, .4)
# whoosh: soft air, for camera moves (kept quiet)
d = .7; n = rng.normal(0, 1, int(SR * d)); sh = np.sin(np.linspace(0, np.pi, len(n))) ** 2
x = np.concatenate([lp(n[:len(n)//2], .03), lp(n[len(n)//2:], .06)]) * sh
save("whoosh", x, .25)
# pop: a node appearing in the diagram, a small round bubble
d = .16; tt = t(d); f = 520 + 380 * np.exp(-tt * 40)
x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 28) * env(len(tt), .004, .05)
save("pop", x, .3)
# sent: two soft rising notes (message delivered)
d = .5; tt = t(d)
a = np.sin(2 * np.pi * 880 * tt) * np.exp(-tt * 9) * (tt < .25); b = np.sin(2 * np.pi * 1318.5 * (tt - .12)) * np.exp(-(tt - .12) * 8) * (tt >= .12)
save("sent", (a + b) * env(len(tt), .005, .2), .28)
# blocked: a low muffled double knock (guardrail)
d = .45; tt = t(d)
k1 = np.sin(2 * np.pi * 160 * tt) * np.exp(-tt * 30); k2 = np.sin(2 * np.pi * 140 * (tt - .16)) * np.exp(-(tt - .16) * 30) * (tt >= .16)
save("blocked", lp(k1 + k2, .4), .6)

# --- music bed: warm pad, Dmaj9 Bm9 Gmaj9 A6sus, 4.8 s per chord, gentle sparse plucks ---
if len(sys.argv) < 3: print("effects written to", OUT); sys.exit(0)
dur = float(sys.argv[2]); N = int(SR * dur); tt = np.arange(N) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[50, 57, 62, 66, 69, 76], [47, 54, 61, 62, 66, 73], [43, 50, 59, 62, 66, 69], [45, 52, 59, 61, 64, 66]]
C = 4.8; pad = np.zeros(N)
for ci in range(int(dur / C) + 2):
    ch = chords[ci % 4]; s0 = int((ci * C - .6) * SR); s1 = int(((ci + 1) * C + 1.2) * SR)
    s0c, s1c = max(0, s0), min(N, s1)
    if s0c >= s1c: continue
    seg = tt[s0c:s1c]; L = s1 - s0; e = env(L, 1.4, 1.8, 1.5)[s0c - s0: s1c - s0]
    for m in ch:
        for det in (-.0025, .0025):
            ph = rng.random() * 6.28
            pad[s0c:s1c] += (np.sin(2 * np.pi * hz(m) * (1 + det) * seg + ph) + .18 * np.sin(4 * np.pi * hz(m) * seg + ph)) * e / len(ch)
pad = lp(pad, .06)
# sparse plucks (felt-piano feel) on chord tones, one every ~2.4 s
pl = np.zeros(N)
for k in range(int(dur / 2.4)):
    ch = chords[int(k * 2.4 / C) % 4]; m = ch[[3, 4, 5, 4][k % 4]] + 12 * (k % 3 == 0)
    s = int((k * 2.4 + .3) * SR); L = min(int(2.2 * SR), N - s)
    if L <= 0: break
    ts = np.arange(L) / SR; pl[s:s + L] += np.sin(2 * np.pi * hz(m) * ts) * np.exp(-ts * 2.6) * (1 - np.exp(-ts * 300)) * .35
bed = pad * .8 + lp(pl, .25)
# slow stereo drift
pan = .5 + .12 * np.sin(2 * np.pi * tt / 11)
st = np.stack([bed * (1 - pan) * 2, bed * pan * 2], 1)
st /= np.abs(st).max(); 
with wave.open(f"{OUT}/bed.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * .9 * 32767).astype(np.int16).tobytes())
print("ok")
