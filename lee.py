#!/usr/bin/env python3
"""
Relocation analysis after Julian Lee's documented method, contiguous US only.

CATEGORY A — verbatim from his own site and interview (julianlee.com):

  "I consider the Jim Lewis astrocartography map and all linemap products to
   be a really bad technique, unreliable, misleading, and even dangerous."
  "It would be more honest to say it's a way of plotting 2 percent of your
   horoscope onto a world map."
  "Linemaps give no information about your house of children, the house of
   money, and a great many other things."
  "I have found that the entire relocated natal chart 'works,' not just parts
   of it, and is more accurate and useful than any linemap."
  "In relocation we can change the way your planets sit in the houses, and
   house rulerships."
  "If you want to know how income will go in a new location, you have to look
   at the second house...the house of money. A 'Jupiter-Midheaven' won't save
   you if your actual money house is bad."
  "That means occupants of the house, ruler of the house, transits and
   progressions to the ruler, and transits to the occupants."
  "I stand by the Placidus House system, and feel it is most accurate in terms
   of the Relocated Natal rulerships. (I've tested it a lot in northern
   latitudes.)"
  "any relocated natal chart, just like a Natal, contains well over a hundred
   technical factors" ... "anywhere you live, there are always about a half
   dozen factors of vital importance"
  On the semi-sextile: "I always hear astrologers say that the semi-sextile
   (dodecile) is a 'minor aspect.'... it became obvious to me this is
   erroneous." And: "I would not recommend a location where the client's new
   forth house ruler was undergoing, say, a long-term progressing dodecile
   (semi-s.) from Saturn. That would make it a harsh location."
  He rejects blanket-negative treatment of outer planets.

CONSEQUENCE THAT DRIVES THIS FILE: no astrocartography line is computed
anywhere in it. Not one. Lee's geography comes from PLACIDUS house cusps and
house rulerships, which vary with BOTH latitude and longitude. So the regimes
here are two-dimensional regions, not the longitude bands every other method
in this repository produced.

CATEGORY C — not documented by Lee, flagged wherever used:
  - which rulership scheme (traditional vs modern). BOTH are computed and
    compared; he never states one.
  - orbs for the semi-sextile and quincunx. Reported at several orbs.
  - zodiac. Tropical assumed, since he is a Western astrologer using
    Placidus, but he does not state it.
  - nodes, Chiron, parans, local space: no documented position. Not used.
"""

import math
from collections import Counter

import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH | swe.FLG_SPEED
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
BLAT, BLON = 40.4406, -79.9959

IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
       ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
       ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
       ("Pluto", swe.PLUTO)]
BODIES = [n for n, _ in IDS]
P = {n: swe.calc_ut(JD, s, FL)[0][0] for n, s in IDS}
SPD = {n: swe.calc_ut(JD, s, FL)[0][3] for n, s in IDS}

TRAD = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
        "Pisces": "Jupiter"}
MOD = dict(TRAD, **{"Scorpio": "Pluto", "Aquarius": "Uranus", "Pisces": "Neptune"})

# Lee's stated priority houses: 1 identity, 2 money, 4 home, 5 children,
# 7 partnership, 10 career, 11 community. 9 for travel.
KEY = [1, 2, 4, 5, 7, 9, 10, 11]
NAMES = {1: "identity/body", 2: "money", 4: "home/roots", 5: "children",
         7: "partnership", 9: "travel/foreign", 10: "career", 11: "community"}


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


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


def chart(lat, lon, RUL=TRAD):
    cusp, am = swe.houses(JD, lat, lon, b"P")
    cusp = list(cusp)

    def hof(v):
        v %= 360.0
        for i in range(12):
            a, b = cusp[i], cusp[(i + 1) % 12]
            if (a < b and a <= v < b) or (a > b and (v >= a or v < b)):
                return i + 1
        return 12

    ph = {b: hof(P[b]) for b in BODIES}
    csign = {h: sg(cusp[h - 1]) for h in range(1, 13)}
    rul = {h: RUL[csign[h]] for h in range(1, 13)}
    occ = {h: [b for b in BODIES if ph[b] == h] for h in range(1, 13)}
    return dict(cusp=cusp, asc=am[0], mc=am[1], ic=(am[1] + 180) % 360,
                dsc=(am[0] + 180) % 360, ph=ph, csign=csign, rul=rul, occ=occ)


