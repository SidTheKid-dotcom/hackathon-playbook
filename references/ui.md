# Phase 5: UI and experience

Goal: a stranger understands what it is, why it matters and what to do next within 5 seconds, and nothing breaks at any width, in any language, on the device users really use. This file is written for screens. For another medium, keep the goal and the habits (mockup, approval, then build; audit, then look by eye) and swap the checks for the craft's own first impression: a game's first minute, a post's first two seconds, a physical demo's first touch.

## Mockup first, then code
1. Write an image prompt (or sketch) per screen, at phone and desktop size, with real text from the data.
2. Generate it (image model or design tool), review it against the brief, revise it, and **get the user's approval**.
3. Code the approved screen. Screenshot it at the same size, compare it with the mockup, and fix the differences.

Cap each screen's mockup loop (about two rounds) so it cannot eat the build. Shared building blocks (tokens, base components) can be built before any screen is approved.

## Inspiration that is actually loved
Gather UI inspiration from designs the community demonstrably loves. Study how they work, not only how they look: measure the interactions (with a scripted browser if needed) before copying them. In our study, the "3D" desk props of a famous studio site were pre-rendered images on flat planes, with no live 3D. Its quality came from one camera angle for every prop, physical "push" on fast cursor sweeps, and restraint (about 8 elements on the first screen).

## Messaging (the most common reason "nobody gets it")
- **Grunt test:** in 5 seconds a visitor can say what it offers, why it matters to them, and what to do next.
- **The headline says the user's task or question in their words**, not a slogan. Unknown products win with a literal task plus one input ("Check if your email is in a data breach"). Keep the tagline, but lower down.
- **One primary action**, named by its outcome ("Ask for the plant to run", not "Draft letter" or "Get started"), and repeated at the end of the page. Keep one name per action through the whole flow.
- Put the proof (a checkable number with its source) next to the main button.
- Explain jargon once, in plain words. Format numbers for the judges' locale.
- **Show the product working on the first screen**: a short animated demo or a real example card. Visitors understand the output before they read any claim.
- When removing words makes a screen feel empty, fill the space with pictures of the data or motion, not with more text.

## Build rules
- Design for the device users really have. If links arrive from chat apps, design for the phone first.
- Every screen has loading, empty and error states.
- Every number links to its source, or to a "how we count" page.
- Translations: the English sentence is the key, so a missing translation falls back to English instead of breaking. Use the spoken register people actually use, not textbook words. A test fails on never-claim words in every language, on dropped placeholders, and on missing keys. Read every string yourself after any bulk edit.
- Do not translate evidence such as verbatim source quotes.
- A dev-only state gallery (one route or scene that renders each state from fixtures) lets audits and screenshots reach loading, empty, error and rare states without a live backend. Keep it out of the demo path.

## Audit, then look
1. Run `scripts/ui_audit.mjs` across every route × widths (320 to 1920, plus a sideways phone) × languages. It flags sideways scroll, clipped text, overlapping elements, tap targets under 44 px on touch widths, and console errors.
2. Include English (or the base language) as a **control**, so you can tell a translation regression from an old problem.
3. **Look at screenshots by eye**: build contact sheets with `scripts/contact_sheet.py`. Scripts missed the logo under the language picker, the pot over the text and the clipped "kg"; eyes caught them.
4. Test interactions with real input: touch scroll past a zoomed map, a tap versus a drag, keyboard Enter in search (it must not open a random first result).
5. Check performance on a throttled CPU if anything animates or redraws a lot.

## Done means
The 5-second test passes with someone outside the team. The audit is clean, the contact sheets have been looked at, and the screenshots match the approved mockups.
