#!/usr/bin/env python3
"""
Astrocartography (relocational) map for the natal chart.

For each planet we take its equatorial position (right ascension, declination)
at the birth moment and Greenwich sidereal time, then solve for the world
locations where that planet sits on an angle:

  MC / IC  vertical meridians where the planet culminates / anti-culminates
  AC / DC  horizon curves where the planet rises / sets

Rendered on an equirectangular world map. Writes astrocartography.svg.
"""

import json
import math

import swisseph as swe
import natal

# --- map geometry -----------------------------------------------------------
W = 1000.0
LAT_MAX = 85.0
SCALE = W / 360.0
H = (LAT_MAX * 2) * SCALE

# --- bodies + per-planet colours (distinct, readable on both grounds) -------
ACG_BODIES = [
    ("Sun", swe.SUN, "☉", "#e6a52e"),
    ("Moon", swe.MOON, "☽", "#8f9bb8"),
    ("Mercury", swe.MERCURY, "☿", "#4fae8f"),
    ("Venus", swe.VENUS, "♀", "#e488b4"),
    ("Mars", swe.MARS, "♂", "#d84b34"),
    ("Jupiter", swe.JUPITER, "♃", "#d07a2a"),
    ("Saturn", swe.SATURN, "♄", "#7d8a55"),
    ("Uranus", swe.URANUS, "♅", "#46a7c6"),
    ("Neptune", swe.NEPTUNE, "♆", "#6b78dd"),
    ("Pluto", swe.PLUTO, "♇", "#b060a6"),
]

VS15 = "\ufe0e"


def norm180(x):
    return ((x + 180.0) % 360.0) - 180.0


def x_of(lon):
    return (lon + 180.0) * SCALE


def y_of(lat):
    return (LAT_MAX - lat) * SCALE


