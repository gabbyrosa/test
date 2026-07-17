#!/usr/bin/env python3
"""
Natal chart computation via the Swiss Ephemeris.

`compute()` returns a single dictionary with every value the report and the
chart-wheel renderer need, so both share one source of truth.
"""

import swisseph as swe

# --- Birth data -------------------------------------------------------------
# June 7, 1996, 3:35 PM EDT (Eastern Daylight Time = UTC-4)
BIRTH = {
    "date_label": "June 7, 1996",
    "time_label": "3:35 PM EDT",
    "place_label": "Pittsburgh, PA (Magee-Womens Hospital)",
    "year": 1996, "month": 6, "day": 7,
    "local_hour": 15, "local_min": 35,
    "utc_offset": -4,          # EDT
    "lat": 40.4426,            # Magee-Womens Hospital, Oakland, Pittsburgh
    "lon": -79.9614,           # west of Greenwich is negative
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
GLYPHS = {
    "Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀",
    "Mars": "♂", "Jupiter": "♃", "Saturn": "♄", "Uranus": "♅",
    "Neptune": "♆", "Pluto": "♇", "North Node": "☊",
    "South Node": "☋", "Chiron": "⚷",
}
SIGN_GLYPHS = ["♈", "♉", "♊", "♋", "♌", "♍",
               "♎", "♏", "♐", "♑", "♒", "♓"]
ELEMENTS = ["fire", "earth", "air", "water"] * 3  # Aries=fire, Taurus=earth, ...

BODIES = [
    ("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
    ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
    ("Pluto", swe.PLUTO), ("North Node", swe.TRUE_NODE), ("Chiron", swe.CHIRON),
]

ASPECTS = [
    ("Conjunction", 0, 8), ("Sextile", 60, 5), ("Square", 90, 6),
    ("Trine", 120, 7), ("Opposition", 180, 8),
]
HARMONIOUS = {"Sextile", "Trine"}
DYNAMIC = {"Square", "Opposition"}


def sign_of(lon):
    lon %= 360.0
    idx = int(lon // 30)
    pos = lon - idx * 30
    deg = int(pos)
    minute = int(round((pos - deg) * 60))
    if minute == 60:
        minute, deg = 0, deg + 1
    return idx, deg, minute


def fmt(lon):
    idx, deg, minute = sign_of(lon)
    return f"{deg}°{minute:02d}' {SIGNS[idx]}"


def compute():
    swe.set_ephe_path("/usr/share/swisseph")
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    ut = BIRTH["local_hour"] - BIRTH["utc_offset"] + BIRTH["local_min"] / 60.0
    jd = swe.julday(BIRTH["year"], BIRTH["month"], BIRTH["day"], ut, swe.GREG_CAL)

    planets = {}
    order = []
    for label, body in BODIES:
        res, _ = swe.calc_ut(jd, body, flags)
        lon, speed = res[0], res[3]
        idx, deg, minute = sign_of(lon)
        planets[label] = {
            "lon": lon, "speed": speed, "retro": speed < 0,
            "sign": SIGNS[idx], "sign_idx": idx, "deg": deg, "min": minute,
            "glyph": GLYPHS[label], "element": ELEMENTS[idx],
        }
        order.append(label)

    # South Node opposes the North (True) Node
    sn = (planets["North Node"]["lon"] + 180) % 360
    idx, deg, minute = sign_of(sn)
    planets["South Node"] = {
        "lon": sn, "speed": 0, "retro": False, "sign": SIGNS[idx],
        "sign_idx": idx, "deg": deg, "min": minute,
        "glyph": GLYPHS["South Node"], "element": ELEMENTS[idx],
    }

    cusps, ascmc = swe.houses(jd, BIRTH["lat"], BIRTH["lon"], b"P")  # Placidus
    asc, mc = ascmc[0], ascmc[1]
    asc_idx = sign_of(asc)[0]

    def house_of(lon):
        lon %= 360.0
        for i in range(12):
            a, b = cusps[i], cusps[(i + 1) % 12]
            if a < b:
                if a <= lon < b:
                    return i + 1
            elif lon >= a or lon < b:
                return i + 1
        return 12

    for label in planets:
        planets[label]["house"] = house_of(planets[label]["lon"])
        # Whole sign: the Ascendant's whole sign is the 1st house, and each
        # following sign is the next house.
        planets[label]["house_ws"] = (
            (planets[label]["sign_idx"] - asc_idx) % 12) + 1

    # Aspects among the ten planets + Chiron (nodes excluded to reduce clutter)
    aspect_names = [n for n in order if n != "North Node"]
    aspects = []
    for i in range(len(aspect_names)):
        for j in range(i + 1, len(aspect_names)):
            a, b = aspect_names[i], aspect_names[j]
            diff = abs(planets[a]["lon"] - planets[b]["lon"]) % 360
            if diff > 180:
                diff = 360 - diff
            for name, angle, orb in ASPECTS:
                if abs(diff - angle) <= orb:
                    aspects.append({
                        "a": a, "b": b, "type": name,
                        "orb": round(abs(diff - angle), 1),
                        "kind": ("harmony" if name in HARMONIOUS
                                 else "tension" if name in DYNAMIC
                                 else "conjunction"),
                    })
                    break

    return {
        "jd": jd, "asc": asc, "mc": mc, "cusps": list(cusps),
        "planets": planets, "order": order, "aspects": aspects,
        "birth": BIRTH, "asc_idx": asc_idx,
        "asc_sign": SIGNS[sign_of(asc)[0]], "mc_sign": SIGNS[sign_of(mc)[0]],
    }
