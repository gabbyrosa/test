#!/usr/bin/env python3
"""
Three separate contiguous-US maps for the four topics. No averaging, no
agreement scoring, no threshold, no cities.

  MAP A   tropical, WHOLE SIGN      Brennan-informed / Hellenistic ontology
  MAP B   tropical, PLACIDUS        Julian Lee's documented framework
  MAP C   sidereal Lahiri, whole sign   Siregar's alternate-zodiac layer

Whole sign and Placidus are not two measurements of one thing. They are two
different definitions of what a house IS. Requiring them to agree before
believing anything guarantees zero agreement, which is what the previous run
found. Each is therefore run on its own terms.

Topic structure, held constant across all three maps so the comparison is
like-for-like:  (ruler of the house, that ruler's house, occupants of the
house)  for houses 1, 4, 9, 10.

MAP C house-system note: Siregar advocates running the analysis in both
zodiacs but names no house system. Whole sign is used here because it is the
Vedic convention that accompanies a sidereal zodiac, which makes Map A vs
Map C a clean zodiac-only comparison. That pairing is my choice, not his.

Rulership is traditional in A and C (Hellenistic and Vedic both use the
classical set) and MODERN in B (Lee documents modern rulers). The previous
run established that rulership never distinguishes a boundary for these four
topics, so this does not affect the geography.
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
TOPIC = {1: "identity", 4: "home", 9: "travel", 10: "career"}
ANGLE_CUSP = {1, 4, 7, 10}


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


def build(lat, lon, mapname):
    cusp, am = swe.houses(JD, lat, lon, b"P")
    cusp = list(cusp)
    if mapname == "A":
        P, R, asc = TROPP, TRAD, am[0]
    elif mapname == "B":
        P, R, asc = TROPP, MOD, am[0]
    else:
        P, R, asc = SIDP, TRAD, (am[0] - AY) % 360.0
    if mapname == "B":
        cs = cusp

        def hof(v):
            v %= 360.0
            for i in range(12):
                a, b = cs[i], cs[(i + 1) % 12]
                if (a < b and a <= v < b) or (a > b and (v >= a or v < b)):
                    return i + 1
            return 12
        csign = {h: sg(cs[h - 1]) for h in range(1, 13)}
    else:
        ai = S.index(sg(asc))

        def hof(v):
            return ((S.index(sg(v)) - ai) % 12) + 1
        csign = {h: S[(ai + h - 1) % 12] for h in range(1, 13)}
        cs = None
    ph = {b: hof(P[b]) for b in B}
    st = {}
    for h in TOPIC:
        r = R[csign[h]]
        st[h] = (r, ph[r], tuple(sorted(b for b in B if ph[b] == h)))
    return st, ph, csign, cs


def cause(lat, lon0, lon1, h):
    """For MAP B: which cusp crossing produced the transition at this topic."""
    s0, ph0, cg0, c0 = build(lat, lon0, "B")
    s1, ph1, cg1, c1 = build(lat, lon1, "B")
    out = []
    if cg0[h] != cg1[h]:
        out.append(f"cusp {h} crossed a sign boundary")
    r0, r1 = s0[h][0], s1[h][0]
    if r0 == r1 and s0[h][1] != s1[h][1]:
        lo_, hi_ = sorted((s0[h][1], s1[h][1]))
        k = hi_ if (hi_ - lo_) == 1 else lo_
        out.append(f"ruler {r0} crossed cusp {k}"
                   + ("  [ANGLE]" if k in ANGLE_CUSP else "  [INTERMEDIATE]"))
    if s0[h][2] != s1[h][2]:
        moved = set(s0[h][2]) ^ set(s1[h][2])
        for m in moved:
            out.append(f"{m} crossed cusp {h}"
                       + ("  [ANGLE]" if h in ANGLE_CUSP else "  [INTERMEDIATE]"))
    return out


HR = "=" * 100
LATS = (30.0, 37.0, 44.0)


def scan(mapname):
    res = {h: {} for h in TOPIC}
    for lat in LATS:
        prev, plon = None, None
        lon = -124.8
        while lon <= -67.0:
            st, _, _, _ = build(lat, lon, mapname)
            if prev is not None:
                for h in TOPIC:
                    if prev[h] != st[h]:
                        res[h].setdefault(round(lon, 1), {})[lat] = (prev[h], st[h], plon)
            prev, plon = st, lon
            lon += 0.1
    return res


def report(mapname, title):
    r = scan(mapname)
    print(f"\n{HR}\n{title}\n{HR}")
    for h in TOPIC:
        pts = sorted(r[h].items())
        merged = []
        for lo, d in pts:
            if merged and abs(lo - merged[-1][0]) <= 0.3:
                merged[-1][1].update(d)
            else:
                merged.append([lo, dict(d)])
        print(f"\n  ▸ {TOPIC[h].upper()} (h{h}) — {len(merged)} transition(s)")
        for lo, d in merged:
            lats = sorted(d)
            a, b2, plon = d[lats[0]]
            drift = ""
            if len(lats) > 1:
                allos = [lo]
                drift = f"   (present at {', '.join(f'{x:.0f}N' for x in lats)})"
            print(f"      {abs(lo):7.2f}W{drift}")
            print(f"        from  ruler {a[0]:<8} h{a[1]:<3} occ {', '.join(a[2]) or '-'}")
            print(f"        to    ruler {b2[0]:<8} h{b2[1]:<3} occ {', '.join(b2[2]) or '-'}")
            if mapname == "B":
                for c in cause(lats[0], plon, lo, h):
                    print(f"        cause: {c}")
    return r


def main():
    ra = report("A", "MAP A — TROPICAL, WHOLE SIGN (Brennan-informed ontology)")
    rb = report("B", "MAP B — TROPICAL, PLACIDUS (Julian Lee's documented framework)")

    print(f"\n{HR}\nMAP A vs MAP B — same story, different story\n{HR}")
    for h in TOPIC:
        la = sorted({round(x, 1) for x in ra[h]})
        lb = sorted({round(x, 1) for x in rb[h]})
        shared = [x for x in la if any(abs(x - y) <= 0.6 for y in lb)]
        onlya = [x for x in la if x not in shared]
        onlyb = [x for x in lb if not any(abs(x - y) <= 0.6 for y in la)]
        print(f"\n  ▸ {TOPIC[h].upper()}")
        print(f"      A has {len(la)} transitions, B has {len(lb)}")
        print(f"      near-coincident : {', '.join(f'{abs(x):.1f}W' for x in shared) or 'none'}")
        print(f"      MAP A only      : {', '.join(f'{abs(x):.1f}W' for x in onlya) or 'none'}")
        print(f"      MAP B only      : {', '.join(f'{abs(x):.1f}W' for x in onlyb) or 'none'}")

    print(f"\n{HR}\nWHICH MAP-B-ONLY BOUNDARIES ARE CAUSED BY INTERMEDIATE CUSPS\n{HR}")
    for h in TOPIC:
        la = sorted({round(x, 1) for x in ra[h]})
        lb = sorted(rb[h].items())
        for lo, d in lb:
            if any(abs(lo - y) <= 0.6 for y in la):
                continue
            lat = sorted(d)[0]
            _, _, plon = d[lat]
            cs = cause(lat, plon, lo, h)
            inter = [c for c in cs if "INTERMEDIATE" in c]
            if inter:
                print(f"  {TOPIC[h]:<10}{abs(lo):7.2f}W   " + "; ".join(inter))

    rc = report("C", "MAP C — SIDEREAL LAHIRI, WHOLE SIGN (Siregar's alternate zodiac)")

    print(f"\n{HR}\nWHAT MAP C ADDS THAT NEITHER TROPICAL MAP CAN PRODUCE\n{HR}")
    print("  Same house system as Map A, so every difference below is the")
    print("  ZODIAC alone, not the house division.\n")
    for lon in (-116.0, -108.0, -103.0, -95.0, -85.0, -73.0):
        sa, _, _, _ = build(37.0, lon, "A")
        sc, _, _, _ = build(37.0, lon, "C")
        print(f"  ▸ {abs(lon):.0f}W, 37N")
        for h in TOPIC:
            same = "same" if sa[h] == sc[h] else "DIFFERS"
            print(f"      {TOPIC[h]:<10}{same:<9}"
                  f"A: {sa[h][0]}(h{sa[h][1]})  C: {sc[h][0]}(h{sc[h][1]})")
    print("\n  natal dignity change caused by the zodiac alone:")
    for b in ("Venus", "Jupiter", "Saturn", "Mars"):
        ts, ss = sg(TROPP[b]), sg(SIDP[b])
        td = ("domicile" if TRAD[ts] == b else
              "fall/detriment or peregrine")
        sd = ("DOMICILE" if TRAD[ss] == b else "peregrine or debilitated")
        print(f"    {b:<9}tropical {ts:<12}-> sidereal {ss:<12}"
              f"{'RULES ITS OWN SIGN in sidereal' if TRAD[ss] == b else ''}")


if __name__ == "__main__":
    main()
