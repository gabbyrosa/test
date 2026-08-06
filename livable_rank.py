#!/usr/bin/env python3
"""
Rank livable places worldwide on the natal chart alone.

"Livable" is a hand-applied filter, not a computed one: a real city or town
with infrastructure and healthcare that an American working remotely could
plausibly relocate to. Excluded on those grounds (not chart grounds):
uninhabited land (Kerguelen, Greenland interior, Sahara), active conflict or
severe-risk zones (Afghanistan, Balochistan), and Russia/Belarus on current
relocation viability. Those exclusions are listed in EXCLUDED below so the
filter stays auditable.

Scoring is pure chart: benefics on angles, malefics on angles, chart ruler,
Moon's house. No climate, no cost, no second chart.
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
BENEFIC = ("Venus", "Jupiter", "Sun", "Moon")
HARD = ("Mars", "Saturn", "Pluto")

EXCLUDED = [
    ("Balochistan / Quetta PK", "global chart peak, excluded: severe security risk"),
    ("Kabul / Mazar AF", "very high chart score, excluded: active conflict"),
    ("Dushanbe TJ", "high chart score, excluded: thin infrastructure, marginal"),
    ("Novosibirsk / Tyumen RU", "high chart score, excluded: relocation not viable"),
    ("Kerguelen (49S 69E)", "highest raw grid point in S. hemisphere, uninhabited"),
    ("N. Canada / Nunavut", "strong Jupiter-IC, excluded: no practical settlement"),
    ("Sahara interior", "Venus-DSC band, excluded: uninhabited"),
]

CITIES = [
    # --- Central Asia (the global peak corridor, livable end) --------------
    ("Almaty, Kazakhstan", 43.24, 76.89), ("Astana, Kazakhstan", 51.17, 71.43),
    ("Tashkent, Uzbekistan", 41.30, 69.24), ("Samarkand, Uzbekistan", 39.63, 66.98),
    ("Bishkek, Kyrgyzstan", 42.87, 74.59),
    # --- South Asia --------------------------------------------------------
    ("Mumbai, India", 19.08, 72.88), ("Goa, India", 15.30, 74.08),
    ("Bengaluru, India", 12.97, 77.59), ("Karachi, Pakistan", 24.86, 67.01),
    ("Kathmandu, Nepal", 27.72, 85.32), ("Colombo, Sri Lanka", 6.93, 79.86),
    ("Dubai, UAE", 25.20, 55.27), ("Muscat, Oman", 23.59, 58.41),
    # --- East / SE Asia ----------------------------------------------------
    ("Tokyo, Japan", 35.68, 139.65), ("Kyoto, Japan", 35.01, 135.77),
    ("Fukuoka, Japan", 33.59, 130.40), ("Seoul, South Korea", 37.57, 126.98),
    ("Busan, South Korea", 35.18, 129.08), ("Taipei, Taiwan", 25.03, 121.57),
    ("Shanghai, China", 31.23, 121.47), ("Hong Kong", 22.32, 114.17),
    ("Bangkok, Thailand", 13.76, 100.50), ("Chiang Mai, Thailand", 18.79, 98.98),
    ("Singapore", 1.35, 103.82), ("Bali, Indonesia", -8.65, 115.22),
    ("Ho Chi Minh City, Vietnam", 10.82, 106.63), ("Manila, Philippines", 14.60, 120.98),
    # --- Oceania -----------------------------------------------------------
    ("Sydney, Australia", -33.87, 151.21), ("Melbourne, Australia", -37.81, 144.96),
    ("Brisbane, Australia", -27.47, 153.03), ("Perth, Australia", -31.95, 115.86),
    ("Auckland, New Zealand", -36.85, 174.76), ("Noumea, New Caledonia", -22.28, 166.46),
    # --- Europe ------------------------------------------------------------
    ("Barcelona, Spain", 41.39, 2.17), ("Valencia, Spain", 39.47, -0.38),
    ("Madrid, Spain", 40.42, -3.70), ("Seville, Spain", 37.39, -5.98),
    ("Malaga, Spain", 36.72, -4.42), ("Palma, Mallorca", 39.57, 2.65),
    ("Lisbon, Portugal", 38.72, -9.14), ("Porto, Portugal", 41.15, -8.61),
    ("Nice, France", 43.70, 7.27), ("Paris, France", 48.86, 2.35),
    ("Lyon, France", 45.76, 4.84), ("Milan, Italy", 45.46, 9.19),
    ("Rome, Italy", 41.90, 12.50), ("Florence, Italy", 43.77, 11.26),
    ("Munich, Germany", 48.14, 11.58), ("Stuttgart, Germany", 48.78, 9.18),
    ("Zurich, Switzerland", 47.37, 8.54), ("Berlin, Germany", 52.52, 13.40),
    ("Amsterdam, Netherlands", 52.37, 4.90), ("Copenhagen, Denmark", 55.68, 12.57),
    ("Stockholm, Sweden", 59.33, 18.07), ("Oslo, Norway", 59.91, 10.75),
    ("Gdansk, Poland", 54.35, 18.65), ("Krakow, Poland", 50.06, 19.94),
    ("Tallinn, Estonia", 59.44, 24.75), ("Riga, Latvia", 56.95, 24.11),
    ("Vienna, Austria", 48.21, 16.37), ("Prague, Czechia", 50.08, 14.44),
    ("Budapest, Hungary", 47.50, 19.04), ("Athens, Greece", 37.98, 23.73),
    ("Split, Croatia", 43.51, 16.44), ("Istanbul, Turkey", 41.01, 28.98),
    ("London, UK", 51.51, -0.13), ("Dublin, Ireland", 53.35, -6.26),
    ("Reykjavik, Iceland", 64.15, -21.94),
    # --- Africa / Middle East ---------------------------------------------
    ("Marrakech, Morocco", 31.63, -7.99), ("Casablanca, Morocco", 33.57, -7.59),
    ("Agadir, Morocco", 30.43, -9.60), ("Essaouira, Morocco", 31.51, -9.77),
    ("Tangier, Morocco", 35.76, -5.83), ("Dakar, Senegal", 14.72, -17.47),
    ("Cairo, Egypt", 30.04, 31.24), ("Nairobi, Kenya", -1.29, 36.82),
    ("Cape Town, South Africa", -33.92, 18.42), ("Tel Aviv, Israel", 32.08, 34.78),
    # --- Latin America -----------------------------------------------------
    ("La Paz, Baja Sur MX", 24.14, -110.31), ("Todos Santos, Baja Sur", 23.45, -110.22),
    ("Cabo San Lucas, MX", 22.89, -109.92), ("Loreto, Baja Sur MX", 26.01, -111.34),
    ("Hermosillo, Mexico", 29.07, -110.97), ("Chihuahua, Mexico", 28.63, -106.08),
    ("Guadalajara, Mexico", 20.67, -103.35), ("San Miguel de Allende", 20.91, -100.74),
    ("Mexico City, Mexico", 19.43, -99.13), ("Oaxaca, Mexico", 17.07, -96.72),
    ("Merida, Mexico", 20.97, -89.62), ("Panama City, Panama", 8.98, -79.52),
    ("San Jose, Costa Rica", 9.93, -84.08), ("Medellin, Colombia", 6.24, -75.58),
    ("Lima, Peru", -12.05, -77.04), ("Cuenca, Ecuador", -2.90, -79.00),
    ("Santiago, Chile", -33.45, -70.67), ("Buenos Aires, Argentina", -34.60, -58.38),
    ("Montevideo, Uruguay", -34.90, -56.16), ("Sao Paulo, Brazil", -23.55, -46.63),
    # --- North America -----------------------------------------------------
    ("Tucson, AZ", 32.22, -110.97), ("Phoenix, AZ", 33.45, -112.07),
    ("Sedona, AZ", 34.87, -111.76), ("Flagstaff, AZ", 35.20, -111.65),
    ("Santa Fe, NM", 35.69, -105.94), ("Albuquerque, NM", 35.08, -106.65),
    ("Las Cruces, NM", 32.32, -106.78), ("El Paso, TX", 31.76, -106.49),
    ("St. George, UT", 37.10, -113.58), ("Salt Lake City, UT", 40.76, -111.89),
    ("Moab, UT", 38.57, -109.55), ("Las Vegas, NV", 36.17, -115.14),
    ("Reno, NV", 39.53, -119.81), ("Boise, ID", 43.62, -116.20),
    ("Missoula, MT", 46.87, -113.99), ("Bozeman, MT", 45.68, -111.04),
    ("Denver, CO", 39.74, -104.99), ("Boulder, CO", 40.01, -105.27),
    ("Calgary, Canada", 51.05, -114.07), ("Vancouver, Canada", 49.28, -123.12),
    ("Palm Springs, CA", 33.83, -116.55), ("San Diego, CA", 32.72, -117.16),
    ("Los Angeles, CA", 34.05, -118.24), ("Ojai, CA", 34.45, -119.24),
    ("San Francisco, CA", 37.77, -122.42), ("Portland, OR", 45.52, -122.68),
    ("Seattle, WA", 47.61, -122.33), ("Austin, TX", 30.27, -97.74),
    ("San Antonio, TX", 29.42, -98.49), ("Marfa, TX", 30.31, -104.02),
    ("St. Petersburg, FL", 27.77, -82.64), ("Sarasota, FL", 27.34, -82.53),
    ("Miami, FL", 25.76, -80.19), ("Asheville, NC", 35.60, -82.55),
    ("Savannah, GA", 32.08, -81.09), ("Charleston, SC", 32.78, -79.93),
    ("Nashville, TN", 36.16, -86.78), ("New Orleans, LA", 29.95, -90.07),
    ("Chicago, IL", 41.88, -87.63), ("New York, NY", 40.71, -74.01),
    ("Pittsburgh, PA", 40.44, -79.96), ("Honolulu, HI", 21.31, -157.86),
]


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def score(lat, lon):
    try:
        cusps, ascmc = swe.houses(JD, lat, lon, b"P")
    except swe.Error:
        cusps, ascmc = swe.houses(JD, lat, lon, b"W")
    asc, mc = ascmc[0], ascmc[1]
    ang = {"ASC": asc, "IC": (mc + 180) % 360,
           "DSC": (asc + 180) % 360, "MC": mc}
    s, hits, hard = 0.0, [], []
    for b in BENEFIC:
        a, o = min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                   key=lambda t: t[1])
        if o <= 8:
            w = 3.0 if o <= 2 else 2.0 if o <= 5 else 1.0
            if a == "MC" and b not in ("Venus", "Sun"):
                w *= 0.5
            s += w
            hits.append(f"{b} {a} {o:.0f}°")
    for b in HARD:
        a, o = min(((k, abs(n180(P[b] - v))) for k, v in ang.items()),
                   key=lambda t: t[1])
        if o <= 6:
            s -= (2.5 if b == "Mars" else 1.5) * (1.0 if o <= 3 else 0.5)
            hard.append(f"{b} {a} {o:.0f}°")
    if RUL[sg(asc)] == "Venus":
        s += 1.0
        hits.append("Venus rules chart")
    p = P["Moon"] % 360
    for i in range(12):
        a2, b2 = cusps[i], cusps[(i + 1) % 12]
        if (a2 < b2 and a2 <= p < b2) or (a2 > b2 and (p >= a2 or p < b2)):
            if i + 1 == 6:
                s += 0.75
                hits.append("Moon h6")
            break
    return s, hits, hard


# --- safety filter, hand-applied and auditable -----------------------------
# "no"      = excluded outright
# "caution" = included but flagged; elevated crime, harassment, or political risk
# Assessment reflects general knowledge as of early 2026, NOT live advisories.
SAFETY = {
    "Karachi, Pakistan": "no", "Cairo, Egypt": "no", "Manila, Philippines": "no",
    "Nairobi, Kenya": "no", "Tel Aviv, Israel": "no", "Sao Paulo, Brazil": "no",
    "Lima, Peru": "caution", "Mexico City, Mexico": "caution",
    "Medellin, Colombia": "caution", "Buenos Aires, Argentina": "caution",
    "Cape Town, South Africa": "caution", "Marrakech, Morocco": "caution",
    "Casablanca, Morocco": "caution", "Dakar, Senegal": "caution",
    "Shanghai, China": "caution", "Hong Kong": "caution",
    "Istanbul, Turkey": "caution", "Bishkek, Kyrgyzstan": "caution",
    "Astana, Kazakhstan": "caution", "Almaty, Kazakhstan": "caution",
    "Tashkent, Uzbekistan": "caution", "Samarkand, Uzbekistan": "caution",
    "New Orleans, LA": "caution", "Chihuahua, Mexico": "caution",
    "Hermosillo, Mexico": "caution", "Ho Chi Minh City, Vietnam": "caution",
    "Kathmandu, Nepal": "caution", "Colombo, Sri Lanka": "caution",
    "Mumbai, India": "caution", "Bengaluru, India": "caution",
    "Goa, India": "caution",
}

rows, dropped = [], []
for nm, la, lo in CITIES:
    s, hits, hard = score(la, lo)
    if SAFETY.get(nm) == "no":
        dropped.append((s, nm))
        continue
    if SAFETY.get(nm) == "caution":
        nm += " *"
    rows.append((s, nm, hits, hard))
rows.sort(key=lambda r: -r[0])
mx = rows[0][0]
print(f"{len(rows)} livable places, scored on the natal chart alone.\n")
print(f"{'#':<4}{'/10':<6}{'PLACE':<28}why")
print("-" * 122)
for i, (s, nm, hits, hard) in enumerate(rows, 1):
    v = round(max(s, 0) / mx * 10, 1)
    w = ", ".join(hits) or "no benefic on an angle"
    if hard:
        w += "   AVOID: " + ", ".join(hard)
    print(f"{i:<4}{v:<6}{nm:<28}{w}")
print("\n* = included but flagged: elevated crime, harassment, or political risk.")
print("\nDROPPED on safety (chart score shown, so nothing is hidden):")
for s, nm in sorted(dropped, key=lambda d: -d[0]):
    print(f"  {nm:<28}raw {s:.2f}")
print("\nEXCLUDED as not livable (chart score would have placed them high):")
for nm, why in EXCLUDED:
    print(f"  {nm:<28}{why}")
