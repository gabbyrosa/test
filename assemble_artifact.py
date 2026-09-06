#!/usr/bin/env python3
"""
Assemble the self-contained birth_chart.html artifact:
compute the chart, render the wheel, inline the fonts, and fill the template.

Fonts are expected as woff2 files in ./fonts/ (cormorant600, ebg400, ebg500).
Writes birth_chart.html.
"""

import base64
import os

import natal
import build_chart_wheel
import astrocartography
from natal import fmt

FONT_DIR = "fonts"
FONTS = {
    "%%CORMORANT%%": "cormorant600.woff2",
    "%%EBG400%%": "ebg400.woff2",
    "%%EBG500%%": "ebg500.woff2",
}


def b64_font(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def placements_rows(data):
    p = data["planets"]
    rows = []
    for label in data["order"] + ["South Node"]:
        d = p[label]
        if label in ("North Node", "South Node"):
            motion = '<span style="color:var(--muted)">node</span>'
        elif d["retro"]:
            motion = 'Retrograde <span class="rx">℞</span>'
        else:
            motion = "Direct"
        dot = (f'<span class="dot" style="background:var(--{d["element"]})">'
               f'</span>')
        rows.append(
            f'<tr>'
            f'<td><span class="pglyph">{d["glyph"]}\ufe0e</span>{label}</td>'
            f'<td class="pos"><span class="elem-tag">{dot}'
            f'{d["deg"]}°{d["min"]:02d}&#39; {d["sign"]}</span></td>'
            f'<td class="house">{d["house"]}</td>'
            f'<td class="house">{d["house_ws"]}</td>'
            f'<td>{motion}</td>'
            f'</tr>'
        )
    return "\n          ".join(rows)


def acg_legend():
    items = []
    for name, _slug, glyph, color in astrocartography.display_bodies():
        items.append(
            f'<span class="item"><span class="sw" style="background:{color}">'
            f'</span><span class="pg">{glyph}\ufe0e</span>{name}</span>'
        )
    return "\n          ".join(items)


def acg_planet_chips():
    chips = []
    for name, slug, _glyph, color in astrocartography.display_bodies():
        chips.append(
            f'<button class="chip pl on" data-b="{slug}" style="--c:{color}">'
            f'<span class="dot"></span>{name}</button>'
        )
    return "\n          ".join(chips)


def acg_readout(data):
    rows = []
    for r in astrocartography.city_readout(data["jd"]):
        cells = [f'<td class="ro-city">{r["city"]}</td>']
        for ang in astrocartography.ANGLE_ORDER:
            c = r[ang]
            extra = " ro-mc" if ang == "MC" else ""
            if c:
                cells.append(
                    f'<td class="ro-cell{extra}">'
                    f'<span class="pg" style="color:{c["color"]}">'
                    f'{c["glyph"]}\ufe0e</span>'
                    f'<span class="ro-mi">{round(c["mi"])}\u2009mi</span></td>'
                )
            else:
                cells.append(f'<td class="ro-cell ro-none{extra}">\u00b7</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "\n          ".join(rows)


def angles_line(data):
    dc = (data["asc"] + 180) % 360
    ic = (data["mc"] + 180) % 360
    return (f'Ascendant {fmt(data["asc"])} &nbsp;·&nbsp; '
            f'Midheaven {fmt(data["mc"])} &nbsp;·&nbsp; '
            f'Descendant {fmt(dc)} &nbsp;·&nbsp; '
            f'Imum Coeli {fmt(ic)}')


def main():
    data = natal.compute()
    svg_placidus = build_chart_wheel.build_svg(data, "placidus")
    svg_whole = build_chart_wheel.build_svg(data, "whole")

    with open("birth_chart_template.html", encoding="utf-8") as f:
        html = f.read()

    for token, fname in FONTS.items():
        html = html.replace(token, b64_font(os.path.join(FONT_DIR, fname)))
    html = html.replace("%%WHEEL_SVG%%", svg_placidus)
    html = html.replace("%%WHEEL_SVG_WS%%", svg_whole)
    html = html.replace("%%ACG_SVG%%", astrocartography.build_svg(data))
    html = html.replace("%%ACG_LEGEND%%", acg_legend())
    html = html.replace("%%ACG_PLANET_CHIPS%%", acg_planet_chips())
    html = html.replace("%%ACG_READOUT%%", acg_readout(data))
    html = html.replace("%%PLACEMENTS_ROWS%%", placements_rows(data))
    html = html.replace("%%ANGLES_LINE%%", angles_line(data))

    with open("birth_chart.html", "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize("birth_chart.html")
    print(f"Wrote birth_chart.html ({size // 1024} KB)")


if __name__ == "__main__":
    main()
