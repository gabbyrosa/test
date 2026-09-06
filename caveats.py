#!/usr/bin/env python3
"""
Stress-tests on two claims from the chart-intrinsic pass.

CLAIM 1  "No US location angularizes Mars."
         True only for the four principal angles by degree. This file also
         computes Mars's Ascendant and Descendant curves, and every paran
         latitude Mars forms with another body, because parans are horizontal
         bands that apply at ALL longitudes. If Mars parans fall inside
         25-49N, the original sentence was too broad.

CLAIM 2  The Lot of Spirit boundary near 110W.
         The Lots are rigid offsets from the Ascendant, so a birth-time error
         displaces them exactly as much as it displaces the Ascendant. This
         file quantifies that in miles of longitude, which is the honest test
         of whether the boundary can carry the interpretive weight it was
         given.

Lot conventions used, stated explicitly:
    DAY chart (verified: Sun above the horizon).
    Fortune = ASC + Moon - Sun
    Spirit  = ASC + Sun  - Moon
    Sect-sensitive: these reverse in a night chart. Hers is a day chart, so
    the day forms above are the correct ones.
    Planetary longitudes are NATAL and never change. Only the Ascendant is
    recomputed for the new location, which is the sole reason the Lots move.
"""

import math
import swisseph as swe

import natal

swe.set_ephe_path("/usr/share/swisseph")
S = natal.SIGNS
FL = swe.FLG_SWIEPH
SWE_ID = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
          "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
          "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE,
          "Pluto": swe.PLUTO, "North Node": swe.TRUE_NODE, "Chiron": swe.CHIRON}
D = natal.compute()
JD = D["jd"]
P = {n: D["planets"][n]["lon"] for n in D["planets"]}
GMST = swe.sidtime(JD) * 15.0


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def n360(x):
    return x % 360.0


