#!/usr/bin/env python3
"""
Blind geographic scan of the contiguous United States.

Deliberately knows nothing about city names until after the astrology is done.
Walks a dense grid, computes the identical variables at every point, assigns
no composite score and no weights, and treats malefic contacts as reported
facts rather than penalties.

ONE GEOMETRY RULE, applied throughout. Within an eight-degree orb a planet
conjunct the MC or IC is necessarily about square the Ascendant, and a planet
conjunct the Descendant is necessarily opposite it. Those are one angular
configuration described twice, so squares and oppositions to the Ascendant are
NOT counted as separate information when the planet is already conjunct an
angle. What remains genuinely independent is:

    conjunct the Ascendant        the planet is in the body
    trine or sextile the ASC      a flowing contact no angle conjunction implies
    the planet's relocated house

Fixed question: where is she most supported in feeling beautiful, attractive,
confident, comfortable, vital and at home in her own body?

Stage 1 finds corridors. Stage 2 overlays cities. Lifestyle filtering happens
elsewhere, by hand, and is never mixed into the astrology.
"""

import math
import swisseph as swe
import natal

swe.set_ephe_path("/usr/share/swisseph")
S = natal.SIGNS
DOM = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Uranus",
       "Pisces": "Neptune"}
FL = swe.FLG_SWIEPH
BODIES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
          "Uranus", "Neptune", "Pluto", "North Node", "Chiron"]
D = natal.compute()
JD = D["jd"]
P = {n: D["planets"][n]["lon"] for n in BODIES}

LAT0, LAT1, LON0, LON1, STEP = 25.0, 49.0, -125.0, -67.0, 0.5
FLOW = {"conjunct", "trine", "sextile"}


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def aspect(a, b):
    sep = abs(n180(a - b))
    for nm, ang, orb in (("conjunct", 0, 8), ("sextile", 60, 5), ("square", 90, 7),
                         ("trine", 120, 8), ("opposite", 180, 8), ("quincunx", 150, 4)):
        if abs(sep - ang) <= orb:
            return nm, abs(sep - ang)
    return None, None


def measure(lat, lon):
    cusps, ascmc = swe.houses(JD, lat, lon, b"P")
    cusps = list(cusps)
    asc, mc = ascmc[0], ascmc[1]
    ic = (mc + 180) % 360
    ang = {"ASC": asc, "MC": mc, "DSC": (asc + 180) % 360, "IC": ic}

    def hp(p):
        p %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
                return i + 1
        return 12

    def angle_conj(p):
        """Which angle, if any, this body is conjunct within 8 degrees."""
        k, o = min(((k, abs(n180(p - v))) for k, v in ang.items()), key=lambda t: t[1])
        return (k, o) if o <= 8 else (None, None)

    m = {"asc": asc, "mc": mc, "ic": ic, "asc_sign": sg(asc),
         "ruler": DOM[sg(asc)], "cusps": cusps}
    m["ruler_house"] = hp(P[m["ruler"]])
    m["ruler_angle"] = angle_conj(P[m["ruler"]])

    # independent embodiment contacts only
    m["asc_flow"] = {}
    m["angle_conj"] = {}
    for b in BODIES:
        ak, ao = angle_conj(P[b])
        if ak:
            m["angle_conj"][b] = (ak, round(ao, 2))
        nm, o = aspect(P[b], asc)
        if nm in FLOW and not (ak in ("MC", "IC", "DSC")):
            m["asc_flow"][b] = (nm, round(o, 2))

    m["ic_flow"] = {}
    for b in ("Moon", "Jupiter", "Venus", "Sun"):
        nm, o = aspect(P[b], ic)
        if nm in FLOW:
            m["ic_flow"][b] = (nm, round(o, 2))

    for h, key in ((1, "h1"), (4, "h4"), (6, "h6")):
        cs = sg(cusps[h - 1])
        m[key] = (cs, DOM[cs], hp(P[DOM[cs]]), [b for b in BODIES if hp(P[b]) == h])
    for b in ("Venus", "Moon", "Sun"):
        m[b.lower() + "_h"] = hp(P[b])
    m["hard"] = {}
    for b in ("Saturn", "Mars", "Uranus", "Neptune", "Pluto", "Chiron"):
        for tgt, lab in ((asc, "ASC"), (ic, "IC")):
            nm, o = aspect(P[b], tgt)
            if nm == "conjunct":
                m["hard"].setdefault(b, []).append(f"conjunct {lab} {o:.1f}")
    return m


