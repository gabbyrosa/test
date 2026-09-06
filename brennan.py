#!/usr/bin/env python3
"""
Hellenistic-ordered relocation analysis (Brennan's sequence).

The ordering is deliberate and is followed literally:

  STEP 3  natal condition of every planet that can become angular in the US
  STEP 4  the houses those planets rule, natally and after relocation
  STEP 5  the whole-sign house each occupies after relocation
  STEP 6  aspects, sect, dignity and reception as modifiers
  STEP 7  soft relocated-angle aspects (Venus trine ASC and friends) LAST

Everything uses TRADITIONAL rulerships, because the method is traditional.
Mixing modern rulers into a sect-and-dignity analysis produces contradictory
statements about the same house; this file never does that.

The one structural fact that makes the whole US tractable: only two signs can
rise anywhere in the contiguous United States, Virgo and Libra. Whole-sign
house topics therefore take exactly TWO configurations across the entire
country, and the boundary is a single meridian. Everything that varies
continuously with location is angularity, which is STEP 2's business, not
STEP 4's or STEP 5's.
"""

import math
import swisseph as swe

import natal

swe.set_ephe_path("/usr/share/swisseph")
S = natal.SIGNS
FL = swe.FLG_SWIEPH | swe.FLG_SPEED

# --- traditional tables -----------------------------------------------------
DOMICILE = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}
EXALT = {"Sun": ("Aries", 19), "Moon": ("Taurus", 3), "Mercury": ("Virgo", 15),
         "Venus": ("Pisces", 27), "Mars": ("Capricorn", 28),
         "Jupiter": ("Cancer", 15), "Saturn": ("Libra", 21)}
ELEMENT = {"Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
           "Taurus": "earth", "Virgo": "earth", "Capricorn": "earth",
           "Gemini": "air", "Libra": "air", "Aquarius": "air",
           "Cancer": "water", "Scorpio": "water", "Pisces": "water"}
# Dorothean triplicity: (day ruler, night ruler, participating)
TRIP = {"fire": ("Sun", "Jupiter", "Saturn"),
        "earth": ("Venus", "Moon", "Mars"),
        "air": ("Saturn", "Mercury", "Jupiter"),
        "water": ("Venus", "Mars", "Moon")}
# Egyptian bounds: (upper degree, ruler)
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
JOY = {"Mercury": 1, "Moon": 3, "Venus": 5, "Mars": 6, "Sun": 9,
       "Jupiter": 11, "Saturn": 12}
DIURNAL = {"Sun", "Jupiter", "Saturn"}
NOCTURNAL = {"Moon", "Venus", "Mars"}
MASCULINE_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}
TRAD = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
ALL = TRAD + ["Uranus", "Neptune", "Pluto", "North Node", "Chiron"]

D = natal.compute()
JD = D["jd"]
PL = D["planets"]
P = {n: PL[n]["lon"] for n in PL}
SPD = {n: PL[n]["speed"] for n in PL}


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def dms(x):
    i, d, m = natal.sign_of(x)
    return f"{d:2d}°{m:02d}' {S[i][:3]}"


def bound_of(lon):
    s, pos = sg(lon), lon % 30
    for hi, r in BOUNDS[s]:
        if pos < hi:
            return r
    return BOUNDS[s][-1][1]


