#!/usr/bin/env python3
"""
Astrocartography (relocational) map for the natal chart.

For each body we take its equatorial position (right ascension, declination)
at the birth moment and Greenwich sidereal time, then solve for the world
locations where it sits on an angle:

  MC / IC  vertical meridians where the body culminates / anti-culminates
  AC / DC  horizon curves where the body rises / sets

Rendered on an equirectangular world map. Also produces a relocation readout:
the nearest line of each angle for a set of world cities.

Writes astrocartography.svg.
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

# --- bodies: (name, slug, swe id, glyph, colour) ----------------------------
# South Node is derived from the North Node (antipode), not a swe body.
ACG_BODIES = [
    ("Sun", "sun", swe.SUN, "☉", "#e6a52e"),
    ("Moon", "moon", swe.MOON, "☽", "#8f9bb8"),
    ("Mercury", "mercury", swe.MERCURY, "☿", "#4fae8f"),
    ("Venus", "venus", swe.VENUS, "♀", "#e488b4"),
    ("Mars", "mars", swe.MARS, "♂", "#d84b34"),
    ("Jupiter", "jupiter", swe.JUPITER, "♃", "#d07a2a"),
    ("Saturn", "saturn", swe.SATURN, "♄", "#7d8a55"),
    ("Uranus", "uranus", swe.URANUS, "♅", "#46a7c6"),
    ("Neptune", "neptune", swe.NEPTUNE, "♆", "#6b78dd"),
    ("Pluto", "pluto", swe.PLUTO, "♇", "#b060a6"),
    ("North Node", "north-node", swe.TRUE_NODE, "☊", "#d9c85f"),
    ("Chiron", "chiron", swe.CHIRON, "⚷", "#cf8f6a"),
]
SOUTH_NODE = ("South Node", "south-node", "☋", "#9a9488")

VS15 = "\ufe0e"

# --- cities for the relocation readout (name, lat, lon) ---------------------
CITIES = [
    ("New York", 40.71, -74.01), ("Los Angeles", 34.05, -118.24),
    ("San Francisco", 37.77, -122.42), ("Austin", 30.27, -97.74),
    ("Denver", 39.74, -104.99), ("Vancouver", 49.28, -123.12),
    ("Mexico City", 19.43, -99.13), ("Medellin", 6.24, -75.58),
    ("Buenos Aires", -34.60, -58.38), ("Lisbon", 38.72, -9.14),
    ("London", 51.51, -0.13), ("Barcelona", 41.39, 2.17),
    ("Berlin", 52.52, 13.40), ("Amsterdam", 52.37, 4.90),
    ("Rome", 41.90, 12.50), ("Athens", 37.98, 23.73),
    ("Cape Town", -33.92, 18.42), ("Dubai", 25.20, 55.27),
    ("Mumbai", 19.08, 72.88), ("Bangkok", 13.76, 100.50),
    ("Bali (Denpasar)", -8.65, 115.22), ("Singapore", 1.35, 103.82),
    ("Tokyo", 35.68, 139.65), ("Sydney", -33.87, 151.21),
    ("Melbourne", -37.81, 144.96),
]

ANGLE_ORDER = ("AC", "IC", "DC", "MC")


def norm180(x):
    return ((x + 180.0) % 360.0) - 180.0


def x_of(lon):
    return (lon + 180.0) * SCALE


def y_of(lat):
    return (LAT_MAX - lat) * SCALE


def positions(jd):
    """Return [(name, slug, glyph, color, ra, dec)] incl. the derived S Node."""
    swe.set_ephe_path("/usr/share/swisseph")
    flags = swe.FLG_SWIEPH | swe.FLG_EQUATORIAL
    out = []
    nn = None
    for name, slug, body, glyph, color in ACG_BODIES:
        res, _ = swe.calc_ut(jd, body, flags)
        ra, dec = res[0], res[1]
        out.append((name, slug, glyph, color, ra, dec))
        if slug == "north-node":
            nn = (ra, dec)
    if nn is not None:  # South Node = antipode of the North Node
        name, slug, glyph, color = SOUTH_NODE
        out.append((name, slug, glyph, color, (nn[0] + 180) % 360, -nn[1]))
    return out


def display_bodies():
    """(name, slug, glyph, color) in reading order: planets, nodes, Chiron."""
    def pick(slug):
        for n, s, _b, g, c in ACG_BODIES:
            if s == slug:
                return (n, s, g, c)
    planets = [(n, s, g, c) for n, s, _b, g, c in ACG_BODIES
               if s not in ("north-node", "chiron")]
    return planets + [pick("north-node"), SOUTH_NODE, pick("chiron")]


def gmst_deg(jd):
    return swe.sidtime(jd) * 15.0


def compute_lines(jd):
    gmst = gmst_deg(jd)
    lines = []
    for name, slug, glyph, color, ra, dec in positions(jd):
        base = dict(planet=name, slug=slug, glyph=glyph, color=color)
        lines.append({**base, "angle": "MC", "kind": "meridian",
                      "lon": norm180(ra - gmst)})
        lines.append({**base, "angle": "IC", "kind": "meridian",
                      "lon": norm180(ra + 180.0 - gmst)})
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
            lon0 = norm180(ra - 90.0 - gmst if angle == "AC"
                           else ra + 90.0 - gmst)
            lines.append({**base, "angle": angle, "kind": "horizon",
                          "segments": segs, "label_lon": lon0})
    return lines, gmst


def _dist_mi(lat, lon, line_lon):
    dlon = abs(norm180(lon - line_lon))
    return dlon * 69.17 * math.cos(math.radians(lat))


def city_readout(jd, max_mi=500.0):
    """Nearest line of each angle type for each city (within max_mi)."""
    gmst = gmst_deg(jd)
    pos = positions(jd)
    rows = []
    for name, lat, lon in CITIES:
        best = {a: None for a in ANGLE_ORDER}

        def consider(angle, line_lon, body):
            d = _dist_mi(lat, lon, line_lon)
            if best[angle] is None or d < best[angle]["mi"]:
                best[angle] = {"mi": d, "glyph": body[2], "color": body[3],
                               "planet": body[0]}

        for body in pos:
            ra, dec = body[4], body[5]
            consider("MC", norm180(ra - gmst), body)
            consider("IC", norm180(ra + 180 - gmst), body)
            x = -math.tan(math.radians(lat)) * math.tan(math.radians(dec))
            if -1.0 <= x <= 1.0:
                h0 = math.degrees(math.acos(x))
                consider("AC", norm180(ra - h0 - gmst), body)
                consider("DC", norm180(ra + h0 - gmst), body)

        row = {"city": name}
        for a in ANGLE_ORDER:
            b = best[a]
            row[a] = b if (b and b["mi"] <= max_mi) else None
        rows.append(row)
    return rows


def line_table(jd, lat_step=5.0):
    """Coordinates for every line. MC/IC are meridians (lat=None, one lon);
    AC/DC are sampled every `lat_step` degrees where the body rises/sets.
    Longitude is east-positive (negative = west)."""
    gmst = gmst_deg(jd)
    rows = []
    for name, slug, glyph, color, ra, dec in positions(jd):
        rows.append(dict(body=name, slug=slug, angle="MC", lat=None,
                         lon=norm180(ra - gmst)))
        rows.append(dict(body=name, slug=slug, angle="IC", lat=None,
                         lon=norm180(ra + 180 - gmst)))
        lat = 85.0
        while lat >= -85.0 - 1e-9:
            x = -math.tan(math.radians(lat)) * math.tan(math.radians(dec))
            if -1.0 <= x <= 1.0:
                h0 = math.degrees(math.acos(x))
                rows.append(dict(body=name, slug=slug, angle="AC",
                                 lat=round(lat, 1),
                                 lon=norm180(ra - h0 - gmst)))
                rows.append(dict(body=name, slug=slug, angle="DC",
                                 lat=round(lat, 1),
                                 lon=norm180(ra + h0 - gmst)))
            lat -= lat_step
    return rows


def export_csv(jd, path="astrocartography_lines.csv"):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["body", "angle", "latitude_deg", "longitude_deg"])
        for r in line_table(jd):
            lat = "" if r["lat"] is None else f"{r['lat']:.1f}"
            w.writerow([r["body"], r["angle"], lat, f"{r['lon']:.2f}"])
    return path


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

    s.append(f'<rect x="0" y="0" width="{W:.0f}" height="{H:.1f}" '
             f'class="acg-ocean"/>')
    s.append(f'<path class="acg-land" d="{" ".join(land_paths())}"/>')

    for lon in range(-150, 180, 30):
        x = x_of(lon)
        s.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}" '
                 f'class="acg-grid"/>')
    for lat in range(-60, 90, 30):
        y = y_of(lat)
        cls = "acg-grid acg-equator" if lat == 0 else "acg-grid"
        s.append(f'<line x1="0" y1="{y:.1f}" x2="{W:.0f}" y2="{y:.1f}" '
                 f'class="{cls}"/>')

    # planet lines (each tagged for interactive filtering)
    for ln in lines:
        tag = f'data-b="{ln["slug"]}" data-a="{ln["angle"]}"'
        c = ln["color"]
        if ln["kind"] == "meridian":
            x = x_of(ln["lon"])
            s.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}" '
                     f'class="acg-line" style="stroke:{c}" {tag}/>')
        else:
            for seg in ln["segments"]:
                d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in seg)
                s.append(f'<path d="{d}" class="acg-line acg-horizon" '
                         f'style="stroke:{c}" {tag}/>')

    # labels, staggered into rows per edge zone to avoid overlaps
    eq = y_of(0)
    zones = {a: [] for a in ANGLE_ORDER}
    for ln in lines:
        x = x_of(ln["lon"]) if ln["kind"] == "meridian" else x_of(ln["label_lon"])
        zones[ln["angle"]].append(
            dict(x=x, slug=ln["slug"], angle=ln["angle"],
                 txt=f'{ln["glyph"]}{VS15}{ln["angle"]}', color=ln["color"]))

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
                     f'data-b="{lb["slug"]}" data-a="{lb["angle"]}" '
                     f'text-anchor="middle">{lb["txt"]}</text>')

    emit("MC", 13, 13, 44)
    emit("IC", H - 5, -13, 44)
    emit("AC", eq - 7, -13, 40)
    emit("DC", eq + 16, 13, 40)

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
            print(f"  {ln['planet']:<11} MC line at longitude {ln['lon']:.1f}")
    with open("astrocartography.svg", "w", encoding="utf-8") as f:
        f.write(build_svg(data) + "\n")
    print("Wrote astrocartography.svg")
    print("Wrote", export_csv(data["jd"]))


if __name__ == "__main__":
    main()
