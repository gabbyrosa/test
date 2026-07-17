#!/usr/bin/env python3
"""
Re-weight the EXISTING raw relocation grades (city_analysis.json) into four
priority-specific rankings. No chart is recalculated here.

Also runs a Whole Sign sensitivity check on the shortlist: angularity (orbs to
the real ASC/MC/DC/IC) is house-system independent and is left untouched; only
the house-placement and house-ruler inputs are recomputed under Whole Sign,
fed back through the identical rubric, and compared.
"""

import json
import city_analysis as ca
import natal

DATA = json.load(open("city_analysis.json", encoding="utf-8"))
D = natal.compute()
SIGNS = natal.SIGNS
SIGN_IDX = {n: D["planets"][n]["sign_idx"] for n in ca.PLANETS}

BASE = ["home", "relationships", "career", "identity",
        "emotional_ease", "creativity", "stability"]

WEIGHTS = {
    "Residential life": {"home": .30, "emotional_ease": .20, "stability": .20,
                         "relationships": .15, "identity": .10, "career": .05},
    "Overall balance": {k: 1 / 7 for k in BASE},
    "Relationships & belonging": {"relationships": .35, "emotional_ease": .20,
                                  "identity": .15, "creativity": .15,
                                  "stability": .10, "home": .05},
    "Career & building": {"career": .30, "home": .25, "identity": .15,
                          "stability": .15, "creativity": .10,
                          "relationships": .05},
}


def composite(grades, w):
    return round(sum(grades[k] * wt for k, wt in w.items()), 3)


def rankings():
    out = {}
    for cat, w in WEIGHTS.items():
        out[cat] = sorted(((c, composite(v["grades"], w)) for c, v in DATA.items()),
                          key=lambda t: t[1], reverse=True)
    return out


def breakdown(cat, cities):
    w = WEIGHTS[cat]
    print(f"\n[{cat}] weighted contribution breakdown")
    hdr = "city".ljust(16) + "".join(f"{k[:4]:>7}" for k in w) + "   TOTAL"
    print(hdr)
    for c in cities:
        g = DATA[c]["grades"]
        parts = "".join(f"{g[k] * wt:>7.2f}" for k, wt in w.items())
        print(f"{c:<16}{parts}   {composite(g, w):.3f}")
    print("weights:        " + "".join(f"{wt:>7.2f}" for wt in w.values()))


def ws_regrade(city):
    raw = DATA[city]["raw"]
    asc_idx = SIGNS.index(raw["asc_sign"])

    def wsh(sign_idx):
        return ((sign_idx - asc_idx) % 12) + 1

    planets = {n: {"lon": raw["planets"][n]["lon"],
                   "orbs": raw["planets"][n]["orbs"],
                   "house": wsh(SIGN_IDX[n])} for n in ca.PLANETS}

    def wsruler(h):
        sign = SIGNS[(asc_idx + h - 1) % 12]
        r = ca.RULER[sign]
        return {"cusp_sign": sign, "ruler": r, "ruler_house": wsh(SIGN_IDX[r]),
                "ruler_sign": D["planets"][r]["sign"]}

    cr = ca.RULER[raw["asc_sign"]]
    rf = {"asc": raw["asc"], "asc_sign": raw["asc_sign"], "mc": raw["mc"],
          "mc_sign": raw["mc_sign"], "chart_ruler": cr,
          "chart_ruler_house": wsh(SIGN_IDX[cr]),
          "chart_ruler_sign": D["planets"][cr]["sign"],
          "rulers": {"4": wsruler(4), "7": wsruler(7), "10": wsruler(10)},
          "planets": planets}
    dims, _, _ = ca.grade(rf)
    return dims


def main():
    ranks = rankings()
    for cat, r in ranks.items():
        print(f"\n=== {cat} ===")
        for c, sc in r[:12]:
            print(f"  {c:<16} {sc:.3f}")

    breakdown("Overall balance", ["Marseille", "Tucson"])
    breakdown("Residential life", ["Marseille", "Tucson"])

    # shortlist = top 10 by overall balance, for the Whole Sign check
    shortlist = [c for c, _ in ranks["Overall balance"][:10]]
    print("\n=== WHOLE SIGN SENSITIVITY (shortlist) ===")
    print("Placidus vs Whole Sign composite per category; flag |delta| >= 0.3")
    for c in shortlist:
        wsg = ws_regrade(c)
        line = [f"\n{c} ({DATA[c]['raw']['asc_sign']} rising)"]
        for cat, w in WEIGHTS.items():
            p = composite(DATA[c]["grades"], w)
            wsc = composite(wsg, w)
            flag = "  <-- FLAG" if abs(wsc - p) >= 0.3 else ""
            line.append(f"  {cat:<26} P {p:.2f}  WS {wsc:.2f}  d {wsc - p:+.2f}{flag}")
        print("\n".join(line))
        # house shifts for key planets
        raw = DATA[c]["raw"]
        asc_idx = SIGNS.index(raw["asc_sign"])
        shifts = []
        for n in ["Sun", "Moon", "Venus", "Mars", "Jupiter", "Saturn"]:
            ph = raw["planets"][n]["house"]
            wh = ((SIGN_IDX[n] - asc_idx) % 12) + 1
            if ph != wh:
                shifts.append(f"{n} P{ph}->WS{wh}")
        if shifts:
            print("   house shifts: " + ", ".join(shifts))


if __name__ == "__main__":
    main()
