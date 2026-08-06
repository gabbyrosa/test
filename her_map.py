#!/usr/bin/env python3
"""
HER astrocartography, benefic lines only, colored by planet, with the spots
where she lights up marked. Writes her_map.svg.
  Venus  = love / beauty (her chart ruler)   rose
  Sun    = vitality / being seen             gold-yellow
  Jupiter= luck / growth / abundance         amber
  Moon   = comfort / home / body             silver-blue
"""
import math
import swisseph as swe
import astrocartography as acg

W, H = acg.W, acg.H
x_of, y_of = acg.x_of, acg.y_of
jd_her = swe.julday(1996, 6, 7, 15 + 35 / 60.0 - (-4), swe.GREG_CAL)

COLOR = {"venus": "#e488b4", "sun": "#f2c14e", "jupiter": "#d98a2b", "moon": "#9bb0d0"}

MARKERS = [  # label, lat, lon, theme-color-key
    ("Pittsburgh (now)", 40.44, -79.96, "home"),
    ("Tucson: beautiful + seen", 32.22, -110.97, "venus"),
    ("Asheville: abundant home", 35.60, -82.55, "jupiter"),
    ("Barcelona: love", 41.39, 2.17, "venus"),
    ("Athens: luck + adventure", 37.98, 23.73, "jupiter"),
    ("Tokyo: at home in your skin", 35.68, 139.65, "sun"),
]

STYLE = """
<style>
 .oc{fill:#0e1420}.ld{fill:#232f40;stroke:#33465f;stroke-width:.5}
 .gr{stroke:#fff;stroke-opacity:.05;stroke-width:.5}.eqline{stroke:#fff;stroke-opacity:.10;stroke-width:.6}
 .ln{fill:none;stroke-width:1.6;stroke-opacity:.92}
 .glyph{font-family:'DejaVu Sans','Noto Sans Symbols2',sans-serif;font-variant-emoji:text;font-size:12px;
        paint-order:stroke;stroke:#0e1420;stroke-width:2.2px;stroke-linejoin:round}
 .cap{font-family:'DejaVu Sans',sans-serif;font-size:12px;fill:#e8ecf4}
 .sub{font-family:'DejaVu Sans',sans-serif;font-size:10px;fill:#9fb0c6}
 .mk{font-family:'DejaVu Sans',sans-serif;font-size:10.5px;paint-order:stroke;stroke:#0e1420;
     stroke-width:2.4px;stroke-linejoin:round}
</style>
"""


def body_lines(jd, slug, color):
    lines, _ = acg.compute_lines(jd)
    out = []
    for ln in lines:
        if ln["slug"] == slug:
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

    VS = acg.VS15
    for slug, color in COLOR.items():
        for ln in body_lines(jd_her, slug, color):
            if ln["kind"] == "meridian":
                x = x_of(ln["lon"])
                s.append(f'<line class="ln" style="stroke:{color}" x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.1f}"/>')
                yb = 15 if ln["angle"] == "MC" else H - 7
                s.append(f'<text class="glyph" x="{x:.1f}" y="{yb:.1f}" fill="{color}" '
                         f'text-anchor="middle">{ln["glyph"]}{VS}</text>')
            else:
                for seg in ln["segments"]:
                    d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in seg)
                    s.append(f'<path class="ln" style="stroke:{color}" d="{d}"/>')

    for label, lat, lon, key in MARKERS:
        x, y = x_of(lon), y_of(lat)
        if key == "home":
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="none" stroke="#fff" stroke-width="1.6"/>')
            col = "#fff"
        else:
            col = COLOR[key]
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{col}" stroke="#0e1420" stroke-width="1"/>')
        dx = 7 if lon < 130 else -7
        anc = "start" if lon < 130 else "end"
        s.append(f'<text class="mk" x="{x+dx:.1f}" y="{y+3.5:.1f}" fill="{col}" text-anchor="{anc}">{label}</text>')

    s.append('<text class="cap" x="12" y="22">Where your lines light up</text>')
    s.append('<text class="sub" x="12" y="37">Your benefic planets sitting on an angle. '
             'Color = which planet: Venus (love, beauty), Sun (vitality), Jupiter (luck, growth), Moon (home, body).</text>')
    lx, ly = 12, H - 60
    leg = [("Venus (love / beauty / you)", "#e488b4"), ("Sun (vitality / seen)", "#f2c14e"),
           ("Jupiter (luck / growth)", "#d98a2b"), ("Moon (home / body)", "#9bb0d0")]
    for i, (lab, col) in enumerate(leg):
        yy = ly + i * 14
        s.append(f'<line x1="{lx}" y1="{yy-3:.1f}" x2="{lx+22}" y2="{yy-3:.1f}" style="stroke:{col};stroke-width:2.6"/>')
        s.append(f'<text class="sub" x="{lx+28}" y="{yy:.1f}" fill="#e8ecf4">{lab}</text>')
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    with open("her_map.svg", "w", encoding="utf-8") as f:
        f.write(build() + "\n")
    print("Wrote her_map.svg")
