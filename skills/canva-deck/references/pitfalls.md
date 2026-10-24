# Pitfalls — what broke last time, and the rule that fixed it

Collected from a real 30-slide deck built this way (HTML → Canva). Each item: symptom → rule.
"Seen" = an error or result showed it. "Inferred" = the cause is a best guess.

## Contents
1. Authoring the HTML (1–8)
2. Hosting (9–11)
3. Import and merge (12–16)
4. Editing in Canva (17–22)
5. Uploads (23–25)

## 1. Authoring the HTML

1. **`box-shadow` disappears on import.** Hard offset shadows vanished (seen).
   Rule: draw the shadow as its own block, absolutely positioned behind the card, offset by the shadow distance
   (`<div class="sh" style="left:130px;top:430px;width:360px;height:360px"></div>` before the card). The starter deck does this.
2. **Badges inside inline text overlap after import.** A pill inside a heading or a sentence landed on top of the words.
   Rule: put a badge next to the text as a flex sibling, never inside an inline element.
3. **Notes and page names come from attributes.** `data-speaker-notes` on the `<section>` becomes the page's speaker notes, and
   `data-label` becomes the page title (seen). Write the spoken script into `data-speaker-notes` while building, so the deck
   arrives with its script.
4. **Never import a PDF.** PDF import splits Korean text into many small boxes, shifts spacing and swaps fonts (seen). HTML
   import keeps text boxes whole.
5. **`<img>` and `<video>` do not come through.** Phone frames arrived as shapes with no screenshot inside, and dashed
   borders became solid (seen).
   Rule: leave an empty, correctly sized frame in the HTML. Put the image in afterwards: crop it locally to the frame's
   aspect ratio, upload it, then `insert_fill` it at the frame's exact left/top/width/height (items 21, 23). Don't rely on dashed
   lines: draw them as short solid segments, or accept them as solid.
6. **Fonts.** Load web fonts from Google Fonts in the page (`Gowun Batang`, `Gowun Dodum` are fine). No font substitution was
   seen with HTML import. Fonts are swapped only on PDF import (inferred).
7. **Not tested:** `clip-path`, gradients, `transform: rotate`. The starter avoids `clip-path` and builds the bookmark's swallow-tail
   notch from a rotated square in the paper colour. That rotated square did import. Treat anything else exotic as unknown and
   check it on one slide first.
8. **Fix the layout in HTML before importing.** Import copies the layout as-is. Screenshots of every slide before import caught
   these: an arrow hidden under a box, a caption wrapping into a rule, a flex icon collapsing (give icons a fixed width and
   height), a title wrapping to leave one lone character on its last line, and tree boxes cutting off their last line.
   Rule: run `scripts/shoot.mjs` and look at every PNG before hosting.

## 2. Hosting

9. **Canva imports only from a public https URL.** Host the HTML somewhere public (Vercel, Netlify, GitHub Pages), with
   `<meta name="robots" content="noindex, nofollow">` in every page and a `robots.txt` of `User-agent: *` / `Disallow: /`.
   Pages are 1920 wide: `<meta name="viewport" content="width=1920">`.
10. **Check the URL returns 200 before importing.** A fresh deploy can take a few seconds. On Windows PowerShell, `vercel` may be
    blocked by script policy (`vercel.ps1`). Call `vercel.cmd deploy --prod --yes`.
11. **Keep private or licensed material out of the hosted HTML.** That includes book covers, other people's photos and
    unreleased numbers. The page is public while it is up. Add such images inside Canva via upload only, and take the
    hosting down or replace it when you are done.

## 3. Import and merge

12. **One import per part.** Split the deck into files of 4–5 slides (`part1.html` …) and import each one. Then append the
    parts to the main design with `merge-designs` (`insert_pages`). To redo a part, import the new file as a new design and
    merge it in place of the old pages.
13. `import-design-from-url` and `merge-designs` returned `status: success` directly. No failed or timed-out import was seen.
    If a job id comes back instead, poll `get-create-design-async-job`.
14. **One operation per `merge-designs` call.** `delete_pages` plus `insert_pages` together failed with "Only a single operation
    per merge request is supported" (seen). Send them as separate calls. `move_pages` (`from_page_numbers`,
    `to_after_page_number`) reorders pages.
15. **Thumbnails lag after a merge.** `read-design` said "No stored thumbnail available for this page yet" for merged pages, and
    some thumbnails were stale (seen). Check the standalone imported design's thumbnails, or check element positions in
    `design_content`.
16. **`read-design` with `design_content` for many pages is huge.** 100k–220k characters overflowed (seen). Ask for a few
    `page_indices` at a time.

## 4. Editing in Canva

17. **Edits live in a transaction.** `read-design` with `open_transaction: true` returns a `transaction_id`. `edit-design` with
    finalize `keep_open` applies the edits (status `edits_unverified`, with a thumbnail). Then finalize `commit` saves, or
    `cancel` discards. Nothing is saved before commit.
18. **Transactions expire while you wait.** A commit after the user took a while to answer failed with "Editing transaction … not
    found" (seen). The likely cause is that the session expired (inferred). Rule: when the user approves late, open a new
    transaction, re-apply the edits, show the thumbnail and commit.
19. **Ask before committing.** Show the thumbnail and say "not saved yet — save?" Commit only on a yes.
20. **Operation schema.** Address elements with `locator_id` (from `design_content`), not `element_id`. Speaker notes are
    changed with `replace_speaker_notes` plus `page_id`. `update_notes` does not exist (seen, error -32602). Operations used:
    `replace_text`, `find_and_replace_text`, `format_text`, `position_element`, `resize_element`, `delete_element`,
    `layer_element`, `insert_shape`, `insert_fill`, `crop_media`, `reorder_page`, `update_text_anchoring`, `add_text`.
21. **`crop_media` zoomed the wrong way** (seen). Crop locally instead (`scripts/fit_image.py` crops to the frame's ratio), then
    `insert_fill` at the frame's exact box.
22. **The user may be editing in Canva at the same time.** If they say they are working in the design, cancel your open
    transaction rather than commit over their changes. Re-read before the next edit, because text they deleted stays deleted.

## 5. Uploads

23. **Upload flow.** `create-upload-url` returns a one-use `uploadUrl`. Upload with
    `curl -X POST -H "Content-Type: application/octet-stream" --data-binary @file.png "<uploadUrl>"`. The response
    `{"mediaId": …}` is the `asset_id` for `insert_fill`. Get a new URL for every file.
24. **Video and GIF.** MP4 failed with "Unsupported file format MP4". A GIF uploaded, but `insert_fill` rejected it with "media
    not found" (seen). Leave a labelled empty frame and tell the user to drop the video or GIF in by hand in Canva.
25. **A PDF sent through `create-upload-url` never appeared as an openable design** (seen). Don't use it to bring in pages.