def sg(x):
    return S[int((x % 360) // 30)]


def eq(pl):
    xx, _ = swe.calc_ut(JD, SWE_ID[pl], FL | swe.FLG_EQUATORIAL)
    return xx[0], xx[1]


def lst_on_angle(pl, angle, lat):
    """Local sidereal time (deg) at which a body sits on a given angle."""
    ra, dec = eq(pl)
    if angle == "MC":
        return n360(ra)
    if angle == "IC":
        return n360(ra + 180.0)
    x = -math.tan(math.radians(lat)) * math.tan(math.radians(dec))
    if abs(x) > 1.0:
        return None                       # circumpolar at this latitude
    h0 = math.degrees(math.acos(x))
    return n360(ra - h0) if angle == "ASC" else n360(ra + h0)


HR = "=" * 96


def main():
    print(HR)
    print("CLAIM 1 — how far does 'no US location angularizes Mars' actually go?")
    print(HR)
    ra, dec = eq("Mars")
    print(f"  Mars {natal.fmt(P['Mars'])}   RA {ra:.3f}°   dec {dec:+.3f}°"
          f"   ecliptic latitude {swe.calc_ut(JD, swe.MARS, FL)[0][1]:+.3f}°")
    print(f"  MC line {abs(n180(ra - GMST)):.3f}W    "
          f"IC line {abs(n180(ra + 180 - GMST)):.3f}"
          f"{'W' if n180(ra+180-GMST) < 0 else 'E'}")
    print("\n  Mars ASC and DSC curves, by latitude:")
    print(f"    {'lat':<7}{'rises at':<14}{'sets at':<14}in the contiguous US?")
    for la in (25, 30, 35, 40, 45, 49):
        a = lst_on_angle("Mars", "ASC", la)
        d = lst_on_angle("Mars", "DSC", la)
        la_, ld_ = n180(a - GMST), n180(d - GMST)
        inus = [nm for nm, v in (("ASC", la_), ("DSC", ld_)) if -125 <= v <= -66.9]
        print(f"    {la:<7}{la_:>8.2f}      {ld_:>8.2f}      "
              f"{', '.join(inus) if inus else 'neither'}")

    print("\n  Mars PARAN latitudes (a paran is a horizontal band, so it applies")
    print("  at every longitude at that latitude):")
    ANG = ("ASC", "MC", "DSC", "IC")
    found = []
    for other in [b for b in SWE_ID if b != "Mars"]:
        for a1 in ANG:
            for a2 in ANG:
                lo, hi = 0.5, 66.0
                def f(la):
                    x, y = lst_on_angle("Mars", a1, la), lst_on_angle(other, a2, la)
                    return None if x is None or y is None else n180(x - y)
                prev = f(lo)
                la = lo + 0.05
                while la <= hi:
                    cur = f(la)
                    if prev is not None and cur is not None and \
                       prev * cur < 0 and abs(prev - cur) < 90:
                        a, b = la - 0.05, la
                        for _ in range(50):
                            m = (a + b) / 2
                            if f(a) * f(m) <= 0:
                                b = m
                            else:
                                a = m
                        found.append(((a + b) / 2, other, a1, a2))
                    prev = cur
                    la += 0.05
    us = sorted(x for x in found if 24.5 <= x[0] <= 49.5)
    if us:
        print(f"    {len(us)} Mars parans fall inside US latitudes:")
        for la, other, a1, a2 in us:
            print(f"      {la:5.2f}N   Mars {a1:<4} with {other} {a2}")
    else:
        print("    none inside 24.5-49.5N")
    print(f"    ({len(found)} Mars parans exist worldwide; "
          f"{len(found) - len(us)} fall outside US latitudes)")
    print()
    print("  CORRECTED STATEMENT:")
    print("  No contiguous-US location places Mars on a principal angle by")
    print("  degree. That is a statement about the four angles only. Mars keeps")
    print("  its whole-sign house, its rulerships, its conjunction with Mercury,")
    print("  and any paran bands listed above, everywhere in the country.")

    # ---------------------------------------------------------------- CLAIM 2
    print("\n" + HR)
    print("CLAIM 2 — how much birth-time error does the Spirit boundary survive?")
    print(HR)
    SP = (P["Sun"] - P["Moon"]) % 360.0
    bdy = (30.0 - SP % 30.0) % 30.0
    print(f"  Spirit sits {SP:.2f}° ahead of the Ascendant, so it leaves the")
    print(f"  angular 4th when the Ascendant passes {bdy:.2f}° of its sign.")
    print(f"  Recorded birth time 15:35 EDT. Testing +/- 8 minutes.\n")

    def boundary(dt_min, lat, target_sign="Virgo"):
        jd = swe.julday(1996, 6, 7, 15 + (35 + dt_min) / 60.0 + 4.0, swe.GREG_CAL)
        pl = {n: swe.calc_ut(jd, SWE_ID[n], FL)[0][0] for n in ("Sun", "Moon")}
        off = (pl["Sun"] - pl["Moon"]) % 360.0
        b = (30.0 - off % 30.0) % 30.0
        tgt = S.index(target_sign) * 30 + b

        def asc(lon):
            return swe.houses(jd, lat, lon, b"P")[1][0]
        best, bo, x = None, 9e9, -180.0
        while x < 180.0:
            v = abs(n180(asc(x) - tgt))
            if v < bo:
                bo, best = v, x
            x += 0.25
        a, b2 = best - 0.6, best + 0.6
        for _ in range(60):
            m = (a + b2) / 2
            if n180(asc(a) - tgt) * n180(asc(m) - tgt) <= 0:
                b2 = m
            else:
                a = m
        return (a + b2) / 2

    lat = 35.0
    base = boundary(0, lat)
    print(f"  {'birth time':<14}{'boundary at 35N':<20}{'shift from recorded'}")
    for dt in (-8, -4, -2, 0, +2, +4, +8):
        b = boundary(dt, lat)
        dl = b - base
        mi = abs(dl) * 111.32 * math.cos(math.radians(lat)) * 0.6214
        hh, mm = divmod(35 + dt, 60)
        print(f"  {'15:%02d' % (35+dt) if 0 <= 35+dt < 60 else '15:%02d' % (35+dt):<14}"
              f"{abs(b):>9.3f}W          {dl:+7.3f}°  = {mi:5.0f} miles")
    b8, bm8 = boundary(8, lat), boundary(-8, lat)
    span = abs(b8 - bm8) * 111.32 * math.cos(math.radians(lat)) * 0.6214
    print(f"\n  A 16-minute window of birth-time uncertainty moves the boundary")
    print(f"  {span:.0f} miles. Tucson sits {abs(-110.974 - base)*111.32*math.cos(math.radians(32.2))*0.6214:.0f}"
          f" miles west of the nominal boundary, so its Spirit result is")
    print(f"  {'ROBUST' if abs(-110.974-base)*111.32*math.cos(math.radians(32.2))*0.6214 > span/2 else 'NOT ROBUST'}"
          f" to that uncertainty; places nearer the line are not.")
    print()
    print("  Same test for the Venus MC line, which sits at 109.132W:")
    d_venus = abs(-109.132 - base) * 111.32 * math.cos(math.radians(35.0)) * 0.6214
    print(f"    {d_venus:.0f} miles east of the nominal boundary "
          f"({'outside' if d_venus > span/2 else 'INSIDE'} the birth-time "
          f"uncertainty band)")


if __name__ == "__main__":
    main()
