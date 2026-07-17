#!/usr/bin/env python3
"""
Blind relocation comparison across a fixed city list.

For every city it computes the full relocation chart (relocated Ascendant, MC,
house cusps, every planet's relocated house, each planet's orb to the four
angles), the relocated Ascendant ruler and the rulers of the 4th/7th/10th with
their placements, nearby astrocartography lines (in miles), meridian-anchored
parans near the latitude, and any angular malefic.

It then applies ONE documented, mechanical rubric to grade eight dimensions
0-5. The city name is never an input to the rubric, so scoring is blind.
Cities are given hash-shuffled codes; the name mapping is revealed only after.

Weights are a transparent heuristic, not gospel; the raw data (written to
city_analysis.json) lets anyone re-interpret.
"""

import hashlib
import json
import math
import statistics

import swisseph as swe
import natal
import astrocartography as acg
import relocation

# --------------------------------------------------------------------------
CITIES = {
    # Europe
    "Barcelona": (41.39, 2.17), "Madrid": (40.42, -3.70),
    "Valencia": (39.47, -0.38), "Lisbon": (38.72, -9.14),
    "Paris": (48.86, 2.35), "Marseille": (43.30, 5.37),
    "Nice": (43.70, 7.27), "Lyon": (45.76, 4.84), "Milan": (45.46, 9.19),
    "Florence": (43.77, 11.26), "Rome": (41.90, 12.50),
    "Amsterdam": (52.37, 4.90), "London": (51.51, -0.13),
    # United States
    "Boston": (42.36, -71.06), "New York": (40.71, -74.01),
    "Washington DC": (38.90, -77.04), "Raleigh": (35.78, -78.64),
    "Charlotte": (35.23, -80.84), "Atlanta": (33.75, -84.39),
    "Nashville": (36.16, -86.78), "Columbus": (39.96, -83.00),
    "Detroit": (42.33, -83.05), "Chicago": (41.88, -87.63),
    "Phoenix": (33.45, -112.07), "Tucson": (32.22, -110.97),
    "Flagstaff": (35.20, -111.65), "Santa Fe": (35.69, -105.94),
    "Salt Lake City": (40.76, -111.89), "San Diego": (32.72, -117.16),
    "San Francisco": (37.77, -122.42), "Portland OR": (45.52, -122.68),
    "Seattle": (47.61, -122.33), "Denver": (39.74, -104.99),
    # Global
    "Tokyo": (35.68, 139.65), "San Jose CR": (9.93, -84.08),
    "Mexico City": (19.43, -99.13), "Montreal": (45.50, -73.57),
    "Vancouver": (49.28, -123.12),
}

RULER = relocation.RULERS
PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
           "Uranus", "Neptune", "Pluto", "North Node", "Chiron", "South Node"]
MALEFICS = ["Mars", "Saturn", "Pluto", "Uranus", "Neptune"]
FIXED = {"Taurus", "Leo", "Scorpio", "Aquarius"}

# Natal valence for THIS chart: benefic(+)/malefic(-) tuned by dignity, aspects,
# rulership. Venus is chart ruler (strong+) but retrograde; Jupiter benefic but
# in fall; Saturn undignified in Aries and opposite Chiron; Uranus dignified in
# Aquarius but disruptive.
BV = {
    "Sun": 1.0, "Moon": 0.3, "Mercury": 0.5, "Venus": 1.5, "Mars": -1.2,
    "Jupiter": 1.0, "Saturn": -1.2, "Uranus": -0.2, "Neptune": -0.4,
    "Pluto": -1.0, "North Node": 0.6, "Chiron": -0.6, "South Node": -0.6,
}

ORB = 8.0  # degrees; angular strength fades linearly to 0 at this orb

_D = natal.compute()
_JD = _D["jd"]
PLON = {n: _D["planets"][n]["lon"] for n in PLANETS}
_PARANS = relocation.parans()          # meridian-anchored, computed once
_ACG_POS = acg.positions(_JD)          # (name, slug, glyph, color, ra, dec)
_GMST = acg.gmst_deg(_JD)


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def strength(orb):
    return max(0.0, 1.0 - orb / ORB)


def clamp(v, lo=0.0, hi=5.0):
    return max(lo, min(hi, v))


