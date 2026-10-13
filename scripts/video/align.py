#!/usr/bin/env python3
"""Word timings from narration audio, and a check that a final mix says every line.

  align.py words [--lines lines.json] [--vo vo] [ids...]
      For each line in lines.json ({"id", "text", "say"?}), transcribe vo/<id>.(wav|m4a|mp3) and write
      vo/<id>.words.json = [{"w", "t", "e"}] over the DISPLAY text (times relative to that file).
      Prints a match score per line; < 0.85 means words were skipped, repeated or misread: listen.
  align.py check <final.mp4|wav> [--lines lines.json]
      Transcribes the finished soundtrack and confirms each line's first and last words are heard, in order.

Needs faster-whisper (pip install faster-whisper, or: uv run --with faster-whisper python align.py ...).
Model: env WHISPER_MODEL (default small.en). Language: env WHISPER_LANG (default en).
"""
import argparse, difflib, json, os, re, sys

norm = lambda w: re.sub(r"[^\w]", "", w.lower())


def model():
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper is missing: pip install faster-whisper  (or run with: uv run --with faster-whisper ...)")
    return WhisperModel(os.environ.get("WHISPER_MODEL", "small.en"), device="cpu", compute_type="int8")


def audio_for(vo, i):
    for ext in ("wav", "m4a", "mp3", "flac", "ogg"):
        p = os.path.join(vo, f"{i}.{ext}")
        if os.path.exists(p):
            return p
    sys.exit(f"no audio for line {i} in {vo}/")


def words(a):
    lines = json.load(open(a.lines)); only = set(a.ids); m = model()
    for L in lines:
        if only and L["id"] not in only:
            continue
        say = L.get("say", L["text"])
        segs, _ = m.transcribe(audio_for(a.vo, L["id"]), language=os.environ.get("WHISPER_LANG", "en"),
                               word_timestamps=True, beam_size=5, initial_prompt=say)
        heard = [w for s in segs for w in s.words]
        H = [norm(w.word) for w in heard]
        score = difflib.SequenceMatcher(None, [norm(w) for w in say.split()], H).ratio()
        disp = L["text"].split(); out = [None] * len(disp)
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, [norm(w) for w in disp], H, autojunk=False).get_opcodes():
            if op == "equal":
                for k in range(i2 - i1):
                    out[i1 + k] = (heard[j1 + k].start, heard[j1 + k].end)
            elif op == "replace" and j2 > j1:  # e.g. "SHA-256" heard as several words: share the span
                s0, s1 = heard[j1].start, heard[j2 - 1].end; n = i2 - i1
                for k in range(n):
                    out[i1 + k] = (s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n)
        for i in range(len(out)):  # words never heard: place between neighbours
            if out[i] is None:
                prev = next((out[j][1] for j in range(i - 1, -1, -1) if out[j]), heard[0].start if heard else 0.0)
                nxt = next((out[j][0] for j in range(i + 1, len(out)) if out[j]), heard[-1].end if heard else prev)
                out[i] = (prev, max(prev, nxt))
        res = [{"w": w, "t": round(s, 3), "e": round(e, 3)} for w, (s, e) in zip(disp, out)]
        json.dump(res, open(os.path.join(a.vo, f"{L['id']}.words.json"), "w"), ensure_ascii=False)
        flag = "  <-- CHECK (listen to this line)" if score < .85 else ""
        print(f"{L['id']:6} match {score:.2f}  heard: {' '.join(w.word.strip() for w in heard)[:100]}{flag}", flush=True)


def check(a):
    lines = json.load(open(a.lines)); m = model()
    segs, _ = m.transcribe(a.audio, language=os.environ.get("WHISPER_LANG", "en"), word_timestamps=True, beam_size=5)
    heard = [(norm(w.word), w.start) for s in segs for w in s.words if norm(w.word)]
    pos, bad = 0, 0
    for L in lines:
        say = [norm(w) for w in L.get("say", L["text"]).split() if norm(w)]
        first, last = say[0], say[-1]
        i = next((k for k in range(pos, len(heard)) if heard[k][0] == first), None)
        j = next((k for k in range((i or pos), len(heard)) if heard[k][0] == last), None) if i is not None else None
        ok = i is not None and j is not None
        bad += not ok
        t = f"{heard[i][1]:7.2f}s" if i is not None else "   ?   "
        print(f"{L['id']:6} {t}  first '{first}' {'ok' if i is not None else 'MISSING'}, last '{last}' {'ok' if j is not None else 'MISSING'}")
        if j is not None:
            pos = j + 1
    print(f"{len(lines) - bad}/{len(lines)} lines start and end on the right word"
          + ("" if not bad else ". Numbers may be heard as digits ('700' vs 'seven'): check flagged lines by ear."))
    sys.exit(1 if bad else 0)


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
w = sub.add_parser("words"); w.add_argument("ids", nargs="*"); w.add_argument("--lines", default="lines.json"); w.add_argument("--vo", default="vo")
c = sub.add_parser("check"); c.add_argument("audio"); c.add_argument("--lines", default="lines.json")
a = ap.parse_args()
words(a) if a.cmd == "words" else check(a)
