#!/usr/bin/env python3
"""
Build a print-ready standalone HTML from jyotish_reading.html and render it
to PDF with the bundled Chromium.

The artifact file is a fragment: no doctype, no <html>/<head>/<body>, because
the Artifact host supplies those. This wraps it, forces the light theme,
drops the sticky section rail, lets the wide tables wrap instead of scroll,
and adds page-break rules so the three-level blocks and the theme cards are
never split across a page.

Writes Jyotish-Natal-Reading.pdf.
"""

import pathlib
import re
import subprocess

SRC = pathlib.Path("/home/user/test/jyotish_reading.html")
OUT_HTML = pathlib.Path("/home/user/test/jyotish_reading_print.html")
OUT_PDF = pathlib.Path("/home/user/test/Jyotish-Natal-Reading.pdf")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

PRINT_CSS = """
@page{size:Letter;margin:15mm 14mm 16mm}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-size:10.2pt;line-height:1.5;background:#fff}

/* the rail is navigation; it has no meaning on paper */
.rail{display:none!important}
.wrap{display:block!important;max-width:none;padding:0;grid-template-columns:none}
.col{max-width:none}

header{padding:0 0 18pt;border-bottom:1.6pt solid var(--ink);
  break-after:avoid;page-break-after:avoid}
h1{font-size:30pt;margin-bottom:12pt;max-width:none}
.dek{font-size:11.5pt;max-width:none}
.eyebrow{font-size:7.5pt;margin-bottom:12pt}
.vitals{margin-top:16pt;gap:0 22pt}
.vitals dt{font-size:7pt}
.vitals dd{font-size:9pt}

section{padding:16pt 0 14pt;break-inside:auto}
.shead{break-after:avoid;page-break-after:avoid;margin-bottom:5pt}
h2{font-size:17pt}
h3{font-size:12.5pt;margin:16pt 0 6pt;break-after:avoid;page-break-after:avoid}
h4{font-size:8pt;margin:14pt 0 5pt;break-after:avoid;page-break-after:avoid}
p{max-width:none;margin-bottom:7pt}
.lede{font-size:11pt;max-width:none;margin-bottom:12pt}
ul{max-width:none;margin-bottom:8pt}
li{margin-bottom:3pt}

/* keep the repeated devices intact across page boundaries */
.tri,.theme,.note,.chart{break-inside:avoid;page-break-inside:avoid}
.tri{margin:12pt 0}
.tri>div{padding:8pt 12pt 9pt}
.tri .lv{font-size:7pt;margin-bottom:4pt}
.t-fact p{font-size:8.8pt;line-height:1.45}
.t-class p{font-size:10.5pt;line-height:1.45}
.t-lived p,.t-lived ul{font-size:9.8pt;line-height:1.45}
.tri p{max-width:none;margin-bottom:5pt}
.note{margin:12pt 0;padding:9pt 13pt}
.note p{font-size:9.6pt;max-width:none;margin-bottom:5pt}
.note .lv{font-size:7pt;margin-bottom:4pt}

/* tables cannot scroll on paper, so let them wrap and shrink */
.tbl{overflow-x:visible;margin:11pt 0;break-inside:auto}
table{font-size:7.6pt;white-space:normal;table-layout:auto}
th{font-size:6.6pt;padding:5pt 6pt;break-inside:avoid}
td{padding:3.6pt 6pt;vertical-align:top}
thead{display:table-header-group}
tr{break-inside:avoid;page-break-inside:avoid}

.charts{gap:14pt;margin:14pt 0;break-inside:avoid;page-break-inside:avoid}
.sq{max-width:74mm}
.sq .rs{font-size:5.6pt}
.sq .gr{font-size:7.2pt}
.core b{font-size:9.5pt}
.core span{font-size:6pt}

.themes{gap:6pt;margin:14pt 0}
.theme{padding:11pt 13pt;gap:10pt;grid-template-columns:22pt 1fr}
.theme h3{font-size:12pt;margin:0 0 5pt}
.theme p{font-size:9.8pt;max-width:none;margin-bottom:5pt}
.theme .combo{font-size:8pt;padding:6pt 8pt;margin-top:7pt;line-height:1.45}
.theme .tn{font-size:9pt}

footer{padding:16pt 0 0;margin-top:12pt;font-size:9pt;break-inside:avoid}
footer p{max-width:none}

/* sections that begin a major movement start on a fresh page */
#s4,#s9,#s13,#s15,#s16,#s17{break-before:page;page-break-before:always}
.tier{break-after:avoid;page-break-after:avoid;font-size:7pt;padding:2pt 5pt}
"""


def main():
    frag = SRC.read_text()

    title = re.search(r"<title>(.*?)</title>", frag).group(1)
    body = re.sub(r"<title>.*?</title>\s*", "", frag, count=1)

    html = (
        '<!doctype html><html lang="en" data-theme="light">'
        '<head><meta charset="utf-8">'
        f"<title>{title}</title>"
        f"{body.split('</style>')[0]}</style>"
        f"<style>{PRINT_CSS}</style>"
        "</head><body>"
        f"{body.split('</style>', 1)[1]}"
        "</body></html>"
    )
    OUT_HTML.write_text(html)
    print(f"wrote {OUT_HTML}  ({len(html):,} bytes)")

    subprocess.run(
        [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
         "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
         "--virtual-time-budget=12000",
         f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()],
        check=True, capture_output=True,
    )
    print(f"wrote {OUT_PDF}  ({OUT_PDF.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
