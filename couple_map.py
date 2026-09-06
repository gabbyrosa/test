#!/usr/bin/env python3
"""
Relationship astrocartography overlay: three sets of benefic lines on one map.

  You     (natal, Jun 7 1996 3:35 PM EDT Pittsburgh)  -> rose
  Him     (natal, Jul 7 1995 12:01 AM EDT Pittsburgh) -> cyan
  The two of you (Davison relationship chart)         -> gold

Only the "thrive" bodies are drawn (Venus, Sun, Jupiter, and the Moon for the
couple), so the map answers one question: where does each of you light up, and
where do you light up together. Writes couple_astrocartography.svg.
"""

import math
import swisseph as swe
import astrocartography as acg

W, H, SCALE, LAT_MAX = acg.W, acg.H, acg.SCALE, acg.LAT_MAX
x_of, y_of = acg.x_of, acg.y_of

# --- the three charts -------------------------------------------------------
jd_her = swe.julday(1996, 6, 7, 15 + 35 / 60.0 - (-4), swe.GREG_CAL)
jd_his = swe.julday(1995, 7, 7, 0 + 1 / 60.0 - (-4), swe.GREG_CAL)
jd_dav = (jd_her + jd_his) / 2.0

LAYERS = [
    ("her", jd_her, "#e488b4", ("venus", "sun", "jupiter")),
    ("him", jd_his, "#46a7c6", ("venus", "sun", "jupiter")),
    ("dav", jd_dav, "#e0b64a", ("venus", "sun", "jupiter", "moon")),
]

MARKERS = [  # (label, lat, lon, kind)
    ("Pittsburgh (now)", 40.44, -79.96, "home"),
    ("Tucson", 32.22, -110.97, "her"),
    ("central Texas", 30.27, -98.5, "him"),
    ("Barcelona", 41.39, 2.17, "both"),
]

STYLE = """
<style>
 .oc{fill:#0e1420}
 .ld{fill:#232f40;stroke:#33465f;stroke-width:.5}
 .gr{stroke:#ffffff;stroke-opacity:.05;stroke-width:.5}
 .eqline{stroke:#ffffff;stroke-opacity:.10;stroke-width:.6}
 .ln{fill:none;stroke-width:1.5;stroke-opacity:.9}
 .glyph{font-family:'DejaVu Sans','Noto Sans Symbols2',sans-serif;
        font-variant-emoji:text;font-size:12px;paint-order:stroke;
        stroke:#0e1420;stroke-width:2.2px;stroke-linejoin:round}
 .cap{font-family:'DejaVu Sans',sans-serif;font-size:12px;fill:#e8ecf4}
 .sub{font-family:'DejaVu Sans',sans-serif;font-size:10px;fill:#9fb0c6}
 .mk{font-family:'DejaVu Sans',sans-serif;font-size:10.5px;paint-order:stroke;
     stroke:#0e1420;stroke-width:2.4px;stroke-linejoin:round}
</style>
"""


def body_lines(jd, slugs, color):
    lines, _ = acg.compute_lines(jd)
    out = []
    for ln in lines:
        if ln["slug"] in slugs:
            ln = dict(ln)
            ln["color"] = color
            out.append(ln)
    return out


def build():
    s = [f'<svg viewBox="0 0 {W:.0f} {H:.1f}" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="DejaVu Sans, sans-serif">', STYLE]
    s.append(f'<rect class="oc" x="0" y="0" width="{W:.0f}" height="{H:.1f}"/>')
    s.append(f'<path class="ld" d="{" ".join(acg.land_paths())}"/>')
    for lon in range(-150, 180, 30):
        x = x_of(lon)
        s.append(f'<line class="gr" x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}"/>')
    for lat in range(-60, 90, 30):
        y = y_of(lat)
        s.append(f'<line class="{"eqline" if lat==0 else "gr"}" x1="0" y1="{y:.1f}" '
                 f'x2="{W:.0f}" y2="{y:.1f}"/>')

    VS = acg.VS15
    for _who, jd, color, slugs in LAYERS:
        for ln in body_lines(jd, slugs, color):
            c = ln["color"]
            if ln["kind"] == "meridian":
                x = x_of(ln["lon"])
                s.append(f'<line class="ln" style="stroke:{c}" x1="{x:.1f}" y1="0" '
                         f'x2="{x:.1f}" y2="{H:.1f}"/>')
                yb = 15 if ln["angle"] == "MC" else H - 7
                s.append(f'<text class="glyph" x="{x:.1f}" y="{yb:.1f}" '
                         f'fill="{c}" text-anchor="middle">{ln["glyph"]}{VS}</text>')
            else:
                for seg in ln["segments"]:
                    d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in seg)
                    s.append(f'<path class="ln" style="stroke:{c}" d="{d}"/>')

    # markers
    for label, lat, lon, kind in MARKERS:
        x, y = x_of(lon), y_of(lat)
        if kind == "home":
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="none" '
                     f'stroke="#ffffff" stroke-width="1.6"/>')
            col = "#ffffff"
        elif kind == "both":
            star = star_path(x, y, 6.2, 3.0)
            s.append(f'<path d="{star}" fill="#e0b64a" stroke="#0e1420" '
                     f'stroke-width="1"/>')
            col = "#f0d178"
        else:
            col = "#e488b4" if kind == "her" else "#46a7c6"
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{col}" '
                     f'stroke="#0e1420" stroke-width="1"/>')
        dx = 7 if lon < 120 else -7
        anc = "start" if lon < 120 else "end"
        s.append(f'<text class="mk" x="{x+dx:.1f}" y="{y+3.5:.1f}" fill="{col}" '
                 f'text-anchor="{anc}">{label}</text>')

    # title + legend
    s.append(f'<text class="cap" x="12" y="22">Where each of you thrives, and where you thrive together</text>')
    s.append(f'<text class="sub" x="12" y="37">Benefic lines only: Venus, Sun, Jupiter (and the Moon for the two of you). '
             f'Glyph marks where that planet sits on an angle.</text>')
    lx, ly = 12, H - 46
    leg = [("You", "#e488b4"), ("Him", "#46a7c6"), ("The two of you (Davison)", "#e0b64a")]
    for i, (lab, col) in enumerate(leg):
        yy = ly + i * 15
        s.append(f'<line x1="{lx}" y1="{yy-3:.1f}" x2="{lx+22}" y2="{yy-3:.1f}" '
                 f'style="stroke:{col};stroke-width:2.4"/>')
        s.append(f'<text class="sub" x="{lx+28}" y="{yy:.1f}" fill="#e8ecf4">{lab}</text>')

    s.append("</svg>")
    return "\n".join(s)


def star_path(cx, cy, r_out, r_in, points=5):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi / points * i - math.pi / 2
        pts.append(f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
    return "M" + "L".join(pts) + "Z"


if __name__ == "__main__":
    with open("couple_astrocartography.svg", "w", encoding="utf-8") as f:
        f.write(build() + "\n")
    print("Wrote couple_astrocartography.svg")
    # confirm the headline longitudes
    for who, jd, _c, _s in LAYERS:
        lines, _ = acg.compute_lines(jd)
        mc = {l["slug"]: l["lon"] for l in lines if l["angle"] == "MC" and l["kind"] == "meridian"}
        print(f"  {who:3} Venus MC {mc['venus']:7.1f}   Sun MC {mc['sun']:7.1f}   Jupiter MC {mc['jupiter']:7.1f}")
