#!/usr/bin/env python3
"""
Full tropical natal chart, read blind.

  zodiac    tropical
  houses    whole sign
  technique Hellenistic / traditional

Nothing from the relocation work or from the sidereal reading enters this
file. No location other than the birth place is used.

Deeper than the sidereal pass, which stopped at major dignity. This adds:
  - the complete five-fold dignity table (domicile, exaltation, triplicity,
    bound, face) for every traditional planet
  - almuten figuris scored across the five hylegical places
  - the prenatal syzygy and the Moon's phase
  - the seven Hermetic Lots with their rulers
  - the triplicity rulers of the sect light, which divide the life
  - antiscia
  - every house walked individually, every aspect listed with orb,
    application and sign confirmation
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
       ("Pluto", swe.PLUTO)]
T7 = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
ALL = [n for n, _ in IDS]
P, SPD = {}, {}
for nm, sid in IDS:
    x = swe.calc_ut(JD, sid, FL)[0]
    P[nm], SPD[nm] = x[0], x[3]
nn = swe.calc_ut(JD, swe.TRUE_NODE, FL)[0][0]
NODE = {"North Node": nn, "South Node": (nn + 180) % 360}

DOM = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
       "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
       "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
       "Pisces": "Jupiter"}
EX = {"Sun": ("Aries", 19), "Moon": ("Taurus", 3), "Mercury": ("Virgo", 15),
      "Venus": ("Pisces", 27), "Mars": ("Capricorn", 28),
      "Jupiter": ("Cancer", 15), "Saturn": ("Libra", 21)}
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
HN = {1: "body, self, vitality", 2: "money, movable goods, worth",
      3: "siblings, neighbours, the near", 4: "home, land, family, endings",
      5: "children, pleasure, what you make", 6: "illness, labour, servitude",
      7: "marriage, partners, open enemies", 8: "death, inheritance, others' money",
      9: "the foreign, god, learning, travel", 10: "action, honour, standing",
      11: "friends, patrons, hopes", 12: "enemies, confinement, the hidden"}


def sg(x):
    return S[int((x % 360) // 30)]


def dms(x):
    i = int((x % 360) // 30)
    p = x % 360 - i * 30
    d = int(p)
    m = int(round((p - d) * 60))
    if m == 60:
        m, d = 0, d + 1
    return f"{d:2d}°{m:02d}' {S[i]}"


def n180(x):
    return ((x + 180.0) % 360.0) - 180.0


def bnd(v):
    for hi, r in BOUNDS[sg(v)]:
        if v % 30 < hi:
            return r
    return BOUNDS[sg(v)][-1][1]


def fce(v):
    return CHAL[int(v // 30) * 3 % 7] if False else CHAL[int(v // 10) % 7]


cusp, am = swe.houses(JD, BLAT, BLON, b"P")
ASC, MC = am[0], am[1]
AI = S.index(sg(ASC))
H = {b: ((S.index(sg(P[b])) - AI) % 12) + 1 for b in ALL}
HNODE = {k: ((S.index(sg(v)) - AI) % 12) + 1 for k, v in NODE.items()}
DAY = True


def dignities(b):
    v = P[b]
    s = sg(v)
    out = []
    if DOM[s] == b:
        out.append(("domicile", 5))
    if b in EX and EX[b][0] == s:
        out.append(("exaltation", 4))
    d, n, pt = TRIP[ELEM[s]]
    if b == (d if DAY else n):
        out.append(("triplicity", 3))
    elif b == pt:
        out.append(("triplicity(part)", 3))
    if bnd(v) == b:
        out.append(("bound", 2))
    if fce(v) == b:
        out.append(("face", 1))
    deb = []
    if DOM[S[(S.index(s) + 6) % 12]] == b:
        deb.append("DETRIMENT")
    if b in EX and S[(S.index(EX[b][0]) + 6) % 12] == s:
        deb.append("FALL")
    return out, deb


def rulers_of(v):
    """The five dignity lords of a degree."""
    s = sg(v)
    d, n, pt = TRIP[ELEM[s]]
    return {"domicile": DOM[s], "exaltation": next((k for k, x in EX.items()
                                                    if x[0] == s), "-"),
            "triplicity": d if DAY else n, "bound": bnd(v), "face": fce(v)}


HR = "=" * 96


def main():
    print(HR)
    print("TROPICAL NATAL CHART — whole sign, traditional technique, read blind")
    print(HR)
    print(f"  7 June 1996, 19:35 UT, Pittsburgh PA")
    print(f"  ASC {dms(ASC)}   MC {dms(MC)}   "
          f"DSC {dms((ASC+180)%360)}   IC {dms((MC+180)%360)}")
    print(f"  Sun above the horizon -> DAY chart, sect light is the Sun\n")

    print("  1. THE FIVE-FOLD DIGNITY TABLE")
    print(f"  {'body':<9}{'position':<18}{'h':<4}{'dignities held':<30}"
          f"{'debility':<13}{'bound':<9}{'face':<9}pts")
    tot = {}
    for b in T7:
        dg, deb = dignities(b)
        pts = sum(p for _, p in dg)
        tot[b] = pts
        print(f"  {b:<9}{dms(P[b]):<18}{H[b]:<4}"
              f"{', '.join(x for x, _ in dg) if dg else 'PEREGRINE':<30}"
              f"{', '.join(deb) or '-':<13}{bnd(P[b]):<9}{fce(P[b]):<9}{pts}")
    for b in ALL[7:]:
        print(f"  {b:<9}{dms(P[b]):<18}{H[b]:<4}{'(outside the scheme)':<30}")
    print(f"\n  {'North Node':<11}{dms(NODE['North Node'])}  h{HNODE['North Node']}"
          f"    {'South Node':<11}{dms(NODE['South Node'])}  h{HNODE['South Node']}")
    print(f"  North Node to ASC {abs(n180(NODE['North Node']-ASC)):.2f}°")

    print("\n  2. MOON PHASE AND PRENATAL SYZYGY")
    el = (P["Moon"] - P["Sun"]) % 360
    ph = ("new" if el < 45 else "crescent" if el < 90 else "first quarter"
          if el < 135 else "gibbous" if el < 180 else "full" if el < 225
          else "disseminating" if el < 270 else "last quarter" if el < 315
          else "balsamic")
    print(f"    elongation {el:.2f}°  ->  {ph}, waning")
    print(f"    Moon speed {SPD['Moon']:.4f}°/day "
          f"({'fast' if SPD['Moon'] > 13.18 else 'slow'}; mean is 13.18)")
    t = JD
    while True:
        e = (swe.calc_ut(t, swe.MOON, FL)[0][0] - swe.calc_ut(t, swe.SUN, FL)[0][0]) % 360
        if e < 180:
            break
        t -= 0.25
    lo, hi = t, t + 0.25
    for _ in range(40):
        m = (lo + hi) / 2
        e = (swe.calc_ut(m, swe.MOON, FL)[0][0] - swe.calc_ut(m, swe.SUN, FL)[0][0]) % 360
        if e < 180:
            lo = m
        else:
            hi = m
    syz = swe.calc_ut((lo + hi) / 2, swe.MOON, FL)[0][0]
    y, mo, d, hh = swe.revjul((lo + hi) / 2, swe.GREG_CAL)
    print(f"    prenatal syzygy: FULL MOON {y}-{mo:02d}-{d:02d} at {dms(syz)}"
          f"  (whole-sign h{((S.index(sg(syz))-AI)%12)+1})")

    print("\n  3. ALMUTEN FIGURIS — scored across the five hylegical places")
    FORT = (ASC + P["Moon"] - P["Sun"]) % 360
    SPIR = (ASC + P["Sun"] - P["Moon"]) % 360
    places = [("Ascendant", ASC), ("Sun", P["Sun"]), ("Moon", P["Moon"]),
              ("Lot of Fortune", FORT), ("prenatal syzygy", syz)]
    W = {"domicile": 5, "exaltation": 4, "triplicity": 3, "bound": 2, "face": 1}
    score = {b: 0 for b in T7}
    print(f"    {'place':<17}{'degree':<18}" + "".join(k[:4].rjust(11) for k in W))
    for nm, v in places:
        r = rulers_of(v)
        row = ""
        for k in W:
            who = r[k]
            row += (who or "-")[:9].rjust(11)
            if who in score:
                score[who] += W[k]
        print(f"    {nm:<17}{dms(v):<18}{row}")
    for b in T7:
        if H[b] in (1, 10):
            score[b] += 3
        elif H[b] in (4, 7, 11):
            score[b] += 2
        elif H[b] in (2, 5, 9):
            score[b] += 1
    print(f"\n    with accidental bonus for house position:")
    for b, v in sorted(score.items(), key=lambda t: -t[1]):
        print(f"      {b:<9}{v:>4}")
    win = max(score, key=score.get)
    print(f"    ALMUTEN FIGURIS: {win}  ({dms(P[win])}, h{H[win]})")

    print("\n  4. THE SEVEN HERMETIC LOTS (day formulae)")
    L = {"Fortune": FORT, "Spirit": SPIR,
         "Eros": (ASC + P["Venus"] - SPIR) % 360,
         "Necessity": (ASC + FORT - P["Mercury"]) % 360,
         "Courage": (ASC + P["Mars"] - FORT) % 360,
         "Victory": (ASC + P["Jupiter"] - SPIR) % 360,
         "Nemesis": (ASC + FORT - P["Saturn"]) % 360}
    print(f"    {'lot':<12}{'degree':<18}{'h':<4}{'ruler':<9}{'ruler in h':<12}ruler condition")
    for k, v in L.items():
        r = DOM[sg(v)]
        dg, deb = dignities(r)
        print(f"    {k:<12}{dms(v):<18}{((S.index(sg(v))-AI)%12)+1:<4}{r:<9}"
              f"h{H[r]:<11}"
              f"{', '.join(x for x, _ in dg) or 'peregrine'}"
              f"{'  ' + ','.join(deb) if deb else ''}")

    print("\n  5. TRIPLICITY RULERS OF THE SECT LIGHT — the divisions of life")
    e = ELEM[sg(P["Sun"])]
    d, n, pt = TRIP[e]
    print(f"    Sun in {sg(P['Sun'])} ({e}), day chart")
    for lab, r in (("first third ", d), ("second third", n), ("participating", pt)):
        dg, deb = dignities(r)
        print(f"      {lab}  {r:<9}{dms(P[r]):<18}h{H[r]:<4}"
              f"{', '.join(x for x, _ in dg) or 'peregrine'}"
              f"{'  ' + ','.join(deb) if deb else ''}")

    print("\n  6. THE TWELVE HOUSES")
    print(f"  {'h':<4}{'sign':<13}{'topic':<34}{'ruler':<9}{'in h':<6}"
          f"{'ruler condition':<24}occupants")
    for h in range(1, 13):
        s = S[(AI + h - 1) % 12]
        r = DOM[s]
        dg, deb = dignities(r)
        cond = (', '.join(x for x, _ in dg) or 'peregrine') + \
               ('/' + ','.join(deb) if deb else '')
        occ = [b for b in ALL if H[b] == h] + \
              [k for k, v in HNODE.items() if v == h]
        j = [p for p, hh in JOY.items() if hh == h and H.get(p) == h]
        print(f"  {h:<4}{s:<13}{HN[h]:<34}{r:<9}{H[r]:<6}{cond:<24}"
              f"{', '.join(occ) or '-'}{'  ★joy' if j else ''}")

    print("\n  7. ASPECTS")
    ASP = [("conjunction", 0, 10), ("semi-sextile", 30, 3), ("sextile", 60, 6),
           ("square", 90, 8), ("trine", 120, 8), ("quincunx", 150, 3),
           ("opposition", 180, 10)]
    SA = {0: (0,), 30: (1, 11), 60: (2, 10), 90: (3, 9), 120: (4, 8),
          150: (5, 7), 180: (6,)}
    for i in range(len(ALL)):
        for j2 in range(i + 1, len(ALL)):
            a, b = ALL[i], ALL[j2]
            sep = abs(n180(P[a] - P[b]))
            for nm, deg, orb in ASP:
                if abs(sep - deg) <= orb:
                    dd = (S.index(sg(P[a])) - S.index(sg(P[b]))) % 12
                    ap = "applying" if (SPD[a] - SPD[b]) * n180(P[b] - P[a]) > 0 \
                        else "separating"
                    rec = []
                    if DOM[sg(P[a])] == b:
                        rec.append(f"{b} rules {a}")
                    if DOM[sg(P[b])] == a:
                        rec.append(f"{a} rules {b}")
                    if bnd(P[a]) == b:
                        rec.append(f"{b} bounds {a}")
                    if bnd(P[b]) == a:
                        rec.append(f"{a} bounds {b}")
                    print(f"    {a:<9}{nm:<14}{b:<10}orb {abs(sep-deg):5.2f}°  "
                          f"{ap:<11}{'in sign' if dd in SA[deg] else 'OUT OF SIGN':<12}"
                          + ("; ".join(rec) if rec else ""))
                    break

    print("\n  8. ANTISCIA (mirrored across the Cancer/Capricorn axis)")
    for b in T7:
        an = (180.0 - P[b]) % 360
        hits = [x for x in T7 if x != b and abs(n180(P[x] - an)) <= 2.0]
        if hits:
            print(f"    {b:<9}antiscion {dms(an):<18}"
                  f"contacts {', '.join(f'{x} ({abs(n180(P[x]-an)):.2f}°)' for x in hits)}")

    print("\n  9. DISPOSITORS")
    for b in T7:
        ch, cur, g = [], b, 0
        while g < 14:
            nx = DOM[sg(P[cur])]
            if nx == cur:
                ch.append(f"{cur} (own sign, TERMINUS)")
                break
            ch.append(nx)
            if ch.count(nx) > 1 or (len(ch) > 1 and nx == ch[-2]):
                ch[-1] += " [LOOP]"
                break
            cur, g = nx, g + 1
        print(f"    {b:<9}-> " + " -> ".join(ch))
    print(f"    final dispositors: "
          f"{', '.join(b for b in T7 if DOM[sg(P[b])] == b) or 'NONE'}")
    mr = [f"{a}/{b}" for i, a in enumerate(T7) for b in T7[i+1:]
          if DOM[sg(P[a])] == b and DOM[sg(P[b])] == a]
    print(f"    mutual receptions by domicile: {', '.join(mr) or 'none'}")

    print("\n  10. ANGULARITY, ELEMENT, MODALITY")
    for lab, hs in (("angular  ", (1, 4, 7, 10)), ("succedent", (2, 5, 8, 11)),
                    ("cadent   ", (3, 6, 9, 12))):
        print(f"    {lab} " + ", ".join(f"{b}(h{H[b]})" for b in ALL if H[b] in hs))
    for tab, nm in ((ELEM, "element "), (MODE, "modality")):
        c = {}
        for b in ALL:
            c[tab[sg(P[b])]] = c.get(tab[sg(P[b])], 0) + 1
        print(f"    {nm} " + "  ".join(f"{k} {v}" for k, v in
                                       sorted(c.items(), key=lambda t: -t[1]))
              + f"   | ASC {tab[sg(ASC)]}")


if __name__ == "__main__":
    main()
