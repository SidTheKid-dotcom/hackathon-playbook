---
name: hackathon-playbook
description: >-
  Runs a win-first hackathon process end to end: decode the organisers,
  judges, rules and past winners; set constraints; hunt, prior-art-check and
  kill-test ideas; lock one with a fallback; then setup, scope, build, UI,
  verification, demo video, README, form and freeze, with every hour mapped to
  the judging criteria. Use whenever the user says things like "help me win
  this hackathon", "find a problem statement for <hackathon>", "research the
  judges / past winners", "score or kill-test our idea", "idea is locked, what
  now", "plan the build", "make / plan / audit the demo video", "check the UI
  before we submit", "write the README or the submission form", "are we ready
  to submit", or "what is left before the deadline", even if they never say
  "playbook". Works for any sponsor or stack, including open-source-only or
  offline events. Not for everyday coding outside a competition or for
  non-competitive side projects.
metadata:
  author: SidTheKid-dotcom
  version: "2.1"
---
# Hackathon playbook: from event page to submission

Goal: find one idea that is unique, impactful and buildable in the time box, then turn it into the entry the judges score highest, inside the rules and the time box. Judges see only what is submitted: usually a video, a repo, a live link and a form. Every hour must move a judging criterion. Be blunt, score honestly, never flatter.

## How to use this skill
- Find the current phase in the map below and read only that phase's reference file. Load files as each phase starts, not all at once.
- If the project has no event profile yet, do Phase 0 first; every later phase reads it. If a `WINNING_PLAYBOOK.md` already exists, distil the profile from it instead of researching again.
- If the team already has a locked idea, skip Phase 1, but still write the ICP, the fallback and the day-1 go/no-go gate.
- Every default here comes with its reason. **The event profile overrides any default** (stack, hosting, repo layout, video format). Only the hard rules below never bend.
- Write project documents (profile, `FACTS.md`, story, plans) in the user's project, not in this skill folder.
- For product or UI changes: propose a short plan, get the user's "go", then build. Bug fixes the user asked for can go straight ahead.
- Do the investigation yourself. Ask the user only for decisions that are theirs: scope, taste, wording, and anything public or hard to undo.
- **Memory across threads:** keep `AGENTS.md`, `PROGRESS.md` and `LEARNINGS.md` in the project from day one. Read them at the start of every session; update them at the end. Switch to a new thread instead of stretching one. See [memory.md](references/memory.md).
- **More than one agent, or work while the user is away:** see [orchestration.md](references/orchestration.md) for roles, task files, worktrees, long jobs and unattended rules.
- **Writing standard:** write agent files and status reports at about 80% of ASD-STE100 Simplified Technical English (one fact per sentence, active voice, one word for one thing). Write the README, form and narration plainly and factually, with no sales language.

## Hard rules (the only ones that never bend)
1. **The official rules win.** Deadline with timezone, eligibility, required artifacts, banned tools. Re-check announcements; deadlines move.
2. **No claim without a source.** Every number, quote, date and name in the UI, README, form and video traces to `FACTS.md` or live data.
3. **Judges score what the submission shows.** A feature that is not in the video (or other required artifact) scores nothing.
4. **Stay inside format limits with margin**: video length, word counts, file sizes.
5. **Submit a complete version early.** Polish only with margin left.
6. **Freeze after the deadline.** No pushes and no live changes during judging, unless the rules allow it.
7. **Never fake anything**: history, users, data, results or testimonials. No mock data in the demo path.

