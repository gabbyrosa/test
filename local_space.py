#!/usr/bin/env python3
"""
Local space astrology, computed from Pittsburgh.

Astrocartography asks "where on Earth is a planet on an angle?" and draws
lines across a world map. Local space asks a different question: standing at
one place, in what compass direction was each planet at the birth moment?

Each planet gets an azimuth (0 = due north, 90 = east, 180 = south, 270 =
west) and an altitude (above or below the horizon). Travelling or moving in a
planet's direction is held to engage that planet; so is orienting a room or a
home along it. Unlike astrocartography lines, these are great circles radiating
from a single origin, so they sweep across the globe and the "Venus direction"
from Pittsburgh hits entirely different countries than the Venus direction from
anywhere else.

Origin here is the birthplace, Magee-Womens Hospital, Pittsburgh, which is also
where she still lives, so the natal and current local-space maps coincide.

Outputs each planet's azimuth/altitude, the compass bearing, and the cities
and regions that fall along each great circle.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH
BODIES = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
          ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
          ("Saturn", swe.SATURN), ("Uranus", swe.URANUS),
          ("Neptune", swe.NEPTUNE), ("Pluto", swe.PLUTO)]
JD = swe.julday(1996, 6, 7, 15 + 35 / 60.0 - (-4), swe.GREG_CAL)
LAT, LON = 40.4426, -79.9614          # Pittsburgh (Magee-Womens)

COMPASS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
           "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

# candidate destinations to test against each great circle
PLACES = [
    ("Reykjavik, Iceland", 64.15, -21.94), ("Dublin, Ireland", 53.35, -6.26),
    ("London, UK", 51.51, -0.13), ("Paris, France", 48.86, 2.35),
    ("Lisbon, Portugal", 38.72, -9.14), ("Madrid, Spain", 40.42, -3.70),
    ("Barcelona, Spain", 41.39, 2.17), ("Valencia, Spain", 39.47, -0.38),
    ("Rome, Italy", 41.90, 12.50), ("Athens, Greece", 37.98, 23.73),
    ("Istanbul, Turkey", 41.01, 28.98), ("Stockholm, Sweden", 59.33, 18.07),
    ("Berlin, Germany", 52.52, 13.40), ("Zurich, Switzerland", 47.37, 8.54),
    ("Marrakech, Morocco", 31.63, -7.99), ("Dakar, Senegal", 14.72, -17.47),
    ("Lagos, Nigeria", 6.52, 3.38), ("Cairo, Egypt", 30.04, 31.24),
    ("Cape Town, South Africa", -33.92, 18.42), ("Nairobi, Kenya", -1.29, 36.82),
    ("Dubai, UAE", 25.20, 55.27), ("Mumbai, India", 19.08, 72.88),
    ("Tashkent, Uzbekistan", 41.30, 69.24), ("Samarkand, Uzbekistan", 39.63, 66.98),
    ("Bangkok, Thailand", 13.76, 100.50), ("Singapore", 1.35, 103.82),
    ("Bali, Indonesia", -8.65, 115.22), ("Tokyo, Japan", 35.68, 139.65),
    ("Kyoto, Japan", 35.01, 135.77), ("Seoul, South Korea", 37.57, 126.98),
    ("Taipei, Taiwan", 25.03, 121.57), ("Shanghai, China", 31.23, 121.47),
    ("Hong Kong", 22.32, 114.17), ("Manila, Philippines", 14.60, 120.98),
    ("Sydney, Australia", -33.87, 151.21), ("Melbourne, Australia", -37.81, 144.96),
    ("Auckland, New Zealand", -36.85, 174.76), ("Honolulu, HI", 21.31, -157.86),
    ("Anchorage, AK", 61.22, -149.90), ("Vancouver, Canada", 49.28, -123.12),
    ("Seattle, WA", 47.61, -122.33), ("Portland, OR", 45.52, -122.68),
    ("San Francisco, CA", 37.77, -122.42), ("Los Angeles, CA", 34.05, -118.24),
    ("San Diego, CA", 32.72, -117.16), ("Las Vegas, NV", 36.17, -115.14),
    ("Phoenix, AZ", 33.45, -112.07), ("Tucson, AZ", 32.22, -110.97),
    ("Santa Fe, NM", 35.69, -105.94), ("Denver, CO", 39.74, -104.99),
    ("Salt Lake City, UT", 40.76, -111.89), ("Bozeman, MT", 45.68, -111.04),
    ("Calgary, Canada", 51.05, -114.07), ("Austin, TX", 30.27, -97.74),
    ("New Orleans, LA", 29.95, -90.07), ("Miami, FL", 25.76, -80.19),
    ("St. Petersburg, FL", 27.77, -82.64), ("Asheville, NC", 35.60, -82.55),
    ("Charleston, SC", 32.78, -79.93), ("Savannah, GA", 32.08, -81.09),
    ("New York, NY", 40.71, -74.01), ("Boston, MA", 42.36, -71.06),
    ("Montreal, Canada", 45.50, -73.57), ("Toronto, Canada", 43.65, -79.38),
    ("Chicago, IL", 41.88, -87.63), ("Mexico City, Mexico", 19.43, -99.13),
    ("Cabo San Lucas, MX", 22.89, -109.92), ("Oaxaca, Mexico", 17.07, -96.72),
    ("San Miguel de Allende", 20.91, -100.74), ("Merida, Mexico", 20.97, -89.62),
    ("Panama City, Panama", 8.98, -79.52), ("San Jose, Costa Rica", 9.93, -84.08),
    ("Medellin, Colombia", 6.24, -75.58), ("Lima, Peru", -12.05, -77.04),
    ("Cuenca, Ecuador", -2.90, -79.00), ("Santiago, Chile", -33.45, -70.67),
    ("Buenos Aires, Argentina", -34.60, -58.38), ("Rio de Janeiro, Brazil", -22.91, -43.20),
    ("Sao Paulo, Brazil", -23.55, -46.63), ("Havana, Cuba", 23.11, -82.37),
    ("San Juan, Puerto Rico", 18.47, -66.11),
]

MEANING = {
    "Sun": "vitality, confidence, being central",
    "Moon": "comfort, belonging, emotional home",
    "Mercury": "voice, making, learning, hands (her Venus's working channel)",
    "Venus": "beauty, love, worth (her chart ruler)",
    "Mars": "drive, heat, assertion, friction",
    "Jupiter": "growth, luck, expansion",
    "Saturn": "structure, discipline, weight, mastery",
    "Uranus": "disruption, freedom, reinvention",
    "Neptune": "dream, romance, dissolution",
    "Pluto": "power, intensity, transformation",
}


def azalt(body):
    """Azimuth (from north, eastward) and altitude of a body at the origin."""
    lon_p, lat_p = swe.calc_ut(JD, body, FL)[0][:2]
    # equatorial -> horizon, via swe.azalt (expects ecliptic in, geo position)
    res = swe.azalt(JD, swe.ECL2HOR, [LON, LAT, 0.0], 0.0, 0.0,
                    [lon_p, lat_p, 1.0])
    az, true_alt = res[0], res[2]
    return az % 360.0, true_alt


def bearing_to(lat2, lon2):
    """Initial great-circle bearing from the origin to a destination."""
    p1, p2 = math.radians(LAT), math.radians(lat2)
    dl = math.radians(lon2 - LON)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(y, x)) % 360.0


def gc_dist_mi(lat2, lon2):
    p1, p2 = math.radians(LAT), math.radians(lat2)
    dl = math.radians(lon2 - LON)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2)
    return 3958.8 * 2 * math.asin(math.sqrt(a))


def compass(az):
    return COMPASS[int((az + 11.25) % 360 // 22.5)]


def main():
    print("LOCAL SPACE from Pittsburgh (40.44N, 79.96W), birth moment\n")
    print(f"{'planet':<9}{'azimuth':<10}{'dir':<6}{'altitude':<11}{'horizon':<12}meaning")
    print("-" * 108)
    rows = []
    for nm, b in BODIES:
        az, alt = azalt(b)
        rows.append((nm, az, alt))
        print(f"{nm:<9}{az:>6.1f}°{'':<3}{compass(az):<6}{alt:>+6.1f}°{'':<4}"
              f"{'above' if alt > 0 else 'below':<12}{MEANING[nm]}")

    print("\n\nWHAT LIES ALONG EACH DIRECTION (within 4° of the great circle)\n")
    for nm, az, alt in rows:
        hits = []
        for pn, la, lo in PLACES:
            d = abs(((bearing_to(la, lo) - az + 180) % 360) - 180)
            if d <= 4.0:
                hits.append((gc_dist_mi(la, lo), pn, d))
        hits.sort()
        tag = "" if alt > 0 else "   (below the horizon at birth)"
        print(f"  {nm} -> {compass(az)} {az:.1f}°{tag}")
        if hits:
            for mi, pn, d in hits[:7]:
                print(f"      {pn:<28}{mi:>6.0f} mi   off-line {d:.1f}°")
        else:
            print("      nothing in the test set lies along this direction")
        print()


if __name__ == "__main__":
    main()
