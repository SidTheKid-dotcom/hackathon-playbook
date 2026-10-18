# Orchestration: one planner, many executor agents

Goal: get more done in the time box without losing control of quality, cost or the repo. Use this when more than one agent works on the event, or when work runs while the user sleeps.

## Roles (by job, not by model)
| Role | Does | Does not |
|---|---|---|
| Planner (orchestrator) | Reads the memory files, picks the next gap from the proxy score, writes task files, reviews results, merges, updates `PROGRESS.md` | Write large amounts of code itself; trust an executor's "done" without evidence |
| Executor | Does one task from a task file in its own worktree, runs the test command, commits, reports evidence | Choose scope, push to main, deploy, change the public state |
| Auditor | Reviews the whole entry with a fresh context and a fixed rubric (see verify.md) | Fix things; it only reports |

Give each role to the model that is best at it **for this event**, and write the choice in `AGENTS.md`. Models and limits change; roles do not. When a provider limit is near, move the role to another model and keep working. Do not stop the event.

## Task files
One file for each task, in a gitignored `tasks/` folder. Use the template in templates.md. Each task has:
- one goal a stranger can check;
- acceptance criteria as commands with an expected result;
- the test command;
- files it may touch and files it must not touch;
- a time limit.

Size: one task fits in one agent session. If it does not, split it.

## Parallel work
- One git worktree per parallel task (`git worktree add ../<repo>-<task> -b <task>`). Executors never share a checkout.
- The planner merges a task only when its test command passes on the merged result. Then it removes the worktree.
- Two tasks that change the same file do not run at the same time.
- Run tasks in a queue with `scripts/run_tasks.sh`: it runs each task file through an agent CLI, retries once on a timeout, and logs commits for each task.

## Long jobs (renders, full test suites, deploys, data runs)
A job started inside an agent's tool call can stop when that call ends. Some tools cancel themselves when their parent process exits.
- Start long jobs as detached processes: `systemd-run --user --unit=<name> ...` or `setsid nohup ... &`. Set the tool's own detach option if it has one.
- Write the output to a log file. Check it with short polls, not one long wait.
- Before you buy more compute, find where the time goes. A job that "is slow" is often a job that was cancelled and restarted.

## Unattended work (overnight, user away)
Allowed: tasks from the queue, tests, merges that pass tests, `PROGRESS.md` updates, research.
Not allowed without the user: public visibility changes, submissions, deploys of code the planner has not reviewed, new paid resources or higher spend caps, history rewrites, deleting anything outside the work tree.

Before the user leaves, write the plan for the night in `PROGRESS.md`. Schedule a check every 1–2 hours. Each check reads the logs, merges finished tasks, starts the next tasks, and rewrites the Now block.

## Review discipline
- Ask for evidence: test output, a screenshot, a live URL, a commit hash. "Done" without evidence is not done.
- Run the **full** test suite before every push. CI runs everything; a subset that passes locally can still turn the public repo red.
- After a batch of merges, run the regression sweep (verify.md) on the live URL.
- Check commit authorship before each push (see setup.md). Executors can add their own author or co-author lines.

## Done means
Every task is merged with evidence or written down as dropped. No worktree holds unmerged work. `PROGRESS.md` says what runs, what is blocked and what is next.
