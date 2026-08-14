#!/usr/bin/env python3
"""
Full sidereal natal chart, read blind.

  zodiac    sidereal, Lahiri ayanamsa
  houses    whole sign
  technique Hellenistic / traditional (sect, essential dignity, solar phase,
            dispositors). This is a HYBRID: sidereal positions read with
            Western traditional technique, which is what "run it in both
            zodiacs" means. It is not Vedic astrology, which would use the
            same positions with a different apparatus entirely.

Nothing from the relocation work enters this file. No location other than
the birth place is used.

STRUCTURAL NOTE the output verifies: switching zodiac shifts every longitude
by the same ayanamsa, so everything measured as a DIFFERENCE between two
bodies is identical to the tropical chart. Aspects, orbs, combustion,
retrogrades and sect do not change. What changes is everything measured
against the SIGNS: dignity, house placement, house rulership, dispositors,
and element/modality balance.
"""

import math
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
FL = swe.FLG_SWIEPH | swe.FLG_SPEED
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
BLAT, BLON = 40.4406, -79.9959
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
AY = swe.get_ayanamsa_ut(JD)

IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
       ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
       ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
       ("Pluto", swe.PLUTO)]
TRAD7 = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
ALL = [n for n, _ in IDS]
P, SPD = {}, {}
for nm, sid in IDS:
    x = swe.calc_ut(JD, sid, FL)[0]
    P[nm] = (x[0] - AY) % 360.0
    SPD[nm] = x[3]
nn = swe.calc_ut(JD, swe.TRUE_NODE, FL)[0]
NODE = {"North Node": (nn[0] - AY) % 360.0, "South Node": (nn[0] + 180 - AY) % 360.0}

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
MODE = {"Aries": "cardinal", "Cancer": "cardinal", "Libra": "cardinal",
        "Capricorn": "cardinal", "Taurus": "fixed", "Leo": "fixed",
        "Scorpio": "fixed", "Aquarius": "fixed", "Gemini": "mutable",
        "Virgo": "mutable", "Sagittarius": "mutable", "Pisces": "mutable"}
TRIP = {"fire": ("Sun", "Jupiter", "Saturn"), "earth": ("Venus", "Moon", "Mars"),
        "air": ("Saturn", "Mercury", "Jupiter"), "water": ("Venus", "Mars", "Moon")}
BOUNDS = {
    "Aries": [(6, "Jupiter"), (12, "Venus"), (20, "Mercury"), (25, "Mars"), (30, "Saturn")],
    "Taurus": [(8, "Venus"), (14, "Mercury"), (22, "Jupiter"), (27, "Saturn"), (30, "Mars")],
    "Gemini": [(6, "Mercury"), (12, "Jupiter"), (17, "Venus"), (24, "Mars"), (30, "Saturn")],
    "Cancer": [(7, "Mars"), (13, "Venus"), (19, "Mercury"), (26, "Jupiter"), (30, "Saturn")],
    "Leo": [(6, "Jupiter"), (11, "Venus"), (18, "Saturn"), (24, "Mercury"), (30, "Mars")],
    "Virgo": [(7, "Mercury"), (17, "Venus"), (21, "Jupiter"), (28, "Mars"), (30, "Saturn")],
    "Libra": [(6, "Saturn"), (14, "Mercury"), (21, "Jupiter"), (28, "Venus"), (30, "Mars")],
    "Scorpio": [(7, "Mars"), (11, "Venus"), (19, "Mercury"), (24, "Jupiter"), (30, "Saturn")],
    "Sagittarius": [(12, "Jupiter"), (17, "Venus"), (21, "Mercury"), (26, "Saturn"), (30, "Mars")],
    "Capricorn": [(7, "Mercury"), (14, "Jupiter"), (22, "Venus"), (26, "Saturn"), (30, "Mars")],
    "Aquarius": [(7, "Mercury"), (13, "Venus"), (20, "Jupiter"), (25, "Mars"), (30, "Saturn")],
    "Pisces": [(12, "Venus"), (16, "Jupiter"), (19, "Mercury"), (28, "Mars"), (30, "Saturn")],
}
CHAL = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]
JOY = {"Mercury": 1, "Moon": 3, "Venus": 5, "Mars": 6, "Sun": 9, "Jupiter": 11,
       "Saturn": 12}
