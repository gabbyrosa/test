#!/usr/bin/env python3
"""
Where is she most supported in feeling beautiful, comfortable, embodied,
confident and at home in her own body?

A deliberately fresh search. It does not use Venus-MC, career, money or the
9th house, and it does not carry forward any earlier shortlist. It records the
same raw fields everywhere and assigns no score:

  relocated Ascendant, its sign and its ruler, and where that ruler lands
  every planet in the 1st house, whole sign and Placidus
  Venus: house, exact distance and aspect to the Ascendant
  Sun: house, aspect to the Ascendant
  Moon: house, its ruler, aspects to Ascendant and IC
  4th house / IC: sign, ruler, where the ruler lands, occupants
  6th house: sign, ruler, occupants (daily embodied life)
  Jupiter, Saturn, Mars, Neptune: contacts to Ascendant, Moon, IC and rulers

Four questions are then read off those fields separately, so that a place can
answer one without being assumed to answer the others.
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
          "Uranus", "Neptune", "Pluto", "North Node", "South Node", "Chiron"]
ASPECTS = [("conjunct", 0, 8), ("sextile", 60, 5), ("square", 90, 6),
           ("trine", 120, 7), ("opposite", 180, 8), ("quincunx", 150, 3)]
EASY = {"conjunct", "sextile", "trine"}

D = natal.compute()
JD = D["jd"]
P = {n: D["planets"][n]["lon"] for n in BODIES}

CITIES = [
    ("Seattle WA", 47.61, -122.33), ("Portland OR", 45.52, -122.68),
    ("Eugene OR", 44.05, -123.09), ("Boise ID", 43.62, -116.20),
    ("Bozeman MT", 45.68, -111.04), ("Salt Lake City UT", 40.76, -111.89),
    ("Reno NV", 39.53, -119.81), ("San Francisco CA", 37.77, -122.42),
    ("Santa Cruz CA", 36.97, -122.03), ("Carmel CA", 36.56, -121.92),
    ("Santa Barbara CA", 34.42, -119.70), ("Ojai CA", 34.45, -119.24),
    ("Los Angeles CA", 34.05, -118.24), ("San Diego CA", 32.72, -117.16),
    ("Palm Springs CA", 33.83, -116.55), ("Las Vegas NV", 36.17, -115.14),
    ("Scottsdale AZ", 33.55, -111.95), ("Tucson AZ", 32.22, -110.97),
    ("Sedona AZ", 34.87, -111.76), ("Santa Fe NM", 35.69, -105.94),
    ("Denver CO", 39.74, -104.99), ("Durango CO", 37.28, -107.88),
    ("Austin TX", 30.27, -97.74), ("San Antonio TX", 29.42, -98.49),
    ("Marfa TX", 30.31, -104.02), ("Oklahoma City OK", 35.47, -97.52),
    ("Kansas City MO", 39.10, -94.58), ("Minneapolis MN", 44.98, -93.27),
    ("Madison WI", 43.07, -89.40), ("Chicago IL", 41.88, -87.63),
    ("Nashville TN", 36.16, -86.78), ("Louisville KY", 38.25, -85.76),
    ("New Orleans LA", 29.95, -90.07), ("Memphis TN", 35.15, -90.05),
    ("Atlanta GA", 33.75, -84.39), ("Asheville NC", 35.60, -82.55),
    ("Greenville SC", 34.85, -82.39), ("Charleston SC", 32.78, -79.93),
    ("Savannah GA", 32.08, -81.09), ("Charlotte NC", 35.23, -80.84),
    ("Wilmington NC", 34.23, -77.94), ("St. Petersburg FL", 27.77, -82.64),
    ("Sarasota FL", 27.34, -82.53), ("Naples FL", 26.14, -81.79),
    ("Miami FL", 25.76, -80.19), ("Orlando FL", 28.54, -81.38),
    ("Charlottesville VA", 38.03, -78.48), ("Richmond VA", 37.54, -77.44),
    ("Washington DC", 38.91, -77.04), ("Baltimore MD", 39.29, -76.61),
    ("Philadelphia PA", 39.95, -75.17), ("Pittsburgh PA", 40.44, -79.96),
    ("New York NY", 40.71, -74.01), ("Hudson NY", 42.25, -73.79),
    ("New Haven CT", 41.31, -72.93), ("Providence RI", 41.82, -71.41),
    ("Boston MA", 42.36, -71.06), ("Burlington VT", 44.48, -73.21),
    ("Portland ME", 43.66, -70.26), ("Bar Harbor ME", 44.39, -68.20),
]


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def aspect(a, b):
    sep = abs(n180(a - b))
    for nm, ang, orb in ASPECTS:
        if abs(sep - ang) <= orb:
            return nm, round(abs(sep - ang), 1)
    return None, None


def read(lat, lon):
    cusps, ascmc = swe.houses(JD, lat, lon, b"P")
    cusps = list(cusps)
    asc, mc = ascmc[0], ascmc[1]
    ic = (mc + 180) % 360
    ang = {"ASC": asc, "MC": mc, "DSC": (asc + 180) % 360, "IC": ic}
    ai = S.index(sg(asc))

    def hp(p):
        p %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
                return i + 1
        return 12

    def hw(p):
        return ((S.index(sg(p)) - ai) % 12) + 1

    def near(p):
        k, o = min(((k, abs(n180(p - v))) for k, v in ang.items()), key=lambda t: t[1])
        return k, round(o, 1)

    r = {}
    r["asc_sign"] = sg(asc)
    r["asc_deg"] = natal.fmt(asc)
    r["ruler"] = DOM[sg(asc)]
    r["ruler_hp"] = hp(P[r["ruler"]])
    r["ruler_hw"] = hw(P[r["ruler"]])
    r["first_p"] = [b for b in BODIES if hp(P[b]) == 1]
    r["first_w"] = [b for b in BODIES if hw(P[b]) == 1]
    r["venus_hp"], r["venus_hw"] = hp(P["Venus"]), hw(P["Venus"])
    r["venus_asc"] = aspect(P["Venus"], asc)
    r["venus_ang"] = near(P["Venus"])
    r["sun_hp"] = hp(P["Sun"])
    r["sun_asc"] = aspect(P["Sun"], asc)
    r["moon_hp"], r["moon_hw"] = hp(P["Moon"]), hw(P["Moon"])
    r["moon_ruler"] = DOM[sg(cusps[hp(P["Moon"]) - 1])]
    r["moon_asc"] = aspect(P["Moon"], asc)
    r["moon_ic"] = aspect(P["Moon"], ic)
    c4 = sg(cusps[3])
    r["ic_sign"], r["ic_ruler"] = c4, DOM[c4]
    r["ic_ruler_h"] = hp(P[DOM[c4]])
    r["fourth_occ"] = [b for b in BODIES if hp(P[b]) == 4]
    c6 = sg(cusps[5])
    r["sixth_sign"], r["sixth_ruler"] = c6, DOM[c6]
    r["sixth_occ"] = [b for b in BODIES if hp(P[b]) == 6]
    r["contacts"] = {}
    for b in ("Jupiter", "Saturn", "Mars", "Neptune"):
        for tgt, lab in ((asc, "ASC"), (P["Moon"], "Moon"), (ic, "IC")):
            a_, o_ = aspect(P[b], tgt)
            if a_:
                r["contacts"].setdefault(b, []).append(f"{a_} {lab} {o_}")
    return r


def main():
    out = {nm: read(la, lo) for nm, la, lo in CITIES}
    any_r = next(iter(out.values()))
    print("=" * 100)
    print("WHAT IS TRUE EVERYWHERE IN THE CONTIGUOUS US")
    print("=" * 100)
    signs = sorted({r["asc_sign"] for r in out.values()})
    print(f"  rising signs available: {', '.join(signs)}")
    for s in signs:
        sample = next(r for r in out.values() if r["asc_sign"] == s)
        print(f"\n  {s} rising  (ruler {sample['ruler']}, lands in h{sample['ruler_hp']} P / h{sample['ruler_hw']} WS)")
        print(f"     whole-sign 1st house holds: {', '.join(sample['first_w']) or 'nothing'}")
        print(f"     Venus to Ascendant: {sample['venus_asc'][0]} ({sample['venus_asc'][1]}°)")
        print(f"     Sun   to Ascendant: {sample['sun_asc'][0]} ({sample['sun_asc'][1]}°)")
        print(f"     Moon  to Ascendant: {sample['moon_asc'][0]} ({sample['moon_asc'][1]}°)")

    def show(title, rows, fmt):
        print("\n" + "=" * 100)
        print(title)
        print("=" * 100)
        for nm, r in rows:
            print(f"  {nm:<22}{fmt(r)}")

    # 1 — embodied Venus
    v = [(nm, r) for nm, r in out.items()
         if r["venus_hp"] == 1 or r["venus_hw"] == 1
         or (r["venus_asc"][0] in EASY) or r["venus_ang"][0] == "ASC"]
    v.sort(key=lambda t: (t[1]["venus_asc"][1] if t[1]["venus_asc"][0] in EASY else 99))
    show("1) EMBODIED VENUS — Venus in the 1st, on the Ascendant, or in easy aspect to it",
         v[:14], lambda r: f"Venus h{r['venus_hp']}P/h{r['venus_hw']}W, "
                           f"{r['venus_asc'][0]} ASC {r['venus_asc'][1]}°, ruler {r['ruler']}")

    # 2 — bodily confidence / vitality
    s = [(nm, r) for nm, r in out.items()
         if r["sun_hp"] in (1, 12) or (r["sun_asc"][0] in EASY)]
    s.sort(key=lambda t: (t[1]["sun_asc"][1] if t[1]["sun_asc"][0] in EASY else 99))
    show("2) BODILY CONFIDENCE / VITALITY — Sun in or near the 1st, or easy to the Ascendant",
         s[:14], lambda r: f"Sun h{r['sun_hp']}, {r['sun_asc'][0]} ASC {r['sun_asc'][1]}°")

    # 3 — emotional ease in the body
    m = [(nm, r) for nm, r in out.items()
         if (r["moon_asc"][0] in EASY) or (r["moon_ic"][0] in EASY)
         or r["moon_hp"] in (1, 4)]
    m.sort(key=lambda t: min(t[1]["moon_asc"][1] if t[1]["moon_asc"][0] in EASY else 99,
                             t[1]["moon_ic"][1] if t[1]["moon_ic"][0] in EASY else 99))
    show("3) EMOTIONAL EASE IN THE BODY — Moon easy to the Ascendant or IC, or in the 1st/4th",
         m[:14], lambda r: f"Moon h{r['moon_hp']} (ruler {r['moon_ruler']}), "
                           f"{r['moon_asc'][0]} ASC {r['moon_asc'][1]}°, {r['moon_ic'][0]} IC {r['moon_ic'][1]}°")

    # 4 — rooted / home
    h = [(nm, r) for nm, r in out.items()
         if r["fourth_occ"] or any("IC" in c for cs in r["contacts"].values() for c in cs)]
    def homescore(t):
        r = t[1]
        good = [c for b in ("Jupiter",) for c in r["contacts"].get(b, []) if "IC" in c]
        return (0 if good else 1, len(r["fourth_occ"]) * -1)
    h.sort(key=homescore)
    show("4) ROOTED / AT HOME — 4th-house occupants and benefic/malefic contacts to the IC",
         h[:14], lambda r: f"IC {r['ic_sign']} (ruler {r['ic_ruler']} h{r['ic_ruler_h']}), "
                           f"in 4th: {', '.join(r['fourth_occ']) or '-'} | "
                           + "; ".join(c for b, cs in r["contacts"].items() for c in cs if "IC" in c))

    # convergence
    print("\n" + "=" * 100)
    print("CONVERGENCE — cities appearing in more than one of the four")
    print("=" * 100)
    sets = {"Venus": {n for n, _ in v[:14]}, "Vitality": {n for n, _ in s[:14]},
            "Emotional": {n for n, _ in m[:14]}, "Home": {n for n, _ in h[:14]}}
    tally = {}
    for k, st in sets.items():
        for nm in st:
            tally.setdefault(nm, []).append(k)
    for nm, ks in sorted(tally.items(), key=lambda t: (-len(t[1]), t[0])):
        if len(ks) >= 2:
            print(f"  {nm:<22}{len(ks)} of 4:  {', '.join(sorted(ks))}")


if __name__ == "__main__":
    main()
