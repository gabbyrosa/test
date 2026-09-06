#!/usr/bin/env python3
"""
US relocation map for the four convention-robust topics only.

Built as CONSTRAINTS, not as a search for a best city. No planet is assumed
good or bad. No line is privileged. The four topics are the ones whose house
rulership survived the cross-method audit at 0-5 percent convention
disagreement; money (57%), partnership (43%) and children (63%) are excluded
because no stable answer exists for them at this level of source certainty.

  identity   1st cusp sign, its ruler, that ruler's house, 1st occupants
  home       4th cusp sign, its ruler, that ruler's house, 4th occupants
  travel     9th cusp sign, its ruler, that ruler's house, 9th occupants
  career     10th cusp sign, its ruler, that ruler's house, 10th occupants

Every structure is computed under all EIGHT combinations of the three
conventions the four astrologers disagree about:

  house system   Placidus (Lee, stated)  vs  whole sign (Hellenistic)
  rulership      modern (Lee, stated)    vs  traditional
  zodiac         tropical                vs  sidereal Lahiri (Siregar: both)

A boundary is HIGH ROBUSTNESS only if it appears under all eight.
FRAMEWORK-DEPENDENT if it appears under some.
LOW if it appears under one or two.
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
TROP = {n: swe.calc_ut(JD, s, FL)[0][0] for n, s in IDS}
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
AY = swe.get_ayanamsa_ut(JD)
SID = {n: (v - AY) % 360.0 for n, v in TROP.items()}

TRAD = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
        "Pisces": "Jupiter"}
MOD = dict(TRAD, **{"Scorpio": "Pluto", "Aquarius": "Uranus", "Pisces": "Neptune"})
TOPIC = {1: "identity", 4: "home", 9: "travel", 10: "career"}
CONV = [(hs, rs, zo) for hs in ("placidus", "wholesign")
        for rs in ("modern", "traditional") for zo in ("tropical", "sidereal")]


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


def structures(lat, lon):
    """All four topics under all eight convention combinations."""
    cusp, am = swe.houses(JD, lat, lon, b"P")
    cusp = list(cusp)
    out = {}
    for hs, rs, zo in CONV:
        P = TROP if zo == "tropical" else SID
        R = MOD if rs == "modern" else TRAD
        if hs == "placidus":
            cs = cusp if zo == "tropical" else [(c - AY) % 360.0 for c in cusp]

            def hof(v, cs=cs):
                v %= 360.0
                for i in range(12):
                    a, b = cs[i], cs[(i + 1) % 12]
                    if (a < b and a <= v < b) or (a > b and (v >= a or v < b)):
                        return i + 1
                return 12
            csign = {h: sg(cs[h - 1]) for h in range(1, 13)}
        else:
            asc = am[0] if zo == "tropical" else (am[0] - AY) % 360.0
            ai = S.index(sg(asc))

            def hof(v, ai=ai):
                return ((S.index(sg(v)) - ai) % 12) + 1
            csign = {h: S[(ai + h - 1) % 12] for h in range(1, 13)}
        ph = {b: hof(P[b]) for b in B}
        st = {}
        for h in TOPIC:
            r = R[csign[h]]
            st[h] = (r, ph[r], tuple(sorted(b for b in B if ph[b] == h)))
        out[(hs, rs, zo)] = st
    return out


HR = "=" * 100


def main():
    print(HR)
    print("STEP 0 — a structural fact that shrinks the convention matrix")
    print(HR)
    c1 = structures(37.0, -100.0)
    same_h, diff_h = 0, 0
    for lat in (28.0, 37.0, 46.0):
        for lon in (-120.0, -105.0, -90.0, -75.0):
            cusp, am = swe.houses(JD, lat, lon, b"P")
            cusp = list(cusp)

            def hp(v, cs):
                v %= 360.0
                for i in range(12):
                    a, b = cs[i], cs[(i + 1) % 12]
                    if (a < b and a <= v < b) or (a > b and (v >= a or v < b)):
                        return i + 1
                return 12
            cs_s = [(c - AY) % 360.0 for c in cusp]
            for b in B:
                if hp(TROP[b], cusp) == hp(SID[b], cs_s):
                    same_h += 1
                else:
                    diff_h += 1
    print(f"  Under PLACIDUS, switching tropical->sidereal leaves the house of a")
    print(f"  planet unchanged in {same_h}/{same_h+diff_h} tested cases, because the")
    print(f"  cusps and the planets shift by the same ayanamsa.")
    print("  So the zodiac changes WHICH SIGN rules a house, not WHICH HOUSE a")
    print("  planet occupies. Whole sign is not guaranteed the same, because")
    print("  sign boundaries can be crossed unequally.\n")

    print(HR)
    print("STEP 1 & 2 — WHERE EACH ROBUST TOPIC ACTUALLY CHANGES")
    print(HR)
    print("  Fine longitude scan at three latitudes. A transition is recorded")
    print("  only when the topic's (ruler, ruler's house, occupants) changes.\n")

    LATS = (30.0, 37.0, 44.0)
    trans = {h: {} for h in TOPIC}
    for lat in LATS:
        prev = None
        lon = -124.8
        while lon <= -67.0:
            st = structures(lat, lon)
            if prev is not None:
                for h in TOPIC:
                    for cv in CONV:
                        if prev[cv][h] != st[cv][h]:
                            trans[h].setdefault(round(lon, 1), {}).setdefault(lat, set()).add(cv)
            prev = st
            lon += 0.1

    for h in TOPIC:
        print(f"\n  ▸ {TOPIC[h].upper()}  (house {h})")
        pts = sorted(trans[h].items())
        if not pts:
            print("      no transition anywhere in the contiguous US")
            continue
        # merge transitions within 0.35 deg
        merged = []
        for lo, d in pts:
            if merged and abs(lo - merged[-1][0]) <= 0.35:
                merged[-1][1].update(d)
            else:
                merged.append([lo, dict(d)])
        for lo, d in merged:
            allcv = set()
            for s in d.values():
                allcv |= s
            n = len(allcv)
            lab = ("HIGH ROBUSTNESS" if n == 8 else
                   "framework-dependent" if n >= 3 else "LOW robustness")
            hs = sorted({c[0] for c in allcv})
            rs = sorted({c[1] for c in allcv})
            zo = sorted({c[2] for c in allcv})
            print(f"      {abs(lo):7.2f}W   {n}/8 conventions   {lab}")
            print(f"                    house sys {','.join(hs):<20}"
                  f"rulers {','.join(rs):<22}zodiac {','.join(zo)}")

    print("\n" + HR)
    print("STEP 3 — WHAT THE CONFIGURATIONS ARE, under all eight conventions")
    print(HR)
    for lon, nm in ((-116.0, "far west"), (-108.0, "interior west"),
                    (-103.0, "high plains"), (-95.0, "mid-continent"),
                    (-85.0, "eastern interior"), (-73.0, "northeast seaboard")):
        st = structures(37.0, lon)
        print(f"\n  ▸ {nm}  ({abs(lon):.0f}W, 37N)")
        for h in TOPIC:
            vals = {}
            for cv in CONV:
                vals.setdefault(st[cv][h], []).append(cv)
            tag = "INVARIANT" if len(vals) == 1 else f"{len(vals)} readings"
            print(f"      {TOPIC[h]:<10}{tag}")
            for v, cvs in sorted(vals.items(), key=lambda t: -len(t[1])):
                who = ("all 8" if len(cvs) == 8 else
                       ", ".join(f"{a[:4]}/{b[:4]}/{c[:4]}" for a, b, c in cvs[:4]))
                print(f"        ruler {v[0]:<9} in h{v[1]:<4}"
                      f"occupants {', '.join(v[2]) or '-':<28}[{len(cvs)}/8: {who}]")


if __name__ == "__main__":
    main()
