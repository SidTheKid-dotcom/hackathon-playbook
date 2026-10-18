# Memory and handoff: work across threads, sessions and agents

Goal: any agent, in any new thread, picks up the work in under two minutes. No one thread has to carry the whole event.

A new session starts with no memory. Compaction keeps one thread alive, but it loses detail and the agent gets less precise as the context fills. A clean new thread plus a short, structured handoff is more reliable. These files are that handoff.

## The files (in the project, gitignored, created on day 1)
| File | Read | Holds | Size |
|---|---|---|---|
| `AGENTS.md` | Every session, first | Stable truth: the situation in 30 seconds, hard rules, how the product works, how to run, test and deploy, where other files are | ≤150 lines. Put detail in linked files |
| `PROGRESS.md` | Every session, second | A **Now** block (done, running, blocked, next, time to deadline), rewritten each session. Below it, a dated log, newest first | Now block ≤20 lines. Archive the log when it passes about 300 lines |
| `LEARNINGS.md` | Every session, third | One line per lesson: what happened → what to do instead → evidence | Prune each day. Delete what is wrong or no longer true |
| `FACTS.md` | When writing copy | Verified facts and the never-claim list (see setup.md) | — |

Keep these four files separate. `AGENTS.md` changes rarely; `PROGRESS.md` changes every session. A file that mixes both gets long, and long always-loaded files get ignored. Agents follow fewer instructions as a file grows, and they discount a file that is mostly irrelevant to the current task.

If the agent tool also loads its own memory file (for example a `MEMORY.md` index or `CLAUDE.md`), point it at `AGENTS.md` with one line. Do not copy the content into a second place.

Not every tool reads user-level settings. Another vendor's coding agent sees only the repo. Put every rule the work needs in `AGENTS.md`.

## Session start (do this before any other step)
1. Read `AGENTS.md`.
2. Read the Now block in `PROGRESS.md`.
3. Run `git log --oneline -10` and `git status`.
4. Read `LEARNINGS.md`.
5. Check that the live state matches the files: is the deploy, the CI result, or the running job what the Now block says? If not, fix the file first.

## Session end, or before the context gets heavy
1. Rewrite the Now block in `PROGRESS.md`. Add one dated log line for each thing done, with its evidence (commit, URL, command output).
2. Add each new lesson to `LEARNINGS.md`.
3. Update `AGENTS.md` only if a stable fact changed (an architecture change, a new deploy target, a rule from the user).
4. Commit or note uncommitted work. Never leave a half-done change undocumented.
5. Start a new thread with the handoff prompt in templates.md.

Switch threads when one of these is true: the thread has run for many hours, the agent repeats a solved mistake, it forgets a rule, or a provider limit is near. Do not wait for an automatic compaction.

## Status questions
When the user asks "status?", answer from the Now block, then check it against live state. Keep the Now block current, so status is a read, not an investigation.

## Learnings: the compounding loop
- Write a lesson when something costs time, breaks, or surprises. Use the form: `what happened → do this instead → evidence`.
- A lesson without a "do this instead" is a diary entry. Cut it.
- At the end of the event, read `LEARNINGS.md` once more. Promote each lesson that will help **every** future hackathon into this skill (a gotcha, a checklist line or a reference). Leave event-specific lessons in the project.
- Before you promote, remove product names, model names and vendor names. Keep the principle.

## Writing standard for these files
Write agent-facing files and status reports at about 80% of ASD-STE100 Simplified Technical English:
- One fact or one instruction in each sentence.
- Active voice. Present tense for current state.
- One word for one thing. Do not change the term in the next line.
- Numbers with their unit and date. Paths and commands in code format.
- No filler and no hedges. If a fact is unknown, write "unknown".

Full ASD-STE100 is too stiff for the README, the form and video narration. Write those plainly and factually, without sales language.