def compute_lines(jd):
    swe.set_ephe_path("/usr/share/swisseph")
    gmst = swe.sidtime(jd) * 15.0  # Greenwich sidereal time, degrees
    lines = []
    for name, body, glyph, color in ACG_BODIES:
        res, _ = swe.calc_ut(jd, body, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
        ra, dec = res[0], res[1]

        lon_mc = norm180(ra - gmst)
        lon_ic = norm180(ra + 180.0 - gmst)
        lines.append(dict(planet=name, glyph=glyph, color=color, angle="MC",
                          kind="meridian", lon=lon_mc))
        lines.append(dict(planet=name, glyph=glyph, color=color, angle="IC",
                          kind="meridian", lon=lon_ic))

        for angle in ("AC", "DC"):
            segs, cur, prev = [], [], None
            lat = -LAT_MAX
            while lat <= LAT_MAX + 1e-9:
                x = -math.tan(math.radians(lat)) * math.tan(math.radians(dec))
                if -1.0 <= x <= 1.0:
                    h0 = math.degrees(math.acos(x))
                    lon = norm180(ra - h0 - gmst if angle == "AC"
                                  else ra + h0 - gmst)
                    if prev is not None and abs(lon - prev) > 180:
                        if len(cur) > 1:
                            segs.append(cur)
                        cur = []
                    cur.append((x_of(lon), y_of(lat)))
                    prev = lon
                else:
                    if len(cur) > 1:
                        segs.append(cur)
                    cur, prev = [], None
                lat += 1.0
            if len(cur) > 1:
                segs.append(cur)
            # label anchor at the equator crossing (always exists)
            lon0 = norm180(ra - 90.0 - gmst if angle == "AC"
                           else ra + 90.0 - gmst)
            lines.append(dict(planet=name, glyph=glyph, color=color,
                              angle=angle, kind="horizon", segments=segs,
                              label_lon=lon0))
    return lines, gmst


def land_paths():
    with open("world_land.json", encoding="utf-8") as f:
        geo = json.load(f)
    paths = []
    for feat in geo["features"]:
        for ring in feat["geometry"]["coordinates"]:
            pts = []
            for lon, lat in ring:
                lat = max(-LAT_MAX, min(LAT_MAX, lat))
                pts.append(f"{x_of(lon):.1f},{y_of(lat):.1f}")
            if len(pts) > 2:
                paths.append("M" + "L".join(pts) + "Z")
    return paths


def build_svg(data):
    lines, _ = compute_lines(data["jd"])
    s = [f'<svg viewBox="0 0 {W:.0f} {H:.1f}" class="acg" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Astrocartography world map">']

    # ocean + land
    s.append(f'<rect x="0" y="0" width="{W:.0f}" height="{H:.1f}" '
             f'class="acg-ocean"/>')
    s.append(f'<path class="acg-land" d="{" ".join(land_paths())}"/>')

    # graticule every 30 degrees
    for lon in range(-150, 180, 30):
        x = x_of(lon)
        s.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}" '
                 f'class="acg-grid"/>')
    for lat in range(-60, 90, 30):
        y = y_of(lat)
        cls = "acg-grid acg-equator" if lat == 0 else "acg-grid"
        s.append(f'<line x1="0" y1="{y:.1f}" x2="{W:.0f}" y2="{y:.1f}" '
                 f'class="{cls}"/>')

    # planet lines
    for ln in lines:
        c = ln["color"]
        if ln["kind"] == "meridian":
            x = x_of(ln["lon"])
            s.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}" '
                     f'class="acg-line" style="stroke:{c}"/>')
        else:
            for seg in ln["segments"]:
                d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in seg)
                s.append(f'<path d="{d}" class="acg-line acg-horizon" '
                         f'style="stroke:{c}"/>')

    # labels: collect per edge zone, then stagger into rows so neighbours
    # with nearby longitudes do not overlap.
    eq = y_of(0)
    zones = {"MC": [], "IC": [], "AC": [], "DC": []}
    for ln in lines:
        x = x_of(ln["lon"]) if ln["kind"] == "meridian" else x_of(ln["label_lon"])
        zones[ln["angle"]].append(
            dict(x=x, txt=f'{ln["glyph"]}{VS15}{ln["angle"]}', color=ln["color"]))

    def emit(zone, base_y, step, min_gap):
        rows_lastx = []
        for lb in sorted(zones[zone], key=lambda d: d["x"]):
            row = None
            for i, lx in enumerate(rows_lastx):
                if lb["x"] - lx >= min_gap:
                    row, rows_lastx[i] = i, lb["x"]
                    break
            if row is None:
                row = len(rows_lastx)
                rows_lastx.append(lb["x"])
            s.append(f'<text x="{lb["x"]:.1f}" y="{base_y + step * row:.1f}" '
                     f'class="acg-label" style="fill:{lb["color"]}" '
                     f'text-anchor="middle">{lb["txt"]}</text>')

    emit("MC", 13, 13, 44)
    emit("IC", H - 5, -13, 44)
    emit("AC", eq - 7, -13, 40)
    emit("DC", eq + 16, 13, 40)

    # birthplace marker
    bx, by = x_of(data["birth"]["lon"]), y_of(data["birth"]["lat"])
    s.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4" class="acg-home"/>')
    s.append(f'<text x="{bx + 7:.1f}" y="{by - 6:.1f}" class="acg-home-label" '
             f'text-anchor="start">Pittsburgh</text>')

    s.append("</svg>")
    return "\n".join(s)


def main():
    data = natal.compute()
    lines, gmst = compute_lines(data["jd"])
    print(f"GMST (deg): {gmst:.3f}")
    for ln in lines:
        if ln["kind"] == "meridian" and ln["angle"] == "MC":
            print(f"  {ln['planet']:<8} MC line at longitude {ln['lon']:.1f}")
    svg = build_svg(data)
    with open("astrocartography.svg", "w", encoding="utf-8") as f:
        f.write(svg + "\n")
    print("Wrote astrocartography.svg")


if __name__ == "__main__":
    main()
