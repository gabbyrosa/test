#!/usr/bin/env python3
"""Generate the two-zodiac controlled reading as a page."""
import html, json

INV = [
 ("Sect", "Day chart in both. Sect light the Sun; benefic of the sect Jupiter; malefic of the sect Saturn; <b>Mars contrary to sect</b>."),
 ("Lord of the Ascendant", "Cadent, in the 9th house, peregrine, in both. Only its identity changes: Venus tropical, Mercury sidereal."),
 ("Sun", "9th house, <b>in its planetary joy</b>, peregrine, in both."),
 ("Moon", "6th house in both."),
 ("Jupiter", "4th house, angular, in both."),
 ("Saturn", "7th house, angular, in both."),
 ("Venus", "<b>Combust at 4.52°</b> in both."),
 ("Mars", "<b>In detriment</b>, with participating triplicity, in both."),
 ("Lot of Fortune", "10th house in both. Prenatal syzygy 3rd house in both."),
 ("Aspects", "Ten of the classical aspects appear in both, including every tropical aspect that carries reception: Sun–Venus 4.52°, Mercury–Mars 2.47°, <b>Moon sextile Jupiter 6.94° with reception</b>, Sun square Moon 8.34°, <b>Jupiter square Saturn 9.88° with reception</b>, Sun–Saturn, Venus–Saturn, Moon–Venus, Moon–Mercury, Moon–Mars."),
 ("House placement", "Five of seven planets keep their house. Only Mercury and Mars move, both from the 8th to the 9th."),
]

