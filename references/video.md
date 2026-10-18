# Phase 7: Demo video

Goal: in the time limit, a judge who knows nothing learns the problem, the user, what the product does, where the sponsor's tech fits, and what changes in the world. The video is often the whole judgement; if it is not shown, it does not count.

## Contents
1. Research the brief
2. Story
3. Script and pacing
4. Picture
5. Voice and sound
6. Production pipeline
7. Audits
8. Change rounds

## 1. Research the brief
- Read the event's video rules (length, host, visibility, required topics) and quote them in the profile.
- Watch the best past winning videos of this organiser. Map each beat to a criterion, second by second.
- Know the judges. Engineers want to see the system working; they spot mock UI and logo-only "architecture" instantly.

## 2. Story
Write the story and video script: problem before fix, real flow on real data, sponsor services visible, one failure case, one honest limit, data freshness, a memorable tagline.
- **Throughline in 15 words or fewer** (TED). Every scene serves it.
- **And, But, Therefore**: "X happens, and Y makes it worse, but Z was already promised, therefore the product does W."
- **Contrast what is with what could be**, and end on the better future plus the action.
- **Open hard**: a bold picture and one number in the first 3 seconds, the name by about 10 seconds, and the track's key phrase in the first 15 seconds. No "Hi, we are team…".
- **A real person** with a lived connection beats a persona ("I live next to one"). Emotion must be true, sourced, and told with respect: one plain sentence about a tragedy, not the whole story built on it.
- **Make the stakes concrete**: what happens to the user if nothing changes (a fine, a deadline, a cost), all sourced.
- **Show who is accountable** when it matters to the outcome, but only with sourced powers.
- **Say plainly where the numbers come from and how fresh they are.** Avoid relative time words ("last night", "this week"); the judge only knows the video, not when it was made.

## 3. Script and pacing
- About 140 words a minute is clear narration, a little slower over demos. **Word budget ≈ (limit − 10 s) × 2.3 words per second** (≈ 390 words for 3:00; aim for about 340).
- Default split: problem 20–30%, live flow on the real product 40–50%, how it works (the sponsor's tech shown running) 15–20%, outcome and close 10%.
- One idea per beat. Re-hook around 60% of the way through: a new person or a new screen.
- Write the script as a table (see templates.md): time, voice line, what is on screen, the animation and the word it lands on, sound, source. Plain words; the user rewords it into their own voice.
- Read it aloud with a timer before recording anything.

## 4. Picture
- **Motion lands on the word.** Show the matching picture at the same moment the narration says it. This had the largest effect of any multimedia principle tested (Mayer, temporal contiguity). Cut on stressed syllables, and let the voice lead into new sections slightly.
- **Signal the essential thing**: one signature motion (for example a highlighter) marks what is being said, at the moment it is said.
- **Cut anything decorative**: logo intros, transitions that call attention to themselves, music-only stretches.
- **Mostly real footage** (default about 60%): the live product, recorded at 2× resolution with a scripted browser so every take is identical, plus real consoles and logs. `scripts/video/record.py` records a headed browser on a virtual display with a smooth cursor and logs when each action happens. To show a coding agent using the product, run the agent for real in non-interactive mode, save its event log, and replay that log on screen with the label "replayed from its log". Drawn scenes (problem, architecture, title and end cards) in the product's own visual style, so it all looks like one film. Never draw a fake product screen.
- Zoom in (1.5–2×) on the element being talked about. No wandering mouse, no real-time typing, no uncropped consoles, no text too small to read.
- Show real outputs, trimmed and labelled "trimmed". A hand-written imitation of a log or API response looks mocked.
- Every on-screen text stays fully readable for at least 0.5 s + 0.22 s per word (minimum 1.2 s). Sources and credits too.
- Captions: always upload a caption file. If you burn them in, keep them short, at the bottom, and clear of the key area (centred under the phone during a phone demo). Build caption text from the **script**, aligned to the speech-to-text word times. Raw transcripts misspell product names and terms.
- Do not put labels, tags or callouts on top of product footage the viewer must read. Zoom to the element and let the caption carry the words.
- Video chapters: take the times from the voice timeline (the start of each line), not from scene detection. Soft fades hide cuts.

## 5. Voice and sound
- **Voice, best first:** a team member's own recorded voice; then a clone of that voice; then a TTS voice. Judges reject fully AI-made work, and a clone mispronounces local names. Record one file per line on a phone, in a quiet room, at the same distance, with a pause before and after each line.
- Processing: trim each clip to the speech plus a little air, cut low rumble, apply gentle noise reduction, and level the clips to one loudness. **Never change the voice speed without telling the user**; if you must, apply the same small factor to every line and keep the pitch.
- Sound effects: few, soft, and on the same trigger words as the motion. Synthesize them or use licensed ones, and credit them.
- A quiet music bed that ducks under the voice. Final loudness about −14 LUFS (YouTube's target), with the peak under −1 dBFS.

## 6. Production pipeline (pick the fastest for this team)
| Approach | When |
|---|---|
| Screen recordings + a normal video editor | The team has an editor and little time |
| Code-drawn composition: an HTML page with `seek(t)`, rendered frame by frame in a headless browser, then joined with ffmpeg | You want exact word sync and re-renders in minutes; `scripts/video/` is a ready kit |
| A code-video framework (Remotion, HyperFrames and similar) | The team already knows one |

Voice first in every approach: record the narration, get the word times (forced alignment with a speech-to-text model), then pin every animation and sound to a word, not to a clock time. When a line is re-recorded, everything re-syncs.

## 7. Audits (run on the final file, every render)
```
- [ ] Length under the limit with margin (ffprobe)
- [ ] Loudness about −14 LUFS, peak under −1 dBFS
- [ ] Every line's first and last word heard correctly (speech-to-text on the final mix)
- [ ] No blank or broken frames (scan, then look at the flagged ones yourself)
- [ ] Contact sheet of the whole film (about 1 frame per second), reviewed by eye
- [ ] Reading-time audit: every text on screen long enough
- [ ] Claims sheet: every number, quote, date, name and place against FACTS.md and live data
- [ ] Voice and screen agree (what is said is what is shown)
- [ ] A person watched it once with sound (agents cannot judge the audio)
- [ ] Proxy viewers who know nothing can state the problem, the solution and the outcome
```
Fact-check every cut frame by frame: every number, quote, date, name and claim against `FACTS.md` and live data. Verify flagged frames yourself; video-reading tools misread text.
Check voice vs screen mismatches, translations, mocked-looking output (label trimmed output), runtime under the limit with margin.

## 8. Change rounds
- Before any re-render, list the exact changes (add, replace, delete), with timestamps and the new estimated length. Get a "go".
- Keep the previous render as a fallback until the new one passes the audits.
- Re-render only the parts that changed, when the pipeline allows.
- When people outside the team give feedback, take it seriously. Proxy judges are the closest thing to the real ones. But apply hard rule 2 to anything they suggest saying.
