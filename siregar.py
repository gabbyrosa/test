#!/usr/bin/env python3
"""
Relocation analysis after Moses Siregar's documented locational method.

CATEGORY A — verbatim from his published essay "A New Look at Locational
Astrology & Astro*Carto*Graphy" (astrologyforthesoul.com):

  "if forced to choose only one astro-locality tool, I would reluctantly give
   up everything else and focus on the natal and relocated charts in
   combination."
  "far too many astrocartographers put the cart before the horse, the map
   before the chart."
  "Look at the condition and position of the ruler of the ASC in the
   relocated chart."
  "4-6 degree range for a planet that we like fairly well; in other words,
   the planet should be between 4-6 degrees from an angle in the relocated
   chart."
  "200-350 miles is roughly the equivalent of a 4-6 degree range, and 350-500
   miles is roughly the equivalent of a 6-8 degree range."
  "For extra credit do the above in both tropical and sidereal astrology."
  "All of these things are very important" (of parans, in mundo, C*C*G, local
   space, geodetics) "But I've found that the relocated chart itself is an
   incredibly important tool."

  Consequence that drives this file: proximity to a line is NOT the target.
  The target band is 4-6 degrees OFF the angle, roughly 200-350 miles from
  the line. This inverts the usual distance logic and therefore generates
  entirely different geography.

CATEGORY B — consistent with his philosophy, not separately documented:
  computing both whole-sign and Placidus because he acknowledges a planet
  "may reside in more than one house natally when we consider multiple house
  systems" but names no preferred system; using Lahiri ayanamsa for the
  sidereal pass, which is the Vedic standard he works in.

CATEGORY C — my own additions: none used for weighting or ranking. No score
  is computed anywhere in this file.

CAVEAT ON THE SOURCE: his consultation page states he no longer uses the
method described in the latter section of that essay, without saying on any
public page which section that is. Flagged, not resolved.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH | swe.FLG_SPEED
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
BLAT, BLON = 40.4406, -79.9959

IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
       ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
       ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
       ("Pluto", swe.PLUTO), ("North Node", swe.TRUE_NODE), ("Chiron", swe.CHIRON),
       ("Ceres", swe.CERES)]
BODIES = [n for n, _ in IDS]
TRAD = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
DOM = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
       "Pisces": "Jupiter"}
EXALT = {"Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo", "Venus": "Pisces",
         "Mars": "Capricorn", "Jupiter": "Cancer", "Saturn": "Libra"}
ELEM = {"Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
        "Taurus": "earth", "Virgo": "earth", "Capricorn": "earth",
        "Gemini": "air", "Libra": "air", "Aquarius": "air",
        "Cancer": "water", "Scorpio": "water", "Pisces": "water"}
TRIP = {"fire": ("Sun", "Jupiter", "Saturn"), "earth": ("Venus", "Moon", "Mars"),
        "air": ("Saturn", "Mercury", "Jupiter"), "water": ("Venus", "Mars", "Moon")}

swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
AYAN = swe.get_ayanamsa_ut(JD)

TROP, SID = {}, {}
RA, DEC = {}, {}
for nm, sid in IDS:
    x = swe.calc_ut(JD, sid, FL)[0]
    TROP[nm] = x[0]
    SID[nm] = (x[0] - AYAN) % 360.0
    y = swe.calc_ut(JD, sid, FL | swe.FLG_EQUATORIAL)[0]
    RA[nm], DEC[nm] = y[0], y[1]
SPD = {nm: swe.calc_ut(JD, sid, FL)[0][3] for nm, sid in IDS}
GMST = swe.sidtime(JD) * 15.0


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


def dignity(pl, P, day=True):
    s = sg(P[pl])
    out = []
    if DOM[s] == pl:
        out.append("domicile")
    if EXALT.get(pl) == s:
        out.append("exaltation")
    if DOM[S[(S.index(s) + 6) % 12]] == pl:
        out.append("DETRIMENT")
    if pl in EXALT and S[(S.index(EXALT[pl]) + 6) % 12] == s:
        out.append("FALL")
    d, n, part = TRIP[ELEM[s]]
    if pl == (d if day else n):
        out.append("triplicity")
    elif pl == part:
        out.append("triplicity (part.)")
    return out


def ws(P, asc):
    i = S.index(sg(asc))
    return {b: ((S.index(sg(P[b])) - i) % 12) + 1 for b in BODIES}, i


def rulers_of(asc):
    i = S.index(sg(asc))
    r = {}
    for h in range(1, 13):
        r.setdefault(DOM[S[(i + h - 1) % 12]], []).append(h)
    return r, {h: DOM[S[(i + h - 1) % 12]] for h in range(1, 13)}


HR = "=" * 100


def stage1():
    print(HR)
    print("STAGE 1 — NATAL CHART AS FOUNDATION, tropical AND sidereal")
    print(HR)
    print(f"  Lahiri ayanamsa at birth: {AYAN:.4f}°")
    cusp, am = swe.houses(JD, BLAT, BLON, b"P")
    asc, mc = am[0], am[1]
    sasc, smc = (asc - AYAN) % 360, (mc - AYAN) % 360
    print(f"  TROPICAL   ASC {fmt(asc)}   MC {fmt(mc)}   "
          f"IC {fmt((mc+180)%360)}   DSC {fmt((asc+180)%360)}")
    print(f"  SIDEREAL   ASC {fmt(sasc)}   MC {fmt(smc)}   "
          f"IC {fmt((smc+180)%360)}   DSC {fmt((sasc+180)%360)}")
    print(f"  Ascendant ruler   tropical: {DOM[sg(asc)]}    "
          f"sidereal: {DOM[sg(sasc)]}")
    print("  -> the two zodiacs do NOT agree on the chart ruler. Siregar says to")
    print("     run both, so this disagreement is a finding, not a problem.\n")

    for lbl, P, a in (("TROPICAL", TROP, asc), ("SIDEREAL (Lahiri)", SID, sasc)):
        w, ai = ws(P, a)
        rl, hr_ = rulers_of(a)
        print(f"  ▸ {lbl}   {sg(a)} rising, ruler {DOM[sg(a)]}")
        print(f"    {'body':<12}{'position':<15}{'WS h':<6}{'rules WS':<12}"
              f"{'dignity':<22}speed")
        for b in BODIES:
            dg = dignity(b, P) if b in TRAD else []
            print(f"    {b:<12}{fmt(P[b]):<15}{w[b]:<6}"
                  f"{','.join(map(str, rl.get(b, []))) or '-':<12}"
                  f"{', '.join(dg) if dg else ('peregrine' if b in TRAD else '-'):<22}"
                  f"{'Rx' if SPD[b] < 0 else ''}")
        print(f"    house rulers: " + ", ".join(f"{h}={hr_[h]}" for h in range(1, 13)))
        # dispositor chains
        chains = []
        for b in TRAD:
            c, cur, g = [b], b, 0
            while g < 12:
                nx = DOM[sg(P[cur])]
                if nx == cur:
                    c.append("(own sign)")
                    break
                if nx in c:
                    c.append(f"{nx} [loop]")
                    break
                c.append(nx)
                cur, g = nx, g + 1
            chains.append(f"{b}->" + "->".join(c[1:]))
        print("    dispositors: " + " | ".join(chains))
        recs = [f"{a2}/{b2}" for i2, a2 in enumerate(TRAD) for b2 in TRAD[i2+1:]
                if DOM[sg(P[a2])] == b2 and DOM[sg(P[b2])] == a2]
        print(f"    mutual receptions by domicile: {', '.join(recs) or 'none'}")
        print()

    print("  major aspects (Ptolemaic, same in both zodiacs since both shift equally)")
    for i in range(len(TRAD)):
        for j in range(i + 1, len(TRAD)):
            a2, b2 = TRAD[i], TRAD[j]
            sep = abs(n180(TROP[a2] - TROP[b2]))
            for nm, deg in (("conjunction", 0), ("sextile", 60), ("square", 90),
                            ("trine", 120), ("opposition", 180)):
                orb = 10 if "Sun" in (a2, b2) or "Moon" in (a2, b2) else 8
                if abs(sep - deg) <= orb:
                    print(f"    {a2:<8}{nm:<12}{b2:<9}orb {abs(sep-deg):.2f}°")
                    break
    print()


def stage2():
    print(HR)
    print("STAGE 2 — WHAT RELOCATION CAN CHANGE ACROSS THE CONTIGUOUS US")
    print(HR)
    print("  Geography searched before any city is named. The question Siregar")
    print("  puts first is the ruler of the relocated Ascendant, so that is the")
    print("  first thing mapped.\n")

    def asc_at(la, lo):
        return swe.houses(JD, la, lo, b"P")[1][0]

    # rising-sign census in both zodiacs
    for lbl, off in (("TROPICAL", 0.0), ("SIDEREAL (Lahiri)", AYAN)):
        seen = {}
        la = 24.5
        while la <= 49.5:
            lo = -125.0
            while lo <= -66.5:
                a = (asc_at(la, lo) - off) % 360.0
                seen.setdefault(sg(a), [0, 999, -1])
                r = seen[sg(a)]
                r[0] += 1
                r[1] = min(r[1], a % 30)
                r[2] = max(r[2], a % 30)
                lo += 0.5
            la += 0.5
        print(f"  ▸ {lbl}: rising signs available in the contiguous US")
        for s, (n, mn, mx) in sorted(seen.items(), key=lambda t: -t[1][0]):
            print(f"      {s:<10}ruler {DOM[s]:<9}{n:>6} pts   "
                  f"spans {mn:5.2f}°..{mx:5.2f}° of the sign")
        print()

    # boundary meridians
    def solve(target_abs, la):
        def f(lo):
            return n180(asc_at(la, lo) - target_abs)
        best, bo, x = None, 9e9, -180.0
        while x < 180.0:
            v = abs(f(x))
            if v < bo:
                bo, best = v, x
            x += 0.25
        a, b = best - 0.6, best + 0.6
        for _ in range(60):
            m = (a + b) / 2
            if f(a) * f(m) <= 0:
                b = m
            else:
                a = m
        return (a + b) / 2

    print("  ▸ ASCENDANT-RULER BOUNDARY MERIDIANS")
    print("    tropical: one boundary. sidereal: two. They fall at different")
    print("    longitudes, so the two zodiacs partition the country differently.")
    for lbl, off, bounds in (
            ("TROPICAL Virgo|Libra  (Mercury | Venus)", 0.0, [180.0]),
            ("SIDEREAL Leo|Virgo    (Sun | Mercury)", AYAN, [150.0]),
            ("SIDEREAL Virgo|Libra  (Mercury | Venus)", AYAN, [180.0])):
        for b in bounds:
            row = []
            for la in (25.0, 32.0, 39.0, 46.0, 49.0):
                row.append(f"{la:.0f}N {abs(solve((b + off) % 360.0, la)):.3f}W")
            print(f"    {lbl:<40}" + "  ".join(row))
    print()

    print("  ▸ MC / IC SIGN REGIMES")
    for lbl, off in (("TROPICAL", 0.0), ("SIDEREAL", AYAN)):
        seen = {}
        la = 24.5
        while la <= 49.5:
            lo = -125.0
            while lo <= -66.5:
                m = (swe.houses(JD, la, lo, b"P")[1][1] - off) % 360.0
                seen.setdefault((sg(m), sg((m + 180) % 360)), 0)
                seen[(sg(m), sg((m + 180) % 360))] += 1
                lo += 0.5
            la += 0.5
        print(f"    {lbl}: " + " | ".join(
            f"MC {a} (ruler {DOM[a]}) / IC {b} (ruler {DOM[b]})"
            for (a, b), n in sorted(seen.items(), key=lambda t: -t[1])))
    print()


def stage3():
    print(HR)
    print("STAGE 3 — THE RELOCATED-CHART REGIMES, and the 4-6 DEGREE BANDS")
    print(HR)
    print("  Siregar's target is NOT the line. It is 4-6 degrees off an angle,")
    print("  which he equates to roughly 200-350 miles from the line, and 6-8")
    print("  degrees to 350-500 miles. So the geography below is a set of")
    print("  CORRIDORS FLANKING each line, not the lines themselves.\n")

    print("  ▸ WHERE EACH BODY SITS 4-6 DEGREES FROM A MERIDIAN ANGLE")
    print("    (a meridian line is a longitude; the 4-6 deg band is two strips,")
    print("     one either side of it)")
    print(f"    {'body':<12}{'angle':<6}{'line':<11}{'west band':<22}"
          f"{'east band':<22}in US?")
    for b in BODIES:
        for k, off in (("MC", 0.0), ("IC", 180.0)):
            L = n180(RA[b] - GMST + off)
            w1, w2 = n180(L - 6.0), n180(L - 4.0)
            e1, e2 = n180(L + 4.0), n180(L + 6.0)
            hits = []
            for tag, a, bb in (("W", w1, w2), ("E", e1, e2)):
                if -125 <= (a + bb) / 2 <= -66.9:
                    hits.append(tag)
            if -125 <= L <= -66.9 or hits:
                print(f"    {b:<12}{k:<6}{abs(L):>7.2f}W   "
                      f"{abs(w1):6.2f}W..{abs(w2):6.2f}W    "
                      f"{abs(e1):6.2f}W..{abs(e2):6.2f}W    "
                      f"{','.join(hits) or 'line only'}")
    print()

    print("  ▸ THE RELOCATED ASCENDANT RULER, mapped (Siregar's first question)")
    print("    For each regime: who rules the relocated ASC, where that ruler")
    print("    sits by whole sign AND Placidus, and its natal condition.")
    print()
    PROBE = [(-122.0, "Pacific coast"), (-117.0, "inland SoCal / NV"),
             (-112.0, "AZ / UT"), (-107.0, "NM / CO"), (-102.0, "high plains"),
             (-97.0, "central TX / OK / KS"), (-92.0, "Mississippi valley"),
             (-87.0, "IL / TN / AL"), (-82.0, "OH / FL / Appalachia"),
             (-77.0, "mid-Atlantic"), (-71.0, "New England")]
    for lbl, off in (("TROPICAL", 0.0), ("SIDEREAL (Lahiri)", AYAN)):
        P = TROP if off == 0.0 else SID
        print(f"    ▸ {lbl}")
        print(f"      {'meridian':<26}{'ASC':<14}{'ruler':<9}"
              f"{'WS h':<6}{'Plac h':<8}{'ruler condition'}")
        seenkey = set()
        for lo, name in PROBE:
            cusp, am = swe.houses(JD, 37.0, lo, b"P")
            a = (am[0] - off) % 360.0
            r = DOM[sg(a)]
            w, ai = ws(P, a)
            cs = [(c - off) % 360.0 for c in cusp]
            pv = P[r] % 360.0
            ph = 12
            for i in range(12):
                x, y = cs[i], cs[(i + 1) % 12]
                if (x < y and x <= pv < y) or (x > y and (pv >= x or pv < y)):
                    ph = i + 1
                    break
            dg = dignity(r, P)
            print(f"      {name:<26}{fmt(a):<14}{r:<9}{w[r]:<6}{ph:<8}"
                  f"{', '.join(dg) if dg else 'peregrine'}")
        print()


if __name__ == "__main__":
    stage1()
    stage2()
    stage3()
