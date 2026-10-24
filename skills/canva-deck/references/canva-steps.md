# Canva steps — host, import, merge, edit, save

Tool names are the Canva connector's (`mcp__<canva>__import-design-from-url` and so on). Read `pitfalls.md` items 12–25
first: the merge and transaction rules come from real errors.

## 1. Host

- Put the part files (`part1.html`, `part2.html` …) and `robots.txt` in one folder. Every page has
  `<meta name="robots" content="noindex, nofollow">` and `<meta name="viewport" content="width=1920">`.
- Deploy to any static host. Vercel: `vercel deploy --prod --yes` from the folder (on Windows PowerShell use `vercel.cmd`).
  Deploying publishes the pages, so confirm with the user first.
- `curl -s -o /dev/null -w "%{http_code}" <url>/part1.html` → `200` before importing.

## 2. Import each part

- `import-design-from-url` with the part's URL and a title such as `<Deck> · part 1`. Note the returned design id.
- If a job id comes back instead of a design, poll `get-create-design-async-job` until it reports success.
- Check: `read-design` (thumbnails) on the imported design. Compare it with your local screenshot of the same slide.

## 3. Merge into one deck

- The first imported part becomes the main design, or create an empty presentation and append everything to it.
- `merge-designs` with ONE operation per call: `insert_pages` (append a part's pages), `delete_pages`, `move_pages`.
- Redoing a part: import the new file as a new design → insert its pages → delete the old pages (two calls).

## 4. Edit

1. `read-design` with `open_transaction: true` and only the `page_indices` you need. Elements come with `locator_id`.
2. `edit-design` with finalize `keep_open` and a list of operations, for example:
   - `replace_text` / `find_and_replace_text` for wording
   - `position_element` / `resize_element` to nudge
   - `insert_fill` with an uploaded `asset_id` and the frame's exact box for screenshots
   - `replace_speaker_notes` with `page_id` for the script
3. Show the returned thumbnail to the user: "Not saved yet — save?"
4. On yes: finalize `commit`. On no: `cancel`. If the commit says the transaction is not found, it expired. Open a new one
   (step 1), re-apply the edits and show the thumbnail again.

## 5. Images

1. Crop locally to the frame's aspect ratio: `python scripts/fit_image.py shot.png 330x625 out.png`.
2. `create-upload-url`, then `curl -X POST -H "Content-Type: application/octet-stream" --data-binary @out.png "<uploadUrl>"`
   → `mediaId`.
3. `insert_fill` with that id at the frame's left/top/width/height (from `design_content`).
4. Video and GIF: leave the frame and ask the user to drop the file in by hand.

## 6. Finish

- Tell the user the design link, which pages still need a hand-placed video or GIF, and that the hosted HTML can come down.
  Remove the deployment, or leave it if it is noindex and has nothing private on it.
