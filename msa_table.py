#!/usr/bin/env python3
"""
The six-cell table over every contiguous-US MSA above 150,000 population.

CITY LIST PROVENANCE, stated because the previous list's provenance was the
problem:
  population  US Census Bureau, cbsa-est2024-alldata.csv, POPESTIMATE2024,
              rows where LSAD == "Metropolitan Statistical Area" and MDIV is
              empty (so metro divisions are not double counted)
  coordinates US Census Bureau 2023 Gazetteer, 2023_Gaz_cbsa_national.txt,
              INTPTLAT / INTPTLONG, CBSA_TYPE == 1
  filter      population > 150000; drop AK, HI, PR; keep 24-49.5N, 125-66W
  additions   none
  removals    none

No entry is included or excluded for any astrological or lifestyle reason.
286 MSAs result.

Maps and margins are as frozen earlier. Six cells per MSA, no seventh.
"""

import json
import math
import os

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
SCRATCH = ("/tmp/claude-0/-home-user-test/"
           "69d90e22-42ef-59e3-b947-6e9046f33faa/scratchpad")


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
        cs = {h: sg(cusp[h - 1]) for h in range(1, 13)}
    else:
        P, R = (TROPP, TRAD) if mp == "A" else (SIDP, TRAD)
        asc = am[0] if mp == "A" else (am[0] - AY) % 360.0
        ai = S.index(sg(asc))

        def hof(v):
            return ((S.index(sg(v)) - ai) % 12) + 1
        cs = {h: S[(ai + h - 1) % 12] for h in range(1, 13)}
    ph = {b: hof(P[b]) for b in B}
    return tuple((R[cs[h]], ph[R[cs[h]]],
                  tuple(sorted(b for b in B if ph[b] == h))) for h in TOPIC)


def mi(lat, dlon):
    return abs(dlon) * 69.172 * math.cos(math.radians(lat))


_SCAN = {}


def boundaries(lat_bucket, mp):
    """Longitudes where the signature changes, at a bucketed latitude."""
    key = (lat_bucket, mp)
    if key in _SCAN:
        return _SCAN[key]
    out, prev, lon = [], None, -125.4
    while lon <= -66.0:
        s = sig(lat_bucket, lon, mp)
        if prev is not None and s != prev:
            out.append(lon - 0.05)
        prev = s
        lon += 0.1
    _SCAN[key] = out
    return out


def main():
    msa = json.load(open(os.path.join(SCRATCH, "msa.json")))
    print(f"{len(msa)} MSAs above 150,000 in the contiguous US\n")

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
        for i, (s, _) in enumerate(sorted(seen.items(), key=lambda t: -t[1]), 1):
            labels.setdefault(mp, {})[s] = f"{mp}{i}"

    rows = []
    for m in msa:
        la, lo = m["lat"], m["lon"]
        bucket = round(la * 4) / 4.0
        cell = []
        for mp in ("A", "B", "C"):
            here = sig(la, lo, mp)
            lab = labels[mp].get(here)
            if lab is None:
                lab = f"{mp}*"
            bl = boundaries(bucket, mp)
            near = min((abs(x - lo) for x in bl), default=None)
            cell.append((lab, mi(la, near) if near is not None else None))
        rows.append({"name": m["name"], "pop": m["pop"], "lat": la, "lon": lo,
                     "cells": cell})

    json.dump({"labels": {mp: {"|".join(f"{r}:{h}:{'/'.join(o)}" for r, h, o in k): v
                               for k, v in labels[mp].items()} for mp in labels},
               "legend": {mp: [[labels[mp][k], [[r, h, list(o)] for r, h, o in k]]
                               for k in labels[mp]] for mp in labels},
               "rows": rows},
              open(os.path.join(SCRATCH, "msa_table.json"), "w"), indent=1)

    print("LEGEND")
    for mp, tag in (("A", "[WS tropical]"), ("B", "[Placidus tropical]"),
                    ("C", "[WS sidereal]")):
        print(f"\n  MAP {mp} {tag}  {len(labels[mp])} regimes")
        used = {}
        for r in rows:
            i = {"A": 0, "B": 1, "C": 2}[mp]
            used[r["cells"][i][0]] = used.get(r["cells"][i][0], 0) + 1
        for k, lab in sorted(labels[mp].items(), key=lambda t: int(t[1][1:])):
            if lab not in used:
                continue
            parts = [f"{TN[h]}: {k[i][0]} h{k[i][1]}"
                     + (f" +{'/'.join(k[i][2])}" if k[i][2] else "")
                     for i, h in enumerate(TOPIC)]
            print(f"    {lab:<5}{used[lab]:>4} MSAs   " + " | ".join(parts))

    print("\nDISTRIBUTION")
    for mp, i in (("A", 0), ("B", 1), ("C", 2)):
        c = {}
        for r in rows:
            c[r["cells"][i][0]] = c.get(r["cells"][i][0], 0) + 1
        print(f"  MAP {mp}: " + ", ".join(f"{k} {v}" for k, v in
                                          sorted(c.items(), key=lambda t: -t[1])))
    print("\nMARGINS (miles to the nearest boundary in the same map)")
    for mp, i in (("A", 0), ("B", 1), ("C", 2)):
        ms = sorted(r["cells"][i][1] for r in rows if r["cells"][i][1] is not None)
        n = len(ms)
        print(f"  MAP {mp}: median {ms[n//2]:.0f} mi, "
              f"{sum(1 for x in ms if x < 25)} MSAs within 25 mi of a boundary, "
              f"{sum(1 for x in ms if x > 500)} beyond 500 mi")
    print(f"\nwrote {SCRATCH}/msa_table.json")


if __name__ == "__main__":
    main()
