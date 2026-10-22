# Phase 1: Constraints, idea hunt and lock

Goal: one locked idea that is unique, impactful, buildable in the time box and scored to win, plus a fallback idea and a day-1 go/no-go gate. Kill weak ideas early and bluntly. Most ideas fail on real data; find out in hours, not days.

## Step 1. Write the constraints before any idea
Write them in the project and filter every idea through them:
- **Team reality:** remote or on site, skills, hours, data access (public data only?).
- **10-second grasp:** a judge understands the problem in 10 to 15 seconds.
- **Real impact:** a specific user making a specific decision, in a niche that is not crowded.
- **Current problem:** people face it now. Back it with news, data or incidents from the last 12 to 18 months. An old, long-discussed problem fails unless something recent made it worse.
- **Story:** a relatable hero; side with the common person.
- **Sponsor removal test:** describe how the product works without the sponsor's tech. If a script, a dict or a generic database does the job as well, the tech is decoration; reshape or drop the idea. Name the exact sponsor capability (query, algorithm, scale feature) that nothing simpler replaces.
- **Genuinely agentic (when the event is about agents or AI):** the agent makes several decisions by itself (what to look at next, when to stop, which branch to follow, how to resolve conflicts). One lookup plus an LLM write-up is a thin layer, not an agent. List the decisions; fewer than three is a fail.
- **Safe:** nothing overstated to the sponsor; nothing that risks disqualification or credits.
- **Conflict check:** if the idea touches the user's employer, ex-employer or client domain, check NDA, IP and non-compete terms first. Use only public data, own accounts and new code.

## Step 2. Hunt wide
Generate many candidates (aim for 50 to 150) through several lenses:
- deadline- or news-driven (what changed in the last 18 months);
- judge-relatable plus sponsor-deep (a judge can be the user, and the sponsor tech does work nothing else can);
- long-term problems that something recent made worse.

## Step 3. Prior-art sweep at shortlist time, not at the end
For every shortlist idea, search GitHub, Product Hunt, Devpost, papers, X and the web for something that already does the core job. Name the closest tools and state exactly what yours does that they don't. If an existing tool does the core job, kill the idea now. Late prior-art finds waste whole rounds of work. Read your own demand sources as prior art too: posts about a pain often link or contain the fix people already use.

## Step 4. Shortlist a top 20
One row per idea (template in templates.md): exact problem, who faces it and how many, recency evidence, who already solves it (from Step 3), data source, rubric fit, sponsor-removal result, the agent's decisions, citations.

## Step 5. Verify before you pitch
Check every headline fact (numbers, dates, quotes, named sources, sponsor posts) live before you present any idea to the user. Mark anything unverified as unverified. Never present a fact that only sounds right; it comes back later as an error on screen.

## Step 6. Pick one ICP (ideal customer profile)
Name one specific user group ("teams building health AI chatbots", not "anyone using AI"). Prefer the group that:
- already feels the pain;
- has a natural moment to use the product;
- fits the delivery format (developers for an MCP server, CLI or CI check; consumers for an app).

The ICP shapes the demo, the README first line, the features and the cut list. Drop features it does not need. Too broad an audience is a common loss reason, and a sharp ICP also strengthens the demand check.

## Step 7. Demand check: will people actually use it?
For each finalist, show:
- **(a) Felt pain:** evidence the user feels it and seeks a fix today (forum posts, complaints, searches, workarounds).
- **(b) Moment of use:** when exactly they open it, and what they do next.
- **(c) Better than doing nothing:** it clearly beats their current habit.

A real problem that nobody feels fails here.

## Step 8. Kill test each finalist with real data (a few hours each)
- Can public data actually prove the gap? Record pass or fail, with numbers.
- **Prove it on the real thing.** When the problem lives inside a product people use (AI answers, apps, search results, platforms), capture that product's real output, not a stand-in. If logged-out access is blocked, sign up with the bot's own email when the user allows it, or ask the user to paste outputs.
- **No strawman.** Test the strongest version (for example, prompts that tell the AI to "check every source"), so the gap is real.
- **Baseline test (when the idea's value is information, answers or generated output):** do the user's real job with the strongest general AI assistant that has web search, using a careful prompt. Record what it gets right and wrong. Usually it does part of the job. Then name the gap it leaves (data it cannot reach, an action it cannot take, a check it cannot verify, a moment or workflow it does not fit) and build the idea around that gap. Kill the idea only if the assistant already does the whole job well. Keep the side-by-side result for the demo. The gap counts only if it is the user's real pain: "it is not wired into tool X" counts only when doing that step by hand is what hurts.

## Step 9. Red-team the survivors
Check each one for: novelty, buildability, the reaction test below, sponsor fit, named user and decision, ICP sharpness, and false-alarm risk.

**Niche check:** ask fresh AI agents for ideas the way a typical entrant would. Count how often yours appears. Ideas that agents suggest by default are crowded.

**Reaction test (obvious in hindsight):** tell the one-line pitch to people from the ICP and stay quiet. Weigh what they say unprompted. Strong signals: "Why doesn't this exist already?", "This would be super helpful", "This would change how I do X", "This solves a burden I have" (ask when they last felt it; a real burden has a recent story). "Cool" with no story is politeness. Confusion, or "why would anyone want this?", is a warning. One strong reaction from a real ICP member outweighs many polite ones. If no real users are reachable in time, use fresh-context agents role-playing the ICP and label the result a proxy.

## Step 10. Lock
- Score finalists on the proxy score from Phase 0. Lock one.
- Write down why the runner-up lost.
- Keep a **fallback idea that survives the most likely reason the gate fails**. If both ideas depend on the same access, platform or data, it is not a fallback.
- If any test left a warning (score below target, a confused or negative reaction, a sponsor-removal doubt), lock only with one written line: what must be true for this idea to win, and the check and time that will show it. If you cannot write that line, reshape before you lock.
- Write a **day-1 go/no-go gate**: a concrete pass/fail test (an accuracy number, or a proof that the gap exists on the full data) with a time. Phase 2 runs it; if it fails, switch to the fallback.

## Idea-stage gotchas
- An early sample statistic is often wrong at full scale. Re-measure on the full data.
- Developer-tool and coding-agent ideas are especially crowded; expect most to be built already.
- A map or dashboard with no decision attached is a weak entry.
- "AI layer over an existing tool" is the most common thin idea. Apply the agentic test.
- Overclaiming the problem ("the AI is wrong") invites pushback. State the narrow, provable gap.

## Done means
The constraints, the shortlist with citations, the kill-test results, the locked idea with its ICP, the runner-up's reason for losing, the fallback and the go/no-go gate are all written in the project docs (`WINNING_PLAYBOOK.md` or similar).