HR = "=" * 100


def stage1():
    print(HR)
    print("STAGE 1 — NATAL CHART, read with Lee's factor set (Placidus, his")
    print("          stated system; semi-sextile and quincunx treated as major)")
    print(HR)
    c = chart(BLAT, BLON)
    print(f"  ASC {fmt(c['asc'])}   MC {fmt(c['mc'])}   "
          f"IC {fmt(c['ic'])}   DSC {fmt(c['dsc'])}\n")
    print(f"  {'house':<7}{'cusp':<14}{'trad ruler':<12}{'in h':<7}"
          f"{'mod ruler':<12}{'in h':<7}occupants")
    for h in range(1, 13):
        tr, mr = TRAD[c["csign"][h]], MOD[c["csign"][h]]
        flag = "  <-- differs" if tr != mr else ""
        print(f"  {h:<7}{fmt(c['cusp'][h-1]):<14}{tr:<12}{c['ph'][tr]:<7}"
              f"{mr:<12}{c['ph'][mr]:<7}{', '.join(c['occ'][h]) or '-'}{flag}")
    print()
    print("  planets by Placidus house:")
    for b in BODIES:
        print(f"    {b:<10}{fmt(P[b]):<14}house {c['ph'][b]:<4}"
              f"{'Rx' if SPD[b] < 0 else ''}")
    print()
    print("  ASPECTS including the two Lee singles out as underrated.")
    print("  Ptolemaic at 8/10 deg; semi-sextile and quincunx shown at 3 orbs")
    print("  because he publishes no orb (Category C).")
    ASP = [("conjunction", 0, 10), ("semi-sextile", 30, None),
           ("sextile", 60, 6), ("square", 90, 8), ("trine", 120, 8),
           ("quincunx", 150, None), ("opposition", 180, 10)]
    for i in range(len(BODIES)):
        for j in range(i + 1, len(BODIES)):
            a, b = BODIES[i], BODIES[j]
            sep = abs(n180(P[a] - P[b]))
            for nm, deg, orb in ASP:
                if orb is None:
                    o = abs(sep - deg)
                    if o <= 6.0:
                        tag = ("TIGHT" if o <= 2 else "close" if o <= 4 else "wide")
                        print(f"    {a:<9}{nm:<14}{b:<10}orb {o:5.2f}°   [{tag}]")
                        break
                elif abs(sep - deg) <= orb:
                    print(f"    {a:<9}{nm:<14}{b:<10}orb {abs(sep-deg):5.2f}°")
                    break
    print()


