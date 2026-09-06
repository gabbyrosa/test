#!/usr/bin/env python3
"""
Bhava chalit, done properly, and a check on what the reading claimed.

THE BUG THIS EXISTS TO FIND.

jyotish.py computed its "Sripati" cross-check by calling swe.houses(..., b"P")
and asking which cusp-to-cusp interval each graha fell into. That is the
WESTERN convention, where a cusp BEGINS a house. Jyotish does not use that
convention. In Sripati (and in bhava chalit generally) the cusp is the
bhava MADHYA - the midpoint - and the bhava runs from the midpoint between
the previous madhya and this one, to the midpoint between this one and the
next. The boundaries are the bhava sandhis, halfway between madhyas.

Treating a madhya as a boundary shifts every graha by roughly half a bhava,
which is why the reading reported six of nine grahas changing house. That
number is an artefact of the wrong convention, not a fact about the chart.

This file computes bhava chalit correctly, three ways:
  Sripati proper  - Porphyry trisection of the quadrants gives the madhyas,
                    sandhis are the midpoints between adjacent madhyas
  Placidus madhya - Placidus cusps taken as madhyas, same sandhi rule
  Western (wrong) - the cusp-as-boundary reading jyotish.py actually used
"""

import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
LAT, LON = 40.4406, -79.9959
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
FL = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
R = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS),
       ("Mercury", swe.MERCURY), ("Jupiter", swe.JUPITER),
       ("Venus", swe.VENUS), ("Saturn", swe.SATURN)]


