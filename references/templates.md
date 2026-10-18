# Templates

Copy into the project and fill in. Delete rows that do not apply.

## Contents
- Winning playbook and idea shortlist (`WINNING_PLAYBOOK.md`)
- Event profile (`JUDGING.md`)
- FACTS.md
- Story and script table (`STORY.md`)
- Claims sheet
- README skeleton
- Who did what block
- Form answer skeletons
- Memory files (`AGENTS.md`, `PROGRESS.md`, `LEARNINGS.md`)
- Task file
- Auditor prompt
- Thread handoff prompt

## Winning playbook and idea shortlist (`WINNING_PLAYBOOK.md`)
```markdown
# <Event>: how it is won (read <date>)
## Organiser and sponsor
Past events: <...>. Sponsor wants showcased: <...> (source)
## Judges
| Name | Role, employer | What they post or talk about | Source |
Gaps: <unnamed judges, assumed profile>
## Past winners vs non-winners
| Entry | Placed? | What it did | Video beats → criteria | Repo/README notes | Source |
## Why teams win or lose (social proof)
- <claim> (source, verified Y/N)

## Constraints
Team: <...>. Data: <...>. Conflict check: <done / n.a.>

## Shortlist
| Idea | Exact problem | Who, how many | Recency evidence | Closest prior art, our difference | Data source | Rubric fit | Sponsor-removal result | Agent decisions (≥3) | ICP | Demand (pain / moment / beats habit) | Kill test (pass/fail, numbers) | Score | Citations |

## Lock
Locked: <idea>, ICP: <group>, score <n>/30.
Runner-up lost because: <...>
Fallback: <idea>
Day-1 go/no-go gate: <pass/fail test> by <time>
```

## Event profile (`JUDGING.md`)
```markdown
# <Event>: profile (read <date>)
Sources: <event page> · <rules> · <FAQ> · <form> · <announcements>
Gaps (could not read): <...>

## Deadline
Submission: <date time TZ>. Feature stop: <time>. Our early submit: <time>.

## Criteria (quoted) and estimated weights
| Criterion | Exact wording | Weight (source: published / inferred / guess) | What must be on screen |

## Required artifacts
Video: <limit, host, visibility, required topics>. Repo: <public when? all files?>. Live link: <yes/no, signed out>. Form fields: <list>.

## Stack constraints
Required: <...>. Allowed: <...>. Banned: <...>. Sponsor wants shown: <...>.

## Judges
<who, background, what they posted about judging>

## Never break (disqualification / point loss)
- <...>

## Proxy score
Target: <n>/30. Current: <n>/30, biggest gap: <...> (dated)
```

## FACTS.md
```markdown
# Facts (only these, or live data, may appear in UI, README, form, video)
| Fact (exact wording to use) | Number | Source URL | Read on | Notes (scope, tense, place) |

## Never claim
| Do not say | Why | Say instead |
| "violated", "failed", "illegal" | data shows promises, not breaches | "promised in writing" |

## Changed numbers log
| Date | What changed | Old → new | Updated in (README/video/form/site) |
```

## Story and script table (`STORY.md`)
```markdown
Throughline (≤15 words): <...>
And / But / Therefore: <...>
Lead user, decision, action: <...>
Word budget: <limit − 10 s> × 2.3 = <n> words. Current: <n>.

| # | Time | Voice line | On screen | Motion lands on word | Sound | Source / fact | Status (new/edited/same) |
```

## Claims sheet
```markdown
| Claim | Where (file, timestamp, field) | Source | Number ok | Tense ok | Place ok | Picture ok | Checked by eye | Action |
```

## README skeleton
```markdown
# <Name>: <what it does, for whom, with the track's key phrase>
**Video:** <link> · **Live:** <link> (no sign-in) · <track>
![<alt>](assets/hero.jpg)

## Try it in 30 seconds
- <direct link 1>: <what you see>

## The problem
- <fact> ([source](...))

## Who uses it, and what changes
| Person | Decision | What the product gives them |

## Proof numbers (as of <run, date>)
## How we used <sponsor tech>
| Service | Job | Why this service | In the video |
## Architecture
## How the AI is checked / when it is unsure
## Run it yourself
## What is not built
## What's next
## Team: who did what
## What we learned
## Feedback on <sponsor> tools
## AI tools used
## Credits and licences
```