## Phase map
| # | Phase | Goal | Read | Gate: answer "yes" before moving on |
|---|---|---|---|---|
| 0 | Decode the game | Rules, judges and past winners become constraints | [event-profile.md](references/event-profile.md) | Can you list the criteria, required artifacts, required or banned tech, deadline with timezone, and what the sponsor wants shown? Are judges and past winners researched, with checked citations, and is there a proxy score with a target? |
| 1 | Ideas and lock | One unique, felt, buildable idea | [ideas.md](references/ideas.md) | Did the locked idea pass prior art, sponsor removal, the agentic test (if AI), demand and a real-data kill test? Is there one ICP, a fallback and a day-1 go/no-go gate? |
| 2 | Setup | Repo, facts, first risk | [setup.md](references/setup.md) | Did the go/no-go gate pass (or did you switch to the fallback)? Is the riskiest unknown tested? Do `FACTS.md` and a never-claim list exist? Is paid spend capped? |
| 3 | Scope | One user, one decision, one action | [scope.md](references/scope.md) | Can a stranger say who it is for and what they do in 10 seconds? Is there a written cut list and a feature-stop time? |
| 4 | Build | One real flow end to end, then depth | [build.md](references/build.md) | Does the core flow run on real data where judges will open it? Can every output be traced and checked? |
| 5 | UI | Clear at first glance, works everywhere | [ui.md](references/ui.md) | Did someone outside the team pass the 5-second test? Was every target width and language checked by eye? |
| 6 | Verify | Nothing false, nothing broken | [verify.md](references/verify.md) | Were old features re-tested? Is every claim matched to a source? Can the tests fail? |
| 7 | Video | The story the judges score | [video.md](references/video.md) | Under the limit? Every claim sourced? Every text readable long enough? Watched once with sound by a person? |
| 8 | Submit and freeze | Complete, consistent, early | [submit.md](references/submit.md) | Do video, repo, live link and form tell one story with the same numbers? Did each open signed out? |

**Before kickoff:** Phases 0 and 1 happen before the event starts when the rules allow (research and kill tests are not project code). If they must happen inside the event, give them about 10% of the hours.

**Time budget (default share of event hours; shift it to match the rubric):** setup 5%, scope 5%, build 40%, UI 15%, verify 5% plus continuous checks, video 20%, submit 10%. Feature stop at about 75% of the time. A design-heavy rubric gets more UI time; a video-only judging round gets more video time.

## The loop inside every phase
- **Re-score bluntly after every change**, against the proxy rubric in the profile. Write down the score and the single biggest gap. Work on that gap next.
- **Handle outside input on evidence.** A teammate's line, a friend's critique or a proxy judge's comment: check each point against sources, take what is true and better, and explain what you drop. No ego either way.
- **Show evidence, not claims of done**: command output, a screenshot, a measured number, a live URL.
- **Record what is deferred.** Keep a short "on hold" list so cut ideas are not lost and are not built by accident.

## Gotchas (each one cost real hours)
- **Ideas that AI agents suggest by default are crowded.** Developer tools and coding agents most of all; test with the niche check in ideas.md.
- **"AI layer over an existing tool" is the most common thin idea.** One lookup plus an LLM write-up is not an agent.
- **A map or dashboard with no decision attached is a weak entry.**
- **Overclaiming the problem invites pushback.** State the narrow, provable gap, not "the AI is wrong".
- **"Deployed" is not "live".** Check the deploy path you assume (a push may not deploy anything). Hosting rewrites and CDN caches can serve stale or wrong files; one SPA fallback served a new file type as HTML. Fetch the live URL.
- **Safety filters read your own instructions too.** A banned-word filter and a prompt-injection filter blocked every legitimate output, because the system prompt mentioned the banned words. Filter outputs; test one case that must be blocked and one that must pass.
- **An overflow audit misses overlap.** Elements on top of each other, clipped letter tails, a sticky bar hiding a button: only looking at screenshots catches these.
- **Non-Latin scripts break layouts.** A tight line-height clips marks above and below; per-letter animations split joined characters. Test every language at the narrowest width.
- **Find-and-replace in translations doubles phrases and breaks grammar.** Read every string afterwards.
- **Sample statistics lie at scale.** "40% of files are scans" from a 25-file sample was 12 in 1,027 on the full set. Re-measure before you state it.
- **Public numbers go stale.** A scheduled job changed totals after the README was written. Regenerate copy from the live source before you submit.
- **An unsourced number never reaches the screen**, however good it sounds and whoever suggested it (a teammate, an AI, you).
- **Overclaims hide in wording and pairing.** Watch for:
  - present tense for a rule that was paused;
  - a fine shown next to a city that has no fines;
  - a power ("officers fine builders") with no source;
  - a headline that says "building collapse" over narration about a waste collapse.

  Check the tense, the place and the picture under every line.