S = [
 dict(id="asc", t="The Ascendant and its lord",
  tf="Ascendant 16°05′ Libra. Lord Venus at 21°50′ Gemini, 9th house, cadent, peregrine, combust 4.52°, retrograde. Venus is in aversion to Jupiter, to Mercury and to Mars.",
  td="The significator of the native is a benefic, essentially undignified, in a cadent but advantageous place, obscured by the Sun, and unable to behold the benefic of the sect.",
  te=["Matters of self may be governed by evaluative or relational faculties rather than assertive ones.",
      "Support relevant to the self may not arrive through the channels that ordinarily carry it.",
      "The significator's own resources are borrowed rather than native, since it holds no dignity where it stands."],
  sf="Ascendant 22°16′ Virgo. Lord Mercury at 0°17′ Taurus, 9th house, cadent, peregrine, free of the beams, direct, conjunct Mars within 2.47°. Mercury is in aversion to Jupiter.",
  sd="The significator of the native is the neutral planet, essentially undignified, in a cadent but advantageous place, unobscured, and joined to the contrary-to-sect malefic.",
  se=["Matters of self may be governed by analytical, discriminating or communicative faculties.",
      "The significator is in immediate contact with the chart's most difficult planet, which may colour how those faculties operate.",
      "Unlike the tropical case it is free of the beams, so its operation is not obscured."]),

 dict(id="jup", t="Jupiter — the crux of the whole comparison",
  tf="15°54′ Capricorn, <b>in fall</b>, 4th house, angular, retrograde, free of the beams. Aspects four planets: sextile Moon (6.94°, receiving it by domicile), trine Mercury (8.19°), trine Mars (10.66°), square Saturn (9.88°). Saturn is in the 10th sign from Jupiter and so overcomes it.",
  td="The benefic of the sect is angular and essentially debilitated, connected to most of the chart, and dominated by the malefic of the sect by superior square.",
  te=["Benefit may be widely distributed but operate under constraint.",
      "Assistance may be conditional, delayed, or subject to structure it does not set.",
      "The domicile reception of the Moon is the strongest supportive link in the chart and it is intact here."],
  sf="22°06′ Sagittarius, <b>in domicile</b>, 4th house, angular, retrograde, free of the beams. <b>In aversion to the Sun, Mercury, Venus and Mars.</b> Aspects only the Moon (sextile 6.94°, receiving it by bound) and Saturn (square 9.88°). Saturn overcomes it here too.",
  sd="The benefic of the sect is angular and in its own domicile, but cannot behold four of the six other planets. Its reach is confined to the Moon and to the malefic that dominates it.",
  se=["Benefit may be intrinsically sound but reach comparatively few areas.",
      "The one channel it does hold, to the Moon, may carry disproportionate weight.",
      "Being overcome by Saturn is present in both charts and is not relieved by the improved dignity."]),

 dict(id="venus", t="Venus",
  tf="21°50′ Gemini, peregrine, 9th house, cadent, retrograde, <b>combust 4.52°</b>, occidental. Bonified by nothing; maltreated by nothing. In aversion to Jupiter, Mercury and Mars.",
  td="A benefic with no essential dignity, obscured by the Sun, isolated from both the other benefic and both malefics, and additionally the lord of the Ascendant.",
  te=["Venusian significations may be central by rulership while difficult to observe from outside.",
      "Neither helped nor harmed by the other planets, its expression may be unusually self-contained.",
      "Retrogradation may indicate matters revisited rather than advanced."],
  sf="28°01′ Taurus, <b>in domicile with triplicity</b>, 9th house, cadent, retrograde, <b>combust 4.52°</b>, occidental. Co-present with the Sun, Mercury and Mars. Maltreated by Mars co-present; bonified by nothing.",
  sd="A benefic in its own domicile and trigon, still obscured by the Sun, and in immediate contact with the contrary-to-sect malefic. A final dispositor of the chart.",
  se=["Venusian significations may be natively well-resourced.",
      "Those resources sit in direct contact with the chart's most difficult planet, which may complicate their expression.",
      "Combustion is identical in both charts and is not relieved by the improved dignity."]),

 dict(id="mars", t="Mars and Saturn — reach",
  tf="Mars 26°33′ Taurus, in detriment, contrary to sect, 8th house. Aspects Mercury (conjunction 2.47°), Jupiter (trine), Moon (sextile). <b>In aversion to the Sun, Venus and Saturn.</b> Saturn 6°01′ Aries, in fall, in sect, 7th, angular; aspects Sun, Venus, Jupiter; averse to Moon, Mercury, Mars.",
  td="The contrary-to-sect malefic is sealed off from the significators of vitality and of the native. Both malefics have limited reach.",
  te=["Difficulty may be localised rather than pervasive.",
      "The topics Mars governs, and the mind it is joined to, may carry that difficulty while other areas remain untouched.",
      "Saturn being in sect moderates its expression regardless of its fall."],
  sf="Mars 2°45′ Taurus, in detriment, contrary to sect, 9th house. Aspects Mercury, the <b>Sun</b>, <b>Venus</b>, the Moon and Saturn. <b>Averse only to Jupiter.</b> Saturn 12°13′ Pisces, peregrine rather than in fall, in sect, 7th, angular; aspects Sun, Mercury, Venus, Mars, Jupiter; averse only to the Moon.",
  sd="Both malefics reach nearly the whole chart. The contrary-to-sect malefic is in immediate contact with the sect light, the lord of the Ascendant and the domiciled Venus.",
  se=["Difficulty may be distributed across most significators rather than confined.",
      "Saturn is better conditioned here and simultaneously more widely connected.",
      "The improvement in Saturn's dignity and the increase in Mars's reach occur together and should be weighed together."]),

 dict(id="disp", t="Dispositors",
  tf="Every chain loops. Sun → Mercury → Venus → Mercury. Moon → Jupiter → Saturn → Mars → Venus → Mercury → Venus. No final dispositor exists, because no planet occupies its own domicile. Mercury and Venus are in mutual reception by domicile but are <b>in aversion</b> and cannot behold one another.",
  td="No significator resolves. Every chain refers onward indefinitely and terminates in an exchange between two planets that cannot see each other.",
  te=["Matters may resolve by referral and exchange rather than by arriving somewhere settled.",
      "The mutual reception can be reported as a structural fact; it should not be described as active, since the two planets are in aversion.",
      "This is a property of the configuration, not a prediction about outcomes."],
  sf="Every chain terminates. Sun → Venus (own domicile). Moon → Saturn → Jupiter (own domicile). Mercury, Mars → Venus. Saturn → Jupiter. <b>Two final dispositors, Venus and Jupiter, both in domicile.</b>",
  sd="Every significator in the chart resolves into one of two planets, each operating from its own resources.",
  se=["Matters may consistently return to two stable centres.",
      "The two endpoints govern, respectively, the 2nd and 9th houses and the 4th and 7th houses.",
      "A resolved dispositor structure describes how significations refer, not whether outcomes are favourable."]),

 dict(id="home", t="The 4th house — home, parents, endings",
  tf="4th is Capricorn. <b>Lord Saturn</b>, in fall but with participating triplicity, in sect, direct, free of the beams, angular <b>in the 7th</b>. Occupied by Jupiter, in fall. Lot of Spirit falls here, lord the same Saturn.",
  td="The topic is administered by the malefic of the sect, essentially debilitated but well placed by sect, motion and quadrant, and located in the house of marriage. The house is occupied by the benefic of the sect, also debilitated.",
  te=["Decisions concerning home may involve a partner substantially, since the two houses share a lord.",
      "Establishing a home may involve commitment, negotiation, delay or long planning.",
      "The presence of Jupiter suggests generosity of intent operating under limitation.",
      "The rulership link is a structural relationship between two topics; it does not establish that one cannot be resolved without the other."],
  sf="4th is Sagittarius. <b>Lord Jupiter</b>, in domicile, angular, <b>occupying the house it rules</b>. Lot of Spirit moves to the 5th; its lord Saturn remains in the 7th.",
  sd="The topic is administered by the benefic of the sect, in its own domicile, in the house itself. But that lord is in aversion to four of the six other planets.",
  se=["The topic may be natively well-resourced and comparatively self-contained.",
      "Because Jupiter here rules the 4th and the 7th, home and marriage still share a lord, though a differently conditioned one.",
      "Jupiter's aversions mean this well-conditioned significator has limited contact with the rest of the chart."]),

 dict(id="seventh", t="The 7th house — marriage and partners",
  tf="7th is Aries. <b>Lord Mars</b>, in detriment and contrary to sect, in the 8th. The house is occupied by <b>Saturn</b>, in fall but in sect, angular. South Node also here.",
  td="The topic is governed by the chart's most difficult planet from a place in aversion to the Ascendant, and occupied by the malefic of the sect.",
  te=["The topic may carry weight, seriousness or duration.",
      "Saturn being in sect suggests structure and time rather than harm.",
      "The lord's placement in the 8th, a place averse to the Ascendant, is a further complication of the significator, not a statement about outcomes."],
  sf="7th is Pisces. <b>Lord Jupiter</b>, in domicile, angular in the 4th. The house is occupied by <b>Saturn</b>, peregrine rather than in fall, in sect, angular.",
  sd="The topic is governed by the benefic of the sect in its own domicile, and occupied by the malefic of the sect in a materially better condition than in the tropical chart.",
  se=["Both significators of the topic are better conditioned here than in the tropical configuration.",
      "Saturn remains present in the house in both charts; only its dignity changes.",
      "Jupiter's aversions apply here as elsewhere."]),

 dict(id="ninth", t="The 9th house — travel, the divine, learning",
  tf="9th is Gemini. Lord Mercury in the 8th. Occupied by the <b>Sun in its joy</b> and by Venus, the lord of the Ascendant. The Sun and Venus are in aversion to Mercury and Mars in the 8th.",
  td="The most emphasised place in the chart holds the sect light in its joy together with the significator of the native. Its own lord sits in a place averse to the Ascendant.",
  te=["Matters of the foreign, of learning, or of worldview may be prominent.",
      "The two planets here cannot behold the two in the 8th, so the emphasis may operate in isolation from the topics Mercury and Mars govern."],
  sf="9th is Taurus. Lord Venus, in domicile, <b>in the house itself</b>. Occupied by the Sun in its joy, Mercury, Venus and Mars — <b>four planets</b>.",
  sd="The most emphasised place in the chart holds four of seven planets including the sect light in its joy and the house's own lord in domicile. It also holds the contrary-to-sect malefic.",
  se=["The emphasis on this topic is considerably heavier than in the tropical configuration.",
      "The house's lord operating from within the house is a self-contained arrangement.",
      "Mars's presence places the chart's most difficult planet inside its most emphasised house."]),

 dict(id="tenth", t="The 10th house and the Lot of Fortune",
  tf="10th is Cancer, empty. <b>Lord the Moon in the 6th</b>, a place averse to the Ascendant. The Moon holds participating triplicity and no debility, and is fast in motion. <b>Fortune falls in the 10th</b>, lord the same Moon.",
  td="Action and standing are governed by the best-conditioned planet in the chart, operating from a place that cannot behold the Ascendant. Fortune occupies the house.",
  te=["Standing may be built through the topics of the 6th — labour, service, regimen — rather than through the house of action directly.",
      "Fortune's presence gives the house material weight the empty sign would not otherwise carry."],
  sf="10th is Gemini, empty. <b>Lord Mercury in the 9th</b>, an advantageous place, conjunct Mars. <b>Fortune falls in the 10th</b>, lord the same Mercury.",
  sd="Action and standing are governed by the lord of the Ascendant, from the chart's most emphasised house, in an advantageous place — but joined to the contrary-to-sect malefic.",
  se=["Standing and identity share a lord here, which they do not in the tropical chart.",
      "Fortune's lord operating from the 9th ties material circumstance to the topics of that house."]),

 dict(id="money", t="The 2nd and 8th — livelihood and others' goods",
  tf="2nd is Scorpio, lord <b>Mars in detriment</b>, in the 8th. 8th is Taurus, lord Venus, combust and cadent in the 9th. Both places are averse to the Ascendant.",
  td="Both significators of material topics are compromised, and both houses are in aversion to the Ascendant.",
  te=["This is a traditional signature of difficulty in the <em>significators</em> of these topics.",
      "It is not, on its own, a prediction about financial outcomes; that would require timing techniques not applied here.",
      "Fortune in the 10th under a well-conditioned Moon runs the other way and should be weighed against it."],
  sf="2nd is Libra, lord <b>Venus in domicile</b>, in the 9th. 8th is Aries, lord <b>Mars in detriment</b>, in the 9th.",
  sd="The lord of the 2nd is in its own domicile; the lord of the 8th remains in detriment. Both operate from the 9th, an advantageous place.",
  se=["The livelihood significator is materially better conditioned here than in the tropical chart.",
      "The 8th's significator is unchanged in dignity but changes house.",
      "The same caution applies: this describes significators, not outcomes."]),

 dict(id="aversion", t="Aversions overall",
  tf="<b>Nine</b> pairs in aversion: Sun/Mercury, Sun/Mars, Sun/Jupiter, Moon/Saturn, Mercury/Venus, Mercury/Saturn, Venus/Mars, Venus/Jupiter, Mars/Saturn.",
  td="The chart is markedly fragmented. Several significators, including the lord of the Ascendant and the benefic of the sect, cannot behold one another.",
  te=["Areas of life may operate with relative independence from each other.",
      "Fragmentation is a structural description and carries no inherent valuation."],
  sf="<b>Five</b> pairs in aversion: Sun/Jupiter, Moon/Saturn, Mercury/Jupiter, Venus/Jupiter, Mars/Jupiter. <b>Four of the five involve Jupiter.</b>",
  sd="The chart is markedly more interconnected, with the isolation concentrated almost entirely on the benefic of the sect.",
  se=["Areas of life may be mutually implicated rather than independent.",
      "The one isolated significator is the one best conditioned, which is the reverse of the tropical arrangement."]),
]

