#!/usr/bin/env python3
"""
Every way the natal chart can express strongly across the United States.

Earlier scans in this repo asked one question ("where is Venus angular?") and
therefore could only ever return one kind of answer. This asks the opposite:
for a wide grid of US cities, compute the full relocated chart and let the
modes of expression emerge from the data.

For each city it records:
  - rising sign, the chart ruler, and where that ruler lands
  - every body within 8 deg of an angle (reported, never scored)
  - which houses accumulate planets (the chart's centre of gravity)
  - Lots of Fortune and Spirit: house and angularity
  - the 9th house, which natally holds Sun, Venus and Fortune
  - the money chain: 2nd cusp/ruler, 8th cusp/ruler
  - whether the chart ruler is itself angular or supported

Coherence is then measured structurally, not by preference: a chart is
coherent when the chart ruler is strong AND several independent significators
(angular bodies, house stacking, the Lots) point at the same few houses,
rather than scattering. That is a property of the chart, not of a wish.
"""

import math
from collections import Counter

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
          "Uranus", "Neptune", "Pluto"]
BENEFIC = ("Venus", "Jupiter")
LUMIN = ("Sun", "Moon")

D = natal.compute()
JD = D["jd"]
P = {n: D["planets"][n]["lon"] for n in BODIES}

HOUSE_THEME = {
    1: "self / body / presentation", 2: "income & self-worth",
    3: "mind, siblings, the local", 4: "home & roots", 5: "pleasure, creativity, romance",
    6: "daily work, health, routine", 7: "partnership & the public one-to-one",
    8: "shared resources, depth, transformation", 9: "the foreign, learning, worldview",
    10: "career & public standing", 11: "gains, friends, networks", 12: "retreat & the unseen",
}

CITIES = [
    ("Seattle WA", 47.61, -122.33), ("Portland OR", 45.52, -122.68),
    ("San Francisco CA", 37.77, -122.42), ("Santa Barbara CA", 34.42, -119.70),
    ("Los Angeles CA", 34.05, -118.24), ("San Diego CA", 32.72, -117.16),
    ("Palm Springs CA", 33.83, -116.55), ("Las Vegas NV", 36.17, -115.14),
    ("Boise ID", 43.62, -116.20), ("Salt Lake City UT", 40.76, -111.89),
    ("Bozeman MT", 45.68, -111.04), ("Scottsdale AZ", 33.55, -111.95),
    ("Sedona AZ", 34.87, -111.76), ("Tucson AZ", 32.22, -110.97),
    ("Santa Fe NM", 35.69, -105.94), ("Albuquerque NM", 35.08, -106.65),
    ("Denver CO", 39.74, -104.99), ("Boulder CO", 40.01, -105.27),
    ("Austin TX", 30.27, -97.74), ("San Antonio TX", 29.42, -98.49),
    ("Dallas TX", 32.78, -96.80), ("Houston TX", 29.76, -95.37),
    ("Kansas City MO", 39.10, -94.58), ("Minneapolis MN", 44.98, -93.27),
    ("New Orleans LA", 29.95, -90.07), ("Chicago IL", 41.88, -87.63),
    ("Nashville TN", 36.16, -86.78), ("Atlanta GA", 33.75, -84.39),
    ("Asheville NC", 35.60, -82.55), ("Charleston SC", 32.78, -79.93),
    ("Savannah GA", 32.08, -81.09), ("St. Petersburg FL", 27.77, -82.64),
    ("Sarasota FL", 27.34, -82.53), ("Miami FL", 25.76, -80.19),
    ("Richmond VA", 37.54, -77.44), ("Washington DC", 38.91, -77.04),
    ("Philadelphia PA", 39.95, -75.17), ("Pittsburgh PA", 40.44, -79.96),
    ("New York NY", 40.71, -74.01), ("Boston MA", 42.36, -71.06),
    ("Burlington VT", 44.48, -73.21), ("Portland ME", 43.66, -70.26),
    ("Honolulu HI", 21.31, -157.86), ("Anchorage AK", 61.22, -149.90),
]


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def chart(lat, lon):
    cusps, ascmc = swe.houses(JD, lat, lon, b"P")
    cusps = list(cusps)
    asc, mc = ascmc[0], ascmc[1]
    ang = {"ASC": asc, "MC": mc, "DSC": (asc + 180) % 360, "IC": (mc + 180) % 360}

    def hof(p):
        p %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
                return i + 1
        return 12

    def near(p):
        return min(((k, abs(n180(p - v))) for k, v in ang.items()), key=lambda t: t[1])

    ruler = DOM[sg(asc)]
    fortune = (asc + P["Moon"] - P["Sun"]) % 360
    spirit = (asc + P["Sun"] - P["Moon"]) % 360
    angular = {b: near(P[b]) for b in BODIES if near(P[b])[1] <= 8}
    houses = Counter(hof(P[b]) for b in BODIES)

    # --- structural coherence, computed not chosen ------------------------
    rk, ro = near(P[ruler])
    ruler_house = hof(P[ruler])
    ruler_strength = (3 if ro <= 3 else 2 if ro <= 8 else 0) \
        + (2 if ruler_house in (1, 10) else 1 if ruler_house in (4, 7, 9, 11) else 0)

    # where do the independent significators point?
    votes = Counter()
    for b, (k, o) in angular.items():
        votes[hof(P[b])] += 2 if o <= 3 else 1
    votes[hof(fortune)] += 2
    votes[hof(spirit)] += 2
    votes[ruler_house] += 2
    for h, n in houses.items():
        if n >= 3:
            votes[h] += n
    top = votes.most_common(3)
    focus = sum(v for _, v in top)
    spread = len([h for h, v in votes.items() if v >= 2])
    coherence = round(ruler_strength + focus / 2.0 - spread * 0.6, 1)

    return dict(
        asc=sg(asc), ruler=ruler, ruler_house=ruler_house, ruler_angle=(rk, round(ro, 1)),
        angular={b: (k, round(o, 1)) for b, (k, o) in angular.items()},
        houses=houses, fortune_h=hof(fortune), spirit_h=hof(spirit),
        fortune_ang=round(near(fortune)[1], 1), spirit_ang=round(near(spirit)[1], 1),
        ninth=[b for b in BODIES if hof(P[b]) == 9],
        c2=sg(cusps[1]), r2=DOM[sg(cusps[1])], r2h=hof(P[DOM[sg(cusps[1])]]),
        c8=sg(cusps[7]), r8=DOM[sg(cusps[7])], r8h=hof(P[DOM[sg(cusps[7])]]),
        top=top, coherence=coherence)


