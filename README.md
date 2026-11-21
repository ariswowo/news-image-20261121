[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/ariswowo/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/ariswowo/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
# The World Today — Saturday, 21 November 2026, in one image

Entry for make.fun bounty **news-image-20261121** —
["Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121)
(pot $100; 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20;
deadline **2026-11-23T00:00:00Z**; published 2026-11-21T00:00:00Z).

A newspaper-style front page: one lead story (Russia's barrage on Ukraine
and missiles landing in Poland), four more stories (Wall Street's AI rout,
the ICJ's Myanmar genocide ruling, the COP31 deadlock, the UK–EU post-Brexit
deals), a diplomacy band (Trump–Xi–Putin Shenzhen declaration) and an
"Also" strip. The image is drawn entirely in code — no photographs, no
AI-generated base image.

## How it works

- `build_image.py` — the generator. Draws the 1024×1024 PNG with PIL
  (system DejaVu fonts only), offline and deterministic. Run it to
  regenerate `assets/entry.png`:
  `python3 build_image.py`
- `assets/entry.png` — the bundled image (138,922 bytes, 1024×1024 PNG).
- `main.py` — the entry program (Python 3.13, standard library only, no
  network, no randomness). It copies `assets/entry.png` byte-for-byte to
  `/output/entry.png`, so two runs write identical bytes. This is the
  approach the bounty itself names ("the simplest program copies an image
  the repository holds") and it keeps the graded run free of any font or
  PIL dependency.
  `OUTPUT_DIR=/tmp/out python3 main.py` (default output dir is `/output`).

## Judging (per the bounty)

An AI judge that can see images compares entries two at a time and picks
the one that best sums up the day's world news; entries rank by how often
they are picked. The judge has **no news feed** — it judges only what the
image itself shows, like a careful picture editor. The 50 highest-ranked
entries share the $100 pot. (The sibling 19 November bounty named the
judge as z-ai/glm-5.3-flash on OpenRouter, pairwise with a 1–5 margin,
each pair in both orders, 3 Swiss rounds plus a playoff among the top 52;
the 21 November page states the same pairwise setup without naming the
model.)

## Rules complied with

- Image: whole PNG, 1024×1024 px, 138,922 bytes — under the 1 MiB and
  1024×1024 limits.
- No network at run time; program runs twice and both runs write the
  same bytes (verified in TESTS.md).
- Public GitHub repo owned by ariswowo, created after the competition
  opened, under the MIT licence; `main.py` in the repo root.
- At most 10 submissions a day, 20 in all; last submission before the
  deadline is the final entry.
- News: see NEWS.md — every fact on the image was verified against
  reporting published/confirmed by 21 November 2026; nothing invented.
  The ICJ ruling is dated 19 November on the image itself.

## Files

| File | What it is |
| --- | --- |
| `main.py` | Entry program (stdlib-only copy to `/output/entry.png`) |
| `build_image.py` | Deterministic PIL generator of the image |
| `assets/entry.png` | The bundled 1024×1024 entry image |
| `NEWS.md` | The verified 21 November stories, with sources |
| `TESTS.md` | Local run results (two runs, identical bytes) |
| `LICENSE` | MIT |

## Status

Built locally only. **Not yet pushed to GitHub, not submitted to
make.fun.** Remaining steps: create the GitHub repo, run the kit's
`grade-local`, bundle the agent transcripts with the kit CLI, connect a
make.fun API key / payout wallet, then submit before 2026-11-23T00:00:00Z.
