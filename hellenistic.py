#!/usr/bin/env python3
"""
Both charts under one declared framework: strictly Hellenistic.

WHAT THIS DROPS, relative to the earlier readings, and why:
  almuten figuris        Ibn Ezra / Lilly. Medieval-Renaissance, not Hellenistic.
  moiety orbs            Lilly. Hellenistic aspect doctrine is sign-based.
  semi-sextile, quincunx NOT aspects. Signs 1 and 5 apart are in AVERSION.
  Node interpretation    the "growth axis" reading is 20th-century.

WHAT IT ADDS, being Hellenistic material the earlier readings omitted:
  whole-sign aspect matrix with aversion marked explicitly
  advantageous vs inoperative places (the houses in aversion to the Ascendant)
  overcoming, co-presence, enclosure
  bonification and maltreatment verdicts per planet
  the angular triads
  Lots with their rulers, triplicity lords of the sect light, solar phases,
  planetary joys

ZODIAC NOTE, computed below: in the Hellenistic period the tropical and
sidereal zodiacs nearly coincided, so the corpus cannot adjudicate between
them. Ptolemy argues for tropical; the tradition he inherited was Babylonian
and sidereal-derived. Choosing Hellenistic technique does not settle the
zodiac. Both are therefore run here.
"""

import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH | swe.FLG_SPEED
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
AY = swe.get_ayanamsa_ut(JD)
IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
       ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
       ("Saturn", swe.SATURN)]
T7 = [n for n, _ in IDS]
DOM = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
       "Pisces": "Jupiter"}
EX = {"Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo", "Venus": "Pisces",
      "Mars": "Capricorn", "Jupiter": "Cancer", "Saturn": "Libra"}
ELEM = {"Aries": "fire", "Leo": "fire", "Sagittarius": "fire",
        "Taurus": "earth", "Virgo": "earth", "Capricorn": "earth",
        "Gemini": "air", "Libra": "air", "Aquarius": "air",
        "Cancer": "water", "Scorpio": "water", "Pisces": "water"}
TRIP = {"fire": ("Sun", "Jupiter", "Saturn"), "earth": ("Venus", "Moon", "Mars"),
        "air": ("Saturn", "Mercury", "Jupiter"), "water": ("Venus", "Mars", "Moon")}
JOY = {"Mercury": 1, "Moon": 3, "Venus": 5, "Mars": 6, "Sun": 9, "Jupiter": 11,
       "Saturn": 12}
