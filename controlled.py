#!/usr/bin/env python3
"""
Controlled zodiac experiment.

ONE technique set, applied identically to two zodiacs. The only variable is
tropical longitude vs Lahiri sidereal longitude.

TECHNIQUE SET (held constant):
  whole-sign houses
  seven traditional planets only
  sect
  domicile, exaltation, triplicity, bounds; detriment and fall
  planetary joys
  angular / succedent / cadent
  traditional rulership and dispositors
  the five classical aspects ONLY: conjunction, sextile, square, trine,
    opposition, taken whole-sign with degree exactness reported
  reception through recognised dignity, requiring an aspect to operate
  Lots of Fortune and Spirit
  prenatal syzygy, in both
  Nodes reported as a separate optional layer with no interpretive language

REMOVED from both:
  almuten figuris; faces as interpretive evidence; semi-sextiles; quincunxes;
  modern outer-planet rulership; the outer planets as primary significators;
  modern nodal interpretation

LABELLING: the tropical run is a Hellenistic technique set on the zodiac that
tradition used. The sidereal run is an EXPERIMENTAL APPLICATION of the same
technique set to Lahiri sidereal longitudes. It is not historical Hellenistic
practice and is not labelled as such.
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
JOY = {"Mercury": 1, "Moon": 3, "Venus": 5, "Mars": 6, "Sun": 9, "Jupiter": 11,
       "Saturn": 12}
HTOPIC = {1: "body and self", 2: "livelihood", 3: "siblings, the near",
          4: "home, parents, endings", 5: "children, pleasure",
          6: "injury, labour", 7: "marriage, partners", 8: "death, others' goods",
          9: "travel, the divine, learning", 10: "action and standing",
          11: "friends and benefactors", 12: "enmity, the hidden"}
ASPD = {0: ("conjunction", 0), 2: ("sextile", 60), 3: ("square", 90),
        4: ("trine", 120), 6: ("opposition", 180), 8: ("trine", 120),
        9: ("square", 90), 10: ("sextile", 60)}


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


def bnd(v):
    for hi, r in BOUNDS[sg(v)]:
        if v % 30 < hi:
            return r
    return BOUNDS[sg(v)][-1][1]


def run(tag, P, ASC, syz, node, day=True):
    AI = S.index(sg(ASC))
    H = {b: ((S.index(sg(P[b])) - AI) % 12) + 1 for b in T7}
    out = {"tag": tag, "ASC": ASC, "H": H, "P": P}
    print("=" * 98)
    print(tag)
    print("=" * 98)
    print(f"  Ascendant {fmt(ASC)}    lord of the Ascendant: {DOM[sg(ASC)]}"
          f" in house {H[DOM[sg(ASC)]]}")
    print(f"  DAY chart. Sect light Sun. Benefic of sect Jupiter. "
          f"Malefic of sect Saturn. Contrary to sect: Mars.\n")

    print("  PLANETS")
    print(f"  {'':<9}{'position':<19}{'h':<4}{'quadrant':<11}{'dignity':<32}"
          f"{'bound':<9}{'solar phase'}")
    for b in T7:
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
        d, n, pt = TRIP[ELEM[s]]
        if b == (d if day else n):
            dg.append("triplicity")
        elif b == pt:
            dg.append("triplicity (part.)")
        if bnd(P[b]) == b:
            dg.append("own bound")
        sep = abs(n180(P[b] - P["Sun"]))
        ph = "" if b == "Sun" else (
            f"COMBUST {sep:.2f}°" if sep <= 8 else
            f"under the beams {sep:.2f}°" if sep <= 15 else "free of the beams")
        q = ("angular" if H[b] in (1, 4, 7, 10) else
             "succedent" if H[b] in (2, 5, 8, 11) else "cadent")
        print(f"  {b:<9}{fmt(P[b]):<19}{H[b]:<4}{q:<11}"
              f"{', '.join(dg) if dg else 'peregrine':<32}{bnd(P[b]):<9}{ph}"
              f"{'   ★JOY' if JOY.get(b) == H[b] else ''}")

    print("\n  HOUSES")
    print(f"  {'h':<4}{'sign':<13}{'topic':<28}{'lord':<9}{'lord in h':<11}occupants")
    for h in range(1, 13):
        s = S[(AI + h - 1) % 12]
        r = DOM[s]
        occ = [b for b in T7 if H[b] == h]
        print(f"  {h:<4}{s:<13}{HTOPIC[h]:<28}{r:<9}{H[r]:<11}"
              f"{', '.join(occ) or '-'}")

    print("\n  ASPECTS — five classical only, whole sign, exactness in degrees")
    asps = []
    for i in range(len(T7)):
        for j in range(i + 1, len(T7)):
            a, b = T7[i], T7[j]
            d = (S.index(sg(P[b])) - S.index(sg(P[a]))) % 12
            if d not in ASPD:
                continue
            nm, deg = ASPD[d]
            ex = abs(abs(n180(P[a] - P[b])) - deg)
            rec = []
            for x, y in ((a, b), (b, a)):
                if DOM[sg(P[y])] == x:
                    rec.append(f"{x} receives {y} by domicile")
                elif EX.get(x) == sg(P[y]):
                    rec.append(f"{x} receives {y} by exaltation")
                elif bnd(P[y]) == x:
                    rec.append(f"{x} receives {y} by bound")
            asps.append((ex, a, nm, b, rec))
    for ex, a, nm, b, rec in sorted(asps):
        print(f"    {a:<9}{nm:<12}{b:<10}exact within {ex:5.2f}°"
              + ("   " + "; ".join(rec) if rec else ""))
    averse = [f"{T7[i]}/{T7[j]}" for i in range(len(T7)) for j in range(i + 1, len(T7))
              if (S.index(sg(P[T7[j]])) - S.index(sg(P[T7[i]]))) % 12 not in ASPD]
    print(f"    IN AVERSION (no relationship): {', '.join(averse) or 'none'}")

    print("\n  DISPOSITORS")
    for b in T7:
        ch, cur, g = [], b, 0
        while g < 14:
            nx = DOM[sg(P[cur])]
            if nx == cur:
                ch.append(f"{cur} (own domicile — terminus)")
                break
            if nx in ch:
                ch.append(f"{nx} [loop]")
                break
            ch.append(nx)
            cur, g = nx, g + 1
        print(f"    {b:<9}" + " → ".join(ch))
    print(f"    final dispositors: "
          f"{', '.join(b for b in T7 if DOM[sg(P[b])] == b) or 'none, all chains loop'}")

    F = (ASC + P["Moon"] - P["Sun"]) % 360
    Sp = (ASC + P["Sun"] - P["Moon"]) % 360
    print("\n  LOTS AND SYZYGY")
    for nm, v in (("Fortune", F), ("Spirit", Sp), ("prenatal syzygy", syz)):
        h = ((S.index(sg(v)) - AI) % 12) + 1
        r = DOM[sg(v)]
        print(f"    {nm:<17}{fmt(v):<19}h{h:<4}lord {r} in h{H[r]}")
    print(f"\n  NODES (separate layer, no interpretation applied)")
    print(f"    North Node {fmt(node):<19}h{((S.index(sg(node)) - AI) % 12) + 1}")
    print(f"    South Node {fmt((node+180)%360):<19}"
          f"h{((S.index(sg((node+180)%360)) - AI) % 12) + 1}\n")
    out["asps"] = {(a, b) for _, a, _, b, _ in asps}
    out["averse"] = set(averse)
    return out


def main():
    P = {n: swe.calc_ut(JD, s, FL)[0][0] for n, s in IDS}
    cusp, am = swe.houses(JD, 40.4406, -79.9959, b"P")
    node = swe.calc_ut(JD, swe.TRUE_NODE, FL)[0][0]
    t = JD
    while ((swe.calc_ut(t, swe.MOON, FL)[0][0]
            - swe.calc_ut(t, swe.SUN, FL)[0][0]) % 360) >= 180:
        t -= 0.25
    lo, hi = t, t + 0.25
    for _ in range(40):
        m = (lo + hi) / 2
        if ((swe.calc_ut(m, swe.MOON, FL)[0][0]
             - swe.calc_ut(m, swe.SUN, FL)[0][0]) % 360) < 180:
            lo = m
        else:
            hi = m
    syz = swe.calc_ut((lo + hi) / 2, swe.MOON, FL)[0][0]

    a = run("TROPICAL — Hellenistic technique set on the zodiac tradition used",
            P, am[0], syz, node)
    b = run("LAHIRI SIDEREAL — EXPERIMENTAL application of the same technique "
            "set.\nNot historical Hellenistic practice.",
            {n: (v - AY) % 360 for n, v in P.items()}, (am[0] - AY) % 360,
            (syz - AY) % 360, (node - AY) % 360)

    print("=" * 98)
    print("WHAT THE ZODIAC CHANGE ACTUALLY CHANGES")
    print("=" * 98)
    print("  aspects present in BOTH (zodiac-invariant):")
    for x in sorted(a["asps"] & b["asps"]):
        print(f"    {x[0]} / {x[1]}")
    print("  aspects present ONLY in tropical:")
    for x in sorted(a["asps"] - b["asps"]):
        print(f"    {x[0]} / {x[1]}")
    print("  aspects present ONLY in sidereal:")
    for x in sorted(b["asps"] - a["asps"]):
        print(f"    {x[0]} / {x[1]}")
    print(f"\n  houses unchanged: "
          f"{', '.join(x for x in T7 if a['H'][x] == b['H'][x])}")
    print(f"  houses changed  : "
          f"{', '.join(f'{x} h{a[chr(72)][x]}->h{b[chr(72)][x]}' for x in T7 if a['H'][x] != b['H'][x])}")


if __name__ == "__main__":
    main()
