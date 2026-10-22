# Phase 2: Setup

Goal: a clean start that cannot be disqualified, with the facts file and the riskiest unknown dealt with in the first hours.

## Repo and history
- Create the project repo after kickoff, if the rules care about dates. Exploration before kickoff (reading data, checking access) is usually allowed; keep that code out of the repo and write the project code fresh.
- Lean repo: only what is necessary. No project code before kickoff; commits spread across the event.
- Set the commit identity so each commit shows the right person and their avatar (for example the GitHub noreply address). Ask before adding any AI co-author line; many teams want none.
- Give teammates access early. Each member must be able to explain the part they own.
- Commit small, working steps often. Never rewrite or back-date history to look busier. A big commit is honest; a faked history is a risk.

## Strategy notes (plans, research, prompts, agent files)
Keep private agent docs out of the public repo via `.gitignore`. **Override when** the rules require every file to be public.
- The method depends on the rules. Options, simplest first:
  - local-only notes that are gitignored;
  - a private second repo, symlinked into the public checkout with gitignored link paths;
  - a `docs/` folder that is safe to publish.
- Check with `git status` that ignored paths really are ignored. A gitignore pattern like `docs/` (trailing slash) does not match a symlink; `/docs` does.

## Memory files
On day one, create `AGENTS.md`, `PROGRESS.md` and `LEARNINGS.md` from `templates.md`, gitignored. They let any agent continue the work in a new thread. Rules: memory.md.

## FACTS.md and the never-claim list
Create these on day one, from `templates.md`.
- Keep a `FACTS.md`: only verified, sourced facts, plus a "never claim" list. UI, README and video use only these. Record each fact with its source URL and the date read; the form uses only these or live data too.
- Never-claim list: wording the data cannot support, for example "violated", "failed", "illegal", or a power or penalty with no source. Add to it whenever a near-miss happens.
- When a number moves (a new data run, a corrected source), update `FACTS.md` first, then everything that quotes it.

## Run the day-1 go/no-go gate
Phase 1 wrote a concrete pass/fail gate and a fallback idea. Run the gate on schedule. If it fails, switch to the fallback the same day; do not argue with the result.

## Build and audit the dataset early
Pull the full dataset in the first hours. Re-measure every number that came from a sample.

## Test the riskiest unknown first (spikes)
List the 2–3 things that, if false, kill the plan. Before testing each one, write a pass bar with a number (a latency, an accuracy, a success rate) and the fallback you will switch to if it fails. Then test it in the first hours and record `RESULT PASS/FAIL` with the measured numbers in `LEARNINGS.md`. When the risk is how parts fit together, run the spike on the real scaffold and keep it; otherwise use a throwaway script. Examples:
- Can the deploy environment reach the data source? Some government sites block foreign or cloud IPs, or have broken TLS.
- Does the model or API we need actually work on this account? Access forms, quotas and regional availability all differ.
- Does the model behave as the design needs (calls the right action, in the right order) often enough?
- Does the full dataset say what the sample said?
- Is the required device, SDK or tool available to the team, and can an agent drive it from a script? Check installs and licences for every tool the medium needs (event-profile.md).

## Money and access
- Estimate the event's cost per service before the first big run. Re-check the estimate after the first real run.
- **Budget alerts are not hard caps**, and billing data lags. Use a cap that actually stops spend (an automated deny, a quota, a per-day counter in your code), plus rate limits on any public endpoint that calls a paid API.
- Use a least-privilege identity for daily work, not the root or owner account. Never paste secrets into chat or the repo.
- Note free-tier limits of third-party tools before you plan around them.

## Team
- Split ownership so each person owns something they can explain: build, design, product, story, video.
- Collect each person's contributions from the start (decisions, files, reviews). The "who did what" section is easier and more honest when it is written as you go.

## Done means
The go/no-go gate passed (or you switched to the fallback). The repo is safe to make public. `FACTS.md` and the memory files exist. The riskiest unknown is tested, with a result. Spend is capped. Everyone knows what they own.
