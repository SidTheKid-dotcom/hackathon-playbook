# hackathon-playbook

An agent skill for any build that someone judges: hackathons, game jams, content and creative challenges, and take-home assignments. It takes an AI coding agent from the event page to a submission it can defend.

It gives the agent a direction, a structure and a working philosophy, not a script:
- **Win on the criteria.** Decode the rules, judges and past winners first. Then every hour moves a judging criterion.
- **Adapt to the medium.** The agent finds out what entries in this event are made of (an app, a game, 3D, hardware, content, research), how the best work in that craft wins, and which tools it uses.
- **Never fake anything.** Every number traces to a source. There is no mock data in the demo.
- **Show evidence, not "done".** Tests that can fail, screenshots, measured numbers, live links.
- **Defaults, not cages.** Every step has a reason. The agent scales the process to the request and the time left. Only seven hard rules never bend.

## Set up with your agent

Copy and paste this into your agent:

```text
Read https://raw.githubusercontent.com/SidTheKid-dotcom/hackathon-playbook/main/INSTALL.md and follow it to install the hackathon-playbook skill for me. Reuse an existing install if there is one, verify it loaded, then ask me for my event link.
```

Works with Claude Code, Cursor, Codex, OpenCode and other agents with a terminal. Prefer doing it yourself? See Install below.

## Install

With the [skills CLI](https://github.com/vercel-labs/skills), for Claude Code, Codex, Cursor and other agents:
```bash
npx skills add SidTheKid-dotcom/hackathon-playbook
```

Or by hand. Clone it into your agent's skills folder:
```bash
git clone https://github.com/SidTheKid-dotcom/hackathon-playbook ~/.claude/skills/hackathon-playbook   # Claude Code
git clone https://github.com/SidTheKid-dotcom/hackathon-playbook ~/.agents/skills/hackathon-playbook   # agents that read ~/.agents/skills
```

## Use

Talk to your agent normally. The skill triggers on requests like these:
- "Help me win this hackathon: <event link>"
- "Research the judges and past winners"
- "Score and kill-test our idea"
- "Idea is locked. What now?"
- "Plan the demo video" / "Audit the video before we submit"
- "Prep me for the take-home review"
- "Are we ready to submit?"

The agent reads `SKILL.md`, finds the current phase, and loads only that phase's reference file.

## What is inside

| Phase | File | Goal |
|---|---|---|
| 0 Decode the game | `references/event-profile.md` | Rules, judges, past winners, the medium and its craft become constraints |
| 1 Ideas and lock | `references/ideas.md` | One unique, felt, buildable idea, with a fallback |
| 2 Setup | `references/setup.md` | Repo, facts file, spikes on the riskiest unknowns |
| 3 Scope | `references/scope.md` | One user, one decision, one action |
| 4 Build | `references/build.md` | One real flow end to end, then depth |
| 5 UI and experience | `references/ui.md` | Clear at first glance, works everywhere |
| 6 Verify | `references/verify.md` | Nothing false, nothing broken |
| 7 Video | `references/video.md` | The story the judges score |
| 8 Submit, defend, freeze | `references/submit.md` | Complete, consistent, early, and defensible |

Also included:
- `references/memory.md`: memory files that let any agent pick up the work in a new thread.
- `references/orchestration.md`: one planner, many executor agents, and an auditor.
- `references/templates.md`: event profile, `FACTS.md`, `DECISIONS.md`, README skeleton, task file and auditor prompt.
- `references/worked-example.md`: one complete run. It is an example, not a template.

## Optional scripts

They work with any product stack. Each one has usage notes in its header.

| Script | Does | Needs |
|---|---|---|
| `scripts/secret_scan.sh` | Scans history, commit messages and tracked files for keys, risky files, personal emails and your own private terms (`DENY_TERMS`) before a repo goes public | git, bash |
| `scripts/ui_audit.mjs` | Checks a web UI across routes, widths and languages: sideways scroll, clipped text, overlaps, small tap targets, console errors | Node 18+, Playwright |
| `scripts/contact_sheet.py` | Puts screenshots or video frames into one labelled grid, for review by eye | Python 3, Pillow |
| `scripts/run_tasks.sh` | Runs task files in order through any agent CLI, one git worktree each | git, an agent CLI |
| `scripts/video/` | A voice-first demo-video kit: word-timed HTML composition, render, mix, captions, audits | ffmpeg, Node, Python; see its README |

## Related

The "Defend it" step can use a grilling skill (one that questions you on each decision), if you have one installed. Without one, the agent runs the same rehearsal from the instructions in `references/submit.md`.

## Contributing

Issues and pull requests are welcome. A good addition is a lesson that helps every future event. Write it as `what happened → do this instead → why`, and leave out product names. Keep `SKILL.md` short: put detail in the phase's reference file.

## License

[MIT](LICENSE)
