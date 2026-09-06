#!/usr/bin/env python3
"""
Where the lines that matter actually fall on the ground in the United States.

Two kinds of line, computed separately because they behave differently:

  MERIDIAN lines (MC / IC) are vertical. One terrestrial longitude, all
  latitudes. Distance from a city is a pure east-west distance.

  HORIZON lines (AC / DC) are curves. The longitude at which a body rises or
  sets changes with latitude, so each city needs its own solve.

Everything is in-mundo, which is what an astrocartography map draws. The
zodiacal orbs are reported alongside so the two conventions can be compared
instead of silently swapped.
"""

import math
import swisseph as swe

import natal

swe.set_ephe_path("/usr/share/swisseph")
S = natal.SIGNS
FL = swe.FLG_SWIEPH
D = natal.compute()
JD = D["jd"]
P = {n: D["planets"][n]["lon"] for n in D["planets"]}
SWE_ID = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
          "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
          "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE,
          "Pluto": swe.PLUTO, "North Node": swe.TRUE_NODE, "Chiron": swe.CHIRON}

# US metros, name / lat / lon / population of the metro area (2020 census)
CITIES = [
    ("New York NY", 40.713, -74.006, 20_140_000), ("Los Angeles CA", 34.052, -118.244, 13_200_000),
    ("Chicago IL", 41.878, -87.630, 9_619_000), ("Dallas TX", 32.777, -96.797, 7_637_000),
    ("Houston TX", 29.760, -95.370, 7_122_000), ("Washington DC", 38.907, -77.037, 6_385_000),
    ("Philadelphia PA", 39.953, -75.165, 6_245_000), ("Miami FL", 25.762, -80.192, 6_139_000),
    ("Atlanta GA", 33.749, -84.388, 6_089_000), ("Boston MA", 42.360, -71.059, 4_942_000),
    ("Phoenix AZ", 33.448, -112.074, 4_845_000), ("San Francisco CA", 37.775, -122.419, 4_749_000),
    ("Riverside CA", 33.954, -117.396, 4_599_000), ("Detroit MI", 42.331, -83.046, 4_392_000),
    ("Seattle WA", 47.606, -122.332, 4_018_000), ("Minneapolis MN", 44.978, -93.265, 3_690_000),
    ("San Diego CA", 32.716, -117.161, 3_298_000), ("Tampa FL", 27.951, -82.457, 3_175_000),
    ("Denver CO", 39.739, -104.990, 2_963_000), ("St. Louis MO", 38.627, -90.199, 2_820_000),
    ("Baltimore MD", 39.290, -76.612, 2_844_000), ("Charlotte NC", 35.227, -80.843, 2_660_000),
    ("Orlando FL", 28.538, -81.379, 2_673_000), ("San Antonio TX", 29.424, -98.494, 2_558_000),
    ("Portland OR", 45.515, -122.678, 2_512_000), ("Sacramento CA", 38.582, -121.494, 2_397_000),
    ("Pittsburgh PA", 40.441, -79.996, 2_370_000), ("Las Vegas NV", 36.170, -115.140, 2_265_000),
    ("Austin TX", 30.267, -97.743, 2_283_000), ("Cincinnati OH", 39.103, -84.512, 2_257_000),
    ("Kansas City MO", 39.100, -94.579, 2_193_000), ("Columbus OH", 39.961, -82.999, 2_138_000),
    ("Cleveland OH", 41.500, -81.695, 2_088_000), ("Indianapolis IN", 39.768, -86.158, 2_111_000),
    ("San Jose CA", 37.339, -121.895, 2_000_000), ("Nashville TN", 36.163, -86.781, 1_989_000),
    ("Virginia Beach VA", 36.853, -75.978, 1_799_000), ("Providence RI", 41.824, -71.413, 1_676_000),
    ("Jacksonville FL", 30.332, -81.656, 1_605_000), ("Milwaukee WI", 43.039, -87.907, 1_575_000),
    ("Oklahoma City OK", 35.468, -97.516, 1_425_000), ("Raleigh NC", 35.780, -78.639, 1_413_000),
    ("Memphis TN", 35.150, -90.049, 1_337_000), ("Richmond VA", 37.541, -77.436, 1_314_000),
    ("Louisville KY", 38.253, -85.759, 1_285_000), ("New Orleans LA", 29.951, -90.072, 1_271_000),
    ("Salt Lake City UT", 40.761, -111.891, 1_258_000), ("Hartford CT", 41.764, -72.685, 1_213_000),
    ("Buffalo NY", 42.887, -78.878, 1_166_000), ("Birmingham AL", 33.519, -86.810, 1_115_000),
    ("Rochester NY", 43.161, -77.611, 1_090_000), ("Grand Rapids MI", 42.963, -85.668, 1_087_000),
    ("Tucson AZ", 32.222, -110.974, 1_043_000), ("Honolulu HI", 21.307, -157.858, 1_016_000),
    ("Tulsa OK", 36.154, -95.993, 1_015_000), ("Fresno CA", 36.738, -119.787, 1_009_000),
    ("Omaha NE", 41.257, -95.938, 967_000), ("Bridgeport CT", 41.187, -73.195, 957_000),
    ("Albuquerque NM", 35.084, -106.651, 916_000), ("Albany NY", 42.652, -73.756, 899_000),
    ("Knoxville TN", 35.961, -83.921, 879_000), ("El Paso TX", 31.759, -106.487, 869_000),
    ("Bakersfield CA", 35.373, -119.019, 909_000), ("Baton Rouge LA", 30.451, -91.187, 870_000),
    ("Columbia SC", 34.001, -81.035, 838_000), ("Charleston SC", 32.777, -79.931, 800_000),
    ("Greenville SC", 34.853, -82.394, 928_000), ("Boise ID", 43.615, -116.202, 764_000),
    ("Dayton OH", 39.759, -84.192, 814_000), ("Stockton CA", 37.958, -121.291, 779_000),
    ("Little Rock AR", 34.746, -92.290, 748_000), ("Colorado Springs CO", 38.834, -104.821, 755_000),
    ("Des Moines IA", 41.587, -93.625, 709_000), ("Spokane WA", 47.659, -117.426, 600_000),
    ("Wichita KS", 37.687, -97.336, 647_000), ("Toledo OH", 41.654, -83.538, 646_000),
    ("Madison WI", 43.073, -89.401, 680_000), ("Syracuse NY", 43.048, -76.147, 662_000),
    ("Harrisburg PA", 40.274, -76.885, 592_000), ("Chattanooga TN", 35.046, -85.310, 566_000),
    ("Scranton PA", 41.409, -75.663, 570_000), ("Asheville NC", 35.595, -82.552, 470_000),
    ("Reno NV", 39.530, -119.814, 490_000), ("Santa Barbara CA", 34.421, -119.698, 449_000),
    ("Fort Collins CO", 40.585, -105.084, 360_000), ("Savannah GA", 32.081, -81.091, 405_000),
    ("Santa Fe NM", 35.687, -105.938, 155_000), ("Sedona AZ", 34.870, -111.761, 10_000),
    ("Flagstaff AZ", 35.198, -111.651, 145_000), ("St. George UT", 37.096, -113.568, 181_000),
    ("Prescott AZ", 34.540, -112.469, 240_000), ("Durango CO", 37.275, -107.880, 56_000),
    ("Farmington NM", 36.728, -108.219, 121_000), ("Gallup NM", 35.528, -108.742, 72_000),
    ("Silver City NM", 32.770, -108.280, 28_000), ("Show Low AZ", 34.254, -110.030, 11_000),
    ("Provo UT", 40.234, -111.659, 672_000), ("Ogden UT", 41.223, -111.973, 694_000),
    ("Idaho Falls ID", 43.492, -112.034, 155_000), ("Bozeman MT", 45.680, -111.039, 118_000),
    ("Great Falls MT", 47.506, -111.301, 84_000), ("Helena MT", 46.589, -112.039, 82_000),
    ("Casper WY", 42.867, -106.313, 80_000), ("Grand Junction CO", 39.064, -108.551, 156_000),
    ("Portland ME", 43.659, -70.255, 551_000), ("Burlington VT", 44.476, -73.212, 225_000),
    ("Manchester NH", 42.996, -71.455, 423_000), ("Sarasota FL", 27.337, -82.531, 834_000),
    ("Naples FL", 26.142, -81.795, 376_000), ("Fort Myers FL", 26.640, -81.873, 787_000),
    ("Lexington KY", 38.041, -84.504, 517_000), ("Ann Arbor MI", 42.281, -83.743, 372_000),
    ("Lansing MI", 42.733, -84.556, 542_000), ("Erie PA", 42.129, -80.085, 270_000),
    ("Roanoke VA", 37.271, -79.941, 315_000), ("Greensboro NC", 36.073, -79.792, 780_000),
    ("Wilmington NC", 34.226, -77.945, 300_000), ("Mobile AL", 30.695, -88.040, 430_000),
    ("Palm Springs CA", 33.830, -116.545, 48_000), ("Scottsdale AZ", 33.494, -111.926, 242_000),
    ("Anchorage AK", 61.218, -149.900, 398_000),
]

