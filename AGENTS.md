# AGENTS.md: maintaining hackathon-playbook

Read this before you change the repo. It covers the philosophy, the writing standard and the checks. Users install the skill with `INSTALL.md`. This file is for maintainers only.

## What this repo is
- An agent skill. Agents load `SKILL.md` first. They load each `references/<phase>.md` file only when that phase starts.
- `SKILL.md` holds the philosophy, the 7 hard rules, the phase map, the gotchas and the "Don't skip" table. Detail goes in the phase's reference file.
- `scripts/` holds optional tools. They work with any product stack.
- Public on GitHub. Assume every line, commit message and file is read by strangers.

## Philosophy (keep it)
- **Direction, not a script.** Each step is a default with a reason. The agent scales the process to the request and the time left. It may skip or change a step if it says why.
- **Only the hard rules never bend.** Do not add a hard rule unless breaking it loses the event (disqualification, a false claim, a fake). Everything else is a default.
- **Weigh, not gate.** Write new tests as evidence to weigh. Allow "skipped, with a reason". A test that blocks progress on a judgement call makes the agent rigid.
- **Medium-neutral.** Apps, games, 3D, hardware, content and research all use this skill. Write the principle first. Web advice is one example of it, not the rule.
- **No overfitting.** Add a lesson only if it helps every future event. Remove product, event, sponsor and stack names. `references/worked-example.md` is the only named example.
- **Evidence over claims.** A change comes from a real failure: an event, a red-team run or a measured result. Never invent a lesson.

## Bar for a change
1. Name the failure it prevents, in one line: `what happened → do this instead → why`.
2. Check whether an existing line already covers it. Edit that line rather than adding a new one.
3. Put it in the right place: a phase rule goes in its reference file, a costly trap goes in Gotchas, and a tempting shortcut goes in "Don't skip".
4. Ask: does it make the agent more rigid, or does it slow a simple request? If yes, scope it ("when the idea's value is generated output") or drop it.
5. Keep the size flat. Each addition should replace or shorten something where it can. `SKILL.md` stays under about 150 lines.

## Writing standard
Write at about 80% of ASD-STE100 Simplified Technical English.
- One fact or one instruction per sentence. Sentences of about 20 words or fewer.
- Active voice. Use the imperative for steps ("Run the gate", not "The gate should be run").
- One word for one thing. Reuse the existing terms: judges, criteria, ICP, proxy score, kill test, fallback, go/no-go gate, feature stop, `FACTS.md`, memory files.
- Give the reason with the rule. A rule with a reason lets the agent judge edge cases.
- Use concrete examples and numbers, not adjectives. No filler, no sales words, no emoji.
- Keep the existing spelling and style: British spelling ("organiser", "licence"), sentence-case headings, en dash in ranges (2–3).

## Hard constraints
- The `SKILL.md` frontmatter `description` must stay at 1024 characters or fewer. It is now close to the limit. Trim it when you add a trigger.
- Bump `metadata.version` in `SKILL.md` when behaviour changes. Use minor versions for new or changed rules.
- If you add, rename or remove a file, update the tables in `README.md` and the links in `SKILL.md`.
- Keep `INSTALL.md` and the README install section consistent.
- Never add private information: names of people, employers, clients, take-home companies, private projects, local paths, personal emails or private links. This applies to files and to commit messages.

## Check before you commit
Run these from the repo root:
```bash
python3 - <<'PY'
import re;s=open('SKILL.md').read();d=re.search(r'description: >-\n(.*?)\nmetadata:',s,re.S).group(1)
print('description chars:',len(' '.join(d.split())))
PY
grep -oE '\]\(([^)#]+\.md)' SKILL.md README.md references/*.md | sed 's/.*](//' | grep -v '^https\?:' | sort -u | while read f; do [ -e "$f" ] || [ -e "references/$f" ] || echo "BROKEN LINK: $f"; done
bash -n scripts/*.sh scripts/video/*.sh && node --check scripts/ui_audit.mjs && python3 -m py_compile scripts/*.py scripts/video/*.py
DENY_TERMS='<private terms, | separated>' bash scripts/secret_scan.sh . ".claude/ .env"
```
- For a change to how the agent behaves, test it. Give a fresh-context agent the skill and one real or recent event. Compare its output before and after the change. Record what changed in the commit body.

## Git
- This checkout may be linked into `~/.agents/skills/hackathon-playbook`. If so, every edit is live for every agent on this machine at once. Use a git worktree for experiments.
- One idea per commit. Subject in the imperative, about 50 characters. The body lists the lessons and their source.
- Author and commit with the owner's GitHub noreply address, never a personal email. Add no `Co-Authored-By` trailers.
- Ask the owner before you push, rewrite history, change repo settings or delete files.
