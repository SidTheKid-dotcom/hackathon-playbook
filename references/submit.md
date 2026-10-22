# Phase 8: Submit and freeze

Goal: a complete, consistent submission well before the deadline, then a freeze. The video, repo, live link and form tell one story with the same numbers.

## README (draft during the build; finish before you submit)
Order it the way judges skim:
1. **Title and one line**: what it does and for whom, with the track's key phrase.
2. **Links row**: video first, then the live link ("no sign-in"), then the track.
3. **One screenshot** that matches the video.
4. **Try it in 30 seconds**: 3–4 direct links into the product (an example record, the main action, the honest-doubt state).
5. **The problem**: 3 bullets, each with its source linked.
6. **Who uses it and what changes**: one table, lead user first.
7. **Proof numbers**, dated to a run ("as of …"), with how fresh the data is.
8. **How we used the sponsor's tech**: a table of service, job, why this service, and a video timestamp link.
9. **Architecture diagram** (Mermaid renders on GitHub).
10. **How the AI is checked**, if it is used, and **what it does when unsure**.
11. **Run it yourself**: steps that work on a fresh machine; how CI deploys.
12. **What is not built**: honest limits.
13. **What's next**: 2–3 lines.
14. **Team: who did what**, see below.
15. **What we learned.**
16. **Feedback on the sponsor's tools**, if asked: what worked, plus one suggestion each.
17. **AI tools used**: every one, and what it did.
18. **Credits and licences**: data, fonts, libraries, news sources shown, music and sound, voice.

Skip badges, tables of contents, long roadmaps and marketing language. Disclose AI tools. Credit third-party code and licences. Add one line if exploration happened before kickoff: "Before kickoff we only checked that the data was public. All code here was written during the event."

## Who did what: equal by structure, honest in content
Give each person the same shape and roughly the same length: role, what they owned, the decisions that shaped the product, and where it shows. Never say a person wrote code they did not write. Every line must be something that person can explain without notes. Non-code work (problem choice, product decisions, design, testing, facts, story) is real work; name it concretely.

## Tone toward the sponsor
Sponsor staff read the README, blog and form. Turn every friction into "what worked, plus one specific suggestion". Never "X blocked us" or "X refused".

## Defend it
Judges, reviewers and interviewers ask "why X, not Y". Keep a `DECISIONS.md` (template in templates.md) from the first big choice: one short record per decision a reviewer would question, not per choice. Before you submit, rehearse: have a fresh agent (the `grilling` skill, if installed) question you on each record and on the code. Turn each answer you cannot give into a fix, a test or an honest line under "What is not built". Questioning often finds real bugs.

## Going public (when the rules say)
1. Scan for secrets **before the first public push** (`DENY_TERMS='name|private-url' scripts/secret_scan.sh`). It covers commit messages too. Confirm no strategy files or `.env` files are tracked.
2. Flip the visibility. Open the repo signed out.
3. Optional polish: description, topics, website link, a release with the video attached, a social-preview image, and a plain `LICENSE` file so the host detects it (put data licences in a `NOTICE` file).
4. Turn on branch protection once it is free, so no one pushes untested code during judging.

GitHub cannot play YouTube inside a README. Use a clickable thumbnail plus chapter links that jump to timestamps (`?t=SECONDS`).

## Video upload
Title (product, outcome, event), a description with chapters and links, the caption file uploaded as subtitles (not through the video uploader), visibility per the rules, and a thumbnail picked from a strong frame. Open it signed out and confirm it plays in HD.

## Form answers
Build them from the README, so the facts stay identical. Answer exactly what each field asks; name the services and tools when asked. Keep a positive tone. Check every number once more against the live data.

## Side prizes (only once the core is safe)
- **Blog**: title it like strong engineering blogs, "How we built X: the one idea" or "A named idea: a plain explanation", not clickbait. Open with the story, then the architecture, the key technique, the honest failures as lessons, and a short numbered list of lessons. Use few images (4–6), each showing what text cannot: the product, the architecture, the proof. Read the platform's content terms (no personal data, no copied third-party images, no implied endorsement) and match its image sizes.
- **Resumes or other per-person items**: check what is needed early, and check the links open signed out.

## Final checklist
```
- [ ] Open the live link signed out; confirm numbers match
- [ ] Video plays signed out; length under the limit
- [ ] README links all work; numbers match the video and live data
- [ ] Repo visibility correct; no secrets; strategy files absent
- [ ] Every required form field filled; per-member items done
- [ ] Upload well before the deadline; verify playback signed out; submit; then freeze repo and video
```

## Freeze
Before the freeze, check that CI is green on the last pushed commit. A red mark on the repo page is the first thing a judge sees.

After submitting: no pushes and no live changes during judging, unless the rules allow it.
If the user decides to change something after the deadline anyway: docs only, no deploys, the full test suite run locally first. Tell the user that commit dates are public and judges can see them. A test that checks for placeholder text ("paste after upload") fails when you fill in the real value; update it in the same commit. Scheduled jobs (nightly data runs) can still change live numbers; know that, and decide with the user whether to pause them. Keep the live link and any paid services running until results are out.
