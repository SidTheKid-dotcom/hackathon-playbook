# Wow factor: making the idea land

Goal: the judge feels one "aha" early, sees it work, then sees the hard part behind it. A strong idea loses when the entry does not show it.

## When to read
Read this at the idea lock, once during the build and again before the feature stop. Most items are already rules in a phase file. This file links to them and adds only what is new. Scale it to the request. A 2-hour jam needs the winning moment and the first-30-seconds check, not every item.

## At the idea lock
- **Write the winning moment in one sentence**: "The judge sees ___ happen and says ___." Plan the build backward from it. A moment you cannot name is a moment the judges will not see.
- **The moment must surprise.** A judge should not predict it from the title. A clean UI of the expected thing is not an aha.
- **Show it on one screen, in one action, with no explanation first.** For a game, a 3D piece or content, use the medium's unit: the first minute of play, the first shot, the hook.
- **Name the one hard part** that makes the moment possible. Plan how it shows: a live trace, a counter, a before and after, a rejected second request.
- Split the plan into independent tasks for parallel agents. See [orchestration.md](orchestration.md).

## During the build
- Build the thin real path first and on real data. See [build.md](build.md), "Order of work".
- Do a few things well, not many things half done. Name the rest as next steps ("next: A, B, C"). See [scope.md](scope.md).
- Add no second platform (phone and web) unless it is the moment itself. The reason is the same as for gadgets in [scope.md](scope.md).
- **Design every state a judge can land on**: empty, waiting, success, conflict, error. Show no raw dialog, no bare error code and no "enter your key" prompt. See [ui.md](ui.md).
- **The demo needs no secrets and no operator steps.** If it needs a key or a reset, it is not ready. See "Public demo guard" in [build.md](build.md).
- **Test the first input a judge will try**, not only your rehearsed input. Pick demo data where the rule behind the result shows clearly.

## Make the depth visible
- **Put the hard part on screen**, not only in the README: the rule firing, the number computed, the race prevented. This extends "make the hidden depth visible" in [scope.md](scope.md).
- **Give a sceptic one proof action**: click it themselves, open a second device, try to break it. Judges check for fakes.
- **The repo must match the video.** A polished video over a thin repo is a common judge complaint. See [submit.md](submit.md).
- For technical judges, show how it is built: the code, or narration over the parts running. The video split in [video.md](video.md) gives this 15–20%.

## The first 30 seconds
The opening rules live in [video.md](video.md), "Story" (open hard, a real person, problem before fix). Add these checks:
- Open with one person in one painful moment, not a category of users.
- Show the problem in the tool people use now, then the fix.
- The aha appears by second 30. Cut every intro, logo and team slide before it.

## Live demo (only when judges see it in the room)
Hard rule 3 still applies: if judging uses only the video, the video is the demo. Then skip this section.
- **Prefer a live demo in the room.** A working live demo shows that nothing is faked.
- **Do not switch to a video in the middle of the pitch.** It costs 10–20 seconds and adds an audio risk. Keep a recording ready as the fallback.
- Rehearse 3 times with a timer, on the real devices and network.
- Use all the judge time: the motivation, the hard part and what you had to solve.

## Gate
Can you say the winning moment in one sentence? Does it appear by second 30? Is the hard part on screen? Before the feature stop: would a tired judge on their 30th entry remember one image from this? Name it, and cut any feature that does not serve it.

## Sources
Public advice from judges and winners, plus one failure at an event. Weigh the public advice; do not treat it as a rule.
- Event evidence (Oct 2026, ride-sharing entry): the demo needed an operator key and room resets, the rehearsed input did not show the rule at the natural station, and the hard parts (fare fairness, direction rules, race-safe accept) lived only in tests and docs. These led to the no-secrets, first-input and depth-on-screen items.
- Winning moment, master plan, design pass, live demo: [talk](https://youtu.be/AoxK3JpxbRc).
- Surprise over a clean UI: [post](https://x.com/tonychang430/status/2109694408127926664).
- Proof action and repo matching video: [judge thread](https://x.com/meataxe/status/2113293829151343091), [post](https://x.com/hndy/status/2112778632473063655).
- Golden path, one specific person: [discussion](https://www.reddit.com/r/hackathon/comments/1s4c5nf/what_separates_a_winning_hackathon_project_from/).
- Few things well, no mid-pitch video: [discussion](https://news.ycombinator.com/item?id=4346602).
- No second platform, problem in the old tool first: [discussion](https://news.ycombinator.com/item?id=4345811).
- Show how it is built: [judging tips](https://info.devpost.com/blog/hackathon-judging-tips).
