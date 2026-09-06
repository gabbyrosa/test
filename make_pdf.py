#!/usr/bin/env python3
"""
Export a standalone, print-friendly astrocartography map to PDF (all lines
shown), for download. Writes astrocartography_map.pdf.
"""

import glob
import natal
import astrocartography as acg
from playwright.sync_api import sync_playwright

GLYPH = '"Noto Sans Symbols2","DejaVu Sans","Segoe UI Symbol",serif'
LABEL = '"DejaVu Sans","Helvetica Neue",Arial,sans-serif'

STYLE = """
:root{--ocean:#e9e2d2;--land:#d6cba9;--grid:rgba(60,50,20,.12);
      --ink:#26263f;--muted:#6c6782;--gold:#9c7523;--line:#cbbf9d;}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);
     font-family:%LABEL%;padding:20px 24px}
h1{font-family:Georgia,serif;font-size:20px;margin:0 0 2px}
.sub{color:var(--muted);font-size:12px;margin:0 0 12px}
.acg{display:block;width:100%%;height:auto;border:1px solid var(--line)}
.acg-ocean{fill:var(--ocean)} .acg-land{fill:var(--land);stroke:none}
.acg-grid{stroke:var(--grid);stroke-width:1} .acg-equator{stroke-width:1.4}
.acg-line{fill:none;stroke-width:1.4;opacity:.95}
.acg-horizon{stroke-dasharray:5 3;opacity:.85}
.acg-label{font-family:%GLYPH%;font-size:11px;paint-order:stroke;
           stroke:var(--ocean);stroke-width:2.4px;stroke-linejoin:round}
.acg-home{fill:var(--gold);stroke:var(--ocean);stroke-width:1.5}
.acg-home-label{fill:var(--ink);font-family:%LABEL%;font-size:11px;font-weight:700;
     paint-order:stroke;stroke:var(--ocean);stroke-width:2.6px;stroke-linejoin:round;
     text-transform:uppercase;letter-spacing:.06em}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:12px;font-size:11px;color:var(--muted)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend .sw{width:16px;height:3px;border-radius:1px}
.legend .pg{font-family:%GLYPH%;color:var(--ink)}
.key{font-size:11px;color:var(--muted);margin-top:8px;line-height:1.5}
""".replace("%GLYPH%", GLYPH).replace("%LABEL%", LABEL)


def legend_html():
    out = []
    for name, _slug, glyph, color in acg.display_bodies():
        out.append(f'<span><span class="sw" style="background:{color}"></span>'
                   f'<span class="pg">{glyph}\ufe0e</span>{name}</span>')
    return "".join(out)


def main():
    data = natal.compute()
    svg = acg.build_svg(data)
    b = data["birth"]
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{STYLE}</style></head>
<body>
<h1>Astrocartography</h1>
<p class="sub">{b['date_label']} &middot; {b['time_label']} &middot; {b['place_label']}
&middot; MC/IC vertical, AC/DC dashed</p>
{svg}
<div class="legend">{legend_html()}</div>
<p class="key">Each line marks where a body is angular at the birth moment. Vertical lines are
MC (culminating) and IC (lowest); dashed curves are AC (rising) and DC (setting).
Computed with the Swiss Ephemeris on an equirectangular projection. The gold dot is Pittsburgh.</p>
</body></html>"""

    with open("standalone_map.html", "w", encoding="utf-8") as f:
        f.write(html)

    exe = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")[0]
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        pg = br.new_page()
        pg.goto("file:///home/user/test/standalone_map.html")
        pg.wait_for_timeout(500)
        pg.pdf(path="astrocartography_map.pdf", landscape=True,
               width="11in", height="8.5in", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        br.close()
    print("Wrote astrocartography_map.pdf")


if __name__ == "__main__":
    main()