def main():
    grid = []
    lat = LAT0
    while lat <= LAT1:
        lon = LON0
        while lon <= LON1:
            grid.append((lat, lon, measure(lat, lon)))
            lon += STEP
        lat += STEP
    print(f"scanned {len(grid)} grid points at {STEP} degrees\n")

    print("=" * 96)
    print("STAGE 1 — WHERE THE INDEPENDENT EMBODIMENT CONTACTS OCCUR (no city names)")
    print("=" * 96)
    print("Reported: bodies conjunct/trine/sextile the Ascendant, excluding aspects")
    print("that merely restate an MC/IC/DSC conjunction.\n")

    keys = {}
    for lat, lon, m in grid:
        sig = tuple(sorted(m["asc_flow"]))
        keys.setdefault(sig, []).append((lat, lon, m))
    for sig, pts in sorted(keys.items(), key=lambda t: -len(t[1])):
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        if not sig:
            print(f"  (no flowing ASC contact)            {len(pts):>5} pts   "
                  f"lon {min(lons):.0f}..{max(lons):.0f}")
            continue
        ex = pts[len(pts) // 2][2]
        detail = ", ".join(f"{b} {ex['asc_flow'][b][0]} {ex['asc_flow'][b][1]}°" for b in sig)
        print(f"  {' + '.join(sig):<34}{len(pts):>5} pts   "
              f"lon {min(lons):>7.1f}..{max(lons):<7.1f} lat {min(lats):.0f}..{max(lats):.0f}")
        print(f"      mid-corridor sample: {detail}")

    print("\n" + "=" * 96)
    print("STAGE 1b — TIGHTEST FLOWING CONTACTS ANYWHERE ON THE GRID, by body")
    print("=" * 96)
    for b in ("Venus", "Sun", "Jupiter", "Moon"):
        best = sorted((m["asc_flow"][b][1], lat, lon, m["asc_flow"][b][0])
                      for lat, lon, m in grid if b in m["asc_flow"])
        if best:
            o, la, lo, kind = best[0]
            print(f"  {b:<9}{kind:<9}ASC   tightest {o:.2f}° near {la:.1f}N {abs(lo):.1f}W"
                  f"   ({len(best)} grid points in orb)")
        else:
            print(f"  {b:<9}no flowing contact to the Ascendant anywhere in the grid")

    print("\n" + "=" * 96)
    print("STAGE 1c — FLOWING CONTACTS TO THE IC (roots), same exclusion rule")
    print("=" * 96)
    for b in ("Moon", "Jupiter", "Venus", "Sun"):
        best = sorted((m["ic_flow"][b][1], lat, lon, m["ic_flow"][b][0])
                      for lat, lon, m in grid if b in m["ic_flow"])
        if best:
            o, la, lo, kind = best[0]
            lons = sorted({round(x[2], 1) for x in best})
            print(f"  {b:<9}{kind:<9}IC   tightest {o:.2f}° near {la:.1f}N {abs(lo):.1f}W"
                  f"   spans lon {min(lons):.0f}..{max(lons):.0f}")
        else:
            print(f"  {b:<9}no flowing contact to the IC anywhere in the grid")

    import json
    with open("blind_scan.json", "w") as f:
        json.dump([{"lat": la, "lon": lo,
                    "asc_flow": m["asc_flow"], "ic_flow": m["ic_flow"],
                    "angle_conj": m["angle_conj"], "hard": m["hard"],
                    "ruler": m["ruler"], "ruler_house": m["ruler_house"],
                    "venus_h": m["venus_h"], "moon_h": m["moon_h"], "sun_h": m["sun_h"]}
                   for la, lo, m in grid], f)
    print("\nwrote blind_scan.json")


if __name__ == "__main__":
    main()
