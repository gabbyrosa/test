#!/usr/bin/env python3
"""
Relocation-chart tools, the core of a professional relocation reading.

A relocation chart keeps the birth moment (same UT) but recomputes the house
framework for a new place: new Ascendant, new Midheaven, new house cusps, and
therefore new houses for every natal planet. Astrocartography lines are just
the special case of a planet sitting exactly on one of those new angles.

Also computes meridian-anchored parans (one body culminating while another
rises or sets), which are latitude phenomena the line map does not show.
"""

import math
import swisseph as swe

import natal
import astrocartography as acg

BODIES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
          "Uranus", "Neptune", "Pluto", "North Node", "Chiron"]
RULERS = {  # modern rulerships, for the relocated chart ruler
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Uranus",
    "Pisces": "Neptune",
}


def norm180(x):
    return ((x + 180.0) % 360.0) - 180.0


def relocate(lat, lon):
    d = natal.compute()
    jd = d["jd"]
    swe.set_ephe_path("/usr/share/swisseph")
    cusps, ascmc = swe.houses(jd, lat, lon, b"P")
    asc, mc = ascmc[0], ascmc[1]
    angles = {"AC": asc, "MC": mc, "DC": (asc + 180) % 360, "IC": (mc + 180) % 360}

    def house_of(lonp):
        lonp %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if a < b:
                if a <= lonp < b:
                    return i + 1
            elif lonp >= a or lonp < b:
                return i + 1
        return 12

    rows = []
    for name in BODIES:
        plon = d["planets"][name]["lon"]
        nearest = min(angles.items(), key=lambda kv: abs(norm180(plon - kv[1])))
        rows.append({
            "body": name, "lon": plon, "house": house_of(plon),
            "sign": d["planets"][name]["sign"],
            "angle": nearest[0], "orb": abs(norm180(plon - nearest[1])),
        })
    asc_sign = natal.SIGNS[natal.sign_of(asc)[0]]
    return {"asc": asc, "mc": mc, "asc_sign": asc_sign,
            "chart_ruler": RULERS[asc_sign], "rows": rows}


def parans(orb_lat=1.5):
    """Meridian-anchored parans: latitude where body1 culminates/anti-culminates
    while body2 rises/sets. Returns list of (b1, a1, b2, a2, latitude)."""
    d = natal.compute()
    pos = acg.positions(d["jd"])  # (name, slug, glyph, color, ra, dec)
    out = []
    for n1, _s1, _g1, _c1, ra1, dec1 in pos:
        for anchor, ra_anchor in (("MC", ra1), ("IC", ra1 + 180.0)):
            for n2, _s2, _g2, _c2, ra2, dec2 in pos:
                if n2 == n1 or abs(math.tan(math.radians(dec2))) < 1e-6:
                    continue
                h2 = norm180(ra_anchor - ra2)
                lat = math.degrees(math.atan(
                    -math.cos(math.radians(h2)) / math.tan(math.radians(dec2))))
                a2 = "AC" if h2 < 0 else "DC"
                out.append((n1, anchor, n2, a2, lat))
    return out


def parans_near(lat, orb=1.5):
    return sorted([p for p in parans() if abs(p[4] - lat) <= orb],
                  key=lambda p: abs(p[4] - lat))


def profile(lat, lon, angle_orb=8.0):
    """Fixed-protocol extraction for one city: the complete relocated chart
    facts, identical fields for every location. Interpretation happens
    elsewhere; this returns only computed facts."""
    d = natal.compute()
    jd = d["jd"]
    swe.set_ephe_path("/usr/share/swisseph")
    cusps, ascmc = swe.houses(jd, lat, lon, b"P")
    asc, mc = ascmc[0], ascmc[1]
    dsc, ic = (asc + 180) % 360, (mc + 180) % 360
    angles = {"ASC": asc, "IC": ic, "DSC": dsc, "MC": mc}

    def house_of(p):
        p %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
                return i + 1
        return 12

    def sign(x):
        return natal.SIGNS[int((x % 360) // 30)]

    bodies = BODIES + ["South Node"]
    planets = {}
    for n in bodies:
        p = d["planets"][n]["lon"]
        near, orb = min(((a, abs(norm180(p - al))) for a, al in angles.items()),
                        key=lambda t: t[1])
        planets[n] = {"house": house_of(p), "angle": near,
                      "orb": round(orb, 1), "sign": d["planets"][n]["sign"]}

    angular = sorted(
        [{"body": n, "angle": planets[n]["angle"], "orb": planets[n]["orb"],
          "house": planets[n]["house"]} for n in bodies
         if planets[n]["orb"] <= angle_orb],
        key=lambda x: x["orb"])

    angle_rulers = {}
    for a, al in angles.items():
        cs = sign(al)
        r = RULERS[cs]
        angle_rulers[a] = {"cusp_sign": cs, "ruler": r,
                           "ruler_house": house_of(d["planets"][r]["lon"]),
                           "ruler_sign": d["planets"][r]["sign"]}

    difficult = [x for x in angular
                 if x["body"] in ("Saturn", "Mars", "Pluto", "Neptune", "Uranus")]

    return {
        "asc": (round(asc % 30, 1), sign(asc)), "mc": (round(mc % 30, 1), sign(mc)),
        "dsc": (round(dsc % 30, 1), sign(dsc)), "ic": (round(ic % 30, 1), sign(ic)),
        "chart_ruler": RULERS[sign(asc)],
        "angular": angular, "planets": planets,
        "angle_rulers": angle_rulers, "difficult_angular": difficult,
        "parans": [{"b1": p[0], "a1": p[1], "b2": p[2], "a2": p[3],
                    "lat": round(p[4], 1)} for p in parans_near(lat)],
    }


def report(name, lat, lon):
    r = relocate(lat, lon)
    print(f"\n=== {name}  ({lat:.2f}, {lon:.2f}) ===")
    print(f"Relocated Ascendant: {natal.fmt(r['asc'])}  "
          f"(chart ruler now {r['chart_ruler']})")
    print(f"Relocated Midheaven: {natal.fmt(r['mc'])}")
    print("Angular planets (within 6 deg of an angle):")
    for row in sorted(r["rows"], key=lambda x: x["orb"]):
        if row["orb"] <= 6.0:
            print(f"  {row['body']:<11} on {row['angle']}  "
                  f"orb {row['orb']:.1f}deg  ({row['sign']})")
    print("Notable house shifts:")
    for row in r["rows"]:
        if row["body"] in ("Sun", "Moon", "Venus", "Jupiter", "Saturn"):
            print(f"  {row['body']:<11} house {row['house']}")
    pn = parans_near(lat)
    print(f"Parans within 1.5 deg of latitude {lat:.1f}:")
    for b1, a1, b2, a2, plat in pn[:8]:
        print(f"  {b1} {a1} / {b2} {a2}  at {plat:.1f} deg")


if __name__ == "__main__":
    report("Pittsburgh (natal)", 40.44, -79.96)
    report("Barcelona", 41.39, 2.17)
    report("Phoenix", 33.45, -112.07)