MERIDIAN = [("Venus", "MC"), ("Sun", "MC"), ("Jupiter", "IC"), ("Neptune", "IC")]
HORIZON = [("Saturn", "DSC"), ("Moon", "DSC"), ("North Node", "ASC"),
           ("Chiron", "ASC"), ("Pluto", "IC")]


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def eq(pl):
    xx, _ = swe.calc_ut(JD, SWE_ID[pl], FL | swe.FLG_EQUATORIAL)
    return xx[0], xx[1]


GMST = swe.sidtime(JD) * 15.0


def meridian(pl, which):
    ra, _ = eq(pl)
    mc = n180(ra - GMST)
    return mc if which == "MC" else n180(mc + 180.0)


def horizon_lon(pl, lat, which):
    """Longitude at which the body is exactly on the given horizon angle."""
    ra, dec = eq(pl)
    x = -math.tan(math.radians(lat)) * math.tan(math.radians(dec))
    if abs(x) > 1.0:
        return None                       # circumpolar: never rises or sets here
    h0 = math.degrees(math.acos(x))       # hour angle at rise (-) / set (+)
    h = -h0 if which == "ASC" else h0
    return n180(ra + h - GMST)


def km(lat, dlon_deg):
    return abs(dlon_deg) * 111.32 * math.cos(math.radians(lat))