## Who did what block
```markdown
**<Name> (@handle): <area, e.g. the build / the problem and the look / the product and its outcome>.**
<Owned: 1–2 sentences.> <Decisions that shaped it: 1–2 concrete ones.> <Where it shows: screens, files, moments.>
```

## Form answer skeletons
- **What does it do / who is it for:** problem with 2–3 sourced numbers → what the product does (one example output) → each user and their action → how it handles doubt → live link.
- **How did you use <sponsor>:** open-source tools used (names) → services used, one line each: what job, with one real number → the cost of the event.
- **What did you like:** per service, one specific thing that worked, with a number.
- **What could be better:** per service, what worked, plus one specific, constructive suggestion.
- **Team contributions:** reuse the who-did-what blocks; add 3–5 concrete deliverables each.

## Memory files (see memory.md)

`AGENTS.md` (≤150 lines, gitignored)
```markdown
# AGENTS.md: <project> for <event>
Read this, then the Now block in PROGRESS.md, then `git log --oneline -10`, then LEARNINGS.md.

## Situation (30 seconds)
- What: <one line>. Track: <name>. Deadline: <date, time, timezone>.
- Owner: <names>. Repo: <url> (<private/public>). Live: <url>.
## Hard rules
1. <the official rules that bind this work, quoted>
2. Commit author <name, email>; no AI co-author lines unless the owner says so.
3. Ask the owner before: public changes, submission, spend, deletes, history rewrites.
## How the product works
<5–15 lines: data flow, where the decision is made, the key query or algorithm>
## Run, test, deploy
<exact commands; where secrets live (never the values)>
## Roles
Planner: <model/tool>. Executors: <model/tool>. Auditor: <model/tool>.
## Pointers
FACTS.md · PROGRESS.md · LEARNINGS.md · tasks/ · <research folder>
```

`PROGRESS.md`
```markdown
# PROGRESS.md
## Now (rewritten <date time tz>, <hours> h to deadline)
- Done since last session: <item → evidence>
- Running: <job → log path, expected end>
- Blocked: <item → what unblocks it, who>
- Next: <ordered list, max 5>
- Live: <deploy id / version>, CI <green/red> on <commit>
## Log (newest first)
- <date time> <what> → <evidence>
```

`LEARNINGS.md`
```markdown
# LEARNINGS.md
<!-- One line each: what happened → do this instead → evidence. Mark [promote] if it helps every hackathon. -->
- <what happened> → <do this instead> → <commit, log or URL> [promote]
```

## Task file (`tasks/<id>.md`)
```markdown
# <id>: <goal a stranger can check>
Worktree: ../<repo>-<id> on branch <id>. Time limit: <minutes>.
Read first: AGENTS.md, <files>.
May change: <paths>. Must not change: <paths>.
Do: <numbered steps, one action each>
Acceptance (all must pass):
- `<command>` → <expected result>
Test command: `<full suite command>`
Report: commit hashes, test output tail, what you did not do and why.
Do not: push to main, deploy, change visibility, add co-author lines.
```

## Auditor prompt (fresh context, see verify.md)
```text
You are an independent, skeptical auditor of <project> for <event>. Trust no claim until you reproduce it.
Read: the official rules <url>, AGENTS.md, FACTS.md, the README, the live URL <url>.
1. Reproduce every claim in the README, the UI and the video script. Mark each true, false or unverified, with the command or URL you used.
2. Try to break the product with adversarial inputs a judge might use. List each wrong result.
3. Score the entry on <rubric, e.g. 6 dimensions × 5 = 30>. Give one line of evidence per score.
4. List CRITICAL problems first (wrong output, false claim, leaked secret or personal data, broken required artifact), then the single biggest gap to fix next.
Do not fix anything. Write the report to AUDIT<n>.md.
```

## Thread handoff prompt (paste into a new thread)
```text
Continue <project> for <event>. Deadline <date time tz>.
Before anything else: read AGENTS.md, the Now block in PROGRESS.md, `git log --oneline -10`, and LEARNINGS.md. Then check live state (deploy, CI, running jobs) against the Now block and tell me any difference.
Your role: <planner/executor>. Next task: <one line or tasks/<id>.md>.
Write status in about 80% ASD-STE100: short sentences, one fact each, with evidence.
```
