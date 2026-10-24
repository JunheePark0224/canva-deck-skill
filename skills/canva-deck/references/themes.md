# Themes — swapping the look

The whole look lives in the `:root` tokens at the top of `assets/starter-deck.html`. Layout and import rules stay the same.
Change only the tokens, and keep the roles:

| Token | Role | Paper + bookmark (default) |
|---|---|---|
| `--paper` | page background | `#FAF5EA` cream paper |
| `--paper-deep` | empty frames, panels | `#F0E6D0` |
| `--paper-line` | hairlines, quiet bars | `#DDD0B4` |
| `--card` | card and picked-row fill | `#FFFFFF` |
| `--ink` / `--ink-soft` / `--ink-muted` | title, body, labels | `#2B2724` / `#4A433D` / `#7A6048` |
| `--accent` | the ONE emphasis colour: one word, one bar, one card per slide | `#B23A48` bookmark string |
| `--cloth` / `--cloth-edge` / `--foil` | the bookmark mark (cover, dividers, dark cards) | `#7A4A2E` / `#5A3420` / `#EAD9B0` |
| `--title` / `--body` | title and body fonts (Google Fonts link in `<head>`) | Gowun Batang / Gowun Dodum |

Why it works: a warm off-white page, near-black ink in three strengths, and a single red used sparingly. The audience's eye
goes where the red is. If a slide has two reds, it has two messages.

## Ready-made alternatives (tokens only)

**Ink on white (report)** — `--paper:#FFFFFF; --paper-deep:#F2F2F2; --paper-line:#DDDDDD; --card:#FFFFFF; --ink:#111111;
--ink-soft:#3A3A3A; --ink-muted:#777777; --accent:#1F5EFF; --cloth:#111111; --cloth-edge:#000000; --foil:#FFFFFF;`
fonts: `Noto Serif KR` / `Noto Sans KR`.

**Night library (dark)** — `--paper:#1E1B18; --paper-deep:#2A2622; --paper-line:#3D3832; --card:#26221E; --ink:#F3EBDD;
--ink-soft:#D6CCBC; --ink-muted:#A2968A; --accent:#E2A64B; --cloth:#5B3A26; --cloth-edge:#3E2718; --foil:#EAD9B0;`
In this theme `.sh` shadows read better at `background: #000`.

## Rules when changing a theme

- Keep body text at least 4.5:1 contrast against `--paper` (WCAG AA). `--ink-muted` is for labels only, so keep it at 3:1 or more.
- Use one accent. Introducing a second colour for "good vs bad" belongs on a chart slide, not in the theme.
- Fonts must load from Google Fonts or be installed in Canva. Check the cover after import, because the title font shows
  any substitution first.
- Re-run `scripts/shoot.mjs` after a theme change. Line lengths change with the font.
