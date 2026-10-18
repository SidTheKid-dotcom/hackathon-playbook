#!/usr/bin/env bash
# Scan a git repo (all history + tracked files) for secrets and for files that should stay private,
# before making it public. Uses gitleaks if installed; always runs a pattern scan too.
# Usage: bash secret_scan.sh [repo_dir] [extra private path patterns, e.g. "CLAUDE.md docs/ .agents/"]
# EMAIL_ALLOW='regex' overrides the list of email addresses that are allowed in tracked files.
# Exit code 1 if anything is found.
set -uo pipefail
REPO="${1:-.}"; shift || true
PRIVATE="${*:-CLAUDE.md AGENTS.md .claude/ .agents/}"
cd "$REPO" || { echo "no such repo: $REPO"; exit 2; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repo: $REPO"; exit 2; }
found=0

if command -v gitleaks >/dev/null 2>&1; then
  echo "== gitleaks (full history)"
  gitleaks detect --source . --no-banner --redact || found=1
fi

echo "== pattern scan over all history ($(git rev-list --all --count) commits)"
PAT='AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|aws_secret_access_key[[:space:]]*[:=]|-----BEGIN [A-Z ]*PRIVATE KEY-----|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}|xox[baprs]-[A-Za-z0-9-]{10,}|sk-[A-Za-z0-9_-]{32,}|sk_live_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJhbGciOi[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'
hits=$(git log --all -p --no-color 2>/dev/null | grep -nE "$PAT" | grep -vE '^[0-9]+:[-+]?\s*#' | head -20)
if [ -n "$hits" ]; then
  echo "$hits" | perl -pe 's/((?:AKIA|ASIA|ghp_|github_pat_|xox[baprs]-|sk_live_|sk-|AIza|eyJhbGciOi|PRIVATE KEY)[A-Za-z0-9_-]{0,2})[A-Za-z0-9_\/+=.-]{4,}/$1…[redacted]/g; s/(aws_secret_access_key\s*[:=]\s*["\x27]?)\S+/$1…[redacted]/g' | cut -c1-160
  echo "  ^ check each hit: test dummies (e.g. \"test\") are fine, real keys must be rotated, not just deleted"
  found=1
else
  echo "  no key patterns found"
fi

echo "== personal emails in tracked files (git author emails are not checked here)"
EMAIL_RE='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
ALLOW_RE="${EMAIL_ALLOW:-noreply|no-reply|example\.(com|org|net)|@users\.noreply\.github\.com|@localhost|@test\.|@sentry|@anthropic\.com}"
emails=$(git grep -I -h -oE "$EMAIL_RE" -- . ':!*.lock' ':!package-lock.json' 2>/dev/null | grep -viE "$ALLOW_RE" | grep -vE '@[0-9]+\.[0-9]+' | sort | uniq -c | sort -rn | head -15)
if [ -n "$emails" ]; then
  echo "$emails"
  echo "  ^ personal addresses go public with the repo; replace them, or allow with EMAIL_ALLOW='regex'"
  found=1
else
  echo "  none"
fi

echo "== risky tracked files"
risky=$(git ls-files | grep -E '(^|/)(\.env(\..*)?|.*\.pem|.*\.p12|id_rsa.*|.*\.key|credentials(\.json)?|service-account.*\.json)$' | grep -vE '\.env\.example$')
if [ -n "$risky" ]; then echo "$risky"; found=1; else echo "  none"; fi

echo "== private paths that must not be tracked: $PRIVATE"
for p in $PRIVATE; do
  t=$(git ls-files -- "$p" | head -5)
  if [ -n "$t" ]; then echo "  TRACKED: $t"; found=1; fi
  h=$(git log --all --format=%h --diff-filter=A -- "$p" | head -3)
  if [ -n "$h" ]; then echo "  in history (commits $h): $p"; found=1; fi
done
[ $found -eq 0 ] && echo "RESULT: clean" || echo "RESULT: review the items above before going public"
exit $found
