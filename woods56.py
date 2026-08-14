#!/usr/bin/env python3
"""
Stages 5 and 6 of the Helena Woods-method analysis: local space, then timing.

STAGE 5 — LOCAL SPACE
  Attributable: Woods treats local space as a SEPARATE directional system from
  astrocartography, one that "does not use houses" and shows planetary energies
  directionally from a location.
  NOT attributable: she does not publish a local space orb. This file therefore
  reports the raw azimuth difference AND the perpendicular (cross-track)
  distance in miles from the great circle, and leaves the orb question open.

  Local space lines are GREAT CIRCLES, so the compass bearing changes along the
  path. Comparing a city's bearing to a planet's azimuth is only valid at the
  origin; the honest measure is cross-track distance, which this file computes.

STAGE 6 — TIMING
  Attributable: Woods uses cyclocartography plus transits, progressions and
  solar returns; she states progressions can last up to 3 years and transits
  from a few days to 3 years, and that hard transits or progressions to the
  angles of the RELOCATED chart bring difficulty even on a supportive line.
  NOT attributable: she does not publish orbs for these, nor a rule ranking
  them against each other.

  Because relocated angles differ by city, transits to them are
  location-specific. That is the whole point of doing this after Stage 4.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH | swe.FLG_SPEED
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
BLAT, BLON = 40.4406, -79.9959
R_MI = 3958.8

IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
       ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
       ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
       ("Pluto", swe.PLUTO), ("North Node", swe.TRUE_NODE), ("Chiron", swe.CHIRON)]
ID = dict(IDS)
BODIES = [n for n, _ in IDS]
P = {}
for nm, sid in IDS:
    P[nm] = swe.calc_ut(JD, sid, FL)[0][0]

FINALISTS = {
    "Florida / Carolinas": [
        ("Tampa FL", 27.951, -82.457), ("Sarasota FL", 27.337, -82.531),
        ("Orlando FL", 28.538, -81.379), ("Naples FL", 26.142, -81.795),
        ("Asheville NC", 35.595, -82.552), ("Greenville SC", 34.853, -82.394),
        ("Charleston SC", 32.777, -79.931), ("Savannah GA", 32.081, -81.091),
        ("Charleston WV", 38.350, -81.633)],
    "Mountain West": [
        ("Missoula MT", 46.872, -113.994), ("Helena MT", 46.589, -112.039),
        ("Bozeman MT", 45.680, -111.039), ("Billings MT", 45.783, -108.501),
        ("St. George UT", 37.096, -113.568), ("Las Vegas NV", 36.170, -115.140),
        ("Phoenix AZ", 33.448, -112.074), ("Prescott AZ", 34.540, -112.469),
        ("Sedona AZ", 34.870, -111.761), ("Flagstaff AZ", 35.198, -111.651),
        ("Tucson AZ", 32.222, -110.974), ("Salt Lake City UT", 40.761, -111.891),
        ("Durango CO", 37.275, -107.880), ("Grand Junction CO", 39.064, -108.551)],
    "Far West Coast": [
        ("Eureka CA", 40.802, -124.164), ("Redding CA", 40.587, -122.391),
        ("Chico CA", 39.729, -121.837), ("Medford OR", 42.327, -122.874),
        ("Eugene OR", 44.052, -123.087), ("Salem OR", 44.943, -123.035),
        ("Portland OR", 45.515, -122.678), ("San Francisco CA", 37.775, -122.419),
        ("Sacramento CA", 38.582, -121.494)],
}
ALL = [c for g in FINALISTS.values() for c in g]


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def sg(x):
    return S[int((x % 360) // 30)]


def fmt(x):
    i = int((x % 360) // 30)
    p = x % 360 - i * 30
    d = int(p)
    m = int(round((p - d) * 60))
    if m == 60:
        m, d = 0, d + 1
    return f"{d:2d}°{m:02d}' {S[i][:3]}"


def bearing(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    return math.degrees(math.atan2(
        math.sin(dl) * math.cos(p2),
        math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl))) % 360.0


def gc_dist(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    c = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl)
    return math.acos(max(-1.0, min(1.0, c))) * R_MI


def cross_track(lat, lon, az):
    """Perpendicular miles from the great circle leaving Pittsburgh on bearing az."""
    d13 = gc_dist(BLAT, BLON, lat, lon) / R_MI
    t13 = math.radians(bearing(BLAT, BLON, lat, lon))
    return abs(math.asin(math.sin(d13) * math.sin(t13 - math.radians(az))) * R_MI)


HR = "=" * 100


def stage5():
    print(HR)
    print("STAGE 5 — LOCAL SPACE, finalists only")
    print(HR)
    print("  Azimuths measured from the birth place, Pittsburgh PA, at birth.")
    print("  0 deg = due north, 90 = east, 180 = south, 270 = west.\n")
    az = {}
    for b in BODIES:
        a, alt, _ = swe.azalt(JD, swe.ECL2HOR, [BLON, BLAT, 300.0], 1013.25, 15.0,
                              [P[b], 0.0, 1.0])
        az[b] = (a + 180.0) % 360.0        # swisseph returns azimuth from south
        print(f"    {b:<12}azimuth {az[b]:6.2f}°   altitude {alt:+6.2f}°"
              f"   {'above' if alt > 0 else 'BELOW'} the horizon")
    print()
    print("  Cross-track distance = perpendicular miles from the great circle.")
    print("  Woods does not publish a local-space orb, so no cut-off is applied;")
    print("  the numbers are reported raw.")
    print("  BRANCH MATTERS: a local space line is a full great circle, so every")
    print("  planet has a FORWARD branch (the planet's own azimuth) and a")
    print("  RECIPROCAL branch 180 deg opposite. Practitioners differ on whether")
    print("  the reciprocal counts, and Woods' public material does not say.")
    print("  Marked fwd / REV below so the distinction is never hidden.\n")
    for grp, cities in FINALISTS.items():
        print(f"  ▸ {grp}")
        print(f"    {'city':<20}{'bearing':>9}{'dist mi':>9}   nearest local-space lines "
              f"(cross-track miles)")
        for nm, la, lo in cities:
            br = bearing(BLAT, BLON, la, lo)
            d = gc_dist(BLAT, BLON, la, lo)
            xs = []
            for b in BODIES:
                fwd = abs(n180(br - az[b]))
                rev = abs(n180(br - (az[b] + 180.0)))
                xs.append((cross_track(la, lo, az[b]), b,
                           "fwd" if fwd <= rev else "REV"))
            xs.sort()
            txt = ", ".join(f"{b} {x:.0f}({tag})" for x, b, tag in xs[:3])
            print(f"    {nm:<20}{br:8.1f}°{d:9.0f}   {txt}")
        print()


def prog_jd(year):
    """Secondary progressed JD: one day per year of life."""
    return JD + (year - 1996.4356)          # birth decimal year


def stage6():
    print("\n" + HR)
    print("STAGE 6 — TIMING, 2027 to 2030 (2028-2029 emphasised)")
    print(HR)
    print("  Techniques, each named as Woods names them:")
    print("    (a) transits to the RELOCATED angles  [location-specific]")
    print("    (b) secondary progressions            [she notes these last up to 3 yrs]")
    print("    (c) relocated solar returns")
    print("    (d) cyclocartography, i.e. where transiting planet lines fall")
    print("  This is 'when', kept strictly separate from 'where'.\n")

    print("  (a) TRANSITS TO RELOCATED ANGLES")
    print("      The relocated ASC and MC differ by city, so these dates are")
    print("      location-specific. Slow planets only; exact crossings listed.")
    print()
    SLOW = [("Jupiter", swe.JUPITER), ("Saturn", swe.SATURN),
            ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE), ("Pluto", swe.PLUTO)]
    # sample the two structural regimes plus the coast
    SAMPLE = [("Sarasota FL", 27.337, -82.531), ("Asheville NC", 35.595, -82.552),
              ("Tampa FL", 27.951, -82.457), ("Missoula MT", 46.872, -113.994),
              ("St. George UT", 37.096, -113.568), ("Tucson AZ", 32.222, -110.974),
              ("Eureka CA", 40.802, -124.164), ("Portland OR", 45.515, -122.678)]
    start = swe.julday(2027, 1, 1, 0.0, swe.GREG_CAL)
    end = swe.julday(2031, 1, 1, 0.0, swe.GREG_CAL)
    for nm, la, lo in SAMPLE:
        cusp, am = swe.houses(JD, la, lo, b"P")
        asc, mc = am[0], am[1]
        ang = {"ASC": asc, "MC": mc, "DSC": (asc + 180) % 360, "IC": (mc + 180) % 360}
        events = []
        for pn, pid in SLOW:
            for anm, av in ang.items():
                prev, t = None, start
                while t <= end:
                    cur = n180(swe.calc_ut(t, pid, FL)[0][0] - av)
                    if prev is not None and prev * cur < 0 and abs(prev - cur) < 30:
                        a2, b2 = t - 5, t
                        for _ in range(40):
                            m = (a2 + b2) / 2
                            fa = n180(swe.calc_ut(a2, pid, FL)[0][0] - av)
                            fm = n180(swe.calc_ut(m, pid, FL)[0][0] - av)
                            if fa * fm <= 0:
                                b2 = m
                            else:
                                a2 = m
                        y, mo, d, _ = swe.revjul((a2 + b2) / 2, swe.GREG_CAL)
                        events.append(((a2 + b2) / 2, f"{y}-{mo:02d}-{d:02d}",
                                       f"{pn} conjunct relocated {anm}"))
                    prev = cur
                    t += 5
        events.sort()
        print(f"    {nm}   ASC {fmt(asc)}  MC {fmt(mc)}")
        if events:
            for _, ds, txt in events:
                print(f"        {ds}   {txt}")
        else:
            print("        no slow-planet conjunction to any relocated angle in the window")
    print()

    print("  (b) SECONDARY PROGRESSIONS (one day = one year)")
    print(f"      {'year':<7}{'prog Sun':<15}{'prog Moon':<15}{'prog Venus':<15}"
          f"{'prog Mercury'}")
    for y in (2027, 2028, 2029, 2030):
        j = prog_jd(y)
        ps = swe.calc_ut(j, swe.SUN, FL)[0][0]
        pm = swe.calc_ut(j, swe.MOON, FL)[0][0]
        pv = swe.calc_ut(j, swe.VENUS, FL)[0]
        pme = swe.calc_ut(j, swe.MERCURY, FL)[0][0]
        print(f"      {y:<7}{fmt(ps):<15}{fmt(pm):<15}"
              f"{fmt(pv[0]) + (' Rx' if pv[3] < 0 else '   '):<15}{fmt(pme)}")
    print()
    print("      progressed contacts to the two regimes' angle ranges:")
    for y in (2027, 2028, 2029, 2030):
        j = prog_jd(y)
        hits = []
        for pn, pid in (("Sun", swe.SUN), ("Venus", swe.VENUS), ("Moon", swe.MOON),
                        ("Mercury", swe.MERCURY)):
            v = swe.calc_ut(j, pid, FL)[0][0]
            if sg(v) in ("Virgo", "Libra"):
                hits.append(f"progressed {pn} at {fmt(v)} is inside the US "
                            f"RISING range")
            if sg(v) in ("Gemini", "Cancer"):
                hits.append(f"progressed {pn} at {fmt(v)} is inside the US MC range")
        for h in hits:
            print(f"      {y}: {h}")
    print()

    print("  (c) RELOCATED SOLAR RETURNS")
    sun0 = P["Sun"]
    for y in (2027, 2028, 2029, 2030):
        lo_, hi_ = swe.julday(y, 6, 4, 0.0, swe.GREG_CAL), swe.julday(y, 6, 10, 0.0, swe.GREG_CAL)
        for _ in range(60):
            m = (lo_ + hi_) / 2
            if n180(swe.calc_ut(lo_, swe.SUN, FL)[0][0] - sun0) * \
               n180(swe.calc_ut(m, swe.SUN, FL)[0][0] - sun0) <= 0:
                hi_ = m
            else:
                lo_ = m
        srj = (lo_ + hi_) / 2
        yy, mo, dd, hh = swe.revjul(srj, swe.GREG_CAL)
        print(f"    SR {y}  exact {yy}-{mo:02d}-{dd:02d} {int(hh):02d}:{int(hh%1*60):02d} UT")
        print(f"      {'city':<20}{'SR ASC':<14}{'SR MC':<14}bodies within 3° of an SR angle")
        for nm, la, lo in SAMPLE:
            c2, a2 = swe.houses(srj, la, lo, b"P")
            sasc, smc = a2[0], a2[1]
            sang = {"ASC": sasc, "MC": smc, "DSC": (sasc + 180) % 360,
                    "IC": (smc + 180) % 360}
            hits = []
            for b, bid in IDS:
                tv = swe.calc_ut(srj, bid, FL)[0][0]
                k, o = min(((k, abs(n180(tv - v))) for k, v in sang.items()),
                           key=lambda t: t[1])
                if o <= 3.0:
                    hits.append(f"t.{b} {k} {o:.1f}°")
            print(f"      {nm:<20}{fmt(sasc):<14}{fmt(smc):<14}"
                  f"{', '.join(hits) or '-'}")
        print()

    print("  (d) CYCLOCARTOGRAPHY — where transiting slow-planet MC/IC lines fall")
    print("      at each solar return moment. These sweep the globe daily, so a")
    print("      line position is only meaningful for a stated instant.")
    for y in (2028, 2029):
        lo_, hi_ = swe.julday(y, 6, 4, 0.0, swe.GREG_CAL), swe.julday(y, 6, 10, 0.0, swe.GREG_CAL)
        for _ in range(60):
            m = (lo_ + hi_) / 2
            if n180(swe.calc_ut(lo_, swe.SUN, FL)[0][0] - sun0) * \
               n180(swe.calc_ut(m, swe.SUN, FL)[0][0] - sun0) <= 0:
                hi_ = m
            else:
                lo_ = m
        srj = (lo_ + hi_) / 2
        g = swe.sidtime(srj) * 15.0
        print(f"      at the {y} solar return instant:")
        for pn, pid in SLOW + [("Sun", swe.SUN), ("Venus", swe.VENUS)]:
            ra = swe.calc_ut(srj, pid, FL | swe.FLG_EQUATORIAL)[0][0]
            mcl = n180(ra - g)
            icl = n180(mcl + 180)
            tags = []
            if -125 <= mcl <= -66.9:
                tags.append(f"MC line {abs(mcl):.2f}W")
            if -125 <= icl <= -66.9:
                tags.append(f"IC line {abs(icl):.2f}W")
            if tags:
                print(f"        t.{pn:<9}{', '.join(tags)}  <-- crosses the US")


if __name__ == "__main__":
    stage5()
    stage6()