def relocate_full(lat, lon):
    swe.set_ephe_path("/usr/share/swisseph")
    cusps, ascmc = swe.houses(_JD, lat, lon, b"P")
    asc, mc = ascmc[0], ascmc[1]
    angles = {"AC": asc, "MC": mc, "DC": (asc + 180) % 360, "IC": (mc + 180) % 360}

    def house_of(p):
        p %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
                return i + 1
        return 12

    planets = {}
    for n in PLANETS:
        p = PLON[n]
        orbs = {a: round(abs(n180(p - al)), 2) for a, al in angles.items()}
        planets[n] = {"lon": round(p, 2), "house": house_of(p), "orbs": orbs}

    def cusp_ruler(house_num):
        cs = natal.SIGNS[int(cusps[house_num - 1] // 30)]
        r = RULER[cs]
        return {"cusp_sign": cs, "ruler": r, "ruler_house": house_of(PLON[r]),
                "ruler_sign": _D["planets"][r]["sign"]}

    asc_sign = natal.SIGNS[int(asc // 30)]
    chart_ruler = RULER[asc_sign]

    # nearby astrocartography lines (miles), all bodies x 4 angles
    lines = []
    for nm, _slug, _g, _c, ra, dec in _ACG_POS:
        cand = [("MC", n180(ra - _GMST)), ("IC", n180(ra + 180 - _GMST))]
        x = -math.tan(math.radians(lat)) * math.tan(math.radians(dec))
        if -1 <= x <= 1:
            h0 = math.degrees(math.acos(x))
            cand += [("AC", n180(ra - h0 - _GMST)), ("DC", n180(ra + h0 - _GMST))]
        for ang, llon in cand:
            mi = abs(n180(lon - llon)) * 69.17 * math.cos(math.radians(lat))
            if mi <= 400:
                lines.append({"body": nm, "angle": ang, "miles": round(mi)})
    lines.sort(key=lambda d: d["miles"])

    pnear = [{"b1": p[0], "a1": p[1], "b2": p[2], "a2": p[3],
              "lat": round(p[4], 1)} for p in _PARANS if abs(p[4] - lat) <= 1.5]
    pnear.sort(key=lambda d: abs(d["lat"] - lat))

    ang_malefics = [{"body": n, "angle": min(planets[n]["orbs"], key=planets[n]["orbs"].get),
                     "orb": min(planets[n]["orbs"].values())}
                    for n in MALEFICS if min(planets[n]["orbs"].values()) <= 6.0]

    return {
        "asc": round(asc, 2), "asc_sign": asc_sign, "mc": round(mc, 2),
        "mc_sign": natal.SIGNS[int(mc // 30)],
        "cusps": [round(c, 2) for c in cusps],
        "chart_ruler": chart_ruler,
        "chart_ruler_house": house_of(PLON[chart_ruler]),
        "chart_ruler_sign": _D["planets"][chart_ruler]["sign"],
        "rulers": {"4": cusp_ruler(4), "7": cusp_ruler(7), "10": cusp_ruler(10)},
        "planets": planets, "acg_lines": lines[:10], "parans": pnear,
        "angular_malefics": ang_malefics,
    }


# --------------------------------------------------------------------------
# Rubric: mechanical, name-blind. Each dimension starts neutral (2.5) and takes
# documented contributions, then clamps to [0, 5].
def grade(rf):
    pl = rf["planets"]

    def s(n, ang):
        return strength(pl[n]["orbs"][ang])

    def s_any(n):
        return strength(min(pl[n]["orbs"].values()))

    def ruler_cond(house_num):  # valence of the ruler of a relocated house
        return BV[rf["rulers"][str(house_num)]["ruler"]]

    def occupants(house_num, bonus=0.0):  # planets sitting in a relocated house
        return sum(BV[n] + bonus for n in PLANETS if pl[n]["house"] == house_num)

    # 1 Home & rootedness: IC / 4th (conjunct-IC weighs most, 4th occupants next)
    home = 2.6
    home += sum(s(n, "IC") * BV[n] * 0.9 for n in PLANETS)
    home += occupants(4) * 0.35
    home += ruler_cond(4) * 0.5
    home += 0.5 * (BV["Moon"] + 0.4) * strength(pl["Moon"]["orbs"]["IC"])

    # 2 Relationships & belonging: DC / 7th (Venus is the natal significator)
    rel = 2.6
    rel += sum(s(n, "DC") * BV[n] * 0.9 for n in PLANETS)
    rel += occupants(7) * 0.35
    rel += ruler_cond(7) * 0.5
    rel += 0.8 * s("Venus", "DC")
    rel += 0.5 if pl["Venus"]["house"] == 7 else 0.0

    # 3 Career & visibility: MC / 10th (magnitude helps visibility; valence eases)
    car = 2.5
    car += sum(s(n, "MC") * (BV[n] + 0.6) * 0.85 for n in PLANETS)
    car += occupants(10, bonus=0.5) * 0.35
    car += ruler_cond(10) * 0.5

    # 4 Identity & confidence: AC / 1st + relocated ruler condition
    idn = 2.5
    idn += sum(s(n, "AC") * (BV[n] + 0.5) * 0.9 for n in PLANETS)
    idn += occupants(1, bonus=0.3) * 0.3
    idn += BV[rf["chart_ruler"]] * 0.5
    idn += 0.4 if rf["chart_ruler_house"] in (1, 10, 7, 4) else 0.0
    idn += 0.5 * s("Sun", "AC") + 0.4 * s("Jupiter", "AC")

    # 5 Emotional ease: benefics angular help, malefics angular hurt, an
    #    angular sensitive Moon tends to overwhelm
    emo = 2.8
    emo += sum(s_any(n) * BV[n] * 0.9 for n in ["Venus", "Jupiter", "Sun"])
    emo += sum(s_any(n) * BV[n] * 1.0 for n in MALEFICS)
    emo += -0.4 * s_any("Moon")

    # 6 Creativity & intellectual growth: Mercury/Venus/Neptune/Jupiter/Uranus
    cre = 2.5
    for n in ["Mercury", "Venus", "Neptune", "Jupiter", "Uranus"]:
        cre += s_any(n) * (0.6 + 0.25 * BV[n])
    cre += 0.4 if pl["Jupiter"]["house"] in (3, 9) else 0.0
    cre += 0.3 if pl["Mercury"]["house"] in (3, 9, 5) else 0.0

    # 7 Long-term stability: Saturn locks in, Uranus/Pluto/Neptune destabilise,
    #    fixed angles steady, benefics support
    sta = 2.6
    sta += 0.4 * s_any("Saturn")
    sta += -0.8 * s_any("Uranus") - 0.5 * s_any("Pluto") - 0.4 * s_any("Neptune")
    sta += -0.3 * s_any("Mars")
    sta += 0.4 * (rf["asc_sign"] in FIXED) + 0.4 * (rf["mc_sign"] in FIXED)
    sta += 0.3 * s_any("Venus") + 0.3 * s_any("Jupiter")

    dims = {"home": home, "relationships": rel, "career": car, "identity": idn,
            "emotional_ease": emo, "creativity": cre, "stability": sta}
    dims = {k: round(clamp(v), 2) for k, v in dims.items()}

    core = list(dims.values())
    balance = round(clamp(statistics.mean(core) - 0.45 * statistics.pstdev(core)), 2)
    dims["balance"] = balance

    # intensity: total angular malefic pull (for "strong but difficult")
    intensity = round(sum(strength(min(pl[n]["orbs"].values())) for n in MALEFICS), 2)
    growth = round(clamp((dims["identity"] + dims["creativity"]) / 2
                         + 0.4 * strength(min(pl["North Node"]["orbs"].values()))), 2)
    return dims, intensity, growth


def main():
    results = {}
    for city, (lat, lon) in CITIES.items():
        rf = relocate_full(lat, lon)
        dims, intensity, growth = grade(rf)
        results[city] = {"lat": lat, "lon": lon, "raw": rf, "grades": dims,
                         "intensity": intensity, "growth": growth}

    # blind, deterministic codes (hash-shuffled, no name order leak)
    codes = {c: f"C{ i+1:02d}" for i, c in enumerate(
        sorted(CITIES, key=lambda n: hashlib.md5(n.encode()).hexdigest()))}
    for c in results:
        results[c]["code"] = codes[c]

    with open("city_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)

    dim_order = ["home", "relationships", "career", "identity",
                 "emotional_ease", "creativity", "stability", "balance"]

    print("BLIND GRADES (0-5)")
    print("code " + " ".join(f"{d[:4]:>5}" for d in dim_order) + "  intns growth")
    for c in sorted(results, key=lambda c: results[c]["code"]):
        g = results[c]["grades"]
        row = " ".join(f"{g[d]:>5.1f}" for d in dim_order)
        print(f"{results[c]['code']} {row}  {results[c]['intensity']:>4.1f} "
              f"{results[c]['growth']:>5.1f}")

    print("\nREVEAL")
    for c in sorted(results, key=lambda c: results[c]["code"]):
        print(f"  {results[c]['code']} = {c}")

    def top(key, n=8, reverse=True):
        return sorted(results, key=key, reverse=reverse)[:n]

    print("\nRANKINGS")
    rankings = {
        "Best overall balance": lambda c: results[c]["grades"]["balance"],
        "Best for home": lambda c: results[c]["grades"]["home"],
        "Best for relationships": lambda c: results[c]["grades"]["relationships"],
        "Best for career": lambda c: results[c]["grades"]["career"],
        "Best for personal growth": lambda c: results[c]["growth"],
    }
    for title, key in rankings.items():
        print(f"\n{title}:")
        for c in top(key):
            print(f"  {c:<16} {key(c):.2f}")
    print("\nStrongest but potentially difficult (high intensity, lower ease/stability):")
    diff_key = (lambda c: results[c]["intensity"]
                - 0.3 * (results[c]["grades"]["emotional_ease"]
                         + results[c]["grades"]["stability"]))
    for c in top(diff_key):
        r = results[c]
        print(f"  {c:<16} intensity {r['intensity']:.1f}  "
              f"ease {r['grades']['emotional_ease']:.1f}  "
              f"stab {r['grades']['stability']:.1f}")


if __name__ == "__main__":
    main()