def main():
    print("=" * 104)
    print("MERIDIAN LINES — vertical, one longitude, every latitude")
    print("=" * 104)
    for pl, which in MERIDIAN:
        L = meridian(pl, which)
        print(f"\n  ▸ {pl} {which} line at {abs(L):.3f}°W"
              f"   (natal {natal.fmt(P[pl])})")
        near = sorted(CITIES, key=lambda c: abs(n180(c[2] - L)))[:9]
        print(f"    {'city':<20}{'pop':>10}   {'Δlon':>8}{'miles':>8}   "
              f"zodiacal orb to the angle")
        for nm, la, lo, pop in near:
            d = n180(lo - L)
            cs, am = swe.houses(JD, la, lo, b"P")
            ang = am[1] if which == "MC" else (am[1] + 180) % 360
            print(f"    {nm:<20}{pop:>10,}   {d:>+8.2f}{km(la, d)*0.6214:>8.0f}   "
                  f"{abs(n180(P[pl]-ang)):.2f}°")

    print("\n" + "=" * 104)
    print("HORIZON LINES — curves; the longitude moves with latitude")
    print("=" * 104)
    for pl, which in HORIZON:
        if which == "IC":
            continue
        print(f"\n  ▸ {pl} {which} curve   (natal {natal.fmt(P[pl])})")
        rows = []
        for nm, la, lo, pop in CITIES:
            L = horizon_lon(pl, la, "ASC" if which == "ASC" else "DSC")
            if L is None or not -126 <= L <= -66:
                continue
            rows.append((abs(n180(lo - L)), nm, la, lo, pop, L))
        rows.sort()
        if not rows:
            print("    the curve does not pass near any city in the list")
            continue
        lats = sorted({round(r[2]) for r in rows})
        print(f"    {'city':<20}{'pop':>10}   {'curve at':>10}{'Δlon':>8}"
              f"{'miles':>8}   zodiacal orb to the angle")
        for d, nm, la, lo, pop, L in rows[:8]:
            cs, am = swe.houses(JD, la, lo, b"P")
            ang = am[0] if which == "ASC" else (am[0] + 180) % 360
            print(f"    {nm:<20}{pop:>10,}   {abs(L):>9.2f}W{n180(lo-L):>+8.2f}"
                  f"{km(la, n180(lo-L))*0.6214:>8.0f}   {abs(n180(P[pl]-ang)):.2f}°")
        print(f"    curve longitude by latitude: " + ", ".join(
            f"{la}N {abs(horizon_lon(pl, la, 'ASC' if which=='ASC' else 'DSC')):.2f}W"
            for la in (25, 30, 35, 40, 45)
            if horizon_lon(pl, la, 'ASC' if which == 'ASC' else 'DSC') is not None))

    print("\n" + "=" * 104)
    print("THE SUN–VENUS BAND — the only stretch of the US where both culminate")
    print("=" * 104)
    a, b = meridian("Sun", "MC"), meridian("Venus", "MC")
    lo_, hi_ = min(a, b), max(a, b)
    print(f"  Sun MC {abs(a):.3f}W   Venus MC {abs(b):.3f}W   "
          f"band is {abs(a-b):.2f}° of longitude wide "
          f"(~{km(34, a-b)*0.6214:.0f} miles at 34N)")
    inside = [c for c in CITIES if lo_ <= c[2] <= hi_]
    print(f"  {'city':<20}{'pop':>10}   {'Sun-MC':>8}{'Ven-MC':>8}   position in the band")
    for nm, la, lo, pop in sorted(inside, key=lambda c: -c[3]):
        cs, am = swe.houses(JD, la, lo, b"P")
        mc = am[1]
        f = (lo - lo_) / (hi_ - lo_)
        print(f"  {nm:<20}{pop:>10,}   {abs(n180(P['Sun']-mc)):>7.2f}°"
              f"{abs(n180(P['Venus']-mc)):>7.2f}°   "
              f"{'|' + '-'*int(f*24) + '●' + '-'*(24-int(f*24)) + '|'}")


if __name__ == "__main__":
    main()
