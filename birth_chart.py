#!/usr/bin/env python3
"""
Print the natal chart and write a Markdown report.

Usage: python3 birth_chart.py
"""

import natal
from natal import fmt


def build_report(data):
    b = data["birth"]
    p = data["planets"]
    lines = []
    add = lines.append

    add(f"# Natal Chart")
    add("")
    add(f"**{b['date_label']} · {b['time_label']} · {b['place_label']}**")
    add("")
    add("Tropical zodiac · Placidus houses · Swiss Ephemeris "
        f"(Julian Day UT {data['jd']:.5f})")
    add("")

    add("## The Big Three")
    add("")
    add(f"- **Sun** in **{p['Sun']['sign']}** ({fmt(p['Sun']['lon'])}), "
        f"house {p['Sun']['house']} (Placidus) / {p['Sun']['house_ws']} (whole sign)")
    add(f"- **Moon** in **{p['Moon']['sign']}** ({fmt(p['Moon']['lon'])}), "
        f"house {p['Moon']['house']} (Placidus) / {p['Moon']['house_ws']} (whole sign)")
    add(f"- **Ascendant** in **{data['asc_sign']}** ({fmt(data['asc'])})")
    add("")

    add("## Planets & Points")
    add("")
    add("House columns show Placidus / whole sign.")
    add("")
    add("| Body | Position | House (Placidus) | House (Whole sign) | Motion |")
    add("| --- | --- | --- | --- | --- |")
    for label in data["order"] + ["South Node"]:
        d = p[label]
        motion = "Retrograde" if d["retro"] else "Direct"
        if label in ("North Node", "South Node"):
            motion = "n/a"
        add(f"| {d['glyph']} {label} | {fmt(d['lon'])} | "
            f"{d['house']} | {d['house_ws']} | {motion} |")
    add("")

    add("## Angles")
    add("")
    add(f"- **Ascendant (AC):** {fmt(data['asc'])}")
    add(f"- **Midheaven (MC):** {fmt(data['mc'])}")
    add(f"- **Descendant (DC):** {fmt((data['asc'] + 180) % 360)}")
    add(f"- **Imum Coeli (IC):** {fmt((data['mc'] + 180) % 360)}")
    add("")

    add("## House Cusps (Placidus)")
    add("")
    for i, c in enumerate(data["cusps"]):
        add(f"- **House {i + 1}:** {fmt(c)}")
    add("")

    add("## Major Aspects")
    add("")
    for a in data["aspects"]:
        add(f"- {a['a']} **{a['type']}** {a['b']} (orb {a['orb']}°)")
    add("")

    return "\n".join(lines)


def main():
    data = natal.compute()
    report = build_report(data)

    with open("birth_chart_report.md", "w") as f:
        f.write(report + "\n")

    # Console view
    print(report)
    print("\nWrote birth_chart_report.md")


if __name__ == "__main__":
    main()
