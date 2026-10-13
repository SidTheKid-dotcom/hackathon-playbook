# Phase 5: Verify (and keep verifying)

Goal: nothing false and nothing broken in anything a judge can see. Run this after every big batch of changes and again before submission, not only once.

## Checklist
```
- [ ] Regression sweep: old features re-tested, not only new ones
- [ ] Live check after deploy: the live URL, signed out, caches cleared
- [ ] Tests proven able to fail (break a rule on purpose, see red, restore)
- [ ] Data contract green on the published data
- [ ] Claims sheet: every claim → source, in UI, README, form and video
- [ ] Same numbers everywhere, as of one stated date
- [ ] Never-claim words absent everywhere, in every language
- [ ] Public endpoints: inputs allow-listed, capped, least privilege
- [ ] Secret scan clean (scripts/secret_scan.sh)
- [ ] Every outside critique point checked against evidence
```

## Regression sweep
Write a short script or checklist of every user flow that existed before the change (search, open a record, the main action, share, the secondary user's screen). Run it on the live site after each batch. When a check fails, find out whether it is the product or the test before fixing either: check the DOM or the data, not your assumption.

## Claims sheet
Extract every claim into one table: spoken lines, on-screen text, README sentences and form answers. Columns: claim, where it appears (with timestamp), source, status. Check four things for each claim:
- **Number**: matches the source or live data.
- **Tense**: "In June it told…", not "Now it tells…", if the rule was paused.
- **Place**: no fine next to a city that has none.
- **Pairing**: the picture under a line must not imply something the line does not say.

Mark the claim true, reword it, or cut it. Mark which items you checked yourself; tools misread text in images.

## Consistency
Pick one "as of" moment for the numbers (a data run, with its date). The video, README, live site and form all match it, or say plainly that live numbers update on a schedule. Regenerate README figures from the live source just before submission.

## Outside critique
When a teammate, a friend or another AI reviews the work, answer point by point with evidence:
- **Confirmed**: what you checked.
- **Partly right**: what is true and what is not.
- **Not an error**: why.

Then rank the fixes by cost and deadline risk. Take the good ones without ego, and drop the wrong ones with reasons.

## Security pass before going public
Scan history and tracked files for secrets. Confirm the strategy files are not tracked. Check every public endpoint's permissions. Check storage buckets are not world-readable unless intended. Report findings that are not yours (an old public bucket in the same account) to the user, and let them decide; do not delete them yourself.

## Done means
The checklist is ticked, with evidence for each line.
