# Phase 0: Decode the game (event profile)

Goal: before any idea, know how this event is won. The output is one page in the project (`JUDGING.md` or `EVENT.md`) that every later decision reads, plus `WINNING_PLAYBOOK.md` with the deeper research. It turns the rules into constraints and sets the stack, so this skill's defaults never fight the event.

## Read these sources, and quote them
- Event page, rules, FAQ, schedule, the submission form's actual fields, and the judging criteria.
- Organiser announcements (blog, Discord, email). **Deadlines and rules change mid-event**; re-check them on the last day.
- Sponsor material: what the sponsor wants showcased, the build guides it published, and its judges' public posts.
- If a `WINNING_PLAYBOOK.md` already exists, copy the relevant parts from it. Do not research twice.

Read the official event page end to end: tracks and example problems, judging criteria, prizes, eligibility, team size, deadline with timezone, submission requirements (repo, video length, writeup), FAQ. Quote rubric lines word for word; they become design rules. Log anything you cannot read (a login-gated form, a 404) as a gap. Never guess it.

## Map the organiser, the judges and past winners
- **Organiser:** past events in the series, and whether this event has prior winners.
- **Sponsor goals:** what the sponsor wants showcased. Read its site, recent blog posts, docs and launches.
- **Judges:** names, roles, employers, talks and posts. If they are unnamed, record the gap and assume a profile (for example, engineers who skim fast).
- **Past winners:** list winners and non-winners from this organiser. Compare their repos, READMEs and demo videos. Break the best winning video down second by second and map each beat to a criterion.
- **Social proof:** search X, Reddit, YouTube, LinkedIn and winners' write-ups for why teams won or lost. Use connectors first.

Write it all into `WINNING_PLAYBOOK.md` with citations. Then red-team it: check every citation, add missing links, mark unverified items.

## Event type and medium
**Event type** changes what is judged:
- **Open hackathon:** the video and live link carry most of the score.
- **Take-home or hiring challenge:** the repo is read closely, then reviewers question you. Code clarity, tests, a decision log and your defence of it outweigh video polish. Move video and form time to these.
- **Sponsor challenge:** the sponsor's tech must do visible, irreplaceable work.

**Medium and craft.** Name what the entry is made of (an app, a game, a 3D scene, hardware, a model, content, research). Then research, with sources:
- what the best work in this craft does that average work does not (for example game feel and the first minute of play, or the hook in the first seconds of a post);
- the tools and pipelines practitioners use, and which of them an agent can script (a 3D suite's Python API, a headless game-engine export, platform analytics and trend research);
- where judges and audiences of this craft look first.

Later phases apply their principles through this lens.

## Fields to fill (template in templates.md)
| Field | Why it matters later |
|---|---|
| Event type, medium, craft notes and tools | Which phases get more time; which tools to install in setup |
| Criteria, their wording, and estimated weights | Proxy score for every re-score; what the video must show |
| Required artifacts: video (limit, host, visibility), repo (public? when?), live link, writeup fields, slides | Phase 8 checklist; the format limits under hard rule 4 |
| Tech requirements: must use X; must be open source (which licences); offline or self-hostable; banned services; credits provided | **Sets the stack.** Overrides every default in build.md |
| Repo rules: history must start after kickoff? all files visible? team commits? | Decides how to keep strategy notes private, and the commit habit |
| Deadline with timezone, feature-stop time, and your own early-submit time | Time budget |
| Judges: who they are (engineers, designers, domain experts, sponsor staff) | Tone, depth of tech shown, what impresses |
| What the sponsor wants showcased | Which tech must do visible work in the video |
| Eligibility and per-member requirements (student proof, resumes, side-prize forms) | Nothing lost at submission time |
| Point-loss and disqualification lines | Never-break list |
| Side prizes (blog, best UI, community vote) | Optional extra time only if the core is safe |

## Derive the stack from the profile
Write a short "stack constraints" block: what is required, what is allowed, what is banned. Examples:
- "Must use the sponsor's cloud and show it" → sponsor services do real jobs and each has a video moment.
- "Open source only, judges run it locally" → reproducible local setup (one command), OSI licences, no paid APIs in the core path, local or open models.
- "No live link required" → put the deploy effort into the video and the repo instead.
- "Repo must show all files" → no private strategy repo; keep notes short, professional and safe to show.

## Proxy score
Turn the criteria into a /30 (or similar) scorecard with estimated weights. Note where each weight came from (published, inferred from past winners, or a guess). Set a target score from known placing and non-placing entries. Re-score after every major change.

## Done means
The profile fits on one page. Every later phase can answer "is this allowed, and does it score?" by reading it. `WINNING_PLAYBOOK.md` holds the organiser, judge and winner research with checked citations, and the proxy score has a target.
