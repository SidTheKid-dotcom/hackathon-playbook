# Phase 3: Build

Goal: the core flow working end to end on real data, where the judges will open it, before any extra. Then depth that the video can show. The stack comes from the event profile; the principles below hold for any stack.

## Order of work
1. **Thinnest end-to-end path on real data first**: input → processing → output a user sees. Ugly is fine. Mocks are allowed only while building, labelled `MOCK` on screen and in file names, and deleted before the demo.
2. **Build and audit the dataset early. Re-measure any number from a sample on the full data.** Totals change once you deduplicate (one site counted once, amendments folded in) and filter properly (only records that meet the claim).
3. Then depth, ranked by criterion moved per hour.

## If AI reads or decides anything: the model proposes, code decides
This was the strongest engineering signal in our run, and judges increasingly penalise unvalidated AI output.
- Give the model one small unit at a time (one record, not the whole document), with a strict output schema.
- **Code checks every output against the source**: the figure must appear word for word, be in the right section, and fall within a believable range. Code picks the quote and the citation, not the model.
- Anything that fails goes to a **visible review state with a plain reason** ("Could not find this figure in the source"). It never counts toward totals and never triggers an action. Showing doubt is a feature, not an embarrassment.
- If citations matter, add a **proof step** that re-fetches each cited source and confirms each quote is still there ("829 of 829 matched"). It makes a great video moment.
- Measure accuracy on a small hand-checked set if time allows, and publish the real figure, whatever it is.

## Batch work and data plumbing
- Store inputs by content hash, so nothing is processed twice and every citation has a stable copy. Mirror the sources you cite, so judges can open them even when the original site is down.
- Use fan-out with retries and a failure budget (for example, the run continues if under 10% of items fail). Size concurrency to the slowest quota (model requests per minute), not to your CPU.
- Make each run reproducible from one command. Keep a log line that proves the result.
- Watch for internal rows (counters, config) leaking into published data; one counter row broke every nightly publish.

## Deploy and hosting
- Deploy where the profile says: the sponsor's platform, a free host, or local only. If a live link is required, it opens signed out.
- Live link that opens signed out on the sponsor's platform (when the rules ask for one).
- Serve the simplest thing that works: static JSON on a CDN beats an API when the data fits in one file. Fewer moving parts during judging.
- After every deploy, fetch the live URL and check the change is there. Rewrite rules and caches serve stale or wrong files.
- Infrastructure as code, if the platform offers it. One command builds and tears everything down. It also makes a good proof shot.

## CI, keys and public endpoints
- CI runs tests on every push and pull request with no secrets. Deploy only from the main branch, and run the tests before deploying.
- Prefer keyless CI authentication (OIDC or the platform's equivalent) over stored keys. Read the real token claims if a trust policy fails; formats change.
- Pin third-party CI actions to full commit hashes. Never run fork code with secrets (for example GitHub's `pull_request_target`). Echo nothing secret: logs go public with the repo.
- Every endpoint open to the public: allow-list its inputs, build any model prompt on the server from your own data, cap requests per day and concurrency, and give it least-privilege access. Check what it can delete or invoke, and narrow it.
- A spend cap that actually stops spend (see setup.md).

## Tests that protect the honesty rules
- A **data contract** check on what is published: every counted record has a source and a quote; review records carry a reason; totals agree.
- A small **rules gold set** built from real source text, including the messy cases.
- A test that no user-facing string or generated text uses the never-claim words, in every language.
- **Prove each test can fail**: break the rule on purpose, watch the test go red, then restore it. A test that passes the first time proves nothing.

## Sponsor tech
If the rubric scores use of the sponsor's tech, each service gets a real job and a moment in the video. Write a table: service → job → why this service → where it shows. Remove any service that is only decoration. "Remove X and you lose Y" should be true for each one.

## If the event is open-source or offline
Same principles, different tools: open-licence models run locally or on donated compute, a self-hostable stack, a one-command start (for example Docker Compose), sample data in the repo, and a licence compatible with the event's rules. Judges may run it, so the README's "run it" steps are part of the build.

## Done means
The core flow runs on real data where judges will open it. Every output traces to a source or shows a reason. CI is green. Public endpoints are capped. The sponsor-tech table is written.