def face_of(lon):
    return CHALDEAN[(int(lon // 10)) % 7]


def dignity(pl, sect_is_day):
    """Full traditional dignity/debility for one planet."""
    lon = P[pl]
    s, pos = sg(lon), lon % 30
    out = []
    if DOMICILE[s] == pl:
        out.append("DOMICILE")
    if pl in EXALT and EXALT[pl][0] == s:
        out.append("EXALTATION")
    det = {v: k for k, v in DOMICILE.items()}
    if DOMICILE[S[(S.index(s) + 6) % 12]] == pl:
        out.append("DETRIMENT")
    if pl in EXALT and S[(S.index(EXALT[pl][0]) + 6) % 12] == s:
        out.append("FALL")
    day_r, night_r, part = TRIP[ELEMENT[s]]
    if pl == (day_r if sect_is_day else night_r):
        out.append("triplicity (ruling)")
    elif pl == part:
        out.append("triplicity (participating)")
    if bound_of(lon) == pl:
        out.append("bound")
    if face_of(lon) == pl:
        out.append("face")
    return out, bound_of(lon), face_of(lon), (day_r if sect_is_day else night_r)


def solar_phase(pl):
    """Combustion state and oriental/occidental phase relative to the Sun."""
    if pl == "Sun":
        return "-", "-"
    sep = abs(n180(P[pl] - P["Sun"]))
    if sep <= 0.2833:
        state = f"CAZIMI ({sep:.2f}°)"
    elif sep <= 8.0:
        state = f"COMBUST ({sep:.2f}°)"
    elif sep <= 15.0:
        state = f"under the beams ({sep:.2f}°)"
    else:
        state = f"free of the beams ({sep:.2f}°)"
    # zodiacally ahead of the Sun = sets after it = occidental / evening star
    phase = "occidental (evening star)" if n180(P[pl] - P["Sun"]) > 0 \
        else "oriental (morning star)"
    return state, phase


def ws_from(asc_sign):
    """Whole-sign house of each sign, and the ruler of each house."""
    i = S.index(asc_sign)
    house_sign = {h: S[(i + h - 1) % 12] for h in range(1, 13)}
    ruler = {h: DOMICILE[house_sign[h]] for h in range(1, 13)}
    rules = {}
    for h, r in ruler.items():
        rules.setdefault(r, []).append(h)
    place = {pl: ((S.index(sg(P[pl])) - i) % 12) + 1 for pl in ALL}
    return house_sign, ruler, rules, place


def meridian_lon(pl):
    """Terrestrial longitude where the planet culminates (in-mundo MC line)."""
    xx, _ = swe.calc_ut(JD, {"Sun": swe.SUN, "Moon": swe.MOON,
                             "Mercury": swe.MERCURY, "Venus": swe.VENUS,
                             "Mars": swe.MARS, "Jupiter": swe.JUPITER,
                             "Saturn": swe.SATURN, "Uranus": swe.URANUS,
                             "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
                             "North Node": swe.TRUE_NODE,
                             "Chiron": swe.CHIRON}[pl],
                        FL | swe.FLG_EQUATORIAL)
    ra = xx[0]
    gmst = swe.sidtime(JD) * 15.0
    return n180(ra - gmst), n180(ra - gmst + 180.0), ra, xx[1]


def zodiacal_mc_lon(target_lon):
    """Longitude where the zodiacal MC equals target_lon (bisection)."""
    def f(lo):
        return n180(swe.houses(JD, 35.0, lo, b"P")[1][1] - target_lon)
    lo, hi = -180.0, 180.0
    best, bo = None, 9e9
    x = -180.0
    while x < 180.0:
        v = abs(f(x))
        if v < bo:
            bo, best = v, x
        x += 0.25
    a, b = best - 0.5, best + 0.5
    for _ in range(60):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


HDR = "=" * 100


def main():
    sect_is_day = True   # Sun above the horizon at birth: verified below
    cusps, ascmc = swe.houses(JD, natal.BIRTH["lat"], natal.BIRTH["lon"], b"P")
    print(f"natal ASC {dms(ascmc[0])}   MC {dms(ascmc[1])}   "
          f"Sun {dms(P['Sun'])}  ->  DAY chart (Sun above horizon, west of ASC-DSC axis)")
    print()

    # ------------------------------------------------------------------ STEP 3
    print(HDR)
    print("STEP 3 - NATAL CONDITION of every body that can become angular in the US")
    print(HDR)
    print("(Mercury, Mars and Uranus are omitted: no US location makes them angular.)")
    print()
    ANGULARIZABLE = ["Venus", "Sun", "Jupiter", "Moon", "Saturn",
                     "Neptune", "Pluto", "North Node", "Chiron"]
    for pl in ANGULARIZABLE:
        digs, bnd, fce, tri = dignity(pl, sect_is_day) if pl in TRAD else ([], "-", "-", "-")
        state, phase = solar_phase(pl) if pl in TRAD else ("-", "-")
        sect = ("IN SECT" if (pl in DIURNAL) == sect_is_day else "out of sect") \
            if pl in DIURNAL | NOCTURNAL else "n/a"
        rx = "Rx" if SPD[pl] < 0 else "direct"
        print(f"  {pl:<11} {dms(P[pl])}   {rx:<7} {SPD[pl]:+7.4f}°/day")
        print(f"    {'dignity':<14}{', '.join(digs) if digs else 'PEREGRINE (no dignity of any kind)'}")
        if pl in TRAD:
            print(f"    {'bound / face':<14}{bnd} / {fce}"
                  f"      triplicity lord of its element: {tri}")
            print(f"    {'sect':<14}{sect}"
                  f"   ({'diurnal' if pl in DIURNAL else 'nocturnal' if pl in NOCTURNAL else '-'} planet, day chart)")
            print(f"    {'solar phase':<14}{state};  {phase}")
        print()

    # ------------------------------------------------------------------ STEP 4/5
    print(HDR)
    print("STEP 4 & 5 - RULERSHIPS AND WHOLE-SIGN PLACEMENTS, natal vs relocated")
    print(HDR)
    print("Only Virgo and Libra can rise anywhere in the contiguous US, so there are")
    print("exactly TWO whole-sign configurations for the whole country.\n")

    configs = [("Libra rising  (natal, and everywhere EAST of 100.22°W)", "Libra"),
               ("Virgo rising  (everywhere WEST of 100.22°W)", "Virgo")]
    tables = {}
    for label, asc_sign in configs:
        hs, rulers, rules, place = ws_from(asc_sign)
        tables[asc_sign] = (hs, rulers, rules, place)
        print(f"  ▸ {label}")
        print(f"    {'house':<7}{'sign':<13}{'ruler':<10}{'ruler sits in':<15}occupants")
        for h in range(1, 13):
            occ = [p for p in ALL if place[p] == h]
            print(f"    {h:<7}{hs[h]:<13}{rulers[h]:<10}"
                  f"h{place[rulers[h]]:<14}{', '.join(occ) or '-'}")
        print()

    print("  ▸ what each angularizable body RULES and OCCUPIES, side by side")
    print(f"    {'body':<12}{'EAST (Libra rising)':<40}{'WEST (Virgo rising)'}")
    for pl in ANGULARIZABLE:
        row = []
        for asc_sign in ("Libra", "Virgo"):
            hs, rulers, rules, place = tables[asc_sign]
            r = rules.get(pl, [])
            rs = "rules " + "+".join(f"{x}" for x in r) if r else "rules nothing"
            joy = "  ★JOY" if JOY.get(pl) == place[pl] else ""
            ang = {1: "ANGULAR", 4: "ANGULAR", 7: "ANGULAR", 10: "ANGULAR",
                   2: "succ", 5: "succ", 8: "succ", 11: "succ"}.get(place[pl], "cadent")
            row.append(f"in h{place[pl]} ({ang}), {rs}{joy}")
        print(f"    {pl:<12}{row[0]:<40}{row[1]}")
    print()

    # ------------------------------------------------------------------ STEP 6
    print(HDR)
    print("STEP 6 - MODIFIERS: aspects with reception, and the dispositor chains")
    print(HDR)
    print("  aspects among the seven traditional planets (degree-based, "
          "with sign-based confirmation)")
    ASP = [("conjunction", 0), ("sextile", 60), ("square", 90),
           ("trine", 120), ("opposition", 180)]
    for i in range(len(TRAD)):
        for j in range(i + 1, len(TRAD)):
            a, b = TRAD[i], TRAD[j]
            sep = abs(n180(P[a] - P[b]))
            for nm, deg in ASP:
                orb = 10 if "Sun" in (a, b) or "Moon" in (a, b) else 8
                if abs(sep - deg) <= orb:
                    same = (S.index(sg(P[a])) - S.index(sg(P[b]))) % 12
                    ws_ok = same in {0: (0,), 60: (2, 10), 90: (3, 9),
                                     120: (4, 8), 180: (6,)}[deg]
                    rec = []
                    if DOMICILE[sg(P[a])] == b:
                        rec.append(f"{b} receives {a} by domicile")
                    if DOMICILE[sg(P[b])] == a:
                        rec.append(f"{a} receives {b} by domicile")
                    if bound_of(P[a]) == b:
                        rec.append(f"{b} receives {a} by bound")
                    if bound_of(P[b]) == a:
                        rec.append(f"{a} receives {b} by bound")
                    applying = "applying" if (SPD[a] - SPD[b]) * n180(P[b] - P[a]) > 0 \
                        else "separating"
                    print(f"    {a:<8}{nm:<12}{b:<9}orb {abs(sep-deg):5.2f}°  "
                          f"{applying:<11}"
                          f"{'whole-sign confirmed' if ws_ok else 'OUT OF SIGN (degree only)'}")
                    for r in rec:
                        print(f"        ↳ {r}")
                    break
    print()
    print("  dispositor chains (who each planet answers to)")
    for pl in TRAD:
        chain, cur, guard = [pl], pl, 0
        while guard < 12:
            nxt = DOMICILE[sg(P[cur])]
            if nxt == cur:
                chain.append("(in its own sign - chain terminates)")
                break
            if nxt in chain:
                chain.append(f"{nxt} ↺ mutual reception loop")
                break
            chain.append(nxt)
            cur, guard = nxt, guard + 1
        print(f"    {pl:<9}→ " + " → ".join(chain[1:]))
    print()

    # ------------------------------------------------------------------ STEP 2 recap
    print(HDR)
    print("ANGULARITY (the continuous variable): exact meridian longitudes")
    print(HDR)
    print(f"  {'body':<12}{'MC line':<14}{'IC line':<14}{'ecl.lat':<10}"
          f"{'zodiacal MC line':<18}difference")
    for pl in ANGULARIZABLE + ["Mercury", "Mars", "Uranus"]:
        mcl, icl, ra, dec = meridian_lon(pl)
        zl = zodiacal_mc_lon(P[pl])
        eclat = swe.calc_ut(JD, {"Sun": swe.SUN, "Moon": swe.MOON,
                                 "Mercury": swe.MERCURY, "Venus": swe.VENUS,
                                 "Mars": swe.MARS, "Jupiter": swe.JUPITER,
                                 "Saturn": swe.SATURN, "Uranus": swe.URANUS,
                                 "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
                                 "North Node": swe.TRUE_NODE,
                                 "Chiron": swe.CHIRON}[pl], FL)[0][1]
        inus = "  <-- in the contiguous US" if -125 <= mcl <= -67 else ""
        inus_ic = "  <-- IC line in the contiguous US" if -125 <= icl <= -67 else ""
        print(f"  {pl:<12}{mcl:>8.3f}°    {icl:>8.3f}°    {eclat:>+6.2f}°   "
              f"{zl:>10.3f}°      {abs(n180(zl-mcl)):5.3f}°{inus}{inus_ic}")
    print()

    # ------------------------------------------------------------------ STEP 7
    print(HDR)
    print("STEP 7 - SOFT RELOCATED-ANGLE ASPECTS, reported last and as context only")
    print(HDR)
    SITES = [
        ("Los Angeles CA", 34.05, -118.24), ("San Diego CA", 32.72, -117.16),
        ("Las Vegas NV", 36.17, -115.14), ("Palm Springs CA", 33.83, -116.55),
        ("Scottsdale AZ", 33.55, -111.95), ("Sedona AZ", 34.87, -111.76),
        ("Tucson AZ", 32.22, -110.97), ("Salt Lake City UT", 40.76, -111.89),
        ("Santa Fe NM", 35.69, -105.94), ("Denver CO", 39.74, -104.99),
        ("Austin TX", 30.27, -97.74), ("Chicago IL", 41.88, -87.63),
        ("Nashville TN", 36.16, -86.78), ("Asheville NC", 35.60, -82.55),
        ("Charleston SC", 32.78, -79.93), ("Sarasota FL", 27.34, -82.53),
        ("Miami FL", 25.76, -80.19), ("Washington DC", 38.91, -77.04),
        ("New York NY", 40.71, -74.01), ("Boston MA", 42.36, -71.06),
        ("Pittsburgh PA", 40.44, -79.96),
        ("Honolulu HI", 21.31, -157.86), ("Anchorage AK", 61.22, -149.90),
    ]
    def to_asc(pl, asc):
        """Closest Ptolemaic aspect from a planet to the Ascendant, or none."""
        sep = abs(n180(P[pl] - asc))
        best = min((("conj", 0), ("sext", 60), ("squa", 90),
                    ("trin", 120), ("oppo", 180)),
                   key=lambda t: abs(sep - t[1]))
        o = abs(sep - best[1])
        return (f"{best[0]} {o:4.2f}°" if o <= 8 else f"none ({sep:.1f}° sep)")

    print(f"  {'city':<19}{'ASC':<13}{'MC':<13}"
          f"{'Venus-ASC':<17}{'Ven-MC':<9}{'Sun-MC':<9}{'Jup-IC':<9}chart ruler")
    for nm, la, lo in SITES:
        try:
            cs, am = swe.houses(JD, la, lo, b"P")
        except swe.Error:
            cs, am = swe.houses(JD, la, lo, b"W")
        asc, mc = am[0], am[1]
        ic = (mc + 180) % 360
        rulr = DOMICILE[sg(asc)]
        ws_r = ((S.index(sg(P[rulr])) - S.index(sg(asc))) % 12) + 1
        print(f"  {nm:<19}{dms(asc):<13}{dms(mc):<13}"
              f"{to_asc('Venus', asc):<17}"
              f"{abs(n180(P['Venus']-mc)):6.2f}°  "
              f"{abs(n180(P['Sun']-mc)):6.2f}°  "
              f"{abs(n180(P['Jupiter']-ic)):6.2f}°  "
              f"  {rulr} h{ws_r}")

    # ------------------------------------------------------- verify the premise
    print()
    print(HDR)
    print("PREMISE CHECK - what can actually rise, and where the boundary is")
    print(HDR)
    seen, asc_min, asc_max = {}, {}, {}
    lat = 24.5
    while lat <= 49.5:
        lo = -125.0
        while lo <= -66.5:
            a = swe.houses(JD, lat, lo, b"P")[1][0]
            s = sg(a)
            seen[s] = seen.get(s, 0) + 1
            asc_min[s] = min(asc_min.get(s, 999), a % 30)
            asc_max[s] = max(asc_max.get(s, -1), a % 30)
            lo += 0.25
        lat += 0.25
    print(f"  scanned the contiguous-US bounding box at 0.25° "
          f"({sum(seen.values())} points)")
    for s, n in sorted(seen.items(), key=lambda t: -t[1]):
        print(f"    {s:<10}{n:>7} points   ASC spans "
              f"{asc_min[s]:5.2f}° .. {asc_max[s]:5.2f}° of the sign")
    print(f"  Venus is at {P['Venus'] % 30:.2f}° Gemini -> it cannot rise here; "
          f"Gemini never rises in the contiguous US.")
    for nm, la, lo in (("Honolulu HI", 21.31, -157.86), ("Anchorage AK", 61.22, -149.90),
                       ("Fairbanks AK", 64.84, -147.72), ("Adak AK", 51.88, -176.66)):
        a = swe.houses(JD, la, lo, b"P")[1][0]
        print(f"    {nm:<14}ASC {dms(a)}   (outside the lower 48)")
    # exact Virgo/Libra boundary meridian
    def f(lo):
        return n180(swe.houses(JD, 39.0, lo, b"P")[1][0] - 180.0)
    a, b = -101.5, -99.0
    for _ in range(70):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    bl = (a + b) / 2
    scorp = []
    lat = 24.5
    while lat <= 49.5:
        lo = -125.0
        while lo <= -66.5:
            if sg(swe.houses(JD, lat, lo, b"P")[1][0]) == "Scorpio":
                scorp.append((lat, lo))
            lo += 0.25
        lat += 0.25
    if scorp:
        print(f"  the Scorpio sliver sits at lat "
              f"{min(p[0] for p in scorp):.2f}..{max(p[0] for p in scorp):.2f}N, "
              f"lon {min(p[1] for p in scorp):.2f}..{max(p[1] for p in scorp):.2f}"
              f"  (bounding-box corner, not US land)")
    print(f"  Virgo/Libra rising boundary at lat 39N: {bl:.6f}°W")
    for la in (25.0, 30.0, 35.0, 40.0, 45.0, 49.0):
        def g(lo, la=la):
            return n180(swe.houses(JD, la, lo, b"P")[1][0] - 180.0)
        a2, b2 = -101.5, -99.0
        for _ in range(70):
            m = (a2 + b2) / 2
            if g(a2) * g(m) <= 0:
                b2 = m
            else:
                a2 = m
        print(f"    lat {la:4.1f}N -> boundary {(a2+b2)/2:.6f}°W")


if __name__ == "__main__":
    main()
