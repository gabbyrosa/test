#!/usr/bin/env python3
"""
Scoring pass for the out-of-sample timing test.

Imports the prediction tables directly from timing_prereg.py so the
predictions scored here are provably the ones committed before any date was
supplied. Nothing in the rubric is redefined in this file.

EVENTS AS SUPPLIED, verbatim, before any astrology was applied:
  "Wed, May 6, 2020, 8:44 PM"                          -- purpose not stated
  "i was offered a full time position at my current
   role mid july of this year"                          -- this year = 2026
  "i got a raise"                                       -- no date given
  "i went on a first date with my current boyfriend
   of 5 years april 1 2021"
  "i got hit by a car mid aug 2016"
  "oct 8 2023 i moved into my boyfriends house where
   i still live"

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
    ("unlabelled event", dt.date(2020, 5, 6), None, None,
     "NO DESCRIPTION SUPPLIED - cannot be assigned a topic, cannot be scored"),
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
    ("moved into partner's house", dt.date(2023, 10, 8), ([4], [7]), ([7], [4]),
     "h4 'home, moving house, property'; h7 'partnership begun'"),
    ("offered full-time position, plus a raise", dt.date(2026, 7, 15),
     ([10], [6, 2]), ([2], [10, 6]),
     "h10 'career action, promotion'; h6 'work conditions'; h2 'income'"),
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
    shared = {"HIT": 0, "PARTIAL": 0, "MISS": 0}
    used, dropped = [], []

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
            shared[sc] += 1
            used.append(name)
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


if __name__ == "__main__":
    main()
