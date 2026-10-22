# Voice-first video kit

Narration drives everything: each animation and sound is pinned to a spoken word, so re-recording a line re-syncs the film. The film is an HTML page with a `seek(t)` function, rendered frame by frame in a headless browser. It works for any product stack. Use it when exact word sync and fast re-renders matter; a normal editor is fine otherwise.

**Needs:** ffmpeg, Node 18+ with Playwright (or `PLAYWRIGHT_PATH` + `CHROME_PATH`), Python 3 with numpy and Pillow, and faster-whisper for alignment (`uv run --with faster-whisper ...` works without installing it).

## Project layout (one folder per video version; keep the previous one as a fallback)
```
lines.json            [{"id":"s01","text":"display words","say":"spoken words if different","gap":0.6}, ...] in film order
vo/<id>.wav|m4a|mp3   one recording per line (a person's own voice is best)
composition.html      copy of the starter; your scenes
rec/<clip>/00001.jpg  screen-recording frames (ffmpeg -i clip.mp4 -vf fps=30 rec/clip/%05d.jpg)
sfx/                  python3 sfx.py sfx <film_seconds>
```

## Recording the real product
`record.py takes.py` records a headed browser on a virtual display with ffmpeg (2880×1620 by default), with a smooth injected cursor and a JSON log of when each action happens. Write your takes in a small `takes.py`; see the header of `record.py`. Use the logged times to cut the clips to the narration.

## Steps
```bash
K=<path-to-skill>/scripts/video          # for example ~/.claude/skills/hackathon-playbook/scripts/video
python3 $K/align.py words                 # word times per line; listen to any line flagged CHECK
python3 $K/timeline.py --limit 180        # lay lines on one clock -> timeline.json; prints total and margin
python3 $K/sfx.py sfx 180                 # synthesized effects + optional music bed
node    $K/render.mjs --workers 6         # -> out/video.mp4 and out/cues.json
python3 $K/mix.py --bed sfx/bed.wav       # voice + cues + ducked bed -> out/mix.wav
bash    $K/finish.sh                      # -> final.mp4 at -14 LUFS, prints length and loudness
python3 $K/srt.py timeline.json captions.srt
node    $K/dwell.mjs                      # every on-screen text readable long enough?
bash    $K/qa.sh final.mp4 180 lines.json # length, loudness, blank frames, contact sheets, every line heard
```
Then **look at every `qa/sheet_*.png` yourself**, check each claim against `FACTS.md`, and have a person watch the film once with sound.

## Rules that save hours
- Fit the length with pauses first (`--gapk 0.8`). Speed the voice (`--tempo 1.03`) only after asking, by the same factor for every line.
- Record screen footage with a scripted browser at 2× resolution and identical steps, so a re-take drops in at the same timings. Log the time of each tap as a marker.
- Every visual is a pure function of `t`: no CSS transitions, timers or `Date.now()`, or frames will differ between workers.
- `timeline.py` trims each clip using whisper's word times plus the audio energy, because whisper's first-word times can be late and clip soft starts.
- After any re-render, re-run `qa.sh`. A fix in one scene can break another.