def main():
    out = {nm: chart(la, lo) for nm, la, lo in CITIES}

    print("=" * 108)
    print("THE MODES — grouping cities by which houses their significators agree on")
    print("=" * 108)
    groups = {}
    for nm, r in out.items():
        key = tuple(sorted(h for h, _ in r["top"][:2]))
        groups.setdefault(key, []).append((r["coherence"], nm, r))
    for key in sorted(groups, key=lambda k: -max(x[0] for x in groups[k])):
        members = sorted(groups[key], reverse=True)
        theme = " + ".join(f"{h}th ({HOUSE_THEME[h]})" for h in key)
        print(f"\n  ▸ {theme}")
        for coh, nm, r in members:
            ang = ", ".join(f"{b} {k}{o:.0f}" for b, (k, o) in
                            sorted(r["angular"].items(), key=lambda t: t[1][1])[:4])
            print(f"      {coh:>5}  {nm:<20}{r['asc'][:3]}↑ {r['ruler']:<8}"
                  f"h{r['ruler_house']:<3} | {ang or 'nothing angular'}")

    print("\n" + "=" * 108)
    print("MOST COHERENT RELOCATED CHARTS overall")
    print("=" * 108)
    print(f"  {'coh':>5}  {'CITY':<20}{'rising':<7}{'ruler':<18}"
          f"{'Fortune':<10}{'Spirit':<10}{'focus houses'}")
    for coh, nm, r in sorted(((v["coherence"], k, v) for k, v in out.items()), reverse=True)[:14]:
        print(f"  {coh:>5}  {nm:<20}{r['asc'][:3]:<7}"
              f"{r['ruler']+' h'+str(r['ruler_house']):<18}"
              f"h{r['fortune_h']:<9}h{r['spirit_h']:<9}"
              f"{', '.join(str(h) for h, _ in r['top'])}")


if __name__ == "__main__":
    main()
