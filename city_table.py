#!/usr/bin/env python3
"""
Cities attached to the three frozen maps. Six cells per city, no seventh.

  READING   what one specific framework says. Never "your chart says".
  MARGIN    east-west miles to the nearest boundary IN THAT SAME MAP that
            would change any of the four topics. It measures how far you
            could settle off-centre before the reading changes. It is NOT a
            quality measure.

No aggregation, no agreement count, no overall column. Each reading carries
its framework label.

  MAP A  [WS tropical]        whole sign, tropical, traditional rulers
  MAP B  [Placidus tropical]  Placidus, tropical, modern rulers (Lee)
  MAP C  [WS sidereal]        whole sign, sidereal Lahiri, traditional rulers

Topics: identity (h1), home (h4), travel (h9), career (h10). Structure per
topic is (ruler, ruler's house, occupants), held identical across maps.

CORRECTION BAKED IN: an earlier count treated the same boundary sampled at
three latitudes as three boundaries. Boundaries are now identified by their
CAUSE, and located separately at each city's own latitude.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH | swe.FLG_SPEED
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
       ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
       ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
       ("Pluto", swe.PLUTO)]
B = [n for n, _ in IDS]
TROPP = {n: swe.calc_ut(JD, s, FL)[0][0] for n, s in IDS}
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
AY = swe.get_ayanamsa_ut(JD)
SIDP = {n: (v - AY) % 360.0 for n, v in TROPP.items()}
TRAD = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
        "Pisces": "Jupiter"}
MOD = dict(TRAD, **{"Scorpio": "Pluto", "Aquarius": "Uranus", "Pisces": "Neptune"})
TOPIC = [1, 4, 9, 10]
TN = {1: "identity", 4: "home", 9: "travel", 10: "career"}

CITIES = [
    ("New York NY", 40.713, -74.006), ("Los Angeles CA", 34.052, -118.244),
    ("Chicago IL", 41.878, -87.630), ("Houston TX", 29.760, -95.370),
    ("Phoenix AZ", 33.448, -112.074), ("Philadelphia PA", 39.953, -75.165),
    ("San Antonio TX", 29.424, -98.494), ("San Diego CA", 32.716, -117.161),
    ("Dallas TX", 32.777, -96.797), ("Austin TX", 30.267, -97.743),
    ("Jacksonville FL", 30.332, -81.656), ("San Jose CA", 37.339, -121.895),
    ("Columbus OH", 39.961, -82.999), ("Charlotte NC", 35.227, -80.843),
    ("Indianapolis IN", 39.768, -86.158), ("Seattle WA", 47.606, -122.332),
    ("Denver CO", 39.739, -104.990), ("Boston MA", 42.360, -71.059),
    ("Portland OR", 45.515, -122.678), ("Las Vegas NV", 36.170, -115.140),
    ("Detroit MI", 42.331, -83.046), ("Memphis TN", 35.150, -90.049),
    ("Louisville KY", 38.253, -85.759), ("Milwaukee WI", 43.039, -87.907),
    ("Albuquerque NM", 35.084, -106.651), ("Tucson AZ", 32.222, -110.974),
    ("Fresno CA", 36.738, -119.787), ("Sacramento CA", 38.582, -121.494),
    ("Kansas City MO", 39.100, -94.579), ("Atlanta GA", 33.749, -84.388),
    ("Omaha NE", 41.257, -95.938), ("Raleigh NC", 35.780, -78.639),
    ("Minneapolis MN", 44.978, -93.265), ("Tampa FL", 27.951, -82.457),
    ("New Orleans LA", 29.951, -90.072), ("Cleveland OH", 41.500, -81.695),
    ("Pittsburgh PA", 40.441, -79.996), ("Salt Lake City UT", 40.761, -111.891),
    ("Boise ID", 43.615, -116.202), ("Billings MT", 45.783, -108.501),
    ("Bangor ME", 44.801, -68.778), ("Burlington VT", 44.476, -73.212),
    ("Rapid City SD", 44.081, -103.231), ("Cheyenne WY", 41.140, -104.820),
    ("Spokane WA", 47.659, -117.426), ("Eureka CA", 40.802, -124.164),
    ("Amarillo TX", 35.222, -101.831), ("Miami FL", 25.762, -80.192),
    ("Reno NV", 39.530, -119.814), ("Bismarck ND", 46.808, -100.784),
    ("Missoula MT", 46.872, -113.994), ("Grand Junction CO", 39.064, -108.551),
    ("Wichita KS", 37.687, -97.336), ("Norfolk VA", 36.851, -76.286),
    ("Savannah GA", 32.081, -81.091), ("Richmond VA", 37.541, -77.436),
    ("Green Bay WI", 44.513, -88.016), ("Casper WY", 42.867, -106.313),
    ("Flagstaff AZ", 35.198, -111.651), ("El Paso TX", 31.759, -106.487),
    ("Sioux Falls SD", 43.550, -96.700), ("Asheville NC", 35.595, -82.552),
    ("Santa Fe NM", 35.687, -105.938), ("Sarasota FL", 27.337, -82.531),
    ("Greenville SC", 34.853, -82.394), ("Portland ME", 43.659, -70.255),
    ("Duluth MN", 46.787, -92.101), ("Bakersfield CA", 35.373, -119.019),
    ("Santa Barbara CA", 34.421, -119.698), ("Knoxville TN", 35.961, -83.921),
    ("Oklahoma City OK", 35.468, -97.516), ("Tulsa OK", 36.154, -95.993),
    ("Des Moines IA", 41.587, -93.625), ("Lubbock TX", 33.578, -101.855),
    ("Bend OR", 44.058, -121.315), ("Medford OR", 42.327, -122.874),
    ("Prescott AZ", 34.540, -112.469), ("St. George UT", 37.096, -113.568),
    ("Traverse City MI", 44.763, -85.620), ("Roanoke VA", 37.271, -79.941),
]


def sg(x):
    return S[int((x % 360) // 30)]


def sig(lat, lon, mp):
    cusp, am = swe.houses(JD, lat, lon, b"P")
    cusp = list(cusp)
    if mp == "B":
        P, R = TROPP, MOD

        def hof(v):
            v %= 360.0
            for i in range(12):
                a, b = cusp[i], cusp[(i + 1) % 12]
                if (a < b and a <= v < b) or (a > b and (v >= a or v < b)):
                    return i + 1
            return 12
        csign = {h: sg(cusp[h - 1]) for h in range(1, 13)}
    else:
        P, R = (TROPP, TRAD) if mp == "A" else (SIDP, TRAD)
        asc = am[0] if mp == "A" else (am[0] - AY) % 360.0
        ai = S.index(sg(asc))

        def hof(v):
            return ((S.index(sg(v)) - ai) % 12) + 1
        csign = {h: S[(ai + h - 1) % 12] for h in range(1, 13)}
    ph = {b: hof(P[b]) for b in B}
    return tuple((R[csign[h]], ph[R[csign[h]]],
                  tuple(sorted(b for b in B if ph[b] == h))) for h in TOPIC)


def mi(lat, dlon):
    return abs(dlon) * 69.172 * math.cos(math.radians(lat))


def main():
    # enumerate regimes per map over a coarse grid, then label
    labels = {}
    for mp in ("A", "B", "C"):
        seen = {}
        la = 26.0
        while la <= 48.0:
            lo = -124.0
            while lo <= -68.0:
                s = sig(la, lo, mp)
                seen[s] = seen.get(s, 0) + 1
                lo += 1.0
            la += 1.0
        order = sorted(seen.items(), key=lambda t: -t[1])
        labels[mp] = {s: f"{mp}{i}" for i, (s, _) in enumerate(order, 1)}

    print("=" * 100)
    print("LEGEND — what each regime label means")
    print("=" * 100)
    tag = {"A": "[WS tropical]", "B": "[Placidus tropical]", "C": "[WS sidereal]"}
    for mp in ("A", "B", "C"):
        print(f"\n  MAP {mp}  {tag[mp]}   {len(labels[mp])} regimes in the contiguous US")
        for s, lab in sorted(labels[mp].items(), key=lambda t: int(t[1][1:])):
            if int(lab[1:]) > 8:
                continue
            parts = []
            for i, h in enumerate(TOPIC):
                r, rh, occ = s[i]
                parts.append(f"{TN[h]}: {r} h{rh}"
                             + (f" +{'/'.join(occ)}" if occ else ""))
            print(f"    {lab:<5}" + "  |  ".join(parts))

    print("\n" + "=" * 100)
    print("CITY TABLE — reading and margin per framework. No overall column.")
    print("=" * 100)
    print(f"  {'city':<20}{'MAP A':<8}{'margin':<9}{'MAP B':<8}{'margin':<9}"
          f"{'MAP C':<8}margin")
    rows = []
    for nm, la, lo in CITIES:
        cell = []
        for mp in ("A", "B", "C"):
            here = sig(la, lo, mp)
            lab = labels[mp].get(here, "?")
            # nearest boundary at THIS latitude
            best = 9e9
            for direction in (-1, 1):
                x = lo
                while -125.5 <= x <= -66.0:
                    x += direction * 0.05
                    if sig(la, x, mp) != here:
                        best = min(best, mi(la, x - lo))
                        break
            cell.append((lab, best))
        rows.append((nm, la, lo, cell))
    for nm, la, lo, cell in sorted(rows, key=lambda r: (r[3][0][0], -r[2])):
        out = ""
        for lab, d in cell:
            out += f"{lab:<8}{('>1500' if d > 1500 else f'{d:.0f} mi'):<9}"
        print(f"  {nm:<20}{out}")


if __name__ == "__main__":
    main()
