#!/usr/bin/env bash
# Run task files in order through any agent CLI, each in its own git worktree.
# One retry on timeout or failure (the retry is told to resume, not restart). Logs commits per task.
# The planner reviews and merges afterwards; this script never pushes, merges or deploys.
#
# Usage: AGENT_CMD='<agent cli that reads the prompt from $PROMPT_FILE>' bash run_tasks.sh <repo_dir> <tasks_dir> <task-id>...
#   AGENT_CMD examples (adapt to your tools):
#     'claude -p "$(cat "$PROMPT_FILE")" --permission-mode acceptEdits'
#     'cursor-agent -p -f "$(cat "$PROMPT_FILE")"'
#   Optional: TIMEOUT_S (default 3000; or a <task-id>.tmo file with seconds), BASE (branch to start from, default HEAD).
# Output: <tasks_dir>/logs/<id>_a<attempt>.log and one line per attempt in <tasks_dir>/pipeline.log
set -uo pipefail
REPO=$(cd "${1:?repo dir}" && pwd); TASKS=$(cd "${2:?tasks dir}" && pwd); shift 2
[ $# -gt 0 ] || { echo "give at least one task id (tasks/<id>.md)"; exit 2; }
: "${AGENT_CMD:?set AGENT_CMD, see the header}"
BASE=${BASE:-HEAD}; mkdir -p "$TASKS/logs"
log() { echo "[$(date '+%a %d %H:%M %Z')] $*" | tee -a "$TASKS/pipeline.log"; }

for id in "$@"; do
  task="$TASKS/$id.md"; [ -f "$task" ] || { log "$id: missing $task, skipped"; continue; }
  wt="$(dirname "$REPO")/$(basename "$REPO")-$id"
  if [ ! -d "$wt" ]; then git -C "$REPO" worktree add -q -b "$id" "$wt" "$BASE" || { log "$id: worktree failed"; continue; }; fi
  tmo=$(cat "$TASKS/$id.tmo" 2>/dev/null || echo "${TIMEOUT_S:-3000}")
  for attempt in 1 2; do
    before=$(git -C "$wt" rev-parse HEAD)
    PROMPT_FILE=$(mktemp); cp "$task" "$PROMPT_FILE"
    if [ "$attempt" = 2 ]; then printf '\n\nRESUME NOTE: an earlier attempt timed out or failed. Read git log, git status and PROGRESS.md in this worktree, keep correct work, and finish the task.\n' >> "$PROMPT_FILE"; fi
    log "$id: start attempt $attempt in $wt (timeout ${tmo}s)"
    (cd "$wt" && PROMPT_FILE="$PROMPT_FILE" timeout "$tmo" bash -c "$AGENT_CMD") > "$TASKS/logs/${id}_a$attempt.log" 2>&1; rc=$?
    rm -f "$PROMPT_FILE"
    after=$(git -C "$wt" rev-parse HEAD)
    commits=$(git -C "$wt" rev-list --count "$before..$after"); dirty=$(git -C "$wt" status --porcelain | grep -vc '^??')
    log "$id: end attempt $attempt rc=$rc commits=$commits uncommitted=$dirty"
    [ "$rc" = 0 ] && break
  done
done
log "queue done: $*  (review each worktree, run the full tests, then merge)"
