---
name: canva-deck
description: Build a presentation the story-first way: write a storyboard where every slide title is a one-sentence conclusion, hand-build the slides as HTML (a warm cream-paper + bookmark theme by default, swappable), check screenshots, host the pages, and import them into Canva as an editable design through the Canva connector, then merge, edit, place screenshots and save after the user approves. Slides are built to be read from the back of the room: one focal point, large type, one accent. Use this whenever someone wants a deck, slides, PPT, 발표 자료, 장표, or a pitch/portfolio/project presentation designed (not just outlined), wants slides in Canva, wants to turn a report or storyboard into slides, or asks for "that paper/bookmark style" deck — even if they don't mention HTML or Canva. Not for editing an existing .pptx file (use a pptx skill) or a one-off single image.
---

# Canva deck — story first, HTML slides, Canva at the end

A deck built this way reads like an argument: the titles alone tell the story, every slide has one point and one
red accent, and the result is a real editable Canva design rather than a picture of slides. HTML is the drafting surface
because exact layout, theme tokens and screenshots are cheap there. Canva is the finishing surface because the user can keep
editing, present and export from it.

The flow has five stages. Don't skip ahead: each stage is cheap to change and expensive to change later.

1. **Story** — storyboard (`assets/storyboard-template.md`)
2. **Slides** — HTML from `assets/starter-deck.html`
3. **Check** — screenshots of every slide (`scripts/shoot.mjs`)
4. **Host + import** — public URL → `import-design-from-url` → `merge-designs`
5. **Finish in Canva** — screenshots, wording, speaker notes; save only after the user says yes

Before stage 2, read `references/pitfalls.md`. It lists what broke on a real 30-slide build and the rule for each.
Also read `references/audience.md`. It holds the readability rules (one focal point, sizes, contrast, wording) that
turned a finished-looking deck into one people could follow from the back of the room.
Before stage 4, read `references/canva-steps.md`.

## 1. Story

Get the facts first: audience, length, the one thing they should believe or do afterwards, and the material (report, data,
screenshots). Then fill the storyboard template.

- **A title is a conclusion, not a topic.** Write "Two in three visitors left without buying", not "Drop-off analysis". Read the titles
  in order. If they don't tell the story by themselves, fix the titles before designing anything.
- One idea per slide. If a slide needs two conclusions, it is two slides.
- Order problem → evidence → idea → test → result → limits → next step, unless the audience needs something else.
- Write the spoken line for each slide now. It goes into `data-speaker-notes` and arrives in Canva as the speaker notes.
- Mark missing numbers ★ and keep going. Never invent a number to fill a slide.

Show the user the list of titles and get a nod before building slides. This is the cheapest point to change the story.

## 2. Slides (HTML)

Copy `assets/starter-deck.html` and use its layouts. Each layout exists because it imports cleanly:

| Layout | Use for |
|---|---|
| cover | opening line + the bookmark mark |
| divider | section breaks (bookmark in the middle, "SECTION 0N") |
| cards | three ideas side by side, hard shadow, one card in accent |
| big number | the one-number summary |
| bars | funnels and comparisons (compute bar widths in px from the values) |
| table | options side by side, the chosen row lifted with accent lines |
| screens | product flow: empty frames, screenshots filled in Canva |
| columns | three short blocks of text on top rules (limits, next steps) |
| closing | return to the opening line |

Build rules (the reasons are in `pitfalls.md`):
- Each slide is `<section data-document-role="page" data-label="N name" data-speaker-notes="…">` at 1920×1080. Use absolute
  positions in px.
- No `box-shadow`: put a `.sh` block behind the card. No `clip-path`. No `<img>`/`<video>`: leave an empty `.frame` of the
  exact size and write the size inside it.
- Badges sit next to text as flex siblings, never inside a sentence. Icons get a fixed width and height.
- Put 4–5 slides in each file (`part1.html`, `part2.html` …), because Canva imports one file at a time. Copy the same
  `<head>` and `<style>` into every part.
- Keep private or licensed images out of the HTML. The pages will be public while hosted.
- Theme: change only the `:root` tokens (`references/themes.md`). Use one accent per slide.

## 3. Check

Run `node scripts/shoot.mjs part1.html shots/part1` for each part (needs Playwright; the script's header says how). Check
every PNG twice.

- **As a layout**: look for overlaps, a title that wraps to leave one lone character on its last line, text cut off at a box
  edge, and captions running into rules.
- **As the audience** (`references/audience.md`, section 5): view it at a quarter of its size. Ask four things:
  - Does the eye land on the point first?
  - Can every word be read? Nothing under 22px, no light-on-light text.
  - Is there one accent, and does it mark the point?
  - Is there any line nobody would miss? Cut it.

Fix all of this in HTML now, because Canva copies the layout exactly. Show the user the screenshots of the key slides before
hosting.

## 4. Host and import

Hosting publishes the pages, so ask the user before deploying and say where. Then follow `references/canva-steps.md`:
deploy with `noindex` and `robots.txt`, confirm a 200, import each part, then merge the parts into one design with one
operation per call.

If the Canva connector isn't connected, stop after stage 3. Give the user the HTML and screenshots and tell them that
connecting Canva lets the deck be imported. Don't fall back to PDF upload, because text breaks apart (pitfall 4).

## 5. Finish in Canva

- Screenshots: `scripts/fit_image.py` crops each one to its frame's ratio. Upload it and `insert_fill` it at the frame's box.
  Video and GIF can't be placed by the tools, so tell the user which frames to fill by hand.
- Edits run in a transaction. Apply them, show the user the thumbnail, and commit only on their yes. If the transaction has
  expired, reopen it and re-apply the edits.
- If the user is editing in Canva at the same time, don't commit over them. Cancel, re-read, then continue.
- End with: the design link, what is left for the user to do by hand, and whether the hosted pages can come down.
