# Birth Chart

A small, reproducible natal-chart calculator and a hand-designed chart page.
Planetary positions come from the [Swiss Ephemeris](https://www.astro.com/swisseph/)
(via `pyswisseph`), so the numbers are accurate rather than approximate.

The chart it renders is for **June 7, 1996, 3:35 PM EDT, Pittsburgh, PA**
(Magee-Womens Hospital). Edit the `BIRTH` block in `natal.py` to compute a
different chart.

## What's here

| File | Purpose |
| --- | --- |
| `natal.py` | Core computation. `compute()` returns every value the other scripts use (planets, houses, angles, aspects). One source of truth. |
| `birth_chart.py` | Prints the chart and writes `birth_chart_report.md`. |
| `build_chart_wheel.py` | Renders the chart wheel to `birth_chart.svg` (Placidus) and `birth_chart_wholesign.svg` (whole sign); theme-aware CSS classes, element-colored zodiac. |
| `astrocartography.py` | Computes the planetary MC/IC/AC/DC lines and renders the astrocartography world map to `astrocartography.svg`. |
| `world_land.json` | Natural Earth 110m land outlines (GeoJSON) used as the map basemap. |
| `assemble_artifact.py` | Fills `birth_chart_template.html` with the fonts, the wheel, and the placements to produce the self-contained `birth_chart.html`. |
| `birth_chart_template.html` | The page design (celestial "star atlas" treatment, light and dark themes). |
| `fonts/` | EB Garamond and Cormorant Garamond (woff2), inlined into the page. |
| `setup_ephemeris.sh` | Downloads the Swiss Ephemeris data files. |

## Setup

```bash
pip install -r requirements.txt
./setup_ephemeris.sh            # downloads ephemeris files to /usr/share/swisseph
```

The ephemeris files are needed for full precision and for Chiron. Without them,
`pyswisseph` can fall back to its built-in Moshier model for the main planets,
but the asteroid file is required for Chiron.

## Usage

```bash
python3 birth_chart.py          # text + birth_chart_report.md
python3 build_chart_wheel.py    # birth_chart.svg + birth_chart_wholesign.svg
python3 astrocartography.py     # astrocartography.svg
python3 assemble_artifact.py    # birth_chart.html (open in a browser)
```

## Method

Tropical zodiac, true lunar node. The chart wheel uses the Placidus house
system; the report and placements table list both Placidus and whole sign
houses, since the house a planet falls in depends on that choice (signs,
degrees, and aspects do not). Local time is converted to UT before computing
the Julian Day. Retrograde motion is taken from each body's instantaneous
speed. Aspect orbs: 8 degrees for conjunction and opposition, 7 trine,
6 square, 5 sextile.

A birth chart is a tool for reflection, offered in that spirit.
