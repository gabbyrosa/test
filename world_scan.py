#!/usr/bin/env python3
"""
Whole-world grid scan of the natal chart.

Instead of scoring a hand-picked city list (which can only ever confirm the
places someone already thought of), this walks a 1-degree grid over every
land point on Earth, relocates the chart there, and scores it on chart
factors alone: benefics on angles, malefics on angles, chart ruler, and the
Moon's house. No climate, no cost, no second chart.

Then it groups the high-scoring points into contiguous zones so the output is
regions rather than 40,000 rows.
"""

import json
import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
RUL = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Uranus",
       "Pisces": "Neptune"}
FL = swe.FLG_SWIEPH
BODIES = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
          ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
          ("Saturn", swe.SATURN), ("Uranus", swe.URANUS),
          ("Neptune", swe.NEPTUNE), ("Pluto", swe.PLUTO)]
JD = swe.julday(1996, 6, 7, 15 + 35 / 60.0 - (-4), swe.GREG_CAL)
P = {n: swe.calc_ut(JD, b, FL)[0][0] for n, b in BODIES}

BENEFIC = ("Venus", "Jupiter", "Sun", "Moon")
HARD = ("Mars", "Saturn", "Pluto")
STEP = 1.0
LAT_MIN, LAT_MAX = -56.0, 71.0        # habitable land band


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def load_land():
    """Return polygons as (minlon, minlat, maxlon, maxlat, ring)."""
    with open("world_land.json", encoding="utf-8") as f:
        geo = json.load(f)
    polys = []
    for feat in geo["features"]:
        geom = feat["geometry"]
        rings = (geom["coordinates"] if geom["type"] == "Polygon"
                 else [r for poly in geom["coordinates"] for r in poly])
        for ring in rings:
            if len(ring) < 4:
                continue
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            polys.append((min(xs), min(ys), max(xs), max(ys), ring))
    return polys


def in_ring(lon, lat, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > lat) != (yj > lat):
            if lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
                inside = not inside
        j = i
    return inside


def is_land(lon, lat, polys):
    for mnx, mny, mxx, mxy, ring in polys:
        if mnx <= lon <= mxx and mny <= lat <= mxy and in_ring(lon, lat, ring):
            return True
    return False


GAZETTEER = [
    ("Tucson / S. Arizona", 32.2, -111.0), ("Phoenix / Sedona AZ", 33.6, -112.0),
    ("Salt Lake / N. Utah", 40.8, -111.9), ("Santa Fe / New Mexico", 35.4, -106.0),
    ("Denver / Colorado", 39.7, -105.0), ("Montana / Idaho", 46.5, -112.5),
    ("Alberta, Canada", 51.0, -114.0), ("Baja California Sur", 24.0, -110.5),
    ("Sonora / NW Mexico", 29.0, -110.9), ("Chihuahua, Mexico", 28.6, -106.1),
    ("Texas Hill Country", 30.3, -98.5), ("Great Plains (KS/NE)", 39.0, -98.5),
    ("Ohio / Kentucky", 38.5, -83.5), ("Florida Gulf coast", 27.8, -82.6),
    ("Carolinas / Appalachia", 35.6, -82.5), ("US Northeast", 41.5, -73.5),
    ("Pacific Northwest", 45.5, -122.7), ("California coast", 34.5, -119.5),
    ("Yucatan / Guatemala", 18.5, -89.0), ("Costa Rica / Panama", 9.6, -83.5),
    ("Colombia", 5.0, -74.5), ("Peru / Bolivia", -13.0, -72.0),
    ("Chile", -33.5, -70.7), ("Argentina", -34.6, -60.0),
    ("Brazil (southeast)", -22.0, -45.0), ("Amazon basin", -4.0, -60.0),
    ("Iceland", 64.9, -21.9), ("Ireland / W. Britain", 53.3, -7.5),
    ("Britain / N. France", 51.0, -1.0), ("Portugal", 39.5, -8.5),
    ("Spain (interior)", 40.0, -4.0), ("Catalonia / E. Spain", 41.0, 1.5),
    ("France / Benelux", 47.5, 3.0), ("Italy", 43.0, 12.0),
    ("Germany / Alps", 48.5, 11.5), ("Scandinavia", 60.5, 12.0),
    ("Poland / Baltics", 53.5, 21.0), ("Balkans / Greece", 40.5, 22.0),
    ("Turkey", 39.0, 33.0), ("Ukraine / S. Russia", 48.5, 36.0),
    ("Morocco / NW Africa", 31.6, -7.0), ("Algeria / Sahara", 27.0, 3.0),
    ("Egypt / Nile", 27.0, 31.0), ("West Africa", 9.0, 0.0),
    ("Ethiopia / Horn", 9.0, 39.0), ("Kenya / Tanzania", -3.0, 36.0),
    ("Southern Africa", -25.0, 26.0), ("South Africa (Cape)", -33.9, 20.0),
    ("Madagascar", -19.0, 46.5), ("Arabia / Gulf", 24.0, 47.0),
    ("Iran", 32.0, 53.0), ("Pakistan / Balochistan", 27.5, 66.0),
    ("Afghanistan / Tajikistan", 36.0, 68.0), ("Kazakhstan", 48.0, 67.0),
    ("W. Siberia / Urals", 62.0, 66.0), ("C. Siberia", 62.0, 97.0),
    ("India (north)", 27.0, 78.0), ("India (south)", 13.0, 78.0),
    ("Nepal / Himalaya", 28.0, 84.0), ("Bangladesh / Burma", 22.0, 92.0),
    ("Thailand / Indochina", 15.0, 101.0), ("Vietnam", 16.0, 107.0),
    ("Malaysia / Sumatra", 2.0, 102.0), ("Java / Bali", -7.5, 111.0),
    ("Philippines", 13.0, 122.0), ("China (east)", 31.0, 118.0),
    ("China (west/Tibet)", 32.0, 90.0), ("Mongolia", 47.0, 105.0),
    ("Korea", 37.0, 127.5), ("Japan", 35.7, 138.0),
    ("E. Siberia / Kamchatka", 60.0, 150.0), ("W. Australia", -28.0, 118.0),
    ("E. Australia", -30.0, 149.0), ("New Zealand", -42.0, 172.0),
    ("Papua New Guinea", -6.0, 145.0), ("Alaska", 63.0, -152.0),
    ("N. Canada", 62.0, -100.0), ("Greenland", 70.0, -40.0),
]


