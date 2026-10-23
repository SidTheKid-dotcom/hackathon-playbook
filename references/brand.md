# Brand: identity for decks, logos, cards and pages

Goal: a look that comes from this problem, not from a template. Often a judge sees the deck before the product, so the deck must look like it belongs to the problem.

## When to read
Read this before any deck, title card, logo, landing page or branded artifact. Read it when the user says the work "has no personality", "looks like a template" or "is just a reskin". For the product screens, read [ui.md](ui.md) first; for the demo video, read [video.md](video.md). This file sets the identity both use.
Scale the process to the request. One title card needs a concept line and the sheet's colours, not a directions board.

## Concept first
Derive the identity from the problem's own material. Use the artifact the user fights (a notice, a form, a receipt), the place or the medium. Name the concept in one line before any colour, font or layout. Example: "the citizen's red pen correcting the official's 'resolved'". Give each colour a meaning and keep it fixed across every artifact. One accent always means the same thing, such as "the user". A colour without a meaning is decoration.

## Process
1. **Brief.** Name the audience (team, judges, sponsors) and what the deck must make them believe. Write both lines first; every choice serves them.
2. **Research.** Collect 3–5 references this community loves. Say in one line why each works. Borrow one part, such as a type scale, a grid or a photo treatment, not the whole look.
3. **Directions board.** Put 2–3 distinct directions on one image, as full slides or title cards. Make them differ in concept, not in shade. The user picks; do not pick for them.
4. **Brand sheet.** Write it with the template in [templates.md](templates.md). Record the palette with hex values and meanings. Record display, body and mono fonts, plus the script font for any non-Latin language, all with open licences. Add the grid, margins, logo mark, textures and image rules.
5. **Build from the sheet.** Every slide uses the sheet. If a slide needs a new colour or font, add it to the sheet first, with its meaning.
6. **Review by eye.** Put every slide on one contact sheet ([scripts/contact_sheet.py](../scripts/contact_sheet.py)) and look at it. Broken rhythm, a stray colour or a weak slide shows only in the grid.

## Real artifacts over stock
Use real photos of the place, real screenshots of real posts, real clippings and real product output. Stock reads as a template at once.
- Log the source and licence of every asset in an `ASSETS.md` list. No entry, no use.
- Show public users' handles only when the posts are public. Blur officials and private people unless the user decides otherwise.
- Label anything constructed "illustrative". A drawn screenshot is never shown as the product.
- Every number on a slide traces to `FACTS.md`, like every public claim (hard rule 2).

## Audience fit
- **Internal deck** (team, mentors, sponsors at the booth): sells the idea, the solution, how it works and why it helps. It has no rubric or score.
- **Judge deck**: maps slide by slide to the published criteria. Put the criterion in your notes, not on the slide.
- Never show the proxy score to judges. It is an internal estimate, not a result.

## Tool limits
- Check what the slide tool's API or connector can change before you plan on it: fonts, backgrounds, free layout, image insertion.
- If it cannot set fonts, backgrounds or free layout, render each slide as a full-bleed image. Use HTML or Python at 1920×1080 or 2×, and keep only key text live.
- Check whether the API can delete what you upload. If it cannot, upload only final assets.

## Gotchas
- Body text under 36 px at 1920 wide is hard to read on a projector. Check the smallest element, not the headline.
- A palette swap on an old deck is not a redesign. Change the concept, the grid and the image rules too, or call it a reskin.

## Gate
Did the user pick a direction, or choose to skip the board? Does the brand sheet exist? Is every image sourced and licensed? Did you look at the contact sheet?
