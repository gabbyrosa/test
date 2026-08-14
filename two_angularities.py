#!/usr/bin/env python3
"""
The distinction the previous pass collapsed: whole-sign angularity is not
degree angularity, and they have completely different geography.

WHOLE-SIGN angularity depends only on which sign rises. In the contiguous US
that is a binary: Virgo west of 100.224548W, Libra east of it. So a planet's
whole-sign house is constant across half a continent.

DEGREE angularity depends on proximity to the actual angle, which is a line on
the map. It is continuous and local.

Conflating them makes a claim that is true of the entire western US sound like
a claim about a 280-mile band in Arizona. This file keeps them apart, and also
audits the essential-dignity claim precisely rather than loosely.
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

DOMICILE = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
            "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus",
            "Scorpio": "Mars", "Sagittarius": "Jupiter", "Capricorn": "Saturn",
            "Aquarius": "Saturn", "Pisces": "Jupiter"}
EXALT = {"Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo", "Venus": "Pisces",
         "Mars": "Capricorn", "Jupiter": "Cancer", "Saturn": "Libra"}
ELEMENT = {"Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
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
CHALDEAN = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
TRAD = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
BODIES = TRAD + ["Uranus", "Neptune", "Pluto", "North Node", "Chiron"]
DAY = True

CITIES = [
    # west of 100.224548W  ->  Virgo rises
    ("Seattle WA", 47.606, -122.332), ("Portland OR", 45.515, -122.678),
    ("San Francisco CA", 37.775, -122.419), ("Sacramento CA", 38.582, -121.494),
    ("San Jose CA", 37.339, -121.895), ("Santa Barbara CA", 34.421, -119.698),
    ("Los Angeles CA", 34.052, -118.244), ("San Diego CA", 32.716, -117.161),
    ("Palm Springs CA", 33.830, -116.545), ("Las Vegas NV", 36.170, -115.140),
    ("St. George UT", 37.096, -113.568), ("Prescott AZ", 34.540, -112.469),
    ("Phoenix AZ", 33.448, -112.074), ("Scottsdale AZ", 33.494, -111.926),
    ("Salt Lake City UT", 40.761, -111.891), ("Sedona AZ", 34.870, -111.761),
    ("Tucson AZ", 32.222, -110.974), ("Santa Fe NM", 35.687, -105.938),
    ("Denver CO", 39.739, -104.990), ("Boise ID", 43.615, -116.202),
    ("Bozeman MT", 45.680, -111.039),
    # east of the boundary  ->  Libra rises
    ("Austin TX", 30.267, -97.743), ("Minneapolis MN", 44.978, -93.265),
    ("Kansas City MO", 39.100, -94.579), ("New Orleans LA", 29.951, -90.072),
    ("St. Louis MO", 38.627, -90.199), ("Chicago IL", 41.878, -87.630),
    ("Nashville TN", 36.163, -86.781), ("Atlanta GA", 33.749, -84.388),
    ("Detroit MI", 42.331, -83.046), ("Columbus OH", 39.961, -82.999),
    ("Asheville NC", 35.595, -82.552), ("Greenville SC", 34.853, -82.394),
    ("Sarasota FL", 27.337, -82.531), ("Tampa FL", 27.951, -82.457),
    ("Charleston SC", 32.777, -79.931), ("Pittsburgh PA", 40.441, -79.996),
    ("Miami FL", 25.762, -80.192), ("Washington DC", 38.907, -77.037),
    ("New York NY", 40.713, -74.006), ("Boston MA", 42.360, -71.059),
    ("Portland ME", 43.659, -70.255),
]


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def bound_of(lon):
    for hi, r in BOUNDS[sg(lon)]:
        if lon % 30 < hi:
            return r
    return BOUNDS[sg(lon)][-1][1]


def face_of(lon):
    return CHALDEAN[int(lon // 10) % 7]


def audit(pl):
    lon = P[pl]
    s = sg(lon)
    has = []
    if DOMICILE[s] == pl:
        has.append("domicile")
    if EXALT.get(pl) == s:
        has.append("exaltation")
    d, n, part = TRIP[ELEMENT[s]]
    if pl == (d if DAY else n):
        has.append("triplicity (ruling)")
    elif pl == part:
        has.append("triplicity (participating)")
    if bound_of(lon) == pl:
        has.append("bound")
    if face_of(lon) == pl:
        has.append("face")
    deb = []
    if DOMICILE[S[(S.index(s) + 6) % 12]] == pl:
        deb.append("detriment")
    if pl in EXALT and S[(S.index(EXALT[pl]) + 6) % 12] == s:
        deb.append("fall")
    return has, deb, bound_of(lon), face_of(lon), (d if DAY else n), part


HR = "=" * 106


def main():
    # ------------------------------------------------------------ dignity audit
    print(HR)
    print("PRECISE ESSENTIAL-DIGNITY AUDIT  (replacing a sentence that was too strong)")
    print(HR)
    print(f"  {'planet':<9}{'position':<15}{'dignities held':<34}"
          f"{'debility':<14}{'bound lord':<12}face lord")
    for pl in TRAD:
        has, deb, b, f, tri_r, tri_p = audit(pl)
        print(f"  {pl:<9}{natal.fmt(P[pl]):<15}"
              f"{', '.join(has) if has else 'NONE (peregrine)':<34}"
              f"{', '.join(deb) if deb else '-':<14}{b:<12}{f}")
    print()
    print("  domicile held by  : " + (", ".join(p for p in TRAD if audit(p)[0] and "domicile" in audit(p)[0]) or "nobody"))
    print("  exaltation held by: " + (", ".join(p for p in TRAD if "exaltation" in audit(p)[0]) or "nobody"))
    print("  bound held by     : " + (", ".join(p for p in TRAD if "bound" in audit(p)[0]) or "nobody"))
    print("  face held by      : " + (", ".join(p for p in TRAD if "face" in audit(p)[0]) or "nobody"))
    print("  triplicity held by: " + (", ".join(
        f"{p} ({[h for h in audit(p)[0] if 'triplicity' in h][0]})"
        for p in TRAD if any("triplicity" in h for h in audit(p)[0])) or "nobody"))
    print()

    # ------------------------------------------------- the Moon-Jupiter structure
    print(HR)
    print("THE MOON-JUPITER SUPPORT STRUCTURE, in full")
    print(HR)
    sep = abs(n180(P["Moon"] - P["Jupiter"]))
    print(f"  Moon {natal.fmt(P['Moon'])}   sextile   Jupiter {natal.fmt(P['Jupiter'])}"
          f"   orb {abs(sep-60):.2f}°  (separating)")
    print(f"    Jupiter rules Pisces, so Jupiter RECEIVES the Moon by domicile.")
    print(f"    Jupiter is the IN-SECT benefic in this day chart.")
    print(f"    Jupiter is in FALL in Capricorn and retrograde, so the receiver is")
    print(f"    itself compromised. The relationship is sound; the receiver is not strong.")
    print(f"    Moon holds participating triplicity in water: a real, minor, essential dignity.")
    print()
    print(f"    bound lord of the Moon    : {bound_of(P['Moon'])}")
    print(f"    bound lord of Jupiter     : {bound_of(P['Jupiter'])}")
    if bound_of(P["Moon"]) == bound_of(P["Jupiter"]) == "Venus":
        print(f"    -> VENUS is the bound lord of BOTH ends of the chart's only")
        print(f"       receptive aspect. Venus holds no dignity of its own, but it is")
        print(f"       the minor dignity lord presiding over the chart's best structure.")
    print()
    print(f"  where each end of that sextile becomes angular BY DEGREE:")
    gmst = swe.sidtime(JD) * 15.0
    for pl, sid in (("Moon", swe.MOON), ("Jupiter", swe.JUPITER)):
        xx, _ = swe.calc_ut(JD, sid, FL | swe.FLG_EQUATORIAL)
        ra, dec = xx[0], xx[1]
        mc = n180(ra - gmst)
        ic = n180(mc + 180)
        line = []
        for la in (30, 35, 40, 45):
            x = -math.tan(math.radians(la)) * math.tan(math.radians(dec))
            if abs(x) <= 1:
                h = math.degrees(math.acos(x))
                line.append(f"{la}N: rise {abs(n180(ra-h-gmst)):.1f}W / "
                            f"set {abs(n180(ra+h-gmst)):.1f}W")
        print(f"    {pl:<9}MC {abs(mc):7.3f}W   IC {abs(ic):7.3f}W")
        print(f"    {'':<9}" + " | ".join(line))
    print()

    # --------------------------------------------- the two kinds of angularity
    print(HR)
    print("WHOLE-SIGN vs DEGREE ANGULARITY, kept apart")
    print(HR)
    print("  WS = whole-sign house (binary across the country). "
          "deg = orb to the nearest actual angle.")
    print()
    print(f"  {'city':<19}{'rises':<7}"
          f"{'Venus':<16}{'Sun':<16}{'Jupiter':<16}{'Moon':<14}chart ruler")
    for nm, la, lo in CITIES:
        cs, am = swe.houses(JD, la, lo, b"P")
        asc, mc = am[0], am[1]
        ang = {"AS": asc, "MC": mc, "DS": (asc + 180) % 360, "IC": (mc + 180) % 360}
        ai = S.index(sg(asc))

        def cell(pl):
            ws = ((S.index(sg(P[pl])) - ai) % 12) + 1
            k, o = min(((k, abs(n180(P[pl] - v))) for k, v in ang.items()),
                       key=lambda t: t[1])
            mark = "*" if o <= 3 else "+" if o <= 8 else " "
            return f"WS{ws:<2} {k}{o:5.1f}{mark}"

        r = DOMICILE[sg(asc)]
        rws = ((S.index(sg(P[r])) - ai) % 12) + 1
        print(f"  {nm:<19}{sg(asc)[:3]:<7}"
              f"{cell('Venus'):<16}{cell('Sun'):<16}{cell('Jupiter'):<16}"
              f"{cell('Moon'):<14}{r} WS{rws}")
    print()
    print("  * = within 3° of the angle   + = within 8°")
    print()

    print(HR)
    print("WHAT IS INVARIANT vs WHAT ACTUALLY DISCRIMINATES")
    print(HR)
    east = [c for c in CITIES if c[2] > -100.224548]
    west = [c for c in CITIES if c[2] < -100.224548]
    print(f"  EAST ({len(east)} cities incl. Pittsburgh) - identical in every one of them:")
    print("    Libra rises | Venus is chart ruler, rules WS 1+8, sits WS 9 cadent")
    print("    Sun WS 9 in its JOY, rules WS 11 | Jupiter WS 4 | Saturn WS 7 | Moon WS 6 rules 10")
    print("    Venus/Mercury mutual reception intact")
    print("    -> none of this can tell one eastern city from another, and none of it")
    print("       is a reason to leave Pittsburgh, which has all of it already.")
    print()
    print(f"  WEST ({len(west)} cities) - identical in every one of them:")
    print("    Virgo rises | Mercury is chart ruler, rules WS 1+10, sits WS 9 cadent")
    print("    Venus WS 10 ANGULAR, rules WS 2+9 | Sun WS 10 ANGULAR, rules WS 12")
    print("    Jupiter WS 5 | Saturn WS 8 | Moon WS 7 angular | Sun out of its joy")
    print("    -> Venus in the whole-sign 10th is true of the ENTIRE west, not of a band.")
    print()
    print("  degree-angular contacts that actually vary by city:")
    for nm, la, lo in CITIES:
        cs, am = swe.houses(JD, la, lo, b"P")
        asc, mc = am[0], am[1]
        ang = {"ASC": asc, "MC": mc, "DSC": (asc + 180) % 360, "IC": (mc + 180) % 360}
        hits = []
        for b in BODIES:
            k, o = min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                       key=lambda t: t[1])
            if o <= 3.0:
                hits.append(f"{b} {k} {o:.2f}°")
        if hits:
            print(f"    {nm:<19}{'; '.join(hits)}")
    print()
    print("  cities in the list with NO body within 3° of any angle:")
    quiet = []
    for nm, la, lo in CITIES:
        cs, am = swe.houses(JD, la, lo, b"P")
        asc, mc = am[0], am[1]
        ang = {"ASC": asc, "MC": mc, "DSC": (asc + 180) % 360, "IC": (mc + 180) % 360}
        if not any(min(abs(n180(P[b] - v)) for v in ang.values()) <= 3.0 for b in BODIES):
            quiet.append(nm)
    print("    " + (", ".join(quiet) if quiet else "none"))


if __name__ == "__main__":
    main()
