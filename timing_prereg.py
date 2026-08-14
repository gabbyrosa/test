#!/usr/bin/env python3
"""
PRE-REGISTERED timing tables for the out-of-sample event test.

Computed and committed BEFORE any life events are supplied. The git commit
is the timestamp. Nothing here may be adjusted after seeing the data, and
any later edit will show in the history.

TECHNIQUE: annual profections only.

Why only profections. Zodiacal releasing is the other core Hellenistic
timing technique and it would discriminate here, since the Lot of Fortune
falls in Cancer tropical and Gemini sidereal. But I cannot implement the
loosing of the bond to the standard this project has been held to, and a
wrong implementation would invalidate the test rather than fail it.
Omitted rather than guessed. Releasing from Spirit would not discriminate
in any case: Spirit falls in Capricorn under both zodiacs.

--------------------------------------------------------------------------
THE STRUCTURAL FACT THAT DEFINES WHAT THIS TEST CAN AND CANNOT MEASURE
--------------------------------------------------------------------------

Whole-sign profection assigns the year to house (age mod 12) + 1. That is
arithmetic on the age. It does not depend on the zodiac. So:

  THE PROFECTED HOUSE IS IDENTICAL UNDER BOTH ZODIACS AT EVERY AGE.
  The topic of the year is therefore NOT a discriminator. Age 7 is a
  7th-house year tropical and a 7th-house year sidereal. Both predict
  partnership. That prediction can be right or wrong, but it cannot
  separate the two zodiacs.

Everything discriminating comes from the LORD of the profected place:

  1. WHICH PLANET rules the year. Tropical Ascendant Libra, sidereal Virgo,
     so the sidereal profected sign is one behind and the lord usually
     differs. Age 0 is a Venus year tropical, a Mercury year sidereal.

  2. WHERE THAT LORD SITS NATALLY. This is the sharp one. Only two planets
     change house between the zodiacs: Mercury and Mars, both 8th tropical
     and 9th sidereal. Sun, Venus (9th), Moon (6th), Jupiter (4th) and
     Saturn (7th) are in the same house in both.

     So the concrete empirical question this test asks is, repeatedly:
     did that year read as an 8th-house year (debt, others' money, crisis,
     mortality) or a 9th-house year (long travel, foreign, higher study)?

  3. THE CONDITION of that lord. See the declared confound below.

--------------------------------------------------------------------------
CONFOUNDS DECLARED IN ADVANCE
--------------------------------------------------------------------------

CONFOUND 1 — the condition axis is structurally biased and will NOT be
counted toward the verdict.
  The sidereal chart has two domiciles (Venus, Jupiter); the tropical chart
  has none, and holds all three debilities (Jupiter fall, Saturn fall, Mars
  detriment). Every DOMICILE year in the table below is sidereal and every
  FALL year is tropical. So "good year" evidence can only ever favour
  sidereal and "bad year" evidence can only ever favour tropical,
  regardless of what actually happened. That is a property of the charts,
  not of her life. It is reported for completeness and excluded from
  scoring. Declared now so it cannot be quietly used later.

CONFOUND 2 — the two zodiacs do not make equally risky predictions.
  Sidereal puts Sun, Venus, Mercury and Mars all in the 9th, so it names
  the 9th house as the lord's seat in 7 of every 12 years. Tropical spreads
  its lords across the 9th, 8th, 4th, 7th and 6th. Sidereal is therefore
  making a narrower and more falsifiable claim, and a broad 9th-house life
  would confirm it cheaply while a life with no 9th-house character would
  damage it heavily. Noted now so neither outcome gets reinterpreted after
  the fact.

--------------------------------------------------------------------------
SCORING, FIXED NOW, BEFORE ANY EVENT IS KNOWN
--------------------------------------------------------------------------

For each dated event, score the LORD OF THE YEAR independently under each
zodiac, on the lord's natal house:

  HIT      the lord's natal house is the standard significator of the
           event's topic
  PARTIAL  the lord's natal house is a secondary significator of the topic
  MISS     neither

Also record, separately and without scoring, whether the lord's planetary
nature fits (Venus year for a relationship, Mercury year for a study or
commercial matter, and so on). This is weaker evidence and is kept apart.

EXCLUSIONS, decided now:
  - Events in a year flagged NOT DISCRIMINATING below are excluded from the
    verdict, because both zodiacs make the same prediction.
  - Events within 14 days of a 7 June profection boundary are marked
    ambiguous and excluded, since the boundary is the solar return and an
    event's onset is rarely dated that precisely.
  - Events whose topic maps to more than one house are marked ambiguous and
    excluded. The decision to exclude is made when the event is read, not
    after seeing which zodiac it would favour.

WHAT COUNTS AS A RESULT:
  A zodiac wins only if it takes clearly more HITs across the discriminating
  events. If the two come out close, the correct conclusion is that
  profections do not discriminate between them on this evidence, and I will
  say that rather than declaring a narrow winner.

--------------------------------------------------------------------------
TOPIC-TO-HOUSE ASSIGNMENTS, FIXED NOW
--------------------------------------------------------------------------
   1  body, health, self-presentation, identity change
   2  income, earnings, possessions
   3  siblings, short travel, local moves, study
   4  home, moving house, property, parents, endings
   5  children, pregnancy, creative output, romance begun in pleasure
   6  illness, injury, work conditions, subordinate labour
   7  marriage, partnership begun or ended, open conflict
   8  debt, inheritance, others' money, crisis, mortality
   9  long travel, relocation abroad, higher study, worldview change
  10  career action, public standing, promotion, reputation
  11  friends, groups, patrons, benefits received
  12  retreat, loss, hidden matters, confinement, undoing
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
TOPIC = {1: "body, identity", 2: "income, possessions",
         3: "siblings, short travel, study", 4: "home, property, parents",
         5: "children, creativity, pleasure", 6: "illness, work conditions",
         7: "partnership, open conflict", 8: "debt, others' money, crisis",
         9: "long travel, foreign, higher study", 10: "career, public standing",
         11: "friends, patrons, benefits", 12: "retreat, loss, hidden matters"}


def sg(x):
    return S[int((x % 360) // 30)]


def cond(b, P):
    s = sg(P[b])
    o = []
    if DOM[s] == b:
        o.append("DOMICILE")
    if EX.get(b) == s:
        o.append("exalt")
    if DOM[S[(S.index(s) + 6) % 12]] == b:
        o.append("DETRIMENT")
    if b in EX and S[(S.index(EX[b]) + 6) % 12] == s:
        o.append("FALL")
    d, n, pt = TRIP[ELEM[s]]
    if b == d:
        o.append("trip")
    elif b == pt:
        o.append("trip(p)")
    return ", ".join(o) or "peregrine"


def main():
    P = {n: swe.calc_ut(JD, s, FL)[0][0] for n, s in IDS}
    SI = {n: (v - AY) % 360 for n, v in P.items()}
    cusp, am = swe.houses(JD, 40.4406, -79.9959, b"P")
    TA, SA = am[0], (am[0] - AY) % 360
    TI, SIa = S.index(sg(TA)), S.index(sg(SA))
    TH = {b: ((S.index(sg(P[b])) - TI) % 12) + 1 for b in T7}
    SH = {b: ((S.index(sg(SI[b])) - SIa) % 12) + 1 for b in T7}

    print("PRE-REGISTERED PROFECTION TABLE")
    print("computed and committed before any event date is supplied\n")
    print(f"  tropical Ascendant {sg(TA)}      sidereal Ascendant {sg(SA)}")
    print("  the profected HOUSE is the same in both; the LORD is what differs\n")

    print("  natal house of each planet, the source of all discrimination:")
    print(f"    {'planet':<10}{'tropical':<12}{'sidereal':<12}")
    for b in T7:
        flag = "  <-- differs" if TH[b] != SH[b] else ""
        print(f"    {b:<10}h{TH[b]:<11}h{SH[b]:<11}{flag}")
    print("    only Mercury and Mars move between the zodiacs: 8th vs 9th\n")

    print("=" * 108)
    print("  THE PREDICTIONS. For each year the lord of the year, its natal")
    print("  house, and the topic that house predicts.")
    print("=" * 108)
    print(f"  {'age':<4}{'year':<12}{'h':<4}"
          f"{'TROPICAL lord / house / prediction':<46}"
          f"{'SIDEREAL lord / house / prediction':<46}")
    disc = []
    for age in range(0, 35):
        y0, y1 = 1996 + age, 1997 + age
        h = (age % 12) + 1
        tl = DOM[S[(TI + age) % 12]]
        sl = DOM[S[(SIa + age) % 12]]
        th, sh = TH[tl], SH[sl]
        t = f"{tl:<8}h{th:<3}{TOPIC[th]:<34}"
        s = f"{sl:<8}h{sh:<3}{TOPIC[sh]:<34}"
        if th != sh:
            mark = "DISCRIMINATING"
            disc.append(age)
        elif tl != sl:
            mark = "lord differs, house same"
        else:
            mark = "NOT DISCRIMINATING"
        print(f"  {age:<4}{str(y0) + '-' + str(y1)[2:]:<12}{h:<4}{t}{s}")
        print(f"  {'':<20}{mark}")

    print("\n" + "=" * 108)
    print("  SUMMARY OF DISCRIMINATING POWER")
    print("=" * 108)
    strong = [a for a in range(12) if TH[DOM[S[(TI + a) % 12]]] != SH[DOM[S[(SIa + a) % 12]]]]
    weak = [a for a in range(12)
            if TH[DOM[S[(TI + a) % 12]]] == SH[DOM[S[(SIa + a) % 12]]]
            and DOM[S[(TI + a) % 12]] != DOM[S[(SIa + a) % 12]]]
    none = [a for a in range(12) if DOM[S[(TI + a) % 12]] == DOM[S[(SIa + a) % 12]]]
    print(f"    ages where the predicted house DIFFERS (usable): "
          f"{', '.join(str(a) for a in strong)}  and +12, +24")
    print(f"    ages where only the lord's identity differs (weak): "
          f"{', '.join(str(a) for a in weak)}  and +12, +24")
    print(f"    ages where the two zodiacs agree entirely (excluded): "
          f"{', '.join(str(a) for a in none)}  and +12, +24")
    print(f"\n    {len(strong)} of every 12 years carry a usable prediction.")

    print("\n  CONFOUND 1, reported and NOT scored — the condition axis.")
    print("  Every domicile below is sidereal and every fall is tropical, so")
    print("  this axis cannot produce evidence against sidereal in a good year")
    print("  or against tropical in a bad one. Excluded from the verdict.")
    for age in range(0, 12):
        tl = DOM[S[(TI + age) % 12]]
        sl = DOM[S[(SIa + age) % 12]]
        tc, sc = cond(tl, P), cond(sl, SI)
        tbad = "FALL" in tc or "DETRIMENT" in tc
        sbad = "FALL" in sc or "DETRIMENT" in sc
        if (tbad and "DOMICILE" in sc) or ("DOMICILE" in tc and sbad):
            print(f"    age {age:<3}(and {age+12}, {age+24})   "
                  f"tropical {tl} {tc:<22} sidereal {sl} {sc}")

    print("\n  CONFOUND 2, declared — how concentrated each zodiac's claim is.")
    for lab, H, I in (("tropical", TH, TI), ("sidereal", SH, SIa)):
        c = {}
        for age in range(12):
            hh = H[DOM[S[(I + age) % 12]]]
            c[hh] = c.get(hh, 0) + 1
        sp = ", ".join(f"h{k} in {v}/12 years" for k, v in sorted(c.items()))
        print(f"    {lab:<10}{sp}")
    print("    sidereal makes the narrower and more falsifiable claim.")


if __name__ == "__main__":
    main()
