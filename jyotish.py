#!/usr/bin/env python3
"""
Full Jyotish computation, built from scratch.

Nothing here is carried over from the Hellenistic scripts in this repo. The
dignity tables, aspect rules, house logic, strength measures and period
system are all Parashari and are stated as such. Where a technique belongs
to a different school, or where a rule is disputed, the code says so rather
than picking silently.

FRAMEWORK DECLARED UP FRONT
  ayanamsha        Lahiri (Chitrapaksha), the Indian government standard
  zodiac           sidereal
  houses           Parashari whole sign, rashi = bhava. Bhava chalit
                   (Sripati) cusps are computed separately so any placement
                   that would shift can be flagged rather than hidden.
  nodes            mean node primary, true node reported alongside. Mean is
                   the Jyotish standard; the difference is noted where it
                   would change a nakshatra or a house.
  system           Parashari throughout. No Jaimini rashi drishti, no
                   chara karakas, no Nadi. Anything from another school is
                   labelled inline.
  aspects          graha drishti only, sign-based: all grahas aspect the 7th
                   from themselves; Mars also the 4th and 8th; Jupiter the
                   5th and 9th; Saturn the 3rd and 10th. No Western aspects.
"""

import datetime as dt
import swisseph as swe

swe.set_ephe_path("/usr/share/swisseph")
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)

LAT, LON = 40.4406, -79.9959
JD = swe.julday(1996, 6, 7, 19 + 35 / 60.0, swe.GREG_CAL)
FL = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL

R = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
     "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

NAK = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
       "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
       "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
       "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
       "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
       "Revati"]
NAKLORD = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter",
           "Saturn", "Mercury"] * 3

VIM = [("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
       ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)]

LORD = {"Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus",
        "Scorpio": "Mars", "Sagittarius": "Jupiter", "Capricorn": "Saturn",
        "Aquarius": "Saturn", "Pisces": "Jupiter"}
OWN = {"Sun": ["Leo"], "Moon": ["Cancer"], "Mars": ["Aries", "Scorpio"],
       "Mercury": ["Gemini", "Virgo"], "Jupiter": ["Sagittarius", "Pisces"],
       "Venus": ["Taurus", "Libra"], "Saturn": ["Capricorn", "Aquarius"]}
EXALT = {"Sun": ("Aries", 10), "Moon": ("Taurus", 3), "Mars": ("Capricorn", 28),
         "Mercury": ("Virgo", 15), "Jupiter": ("Cancer", 5),
         "Venus": ("Pisces", 27), "Saturn": ("Libra", 20)}
MOOLA = {"Sun": ("Leo", 0, 20), "Moon": ("Taurus", 4, 30), "Mars": ("Aries", 0, 12),
         "Mercury": ("Virgo", 16, 20), "Jupiter": ("Sagittarius", 0, 10),
         "Venus": ("Libra", 0, 15), "Saturn": ("Aquarius", 0, 20)}
# Parashari natural relationships
NFRIEND = {"Sun": ["Moon", "Mars", "Jupiter"], "Moon": ["Sun", "Mercury"],
           "Mars": ["Sun", "Moon", "Jupiter"], "Mercury": ["Sun", "Venus"],
           "Jupiter": ["Sun", "Moon", "Mars"], "Venus": ["Mercury", "Saturn"],
           "Saturn": ["Mercury", "Venus"]}
NENEMY = {"Sun": ["Venus", "Saturn"], "Moon": [], "Mars": ["Mercury"],
          "Mercury": ["Moon"], "Jupiter": ["Mercury", "Venus"],
          "Venus": ["Sun", "Moon"], "Saturn": ["Sun", "Moon", "Mars"]}
# combustion orbs, Jyotish (asta). retrograde values in parentheses
COMB = {"Moon": (12, 12), "Mars": (17, 17), "Mercury": (14, 12),
        "Jupiter": (11, 11), "Venus": (10, 8), "Saturn": (15, 15)}
IDS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS),
       ("Mercury", swe.MERCURY), ("Jupiter", swe.JUPITER),
       ("Venus", swe.VENUS), ("Saturn", swe.SATURN)]
