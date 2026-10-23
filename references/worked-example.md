# Worked example: VACHAN (WeMakeDevs x AWS Environmental Hacks, 8–11 Oct 2026)

One complete run, kept so you can see the phases applied. **It is an example, not a template.** Its stack was AWS because the event required AWS; another event needs another stack.

## Contents
- The entry
- Phase by phase: what we did
- What went wrong and the fix
- Final numbers

## The entry
- **Problem:** large Pune housing projects promised in writing (in public environmental-clearance minutes) to process their own wet waste on site. Nobody tracked those promises, while the city fined societies and sent hundreds of tonnes a day to plants.
- **Product:** it reads 1,027 government PDFs and turns each project's promise into a card: kg a day, plant type, and the exact PDF page, highlighted. Residents send a letter asking for the plant to run; ward officers get a check-first list.
- **Tagline:** "Read the fine print before you pay the fine." Mission line: "Get waste processed where it's made."
- **Team of 3:** one person on the build, one on problem and design, one on product and outcome. Claude Code was the coding partner, and the README disclosed it.

## Identity
Concept: "the citizen's red pen correcting the official's 'resolved'". Red meant only the citizen, on every slide.
Real posts and city photos replaced stock; each source and licence went into `ASSETS.md`.
Slides were rendered as images because the slide tool's API could not change fonts.

## Phase by phase: what we did
| Phase | What we did | Lesson |
|---|---|---|
| 0 Decode | Quoted the rubric. Found the real deadline in an organiser blog post (it later moved to midnight). Built a /30 proxy score. | Re-check announcements on the last day. |
| 2 Setup | Public repo created after kickoff. Strategy docs in a private repo, symlinked in. Budget alerts plus an automated deny at $50. First risk tested: could a cloud function reach the government portal? (Yes.) | Alerts are not caps. A symlink needs `/docs`, not `docs/`, in gitignore. |
| 3 Scope | Debated resident vs ward officer as the lead user. The impact chain favoured the officer; scoring against the judges picked the resident (judges can *be* residents, the team lived it, real use was possible). Officer second. Product frozen early; only technical fixes after. | Score the user options; don't argue from one criterion. |
| 4 Build | Crawl → hash-keyed storage → fan-out over PDFs → model extracts one project at a time into a schema → plain code checks the figure appears verbatim, is the operation-phase figure, and is 0.5–3 kg per flat → review state with a reason → static JSON on a CDN → proof step re-fetching every cited PDF (829/829). CI on OIDC, data contract, rules gold set, tests mutation-checked. | "The model reads, code decides" was the strongest engineering story. |
| 5 UI | Mockups via image generation, approved, then coded. Studied a loved site by measuring it. Messaging rewrite: question headline, one outcome-named button, proof line under the button, a live phone demo on the first screen. English, Marathi and Hindi with tests on banned words. | Overflow audits passed while elements overlapped; contact sheets caught it. |
| 6 Verify | Regression sweeps on the live site, a security audit (narrowed the public endpoint's permissions), README numbers regenerated from live data. | Checked old features, not just new ones. |
| 7 Video | Researched the judges and storytelling (Mayer, And/But/Therefore). Voice-first HTML composition with word-pinned motion, about 60% real recordings. Tried TTS, then a clone, then the founder's real voice (best). Six versions; proxy judges asked for urgency and the builder's accountability; audits for claims, frames, reading time and loudness. 2:59.5. | Every "small" change moved the length. Real voice won. |
| 8 Submit | README in skim order with timestamp links, equal team split, positive AWS feedback, form answers from the README, repo public after a secret scan, release with the video, blog with 5 images. | Negative wording about the sponsor was rewritten as suggestions. |

## What went wrong and the fix
- A sample said 40% of PDFs were scans; the full set had 12 of 1,027. Textract stayed a side path.
- The first headline total (350 t a day) double-counted amendments and included deferred projects. After deduplication and filtering it was 313.7 t (PCMC).
- A counter row in the same table as the data broke two nightly publishes. Publish now skips internal rows, with a test.
- The Bedrock Guardrail blocked every letter: once because the prompt listed the banned words, and once because of the prompt-attack filter. It now guards the output only.
- The site served the PDF worker (`.mjs`) as HTML because of an SPA rewrite rule, and the CDN cached it.
- "Push deploys automatically" was assumed, and false (there was no repo connection). Real CI/CD was then set up.
- Devanagari was clipped by `line-height: 1` and split by a per-letter hover animation.
- Video: a silence-trim rule clipped first words; a headline said "building collapse" over waste narration; a teammate's number (39 of 44) had no source; "officers fine builders" was unverified and was reworded to "go to the builder first".

## Final numbers (11 Oct 2026)
735.6 t a day promised in writing across 783 checked projects; 385 waiting for a person; 829 of 829 quotes verified; about $10 of AWS spend for the whole event.
