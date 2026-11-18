# News Image — Wednesday 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/ayukwulan/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/ayukwulan/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A newspaper front page summing up the real world news of Wednesday
18 November 2026, drawn entirely with PIL shapes (no photographs).

## The stories

1. **Lead — Iran hits US bases in the Gulf.** The US struck an
   Iranian Revolutionary Guard missile launch site on Qeshm Island in
   the Strait of Hormuz. Iran retaliated early Wednesday, launching
   strikes and drones against Kuwait (Ali Al Salem Air Base, which
   hosts US forces) and Bahrain (a US radar site and Patriot missile
   systems). Iran also shot down a US MQ-9 drone near the strait.
2. **Kerch Bridge hit again.** Ukraine struck the Kerch (Crimean)
   Bridge for a second day; part of its road span fell into the
   strait and one road arch collapsed.
3. **APEC Shenzhen.** Xi Jinping and Vladimir Putin met in Shenzhen
   ahead of the trilateral summit with Donald Trump on Thursday. Xi
   pledged to stand against trade protectionism; Putin criticised
   Western sanctions.
4. **US Senate.** Democrat Mary Peltola defeated Republican Sen. Dan
   Sullivan in Alaska, giving Democrats a projected 56–44 majority
   in the incoming Senate.
5. **Siberia crash.** A Russian military plane (An-12) crashed in the
   Kemerovo region of Siberia, killing all 19 people on board.
6. **Israel.** Israel's parliament elected Matan Kahana as the new
   Knesset speaker, a win for Prime Minister-elect Gadi Eisenkot's
   Yashar party and a setback for Benjamin Netanyahu.
7. **Also in the news.** Ebola outbreak in DR Congo more than doubled
   in three months — 11,000+ cases, 5,400 deaths. Houthis launched 5
   drones at Saudi East-West pipeline pumping stations. Category 5
   Cyclone Xavier hits the Northern Cook Islands. A 6.0-magnitude
   earthquake strikes Papua New Guinea.

## Sources

Just Security · Open Chronicle · Horizon · One Turn · Daily Baku.

## Files

- `draw.py` — PIL script that draws `entry.png` (1024×1024).
- `entry.png` — the finished front page.
- `main.py` — stdlib-only entry program: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), with a
  copy-size verification.

## Design notes

Masthead "THE WORLD TODAY" with the date in a black band so it reads
at small size. The lead story takes the top half: a large serif
headline, a drawn schematic map of the Gulf (Iran, the Arabian
Peninsula, Qeshm Island, strike markers at Qeshm, Kuwait and Bahrain,
and the downed MQ-9), and a fact column with the four key facts. Five
more stories sit in a 3×2 grid, each with a short headline, a one-line
summary and a small drawn icon (broken bridge, globe, capitol, plane,
Knesset); the sixth cell holds four short items. Light paper
background, dark text, no invented facts, no hype.

## Verification

- `entry.png` is exactly 1024×1024 and 139,743 bytes (under the
  1 MiB cap).
- `main.py` run twice to two different output dirs produces
  byte-identical files (matching sha256).
- The image was viewed and checked: date legible, all headlines
  readable, no overlapping or cut-off text.

## How to run

```sh
python3 draw.py          # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` uses only the Python standard library and runs offline; two
runs write byte-identical files.
