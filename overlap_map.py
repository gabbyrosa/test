#!/usr/bin/env python3
"""
Overlay: HIS career + wealth lines on top of HER thrive zones, to show where
the two overlap. Rose = her blooming planets (Venus, Sun, Jupiter). Cyan = his
career/wealth planets (Sun, Jupiter, Saturn, Pluto). A gold band marks the dry
Southwest, where both stack up. Writes overlap_map.svg.
"""

import math
import swisseph as swe
import astrocartography as acg

W, H = acg.W, acg.H
x_of, y_of = acg.x_of, acg.y_of

jd_her = swe.julday(1996, 6, 7, 15 + 35 / 60.0 - (-4), swe.GREG_CAL)
jd_his = swe.julday(1995, 7, 7, 0 + 1 / 60.0 - (-4), swe.GREG_CAL)

LAYERS = [
    ("her", jd_her, "#e488b4", ("venus", "sun", "jupiter")),          # thrive
    ("him", jd_his, "#46a7c6", ("sun", "jupiter", "saturn", "pluto")),  # career/wealth
]

MARKERS = [
    ("Pittsburgh (now)", 40.44, -79.96, "home"),
    ("Tucson", 32.22, -110.97, "both"),
    ("Santa Fe", 35.69, -105.94, "both"),
    ("Austin", 30.27, -97.74, "him"),
    ("St. Pete", 27.77, -82.64, "her"),
]

# dry-Southwest overlap band (lon, lat corners)
BAND = dict(lon0=-114.5, lon1=-99.0, lat0=45.5, lat1=28.0)

STYLE = """
<style>
 .oc{fill:#0e1420}.ld{fill:#232f40;stroke:#33465f;stroke-width:.5}
 .gr{stroke:#fff;stroke-opacity:.05;stroke-width:.5}.eqline{stroke:#fff;stroke-opacity:.10;stroke-width:.6}
 .ln{fill:none;stroke-width:1.5;stroke-opacity:.9}
 .band{fill:#e0b64a;fill-opacity:.13;stroke:#e0b64a;stroke-opacity:.5;stroke-width:1.2;stroke-dasharray:5 4}
 .glyph{font-family:'DejaVu Sans','Noto Sans Symbols2',sans-serif;font-variant-emoji:text;font-size:12px;
        paint-order:stroke;stroke:#0e1420;stroke-width:2.2px;stroke-linejoin:round}
 .cap{font-family:'DejaVu Sans',sans-serif;font-size:12px;fill:#e8ecf4}
 .sub{font-family:'DejaVu Sans',sans-serif;font-size:10px;fill:#9fb0c6}
 .mk{font-family:'DejaVu Sans',sans-serif;font-size:10.5px;paint-order:stroke;stroke:#0e1420;
     stroke-width:2.4px;stroke-linejoin:round}
 .bandlbl{font-family:'DejaVu Sans',sans-serif;font-size:10px;fill:#e8c766;font-style:italic}
</style>
"""


def star_path(cx, cy, ro, ri, pts=5):
    p = []
    for i in range(pts * 2):
        r = ro if i % 2 == 0 else ri
        a = math.pi / pts * i - math.pi / 2
        p.append(f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
    return "M" + "L".join(p) + "Z"


def body_lines(jd, slugs, color):
    lines, _ = acg.compute_lines(jd)
    out = []
    for ln in lines:
        if ln["slug"] in slugs:
            ln = dict(ln); ln["color"] = color; out.append(ln)
    return out


def build():
    s = [f'<svg viewBox="0 0 {W:.0f} {H:.1f}" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="DejaVu Sans, sans-serif">', STYLE]
    s.append(f'<rect class="oc" x="0" y="0" width="{W:.0f}" height="{H:.1f}"/>')
    s.append(f'<path class="ld" d="{" ".join(acg.land_paths())}"/>')
    for lon in range(-150, 180, 30):
        x = x_of(lon); s.append(f'<line class="gr" x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}"/>')
    for lat in range(-60, 90, 30):
        y = y_of(lat)
        s.append(f'<line class="{"eqline" if lat==0 else "gr"}" x1="0" y1="{y:.1f}" x2="{W:.0f}" y2="{y:.1f}"/>')

    # overlap band (drawn under the lines)
    bx, by = x_of(BAND["lon0"]), y_of(BAND["lat0"])
    bw, bh = x_of(BAND["lon1"]) - bx, y_of(BAND["lat1"]) - by
    s.append(f'<rect class="band" x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="7"/>')
    s.append(f'<text class="bandlbl" x="{bx + bw/2:.1f}" y="{by - 5:.1f}" text-anchor="middle">'
             f'your dry heat  +  his wealth</text>')

    VS = acg.VS15
    for _who, jd, color, slugs in LAYERS:
        for ln in body_lines(jd, slugs, color):
            c = ln["color"]
            if ln["kind"] == "meridian":
                x = x_of(ln["lon"])
                s.append(f'<line class="ln" style="stroke:{c}" x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}"/>')
                yb = 15 if ln["angle"] == "MC" else H - 7
                s.append(f'<text class="glyph" x="{x:.1f}" y="{yb:.1f}" fill="{c}" '
                         f'text-anchor="middle">{ln["glyph"]}{VS}</text>')
            else:
                for seg in ln["segments"]:
                    d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in seg)
                    s.append(f'<path class="ln" style="stroke:{c}" d="{d}"/>')

    for label, lat, lon, kind in MARKERS:
        x, y = x_of(lon), y_of(lat)
        if kind == "home":
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="none" stroke="#fff" stroke-width="1.6"/>')
            col = "#fff"
        elif kind == "both":
            s.append(f'<path d="{star_path(x, y, 6.2, 3.0)}" fill="#e0b64a" stroke="#0e1420" stroke-width="1"/>')
            col = "#f0d178"
        else:
            col = "#e488b4" if kind == "her" else "#46a7c6"
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{col}" stroke="#0e1420" stroke-width="1"/>')
        s.append(f'<text class="mk" x="{x+7:.1f}" y="{y+3.5:.1f}" fill="{col}" text-anchor="start">{label}</text>')

    s.append('<text class="cap" x="12" y="22">His career and wealth lines over your thrive zones</text>')
    s.append('<text class="sub" x="12" y="37">Rose = where you bloom (Venus, Sun, Jupiter). '
             'Cyan = where his career and money peak (Sun, Jupiter, Saturn, Pluto). '
             'Gold band = where both stack up.</text>')
    lx, ly = 12, H - 32
    for i, (lab, col) in enumerate([("You (thrive)", "#e488b4"), ("Him (career + wealth)", "#46a7c6")]):
        yy = ly + i * 15
        s.append(f'<line x1="{lx}" y1="{yy-3:.1f}" x2="{lx+22}" y2="{yy-3:.1f}" style="stroke:{col};stroke-width:2.4"/>')
        s.append(f'<text class="sub" x="{lx+28}" y="{yy:.1f}" fill="#e8ecf4">{lab}</text>')
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    with open("overlap_map.svg", "w", encoding="utf-8") as f:
        f.write(build() + "\n")
    print("Wrote overlap_map.svg")
