#!/usr/bin/env python3
"""
Scoring pass for the out-of-sample timing test.

Imports the prediction tables directly from timing_prereg.py so the
predictions scored here are provably the ones committed before any date was
supplied. Nothing in the rubric is redefined in this file.

EVENTS AS SUPPLIED, verbatim, before any astrology was applied:
  "Wed, May 6, 2020, 8:44 PM / i was offered a full time position at my
   current role / mid july of this year i got a raise / i went on a first
   date with my current boyfriend of 5 years april 1 2021 / um i got hit by
   a car mid aug 2016"
  "oct 8 2023 i moved into my boyfriends house where i still live"
  "mRCH 2019 I started working part time at anthropology"

PARSING CORRECTION. The first message was dictated as one run-on line and I
split it wrongly on the first pass: I read the 6 May 2020 timestamp as an
unlabelled event and attached the job offer to "mid july of this year". She
corrected it. The timestamp belongs to the job offer; "mid july of this
year" belongs to the raise. This moves the job offer from age 30 to age 23,
which changes its prediction under both zodiacs, so the earlier scoring of
that event is void and is replaced here.

TOPIC ASSIGNMENT. Each event is mapped to houses using ONLY the twelve
entries pre-registered in timing_prereg.py, quoted alongside each assignment.

RANKING SENSITIVITY. The pre-registration says events whose topic maps to
more than one house are ambiguous and excluded, and that the decision is
made when the event is read rather than after seeing who it favours. To make
that auditable rather than a matter of my word, every event that admits a
defensible alternative ranking of its houses is scored BOTH WAYS below. If
the two rankings disagree about which zodiac did better, the event is
excluded automatically, whichever way it happened to fall.
"""

import datetime as dt
from timing_prereg import S, DOM, TOPIC, cond, sg, IDS, T7, AY, JD, FL
import swisseph as swe

# name, date, (primary, secondary), alternative (primary, secondary) or None,
# justification quoted from the pre-registered topic map
EVENTS = [
    # Confirmed: she moved out of the parental home to attend, and took on NO
    # student loans. So h4 'moving house' is genuinely touched and h8 'debt'
    # is genuinely NOT. Scored as one episode rather than two events, because
    # the move was caused by the enrolment, unlike the age-22 pair which were
    # independent activities that merely coincided. Scored both ways below.
    ("started at Kent State, moving out of parents' house", dt.date(2014, 8, 25),
     ([9], [3, 4]), ([4], [9, 3]),
     "h9 'higher study'; h4 'moving house, parents'; h3 'study'"),
    ("transferred to Ohio State University", dt.date(2015, 9, 20), ([9], [3]), ([3], [9]),
     "h9 'higher study, worldview change'; h3 'study'"),
    ("hit by a car", dt.date(2016, 8, 15), ([6], [8, 1]), ([8], [6, 1]),
     "h6 'illness, injury'; h8 'crisis, mortality'; h1 'body'"),
    ("first date with current partner", dt.date(2021, 4, 1), ([7], [5]), ([5], [7]),
     "h7 'partnership begun'; h5 'romance begun in pleasure'"),
    # Read as Anthropologie the retailer, on "working part time AT". If it
    # were instead an anthropology programme the topic becomes h9 'higher
    # study' and the result flips to favour tropical. Flagged to her.
    ("started part-time work at Anthropologie", dt.date(2019, 3, 15),
     ([6], [10, 2]), ([10], [6, 2]),
     "h6 'work conditions, subordinate labour'; h10 'career action'; h2 'income'"),
    # Concurrent with the retail job, per "part time while i was getting my
    # yoga teacher training certification". Exact start and end unknown, so
    # it may also extend into the age-23 year. What is certain is that it
    # was under way in March 2019, inside the age-22 year.
    ("yoga teacher training certification", dt.date(2019, 3, 15),
     ([9], [3]), ([3], [9]),
     "h9 'higher study, worldview change'; h3 'study'"),
    ("moved into partner's house", dt.date(2023, 10, 8), ([4], [7]), ([7], [4]),
     "h4 'home, moving house, property'; h7 'partnership begun'"),
    ("offered full-time position at current role", dt.date(2020, 5, 6),
     ([10], [6, 2]), ([6], [10, 2]),
     "h10 'career action, promotion'; h6 'work conditions'; h2 'income'"),
    ("got a raise", dt.date(2026, 7, 15), ([2], [10, 6]), ([10], [2, 6]),
     "h2 'income, earnings'; h10 'career action'; h6 'work conditions'"),
]


