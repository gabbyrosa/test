#!/usr/bin/env python3
"""Generate the MSA relocation reference page from msa_table.json."""
import json, os, html

SC = "/tmp/claude-0/-home-user-test/69d90e22-42ef-59e3-b947-6e9046f33faa/scratchpad"
d = json.load(open(os.path.join(SC, "msa_table.json")))
rows, legend = d["rows"], d["legend"]
TN = ["identity", "home", "travel", "career"]
TAG = {"A": "WS tropical", "B": "Placidus tropical", "C": "WS sidereal"}
FULL = {"A": "whole sign · tropical · traditional rulers",
        "B": "Placidus · tropical · modern rulers",
        "C": "whole sign · sidereal Lahiri · traditional rulers"}
used = {m: set() for m in "ABC"}
for r in rows:
    for i, m in enumerate("ABC"):
        used[m].add(r["cells"][i][0])
mx = {m: max(r["cells"][i][1] or 0 for r in rows) for i, m in enumerate("ABC")}

def leg(m):
    out = []
    for lab, topics in sorted(legend[m], key=lambda t: int(t[0][1:])):
        if lab not in used[m]:
            continue
        n = sum(1 for r in rows if r["cells"]["ABC".index(m)][0] == lab)
        cells = "".join(
            f'<div class="tp"><span class="tp-n">{TN[i]}</span>'
            f'<span class="tp-v">{html.escape(t[0])} <em>h{t[1]}</em>'
            + (f'<span class="occ">{html.escape("·".join(t[2]))}</span>' if t[2] else "")
            + "</span></div>" for i, t in enumerate(topics))
        out.append(f'<article class="lg-row"><header><span class="chip c{m}">{lab}</span>'
                   f'<span class="lg-n">{n} MSA{"s" if n != 1 else ""}</span></header>'
                   f'<div class="tp-grid">{cells}</div></article>')
    return "".join(out)

def cells(r):
    o = ""
    for i, m in enumerate("ABC"):
        lab, mar = r["cells"][i]
        pct = min(100, (mar or 0) / mx[m] * 100)
        o += (f'<td class="k k{m}"><span class="chip c{m}">{lab}</span></td>'
              f'<td class="mg k{m}" data-v="{mar or 0:.0f}"><span class="mv">'
              f'{mar or 0:,.0f}</span><span class="bar"><i style="width:{pct:.1f}%"></i>'
              f'</span></td>')
    return o

trs = "".join(
    f'<tr data-n="{html.escape(r["name"].lower())}" '
    f'data-a="{r["cells"][0][0]}" data-b="{r["cells"][1][0]}" data-c="{r["cells"][2][0]}">'
    f'<td class="nm">{html.escape(r["name"])}</td>'
    f'<td class="pop" data-v="{r["pop"]}">{r["pop"]:,}</td>{cells(r)}</tr>'
    for r in rows)

def chips(m):
    return "".join(f'<button class="fc c{m}" data-m="{m}" data-l="{l}">{l}</button>'
                   for l in sorted(used[m], key=lambda x: int(x[1:])))

