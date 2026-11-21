# Local test results

Run 2026-11-21 ~11:00 UTC (Asia/Jakarta), local machine.
Python 3.12.3, Pillow 10.2.0 (the entry itself, `main.py`, needs only the
Python 3.13 standard library; the graded environment is Python 3.13).

## 1. Image generation is deterministic

`build_image.py` run twice to different paths, plus the bundled asset:

```
python3 build_image.py /tmp/test1/entry.png
python3 build_image.py /tmp/test2/entry.png
sha256sum /tmp/test1/entry.png /tmp/test2/entry.png assets/entry.png
150e01ef4dc29546b5189087fd4b557d69131a61675c9e5f563302db367b0dba  /tmp/test1/entry.png
150e01ef4dc29546b5189087fd4b557d69131a61675c9e5f563302db367b0dba  /tmp/test2/entry.png
150e01ef4dc29546b5189087fd4b557d69131a61675c9e5f563302db367b0dba  assets/entry.png
cmp: identical
```

Result: **PASS** — both runs byte-identical and identical to the bundled
`assets/entry.png`.

## 2. Entry program runs twice, identical bytes

```
OUTPUT_DIR=/tmp/out1 python3 main.py
  wrote /tmp/out1/entry.png (138922 bytes, sha256=150e01ef4dc29546b5189087fd4b557d69131a61675c9e5f563302db367b0dba)
OUTPUT_DIR=/tmp/out2 python3 main.py
  wrote /tmp/out2/entry.png (138922 bytes, sha256=150e01ef4dc29546b5189087fd4b557d69131a61675c9e5f563302db367b0dba)
cmp /tmp/out1/entry.png /tmp/out2/entry.png  -> identical
cmp /tmp/out1/entry.png assets/entry.png    -> identical
```

Default-path run also verified:

```
python3 main.py
  wrote /output/entry.png (138922 bytes, sha256=150e01ef4dc29546b5189087fd4b557d69131a61675c9e5f563302db367b0dba)
```

Result: **PASS** — two runs write the same bytes, as the bounty requires.

## 3. Size and dimensions

```
assets/entry.png  (1024, 1024) PNG  138922 bytes
```

Result: **PASS** — 1024×1024 px, 138,922 bytes, under the 1 MiB
(1,048,576 bytes) and 1024×1024 limits.

## 4. Visual check

The rendered image was inspected visually: masthead, date line, lead
story with stat chips (400+ drones / 110+ missiles / 8+ killed /
3 Kyiv bridges hit), four story cards, diplomacy band, "Also" strip and
sources footer are all fully legible with no clipped or overlapping text.
(An earlier draft had the lead body overlapping the stat chips and two
card bodies clipped at the card edge; both were fixed by trimming the
text to measured wrap widths and re-rendered — final sha256 above is the
fixed version.)

## 5. Not yet done (needs the kit / user approval)

- `grade-local` with the **news-image-20261121 kit** has NOT been run:
  the kit already present at `~/workspace/makefun/kit/` belongs to a
  different competition (`csv-reader-speed-01-run-20261121`), so it
  cannot grade this entry. Download the news-image kit and run
  `node cli/makefun.mjs grade-local` before submitting.
- No GitHub push and no make.fun submission have been made.
- No network use at run time: `main.py` imports only `hashlib`, `os`,
  `shutil`, `sys`, `pathlib`; `build_image.py` uses only local fonts.