def prof_age(d):
    return d.year - 1996 if (d.month, d.day) >= (6, 7) else d.year - 1997


def days_from_boundary(d):
    a = prof_age(d)
    return min(abs((d - dt.date(1996 + a, 6, 7)).days),
               abs((d - dt.date(1997 + a, 6, 7)).days))


RANK = {"HIT": 2, "PARTIAL": 1, "MISS": 0}


def score(house, rank):
    if rank is None:
        return "UNSCORABLE"
    pri, sec = rank
    return "HIT" if house in pri else "PARTIAL" if house in sec else "MISS"


def main():
    P = {n: swe.calc_ut(JD, s, FL)[0][0] for n, s in IDS}
    SI = {n: (v - AY) % 360 for n, v in P.items()}
    cusp, am = swe.houses(JD, 40.4406, -79.9959, b"P")
    TI, SIa = S.index(sg(am[0])), S.index(sg((am[0] - AY) % 360))
    TH = {b: ((S.index(sg(P[b])) - TI) % 12) + 1 for b in T7}
    SH = {b: ((S.index(sg(SI[b])) - SIa) % 12) + 1 for b in T7}

    tt = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    st = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    used, dropped, rows = [], [], []

    for name, d, rank, alt, why in EVENTS:
        a = prof_age(d)
        ph = (a % 12) + 1
        tl, sl = DOM[S[(TI + a) % 12]], DOM[S[(SIa + a) % 12]]
        th, sh = TH[tl], SH[sl]
        print("=" * 96)
        print(f"{name.upper()}   {d.isoformat()}")
        print("=" * 96)
        print(f"  profection year age {a}: 7 Jun {1996+a} to 6 Jun {1997+a}")
        b = days_from_boundary(d)
        print(f"  {b} days from a profection boundary -> "
              f"{'EXCLUDED, inside the 14-day window' if b <= 14 else 'usable'}")
        print(f"  topic from the pre-registered map: {why}")

        print(f"\n  SHARED LAYER, identical in both zodiacs, NOT evidence about the zodiac:")
        sc = score(ph, rank)
        print(f"    profected house h{ph}: {TOPIC[ph]:<38} {sc}")

        print(f"\n  THE DISCRIMINATOR, lord of the year:")
        s1, s2 = score(th, rank), score(sh, rank)
        print(f"    tropical  {tl:<8} natal h{th:<3} {TOPIC[th]:<38} {s1}")
        print(f"    sidereal  {sl:<8} natal h{sh:<3} {TOPIC[sh]:<38} {s2}")

        verdict = None
        if rank is None:
            verdict = "UNSCORABLE - no event description supplied"
        elif b <= 14:
            verdict = "EXCLUDED - inside the boundary window"
        elif th == sh:
            verdict = "EXCLUDED - both zodiacs predict the same house"
        elif alt is not None:
            a1, a2 = score(th, alt), score(sh, alt)
            lead = RANK[s1] - RANK[s2]
            altlead = RANK[a1] - RANK[a2]
            print(f"\n  alternative ranking ({alt[0][0]} primary instead of {rank[0][0]}):")
            print(f"    tropical {a1}, sidereal {a2}")
            if (lead > 0) != (altlead > 0) or (lead < 0) != (altlead < 0):
                verdict = ("EXCLUDED - ranking-sensitive. The two defensible "
                           "readings disagree\n             about which zodiac "
                           "did better, so the result would be my\n             "
                           "choice of ranking rather than the astrology.")
            else:
                print("    same direction under both rankings, so the result is "
                      "not an artefact of ranking")

        if verdict:
            print(f"\n  >> {verdict}")
            dropped.append(name)
        else:
            tt[s1] += 1
            st[s2] += 1
            used.append(name)
            rows.append((a, name, s1, s2, score(th, (rank[0], [])),
                         score(sh, (rank[0], []))))
            print(f"\n  >> COUNTED")

        print(f"\n  recorded, NOT scored - nature of the lord: "
              f"tropical {tl} vs sidereal {sl}")
        print(f"  recorded, NOT scored - condition (confound 1): "
              f"tropical {tl} {cond(tl, P)} vs sidereal {sl} {cond(sl, SI)}")
        print()

    print("=" * 96)
    print("VERDICT")
    print("=" * 96)
    print(f"  events supplied            {len(EVENTS)}")
    print(f"  counted                    {len(used)}  ({', '.join(used) or 'none'})")
    print(f"  excluded                   {len(dropped)}  ({', '.join(dropped) or 'none'})")
    print()
    for lab, t in (("tropical", tt), ("sidereal", st)):
        print(f"    {lab:<10}{t['HIT']} hit, {t['PARTIAL']} partial, {t['MISS']} miss")
    print(f"\n  the shared layer, which says nothing about the zodiac but does")
    print(f"  say something about profections as a technique, across ALL events")
    print(f"  that had a description and fell outside the boundary window:")
    tot = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    for name, d, rank, alt, why in EVENTS:
        if rank is None or days_from_boundary(d) <= 14:
            continue
        tot[score((prof_age(d) % 12) + 1, rank)] += 1
    print(f"    profected house  {tot['HIT']} hit, {tot['PARTIAL']} partial, "
          f"{tot['MISS']} miss")

    print("\n" + "=" * 96)
    print("ROBUSTNESS CHECKS")
    print("  Reported alongside the pre-registered tally above, not instead of")
    print("  it. Both were forced into view by the data rather than planned.")
    print("=" * 96)

    print("\n  CHECK A - years that contain events pointing BOTH ways.")
    print("  The pre-registration scores events, not years, and did not")
    print("  anticipate one profection year producing an event that fits each")
    print("  zodiac. A year like that discriminates nothing: both predicted")
    print("  houses had real content in her life. Tally with such years dropped:")
    by_age = {}
    for a, name, s1, s2, _, _ in rows:
        by_age.setdefault(a, []).append((name, s1, s2))
    bad = set()
    for a, evs in by_age.items():
        tw = any(RANK[x] > RANK[y] for _, x, y in evs)
        sw = any(RANK[y] > RANK[x] for _, x, y in evs)
        if tw and sw:
            bad.add(a)
            print(f"    age {a} contradicts itself: "
                  + "; ".join(f"{n} (T {x}, S {y})" for n, x, y in evs))
    if not bad:
        print("    none")
    ta = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    sa = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    for a, name, s1, s2, _, _ in rows:
        if a not in bad:
            ta[s1] += 1
            sa[s2] += 1
    print(f"    tropical  {ta['HIT']} hit, {ta['PARTIAL']} partial, {ta['MISS']} miss")
    print(f"    sidereal  {sa['HIT']} hit, {sa['PARTIAL']} partial, {sa['MISS']} miss")

    print("\n  CHECK B - strict scoring, exact primary matches only, no partial")
    print("  credit. Tests whether the result rests on secondary significators:")
    tb = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    sb = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    for a, name, _, _, x, y in rows:
        tb[x] += 1
        sb[y] += 1
    print(f"    tropical  {tb['HIT']} hit, {tb['MISS']} miss")
    print(f"    sidereal  {sb['HIT']} hit, {sb['MISS']} miss")


if __name__ == "__main__":
    main()