open("/home/user/test/msa_page.html", "w").write(f"""<title>Relocation Regimes</title>
<style>
:root{{--ground:#F6F7F9;--surface:#FFF;--raise:#FBFCFD;--ink:#161A22;--mut:#68707E;
--rule:#DFE3EA;--rule2:#EBEEF3;--A:#4B5EA6;--B:#9C6B24;--C:#2A7873;
--Aw:#EDEFF8;--Bw:#F7F0E4;--Cw:#E7F2F1;--focus:#4B5EA6;}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
--ground:#11141A;--surface:#181C24;--raise:#1E232C;--ink:#E6E9F0;--mut:#98A1B2;
--rule:#262C38;--rule2:#1F242E;--A:#8B9BDC;--B:#D3A05A;--C:#5FB3AC;
--Aw:#1B2030;--Bw:#2A2318;--Cw:#152724;--focus:#8B9BDC;}}}}
:root[data-theme="dark"]{{--ground:#11141A;--surface:#181C24;--raise:#1E232C;--ink:#E6E9F0;
--mut:#98A1B2;--rule:#262C38;--rule2:#1F242E;--A:#8B9BDC;--B:#D3A05A;--C:#5FB3AC;
--Aw:#1B2030;--Bw:#2A2318;--Cw:#152724;--focus:#8B9BDC;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
font:15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 22px 80px}}
h1{{font:600 30px/1.15 "Iowan Old Style",Palatino,Georgia,serif;margin:0;
letter-spacing:-.01em;text-wrap:balance}}
.mast{{padding:44px 0 22px;border-bottom:1px solid var(--rule);
display:flex;flex-direction:column;gap:14px}}
.sub{{color:var(--mut);max-width:66ch;margin:0}}
.crit{{display:flex;flex-wrap:wrap;gap:6px 18px;font:12px/1.5 ui-monospace,
SFMono-Regular,Menlo,monospace;color:var(--mut)}}
.crit b{{color:var(--ink);font-weight:600}}
.warn{{border-left:2px solid var(--A);padding:10px 0 10px 14px;color:var(--mut);
max-width:70ch;font-size:14px}}
.warn b{{color:var(--ink)}}
h2{{font:600 12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.14em;
text-transform:uppercase;color:var(--mut);margin:44px 0 16px}}
.legends{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:18px}}
.lg{{background:var(--surface);border:1px solid var(--rule);border-radius:3px;overflow:hidden}}
.lg>h3{{margin:0;padding:12px 16px;border-bottom:1px solid var(--rule);
font:600 13px/1.3 ui-sans-serif,system-ui,sans-serif;display:flex;
justify-content:space-between;align-items:baseline;gap:10px}}
.lg>h3 small{{font:11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);
font-weight:400;letter-spacing:.02em}}
.lgA>h3{{background:var(--Aw);color:var(--A)}}
.lgB>h3{{background:var(--Bw);color:var(--B)}}
.lgC>h3{{background:var(--Cw);color:var(--C)}}
.lg-row{{padding:11px 16px;border-bottom:1px solid var(--rule2)}}
.lg-row:last-child{{border-bottom:0}}
.lg-row>header{{display:flex;gap:10px;align-items:center;margin-bottom:7px}}
.lg-n{{font:11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut)}}
.tp-grid{{display:grid;gap:3px}}
.tp{{display:grid;grid-template-columns:62px 1fr;gap:10px;font-size:12.5px}}
.tp-n{{color:var(--mut);font:11px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}
.tp-v em{{font-style:normal;color:var(--mut)}}
.occ{{color:var(--mut);font-size:11px;margin-left:6px}}
.chip{{font:600 11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;padding:4px 7px;
border-radius:3px;letter-spacing:.02em;white-space:nowrap}}
.cA{{background:var(--Aw);color:var(--A)}}
.cB{{background:var(--Bw);color:var(--B)}}
.cC{{background:var(--Cw);color:var(--C)}}
.ctl{{position:sticky;top:0;z-index:5;background:var(--ground);
padding:16px 0 12px;border-bottom:1px solid var(--rule);
display:flex;flex-wrap:wrap;gap:12px;align-items:center}}
input[type=search]{{flex:1 1 240px;min-width:200px;padding:8px 12px;font:14px/1.4 inherit;
background:var(--surface);color:var(--ink);border:1px solid var(--rule);border-radius:3px}}
input:focus-visible,button:focus-visible{{outline:2px solid var(--focus);outline-offset:1px}}
.fset{{display:flex;flex-wrap:wrap;gap:4px}}
.fc{{font:600 11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;padding:6px 8px;
border:1px solid transparent;border-radius:3px;cursor:pointer;opacity:.42}}
.fc.on{{opacity:1;border-color:currentColor}}
#cnt{{font:12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);
margin-left:auto}}
.tw{{overflow-x:auto;border:1px solid var(--rule);border-radius:3px;background:var(--surface)}}
table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}}
thead th{{position:sticky;top:0;background:var(--raise);border-bottom:1px solid var(--rule);
font:600 11px/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.06em;
text-transform:uppercase;color:var(--mut);padding:10px;text-align:left;white-space:nowrap;
cursor:pointer;user-select:none}}
thead th.gA{{color:var(--A);border-left:2px solid var(--A)}}
thead th.gB{{color:var(--B);border-left:2px solid var(--B)}}
thead th.gC{{color:var(--C);border-left:2px solid var(--C)}}
tbody td{{padding:7px 10px;border-bottom:1px solid var(--rule2);font-size:13px}}
tbody tr:hover td{{background:var(--raise)}}
.nm{{font-weight:500;min-width:230px}}
.pop{{color:var(--mut);font:12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;
text-align:right}}
.kA{{border-left:2px solid var(--Aw)}}
.kB{{border-left:2px solid var(--Bw)}}
.kC{{border-left:2px solid var(--Cw)}}
.mg{{white-space:nowrap;min-width:104px}}
.mv{{font:12px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);
display:inline-block;width:38px;text-align:right}}
.bar{{display:inline-block;width:48px;height:3px;background:var(--rule);
margin-left:8px;vertical-align:middle;border-radius:2px;overflow:hidden}}
.bar i{{display:block;height:100%;background:var(--mut);opacity:.55}}
footer{{margin-top:38px;color:var(--mut);font-size:12.5px;max-width:70ch}}
@media (max-width:640px){{.mast{{padding-top:30px}}h1{{font-size:24px}}}}
</style>
<div class="wrap">
<div class="mast">
<h1>Relocation regimes across 286 US metro areas</h1>
<p class="sub">Every contiguous-US metropolitan statistical area above 150,000 people,
read under three mutually incompatible astrological frameworks. Whole sign and Placidus
are not two measurements of one thing; they are different definitions of what a house is.
So the three readings sit side by side and are never combined.</p>
<div class="crit">
<span><b>population</b> Census cbsa-est2024, POPESTIMATE2024</span>
<span><b>coordinates</b> Census 2023 Gazetteer, CBSA internal points</span>
<span><b>filter</b> MSA &gt; 150,000, contiguous US</span>
<span><b>additions</b> none</span><span><b>removals</b> none</span>
</div>
<p class="warn"><b>There is no overall column, and adding one would be an error.</b>
The three maps are built on incompatible premises, so agreement between them is not
evidence. A city favoured by all three is not more likely to be right; it usually just
sits far from every boundary. <b>Margin</b> measures miles to the nearest boundary
<em>within that same map</em> — how far you could settle off-centre before the reading
changes. It is not a quality score.</p>
</div>
<h2>What each regime says</h2>
<div class="legends">
<section class="lg lgA"><h3>Map A <small>{FULL['A']}</small></h3>{leg('A')}</section>
<section class="lg lgB"><h3>Map B <small>{FULL['B']}</small></h3>{leg('B')}</section>
<section class="lg lgC"><h3>Map C <small>{FULL['C']}</small></h3>{leg('C')}</section>
</div>
<h2>The metro areas</h2>
<div class="ctl">
<input type="search" id="q" placeholder="Search metro area or state…" aria-label="Search">
<div class="fset">{chips('A')}</div><div class="fset">{chips('B')}</div>
<div class="fset">{chips('C')}</div>
<span id="cnt"></span>
</div>
<div class="tw"><table>
<thead><tr>
<th data-s="t">Metro area</th><th data-s="n" class="pop">Population</th>
<th class="gA" data-s="s">Map A</th><th class="gA" data-s="n">Margin</th>
<th class="gB" data-s="s">Map B</th><th class="gB" data-s="n">Margin</th>
<th class="gC" data-s="s">Map C</th><th class="gC" data-s="n">Margin</th>
</tr></thead><tbody id="tb">{trs}</tbody></table></div>
<footer>Birth data 7 June 1996, 19:35 UT, Pittsburgh PA. Topics are identity (1st),
home (4th), travel (9th) and career (10th); each reading gives the house ruler, the
house that ruler occupies, and the planets occupying the house. Money, partnership and
children are excluded: their rulership disagrees 43–63% of the time across conventions,
so no stable reading exists for them.</footer>
</div>
<script>
const tb=document.getElementById('tb'),q=document.getElementById('q'),
cnt=document.getElementById('cnt'),all=[...tb.rows],F={{A:new Set(),B:new Set(),C:new Set()}};
function run(){{const s=q.value.trim().toLowerCase();let n=0;
for(const r of all){{const ok=(!s||r.dataset.n.includes(s))
&&(!F.A.size||F.A.has(r.dataset.a))&&(!F.B.size||F.B.has(r.dataset.b))
&&(!F.C.size||F.C.has(r.dataset.c));r.hidden=!ok;if(ok)n++;}}
cnt.textContent=n+' of {len(rows)} shown';}}
q.addEventListener('input',run);
for(const b of document.querySelectorAll('.fc'))b.addEventListener('click',()=>{{
const m=b.dataset.m,l=b.dataset.l;F[m].has(l)?F[m].delete(l):F[m].add(l);
b.classList.toggle('on');run();}});
let last=-1,dir=1;
document.querySelectorAll('thead th').forEach((th,i)=>th.addEventListener('click',()=>{{
dir=(last===i)?-dir:1;last=i;const k=th.dataset.s;
all.sort((x,y)=>{{const a=x.cells[i],b=y.cells[i];
if(k==='n')return dir*((+a.dataset.v||0)-(+b.dataset.v||0));
return dir*a.textContent.trim().localeCompare(b.textContent.trim());}});
for(const r of all)tb.appendChild(r);}}));
run();
</script>
""")
print("wrote msa_page.html")
