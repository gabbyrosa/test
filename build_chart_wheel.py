#!/usr/bin/env python3
"""
Render the natal chart as an SVG wheel.

Structural strokes and text use CSS classes (no baked colors) so the wheel
adapts to light/dark themes when embedded in an HTML page. Only the four
element hues are fixed, since they carry meaning.

Writes birth_chart.svg.
"""

import math
import natal

SIZE = 820
CX = CY = SIZE / 2

R_OUT = 398          # outer circle
R_SIGN_IN = 344      # inner edge of zodiac band
R_TICK = 344         # degree ticks live just inside the band
R_PLANET = 300       # planet glyph ring (before declustering nudges)
R_DEG = 322          # small degree label ring
R_HUB = 250          # inner circle; aspect lines live inside it
R_SIGN_GLYPH = 371   # zodiac glyph radius
R_HOUSE_NUM = 236    # house numbers just inside the hub

MIN_SEP = 9.0        # minimum degrees between planet glyphs on the ring

VS15 = "\ufe0e"      # variation selector: force text (not emoji) presentation


def angle(lon, asc):
    """Ecliptic longitude -> screen radians (Ascendant at left, MC at top)."""
    return math.radians(180 + (lon - asc))


def pt(lon, r, asc):
    a = angle(lon, asc)
    return CX + r * math.cos(a), CY - r * math.sin(a)


def arc_path(lon1, lon2, r, asc):
    """SVG arc between two longitudes at radius r (counterclockwise band)."""
    x1, y1 = pt(lon1, r, asc)
    x2, y2 = pt(lon2, r, asc)
    span = (lon2 - lon1) % 360
    large = 1 if span > 180 else 0
    # screen angle decreases as longitude increases (y flipped) -> sweep 1
    return f"M {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 0 {x2:.2f} {y2:.2f}"


