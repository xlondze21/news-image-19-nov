# news-image-19-nov

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/xlondze21/news-image-19-nov/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/xlondze21/news-image-19-nov/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A 1024x1024 newspaper-style infographic summing up 19 November 2026's world news in one image — "19 November 2026 — The World in One Day".

## Run it

```sh
python3 render.py entry.png   # draw the image
python3 main.py               # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Requires Pillow (`pip install Pillow`). No network. Deterministic:
running the generator twice produces byte-identical PNGs.

## The image

- **Hero:** Trump, Xi and Putin hold their first three-way summit in
  Shenzhen, on the APEC sidelines.
- **Four stories:** the ICJ's Rohingya genocide verdict on Myanmar
  (The Hague); the Crimean Bridge hit for a third time this week;
  Hakeem Jeffries picked as the Democrats' Speaker nominee; Iran
  widening its Gulf attacks after US strikes.
- **Strip:** NASA's Voyager 1 nears one light-day from Earth.
- **Ticker:** US markets, final closes of Wednesday 18 November 2026
  (labelled as such — the 19 Nov close did not exist yet at build time).

## License

MIT — see LICENSE.

---

<sub>Entered on [make.fun](https://make.fun/?ref=3f98mdh8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
