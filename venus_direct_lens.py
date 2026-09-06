#!/usr/bin/env python3
"""
Astrocartography re-scored through the "Venus is hers to generate" lens.

The earlier rankings implicitly asked: where does beauty/worth arrive from
outside? That suits a direct, unobstructed Venus. Hers is retrograde, born
combust at the inferior conjunction, and by secondary progression she went
morning-star at ~age 3, cleared the beams at ~age 8, and stationed direct at
~24.5. So the question is not where Venus is delivered but where she has room
to work. That reorders the angles:

  Venus on the ASCENDANT   you become it            highest
  Venus in the 1st or 2nd  body, and self-worth     high
  Venus on the MC          you are seen as it       moderate
  Venus on the DSC         it arrives via others    lowest of the four

and it promotes two things the old scoring barely counted:

  MERCURY   her Venus is in Gemini and her Mercury in Taurus, a mutual
            reception, and Mercury is direct. Mercury is the working channel:
            hands, making, tending, choosing. Mercury angular or in 1/2/6
            is Venus's tool being available.
  6th HOUSE her Pisces Moon lives there, so her feeling life is physically
            located in daily routine. A strong relocated 6th is a body that
            can be tended day to day.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
RUL = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Uranus",
       "Pisces": "Neptune"}
FL = swe.FLG_SWIEPH
BODIES = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
          ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
          ("Saturn", swe.SATURN), ("Uranus", swe.URANUS),
          ("Neptune", swe.NEPTUNE), ("Pluto", swe.PLUTO)]
JD = swe.julday(1996, 6, 7, 15 + 35 / 60.0 - (-4), swe.GREG_CAL)
P = {n: swe.calc_ut(JD, b, FL)[0][0] for n, b in BODIES}

exec(open("livable_rank.py").read().split("def n180")[0].split("CITIES = [")[1]
     .join(["CITIES = [", ""]) if False else "")
# reuse the vetted city + safety lists from the previous script
_src = open("livable_rank.py").read()
_ns = {}
exec("CITIES = [" + _src.split("CITIES = [", 1)[1].split("\n]", 1)[0] + "\n]", _ns)
exec("SAFETY = {" + _src.split("SAFETY = {", 1)[1].split("\n}", 1)[0] + "\n}", _ns)
CITIES, SAFETY = _ns["CITIES"], _ns["SAFETY"]

# angle weights under this lens
ANGLE_W = {"ASC": 1.00, "MC": 0.60, "IC": 0.55, "DSC": 0.40}


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def house_of(cusps, p):
    p %= 360.0
    for i in range(12):
        a, b = cusps[i], cusps[(i + 1) % 12]
        if (a < b and a <= p < b) or (a > b and (p >= a or p < b)):
            return i + 1
    return 12


def score(lat, lon):
    try:
        cusps, ascmc = swe.houses(JD, lat, lon, b"P")
    except swe.Error:
        cusps, ascmc = swe.houses(JD, lat, lon, b"W")
    asc, mc = ascmc[0], ascmc[1]
    ang = {"ASC": asc, "IC": (mc + 180) % 360, "DSC": (asc + 180) % 360, "MC": mc}
    s, why = 0.0, []

    def nearest(b):
        return min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                   key=lambda t: t[1])

    # --- Venus, weighted by which angle -----------------------------------
    a, o = nearest("Venus")
    if o <= 8:
        base = 4.0 if o <= 2 else 2.6 if o <= 5 else 1.3
        s += base * ANGLE_W[a]
        why.append(f"Venus {a} {o:.0f}°")
    vh = house_of(cusps, P["Venus"])
    if vh in (1, 2, 6):
        s += {1: 2.0, 2: 2.2, 6: 1.4}[vh]
        why.append(f"Venus h{vh}" + {1: " (body)", 2: " (self-worth)",
                                     6: " (daily practice)"}[vh])

    # --- Mercury, the working channel -------------------------------------
    a, o = nearest("Mercury")
    if o <= 6:
        s += 1.8 if o <= 3 else 1.0
        why.append(f"Mercury {a} {o:.0f}°")
    mh = house_of(cusps, P["Mercury"])
    if mh in (1, 2, 6):
        s += 1.2
        why.append(f"Mercury h{mh}")

    # --- the 6th house / daily body ---------------------------------------
    if house_of(cusps, P["Moon"]) == 6:
        s += 1.5
        why.append("Moon h6 (feeling lives in routine)")
    c6 = sg(cusps[5])
    if RUL[c6] in ("Venus", "Mercury", "Jupiter"):
        s += 0.6
        why.append(f"6th ruled by {RUL[c6]}")

    # --- supporting light --------------------------------------------------
    a, o = nearest("Sun")
    if o <= 6 and a == "ASC":
        s += 1.2
        why.append(f"Sun ASC {o:.0f}° (vitality in the body)")
    if RUL[sg(asc)] == "Venus":
        s += 1.0
        why.append("Venus rules chart")
    return s, why


rows = []
for nm, la, lo in CITIES:
    if SAFETY.get(nm) == "no":
        continue
    sc, why = score(la, lo)
    rows.append((sc, nm + (" *" if SAFETY.get(nm) == "caution" else ""), why))
rows.sort(key=lambda r: -r[0])
mx = rows[0][0]
print("ASTROCARTOGRAPHY THROUGH THE 'VENUS IS YOURS TO GENERATE' LENS")
print("Venus rising and Venus in the 1st/2nd outrank Venus on the MC or DSC.")
print("Mercury (her working channel) and the 6th house (her Moon) now count.\n")
print(f"{'#':<4}{'/10':<6}{'PLACE':<28}why")
print("-" * 124)
for i, (sc, nm, why) in enumerate(rows[:45], 1):
    print(f"{i:<4}{round(sc / mx * 10, 1):<6}{nm:<28}{', '.join(why)}")
print("\n* = elevated crime, harassment, or political risk.")