def declutter(items):
    """items: list of (name, lon). Returns {name: display_lon} spread apart."""
    ordered = sorted(items, key=lambda t: t[1])
    disp = [lon for _, lon in ordered]
    n = len(disp)
    for _ in range(400):
        moved = False
        for i in range(n):
            j = (i + 1) % n
            gap = (disp[j] - disp[i]) % 360
            if gap < MIN_SEP:
                push = (MIN_SEP - gap) / 2 + 0.02
                disp[i] = (disp[i] - push) % 360
                disp[j] = (disp[j] + push) % 360
                moved = True
        if not moved:
            break
    return {ordered[i][0]: disp[i] for i in range(n)}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(data):
    asc = data["asc"]
    cusps = data["cusps"]
    p = data["planets"]
    s = []
    s.append(
        f'<svg viewBox="0 0 {SIZE} {SIZE}" class="wheel" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Natal chart wheel">'
    )

    # --- zodiac band: subtle element-tinted fills + glyphs ------------------
    for i in range(12):
        lon1, lon2 = i * 30, i * 30 + 30
        elem = natal.ELEMENTS[i]
        outer = arc_path(lon1, lon2, R_OUT, asc)
        # build a filled wedge segment for the band
        x_o1, y_o1 = pt(lon1, R_OUT, asc)
        x_o2, y_o2 = pt(lon2, R_OUT, asc)
        x_i1, y_i1 = pt(lon1, R_SIGN_IN, asc)
        x_i2, y_i2 = pt(lon2, R_SIGN_IN, asc)
        seg = (
            f'M {x_o1:.2f} {y_o1:.2f} '
            f'A {R_OUT} {R_OUT} 0 0 0 {x_o2:.2f} {y_o2:.2f} '
            f'L {x_i2:.2f} {y_i2:.2f} '
            f'A {R_SIGN_IN} {R_SIGN_IN} 0 0 1 {x_i1:.2f} {y_i1:.2f} Z'
        )
        s.append(f'<path d="{seg}" class="band-fill el-{elem}"/>')
        gx, gy = pt(i * 30 + 15, R_SIGN_GLYPH, asc)
        s.append(
            f'<text x="{gx:.2f}" y="{gy:.2f}" class="sign-glyph el-{elem}" '
            f'text-anchor="middle" dominant-baseline="central">'
            f'{natal.SIGN_GLYPHS[i]}{VS15}</text>'  # VS15 forces text, not emoji
        )

    # ring circles
    for r in (R_OUT, R_SIGN_IN, R_HUB):
        s.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" class="ring"/>')

    # sign divider lines (every 30 degrees)
    for i in range(12):
        x1, y1 = pt(i * 30, R_SIGN_IN, asc)
        x2, y2 = pt(i * 30, R_OUT, asc)
        s.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" '
                 f'y2="{y2:.2f}" class="ring"/>')

    # degree ticks every 5 degrees inside the band
    for d in range(0, 360, 5):
        length = 9 if d % 30 == 0 else (6 if d % 10 == 0 else 3)
        x1, y1 = pt(d, R_TICK, asc)
        x2, y2 = pt(d, R_TICK - length, asc)
        s.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" '
                 f'y2="{y2:.2f}" class="tick"/>')

    # --- house cusps + numbers ---------------------------------------------
    ANGLE_CUSPS = {0: "AC", 3: "IC", 6: "DC", 9: "MC"}
    for i in range(12):
        cusp = cusps[i]
        x1, y1 = pt(cusp, R_HUB, asc)
        x2, y2 = pt(cusp, R_SIGN_IN, asc)
        cls = "cusp-angle" if i in ANGLE_CUSPS else "cusp"
        s.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" '
                 f'y2="{y2:.2f}" class="{cls}"/>')
        # angle label just outside the wheel
        if i in ANGLE_CUSPS:
            lx, ly = pt(cusp, R_OUT + 16, asc)
            s.append(
                f'<text x="{lx:.2f}" y="{ly:.2f}" class="angle-label" '
                f'text-anchor="middle" dominant-baseline="central">'
                f'{ANGLE_CUSPS[i]}</text>'
            )
        # house number at mid-house, just inside the hub
        nxt = cusps[(i + 1) % 12]
        mid = (cusp + ((nxt - cusp) % 360) / 2) % 360
        hx, hy = pt(mid, R_HOUSE_NUM, asc)
        s.append(
            f'<text x="{hx:.2f}" y="{hy:.2f}" class="house-num" '
            f'text-anchor="middle" dominant-baseline="central">{i + 1}</text>'
        )

    # --- aspect lines inside the hub ---------------------------------------
    for a in data["aspects"]:
        if a["kind"] == "conjunction":
            continue  # adjacent points; a line adds noise
        x1, y1 = pt(p[a["a"]]["lon"], R_HUB, asc)
        x2, y2 = pt(p[a["b"]]["lon"], R_HUB, asc)
        s.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" '
                 f'y2="{y2:.2f}" class="aspect aspect-{a["kind"]}"/>')

    # --- planets (declustered) ---------------------------------------------
    wheel_bodies = [(n, p[n]["lon"]) for n in data["order"]]  # 10 planets+node+chiron
    disp = declutter(wheel_bodies)
    for name, _ in wheel_bodies:
        d = p[name]
        true_lon = d["lon"]
        dlon = disp[name]
        # pointer from true degree (band inner edge) to glyph
        px1, py1 = pt(true_lon, R_SIGN_IN, asc)
        px2, py2 = pt(dlon, R_PLANET + 14, asc)
        s.append(f'<line x1="{px1:.2f}" y1="{py1:.2f}" x2="{px2:.2f}" '
                 f'y2="{py2:.2f}" class="pointer"/>')
        gx, gy = pt(dlon, R_PLANET, asc)
        lum = " luminary" if name in ("Sun", "Moon") else ""
        s.append(
            f'<text x="{gx:.2f}" y="{gy:.2f}" class="planet-glyph{lum}" '
            f'text-anchor="middle" dominant-baseline="central">'
            f'{d["glyph"]}{VS15}</text>'
        )
        # degree-in-sign label + retro mark
        dx, dy = pt(dlon, R_DEG, asc)
        retro = "℞" if d["retro"] else ""
        s.append(
            f'<text x="{dx:.2f}" y="{dy:.2f}" class="deg-label" '
            f'text-anchor="middle" dominant-baseline="central">'
            f'{d["deg"]}°{retro}</text>'
        )

    s.append("</svg>")
    return "\n".join(s)


def main():
    data = natal.compute()
    svg = build_svg(data)
    with open("birth_chart.svg", "w") as f:
        f.write(svg + "\n")
    print("Wrote birth_chart.svg")


if __name__ == "__main__":
    main()
