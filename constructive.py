#!/usr/bin/env python3
"""
Which US relocations most constructively alter the whole traditional chart.

The hard part of this question is defining "constructively" without smuggling
in a wish. Every earlier file in this repo failed that test in some way: it
picked Venus, or beauty, or a composite score I invented.

So this file uses only criteria that are DOCTRINE in the Hellenistic
tradition, applies them to the complete chart, and reports a LEDGER of gains
and losses rather than a number. Where doctrine does not rank two items
against each other, this file does not either; it prints both and says so.

The doctrinal criteria used, and nothing else:

  1  benefics are helped by angularity, malefics harmed by it
  2  sect weights that: in a day chart Jupiter is the more helpful benefic and
     Mars the more harmful malefic, so angularizing Jupiter matters more than
     angularizing Venus, and angularizing Mars would matter more than Saturn
  3  the seven planetary joys (Mercury 1, Moon 3, Venus 5, Mars 6, Sun 9,
     Jupiter 11, Saturn 12) are fixed house assignments
  4  the "dark" or inoperative places are those that do not aspect the
     Ascendant: 2, 6, 8, 12
  5  a benefic ruling the Ascendant is preferable to a neutral or malefic one
  6  the Lots of Fortune and Spirit, and the condition of their rulers
  7  the ruler of the Ascendant should be in an advantageous place

Three independent layers come out of this, and they have different geography:

  LAYER A  the rising sign. Binary in the contiguous US. Sets every
           whole-sign house and every relocated rulership at once.
  LAYER B  the Lots. Fortune and Spirit sit at fixed degree offsets from the
           Ascendant, so their houses flip at specific Ascendant degrees,
           which are specific meridians. Continuous, and nothing else moves.
  LAYER C  degree angularity. The actual astrocartography lines.
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

DOM = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
       "Pisces": "Jupiter"}
JOY = {"Mercury": 1, "Moon": 3, "Venus": 5, "Mars": 6, "Sun": 9,
       "Jupiter": 11, "Saturn": 12}
ANGULAR, SUCCEDENT = {1, 4, 7, 10}, {2, 5, 8, 11}
DARK = {2, 6, 8, 12}                       # do not aspect the Ascendant
TRAD = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
# day chart: Jupiter is the in-sect benefic, Mars the out-of-sect malefic
ROLE = {"Jupiter": "benefic, IN SECT", "Venus": "benefic, out of sect",
        "Saturn": "malefic, IN SECT", "Mars": "malefic, OUT OF SECT",
        "Sun": "sect light", "Moon": "light, out of sect",
        "Mercury": "neutral"}
GMST = swe.sidtime(JD) * 15.0
SWE_ID = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
          "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
          "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE,
          "Pluto": swe.PLUTO, "North Node": swe.TRUE_NODE, "Chiron": swe.CHIRON}

FORT_OFF = (P["Moon"] - P["Sun"]) % 360.0      # Lot of Fortune, day formula
SPIR_OFF = (P["Sun"] - P["Moon"]) % 360.0      # Lot of Spirit, day formula


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def place(h):
    return ("angular" if h in ANGULAR else
            "succedent" if h in SUCCEDENT else "cadent")


def config(asc):
    """Everything the whole-sign layer determines, given an Ascendant."""
    ai = S.index(sg(asc))
    ws = {p: ((S.index(sg(P[p])) - ai) % 12) + 1 for p in P}
    hsign = {h: S[(ai + h - 1) % 12] for h in range(1, 13)}
    rules = {}
    for h in range(1, 13):
        rules.setdefault(DOM[hsign[h]], []).append(h)
    fort = (asc + FORT_OFF) % 360.0
    spir = (asc + SPIR_OFF) % 360.0
    return dict(ai=ai, ws=ws, hsign=hsign, rules=rules,
                ruler=DOM[hsign[1]],
                fort=fort, fort_h=((S.index(sg(fort)) - ai) % 12) + 1,
                fort_lord=DOM[sg(fort)],
                spir=spir, spir_h=((S.index(sg(spir)) - ai) % 12) + 1,
                spir_lord=DOM[sg(spir)])


def ledger(a, b, la, lb):
    """Doctrinal gains and losses moving from configuration a to b."""
    gains, losses, same = [], [], []
    for p in TRAD:
        ha, hb = a["ws"][p], b["ws"][p]
        if ha == hb:
            continue
        pa, pb = place(ha), place(hb)
        benefic = p in ("Jupiter", "Venus")
        malefic = p in ("Mars", "Saturn")
        msg = f"{p} ({ROLE[p]}) h{ha} {pa} -> h{hb} {pb}"
        if benefic and pa != "angular" and pb == "angular":
            gains.append(msg + "  [benefic gains an angle]")
        elif benefic and pa == "angular" and pb != "angular":
            losses.append(msg + "  [benefic loses an angle]")
        elif malefic and pa == "angular" and pb != "angular":
            gains.append(msg + "  [malefic leaves an angle]")
        elif malefic and pa != "angular" and pb == "angular":
            losses.append(msg + "  [malefic gains an angle]")
        elif ha in DARK and hb not in DARK:
            gains.append(msg + "  [leaves a dark place]")
        elif hb in DARK and ha not in DARK:
            losses.append(msg + "  [enters a dark place]")
        else:
            same.append(msg)
        if JOY.get(p) == ha and JOY.get(p) != hb:
            losses.append(f"{p} leaves its joy (h{JOY[p]})")
        if JOY.get(p) == hb and JOY.get(p) != ha:
            gains.append(f"{p} enters its joy (h{JOY[p]})")
    if a["ruler"] != b["ruler"]:
        ra, rb = a["ruler"], b["ruler"]
        line = (f"Ascendant ruler {ra} ({ROLE[ra]}, h{a['ws'][ra]}) -> "
                f"{rb} ({ROLE[rb]}, h{b['ws'][rb]})")
        (gains if rb in ("Venus", "Jupiter") and ra not in ("Venus", "Jupiter")
         else losses if ra in ("Venus", "Jupiter") and rb not in ("Venus", "Jupiter")
         else same).append(line + "  [benefic vs neutral rulership]")
    for lot in ("fort", "spir"):
        nm = "Fortune" if lot == "fort" else "Spirit"
        ha, hb = a[lot + "_h"], b[lot + "_h"]
        lda, ldb = a[lot + "_lord"], b[lot + "_lord"]
        if ha != hb:
            (gains if place(hb) == "angular" and place(ha) != "angular"
             else losses if place(ha) == "angular" and place(hb) != "angular"
             else same).append(
                f"Lot of {nm} h{ha} {place(ha)} -> h{hb} {place(hb)}")
        if lda != ldb:
            better = (place(b["ws"][ldb]) != "cadent" or b["ws"][ldb] not in DARK) \
                and (a["ws"][lda] in DARK and b["ws"][ldb] not in DARK)
            line = (f"lord of {nm}: {lda} (h{a['ws'][lda]}) -> "
                    f"{ldb} (h{b['ws'][ldb]})")
            (gains if better else same).append(line)
    return gains, losses, same


def meridian(pl, which="MC"):
    xx, _ = swe.calc_ut(JD, SWE_ID[pl], FL | swe.FLG_EQUATORIAL)
    m = n180(xx[0] - GMST)
    return m if which == "MC" else n180(m + 180)


def asc_at(lat, lon):
    return swe.houses(JD, lat, lon, b"P")[1][0]


def solve_asc(target, lat):
    """Longitude where the Ascendant equals a target degree, at one latitude."""
    lo, hi, best, bo = -180.0, 180.0, None, 9e9
    x = -180.0
    while x < 180.0:
        v = abs(n180(asc_at(lat, x) - target))
        if v < bo:
            bo, best = v, x
        x += 0.25
    a, b = best - 0.6, best + 0.6
    for _ in range(60):
        m = (a + b) / 2
        if n180(asc_at(lat, a) - target) * n180(asc_at(lat, m) - target) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


HR = "=" * 100


def main():
    natal_asc = D["asc"]
    print(f"natal Ascendant {natal.fmt(natal_asc)}   DAY chart")
    print(f"Lot of Fortune sits {FORT_OFF:.2f}° ahead of the Ascendant, "
          f"Lot of Spirit {SPIR_OFF:.2f}°.")
    print("Both are rigid offsets, so their houses flip at fixed Ascendant "
          "degrees.\n")

    # ------------------------------------------------------------- LAYER A
    print(HR)
    print("LAYER A — THE RISING SIGN. Binary across the contiguous US.")
    print(HR)
    east = config(196.0)      # any Libra Ascendant
    west = config(170.0)      # any Virgo Ascendant
    for nm, c in (("EAST of 100.22W  (Libra rising, = natal)", east),
                  ("WEST of 100.22W  (Virgo rising)", west)):
        print(f"\n  ▸ {nm}")
        print(f"    Ascendant ruler : {c['ruler']} ({ROLE[c['ruler']]}), "
              f"h{c['ws'][c['ruler']]} {place(c['ws'][c['ruler']])}")
        ang = [f"{p} h{c['ws'][p]}" for p in TRAD if c['ws'][p] in ANGULAR]
        drk = [f"{p} h{c['ws'][p]}" for p in TRAD if c['ws'][p] in DARK]
        joys = [f"{p} h{c['ws'][p]}" for p in TRAD if JOY.get(p) == c['ws'][p]]
        print(f"    angular planets : {', '.join(ang) or 'none'}")
        print(f"    in dark places  : {', '.join(drk) or 'none'}")
        print(f"    in their joys   : {', '.join(joys) or 'NONE'}")
        print(f"    Jupiter (in-sect benefic) h{c['ws']['Jupiter']} "
              f"{place(c['ws']['Jupiter'])}   |   "
              f"Saturn (in-sect malefic) h{c['ws']['Saturn']} "
              f"{place(c['ws']['Saturn'])}")
        print(f"    Mars (out-of-sect malefic, the most harmful body in a day "
              f"chart) h{c['ws']['Mars']} {place(c['ws']['Mars'])}")

    g, l, s = ledger(east, west, "east", "west")
    print(f"\n  ▸ LEDGER, moving EAST -> WEST")
    print("    GAINS by doctrine")
    for x in g:
        print(f"      +  {x}")
    print("    LOSSES by doctrine")
    for x in l:
        print(f"      -  {x}")
    if s:
        print("    changed, but doctrine does not rank the two states")
        for x in s:
            print(f"      =  {x}")

    # ------------------------------------------------------------- LAYER B
    print("\n" + HR)
    print("LAYER B — THE LOTS. Continuous, and independent of everything else.")
    print(HR)
    fb = (30.0 - FORT_OFF % 30.0) % 30.0
    sb = (30.0 - SPIR_OFF % 30.0) % 30.0
    print(f"  Fortune changes whole-sign house when the Ascendant passes "
          f"{fb:.2f}° of its sign.")
    print(f"  Spirit  changes whole-sign house when the Ascendant passes "
          f"{sb:.2f}° of its sign.")
    print()
    for lab, tgt in (("Spirit drops from the ANGULAR 4th to the succedent 5th",
                      S.index("Virgo") * 30 + sb),
                     ("(same boundary, Libra rising)",
                      S.index("Libra") * 30 + sb)):
        print(f"  {lab}")
        for lat in (30.0, 35.0, 40.0, 45.0):
            print(f"      lat {lat:4.1f}N  ->  {abs(solve_asc(tgt, lat)):.3f}W")
    print()
    print("  so, by Ascendant degree:")
    for nm, la, lo in (("Los Angeles CA", 34.052, -118.244),
                       ("Phoenix AZ", 33.448, -112.074),
                       ("Tucson AZ", 32.222, -110.974),
                       ("Salt Lake City UT", 40.761, -111.891),
                       ("Santa Fe NM", 35.687, -105.938),
                       ("Denver CO", 39.739, -104.990),
                       ("Eureka CA", 40.802, -124.164),
                       ("San Francisco CA", 37.775, -122.419),
                       ("Seattle WA", 47.606, -122.332),
                       ("Asheville NC", 35.595, -82.552),
                       ("Sarasota FL", 27.337, -82.531),
                       ("Pittsburgh PA", 40.441, -79.996),
                       ("Washington DC", 38.907, -77.037),
                       ("New York NY", 40.713, -74.006),
                       ("Boston MA", 42.360, -71.059)):
        a = asc_at(la, lo)
        c = config(a)
        print(f"    {nm:<19}ASC {natal.fmt(a):<15}"
              f"Fortune h{c['fort_h']:<3}({place(c['fort_h'])[:4]}) lord "
              f"{c['fort_lord']:<8}"
              f"Spirit h{c['spir_h']:<3}({place(c['spir_h'])[:4]}) lord "
              f"{c['spir_lord']}")

    # ------------------------------------------------------------- LAYER C
    print("\n" + HR)
    print("LAYER C — DEGREE ANGULARITY. Which planet, and what it is by sect.")
    print(HR)
    print(f"  {'planet':<10}{'role in a DAY chart':<26}{'angle':<7}"
          f"{'line':<12}reachable on US land?")
    for pl, ang in (("Jupiter", "IC"), ("Sun", "MC"), ("Venus", "MC"),
                    ("Moon", "DSC"), ("Saturn", "DSC"), ("Mars", "MC"),
                    ("Mercury", "MC")):
        if ang in ("MC", "IC"):
            L = meridian(pl, ang)
            reach = "YES" if -125 <= L <= -66.9 else "no, falls in the Pacific"
            print(f"  {pl:<10}{ROLE[pl]:<26}{ang:<7}{abs(L):>7.3f}W    {reach}")
        else:
            xx, _ = swe.calc_ut(JD, SWE_ID[pl], FL | swe.FLG_EQUATORIAL)
            ra, dec = xx[0], xx[1]
            x = -math.tan(math.radians(37.0)) * math.tan(math.radians(dec))
            L = n180(ra + math.degrees(math.acos(x)) - GMST)
            reach = "YES" if -125 <= L <= -66.9 else "just offshore in the Pacific"
            print(f"  {pl:<10}{ROLE[pl]:<26}{ang:<7}{abs(L):>7.3f}W    {reach}")
    print()
    print("  NOTE, and it is the most important single fact in this layer:")
    print("  Mars is the out-of-sect malefic, the body classical doctrine says")
    print("  does the most harm when angular. Its MC line falls at 135.9W and")
    print("  its IC line at 44.1W, both in open ocean. Mercury's likewise.")
    print("  There is NO location in the United States that angularizes Mars.")
    print()
    print("  Saturn's Descendant curve DOES cross US land near 93.5W, and east")
    print("  of 100.22W Saturn is already whole-sign angular in the 7th, so")
    print("  that meridian is the one place in the country where a malefic is")
    print("  angular in both senses at once. Reported as doctrine, not scored.")


if __name__ == "__main__":
    main()