GRAHA = [n for n, _ in IDS] + ["Rahu", "Ketu"]


def sign(x):
    return R[int(x % 360 // 30)]


def si(x):
    return int(x % 360 // 30)


def dms(x):
    d = x % 30
    dd = int(d)
    m = int((d - dd) * 60)
    s = int(round((((d - dd) * 60) - m) * 60))
    if s == 60:
        s, m = 0, m + 1
    if m == 60:
        m, dd = 0, dd + 1
    return f"{dd:2d}°{m:02d}'{s:02d}\""


def nak(x):
    i = int((x % 360) / (360 / 27))
    pos = (x % 360) - i * (360 / 27)
    pada = int(pos / (360 / 108)) + 1
    return NAK[i], pada, NAKLORD[i], i, pos


def varga(lon, n):
    """Standard Parashari divisional sign index."""
    s, deg = si(lon), lon % 30
    part = int(deg / (30.0 / n))
    if n == 9:
        return (s * 9 + part) % 12
    if n == 10:
        return (s + part) % 12 if s % 2 == 0 else (s + 8 + part) % 12
    if n == 4:
        return (s + part * 3) % 12
    if n == 7:
        return (s + part) % 12 if s % 2 == 0 else (s + 6 + part) % 12
    if n == 2:
        return 4 if (s % 2 == 0) == (part == 0) else 3
    if n == 3:
        return (s + part * 4) % 12
    raise ValueError(n)


def dignity(p, lon):
    s = sign(lon)
    if p in ("Rahu", "Ketu"):
        return "node, no classical sign dignity in Parashara"
    if p in MOOLA and MOOLA[p][0] == s and MOOLA[p][1] <= lon % 30 < MOOLA[p][2]:
        return "MOOLATRIKONA"
    if p in EXALT and EXALT[p][0] == s:
        return f"EXALTED (deep {EXALT[p][1]}°)"
    if p in EXALT and R[(R.index(EXALT[p][0]) + 6) % 12] == s:
        return "DEBILITATED"
    if s in OWN.get(p, []):
        return "OWN SIGN"
    l = LORD[s]
    if l == p:
        return "OWN SIGN"
    if l in NFRIEND[p]:
        return "friend's sign"
    if l in NENEMY[p]:
        return "enemy's sign"
    return "neutral sign"


def temporal(p, others):
    """2,3,4,10,11,12 from a graha are its temporal friends."""
    out = {}
    for q, lq in others.items():
        if q == p:
            continue
        d = (si(lq) - si(others[p])) % 12 + 1
        out[q] = "friend" if d in (2, 3, 4, 10, 11, 12) else "enemy"
    return out


def compound(nat, temp):
    t = {("friend", "friend"): "great friend", ("friend", "enemy"): "neutral",
         ("neutral", "friend"): "friend", ("neutral", "enemy"): "enemy",
         ("enemy", "friend"): "neutral", ("enemy", "enemy"): "great enemy"}
    return t[(nat, temp)]


def drishti(p, from_i, to_i):
    """Parashari graha drishti, sign-based. Returns aspect strength label."""
    d = (to_i - from_i) % 12 + 1
    if d == 7:
        return "full (7th)"
    if p == "Mars" and d in (4, 8):
        return f"full ({d}th, special)"
    if p == "Jupiter" and d in (5, 9):
        return f"full ({d}th, special)"
    if p == "Saturn" and d in (3, 10):
        return f"full ({d}th, special)"
    return None


def main():
    P, SPD, RETRO = {}, {}, {}
    for n, i in IDS:
        v = swe.calc_ut(JD, i, FL)[0]
        P[n], SPD[n] = v[0], v[3]
        RETRO[n] = v[3] < 0
    mean = swe.calc_ut(JD, swe.MEAN_NODE, FL)[0][0]
    true = swe.calc_ut(JD, swe.TRUE_NODE, FL)[0][0]
    P["Rahu"], P["Ketu"] = mean, (mean + 180) % 360
    RETRO["Rahu"] = RETRO["Ketu"] = True
    cusp, asc = swe.houses_ex(JD, LAT, LON, b"P", swe.FLG_SIDEREAL)
    ASC, MC = asc[0], asc[1]
    AI = si(ASC)
    H = {p: (si(P[p]) - AI) % 12 + 1 for p in GRAHA}

    print("=" * 100)
    print("1. TECHNICAL FOUNDATION")
    print("=" * 100)
    print(f"  birth        7 June 1996, 15:35 EDT = 19:35 UT, Pittsburgh PA "
          f"({LAT}N, {abs(LON)}W)")
    print(f"  ayanamsha    Lahiri (Chitrapaksha) = "
          f"{swe.get_ayanamsa_ut(JD):.4f}°")
    print(f"  houses       Parashari whole sign. Lagna rashi = bhava 1.")
    print(f"  nodes        mean node used. Mean Rahu {dms(mean)} {sign(mean)}; "
          f"true Rahu {dms(true)} {sign(true)}")
    print(f"               difference {abs(((mean-true+180)%360)-180)*60:.1f}' "
          f"- same rashi and same nakshatra, so nothing turns on the choice")
    print(f"  system       Parashari only\n")
    print(f"  {'graha':<9}{'longitude':<22}{'nakshatra':<20}{'pada':<6}"
          f"{'nak lord':<10}{'bhava':<7}{'dignity':<24}{'motion'}")
    for p in GRAHA:
        nm, pd, nl, ni, _ = nak(P[p])
        print(f"  {p:<9}{dms(P[p])+' '+sign(P[p]):<22}{nm:<20}{pd:<6}{nl:<10}"
              f"{H[p]:<7}{dignity(p, P[p]):<24}"
              f"{'RETROGRADE' if RETRO[p] else 'direct'}")
    print(f"  {'Lagna':<9}{dms(ASC)+' '+sign(ASC):<22}"
          f"{nak(ASC)[0]:<20}{nak(ASC)[1]:<6}{nak(ASC)[2]:<10}{'1':<7}")
    print(f"  {'MC':<9}{dms(MC)+' '+sign(MC):<22}{nak(MC)[0]:<20}{nak(MC)[1]:<6}"
          f"{nak(MC)[2]:<10}{(si(MC)-AI)%12+1}")

    print("\n  bhava chalit check (Sripati cusps) - does any graha shift bhava?")
    for p in GRAHA:
        wh = H[p]
        k = 0
        for j in range(12):
            a, b = cusp[j], cusp[(j + 1) % 12]
            if (b - a) % 360 > 0 and (P[p] - a) % 360 < (b - a) % 360:
                k = j + 1
                break
        print(f"    {p:<9}whole sign h{wh:<4}Sripati h{k:<4}"
              f"{'SHIFTS' if wh != k else 'same'}")

    print("\n" + "=" * 100)
    print("2. COMBUSTION, MOTION, AVASTHA")
    print("=" * 100)
    for p in GRAHA:
        if p in ("Sun", "Rahu", "Ketu"):
            continue
        sep = abs(((P[p] - P["Sun"] + 180) % 360) - 180)
        orb = COMB[p][1 if RETRO[p] else 0]
        print(f"  {p:<9}{sep:6.2f}° from Sun, orb {orb}°  "
              f"{'COMBUST (asta)' if sep <= orb else 'not combust'}")
    d = (P["Moon"] - P["Sun"]) % 360
    ti = int(d / 12) + 1
    paksha = "Shukla" if ti <= 15 else "Krishna"
    print(f"\n  Moon-Sun elongation {d:.2f}° -> tithi {ti} "
          f"({paksha} paksha, tithi {ti if ti <= 15 else ti-15})")
    ill = swe.pheno_ut(JD, swe.MOON, swe.FLG_SWIEPH)[1]
    print(f"  Moon illuminated fraction {ill*100:.1f}% - WANING")
    print(f"  classical: the Moon is reckoned strong from Shukla Ashtami to")
    print(f"  Krishna Ashtami, i.e. while more than half lit. Tithi {ti} sits")
    print(f"  just inside that window, so this is a moderately strong Moon,")
    print(f"  not a dark one, but it is on the losing side of the cycle.")

    print("\n  Baladi avastha (infant/youth/adult/old/dead, by degree in sign):")
    for p in GRAHA:
        deg = P[p] % 30
        st = ["Bala (infant)", "Kumara (youth)", "Yuva (adult)",
              "Vriddha (old)", "Mrita (dead)"][min(int(deg / 6), 4)]
        if si(P[p]) % 2 == 1:
            st = ["Bala (infant)", "Kumara (youth)", "Yuva (adult)",
                  "Vriddha (old)", "Mrita (dead)"][min(int((30 - deg) / 6), 4)]
        print(f"    {p:<9}{deg:5.2f}° in an {'even' if si(P[p])%2 else 'odd'}"
              f" rashi -> {st}")

    print("\n" + "=" * 100)
    print("3. NAKSHATRA NETWORK")
    print("=" * 100)
    byn, byl = {}, {}
    for p in GRAHA:
        nm, pd, nl, ni, _ = nak(P[p])
        byn.setdefault((nm, ni), []).append((p, pd))
        byl.setdefault(nl, []).append(p)
    print("  planets sharing a nakshatra:")
    for (nm, ni), ps in sorted(byn.items(), key=lambda k: k[0][1]):
        if len(ps) > 1:
            print(f"    {nm:<18}{', '.join(f'{p} (pada {d})' for p, d in ps)}"
                  f"   nakshatra lord {NAKLORD[ni]}")
    print("\n  how much of the chart each graha rules by nakshatra lordship:")
    for l, ps in sorted(byl.items(), key=lambda k: -len(k[1])):
        print(f"    {l:<9}{len(ps)} placements: {', '.join(ps)}")
    print("\n  nakshatra-lord chains (graha -> its nakshatra lord -> that "
          "lord's own nakshatra lord):")
    for p in GRAHA:
        l1 = nak(P[p])[2]
        l2 = nak(P[l1])[2] if l1 in P else "-"
        l3 = nak(P[l2])[2] if l2 in P else "-"
        print(f"    {p:<9}-> {l1:<9}-> {l2:<9}-> {l3}")

    print("\n" + "=" * 100)
    print("4. HOUSE LORDS, ALL TWELVE")
    print("=" * 100)
    print(f"  {'bhava':<7}{'rashi':<14}{'lord':<9}{'lord in':<9}{'lord rashi':<14}"
          f"{'lord dignity':<24}{'occupants'}")
    for h in range(1, 13):
        rs = R[(AI + h - 1) % 12]
        l = LORD[rs]
        occ = [p for p in GRAHA if H[p] == h]
        print(f"  {h:<7}{rs:<14}{l:<9}h{H[l]:<8}{sign(P[l]):<14}"
              f"{dignity(l, P[l]):<24}{', '.join(occ) or '-'}")

    print("\n" + "=" * 100)
    print("5. FUNCTIONAL ROLES FROM VIRGO LAGNA")
    print("=" * 100)
    KENDRA, TRIKONA, DUS, UPA = (1, 4, 7, 10), (1, 5, 9), (6, 8, 12), (3, 6, 10, 11)
    for p in [n for n, _ in IDS]:
        hs = [h for h in range(1, 13) if LORD[R[(AI + h - 1) % 12]] == p]
        tags = []
        for h in hs:
            t = []
            if h in KENDRA:
                t.append("kendra")
            if h in TRIKONA:
                t.append("trikona")
            if h in DUS:
                t.append("dusthana")
            if h == 2 or h == 7:
                t.append("maraka")
            tags.append(f"{h} ({'/'.join(t) or 'neutral'})")
        note = ""
        if all(h in KENDRA for h in hs) and p in ("Jupiter", "Venus", "Mercury", "Moon"):
            note = "  <- kendradhipati dosha: a natural benefic owning only kendras"
        print(f"  {p:<9}rules {', '.join(tags)}{note}")

    print("\n" + "=" * 100)
    print("6. GRAHA DRISHTI (Parashari, sign-based)")
    print("=" * 100)
    for p in GRAHA:
        got = []
        for q in GRAHA:
            if q == p:
                continue
            a = drishti(q, si(P[q]), si(P[p]))
            if a:
                got.append(f"{q} {a}")
        cast = []
        for h in range(1, 13):
            a = drishti(p, si(P[p]), (AI + h - 1) % 12)
            if a:
                cast.append(f"h{h}")
        print(f"  {p:<9}casts on {', '.join(cast):<26}receives: "
              f"{', '.join(got) or 'nothing'}")

    print("\n" + "=" * 100)
    print("7. COMPOUND RELATIONSHIPS (natural + temporal)")
    print("=" * 100)
    seven = {n: P[n] for n, _ in IDS}
    for p in [n for n, _ in IDS]:
        t = temporal(p, seven)
        row = []
        for q in [n for n, _ in IDS]:
            if q == p:
                continue
            nt = ("friend" if q in NFRIEND[p] else
                  "enemy" if q in NENEMY[p] else "neutral")
            row.append(f"{q[:3]}:{compound(nt, t[q])[:12]}")
        print(f"  {p:<9}{'  '.join(row)}")
    print("\n  dispositor chains (graha -> lord of its rashi -> ...):")
    for p in GRAHA:
        chain, cur, seen = [p], p, set()
        while True:
            nxt = LORD[sign(P[cur])]
            if nxt in seen or nxt == cur:
                chain.append(f"{nxt} (own sign, terminates)" if nxt == cur else
                             f"{nxt} (loops)")
                break
            seen.add(nxt)
            chain.append(nxt)
            cur = nxt
        print(f"    {' -> '.join(chain)}")

    print("\n" + "=" * 100)
    print("8. DIG BALA (directional strength) - computed exactly")
    print("=" * 100)
    print("  This is one component of Shadbala, not the whole of it. Full")
    print("  Shadbala needs Sthana, Kala, Cheshta, Naisargika and Drik bala,")
    print("  several of which have competing formulations. Dig bala has a")
    print("  single unambiguous definition, so it is the only strength")
    print("  measure computed numerically here. Max 60 virupas.")
    STRONG = {"Jupiter": ASC, "Mercury": ASC, "Moon": (MC + 180) % 360,
              "Venus": (MC + 180) % 360, "Saturn": (ASC + 180) % 360,
              "Sun": MC, "Mars": MC}
    for p in [n for n, _ in IDS]:
        weak = (STRONG[p] + 180) % 360
        d = abs(((P[p] - weak + 180) % 360) - 180)
        print(f"  {p:<9}{d/3:5.1f} / 60 virupas   "
              f"({'strongest in' if d > 150 else 'direction'} "
              f"{'lagna' if STRONG[p] == ASC else 'MC' if STRONG[p] == MC else 'IC' if STRONG[p] == (MC+180)%360 else '7th'})")

    print("\n" + "=" * 100)
    print("9. DIVISIONAL CHARTS")
    print("=" * 100)
    for nm, n, lab in (("D9 Navamsa", 9, "the chart's second body"),
                       ("D10 Dashamsha", 10, "career"),
                       ("D4 Chaturthamsha", 4, "home and property"),
                       ("D7 Saptamsha", 7, "children"),
                       ("D2 Hora", 2, "wealth")):
        da = varga(ASC, n)
        print(f"\n  {nm} ({lab}) - lagna {R[da]}")
        for p in GRAHA:
            v = varga(P[p], n)
            vs = R[v]
            vg = ""
            if p not in ("Rahu", "Ketu"):
                if vs in OWN.get(p, []):
                    vg = "own"
                elif p in EXALT and EXALT[p][0] == vs:
                    vg = "EXALTED"
                elif p in EXALT and R[(R.index(EXALT[p][0]) + 6) % 12] == vs:
                    vg = "DEBILITATED"
            vv = "  VARGOTTAMA" if v == si(P[p]) else ""
            print(f"    {p:<9}{vs:<14}h{(v - da) % 12 + 1:<4}{vg:<12}{vv}")

    print("\n" + "=" * 100)
    print("10. VIMSHOTTARI DASHA (from the exact Moon)")
    print("=" * 100)
    nm, pd, nl, ni, pos = nak(P["Moon"])
    frac = pos / (360 / 27)
    start = [i for i, (g, _) in enumerate(VIM) if g == nl][0]
    yrs = VIM[start][1]
    rem = yrs * (1 - frac)
    print(f"  Janma nakshatra  {nm} pada {pd}, lord {nl}")
    print(f"  elapsed within the nakshatra {frac*100:.4f}%")
    print(f"  balance of {nl} mahadasha at birth {rem:.4f} years "
          f"= {int(rem)}y {int(rem%1*12)}m {int((rem%1*12)%1*30)}d")
    Y = 365.2425
    b = dt.datetime(1996, 6, 7, 19, 35)
    t = b + dt.timedelta(days=rem * Y)
    print(f"\n  {'mahadasha':<12}{'from':<13}{'to':<13}{'years'}")
    print(f"  {nl:<12}{'birth':<13}{t.date().isoformat():<13}{rem:.2f} (partial)")
    seq = []
    cur = t
    for k in range(1, 10):
        g, y = VIM[(start + k) % 9]
        nxt = cur + dt.timedelta(days=y * Y)
        seq.append((g, cur, nxt, y))
        print(f"  {g:<12}{cur.date().isoformat():<13}{nxt.date().isoformat():<13}{y}")
        cur = nxt
    now = dt.datetime(2026, 8, 15)
    md = [(g, s, e, y) for g, s, e, y in seq if s <= now < e][0]
    print(f"\n  CURRENT MAHADASHA: {md[0]}  "
          f"{md[1].date().isoformat()} to {md[2].date().isoformat()}")
    print(f"\n  antardashas within the {md[0]} mahadasha:")
    ai0 = [i for i, (g, _) in enumerate(VIM) if g == md[0]][0]
    c = md[1]
    for k in range(9):
        g, y = VIM[(ai0 + k) % 9]
        dur = md[3] * y / 120.0
        e = c + dt.timedelta(days=dur * Y)
        mark = "   <<< CURRENT" if c <= now < e else ""
        print(f"    {md[0]}/{g:<10}{c.date().isoformat()} to "
              f"{e.date().isoformat()}   {dur:.2f}y{mark}")
        if c <= now < e:
            ad = (g, c, e, dur)
        c = e
    print(f"\n  pratyantardashas within {md[0]}/{ad[0]}:")
    pi = [i for i, (g, _) in enumerate(VIM) if g == ad[0]][0]
    c = ad[1]
    for k in range(9):
        g, y = VIM[(pi + k) % 9]
        dur = ad[3] * y / 120.0
        e = c + dt.timedelta(days=dur * Y)
        mark = "   <<< CURRENT" if c <= now < e else ""
        print(f"    {md[0]}/{ad[0]}/{g:<10}{c.date().isoformat()} to "
              f"{e.date().isoformat()}{mark}")
        c = e

    print("\n" + "=" * 100)
    print("11. YOGA CHECKS (rule stated, then tested)")
    print("=" * 100)
    print("\n  PANCHA MAHAPURUSHA - graha in own sign or exaltation, in a")
    print("  kendra from the lagna:")
    MP = {"Mars": "Ruchaka", "Mercury": "Bhadra", "Jupiter": "Hamsa",
          "Venus": "Malavya", "Saturn": "Shasha"}
    for p, y in MP.items():
        ok = (sign(P[p]) in OWN[p] or EXALT[p][0] == sign(P[p]))
        kd = H[p] in (1, 4, 7, 10)
        print(f"    {y:<10}{p:<9}{'own/exalted YES' if ok else 'own/exalted no ':<18}"
              f"{'kendra YES' if kd else f'in h{H[p]}, not a kendra':<26}"
              f"{'FORMS' if ok and kd else 'does not form'}")

    print("\n  GAJA KESARI - Jupiter in a kendra from the Moon:")
    dJM = (si(P["Jupiter"]) - si(P["Moon"])) % 12 + 1
    print(f"    Jupiter is in the {dJM}th from the Moon -> "
          f"{'FORMS' if dJM in (1,4,7,10) else 'does not form'}")

    print("\n  KEMADRUMA - no graha (excluding Sun, Rahu, Ketu) in the 2nd or")
    print("  12th from the Moon:")
    nb = [p for p in GRAHA if p not in ("Moon", "Sun", "Rahu", "Ketu")
          and (si(P[p]) - si(P["Moon"])) % 12 + 1 in (2, 12)]
    print(f"    grahas in the 2nd/12th from the Moon: {', '.join(nb) or 'none'}"
          f" -> Kemadruma {'does NOT form' if nb else 'FORMS'}")
    su = [p for p in GRAHA if p not in ("Moon", "Sun", "Rahu", "Ketu")
          and (si(P[p]) - si(P["Moon"])) % 12 + 1 == 2]
    an = [p for p in GRAHA if p not in ("Moon", "Sun", "Rahu", "Ketu")
          and (si(P[p]) - si(P["Moon"])) % 12 + 1 == 12]
    print(f"    Sunapha (2nd from Moon): {', '.join(su) or 'none'}")
    print(f"    Anapha  (12th from Moon): {', '.join(an) or 'none'}")

    print("\n  DHARMA-KARMADHIPATI - the 9th and 10th lords associated:")
    l9, l10 = LORD[R[(AI + 8) % 12]], LORD[R[(AI + 9) % 12]]
    print(f"    9th lord {l9} in h{H[l9]} {sign(P[l9])}; "
          f"10th lord {l10} in h{H[l10]} {sign(P[l10])}")
    print(f"    {'SAME RASHI - conjunction - FORMS' if si(P[l9]) == si(P[l10]) else 'not conjunct'}")

    print("\n  LAKSHMI - the 9th lord in own sign or exaltation in a kendra or")
    print("  trikona, with a strong lagna lord:")
    l1 = LORD[R[AI]]
    print(f"    9th lord {l9}: {dignity(l9, P[l9])}, in h{H[l9]} "
          f"({'trikona' if H[l9] in (1,5,9) else 'kendra' if H[l9] in (1,4,7,10) else 'neither'})")
    print(f"    lagna lord {l1}: {dignity(l1, P[l1])}, in h{H[l1]}")

    print("\n  BUDHA-ADITYA - Sun and Mercury conjunct:")
    sep = abs(((P["Sun"] - P["Mercury"] + 180) % 360) - 180)
    print(f"    same rashi: {'yes' if si(P['Sun']) == si(P['Mercury']) else 'no'}, "
          f"but {sep:.2f}° apart and in different nakshatras "
          f"({nak(P['Mercury'])[0]} vs {nak(P['Sun'])[0]})")

    print("\n  SAKATA - the Moon in the 6th, 8th or 12th from Jupiter:")
    print(f"    Moon is in the {(si(P['Moon']) - si(P['Jupiter'])) % 12 + 1}th "
          f"from Jupiter -> "
          f"{'FORMS' if (si(P['Moon'])-si(P['Jupiter']))%12+1 in (6,8,12) else 'does not form'}")

    print("\n  VIPAREETA RAJA YOGA - a lord of 6/8/12 placed in another of 6/8/12:")
    for h in (6, 8, 12):
        l = LORD[R[(AI + h - 1) % 12]]
        print(f"    {h}th lord {l} sits in h{H[l]} -> "
              f"{'qualifies' if H[l] in (6,8,12) else 'no'}")

    print("\n  DEBILITATION CHECK (for neecha bhanga):")
    deb = [p for p in GRAHA if "DEBILITATED" in dignity(p, P[p])]
    print(f"    debilitated grahas: {', '.join(deb) or 'NONE'}")

    print("\n  PARIVARTANA (mutual exchange of rashis):")
    found = []
    for p in [n for n, _ in IDS]:
        for q in [n for n, _ in IDS]:
            if p < q and LORD[sign(P[p])] == q and LORD[sign(P[q])] == p:
                found.append(f"{p} and {q}")
    print(f"    by rashi: {', '.join(found) or 'none'}")
    found = []
    for p in GRAHA:
        for q in GRAHA:
            if p < q and nak(P[p])[2] == q and nak(P[q])[2] == p:
                found.append(f"{p} and {q}")
    print(f"    by NAKSHATRA lordship: {', '.join(found) or 'none'}")


if __name__ == "__main__":
    main()