def blk(f, d, e, cls):
    lis = "".join(f"<li>{x}</li>" for x in e)
    return (f'<div class="pane {cls}">'
            f'<div class="lv fact"><span class="lb">Technical fact</span><p>{f}</p></div>'
            f'<div class="lv del"><span class="lb">Traditional delineation</span><p>{d}</p></div>'
            f'<div class="lv exp"><span class="lb">Possible lived expressions</span>'
            f'<ul>{lis}</ul></div></div>')

secs = "".join(
    f'<section id="{s["id"]}"><h2>{s["t"]}</h2><div class="pair">'
    f'<div class="col"><h3 class="ht">Tropical</h3>{blk(s["tf"], s["td"], s["te"], "trop")}</div>'
    f'<div class="col"><h3 class="hs">Lahiri sidereal</h3>{blk(s["sf"], s["sd"], s["se"], "sid")}</div>'
    f'</div></section>' for s in S)

invrows = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in INV)
nav = "".join(f'<a href="#{s["id"]}">{s["t"].split(" — ")[0]}</a>' for s in S)

open("/home/user/test/two_zodiacs.html", "w").write(f"""<title>Two Zodiacs, One Method</title>
<style>
:root{{--pg:#F5F6F8;--sf:#FFF;--rz:#FAFBFC;--ink:#15181F;--mut:#646C7A;--rl:#E0E4EA;
--rl2:#EDF0F4;--trop:#A6552C;--sid:#3A5A8C;--tropw:#F7EFE8;--sidw:#EBF0F7;--fc:#3A5A8C}}
@media(prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--pg:#13161C;--sf:#1A1E26;
--rz:#20252E;--ink:#E5E8EF;--mut:#98A0AE;--rl:#282E38;--rl2:#1F242C;--trop:#D18A5A;
--sid:#7C9FD4;--tropw:#241C16;--sidw:#161C27;--fc:#7C9FD4}}}}
:root[data-theme="dark"]{{--pg:#13161C;--sf:#1A1E26;--rz:#20252E;--ink:#E5E8EF;--mut:#98A0AE;
--rl:#282E38;--rl2:#1F242C;--trop:#D18A5A;--sid:#7C9FD4;--tropw:#241C16;--sidw:#161C27;--fc:#7C9FD4}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--pg);color:var(--ink);
font:16px/1.6 "Iowan Old Style",Palatino,"Palatino Linotype",Georgia,serif;
-webkit-font-smoothing:antialiased}}
.w{{max-width:1180px;margin:0 auto;padding:0 24px 90px}}
header.m{{padding:52px 0 26px;border-bottom:1px solid var(--rl)}}
h1{{font:600 34px/1.14 inherit;margin:0 0 16px;letter-spacing:-.012em;text-wrap:balance}}
.lede{{max-width:64ch;margin:0 0 18px;color:var(--mut)}}
.spec{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;
margin-top:22px}}
.spec div{{background:var(--sf);border:1px solid var(--rl);border-radius:2px;padding:12px 14px}}
.spec b{{display:block;font:600 10.5px/1 ui-monospace,SFMono-Regular,Menlo,monospace;
letter-spacing:.13em;text-transform:uppercase;color:var(--mut);margin-bottom:7px}}
.spec p{{margin:0;font-size:13.5px}}
.warn{{margin-top:20px;border-left:2px solid var(--sid);padding:2px 0 2px 15px;
font-size:14px;color:var(--mut);max-width:70ch}}
.warn b{{color:var(--ink)}}
h2{{font:600 22px/1.25 inherit;margin:0 0 18px;letter-spacing:-.008em;text-wrap:balance}}
section{{margin-top:52px;scroll-margin-top:66px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:860px){{.pair{{grid-template-columns:1fr}}}}
h3.ht,h3.hs{{font:600 11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.15em;
text-transform:uppercase;margin:0 0 9px;padding:7px 11px;border-radius:2px}}
h3.ht{{color:var(--trop);background:var(--tropw)}}
h3.hs{{color:var(--sid);background:var(--sidw)}}
.pane{{background:var(--sf);border:1px solid var(--rl);border-radius:2px;overflow:hidden;
height:calc(100% - 34px)}}
.pane.trop{{border-top:2px solid var(--trop)}}
.pane.sid{{border-top:2px solid var(--sid)}}
.lv{{padding:13px 16px;border-bottom:1px solid var(--rl2)}}
.lv:last-child{{border-bottom:0}}
.lb{{display:block;font:600 10px/1 ui-monospace,SFMono-Regular,Menlo,monospace;
letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin-bottom:8px}}
.lv p,.lv ul{{margin:0}}
.fact{{background:var(--rz)}}
.fact p{{font:13px/1.62 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut)}}
.fact b{{color:var(--ink);font-weight:600}}
.del p{{font-size:15.5px}}
.exp{{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}}
.exp ul{{padding-left:17px;font-size:13.5px;color:var(--mut)}}
.exp li{{margin-bottom:5px}}
.exp li:last-child{{margin-bottom:0}}
nav{{position:sticky;top:0;z-index:4;background:var(--pg);border-bottom:1px solid var(--rl);
padding:11px 0;display:flex;gap:5px;overflow-x:auto;margin-top:34px}}
nav a{{font:11px/1 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);
text-decoration:none;padding:6px 9px;border:1px solid transparent;border-radius:2px;
white-space:nowrap}}
nav a:hover{{color:var(--ink);border-color:var(--rl)}}
nav a:focus-visible{{outline:2px solid var(--fc);outline-offset:1px}}
table.inv{{width:100%;border-collapse:collapse;background:var(--sf);
border:1px solid var(--rl);border-radius:2px}}
table.inv th{{text-align:left;vertical-align:top;padding:10px 14px;width:190px;
font:600 12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);
border-bottom:1px solid var(--rl2)}}
table.inv td{{padding:10px 14px;border-bottom:1px solid var(--rl2);font-size:14.5px}}
table.inv tr:last-child th,table.inv tr:last-child td{{border-bottom:0}}
footer{{margin-top:56px;padding-top:22px;border-top:1px solid var(--rl);color:var(--mut);
font-size:13.5px;max-width:72ch}}
@media(max-width:640px){{h1{{font-size:26px}}header.m{{padding-top:34px}}}}
</style>
<div class="w">
<header class="m">
<h1>Two zodiacs, one method</h1>
<p class="lede">A controlled experiment on a single nativity. One technique set is applied
identically to two zodiacs, so that the only variable is tropical longitude against Lahiri
sidereal longitude. Every claim is separated into three levels, so you can see exactly where
calculation ends and interpretation begins.</p>
<div class="spec">
<div><b>Held constant</b><p>Whole-sign houses; seven traditional planets; sect; domicile,
exaltation, triplicity and bounds; detriment and fall; planetary joys; quadrant; traditional
rulership and dispositors; the five classical aspects taken whole-sign; dignity-based
reception; the Lots of Fortune and Spirit; the prenatal syzygy.</p></div>
<div><b>Removed from both</b><p>Almuten figuris; faces as interpretive evidence;
semi-sextiles and quincunxes, which are aversions rather than aspects; the outer planets
and modern rulerships; modern nodal interpretation.</p></div>
<div><b>Nativity</b><p>7 June 1996, 19:35 UT, Pittsburgh, Pennsylvania. Day chart in both
zodiacs. Lahiri ayanamsa at birth 23.8073°.</p></div>
</div>
<p class="warn"><b>On labelling.</b> The tropical column applies a Hellenistic technique set
to the zodiac the tradition itself used. The sidereal column is an <b>experimental
application</b> of that same set to Lahiri longitudes. It is not historical Hellenistic
practice and is not presented as such. In the Hellenistic period the two zodiacs sat within
about two and a half degrees of one another, so the surviving corpus cannot settle the
question either way.</p>
</header>
<nav>{nav}</nav>
<section id="inv"><h2>What the zodiac change does not touch</h2>
<table class="inv">{invrows}</table></section>
{secs}
<footer>Three levels throughout. <b>Technical fact</b> is calculation and is checkable.
<b>Traditional delineation</b> is what the technique set says about that calculation.
<b>Possible lived expressions</b> are deliberately plural and probabilistic: they are the
range of ways a delineation might show up, not a prediction that it will. Where a single
behavioural claim appears anywhere below, it is a mistake.</footer>
</div>
""")
print("wrote two_zodiacs.html")
