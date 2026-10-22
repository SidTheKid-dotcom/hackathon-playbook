# Install hackathon-playbook (instructions for an AI agent)

The user asked you to install this skill. Follow these steps in order. Run commands yourself; ask the user only where a step says so.

Repo: https://github.com/SidTheKid-dotcom/hackathon-playbook

## 1. Check for an existing install
Look for `hackathon-playbook/SKILL.md` in your skills folders (for example `~/.claude/skills/`, `~/.agents/skills/`, or `.claude/skills/` / `.agents/skills/` in the current project). You can also run `npx skills ls` and `npx skills ls -g`.
- **Found, installed with the skills CLI:** run `npx skills update hackathon-playbook -y`, then go to step 4.
- **Found, a git clone:** run `git -C <path> pull --ff-only`, then go to step 4.
- **Not found:** continue.

## 2. Ask the user one question
"Install for this project only, or globally for all your projects?"

## 3. Install
**With Node 22.20 or newer** (check with `node --version`):
```bash
npx skills add SidTheKid-dotcom/hackathon-playbook -y        # this project
npx skills add SidTheKid-dotcom/hackathon-playbook -g -y     # global
```
If the CLI asks which agents to install for, choose the one you are.

**Without Node 22.20+**, clone into your skills folder:
```bash
git clone https://github.com/SidTheKid-dotcom/hackathon-playbook ~/.claude/skills/hackathon-playbook   # Claude Code, global
git clone https://github.com/SidTheKid-dotcom/hackathon-playbook ~/.agents/skills/hackathon-playbook   # agents that read ~/.agents/skills
```
For a project install, clone into the project's skills folder instead. Never delete an existing folder to reinstall.

## 4. Verify
- `SKILL.md` and `references/` exist in the installed folder.
- The skill is visible: it appears in `npx skills ls` (add `-g` for global) or in your skill list. If your agent loads skills only at session start, tell the user to start a new session.

If a check fails, report the exact error to the user. Do not claim success.

## 5. Report back
Tell the user where the skill is installed. Then give 2–3 example requests:
- "Help me win this hackathon: <event link>"
- "Score and kill-test our idea"
- "Are we ready to submit?"

End by asking for their event link.