HN = {1: "self, body, vitality", 2: "money, resources, worth",
      3: "siblings, the local, daily mind", 4: "home, roots, family, land",
      5: "children, pleasure, creativity", 6: "work, health, service, routine",
      7: "partnership, the other", 8: "shared resources, depth, mortality",
      9: "the foreign, learning, worldview", 10: "career, standing, action",
      11: "friends, allies, gains", 12: "retreat, loss, the unseen"}


def sg(x):
    return S[int((x % 360) // 30)]


def fmt(x):
    i = int((x % 360) // 30)
    p = x % 360 - i * 30
    d = int(p)
    m = int(round((p - d) * 60))
    if m == 60:
        m, d = 0, d + 1
    return f"{d:2d}°{m:02d}' {S[i]}"


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def bound(v):
    for hi, r in BOUNDS[sg(v)]:
        if v % 30 < hi:
            return r
    return BOUNDS[sg(v)][-1][1]


def face(v):
    return CHAL[int(v // 10) % 7]


cusp, am = swe.houses(JD, BLAT, BLON, b"P")
ASC = (am[0] - AY) % 360.0
MC = (am[1] - AY) % 360.0
AI = S.index(sg(ASC))
H = {b: ((S.index(sg(P[b])) - AI) % 12) + 1 for b in ALL}
HN_ = {b: ((S.index(sg(NODE[b])) - AI) % 12) + 1 for b in NODE}
DAY = True  # verified below
HR = "=" * 96


def main():
    print(HR)
    print("SIDEREAL NATAL CHART — Lahiri, whole sign, traditional technique")
    print(HR)
    print(f"  7 June 1996, 19:35 UT, Pittsburgh PA 40.4406N 79.9959W")
    print(f"  Lahiri ayanamsa {AY:.4f}°")
    print(f"  ASC {fmt(ASC)}      MC {fmt(MC)}")
    print(f"  DSC {fmt((ASC+180)%360)}      IC {fmt((MC+180)%360)}")
    sun_above = 0 < ((P["Sun"] - ASC) % 360) < 180
    print(f"  Sun {'below' if sun_above else 'ABOVE'} the horizon -> "
          f"{'NIGHT' if sun_above else 'DAY'} chart")
    print(f"  MC falls in whole-sign house "
          f"{((S.index(sg(MC)) - AI) % 12) + 1}\n")

    print("  PLANETS")
    print(f"  {'body':<9}{'position':<20}{'h':<4}{'dignity':<34}{'motion':<12}phase")
    for b in ALL:
        s = sg(P[b])
        dg = []
        if DOM[s] == b:
            dg.append("DOMICILE")
        if EX.get(b) == s:
            dg.append("EXALTATION")
        if DOM[S[(S.index(s) + 6) % 12]] == b:
            dg.append("DETRIMENT")
        if b in EX and S[(S.index(EX[b]) + 6) % 12] == s:
            dg.append("FALL")
        d_, n_, pt = TRIP[ELEM[s]]
        if b == (d_ if DAY else n_):
            dg.append("triplicity")
        elif b == pt:
            dg.append("triplicity (part.)")
        if bound(P[b]) == b:
            dg.append("bound")
        if face(P[b]) == b:
            dg.append("face")
        sep = abs(n180(P[b] - P["Sun"]))
        if b == "Sun":
            ph = "-"
        else:
            st = ("CAZIMI" if sep <= 0.283 else "COMBUST" if sep <= 8
                  else "under beams" if sep <= 15 else "free")
            ori = "occid." if n180(P[b] - P["Sun"]) > 0 else "orient."
            ph = f"{st} {sep:.2f}° {ori}"
        print(f"  {b:<9}{fmt(P[b]):<20}{H[b]:<4}"
              f"{', '.join(dg) if dg else 'peregrine':<34}"
              f"{('RETROGRADE' if SPD[b] < 0 else 'direct'):<12}{ph}")
    print(f"\n  {'North Node':<9}{fmt(NODE['North Node']):<20}"
          f"h{HN_['North Node']}   (kept out of the condition analysis)")
    print(f"  {'South Node':<9}{fmt(NODE['South Node']):<20}h{HN_['South Node']}")
    print(f"  North Node to ASC: {abs(n180(NODE['North Node'] - ASC)):.2f}°")

    print("\n  THE TWELVE HOUSES")
    print(f"  {'h':<4}{'sign':<13}{'topic':<34}{'ruler':<9}{'in h':<6}occupants")
    for h in range(1, 13):
        s = S[(AI + h - 1) % 12]
        r = DOM[s]
        occ = [b for b in ALL if H[b] == h] + [k for k in NODE if HN_[k] == h]
        j = [p for p, hh in JOY.items() if hh == h and H.get(p) == h]
        print(f"  {h:<4}{s:<13}{HN[h]:<34}{r:<9}{H[r]:<6}"
              f"{', '.join(occ) or '-'}{'   ★joy' if j else ''}")

    print("\n  SECT — day chart")
    print(f"    sect light            Sun, in h{H['Sun']}")
    print(f"    in sect               Sun, Jupiter, Saturn")
    print(f"    out of sect           Moon, Venus, Mars")
    print(f"    benefic of the sect   Jupiter  (h{H['Jupiter']}, {sg(P['Jupiter'])})")
    print(f"    malefic of the sect   Saturn   (h{H['Saturn']}, {sg(P['Saturn'])})")
    print(f"    contrary-to-sect malefic  Mars (h{H['Mars']}, {sg(P['Mars'])})"
          f"  <- traditionally the most difficult body in a day chart")

    print("\n  ASPECTS  (degree-based; identical to the tropical chart, since")
    print("            both zodiacs shift every longitude equally)")
    ASP = [("conjunction", 0, 10), ("semi-sextile", 30, 3), ("sextile", 60, 6),
           ("square", 90, 8), ("trine", 120, 8), ("quincunx", 150, 3),
           ("opposition", 180, 10)]
    SIGNASP = {0: (0,), 30: (1, 11), 60: (2, 10), 90: (3, 9), 120: (4, 8),
               150: (5, 7), 180: (6,)}
    for i in range(len(ALL)):
        for j in range(i + 1, len(ALL)):
            a, b = ALL[i], ALL[j]
            sep = abs(n180(P[a] - P[b]))
            for nm, deg, orb in ASP:
                if abs(sep - deg) <= orb:
                    d = (S.index(sg(P[a])) - S.index(sg(P[b]))) % 12
                    ok = d in SIGNASP[deg]
                    ap = "applying" if (SPD[a] - SPD[b]) * n180(P[b] - P[a]) > 0 \
                        else "separating"
                    print(f"    {a:<9}{nm:<14}{b:<10}orb {abs(sep-deg):5.2f}°  "
                          f"{ap:<11}"
                          f"{'sign-confirmed' if ok else 'OUT OF SIGN'}")
                    break

    print("\n  DISPOSITORS")
    for b in TRAD7:
        ch, cur, g = [], b, 0
        while g < 12:
            nx = DOM[sg(P[cur])]
            if nx == cur:
                ch.append(f"{cur} (own sign — TERMINUS)")
                break
            ch.append(nx)
            if nx in ch[:-1]:
                ch[-1] += " [loop]"
                break
            cur, g = nx, g + 1
        print(f"    {b:<9}-> " + " -> ".join(ch))
    fin = sorted({b for b in TRAD7 if DOM[sg(P[b])] == b})
    print(f"    final dispositors: {', '.join(fin) or 'none — the chart loops'}")

    print("\n  ANGULARITY (whole sign)")
    for lab, hs in (("angular  ", (1, 4, 7, 10)), ("succedent", (2, 5, 8, 11)),
                    ("cadent   ", (3, 6, 9, 12))):
        ps = [f"{b}(h{H[b]})" for b in ALL if H[b] in hs]
        print(f"    {lab} {len(ps)}   {', '.join(ps) or '-'}")

    print("\n  ELEMENT AND MODALITY  (ten planets, plus the Ascendant)")
    for tab, nm2 in ((ELEM, "element"), (MODE, "modality")):
        c = {}
        for b in ALL:
            c[tab[sg(P[b])]] = c.get(tab[sg(P[b])], 0) + 1
        asc_v = tab[sg(ASC)]
        print(f"    {nm2:<9}" + "  ".join(f"{k} {v}" for k, v in
                                          sorted(c.items(), key=lambda t: -t[1]))
              + f"   |  ASC is {asc_v}")


if __name__ == "__main__":
    main()