def stage23():
    print(HR)
    print("STAGE 2 & 3 — THE PLACIDUS REGIMES ACROSS THE CONTIGUOUS US")
    print(HR)
    print("  No astrocartography line is computed. Regimes are defined by the")
    print("  thing Lee says matters: which sign sits on each house cusp (which")
    print("  fixes the house rulers) and which house each planet falls in.")
    print("  Placidus cusps move with BOTH latitude and longitude, so these are")
    print("  two-dimensional regions, not longitude bands.\n")

    grid = []
    la = 25.0
    while la <= 49.0:
        lo = -124.5
        while lo <= -67.0:
            c = chart(la, lo)
            sig = (tuple(c["rul"][h] for h in KEY),
                   tuple(c["ph"][b] for b in BODIES))
            grid.append((la, lo, sig, c))
            lo += 1.0
        la += 1.0
    print(f"  sampled {len(grid)} points at 1 degree\n")

    groups = {}
    for la, lo, sig, c in grid:
        groups.setdefault(sig, []).append((la, lo, c))
    print(f"  {len(groups)} materially distinct regimes exist in the "
          f"contiguous US by this definition.\n")

    big = sorted(groups.items(), key=lambda t: -len(t[1]))
    print("  REGIMES covering 2%+ of sampled land-box points:")
    for k, (sig, pts) in enumerate(big, 1):
        if len(pts) / len(grid) < 0.02:
            continue
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        c = pts[len(pts) // 2][2]
        print(f"\n  ▸ REGIME {k}   {len(pts)} pts ({100*len(pts)/len(grid):.0f}%)   "
              f"lat {min(lats):.0f}-{max(lats):.0f}N  lon {abs(max(lons)):.0f}-"
              f"{abs(min(lons)):.0f}W")
        print(f"      ASC {fmt(c['asc'])}  MC {fmt(c['mc'])}")
        for h in KEY:
            print(f"      h{h:<3}{NAMES[h]:<16}{c['csign'][h]:<13}"
                  f"ruler {c['rul'][h]:<9} in h{c['ph'][c['rul'][h]]:<4}"
                  f"occupants: {', '.join(c['occ'][h]) or '-'}")
    return groups, grid


def stage4(groups, grid):
    print("\n" + HR)
    print("STAGE 4 — LEDGERS vs PITTSBURGH. No score, no counting.")
    print(HR)
    base = chart(BLAT, BLON)
    big = [g for g in sorted(groups.items(), key=lambda t: -len(t[1]))
           if len(g[1]) / len(grid) >= 0.02]
    for k, (sig, pts) in enumerate(big, 1):
        c = pts[len(pts) // 2][2]
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        print(f"\n  ▸ REGIME {k}  (lat {min(lats):.0f}-{max(lats):.0f}N, "
              f"lon {abs(max(lons)):.0f}-{abs(min(lons)):.0f}W)")
        moved = [f"{b} h{base['ph'][b]}->h{c['ph'][b]}" for b in BODIES
                 if base["ph"][b] != c["ph"][b]]
        print(f"      planets changing house: {', '.join(moved) or 'none'}")
        rch = [f"h{h} {base['rul'][h]}->{c['rul'][h]}" for h in KEY
               if base["rul"][h] != c["rul"][h]]
        print(f"      key-house rulers changing: {', '.join(rch) or 'none'}")
        rmv = [f"h{h} ruler {c['rul'][h]} h{base['ph'][c['rul'][h]]}->"
               f"h{c['ph'][c['rul'][h]]}" for h in KEY
               if base["ph"][c["rul"][h]] != c["ph"][c["rul"][h]]
               and base["rul"][h] == c["rul"][h]]
        print(f"      same ruler, moved house: {', '.join(rmv) or 'none'}")
        ang = [b for b in BODIES if c["ph"][b] in (1, 4, 7, 10)]
        bang = [b for b in BODIES if base["ph"][b] in (1, 4, 7, 10)]
        print(f"      angular by Placidus: {', '.join(ang) or 'none'}"
              f"   (Pittsburgh: {', '.join(bang) or 'none'})")


def stage5(groups, grid):
    print("\n" + HR)
    print("STAGE 5 — CITIES, attached only now, by which regime contains them")
    print(HR)
    CITIES = [
        ("New York NY", 40.713, -74.006), ("Los Angeles CA", 34.052, -118.244),
        ("Chicago IL", 41.878, -87.630), ("Houston TX", 29.760, -95.370),
        ("Phoenix AZ", 33.448, -112.074), ("Philadelphia PA", 39.953, -75.165),
        ("San Antonio TX", 29.424, -98.494), ("San Diego CA", 32.716, -117.161),
        ("Dallas TX", 32.777, -96.797), ("Jacksonville FL", 30.332, -81.656),
        ("Austin TX", 30.267, -97.743), ("San Jose CA", 37.339, -121.895),
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
        ("Fargo ND", 46.877, -96.789), ("Duluth MN", 46.787, -92.101),
        ("Bangor ME", 44.801, -68.778), ("Burlington VT", 44.476, -73.212),
        ("Rapid City SD", 44.081, -103.231), ("Cheyenne WY", 41.140, -104.820),
        ("Spokane WA", 47.659, -117.426), ("Eureka CA", 40.802, -124.164),
        ("Amarillo TX", 35.222, -101.831), ("Miami FL", 25.762, -80.192),
        ("Corpus Christi TX", 27.801, -97.396), ("Reno NV", 39.530, -119.814),
        ("Bismarck ND", 46.808, -100.784), ("Missoula MT", 46.872, -113.994),
        ("Grand Junction CO", 39.064, -108.551), ("Wichita KS", 37.687, -97.336),
        ("Lubbock TX", 33.578, -101.855), ("Norfolk VA", 36.851, -76.286),
        ("Savannah GA", 32.081, -81.091), ("Richmond VA", 37.541, -77.436),
        ("Green Bay WI", 44.513, -88.016), ("Traverse City MI", 44.763, -85.620),
        ("Casper WY", 42.867, -106.313), ("Pocatello ID", 42.871, -112.445),
        ("Flagstaff AZ", 35.198, -111.651), ("Roswell NM", 33.394, -104.523),
        ("El Paso TX", 31.759, -106.487), ("Pueblo CO", 38.254, -104.609),
        ("Sioux Falls SD", 43.550, -96.700), ("Toledo OH", 41.654, -83.538),
    ]
    big = {}
    for k, (sig, pts) in enumerate(
            sorted(groups.items(), key=lambda t: -len(t[1])), 1):
        big[sig] = k
    rows = {}
    for nm, la, lo in CITIES:
        c = chart(la, lo)
        sig = (tuple(c["rul"][h] for h in KEY),
               tuple(c["ph"][b] for b in BODIES))
        rows.setdefault(big.get(sig, 999), []).append((nm, c))
    for k in sorted(rows):
        print(f"\n  ▸ REGIME {k if k != 999 else '(minor/transitional)'}")
        for nm, c in sorted(rows[k]):
            print(f"      {nm:<20}ASC {fmt(c['asc'])}  "
                  f"h1 rlr {c['rul'][1]}(h{c['ph'][c['rul'][1]]})  "
                  f"h2 rlr {c['rul'][2]}(h{c['ph'][c['rul'][2]]})  "
                  f"h4 rlr {c['rul'][4]}(h{c['ph'][c['rul'][4]]})  "
                  f"h7 rlr {c['rul'][7]}(h{c['ph'][c['rul'][7]]})")


def stage8():
    print("\n" + HR)
    print("STAGE 8 — SENSITIVITY on the choices Lee does not document")
    print(HR)
    print("  (a) RULERSHIP SCHEME. Lee never states traditional or modern.")
    print("      Where do the two disagree on a KEY house ruler?")
    T = [("Pittsburgh PA", 40.441, -79.996), ("Los Angeles CA", 34.052, -118.244),
         ("Chicago IL", 41.878, -87.630), ("Denver CO", 39.739, -104.990),
         ("Miami FL", 25.762, -80.192), ("Seattle WA", 47.606, -122.332),
         ("Bangor ME", 44.801, -68.778), ("Houston TX", 29.760, -95.370)]
    for nm, la, lo in T:
        ct, cm = chart(la, lo, TRAD), chart(la, lo, MOD)
        d = [f"h{h}: {ct['rul'][h]} vs {cm['rul'][h]}" for h in KEY
             if ct["rul"][h] != cm["rul"][h]]
        print(f"      {nm:<20}{'; '.join(d) or 'no disagreement on key houses'}")
    print()
    print("  (b) PLACIDUS vs WHOLE SIGN, for the same key houses.")
    print("      Lee states Placidus explicitly, so this is a robustness check,")
    print("      not a competing option.")
    for nm, la, lo in T:
        c = chart(la, lo)
        ai = S.index(sg(c["asc"]))
        ws_r = {h: TRAD[S[(ai + h - 1) % 12]] for h in KEY}
        d = [f"h{h}: Plac {c['rul'][h]} vs WS {ws_r[h]}" for h in KEY
             if c["rul"][h] != ws_r[h]]
        print(f"      {nm:<20}{'; '.join(d) or 'agree on all key houses'}")
    print()
    print("  (c) SEMI-SEXTILE / QUINCUNX ORB. Lee publishes none.")
    for orb in (2.0, 3.0, 5.0, 6.0):
        hits = []
        for i in range(len(BODIES)):
            for j in range(i + 1, len(BODIES)):
                a, b = BODIES[i], BODIES[j]
                sep = abs(n180(P[a] - P[b]))
                for nm2, deg in (("semi-sextile", 30), ("quincunx", 150)):
                    if abs(sep - deg) <= orb:
                        hits.append(f"{a}-{b} {nm2[:4]} {abs(sep-deg):.1f}")
        print(f"      orb {orb:.0f}°: {len(hits)} hits   {', '.join(hits) or '-'}")


if __name__ == "__main__":
    stage1()
    g, gr = stage23()
    stage4(g, gr)
    stage5(g, gr)
    stage8()