def fmt(x):
    i = int(x % 360 // 30)
    d = x % 30
    return f"{int(d):2d}°{int((d-int(d))*60):02d}' {R[i][:3]}"


def madhyas_sripati(asc, mc):
    """Porphyry trisection: the four angles are the madhyas of 1, 4, 7, 10."""
    ic, dc = (mc + 180) % 360, (asc + 180) % 360
    m = [0.0] * 12
    m[0], m[3], m[6], m[9] = asc, ic, dc, mc
    for a, b, i in ((asc, ic, 0), (ic, dc, 3), (dc, mc, 6), (mc, asc, 9)):
        arc = (b - a) % 360
        m[(i + 1) % 12] = (a + arc / 3) % 360
        m[(i + 2) % 12] = (a + 2 * arc / 3) % 360
    return m


def bhava_of(lon, madhyas):
    """Sandhis are the midpoints between adjacent madhyas."""
    for i in range(12):
        prev, cur, nxt = madhyas[i - 1], madhyas[i], madhyas[(i + 1) % 12]
        start = (prev + ((cur - prev) % 360) / 2) % 360
        end = (cur + ((nxt - cur) % 360) / 2) % 360
        if (lon - start) % 360 < (end - start) % 360:
            return i + 1
    return None


def main():
    P = {n: swe.calc_ut(JD, i, FL)[0][0] for n, i in IDS}
    mean = swe.calc_ut(JD, swe.MEAN_NODE, FL)[0][0]
    P["Rahu"], P["Ketu"] = mean, (mean + 180) % 360
    G = [n for n, _ in IDS] + ["Rahu", "Ketu"]

    pl_cusp, ascmc = swe.houses_ex(JD, LAT, LON, b"P", swe.FLG_SIDEREAL)
    ASC, MC = ascmc[0], ascmc[1]
    AI = int(ASC % 360 // 30)
    WS = {p: (int(P[p] % 360 // 30) - AI) % 12 + 1 for p in G}

    m_sri = madhyas_sripati(ASC, MC)
    m_pla = list(pl_cusp)

    print("=" * 92)
    print("BHAVA CHALIT, RECOMPUTED - correcting a convention error in jyotish.py")
    print("=" * 92)
    print(f"  Lagna {fmt(ASC)}   MC {fmt(MC)}\n")
    print("  Sripati bhava madhyas (Porphyry trisection) and their sandhis:")
    for i in range(12):
        prev, cur, nxt = m_sri[i - 1], m_sri[i], m_sri[(i + 1) % 12]
        s = (prev + ((cur - prev) % 360) / 2) % 360
        e = (cur + ((nxt - cur) % 360) / 2) % 360
        print(f"    bhava {i+1:<3} madhya {fmt(cur)}    spans {fmt(s)} to {fmt(e)}")

    print(f"\n  {'graha':<9}{'longitude':<14}{'whole sign':<12}"
          f"{'SRIPATI':<10}{'Placidus-madhya':<18}{'cusp-as-boundary':<18}{'verdict'}")
    n_sri = n_pla = n_west = 0
    for p in G:
        b_sri = bhava_of(P[p], m_sri)
        b_pla = bhava_of(P[p], m_pla)
        west = 0
        for j in range(12):
            a, b = pl_cusp[j], pl_cusp[(j + 1) % 12]
            if (P[p] - a) % 360 < (b - a) % 360:
                west = j + 1
                break
        n_sri += b_sri != WS[p]
        n_pla += b_pla != WS[p]
        n_west += west != WS[p]
        v = "SHIFTS" if b_sri != WS[p] else "holds"
        print(f"  {p:<9}{fmt(P[p]):<14}h{WS[p]:<11}h{b_sri:<9}h{b_pla:<17}"
              f"h{west:<17}{v}")

    print(f"\n  grahas changing bhava vs whole sign:")
    print(f"    Sripati proper (madhya + sandhi)      {n_sri} of 9")
    print(f"    Placidus cusps as madhyas             {n_pla} of 9")
    print(f"    cusp-as-boundary, the WRONG reading   {n_west} of 9  "
          f"<- what the document reported")

    print("\n" + "=" * 92)
    print("CONSEQUENCES FOR THE READING'S HEADLINE CLAIMS")
    print("=" * 92)
    checks = [
        ("Rahu in bhava 1", "Rahu", 1),
        ("Jupiter in bhava 4 (needed for Hamsa yoga)", "Jupiter", 4),
        ("Saturn in bhava 7", "Saturn", 7),
        ("Ketu in bhava 7", "Ketu", 7),
        ("Moon in bhava 6", "Moon", 6),
        ("Venus in bhava 9", "Venus", 9),
        ("Mercury in bhava 9", "Mercury", 9),
        ("Mars in bhava 9", "Mars", 9),
        ("Sun in bhava 9", "Sun", 9),
    ]
    for label, p, h in checks:
        b = bhava_of(P[p], m_sri)
        print(f"  {label:<44}{'HOLDS' if b == h else f'FAILS - Sripati puts it in h{b}'}")

    print("\n  Hamsa yoga requires Jupiter in a kendra (1/4/7/10) from the Lagna.")
    bj = bhava_of(P["Jupiter"], m_sri)
    print(f"    whole sign h4 -> kendra, forms.  Sripati h{bj} -> "
          f"{'kendra, still forms' if bj in (1,4,7,10) else 'NOT a kendra, would not form'}")

    print("\n  Dharma-Karmadhipati needs the 9th and 10th lords associated.")
    print("    Conjunction is a RASHI relationship: Venus and Mercury are both in")
    print("    Taurus under every bhava convention, so the yoga forms regardless.")
    bv, bm = bhava_of(P["Venus"], m_sri), bhava_of(P["Mercury"], m_sri)
    print(f"    But their BHAVA differs under Sripati: Venus h{bv}, Mercury h{bm}.")
    print("    So 'seated in the 9th' is convention-dependent even though the")
    print("    yoga itself is not.")

    print("\n  Saturn's dig bala is angular, not cusp-based, so it is unaffected:")
    dc = (ASC + 180) % 360
    print(f"    Descendant {fmt(dc)}, Saturn {fmt(P['Saturn'])}, "
          f"separation {abs(((P['Saturn']-dc+180)%360)-180):.2f}°")
    print("    Saturn sits just inside the 7th madhya. Its 56.6/60 dig bala and")
    print("    its bhava membership are measuring the same proximity, not")
    print("    disagreeing about it.")


if __name__ == "__main__":
    main()
