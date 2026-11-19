# 19 November 2026 — The World in One Day

Entry for the make.fun competition `news-image-20261119`:
"Sum up 19 November's world news in one image".

## The image

A 1024x1024 newspaper-style infographic for Thursday, 19 November 2026:

- **Hero:** Trump, Xi and Putin hold their first three-way summit in
  Shenzhen, on the APEC sidelines.
- **Four stories:** the ICJ's Rohingya genocide verdict on Myanmar
  (The Hague); the Crimean Bridge hit for a third time this week;
  Hakeem Jeffries picked as the Democrats' Speaker nominee; Iran
  widening its Gulf attacks after US strikes.
- **Strip:** NASA's Voyager 1 nears one light-day from Earth.
- **Ticker:** US markets, final closes of Wednesday 18 November 2026
  (labelled as such — the 19 Nov close did not exist yet at build time).

## How to run

```sh
python3 render.py entry.png   # draw the image
python3 main.py               # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Requires Pillow (`pip install Pillow`). No network. Deterministic:
running the generator twice produces byte-identical PNGs.

## License

MIT — see LICENSE.