- **A fix can cause new damage.** A rule to trim silence clipped the first word of narration lines. After any fix, re-check the whole output, not only the thing you fixed.
- **`pkill -f pattern` can match its own shell** and kill your command. Kill by PID or by port.
- **Video length creeps.** Each improvement adds seconds. Measure the runtime after every change, and tell the user whenever you change speed or pacing.
- **Long jobs die with the agent's tool call.** A render or test run started inside a tool call can be cancelled when the call ends. Start long jobs detached (`systemd-run --user` or `setsid nohup`) and poll the log. Find where time goes before you buy more compute.
- **Run the full test suite before every push.** A subset that passes locally can still turn CI red on the public repo page. Tests that check for placeholder text fail when you fill in the real value.
- **Data defaults fake precision.** A stored date of the 1st of a month, or midnight UTC, often means "unknown day". Print only the precision the source gives.
- **The secret scan does not see personal data unless you ask it to.** Check tracked files for personal emails and names before going public; `scripts/secret_scan.sh` now does.
- **Platforms change under you.** GPU quota was 0 in the main cloud region; GitHub OIDC switched to immutable subject IDs; a free TTS plan could not use library voices over the API. Read the actual error or claim before you guess.
- **Negative wording about the sponsor's products reads badly to sponsor judges.** Write feedback as "what worked, plus one suggestion".

## Don't skip
| Temptation | Why not |
|---|---|
| "We already like this idea, skip the kill test" | Most ideas fail on real data; find out in hours, not days. |
| "Prior art later, after we've scored it" | Late prior-art finds waste whole rounds of work. |
| "Everyone could use it" | Broad audiences make vague demos. Pick one ICP and build for them. |
| "It's a real problem, so people will use it" | Real but unfelt problems get no users. Check demand. |
| "That fact sounds right, pitch it" | Unverified pitch facts erode trust and resurface as errors. |
| "A stand-in shows the problem well enough" | Judges trust the real product's output. Capture it early. |
| "Judges are unknown, skip that step" | Recording the gap sets the right assumption. |
| "The audit passed, ship it" | Scripts check only what you told them to check. Look at the screenshots and frames yourself. |
| "It works locally" | Judges open the live link. Test it signed out, after deploy, after caches clear. |
| "One more feature" after the feature stop | Each feature needs UI, video time, README text and verification. Shown depth beats added breadth. |
| "The model's output looks right" | Make code verify it against the source, and send doubt to a visible review state. |
| "The number is close enough" | One wrong figure discredits every right one. Trace it or cut it. |
| "A cooler device would impress (watch, VR, 3D)" | Judges punish shoehorning. Fit the device to the user, and make the existing depth visible. |
| "We'll write the README at the end" | Draft it during the build. The last day belongs to the video. |
| "Just speed the voice up a little" | Say so. Silent pacing changes break trust and sync. |

## Templates, example and scripts
- [templates.md](references/templates.md): winning playbook and idea shortlist, event profile, `FACTS.md`, story table, claims sheet, README skeleton, form answers, memory files, task file, auditor prompt, thread handoff prompt.
- [worked-example.md](references/worked-example.md): one complete run (VACHAN, WeMakeDevs x AWS, Oct 2026). It is one example, not a template; do not copy its stack.
- Optional scripts, independent of the product's stack (need Node 18+ with Playwright, Python 3 with Pillow, and ffmpeg):
  - `scripts/ui_audit.mjs`: any web UI across routes, widths and languages. Checks sideways scroll, clipped text, overlaps, small tap targets and console errors, and saves screenshots.
  - `scripts/contact_sheet.py`: images or video frames in one labelled grid, for review by eye.
  - `scripts/secret_scan.sh`: scans git history and tracked files for keys, risky files and personal emails before a repo goes public.
  - `scripts/run_tasks.sh`: runs task files in order through an agent CLI in a worktree, retries once on timeout, logs commits per task. See orchestration.md.
  - `scripts/video/`: a voice-first video kit (word-timed HTML composition, parallel render, mix, captions, audits). See `scripts/video/README.md`.
