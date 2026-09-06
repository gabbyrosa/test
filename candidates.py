#!/usr/bin/env python3
"""
Structured relocation readout for a short candidate list. No composite score.

Each city gets the identical set of computed facts so they can be compared
directly:

  1  Venus  angle + orb, house (Placidus and whole sign)
  2  Sun    angle + orb, house
  3  Jupiter angle + orb, house
  4  1st-house ruler and where it lands
  5  2nd-house cusp, ruler, ruler's house, occupants   (money / self-worth)
  6  5th / 7th / 10th houses: cusp, ruler, occupants   (glamour / attraction / status)
  7  parans within the declared latitude orb (primary <=0.5, background <=1.5)
  8  Saturn, Mars, Neptune, Pluto angularity            (reported, not scored)
  9  Venus-Jupiter mutual condition and relocated aspects to the angles

Interpretation happens in prose afterwards; this file only computes.
"""

import json
import math
import swisseph as swe

import natal
import relocation as R

swe.set_ephe_path("/usr/share/swisseph")
S = natal.SIGNS
RUL = R.RULERS
FL = swe.FLG_SWIEPH
D = natal.compute()
JD = D["jd"]
P = {n: D["planets"][n]["lon"] for n in D["planets"]}

CANDIDATES = [
    ("Tokyo, Japan", 35.68, 139.65),
    ("Barcelona, Spain", 41.39, 2.17),
    ("Valencia, Spain", 39.47, -0.38),
    ("Palma de Mallorca", 39.57, 2.65),
    ("Nice, France", 43.70, 7.27),
    ("Milan, Italy", 45.46, 9.19),
    ("Geneva, Switzerland", 46.20, 6.14),
    ("Lisbon, Portugal", 38.72, -9.14),
    ("Cabo San Lucas, MX", 22.89, -109.92),
    ("Scottsdale, AZ", 33.55, -111.95),
    ("Sedona, AZ", 34.87, -111.76),
    ("Auckland, New Zealand", -36.85, 174.76),
    ("St. Petersburg, FL", 27.77, -82.64),
    ("Asheville, NC", 35.60, -82.55),
]

ASPECTS = [("conj", 0, 6), ("sext", 60, 4), ("squa", 90, 5),
           ("trin", 120, 5), ("oppo", 180, 6)]


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def profile(lat, lon):
    try:
        cusps, ascmc = swe.houses(JD, lat, lon, b"P")
    except swe.Error:
        cusps, ascmc = swe.houses(JD, lat, lon, b"W")
    cusps = list(cusps)
    asc, mc = ascmc[0], ascmc[1]
    ang = {"ASC": asc, "MC": mc, "DSC": (asc + 180) % 360, "IC": (mc + 180) % 360}

    def house(p):
        p %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
                return i + 1
        return 12

    ai = S.index(sg(asc))

    def ws(p):
        return ((S.index(sg(p)) - ai) % 12) + 1

    def nearest(b):
        k, o = min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                   key=lambda t: t[1])
        return k, round(o, 1)

    def hinfo(h):
        cs = sg(cusps[h - 1])
        r = RUL[cs]
        occ = [n for n in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter",
                           "Saturn", "Uranus", "Neptune", "Pluto")
               if house(P[n]) == h]
        return dict(cusp=cs, ruler=r, ruler_house=house(P[r]), occupants=occ)

    # relocated aspects from Venus / Jupiter to the angles
    asp = []
    for b in ("Venus", "Jupiter"):
        for an, av in (("ASC", asc), ("MC", mc)):
            sep = abs(n180(P[b] - av))
            for nm, deg, orb in ASPECTS:
                if abs(sep - deg) <= orb and nm != "conj":
                    asp.append(f"{b} {nm} {an} ({abs(sep-deg):.1f})")
                    break

    pr = [p for p in R.parans_near(lat, orb=1.5)]
    parans = [f"{a} {b}/{c} {d} @{e:.1f}"
              + ("*" if abs(e - lat) <= 0.5 else "")
              for a, b, c, d, e in pr[:6]]

    hard = {b: nearest(b) for b in ("Saturn", "Mars", "Neptune", "Pluto")}
    return dict(
        asc=sg(asc), mc=sg(mc),
        venus=nearest("Venus"), venus_h=house(P["Venus"]), venus_ws=ws(P["Venus"]),
        sun=nearest("Sun"), sun_h=house(P["Sun"]), sun_ws=ws(P["Sun"]),
        jup=nearest("Jupiter"), jup_h=house(P["Jupiter"]), jup_ws=ws(P["Jupiter"]),
        h1=hinfo(1), h2=hinfo(2), h5=hinfo(5), h7=hinfo(7), h10=hinfo(10),
        aspects=asp, parans=parans,
        hard={k: v for k, v in hard.items() if v[1] <= 8},
    )


def main():
    out = {}
    for nm, la, lo in CANDIDATES:
        out[nm] = profile(la, lo)
        r = out[nm]
        print(f"\n{'='*78}\n{nm}   rising {r['asc']}, MC {r['mc']}\n{'='*78}")
        for lbl, key, hk, wk in (("Venus", "venus", "venus_h", "venus_ws"),
                                 ("Sun", "sun", "sun_h", "sun_ws"),
                                 ("Jupiter", "jup", "jup_h", "jup_ws")):
            a, o = r[key]
            print(f"  {lbl:<8} {a} {o:>4}°   house {r[hk]} (Placidus) / "
                  f"{r[wk]} (whole sign)")
        for lbl, k in (("1st self/body", "h1"), ("2nd money/worth", "h2"),
                       ("5th glamour/play", "h5"), ("7th attraction", "h7"),
                       ("10th status", "h10")):
            h = r[k]
            print(f"  {lbl:<17} {h['cusp']:<12} ruler {h['ruler']:<8} in h"
                  f"{h['ruler_house']:<3} occupants: {', '.join(h['occupants']) or '-'}")
        print(f"  aspects to angles: {', '.join(r['aspects']) or 'none in orb'}")
        print(f"  hard angular:      "
              f"{', '.join(f'{k} {v[0]} {v[1]}°' for k, v in r['hard'].items()) or 'none within 8°'}")
        print(f"  parans (*=primary): {'; '.join(r['parans']) or 'none within 1.5° lat'}")
    with open("candidates.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print("\nWrote candidates.json")


if __name__ == "__main__":
    main()
