#!/usr/bin/env python3
"""
Full four-lens location scan.

For every city, compute the same fixed set of facts for each of the three
charts we care about, then score transparently:

  YOU      her relocated chart: benefics on angles, hard planets on angles,
           chart ruler, 6th-house/Moon condition
  HIM      his career + wealth: MC-line proximity for Sun/Jupiter/Saturn/Pluto,
           plus Fortune / Jupiter / Pluto landing in houses 2, 8, 10, 11
  US       the Davison relationship chart: benefic line proximity
  LIFE     climate + cost + walkability (hand-coded real-world data, NOT
           computed -- flagged as such in the output)

Weights follow her stated priorities: dry heat, wellness / nervous-system,
financial ease, walkable-not-isolated. Career-for-her is deliberately NOT
scored; she said she does not care about being valued for her work.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
RUL = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Uranus",
       "Pisces": "Neptune"}
FL, FLE = swe.FLG_SWIEPH, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL
BODIES = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
          ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
          ("Saturn", swe.SATURN), ("Uranus", swe.URANUS),
          ("Neptune", swe.NEPTUNE), ("Pluto", swe.PLUTO)]

JD_HER = swe.julday(1996, 6, 7, 15 + 35 / 60.0 - (-4), swe.GREG_CAL)
JD_HIM = swe.julday(1995, 7, 7, 0 + 1 / 60.0 - (-4), swe.GREG_CAL)
JD_DAV = (JD_HER + JD_HIM) / 2.0


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def lons(jd):
    return {n: swe.calc_ut(jd, b, FL)[0][0] for n, b in BODIES}


def mc_lon(jd, body):
    ra = swe.calc_ut(jd, body, FLE)[0][0]
    return n180(ra - swe.sidtime(jd) * 15.0)


def house_of(cusps, p):
    p %= 360.0
    for i in range(12):
        a, b = cusps[i], cusps[(i + 1) % 12]
        if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
            return i + 1
    return 12


HER, HIM, DAV = lons(JD_HER), lons(JD_HIM), lons(JD_DAV)
HIS_MC = {n: mc_lon(JD_HIM, b) for n, b in BODIES}


def angles_of(jd, lat, lon):
    cusps, ascmc = swe.houses(jd, lat, lon, b"P")
    asc, mc = ascmc[0], ascmc[1]
    return list(cusps), {"ASC": asc, "IC": (mc + 180) % 360,
                         "DSC": (asc + 180) % 360, "MC": mc}, asc, mc


def orb_to_angle(planet_lon, angles):
    a, o = min(((k, abs(n180(planet_lon - v))) for k, v in angles.items()),
               key=lambda t: t[1])
    return a, o


def line_mi(lat, lon, line_lon):
    return abs(n180(lon - line_lon)) * 69.17 * math.cos(math.radians(lat))


def dav_best(lat, lon):
    """Closest Davison benefic line (Venus/Jupiter/Sun/Moon, any angle)."""
    gmst = swe.sidtime(JD_DAV) * 15.0
    best = None
    for nm, b in [("Venus", swe.VENUS), ("Jupiter", swe.JUPITER),
                  ("Sun", swe.SUN), ("Moon", swe.MOON)]:
        ra, dec = swe.calc_ut(JD_DAV, b, FLE)[0][:2]
        cands = [("MC", n180(ra - gmst)), ("IC", n180(ra + 180 - gmst))]
        x = -math.tan(math.radians(lat)) * math.tan(math.radians(dec))
        if -1 <= x <= 1:
            h0 = math.degrees(math.acos(x))
            cands += [("AC", n180(ra - h0 - gmst)), ("DC", n180(ra + h0 - gmst))]
        for ang, llon in cands:
            mi = line_mi(lat, lon, llon)
            if best is None or mi < best[0]:
                best = (mi, nm, ang)
    return best


# ---- real-world data, hand-coded (NOT computed) ---------------------------
# (dry_heat 0-3, cost 0-3 cheap=3, walkable/scene 0-3)
LIFE = {
    "Tucson AZ": (3, 3, 2), "Phoenix AZ": (3, 2, 1), "Sedona AZ": (3, 1, 1),
    "Santa Fe NM": (3, 2, 2), "Albuquerque NM": (3, 3, 2), "El Paso TX": (3, 3, 1),
    "Las Cruces NM": (3, 3, 1), "St. George UT": (3, 2, 1), "Palm Springs CA": (3, 1, 2),
    "Las Vegas NV": (3, 2, 1), "Reno NV": (2, 2, 2), "Boise ID": (2, 2, 2),
    "Denver CO": (2, 1, 3), "Boulder CO": (2, 1, 3), "Salt Lake City UT": (2, 2, 2),
    "Austin TX": (1, 1, 3), "San Antonio TX": (1, 3, 2), "Marfa TX": (3, 3, 1),
    "San Diego CA": (2, 0, 3), "Los Angeles CA": (2, 0, 3), "Ojai CA": (2, 0, 1),
    "St. Petersburg FL": (0, 2, 3), "Sarasota FL": (0, 2, 2), "Miami FL": (0, 0, 3),
    "Asheville NC": (1, 2, 3), "Charleston SC": (0, 1, 3), "Savannah GA": (0, 2, 2),
    "New Orleans LA": (0, 2, 3), "Nashville TN": (0, 1, 3), "Pittsburgh PA": (0, 3, 2),
    "Chicago IL": (0, 2, 3), "New York NY": (0, 0, 3), "Portland OR": (0, 1, 3),
    "Honolulu HI": (0, 0, 2), "Barcelona ES": (2, 2, 3), "Madrid ES": (3, 2, 3),
    "Valencia ES": (2, 3, 3), "Seville ES": (3, 3, 2), "Lisbon PT": (2, 2, 3),
    "Athens GR": (3, 3, 3), "Rome IT": (2, 1, 3), "Florence IT": (2, 1, 3),
    "Milan IT": (1, 1, 3), "Nice FR": (2, 1, 3), "Paris FR": (0, 0, 3),
    "Marrakech MA": (3, 3, 2), "Istanbul TR": (1, 3, 3), "Dubai AE": (3, 0, 2),
    "Cape Town ZA": (2, 3, 3), "Mexico City MX": (1, 3, 3), "Oaxaca MX": (2, 3, 2),
    "Guadalajara MX": (2, 3, 2), "Monterrey MX": (2, 3, 2), "San Miguel MX": (2, 3, 2),
    "Cabo San Lucas MX": (3, 2, 1), "Medellin CO": (1, 3, 3), "Buenos Aires AR": (1, 3, 3),
    "Sydney AU": (1, 0, 3), "Tokyo JP": (0, 1, 3), "Kyoto JP": (0, 2, 3),
    "Bali ID": (0, 3, 2), "Singapore SG": (0, 0, 3), "Shanghai CN": (0, 1, 3),
}

CITIES = [
    ("Tucson AZ", 32.22, -110.97), ("Phoenix AZ", 33.45, -112.07),
    ("Sedona AZ", 34.87, -111.76), ("Santa Fe NM", 35.69, -105.94),
    ("Albuquerque NM", 35.08, -106.65), ("El Paso TX", 31.76, -106.49),
    ("Las Cruces NM", 32.32, -106.78), ("St. George UT", 37.10, -113.58),
    ("Palm Springs CA", 33.83, -116.55), ("Las Vegas NV", 36.17, -115.14),
    ("Reno NV", 39.53, -119.81), ("Boise ID", 43.62, -116.20),
    ("Denver CO", 39.74, -104.99), ("Boulder CO", 40.01, -105.27),
    ("Salt Lake City UT", 40.76, -111.89), ("Austin TX", 30.27, -97.74),
    ("San Antonio TX", 29.42, -98.49), ("Marfa TX", 30.31, -104.02),
    ("San Diego CA", 32.72, -117.16), ("Los Angeles CA", 34.05, -118.24),
    ("Ojai CA", 34.45, -119.24), ("St. Petersburg FL", 27.77, -82.64),
    ("Sarasota FL", 27.34, -82.53), ("Miami FL", 25.76, -80.19),
    ("Asheville NC", 35.60, -82.55), ("Charleston SC", 32.78, -79.93),
    ("Savannah GA", 32.08, -81.09), ("New Orleans LA", 29.95, -90.07),
    ("Nashville TN", 36.16, -86.78), ("Pittsburgh PA", 40.44, -79.96),
    ("Chicago IL", 41.88, -87.63), ("New York NY", 40.71, -74.01),
    ("Portland OR", 45.52, -122.68), ("Honolulu HI", 21.31, -157.86),
    ("Barcelona ES", 41.39, 2.17), ("Madrid ES", 40.42, -3.70),
    ("Valencia ES", 39.47, -0.38), ("Seville ES", 37.39, -5.98),
    ("Lisbon PT", 38.72, -9.14), ("Athens GR", 37.98, 23.73),
    ("Rome IT", 41.90, 12.50), ("Florence IT", 43.77, 11.26),
    ("Milan IT", 45.46, 9.19), ("Nice FR", 43.70, 7.27),
    ("Paris FR", 48.86, 2.35), ("Marrakech MA", 31.63, -7.99),
    ("Istanbul TR", 41.01, 28.98), ("Dubai AE", 25.20, 55.27),
    ("Cape Town ZA", -33.92, 18.42), ("Mexico City MX", 19.43, -99.13),
    ("Oaxaca MX", 17.07, -96.72), ("Guadalajara MX", 20.67, -103.35),
    ("Monterrey MX", 25.69, -100.32), ("San Miguel MX", 20.91, -100.74),
    ("Cabo San Lucas MX", 22.89, -109.92), ("Medellin CO", 6.24, -75.58),
    ("Buenos Aires AR", -34.60, -58.38), ("Sydney AU", -33.87, 151.21),
    ("Tokyo JP", 35.68, 139.65), ("Kyoto JP", 35.01, 135.77),
    ("Bali ID", -8.65, 115.22), ("Singapore SG", 1.35, 103.82),
    ("Shanghai CN", 31.23, 121.47),
]

BENEFIC = ("Venus", "Jupiter", "Sun", "Moon")
HARD = ("Mars", "Saturn", "Pluto")


def score_city(name, lat, lon):
    # ---- YOU -------------------------------------------------------------
    cusps, ang, asc, mc = angles_of(JD_HER, lat, lon)
    you, hits = 0.0, []
    for b in BENEFIC:
        a, o = orb_to_angle(HER[b], ang)
        if o <= 8:
            w = 3.0 if o <= 2 else 2.0 if o <= 5 else 1.0
            # personal angles (ASC/IC/DSC) matter more to her than MC,
            # EXCEPT Venus/Sun on MC = "seen as beautiful", which she asked for
            if a == "MC" and b in ("Venus", "Sun"):
                w *= 1.0
            elif a == "MC":
                w *= 0.5
            you += w
            hits.append(f"{b}{'' if o>2 else '!'}·{a}{o:.0f}°")
    hard = []
    for b in HARD:
        a, o = orb_to_angle(HER[b], ang)
        if o <= 6:
            pen = 2.5 if b == "Mars" else 1.5   # Mars = her out-of-sect malefic
            you -= pen * (1.0 if o <= 3 else 0.5)
            hard.append(f"{b}·{a}{o:.0f}°")
    if RUL[sg(asc)] == "Venus":
        you += 1.0
        hits.append("Venus rules chart")

    # ---- HIM -------------------------------------------------------------
    him, hhits = 0.0, []
    for b in ("Jupiter", "Pluto", "Sun", "Saturn"):
        d = abs(n180(lon - HIS_MC[b]))
        if d <= 8:
            him += 3.0 if d <= 2 else 2.0 if d <= 5 else 1.0
            hhits.append(f"{b}-MC {d:.0f}°")
    hc, hang, hasc, hmc = angles_of(JD_HIM, lat, lon)
    fortune = (hasc + HIM["Sun"] - HIM["Moon"]) % 360   # night formula
    for lbl, p in [("Fortune", fortune), ("Jupiter", HIM["Jupiter"]),
                   ("Pluto", HIM["Pluto"])]:
        h = house_of(hc, p)
        if h in (2, 8, 10, 11):
            him += 1.5
            hhits.append(f"{lbl} h{h}")

    # ---- US (Davison) ----------------------------------------------------
    mi, dnm, dang = dav_best(lat, lon)
    us = 3.0 if mi <= 150 else 2.0 if mi <= 400 else 1.0 if mi <= 700 else 0.0
    uhit = f"{dnm}·{dang} {mi:.0f}mi" if us else "-"

    # ---- LIFE (hand-coded) ----------------------------------------------
    dry, cost, walk = LIFE[name]
    life = dry * 1.6 + cost * 0.9 + walk * 0.9

    total = (max(you, 0) * 1.25) + (him * 0.75) + (us * 0.8) + (life * 0.62)
    return dict(name=name, you=you, him=him, us=us, life=life, total=total,
                hits=hits, hard=hard, hhits=hhits, uhit=uhit,
                dry=dry, cost=cost, walk=walk)


rows = sorted((score_city(*c) for c in CITIES),
              key=lambda r: -r["total"])
mx = rows[0]["total"]
print(f"{'#':<3}{'CITY':<19}{'/10':<6}{'you':<6}{'him':<6}{'us':<5}{'dry':<5}"
      f"why (you) | (him) | (us)")
print("-" * 150)
for i, r in enumerate(rows, 1):
    out10 = round(r["total"] / mx * 9.6, 1)
    why = ", ".join(r["hits"][:3]) or "no benefic angle"
    if r["hard"]:
        why += "  [" + ",".join(r["hard"]) + "]"
    print(f"{i:<3}{r['name']:<19}{out10:<6}{r['you']:<6.1f}{r['him']:<6.1f}"
          f"{r['us']:<5.1f}{r['dry']:<5}{why[:52]:<54}| "
          f"{', '.join(r['hhits'][:2])[:26]:<28}| {r['uhit']}")
