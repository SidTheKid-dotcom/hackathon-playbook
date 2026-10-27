# Council: independent reviewers at three decisions

Goal: catch a weak idea, a flat demo or a missing "whoa" before it costs the event. Several reviewers judge the same artifact against the proxy rubric, alone. A chair merges their reviews. The council advises; the user makes the final call.

Why: at recent events, strong ideas ended as entries whose build and demo had no wow factor. One reviewer misses what three independent reviewers catch.

## When to run it
Run it only at these three points. Skip it, with a reason, when the time box is short (a 2-hour jam needs one wow check at most).
1. **Idea lock council** (ideas.md, Step 10). Input: the top 2–3 finalists and the proxy rubric.
2. **Judge panel** (video.md, change rounds). Input: the script or the current cut.
3. **Wow check before feature stop** (wow-factor.md, gate). Input: the winning moment, screenshots and the current build.

The council is not a code review. Code goes through the auditor in orchestration.md.

## Protocol
- Give each reviewer the same artifact, the proxy rubric and `FACTS.md`. Give no reviewer the others' output.
- Each reviewer plays one persona. Use one call per reviewer.
- The chair merges the reviews into agreements, disagreements and a verdict. The chair adds no new ideas.
- Save the raw reviews and the verdict in `council/<point>/` in the user's project.
- Treat the verdict as outside input on evidence (SKILL.md loop). A real ICP member or a real judge outranks the council.

## Personas
| Persona | Asks |
|---|---|
| Technical judge | Does it really work? What looks faked? Is the hard part on screen? |
| Impact judge | Who uses it, and do they feel the problem? Is every number sourced? |
| Sponsor and track judge | Is the sponsor tech shown and needed? Does it fit the track? |

## Prompts
Common header for every reviewer:
```text
You are the <persona> on a review council. Work alone. Score only against this rubric: <rubric>.
Cite the artifact for every point. Mark any claim that FACTS.md does not support. Do not soften.
```
Idea lock council, added:
```text
Score each idea 1–10 per criterion. Pick the idea you like least and argue against it in 3 points.
Name the biggest risk of the idea you rank first.
```
Judge panel, added:
```text
Score the script or cut 1–10 per criterion. Give the timestamp where your attention dropped.
Give the one line you remember, and the first question you would ask the team.
```
Wow check, added:
```text
What would make a judge say "whoa"? List up to 3 changes that use what already exists. No new features.
```
Chair:
```text
Merge these reviews. Write: Agreements (points from 2 or more reviewers), Disagreements (each side),
Verdict (one recommendation with its reason), Polish list (wow check only: items flagged by 2 or more).
Quote the reviewers. Add no ideas of your own.
```
After the feature stop, the polish list may only make existing depth visible (scope.md).

## Runtimes
Use the first one that is available.
1. **T3 Code MCP (preferred).** Use this route only if the T3 Code thread tools (`t3_thread_launch` and friends) are in your tool list. Your harness may prefix them, for example `mcp__t3__t3_thread_launch` or `mcp_t3_t3_thread_launch`. Otherwise go straight to route 2. The chair agent (here, Claude Code) calls the T3 Code MCP tools once per reviewer, in parallel: `t3_thread_launch` with `scratch: true`, `runtimeMode: "approval-required"`, `modelSelection: {instanceId, model}` and the reviewer prompt as `message`; then `t3_thread_wait` (`timeoutMs` 180000) and `t3_thread_read`. Each reviewer thread sees only its prompt. If one reviewer fails, merge the others and say so. Never grant full access; the reviewers only read. Sources: [outside agents](https://github.com/pingdotgg/t3code/blob/main/docs/user/outside-agents.md), [orchestrator MCP server](https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/orchestrator-mcp-server.md).
   Headless start, from a shell on the T3 host:
   ```sh
   claude -p '<chair prompt: launch the 3 reviewers above, wait, read, then merge>' --allowedTools "mcp__t3__*"
   ```
2. **Single agent (no T3 Code, or one vendor only).** Start one fresh-context subagent per persona, in parallel, then chair the result yourself. If your agent cannot start subagents, run each persona one after another in a fresh context. If your harness can set a model per subagent (for example, oh-my-pi), give each persona a different model to cut correlated errors. If all reviewers share one model, write this in the verdict: "All reviewers share one model. Their errors are correlated, so agreement is weak evidence."

Reviewers from different vendors make errors that are less correlated. That is the reason to prefer runtime 1.

Default lineup. These are configurable examples; confirm each instance id and model slug in your T3 Code provider list.
| Role | `instanceId` | `model` |
|---|---|---|
| Chair | `claudeAgent` | `claude-opus-5-5` |
| Technical judge | `opencode` | `azure/gpt-5.6-sol` |
| Impact judge | `opencode` | `opencode/deepseek-v4.1-flash-free` |
| Sponsor and track judge | `cursor` | `grok-4.7` |

## Done means
The verdict file exists, or a one-line reason says why the council was skipped. The user has decided.
