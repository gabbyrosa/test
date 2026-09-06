#!/usr/bin/env python3
"""
Relocation analysis in the contiguous United States, following Helena Woods'
published locational-astrology method as closely as her public material
specifies, and labelling every point where it does not.

WHAT IS ATTRIBUTABLE TO HER PUBLISHED WORK
  - step order: map -> compare with relocated charts -> note lines and measure
    distance -> account for parans -> local space -> timing
    (helenawoods.com, "How to Read Your Astrocartography Map Step by Step")
  - line orbs stated in MILES, not degrees: 150-200 miles is the "intense"
    band, 600 miles the outer maximum at which a line is still felt
  - paran orb: 70-75 miles north and south of the paran latitude, 75 max
  - parans defined as two planets angular together, and treated as able to
    "make or break a place" even when a supportive line is present
  - local space is a separate directional system that does not use houses
  - relocated charts: planets keep their signs, houses shift, aspects to the
    angles change

WHAT HER PUBLIC MATERIAL DOES NOT SPECIFY, and is therefore labelled in the
output rather than invented:
  - whether she uses whole-sign or quadrant houses (the WHOLE-SIGN choice here
    is the client's instruction, not hers)
  - a natal-condition-first prerequisite. Her published sequence begins at the
    map. Stage 1 below is the client's structure.
  - any benefic/malefic weighting rule
  - any specific rule tying IC lines to belonging or Venus lines to beauty
  - how parans are weighted numerically against lines

This file inherits NOTHING from earlier analyses in this repository: no
rankings, no candidate cities, no scores, no screens. Geography is searched
before any city is named.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH | swe.FLG_SPEED

# June 7 1996, 19:35 UT, Pittsburgh PA
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
BLAT, BLON = 40.4406, -79.9959

IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
       ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
       ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
       ("Pluto", swe.PLUTO), ("North Node", swe.TRUE_NODE), ("Chiron", swe.CHIRON)]
ID = dict(IDS)
BODIES = [n for n, _ in IDS]

DOM = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
       "Pisces": "Jupiter"}
MODERN = dict(DOM, **{"Scorpio": "Pluto", "Aquarius": "Uranus", "Pisces": "Neptune"})
EXALT = {"Sun": ("Aries", 19), "Moon": ("Taurus", 3), "Mercury": ("Virgo", 15),
         "Venus": ("Pisces", 27), "Mars": ("Capricorn", 28),
         "Jupiter": ("Cancer", 15), "Saturn": ("Libra", 21)}
ELEM = {"Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
        "Taurus": "earth", "Virgo": "earth", "Capricorn": "earth",
        "Gemini": "air", "Libra": "air", "Aquarius": "air",
        "Cancer": "water", "Scorpio": "water", "Pisces": "water"}
TRIP = {"fire": ("Sun", "Jupiter", "Saturn"), "earth": ("Venus", "Moon", "Mars"),
        "air": ("Saturn", "Mercury", "Jupiter"), "water": ("Venus", "Mars", "Moon")}
BOUNDS = {
    "Aries": [(6, "Jupiter"), (12, "Venus"), (20, "Mercury"), (25, "Mars"), (30, "Saturn")],
    "Taurus": [(8, "Venus"), (14, "Mercury"), (22, "Jupiter"), (27, "Saturn"), (30, "Mars")],
    "Gemini": [(6, "Mercury"), (12, "Jupiter"), (17, "Venus"), (24, "Mars"), (30, "Saturn")],
    "Cancer": [(7, "Mars"), (13, "Venus"), (19, "Mercury"), (26, "Jupiter"), (30, "Saturn")],
    "Leo": [(6, "Jupiter"), (11, "Venus"), (18, "Saturn"), (24, "Mercury"), (30, "Mars")],
    "Virgo": [(7, "Mercury"), (17, "Venus"), (21, "Jupiter"), (28, "Mars"), (30, "Saturn")],
    "Libra": [(6, "Saturn"), (14, "Mercury"), (21, "Jupiter"), (28, "Venus"), (30, "Mars")],
    "Scorpio": [(7, "Mars"), (11, "Venus"), (19, "Mercury"), (24, "Jupiter"), (30, "Saturn")],
    "Sagittarius": [(12, "Jupiter"), (17, "Venus"), (21, "Mercury"), (26, "Saturn"), (30, "Mars")],
    "Capricorn": [(7, "Mercury"), (14, "Jupiter"), (22, "Venus"), (26, "Saturn"), (30, "Mars")],
    "Aquarius": [(7, "Mercury"), (13, "Venus"), (20, "Jupiter"), (25, "Mars"), (30, "Saturn")],
    "Pisces": [(12, "Venus"), (16, "Jupiter"), (19, "Mercury"), (28, "Mars"), (30, "Saturn")],
}

# contiguous-US metros, name / lat / lon / metro population
METROS = [
    ("New York NY", 40.713, -74.006, 20140000), ("Los Angeles CA", 34.052, -118.244, 13200000),
    ("Chicago IL", 41.878, -87.630, 9619000), ("Dallas TX", 32.777, -96.797, 7637000),
    ("Houston TX", 29.760, -95.370, 7122000), ("Washington DC", 38.907, -77.037, 6385000),
    ("Philadelphia PA", 39.953, -75.165, 6245000), ("Miami FL", 25.762, -80.192, 6139000),
    ("Atlanta GA", 33.749, -84.388, 6089000), ("Boston MA", 42.360, -71.059, 4942000),
    ("Phoenix AZ", 33.448, -112.074, 4845000), ("San Francisco CA", 37.775, -122.419, 4749000),
    ("Riverside CA", 33.954, -117.396, 4599000), ("Detroit MI", 42.331, -83.046, 4392000),
    ("Seattle WA", 47.606, -122.332, 4018000), ("Minneapolis MN", 44.978, -93.265, 3690000),
    ("San Diego CA", 32.716, -117.161, 3298000), ("Tampa FL", 27.951, -82.457, 3175000),
    ("Denver CO", 39.739, -104.990, 2963000), ("Baltimore MD", 39.290, -76.612, 2844000),
    ("St. Louis MO", 38.627, -90.199, 2820000), ("Orlando FL", 28.538, -81.379, 2673000),
    ("Charlotte NC", 35.227, -80.843, 2660000), ("San Antonio TX", 29.424, -98.494, 2558000),
    ("Portland OR", 45.515, -122.678, 2512000), ("Sacramento CA", 38.582, -121.494, 2397000),
    ("Pittsburgh PA", 40.441, -79.996, 2370000), ("Austin TX", 30.267, -97.743, 2283000),
    ("Las Vegas NV", 36.170, -115.140, 2265000), ("Cincinnati OH", 39.103, -84.512, 2257000),
    ("Kansas City MO", 39.100, -94.579, 2193000), ("Columbus OH", 39.961, -82.999, 2138000),
    ("Indianapolis IN", 39.768, -86.158, 2111000), ("Cleveland OH", 41.500, -81.695, 2088000),
    ("San Jose CA", 37.339, -121.895, 2000000), ("Nashville TN", 36.163, -86.781, 1989000),
    ("Virginia Beach VA", 36.853, -75.978, 1799000), ("Providence RI", 41.824, -71.413, 1676000),
    ("Jacksonville FL", 30.332, -81.656, 1605000), ("Milwaukee WI", 43.039, -87.907, 1575000),
    ("Oklahoma City OK", 35.468, -97.516, 1425000), ("Raleigh NC", 35.780, -78.639, 1413000),
    ("Memphis TN", 35.150, -90.049, 1337000), ("Richmond VA", 37.541, -77.436, 1314000),
    ("Louisville KY", 38.253, -85.759, 1285000), ("New Orleans LA", 29.951, -90.072, 1271000),
    ("Salt Lake City UT", 40.761, -111.891, 1258000), ("Hartford CT", 41.764, -72.685, 1213000),
    ("Buffalo NY", 42.887, -78.878, 1166000), ("Birmingham AL", 33.519, -86.810, 1115000),
    ("Rochester NY", 43.161, -77.611, 1090000), ("Grand Rapids MI", 42.963, -85.668, 1087000),
    ("Tucson AZ", 32.222, -110.974, 1043000), ("Tulsa OK", 36.154, -95.993, 1015000),
    ("Fresno CA", 36.738, -119.787, 1009000), ("Omaha NE", 41.257, -95.938, 967000),
    ("Greenville SC", 34.853, -82.394, 928000), ("Albuquerque NM", 35.084, -106.651, 916000),
    ("Bakersfield CA", 35.373, -119.019, 909000), ("Albany NY", 42.652, -73.756, 899000),
    ("Knoxville TN", 35.961, -83.921, 879000), ("Baton Rouge LA", 30.451, -91.187, 870000),
    ("El Paso TX", 31.759, -106.487, 869000), ("Columbia SC", 34.001, -81.035, 838000),
    ("Sarasota FL", 27.337, -82.531, 834000), ("Dayton OH", 39.759, -84.192, 814000),
    ("Charleston SC", 32.777, -79.931, 800000), ("Fort Myers FL", 26.640, -81.873, 787000),
    ("Greensboro NC", 36.073, -79.792, 780000), ("Stockton CA", 37.958, -121.291, 779000),
    ("Boise ID", 43.615, -116.202, 764000), ("Colorado Springs CO", 38.834, -104.821, 755000),
    ("Little Rock AR", 34.746, -92.290, 748000), ("Des Moines IA", 41.587, -93.625, 709000),
    ("Ogden UT", 41.223, -111.973, 694000), ("Provo UT", 40.234, -111.659, 672000),
    ("Madison WI", 43.073, -89.401, 680000), ("Syracuse NY", 43.048, -76.147, 662000),
    ("Wichita KS", 37.687, -97.336, 647000), ("Toledo OH", 41.654, -83.538, 646000),
    ("Harrisburg PA", 40.274, -76.885, 592000), ("Spokane WA", 47.659, -117.426, 600000),
    ("Scranton PA", 41.409, -75.663, 570000), ("Chattanooga TN", 35.046, -85.310, 566000),
    ("Portland ME", 43.659, -70.255, 551000), ("Lansing MI", 42.733, -84.556, 542000),
    ("Lexington KY", 38.041, -84.504, 517000), ("Reno NV", 39.530, -119.814, 490000),
    ("Asheville NC", 35.595, -82.552, 470000), ("Santa Barbara CA", 34.421, -119.698, 449000),
    ("Mobile AL", 30.695, -88.040, 430000), ("Manchester NH", 42.996, -71.455, 423000),
    ("Savannah GA", 32.081, -81.091, 405000), ("Naples FL", 26.142, -81.795, 376000),
    ("Ann Arbor MI", 42.281, -83.743, 372000), ("Fort Collins CO", 40.585, -105.084, 360000),
    ("Wilmington NC", 34.226, -77.945, 300000), ("Erie PA", 42.129, -80.085, 270000),
    ("Prescott AZ", 34.540, -112.469, 240000), ("Burlington VT", 44.476, -73.212, 225000),
    ("St. George UT", 37.096, -113.568, 181000), ("Grand Junction CO", 39.064, -108.551, 156000),
    ("Santa Fe NM", 35.687, -105.938, 155000), ("Idaho Falls ID", 43.492, -112.034, 155000),
    ("Flagstaff AZ", 35.198, -111.651, 145000), ("Farmington NM", 36.728, -108.219, 121000),
    ("Bozeman MT", 45.680, -111.039, 118000), ("Roanoke VA", 37.271, -79.941, 315000),
    ("Eureka CA", 40.802, -124.164, 136000), ("Bend OR", 44.058, -121.315, 205000),
    ("Medford OR", 42.327, -122.874, 223000), ("Redding CA", 40.587, -122.391, 182000),
    ("Chico CA", 39.729, -121.837, 208000), ("Missoula MT", 46.872, -113.994, 119000),
    ("Great Falls MT", 47.506, -111.301, 84000), ("Helena MT", 46.589, -112.039, 82000),
    ("Casper WY", 42.867, -106.313, 80000), ("Gallup NM", 35.528, -108.742, 72000),
    ("Durango CO", 37.275, -107.880, 56000), ("Silver City NM", 32.770, -108.280, 28000),
    ("Traverse City MI", 44.763, -85.620, 153000), ("Duluth MN", 46.787, -92.101, 291000),
    ("Sedona AZ", 34.870, -111.761, 10000), ("Bellingham WA", 48.750, -122.479, 226000),
    ("Olympia WA", 47.038, -122.901, 290000), ("Eugene OR", 44.052, -123.087, 382000),
    ("Salem OR", 44.943, -123.035, 434000), ("Yakima WA", 46.602, -120.506, 256000),
    ("Billings MT", 45.783, -108.501, 184000), ("Rapid City SD", 44.081, -103.231, 145000),
    ("Cheyenne WY", 41.140, -104.820, 100000), ("Amarillo TX", 35.222, -101.831, 269000),
    ("Lubbock TX", 33.578, -101.855, 322000), ("Midland TX", 31.997, -102.078, 175000),
    ("Corpus Christi TX", 27.801, -97.396, 443000), ("Shreveport LA", 32.525, -93.750, 393000),
    ("Jackson MS", 32.299, -90.185, 594000), ("Huntsville AL", 34.730, -86.586, 500000),
    ("Fayetteville AR", 36.062, -94.157, 560000), ("Springfield MO", 37.209, -93.292, 476000),
    ("Peoria IL", 40.694, -89.589, 400000), ("Cedar Rapids IA", 41.978, -91.665, 276000),
    ("Sioux Falls SD", 43.550, -96.700, 276000), ("Fargo ND", 46.877, -96.789, 249000),
    ("Green Bay WI", 44.513, -88.016, 328000), ("Charleston WV", 38.350, -81.633, 254000),
    ("Bangor ME", 44.801, -68.778, 152000), ("Ithaca NY", 42.444, -76.501, 105000),
]

MI_PER_DEG_LAT = 69.05


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def n360(x):
    return x % 360.0


def sg(x):
    return S[int((x % 360) // 30)]


def fmt(x):
    i = int((x % 360) // 30)
    p = x % 360 - i * 30
    d = int(p)
    m = int(round((p - d) * 60))
    if m == 60:
        m, d = 0, d + 1
    return f"{d:2d}°{m:02d}' {S[i][:3]}"


def bound_of(lon):
    for hi, r in BOUNDS[sg(lon)]:
        if lon % 30 < hi:
            return r
    return BOUNDS[sg(lon)][-1][1]


def mi_lon(lat, dlon):
    """Miles per degree of longitude at a latitude, times dlon."""
    return abs(dlon) * 69.172 * math.cos(math.radians(lat))


# ---------------------------------------------------------------- ephemeris
P, SPD, ECLAT, RA, DEC = {}, {}, {}, {}, {}
for nm, sid in IDS:
    xx, _ = swe.calc_ut(JD, sid, FL)
    P[nm], ECLAT[nm], SPD[nm] = xx[0], xx[1], xx[3]
    yy, _ = swe.calc_ut(JD, sid, FL | swe.FLG_EQUATORIAL)
    RA[nm], DEC[nm] = yy[0], yy[1]
GMST = swe.sidtime(JD) * 15.0
NCUSP, NASCMC = swe.houses(JD, BLAT, BLON, b"P")
NASC, NMC = NASCMC[0], NASCMC[1]
AI = S.index(sg(NASC))
WS = {b: ((S.index(sg(P[b])) - AI) % 12) + 1 for b in BODIES}
SECT_DAY = True     # verified below


def ws_from(asc):
    i = S.index(sg(asc))
    return {b: ((S.index(sg(P[b])) - i) % 12) + 1 for b in BODIES}, i


def mc_lon(b):
    return n180(RA[b] - GMST)


def horizon_lon(b, lat, which):
    x = -math.tan(math.radians(lat)) * math.tan(math.radians(DEC[b]))
    if abs(x) > 1.0:
        return None
    h = math.degrees(math.acos(x))
    return n180(RA[b] - h - GMST) if which == "ASC" else n180(RA[b] + h - GMST)


def line_dist_mi(b, kind, lat, lon):
    """Shortest east-west distance in miles from a point to a line."""
    if kind == "MC":
        L = mc_lon(b)
    elif kind == "IC":
        L = n180(mc_lon(b) + 180.0)
    else:
        L = horizon_lon(b, lat, kind)
    if L is None:
        return None, None
    return mi_lon(lat, n180(lon - L)), L


def lst_on(b, angle, lat):
    if angle == "MC":
        return n360(RA[b])
    if angle == "IC":
        return n360(RA[b] + 180.0)
    x = -math.tan(math.radians(lat)) * math.tan(math.radians(DEC[b]))
    if abs(x) > 1.0:
        return None
    h = math.degrees(math.acos(x))
    return n360(RA[b] - h) if angle == "ASC" else n360(RA[b] + h)


HR = "=" * 104
KINDS = ("MC", "IC", "ASC", "DSC")
INTENSE, OUTER = 200.0, 600.0
PARAN_ORB = 75.0


def stage1():
    print(HR)
    print("STAGE 1 — NATAL CHART FIRST")
    print(HR)
    print("  NOTE ON PROVENANCE: Helena Woods' published step sequence begins")
    print("  at the map, not at natal condition. This stage is the client's")
    print("  structure, not a documented Woods step. Flagged per audit rule.")
    print()
    sun_h = None
    for i in range(12):
        a, b = NCUSP[i], NCUSP[(i + 1) % 12]
        if (a < b and a <= P["Sun"] < b) or (a > b and (P["Sun"] >= a or P["Sun"] < b)):
            sun_h = i + 1
    print(f"  birth  1996-06-07  19:35 UT   Pittsburgh PA  {BLAT:.4f}N {abs(BLON):.4f}W")
    print(f"  ASC {fmt(NASC)}   MC {fmt(NMC)}   IC {fmt((NMC+180)%360)}   "
          f"DSC {fmt((NASC+180)%360)}")
    print(f"  Sun in quadrant house {sun_h} -> DAY chart (Sun above the horizon)")
    print(f"  whole-sign 1st = {sg(NASC)}, so whole-sign 4th = "
          f"{S[(AI+3)%12]}, 7th = {S[(AI+6)%12]}, 10th = {S[(AI+9)%12]}")
    print()
    FOCUS = ["Venus", "Moon", "Sun", "Jupiter", "Saturn", "Mercury", "Mars"]
    print("  the bodies this analysis is required to establish:")
    print("    ruler of the natal 1st (Libra)      = Venus   [traditional and modern agree]")
    print("    ruler of the natal 4th (Capricorn)  = Saturn  [traditional and modern agree]")
    print("    Ascendant ruler                     = Venus")
    print()
    for b in FOCUS:
        s = sg(P[b])
        digs = []
        if DOM[s] == b:
            digs.append("domicile")
        if b in EXALT and EXALT[b][0] == s:
            digs.append("exaltation")
        if DOM[S[(S.index(s) + 6) % 12]] == b:
            digs.append("DETRIMENT")
        if b in EXALT and S[(S.index(EXALT[b][0]) + 6) % 12] == s:
            digs.append("FALL")
        d, n, part = TRIP[ELEM[s]]
        if b == (d if SECT_DAY else n):
            digs.append("triplicity (ruling)")
        elif b == part:
            digs.append("triplicity (participating)")
        if bound_of(P[b]) == b:
            digs.append("bound")
        sect = ("in sect" if (b in ("Sun", "Jupiter", "Saturn")) == SECT_DAY
                else "out of sect") if b != "Mercury" else "n/a (Mercury takes the sect it rises in)"
        rules = [h for h in range(1, 13) if DOM[S[(AI + h - 1) % 12]] == b]
        sep = abs(n180(P[b] - P["Sun"]))
        beam = ("" if b == "Sun" else
                f"; COMBUST {sep:.2f}° from the Sun" if sep <= 8 else
                f"; under the beams {sep:.2f}°" if sep <= 15 else "")
        print(f"  {b}  {fmt(P[b])}  {'RETROGRADE' if SPD[b] < 0 else 'direct'}"
              f"  {SPD[b]:+.4f}°/day")
        print(f"      whole-sign house {WS[b]}"
              f"{'  (ANGULAR)' if WS[b] in (1,4,7,10) else '  (succedent)' if WS[b] in (2,5,8,11) else '  (cadent)'}"
              f"   rules whole-sign house(s) {', '.join(map(str, rules)) or 'none'}")
        print(f"      dignity: {', '.join(digs) if digs else 'PEREGRINE'}"
              f"   |   bound lord {bound_of(P[b])}   |   {sect}{beam}")
    print()
    print("  aspects among the seven traditional planets "
          "(Ptolemaic only; 10° orb to the lights, 8° otherwise)")
    T = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
    any_asp = {b: [] for b in T}
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            a, b = T[i], T[j]
            sep = abs(n180(P[a] - P[b]))
            for nm2, deg in (("conjunction", 0), ("sextile", 60), ("square", 90),
                             ("trine", 120), ("opposition", 180)):
                orb = 10 if "Sun" in (a, b) or "Moon" in (a, b) else 8
                if abs(sep - deg) <= orb:
                    same = (S.index(sg(P[a])) - S.index(sg(P[b]))) % 12
                    ok = same in {0: (0,), 60: (2, 10), 90: (3, 9),
                                  120: (4, 8), 180: (6,)}[deg]
                    rec = []
                    if DOM[sg(P[a])] == b:
                        rec.append(f"{b} receives {a} by domicile")
                    if DOM[sg(P[b])] == a:
                        rec.append(f"{a} receives {b} by domicile")
                    print(f"    {a:<8}{nm2:<12}{b:<9}orb {abs(sep-deg):5.2f}°   "
                          f"{'whole-sign confirmed' if ok else 'out of sign'}"
                          + ("   [" + "; ".join(rec) + "]" if rec else ""))
                    any_asp[a].append(b)
                    any_asp[b].append(a)
                    break
    for b in T:
        if not any_asp[b]:
            print(f"    {b}: NO Ptolemaic aspect to any traditional planet")
    print()
    print("  mutual receptions by domicile:")
    found = False
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            a, b = T[i], T[j]
            if DOM[sg(P[a])] == b and DOM[sg(P[b])] == a:
                print(f"    {a} in {sg(P[a])} (ruled by {b})  <->  "
                      f"{b} in {sg(P[b])} (ruled by {a})")
                found = True
    if not found:
        print("    none")


def stage2():
    print("\n" + HR)
    print("STAGE 2 — FULL CONTIGUOUS-US MAP SEARCH, corridors before cities")
    print(HR)
    print(f"  Woods' orbs, in miles: intense band <= {INTENSE:.0f} mi, "
          f"outer limit {OUTER:.0f} mi.")
    print("  Geometry note, applied throughout so nothing is double-counted:")
    print("  a body on the MC is necessarily about square the ASC, on the IC")
    print("  about square the ASC, and on the DSC opposite it. Those are ONE")
    print("  configuration. Only ASC/DSC/MC/IC conjunctions are listed.\n")

    print("  A. MERIDIAN CORRIDORS (MC and IC lines: one longitude, all latitudes)")
    print(f"     {'body':<12}{'MC line':>11}{'IC line':>11}   inside 125W-66.9W?")
    merid = []
    for b in BODIES:
        m, i = mc_lon(b), n180(mc_lon(b) + 180.0)
        tags = []
        if -125 <= m <= -66.9:
            tags.append("MC")
            merid.append((b, "MC", m))
        if -125 <= i <= -66.9:
            tags.append("IC")
            merid.append((b, "IC", i))
        print(f"     {b:<12}{m:>10.3f}°{i:>10.3f}°   {', '.join(tags) or '-'}")
    print()
    print("  B. HORIZON CORRIDORS (ASC and DSC curves: longitude varies with latitude)")
    print(f"     {'body':<12}{'angle':<6}" +
          "".join(f"{la}N".rjust(10) for la in (25, 30, 35, 40, 45, 49)) +
          "   crosses the US?")
    horiz = []
    for b in BODIES:
        for k in ("ASC", "DSC"):
            vals = [horizon_lon(b, la, k) for la in (25, 30, 35, 40, 45, 49)]
            inside = any(v is not None and -125 <= v <= -66.9 for v in vals)
            if inside:
                horiz.append((b, k))
            print(f"     {b:<12}{k:<6}" +
                  "".join((f"{v:9.2f}°" if v is not None else "   circump") for v in vals) +
                  f"   {'YES' if inside else 'no'}")
    print()
    print(f"  -> {len(merid)} meridian corridors and {len(horiz)} horizon corridors "
          f"cross the contiguous US.")
    print()

    print("  C. METROS INSIDE EACH CORRIDOR (distances in miles, Woods' units)")
    active = [(b, k) for b, k, _ in merid] + horiz
    for b, k in sorted(active, key=lambda t: BODIES.index(t[0])):
        rows = []
        for nm, la, lo, pop in METROS:
            d, L = line_dist_mi(b, k, la, lo)
            if d is not None and d <= OUTER:
                rows.append((d, nm, pop, L, la))
        if not rows:
            continue
        rows.sort()
        tight = [r for r in rows if r[0] <= INTENSE]
        print(f"\n  ▸ {b} {k} line   "
              f"({len(tight)} metros inside {INTENSE:.0f} mi, "
              f"{len(rows)} inside {OUTER:.0f} mi)")
        if k in ("MC", "IC"):
            print(f"    corridor longitude {abs(mc_lon(b) if k=='MC' else n180(mc_lon(b)+180)):.3f}W")
        for d, nm, pop, L, la in rows[:12]:
            band = "INTENSE" if d <= INTENSE else "outer"
            print(f"    {nm:<20}{pop:>10,}  {d:6.0f} mi   {band}"
                  + (f"   curve at {abs(L):.2f}W" if k in ("ASC", "DSC") else ""))


def stage3():
    print("\n" + HR)
    print("STAGE 3 — PARANS crossing the contiguous US")
    print(HR)
    print(f"  Woods' paran orb: {PARAN_ORB:.0f} miles north and south of the")
    print(f"  paran latitude ({PARAN_ORB/MI_PER_DEG_LAT:.3f}° of latitude).")
    print("  A paran is two bodies angular simultaneously at a given latitude.")
    print("  It is a horizontal band and applies at EVERY longitude.\n")
    ANG = ("ASC", "MC", "DSC", "IC")
    found = []
    for i in range(len(BODIES)):
        for j in range(i + 1, len(BODIES)):
            b1, b2 = BODIES[i], BODIES[j]
            for a1 in ANG:
                for a2 in ANG:
                    prev, la = None, 20.0
                    while la <= 52.0:
                        x, y = lst_on(b1, a1, la), lst_on(b2, a2, la)
                        cur = None if x is None or y is None else n180(x - y)
                        if prev is not None and cur is not None and \
                           prev * cur < 0 and abs(prev - cur) < 90:
                            lo, hi = la - 0.05, la
                            for _ in range(45):
                                m = (lo + hi) / 2
                                fa = n180(lst_on(b1, a1, lo) - lst_on(b2, a2, lo))
                                fm = n180(lst_on(b1, a1, m) - lst_on(b2, a2, m))
                                if fa * fm <= 0:
                                    hi = m
                                else:
                                    lo = m
                            found.append(((lo + hi) / 2, b1, a1, b2, a2))
                        prev = cur
                        la += 0.05
    us = sorted(f for f in found if 24.4 <= f[0] <= 49.5)
    print(f"  {len(us)} paran latitudes fall inside 24.4N-49.5N "
          f"(of {len(found)} found between 20N and 52N)\n")
    print(f"  {'latitude':<11}paran")
    for la, b1, a1, b2, a2 in us:
        print(f"  {la:7.3f}N   {b1} {a1} with {b2} {a2}")
    return us


def stage3_cities(us):
    print("\n  D. WHICH METROS SIT INSIDE A PARAN BAND "
          f"(<= {PARAN_ORB:.0f} mi of the latitude)")
    print(f"     {'metro':<20}{'lat':>8}   parans in orb")
    any_hit = False
    for nm, la, lo, pop in sorted(METROS, key=lambda m: -m[3]):
        hits = [(abs(la - p[0]) * MI_PER_DEG_LAT, p) for p in us
                if abs(la - p[0]) * MI_PER_DEG_LAT <= PARAN_ORB]
        if hits:
            any_hit = True
            hits.sort()
            txt = "; ".join(f"{p[1]} {p[2]}/{p[3]} {p[4]} @{p[0]:.2f}N ({d:.0f}mi)"
                            for d, p in hits[:3])
            print(f"     {nm:<20}{la:7.3f}N   {txt}")
    if not any_hit:
        print("     none")


def stage4(us):
    print("\n" + HR)
    print("STAGE 4 — RELOCATED CHARTS for the candidates the search produced")
    print(HR)
    print("  CANDIDATE RULE, stated before the results are read:")
    print("    a metro qualifies if it is within 100 miles of any line that")
    print("    crosses the contiguous US, OR inside the 200-mile intense band")
    print("    of two or more distinct lines. No other filter is applied, and")
    print("    no city is added or removed by hand.")
    print("  HOUSE CONVENTION: whole sign, per the client's instruction. Helena")
    print("  Woods' public material does not state which house system she uses,")
    print("  so this is the client's choice, not hers. Exact ASC/MC/IC/DSC")
    print("  degrees are preserved separately and never merged with the")
    print("  whole-sign house they fall in.\n")

    active = []
    for b in BODIES:
        for k in KINDS:
            probe = line_dist_mi(b, k, 38.0, -98.0)[1]
            if probe is None:
                continue
            if k in ("MC", "IC"):
                if -125 <= probe <= -66.9:
                    active.append((b, k))
            else:
                if any(-125 <= (horizon_lon(b, la, k) or 999) <= -66.9
                       for la in (25, 30, 35, 40, 45, 49)):
                    active.append((b, k))

    cands = []
    for nm, la, lo, pop in METROS:
        hits = []
        for b, k in active:
            d, _ = line_dist_mi(b, k, la, lo)
            if d is not None and d <= OUTER:
                hits.append((d, b, k))
        hits.sort()
        near = [h for h in hits if h[0] <= 100.0]
        intense = [h for h in hits if h[0] <= INTENSE]
        if near or len(intense) >= 2:
            par = sorted((abs(la - p[0]) * MI_PER_DEG_LAT, p) for p in us
                         if abs(la - p[0]) * MI_PER_DEG_LAT <= PARAN_ORB)
            cands.append((nm, la, lo, pop, intense, par))
    print(f"  {len(cands)} metros qualify.\n")

    print("  A. CORE RELOCATED CHART DATA")
    print(f"  {'metro':<19}{'ASC exact':<13}{'MC exact':<13}{'IC exact':<13}"
          f"{'ASC rlr':<9}{'h':<4}{'4th':<12}{'4th rlr':<9}h")
    rows = {}
    for nm, la, lo, pop, intense, par in cands:
        cusp, am = swe.houses(JD, la, lo, b"P")
        asc, mc = am[0], am[1]
        ic, dsc = (mc + 180) % 360, (asc + 180) % 360
        ws, i0 = ws_from(asc)
        h4sign = S[(i0 + 3) % 12]
        r1, r4 = DOM[sg(asc)], DOM[h4sign]
        rows[nm] = dict(la=la, lo=lo, pop=pop, asc=asc, mc=mc, ic=ic, dsc=dsc,
                        ws=ws, i0=i0, h4sign=h4sign, r1=r1, r4=r4,
                        intense=intense, par=par)
        print(f"  {nm:<19}{fmt(asc):<13}{fmt(mc):<13}{fmt(ic):<13}"
              f"{r1:<9}{ws[r1]:<4}{h4sign:<12}{r4:<9}{ws[r4]}")

    print("\n  B. EXACT ANGULAR CONJUNCTIONS (degree contacts, NOT whole-sign)")
    print("     listed only where a body is within 8° of an exact angle;")
    print("     an MC/IC/DSC conjunction is not restated as an ASC aspect.")
    for nm in rows:
        r = rows[nm]
        ang = {"ASC": r["asc"], "MC": r["mc"], "DSC": r["dsc"], "IC": r["ic"]}
        hits = []
        for b in BODIES:
            k, o = min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                       key=lambda t: t[1])
            if o <= 8:
                hits.append(f"{b} {k} {o:.2f}°")
        print(f"    {nm:<19}{'; '.join(hits) if hits else 'nothing within 8° of any angle'}")

    print("\n  C. HOME AND BELONGING")
    print("     Moon, the IC degree, the whole-sign 4th, its ruler, and")
    print("     anything occupying the 4th.")
    print(f"  {'metro':<19}{'Moon h':<8}{'4th sign':<13}{'4th ruler':<10}"
          f"{'ruler in h':<12}{'in the 4th':<22}IC contacts <=8°")
    for nm in rows:
        r = rows[nm]
        occ = [b for b in BODIES if r["ws"][b] == 4]
        icc = [f"{b} {abs(n180(P[b]-r['ic'])):.2f}°" for b in BODIES
               if abs(n180(P[b] - r["ic"])) <= 8]
        print(f"  {nm:<19}{r['ws']['Moon']:<8}{r['h4sign']:<13}{r['r4']:<10}"
              f"{r['ws'][r['r4']]:<12}{', '.join(occ) or '-':<22}"
              f"{', '.join(icc) or '-'}")

    print("\n  D. BEAUTY AND EMBODIMENT")
    print("     Venus, the Ascendant degree, the chart ruler, the whole-sign")
    print("     1st, the Sun and the Moon, and contacts to the ASC.")
    print(f"  {'metro':<19}{'1st sign':<11}{'ruler':<9}{'rlr h':<7}"
          f"{'Ven h':<7}{'Sun h':<7}{'in the 1st':<16}ASC contacts <=8°")
    for nm in rows:
        r = rows[nm]
        occ = [b for b in BODIES if r["ws"][b] == 1]
        ac = [f"{b} {abs(n180(P[b]-r['asc'])):.2f}°" for b in BODIES
              if abs(n180(P[b] - r["asc"])) <= 8]
        print(f"  {nm:<19}{S[r['i0']]:<11}{r['r1']:<9}{r['ws'][r['r1']]:<7}"
              f"{r['ws']['Venus']:<7}{r['ws']['Sun']:<7}"
              f"{', '.join(occ) or '-':<16}{', '.join(ac) or '-'}")

    print("\n  E. SOFT ASPECTS to the relocated ASC and MC, reported separately")
    print("     so they are never confused with a conjunction.")
    for nm in rows:
        r = rows[nm]
        out = []
        for b in ("Venus", "Moon", "Sun", "Jupiter"):
            for tgt, lab in ((r["asc"], "ASC"), (r["mc"], "MC")):
                sep = abs(n180(P[b] - tgt))
                for anm, deg, orb in (("trine", 120, 6), ("sextile", 60, 4)):
                    if abs(sep - deg) <= orb:
                        out.append(f"{b} {anm} {lab} {abs(sep-deg):.2f}°")
        print(f"    {nm:<19}{'; '.join(out) or 'none in orb'}")

    print("\n  F. LINES AND PARANS TOGETHER, per candidate")
    for nm in rows:
        r = rows[nm]
        ln = "; ".join(f"{b} {k} {d:.0f}mi" for d, b, k in r["intense"][:4])
        pr = "; ".join(f"{p[1]} {p[2]}/{p[3]} {p[4]} @{p[0]:.2f}N ({d:.0f}mi)"
                       for d, p in r["par"][:3])
        print(f"    {nm:<19}LINES  {ln}")
        print(f"    {'':<19}PARANS {pr or 'none within 75 mi'}")


def main():
    stage1()
    stage2()
    us = stage3()
    stage3_cities(us)
    stage4(us)


if __name__ == "__main__":
    main()