BENEFIC, MALEFIC = ("Venus", "Jupiter"), ("Mars", "Saturn")
ADVANTAGEOUS = {1, 3, 4, 5, 7, 9, 10, 11}   # the places that aspect the 1st
ASPNAME = {0: "co-present", 2: "sextile", 3: "square", 4: "trine", 6: "opposition",
           8: "trine", 9: "square", 10: "sextile"}


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


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def analyse(label, P, ASC, day=True):
    AI = S.index(sg(ASC))
    H = {b: ((S.index(sg(P[b])) - AI) % 12) + 1 for b in T7}
    print("=" * 96)
    print(f"{label}")
    print("=" * 96)
    print(f"  ASC {fmt(ASC)}   sect: {'DAY' if day else 'NIGHT'}   "
          f"lord of the Ascendant: {DOM[sg(ASC)]} (h{H[DOM[sg(ASC)]]})")
    print(f"  sect light {'Sun' if day else 'Moon'}   "
          f"benefic of sect {'Jupiter' if day else 'Venus'}   "
          f"malefic of sect {'Saturn' if day else 'Mars'}   "
          f"contrary-to-sect malefic {'Mars' if day else 'Saturn'}\n")

    print("  PLACES — Hellenistic doctrine: houses 2, 6, 8 and 12 are in aversion")
    print("  to the Ascendant and are the inoperative or 'dark' places.")
    for b in T7:
        s = sg(P[b])
        dg = []
        if DOM[s] == b:
            dg.append("domicile")
        if EX.get(b) == s:
            dg.append("exaltation")
        if DOM[S[(S.index(s) + 6) % 12]] == b:
            dg.append("DETRIMENT")
        if b in EX and S[(S.index(EX[b]) + 6) % 12] == s:
            dg.append("FALL")
        d, n, pt = TRIP[ELEM[s]]
        if b == (d if day else n):
            dg.append("trigon lord")
        elif b == pt:
            dg.append("trigon (partic.)")
        sep = abs(n180(P[b] - P["Sun"]))
        ph = "" if b == "Sun" else (
            "CAZIMI" if sep <= 0.283 else "combust" if sep <= 8 else
            "under the beams" if sep <= 15 else "free of the beams")
        if b != "Sun" and ph != "free of the beams":
            ph += f" {sep:.2f}°"
        piv = ("PIVOT" if H[b] in (1, 4, 7, 10) else
               "succedent" if H[b] in (2, 5, 8, 11) else "declining")
        print(f"    {b:<9}{fmt(P[b]):<13}h{H[b]:<3}"
              f"{'ADVANTAGEOUS' if H[b] in ADVANTAGEOUS else 'DARK PLACE':<14}"
              f"{piv:<11}{', '.join(dg) if dg else 'peregrine':<24}"
              f"{'★joy  ' if JOY.get(b) == H[b] else ''}{ph}")

    print("\n  WHOLE-SIGN ASPECT MATRIX  (- = aversion, no relationship)")
    print("           " + "".join(f"{b[:3]:>12}" for b in T7))
    for a in T7:
        row = ""
        for b in T7:
            if a == b:
                row += f"{'.':>12}"
                continue
            d = (S.index(sg(P[b])) - S.index(sg(P[a]))) % 12
            nm = ASPNAME.get(d)
            if nm is None:
                row += f"{'—':>12}"
            else:
                exact = abs(abs(n180(P[a] - P[b])) - {0: 0, 2: 60, 3: 90, 4: 120,
                                                      6: 180, 8: 120, 9: 90,
                                                      10: 60}[d])
                row += f"{nm[:4] + f'{exact:.0f}':>12}"
        print(f"    {a[:8]:<7}" + row)

    print("\n  OVERCOMING  (a planet in the 10th sign from another dominates it)")
    ov = []
    for a in T7:
        for b in T7:
            if a == b:
                continue
            if (S.index(sg(P[b])) - S.index(sg(P[a]))) % 12 == 9:
                ov.append(f"{a} overcomes {b}")
    print("    " + ("; ".join(ov) if ov else "no overcoming configurations"))

    print("\n  CO-PRESENCE and ENCLOSURE")
    for a in T7:
        co = [b for b in T7 if b != a and sg(P[b]) == sg(P[a])]
        if co:
            print(f"    {a} co-present with {', '.join(co)}")
    for b in T7:
        if b in MALEFIC:
            continue
        ahead = min(((P[m] - P[b]) % 360, m) for m in MALEFIC)
        behind = min(((P[b] - P[m]) % 360, m) for m in MALEFIC)
        if ahead[0] <= 30 and behind[0] <= 30:
            print(f"    {b} ENCLOSED by {behind[1]} ({behind[0]:.1f}° behind) "
                  f"and {ahead[1]} ({ahead[0]:.1f}° ahead)")

    print("\n  BONIFICATION / MALTREATMENT")
    for b in T7:
        if b in BENEFIC or b in MALEFIC:
            pass
        good, bad = [], []
        for o in BENEFIC:
            if o == b:
                continue
            d = (S.index(sg(P[o])) - S.index(sg(P[b]))) % 12
            if d == 0:
                good.append(f"{o} co-present")
            elif d in (4, 8):
                good.append(f"{o} trine")
            elif d in (2, 10):
                good.append(f"{o} sextile")
        for o in MALEFIC:
            if o == b:
                continue
            d = (S.index(sg(P[o])) - S.index(sg(P[b]))) % 12
            if d == 0:
                bad.append(f"{o} co-present")
            elif d in (3, 9):
                bad.append(f"{o} square" + (" (overcoming)" if d == 9 else ""))
            elif d == 6:
                bad.append(f"{o} opposition")
        print(f"    {b:<9}bonified by: {', '.join(good) or 'nothing':<34}"
              f"maltreated by: {', '.join(bad) or 'nothing'}")

    F = (ASC + P["Moon"] - P["Sun"]) % 360 if day else (ASC + P["Sun"] - P["Moon"]) % 360
    Sp = (ASC + P["Sun"] - P["Moon"]) % 360 if day else (ASC + P["Moon"] - P["Sun"]) % 360
    print("\n  LOTS")
    for nm, v in (("Fortune", F), ("Spirit", Sp)):
        h = ((S.index(sg(v)) - AI) % 12) + 1
        r = DOM[sg(v)]
        print(f"    {nm:<9}{fmt(v):<13}h{h:<3}"
              f"{'ADVANTAGEOUS' if h in ADVANTAGEOUS else 'DARK PLACE':<14}"
              f"lord {r} in h{H[r]}")

    e = ELEM[sg(P["Sun" if day else "Moon"])]
    d, n, pt = TRIP[e]
    print(f"\n  TRIGON LORDS OF THE SECT LIGHT ({'Sun' if day else 'Moon'} in "
          f"{sg(P['Sun' if day else 'Moon'])}, {e})")
    for lab, r in (("first", d), ("second", n), ("participating", pt)):
        print(f"    {lab:<14}{r:<9}{fmt(P[r]):<13}h{H[r]:<3}"
              f"{'ADVANTAGEOUS' if H[r] in ADVANTAGEOUS else 'DARK PLACE'}")
    print()


def main():
    print("ZODIAC NOTE — can the Hellenistic corpus settle the zodiac question?")
    for yr in (100, 150, 200, 285):
        j = swe.julday(yr, 6, 1, 12.0, swe.GREG_CAL)
        v = swe.get_ayanamsa_ut(j)
        print(f"    ayanamsa in {yr} CE: {((v + 180) % 360) - 180:+.2f}°")
    print("  The two zodiacs were within a couple of degrees through the whole")
    print("  Hellenistic period. The corpus did not have to choose, so it cannot")
    print("  settle the question for us. Ptolemy argues tropical; the Babylonian")
    print("  material he inherited was sidereal-derived. Both are run below.\n")

    P = {n: swe.calc_ut(JD, s, FL)[0][0] for n, s in IDS}
    cusp, am = swe.houses(JD, 40.4406, -79.9959, b"P")
    analyse("TROPICAL — Hellenistic technique", P, am[0])
    analyse("SIDEREAL (Lahiri) — Hellenistic technique, an acknowledged hybrid",
            {n: (v - AY) % 360 for n, v in P.items()}, (am[0] - AY) % 360)


if __name__ == "__main__":
    main()
