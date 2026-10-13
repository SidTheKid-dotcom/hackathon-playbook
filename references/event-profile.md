# Phase 0: Event profile

Goal: one page in the project (`JUDGING.md` or `EVENT.md`) that every later decision reads. It turns the rules into constraints and sets the stack, so this skill's defaults never fight the event.

## Read these sources, and quote them
- Event page, rules, FAQ, schedule, the submission form's actual fields, and the judging criteria.
- Organiser announcements (blog, Discord, email). **Deadlines and rules change mid-event**; re-check them on the last day.
- Sponsor material: what the sponsor wants showcased, the build guides it published, and its judges' public posts.
- If `hackathon-win-playbook` already produced `WINNING_PLAYBOOK.md`, copy the relevant parts from it. Do not research twice.

Quote rubric lines word for word. Log anything you cannot read (a login-gated form, a 404) as a gap. Never guess it.

## Fields to fill (template in templates.md)
| Field | Why it matters later |
|---|---|
| Criteria, their wording, and estimated weights | Proxy score for every re-score; what the video must show |
| Required artifacts: video (limit, host, visibility), repo (public? when?), live link, writeup fields, slides | Phase 7 checklist; the format limits under hard rule 4 |
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
The profile fits on one page. Every later phase can answer "is this allowed, and does it score?" by reading it.