def nearest_place(lat, lon):
    return min(GAZETTEER,
               key=lambda g: math.hypot(lat - g[1], n180(lon - g[2])))[0]


def score(lat, lon):
    try:                                    # Placidus is undefined near the poles
        cusps, ascmc = swe.houses(JD, lat, lon, b"P")
    except swe.Error:
        cusps, ascmc = swe.houses(JD, lat, lon, b"W")   # whole-sign fallback
    asc, mc = ascmc[0], ascmc[1]
    ang = {"ASC": asc, "IC": (mc + 180) % 360,
           "DSC": (asc + 180) % 360, "MC": mc}
    s, hits, hard = 0.0, [], []
    for b in BENEFIC:
        a, o = min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                   key=lambda t: t[1])
        if o <= 8:
            w = 3.0 if o <= 2 else 2.0 if o <= 5 else 1.0
            if a == "MC" and b not in ("Venus", "Sun"):
                w *= 0.5
            s += w
            hits.append(f"{b} {a} {o:.0f}")
    for b in HARD:
        a, o = min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                   key=lambda t: t[1])
        if o <= 6:
            pen = 2.5 if b == "Mars" else 1.5
            s -= pen * (1.0 if o <= 3 else 0.5)
            hard.append(f"{b} {a} {o:.0f}")
    if RUL[sg(asc)] == "Venus":
        s += 1.0
        hits.append("Venus rules")
    p = P["Moon"] % 360
    for i in range(12):
        a2, b2 = cusps[i], cusps[(i + 1) % 12]
        if (a2 < b2 and a2 <= p < b2) or (a2 > b2 and (p >= a2 or p < b2)):
            if i + 1 == 6:
                s += 0.75
                hits.append("Moon h6")
            break
    return s, hits, hard


def main():
    polys = load_land()
    pts = []
    lat = LAT_MIN
    while lat <= LAT_MAX:
        lon = -180.0
        while lon < 180.0:
            if is_land(lon, lat, polys):
                s, hits, hard = score(lat, lon)
                pts.append((lat, lon, s, hits, hard))
            lon += STEP
        lat += STEP
    print(f"scored {len(pts)} land points at {STEP}-degree resolution")

    best = max(p[2] for p in pts)
    top = [p for p in pts if p[2] >= best - 0.01]
    print(f"global maximum raw score = {best:.2f}  ({len(top)} points reach it)\n")

    # distinct regional peaks: greedily take the best point, then suppress
    # everything within SEP degrees of it, so each row is a separate region
    SEP = 9.0
    ranked = sorted(pts, key=lambda p: -p[2])
    peaks = []
    for lat, lon, s, hits, hard in ranked:
        if s <= 0:
            break
        # great-circle separation, not raw degrees: a degree of longitude is
        # much shorter than a degree of latitude away from the equator
        def far(q):
            p1, p2 = math.radians(lat), math.radians(q["lat"])
            dl = math.radians(n180(lon - q["lon"]))
            c = (math.sin(p1) * math.sin(p2)
                 + math.cos(p1) * math.cos(p2) * math.cos(dl))
            return math.degrees(math.acos(max(-1.0, min(1.0, c)))) > SEP
        if all(far(q) for q in peaks):
            peaks.append(dict(lat=lat, lon=lon, s=s, hits=hits, hard=hard,
                              where=nearest_place(lat, lon)))
        if len(peaks) >= 40:
            break
    print(f"{'#':<4}{'score':<7}{'lat,lon':<13}{'region':<34}why")
    print("-" * 128)
    for i, z in enumerate(peaks, 1):
        w = ", ".join(z["hits"])
        if z["hard"]:
            w += "  AVOID " + ", ".join(z["hard"])
        print(f"{i:<4}{z['s']:<7.2f}"
              + f"{z['lat']:.0f},{z['lon']:.0f}".ljust(13)
              + f"{z['where']:<34}{w}")


if __name__ == "__main__":
    main()
