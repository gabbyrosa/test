# Doctrinal provenance audit — Jyotish natal reading

Audit only. The chart is not recomputed and the design is not touched. Two
overstatements named in the review are corrected in the document; nothing else
is rewritten.

---

## CLOSED — all three actioned

The three parked corrections were applied as one discrete audit. Every landing
site listed below was edited and then grep-verified; zero stale claims remained.

| # | Correction | Outcome |
|---|---|---|
| 1 | Functional-table errors | Moon corrected to **malefic** (stated in the text). Sun corrected to **"role will depend on his association"**, not classed either way. Saturn relabelled **not named for this lagna, verdict inferred**. Mars, Jupiter, Mercury and Venus confirmed as they stood. Jupiter's two mechanisms now separated: ch. 34 vv. 2–7 mute a benefic, ch. 34 vv. 31–32 class Guru a malefic for Kanya outright. |
| 2 | Yoga citation | Dharma-Karmadhipati now rests on ch. 34 vv. 31–32 naming the Venus–Mercury yuti as yoga-producing for Kanya specifically, rather than on the generic kendra–trikona rule. Carries **low textual stability** inline. |
| 3 | Node drishti removal | Both cast rows removed from §6, §14 rebuilt with separate cast and received rows, §17 conventions row changed to **excluded**, citing ch. 34 vv. 16–17. |

**Two things surfaced during the audit that were not on the list.**

Removing the node casts leaves **Saturn and Ketu receiving no drishti at all**,
joining the Moon. Three of nine bodies are now unaspected, where the document
previously had one.

And the claim that Saturn aspects "seven of the other eight bodies" was an
**arithmetic error**, present in two places and independent of the node
question. It is six: Sun, Mars, Mercury, Jupiter, Venus and Rahu. The two it
misses are the Moon and Ketu.

## Audited baseline

**Commit `12a79c71c8e3762776c1f807522fe5cb53857869`** (short `12a79c7`) is the audited baseline. Referenced by
SHA rather than by tag: this session's git credentials return HTTP 403 on tag
refs, consistently across retries, so `jyotish-audit-baseline` exists locally
but could not be pushed and will not survive the container. The SHA is
immutable and is on the remote branch, so it anchors the state just as well.

**What this state claims:**

- The three parked corrections are actioned — functional table, yoga citation, node drishti removal.
- A stale-claim sweep across 20 searched patterns returns zero instances.
- Two count errors were found by enumeration and fixed: Saturn aspects six of the other eight bodies, not seven; six of nine grahas resolve into the Sun–Mars cycle, not seven.
- One invented attribution withdrawn ("Parashara treats an unaspected Moon as self-referring"); one softened and given the verse that supports its mechanism.
- Section 17's claim that a cleanup had already happened is corrected, and the sequence recorded.

**What this state does not claim:** that the document is verified. Four
provenance questions remain open below, with four distinct dispositions. The
next audit should be able to fail cleanly against this SHA rather than against
a standard that moved underneath it.

## STILL OPEN — four items, four different dispositions

Not to be rolled into a generic "citations cleanup." Each needs a different
kind of work, and merging them would hide which question is actually unanswered.

| Item | Problem type | The question that has to be answered first |
|---|---|---|
| **Nakshatra-chain framing (§5)** | Provenance / framework | Not "find a citation." Whether the technique belongs inside the declared framework at all. Confirmed KP-weighted; the choice is to relabel the section or drop its interpretive weight. |
| ~~Lakshmi yoga conditions~~ | Doctrinal verification | **CLOSED — see below. Outcome: confirmed, rule replaced, false qualification withdrawn, real qualification attached.** |
| **Hora doctrine** | Implementation + provenance | Item 4, still open. Baladi split out and CLOSED separately below. |
| ~~Rashi sandhi~~ | Definition + provenance | **CLOSED — see below. Outcome: no sourced threshold exists; claim withdrawn, no verdict given.** |

### Item 1 of 4 — Lakshmi Yoga — **CLOSED: forms under the ordinary reading of Phaladeepika 6.21**

**Source.** *Phaladeepika* of Mantreswara, ch. 6 v. 21, wisdomlib text-and-translation
edition. Textual stability: **not tested** — one translation consulted.

> "If the lord of the 9th and Venus be posited in their own or exaltation houses
> identical with a Trikona or a Kendra, the resulting Yoga is Lakshmi."

**The rule the document was using was wrong twice.** It read "the 9th lord in its
own sign or exaltation, in a kendra or trikona, with a strong Lagna lord." That
**omitted the condition on Venus** and **added a Lagna-lord condition verse 21 does
not contain**. Verse 21 is silent on the Lagna lord, and equally silent on
combustion, retrogression and affliction.

The document had then reported the yoga as forming "with one condition partially
met" — a qualification manufactured out of a requirement that does not exist. That
is the inverse of the usual failure: not a caveat that decayed, but a caveat
invented from a misremembered rule.

**Test against verse 21 as written.**

| Condition | Chart | Verdict |
|---|---|---|
| Lord of the 9th, own or exaltation, in trikona or kendra | 9th from Virgo is Taurus, so the 9th lord is Venus; Venus 28°01′ Taurus, own sign, in the 9th, a trikona | satisfied |
| Venus, own or exaltation, in trikona or kendra | same placement | satisfied |

**Outcome: forms under the ordinary reading of 6.21.** Both stated conditions are
met and the yoga retains principal status.

**Citation error, corrected.** This audit first recorded the verse as **6.28**. That
was wrong — 6.28 defines Srikantha, Srinatha and Virinchi. Caught on review. My
automated reads of the wisdomlib page returned the verse number inconsistently
(first 28, then 21 with an internally contradictory answer about what 21 contains),
so the number now rests on a human check rather than on my own reading.

**Consequence for the citation format.** The *passage* field is only ever as good as
the read that produced it, and can fail independently of the text being correct. The
four-field citation shape needs passage-number confidence tracked separately from
textual stability. Recorded here; propagated to CLAUDE.md.

**Real qualification, which replaces the false one.** For Virgo lagna the 9th lord
*is* Venus, so verse 21's two named roles collapse onto one graha and a single
placement does double duty. Enumerating all twelve lagnas, this occurs for exactly
**two — Virgo and Aquarius** — the only ones whose 9th sign is Taurus or Libra. The
other ten require two distinct grahas simultaneously dignified.

What this establishes is narrow: the yoga here **requires only one distinct graha to
be dignified rather than two**. That is a statement about how many bodies the
condition needs — not about the yoga being weaker or easier in effect. The earlier
wording, "a materially cheaper condition," overstated it in the direction of a
quality judgement and is withdrawn.

**Provenance of the one-graha reading: secondary.** Later and practical Jyotish
sources recognise this single-planet form for Virgo and Aquarius ascendants. Verse 21
itself names "the lord of the 9th and Venus" without separately discussing the case
where the two roles fall on the same graha, so the classical text does not explicitly
confirm the Virgo one-planet case.

**Not disqualifying, but still true.** Verse 21 says nothing about combustion or
navamsa dignity, so Venus being combust at 4°32′ and debilitated in D9 does not
block formation. Those travel with the claim regardless.

**Incidental findings from the same source, recorded but NOT actioned** (scope
discipline — these belong to no open item and would need their own pass):
Phaladeepika sloka 5 defines Kemadruma as the absence of Sunapha, Anapha and
Durudhara *and* no kendra association with the Moon — a condition the reading does
not state. Sloka 14 phrases Gaja Kesari as "the Moon in a Kendra position to
Jupiter," the mirror of the reading's phrasing; the relation is symmetric so the
verdict is unchanged.

**Landing sites edited:** §9 rule and test, §13 Saturn/Venus dasha, §15 Money,
§16 Theme I combo. Verified: old rule appears only inside the correction note as a
recorded quotation, zero live instances.

### Item 2 of 4 — Rashi sandhi — **CLOSED: threshold not establishable; claim withdrawn**

**Scope first.** The document used "sandhi" in two unrelated senses. *Bhava sandhi*
(§1, §17) is a computational definition I stated and implemented — the midpoint
between adjacent bhava madhyas — and is not in dispute. *Rashi sandhi* is the open
claim and landed in exactly two places, both about Mercury.

**Disclosure.** Mercury's position (0°16′53″ Taurus) was already known to me before
this search, so the threshold could not be fixed blind. Mitigation: report every
threshold variant found rather than selecting one, and record which side Mercury
falls on for each.

**Definition search — three searches, no classical passage found.**

| Source | Threshold given | Cites a text for the number? |
|---|---|---|
| secondary | 29°40′ of preceding rashi to **0°20′** of following | no |
| secondary (Sarbani Rath) | none stated; worked example places a graha "at rāśi sandhi" at **0°05′** | no |
| secondary, on **gandanta** | last/first 3°20′ at three junctions | **yes — attributed to Parāśara** |

**Test, both variants, computed.**

| Variant | Threshold | Mercury 0°16′53″ |
|---|---|---|
| 0°20′ band | 0°20′00″ | **inside by 3′07″** |
| 0°05′ scale | 0°05′00″ | **outside by 11′53″** |

**Outcome: no verdict.** The claim flips on a choice between two unsourced
conventions separated by 15 arcminutes, with Mercury sitting between them. Under
the rule that a measure with competing formulations and no way to choose produces
no number, none is produced. The attribution to "classical texts" is withdrawn as
unsupported.

**The one named attribution does not apply.** Gandanta — the severe form, attributed
to Parāśara (secondary) — covers Pisces–Aries, Cancer–Leo and Scorpio–Sagittarius,
the water-to-fire joins. **Aries–Taurus is not among them**, so gandanta is
inapplicable to Mercury at any degree.

**What this audit did and did not falsify.** It falsified *this document's*
attribution and *this document's* numerical implementation. It did not falsify the
concept of sandhi at sign boundaries, and it is not a finding that no such doctrine
exists. The precise result is: **no classical passage supporting the specific
numerical rashi-sandhi threshold used in this document was located.** A textual
source may surface later without making this audit wrong.

**What survives.** The geometric fact — Mercury is 17 arcminutes into Taurus, the
first graha by degree in that sign — is computed and stands on its own, with no
doctrinal weight attached. Mercury's Mrita avastha, the second counterweight in the
same passage, is untouched here; it belongs to item 3.

**Landing sites edited:** §4 Mercury (full note), §9 Dharma-Karmadhipati modification
(sandhi clause removed), §17 conventions table (new row: rashi sandhi **not used**).
Verified: the old attribution appears only inside the correction note as a recorded
quotation, zero live instances.

### Item 3 of 4 — Baladi avastha — **CLOSED: classification confirmed, weight scheme corrected**

Two questions, deliberately not collapsed.

**Q1 — Classification. CONFIRMED.** All nine bodies recomputed from degrees, not from
stored labels, against the sourced rule: five states of 6°, odd signs running
Bala→Mrita from 0°, even signs reversed. **Zero mismatches.** The parity rule was
validated independently by the invariant the sources state separately — 12°–18° must
be Yuva under *both* parities — which the implementation reproduces.

| graha | degree | parity | computed | document |
|---|---|---|---|---|
| Sun | 23°30′ Taurus | even | Kumara | Kumara |
| Moon | 15°09′ Aquarius | odd | Yuva | Yuva |
| Mars | 2°45′ Taurus | even | Mrita | Mrita |
| Mercury | 0°17′ Taurus | even | Mrita | Mrita |
| Jupiter | 22°06′ Sagittarius | odd | Vriddha | Vriddha |
| Venus | 28°02′ Taurus | even | Bala | Bala |
| Saturn | 12°12′ Pisces | even | Yuva | Yuva |
| Rahu / Ketu | 20°13′ | even | Kumara | Kumara |

**Q2 — Weight. NOT what the document claimed.** Four findings.

**(a) Category error, now withdrawn.** §10 called baladi *"a second, independent
measure agreeing with dig bala on the same point."* Shadbala has six named components
— Sthana, Dig, Kala, Cheshta, Naisargika, Drik. **Baladi is not among them.** It is a
separate scheme that does not feed the Shadbala total. Dig bala and baladi are not two
witnesses to one proposition, and presenting them as agreeing manufactured
corroboration out of two incommensurable things. This is rule 2 — non-independent
agreement — inverted: not two descriptions of one quantity, but two *different*
quantities treated as one.

**(b) What avasthas actually do.** Sources describe them as tempering how effectively
strength manifests, and specifically as modifying **the effectiveness of yogas**. Also:
a graha in Mrita that sits in its own or exaltation sign is better placed than one in
debilitation — so **Mrita does not mean inert**, and "the weakest" was the wrong gloss.

**(c) One use was better grounded than assumed.** §9 cites Mercury's Mrita avastha as
tempering the Dharma-Karmadhipati yoga. That is *precisely* what sources say avasthas
do. That use is strengthened with the attribution rather than weakened — the only place
in this pass where the audit improved a claim instead of cutting one.

**(d) Two specificities were mine, not the sources'.** §17 gave the multipliers as
"Bala ¼, Kumara ½, Yuva full, **Vriddha ¼**, **Mrita negligible**." Sources give Vriddha
as *"minimum"* and Mrita as *"gives no result"*. Corrected. The fractions remain
**unapplied**, and what they modify is not stated in commensurable units by any source
consulted.

**(e) Nodes: unsupported extension.** No source consulted states that baladi applies to
Rahu and Ketu. Their row is computed by the same arithmetic, marked as not relied on,
and flagged in §17.

**Provenance: secondary / standard practice throughout.** No primary passage was
reached for baladi. The degree scheme is consistent across sources; the weight language
is not.

**Scope of the finding.** What is corrected is this document's treatment of baladi as a
strength axis. The classification scheme itself survives intact and is now
independently verified.

**Landing sites:** 32 live strings enumerated first. Edited: §10 (opening claim, the
comparison paragraph, three table rows), §15 identity, §15 career, §9 modification
(strengthened), §17 formula block and fractions and a new nodes note, footer. Verified:
one stale string remains and it is the recorded quotation inside the correction.

---

Two of the original audit's own conclusions were also reversed by the search
addendum at the end of this file and are already recorded there: the Jupiter
"functional malefic" label for Virgo is textually supported, and the
per-lagna functional table is not a modern systematization.

---

## The limit of this audit, stated first

**I do not have Brihat Parashara Hora Shastra, Phaladeepika, Jataka Parijata,
Saravali, or any primary Sanskrit source in this environment.** Every
provenance judgement below comes from training knowledge, which is exactly the
kind of thing that can be confidently wrong about which text says what.

Consequences I am holding myself to:

- **No chapter and verse anywhere in this audit.** Inventing a citation would
  be worse than admitting I cannot supply one.
- Where I say something is "in BPHS," read it as *I believe it is, and this
  needs checking against the text before it is relied on.*
- I did not search the web for this. English-language Jyotish material online
  is overwhelmingly secondary, unsourced, and mutually copied, and citing it
  would launder low-quality sources into apparent authority. The claims below
  that need verification need a *text*, not a search result.

The audit is therefore useful for **finding what needs checking and what I got
structurally wrong**, and not as a substitute for consulting the sources.

## Categories used

| | Meaning |
|---|---|
| **1** | Believed directly supported by a named classical source |
| **2** | Standard later Parashari practice, widely held, grounding uncertain |
| **3** | School-dependent or contemporary practice |
| **4** | My own synthesis |

---

## The three most serious findings

Before the table, the three that actually damage the document:

**1. The nakshatra-chain apparatus is not Parashari, and the document says it
is.** Section 5 is largely a *Krishnamurti Paddhati*-flavoured technique
running under a banner that reads "Parashari only." Theme IV in the closing
summary rests on it. This is a framework-labelling failure of exactly the kind
this project exists to prevent, and it is mine.

**2. I attributed a claim to Parashara that I cannot source.** Section 3
states: *"Parashara treats an unaspected Moon as self-referring."* I have no
source for that sentence. The geometry (no graha aspects the Moon) is
computed and correct; the attribution is not.

**3. Counting Venus's retrogression as a weakness is probably backwards.** In
Shadbala, retrograde grahas receive *high* cheshta bala — retrogression is
classically a **strength**. The "turns inward, revisits, reworks" reading I
used is a modern and largely Western gloss. This removes one of the five
"independent measures" I stacked against Venus, and it compounds with the
D10/D7 correction below.

---

## Nakshatra parivartana and nakshatra-lord chains

| Claim | Current wording | Source / school | Confidence | Correction needed |
|---|---|---|---|---|
| Moon↔Rahu and Sun↔Mars are "nakshatra parivartana" | "a *nakshatra parivartana*, a mutual exchange at the nakshatra level" | **4.** *Parivartana* is a rashi-level term for exchange between two sign lords. I extended it to nakshatra lordship. I am not aware of a classical source naming a nakshatra-level exchange. | Low that it is classical; high that the configuration itself is real | Relabel as a mutual nakshatra relationship, state that I am borrowing the rashi term, and drop the implication that it carries rashi parivartana's classical weight |
| Nakshatra-lord chains as a structural map of the chart | Section 5, "seven of nine grahas resolve into or through the Sun–Mars loop" | **3.** Nakshatra lordship is classical *insofar as Vimshottari depends on it*. Chains-of-chains as a primary analytical device is characteristic of **KP (K.S. Krishnamurti, mid-20th c.)** and some contemporary nadi-influenced practice. | Medium-high | Relabel section 5 as contemporary/KP-influenced, or drop its interpretive weight. Computation is fine; the framing is not. |
| Theme IV, "the emotional apparatus runs separately from everything else" | Closing summary, built on the nakshatra network plus dispositor chains | **Mixed.** The *dispositor-chain* half is classical. The *nakshatra-chain* half is category 3. | Medium | Theme survives on the dispositor evidence alone. Say so, rather than presenting both halves as equally grounded. |

## Rahu and Ketu drishti

| Claim | Current wording | Source / school | Confidence | Correction needed |
|---|---|---|---|---|
| Nodes cast 7th-house drishti | Drishti table: "Rahu casts on 7th", "Ketu casts on 1st", "Saturn receives Rahu (7th)" | **3.** BPHS gives graha drishti for the seven grahas. Node aspects are not part of that scheme as far as I know. Later and regional practice variously gives 5/7/9, or 3/11, or none. | High that it is disputed | Under a declared "Parashari only" framework, remove node *cast* aspects and read the nodes through occupation, conjunction, dispositor and nakshatra lord — or state the rule and its school explicitly |
| Nodes as *chhaya grahas* acting through their dispositor | Section 14 classical band | **2.** The chhaya graha terminology and the dispositor mechanism are genuine and standard. | Medium-high | None |

## Functional benefics and malefics

| Claim | Current wording | Source / school | Confidence | Correction needed |
|---|---|---|---|---|
| The seven-row functional table itself | Section 7, "functional verdict" column | **3.** The binary functional benefic/malefic classification by lagna is a 20th-century systematization widespread in English-language Vedic astrology. BPHS gives *component* lordship rules; it does not give this table. | Medium-high | Relabel as a contemporary systematization resting on classical lordship rules. The document currently presents it as classical doctrine. |
| "Jupiter = functional malefic by kendradhipati dosha" | Section 7 table and section 4 callout | **2 overstated.** The classical kendradhipati doctrine concerns a benefic *losing its beneficence* through sole kendra lordship — not becoming malefic. The 7th's maraka function is a **separate** mechanism, and I compressed the two into one verdict. | High that it is overstated | Separate the two mechanisms explicitly: loss of beneficence via kendradhipati, maraka function via the 7th. Do not collapse them into "functional malefic." |
| "Parashari doctrine is explicit that lordship governs function" | Section 7 classical band | **2**, but "explicit" is too strong | Medium | Soften to "standard practice holds" |
| "Saturn mixed, tilting benefic" | Section 7 table | **4.** The components (5th trikona lordship auspicious, 6th dusthana lordship difficult) are classical; "tilting benefic" is my summary verdict. | High | Attribute the summary to me, not to the tradition |
| "Moon merely mixed" as 11th lord | Section 7 table | **3.** The doctrine that the 11th lord tends malefic is school-dependent. | Medium | Label as school-dependent |
| Lagna lord exempt from kendradhipati dosha | Section 7 callout | **2.** Widely held standard practice; I could not cite the verse. | Medium-high | Mark as standard practice rather than cited doctrine |

## Retrograde motion

| Claim | Current wording | Source / school | Confidence | Correction needed |
|---|---|---|---|---|
| Retrogression counted among Venus's weakening factors | Theme II combo line lists "retrograde" among the weakening measures; section 4 lists it likewise | **3, and arguably inverted.** Shadbala assigns retrograde grahas *high cheshta bala*. Treating retrogression as weakness is a modern reading, not the classical strength system. | High | Remove from the weakness stack, or state explicitly that cheshta bala treats it as strength and that a contested modern reading is being used |
| "Retrogression classically turns a graha's work inward or backward: revisiting, reworking" | Section 4, Venus lived-expression band | **4 / Western import.** The word "classically" is unearned. | High | Drop "classically", or drop the sentence |
| Jupiter retrograde listed as a qualification on Hamsa yoga | Section 9 | **3**, same issue | Medium-high | Same treatment |

## Vargottama, avastha, dig bala

| Claim | Current wording | Source / school | Confidence | Correction needed |
|---|---|---|---|---|
| Vargottama treated as strength | "In classical terms this is a real strength" | **1/2.** Well attested; some texts equate it to own-sign strength. Correctly treated as *strength*, not as beneficence. | High | None |
| Baladi avastha given equal billing with dig bala as an "independent measure" | Theme II, "Bala avastha" listed alongside combustion and dig bala | **1 for existence, 4 for the weight.** Avastha schemes are classical; baladi is generally a *minor* modifier, and I gave it the same evidentiary standing as a Shadbala component. | Medium-high | Downgrade to a minor modifier listed for completeness |
| Baladi proportional strength not applied | — | Some treatments assign fractional strength (Bala ¼, Kumara ½, Yuva full, Vriddha ¼, Mrita ~0). I computed the state but not the multiplier. | Medium | Note the omission, or apply it |
| "A graha strong in *sthana* and weak in *dig* is classically read as having capacity without natural placement for exercising it" | Section 10, **classical band** | **4.** This is my inference sitting in the serif register reserved for the tradition's voice. A category error in my own three-register system, not just a wording problem. | High | Move to the explanatory register or attribute to me |
| "Effectiveness in Saturn's domains that exceeds any felt enthusiasm" | Section 10 lived expressions | **4**, correctly placed in the sans register | High | None |

## Direct attributions to named sources

| Claim | Current wording | Source / school | Confidence | Correction needed |
|---|---|---|---|---|
| Unaspected Moon | "**Parashara treats** an unaspected Moon as self-referring" | **4 misattributed.** I have no source for this. | High that it is unsourced | Remove the attribution. The geometry stands; the sentence must not claim Parashara said it. |
| Moon strong Shukla Ashtami → Krishna Ashtami | Section 2 | **2.** Commonly cited, related to paksha bala. | Medium-high | Mark as standard practice |
| Hora doctrine on self-generated vs received wealth | Section 12 | **2/3.** Commonly stated; grounding uncertain. Already flagged in the document as the lightest evidence. | Medium | Adequate as flagged |
| Rashi sandhi weakening Mercury at 0°16′ | Section 4 | **3.** The sandhi concept is real; its weight and the exact degree band vary by authority. | Medium | Label as school-dependent |
| "Yogas deliver in the periods of their participants" | Sections 4, 9, 13 | **2.** That yogas fructify in their participants' dashas is standard and well grounded. | High | None |

## Yoga definitions

| Yoga | Rule as given | Source / school | Confidence | Correction needed |
|---|---|---|---|---|
| Pancha Mahapurusha / Hamsa | own sign or exaltation in a kendra **from the Lagna** | **1/2.** Standard. Variant: some authorities also allow a kendra from Chandra Lagna. | High | Note the variant |
| Gaja Kesari | Jupiter in a kendra from the Moon | **2.** Appears in later classical texts; some versions add conditions. | Medium-high | Note that stricter versions exist |
| Sunapha / Anapha / Durudhara / Kemadruma | grahas in the 2nd/12th from the Moon, **excluding Sun, Rahu, Ketu** | **1 for the yogas; 3 for my exclusion rule.** Excluding the Sun is standard; whether the nodes count for Kemadruma cancellation is disputed. | Medium | State that the node exclusion is a choice among authorities. Note: Saturn cancels Kemadruma here regardless, so nothing turns on it. |
| Dharma-Karmadhipati | 9th lord and 10th lord associated | **1/2 for the concept** (kendra–trikona lord association is core Parashari raja yoga doctrine); **2/3 for the name.** | Medium-high | Attribute the label as common usage |
| Lakshmi | 9th lord own/exalted in kendra or trikona + strong Lagna lord | **3.** Conditions vary materially between sources; I stated one version as *the* rule. | Medium | Label school-dependent and name the version used |
| Budha-Aditya | Sun and Mercury conjunct | **2/3.** Name widespread; degree qualifications later. Already downgraded to "nominal only" in the document on correct grounds. | Medium-high | Adequate |
| Vipareeta Raja | 6/8/12 lord in another of 6/8/12 | **2.** Named subtypes appear in later texts. | Medium-high | None |
| Sakata | Moon in 6/8/12 from Jupiter | **2/3.** Rules vary. | Medium | Label variant-dependent |
| Malavya near-miss | "Had the Lagna been Scorpio or Aquarius, the same Venus would have produced a Mahapurusha yoga" | **Factually incomplete.** Venus in Taurus is in a kendra from Taurus, Leo, Scorpio **and** Aquarius lagnas. I named two of four. | High | Complete the list |

## The two overstatements named in the review

| Claim | Current wording | Problem | Correction |
|---|---|---|---|
| Venus's layers | "Venus is strong in exactly one layer and weak in every other one examined" | **Internally contradicted by my own section 12.** Venus is own sign in the D10 11th and own sign + vargottama in D7. Compounded by the retrograde finding above, which removes a fourth "weakness." | Applied — see below |
| Saturn's strength | "Saturn is the strongest body by every measure except sign" | The document explicitly declines to compute Shadbala, Ishta and Kashta phala. It cannot then claim *every* measure. | Applied — see below |

## Flagged but not applied, pending your decision

| Claim | Current wording | Problem |
|---|---|---|
| Moon psychology | "Emotional processing that happens internally and **arrives already resolved**" | "Arrives already resolved" is not established by an unaspected Moon. "Internally processed", "less directly modified by other grahas", or "more self-referential" is defensible; the resolution claim is not. The later synthesis already handles this better by calling the Moon comparatively self-contained. |

---

## What survives the audit unchanged

Worth stating, because most of the document does survive:

- Every computed value. Nothing in the audit touches the ephemeris output,
  the nakshatra and pada assignments, the vargas, the dig bala arithmetic, the
  Vimshottari derivation, or the yoga *tests*.
- The Jupiter treatment, which refuses to let own-sign placement end the
  conversation, and which stacks retrogression, kendradhipati, the maraka
  connection, both malefic aspects, and D9 loss against it. The mechanism
  labels need separating; the refusal to oversimplify was right.
- The bhava chalit caveat and its prominence.
- The refusal to compute Shadbala rather than approximate it — which is
  precisely what makes the Saturn overstatement indefensible.
- The Venus structure, which was the document's most valuable result and
  becomes *more* interesting once corrected: not weak, but context-dependent.

---

# Addendum: web search performed

The original audit declined to search, on the grounds that online Jyotish
material is mostly unsourced and mutually copied. That was a judgement call,
not a capability limit, and it was overruled. Searched August 2026.

## Source quality tiers used below

| Tier | Meaning |
|---|---|
| **A** | A published translation of the primary text, quoted directly |
| **B** | Named secondary source giving a specific, checkable citation |
| **C** | Practitioner site, unsourced, of the kind that copies from other practitioner sites |
| **D** | SEO content farm. Ignored entirely. |

Most results were tier C or D and are not cited. One tier-A source was
reached: a public translation of *Brihat Parashara Hora Shastra* chapters
34-45 at sanskritdocuments.org. **It is still a translation of uncertain
edition**, and the caution below about editions is not rhetorical.

## Two findings that REVERSE the original audit

### 1. "Jupiter is a functional malefic for Virgo" was correct. My softening was wrong.

**Tier A.** BPHS ch. 34, vv. 31-32, on Kanya (Virgo) lagna:

> "Mangal, Guru, and Chandr are malefics, while Buddh and Shukr are
> auspicious. Shukr's yuti with Buddh will produce Yog. Shukr is a killer as
> well. Surya's role will depend on his association."

Guru is Jupiter, and the text names it a malefic for this lagna directly. The
original audit said "functional malefic" overstated the kendradhipati
doctrine. Both things turn out to be true at once, in the same chapter: the
*general* rule (vv. 2-7) is muting, not reversal —

> "Benefics owning Kendras will not give benefic effects, while malefics
> owning Kendras will not remain inauspicious."

— but the *per-lagna list* applies the malefic label to Jupiter for Virgo
without qualification. The reading's original wording stands; my audit's
correction of it does not.

### 2. The functional benefic/malefic table is not a modern systematization.

The original audit called the per-lagna table "a 20th-century systematization"
that BPHS does not provide. **That is wrong.** BPHS ch. 34 gives per-lagna
benefic and malefic lists explicitly. The table's *form* is classical.

## Three errors in the reading's table, found against the text

**Tier A**, same passage:

| Graha | Reading says | BPHS ch. 34 vv. 31-32 says | Verdict |
|---|---|---|---|
| Jupiter | functional malefic | malefic | correct |
| Mars | functional malefic | malefic | correct |
| Mercury | strongest functional benefic | auspicious | correct |
| Venus | benefic with maraka duty | auspicious, "a killer as well" | correct |
| **Moon** | **"mixed"** | **malefic** | **under-called** |
| **Sun** | **functional malefic** | **"role will depend on his association"** | **over-called** |
| **Saturn** | **"mixed, tilting benefic"** | **not mentioned for this lagna** | **unsupported by this passage** |

## A citation for the chart's central yoga

**Tier A.** The same passage continues: *"Shukr's yuti with Buddh will produce
Yog."* BPHS names the **Venus-Mercury conjunction as yoga-producing for Virgo
lagna specifically** — and that is exactly the configuration in this chart,
Venus and Mercury conjunct in Taurus.

This is better textual grounding than the generic kendra-trikona raja yoga
rule the reading cited for Dharma-Karmadhipati. The reading should cite this
verse instead.

**Translation caveat, which matters here.** A tier-C source quotes the same
passage as "Indeed, Mercury and Venus become Yogakaraka" — a materially
stronger claim than "their yuti will produce Yog." Two translations, two
different strengths of claim, from one verse. This is precisely why the
edition needs to be named before the citation is trusted.

## Node aspects: unsupported, and the 5/7/9 rule traces to an edition dispute

**Tier A.** BPHS ch. 34, vv. 16-17:

> "Rahu and Ketu give predominantly the effects as due to their yuti with a
> bhava lord or as due to the bhava they occupy."

Conjunction and occupation. No drishti. This is exactly the treatment the
original audit recommended, now with a text behind it.

**Tier B.** The 5/7/9 node-aspect doctrine is reported to derive from the
**Khemraj 1932 edition** of BPHS, which differs from the **Santhanam 1984**
edition, and to have been popularised by J.N. Bhasin. Separately, Ketu is
argued to cast no graha drishti at all on doctrinal grounds — being headless,
it cannot glance — and to have rashi drishti only.

**Correction needed:** remove both node rows from the drishti table. The
reading currently gives Rahu and Ketu a 7th aspect each, which no tier-A
source supports and which a doctrinal argument specifically denies for Ketu.

## Retrograde and cheshta bala: the correction was right

**Tier B.** Retrograde grahas receive maximum cheshta bala, 60 shashtiamsas,
placing them in the same bracket as exalted grahas for that component. A
pointer worth checking: **Saravali 5.39**, reported as "a benefic, if
retrograde, is strong and is capable of conferring kingdom."

Not verified against Saravali itself. But it is a named text and verse, which
is a real improvement over the nothing the reading had.

## Nakshatra chains: confirmed as KP, not Parashari

**Tier C**, but consistent across many independent sources, and the
distinction is definitional rather than doctrinal:

In Parashari, sign lordship dominates interpretation and nakshatra is used
mainly for dasha calculation. KP's signature methodological departure is
**inverting that weighting** so the star lord overrides the planet itself.

Section 5 of the reading builds a structural map out of nakshatra-lord chains
and treats it as parallel in authority to the rashi analysis. That is the KP
weighting. The original audit's most serious finding is confirmed.

K.S. Krishnamurti worked in Madras from the early 1950s; the first
*Krishnamurti Paddhati Reader* appeared in 1963. So the technique postdates
the Parashari corpus by a very long way.

## Nakshatra parivartana: still no classical basis found

Searching found parivartana defined consistently as an **exchange of rashis**
between two house lords, attributed to BPHS. Nothing named a nakshatra-level
exchange. Absence of evidence from a search is weak, but it is consistent
with the original finding: the term is my extension.

## What remains unverified

Lakshmi yoga's conditions, the hora doctrine on self-generated versus received
wealth, the baladi avastha multipliers, rashi sandhi weighting, and the claim
about an unaspected Moon. None were reached at tier A or B. The last of these
was an invented attribution and is already withdrawn from the reading.

## Sources

- [Brihat Parashara Hora Shastra, chapters 34-45 (translation)](https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45.html) — tier A
- [Brihat Parashara Hora Shastra (overview)](https://en.wikipedia.org/wiki/Brihat_Parashara_Hora_Shastra) — tier B
- [Aspects of the Nodes, jyotishvidya.com](https://www.jyotishvidya.com/nodes.htm) — tier B, the Khemraj/Santhanam edition claim
- [Cheshta Bala, astrosutras.in](https://astrosutras.in/index.php/2025/03/04/cheshta-bala-motional-strength-detailed-explanation/) — tier B/C, the Saravali 5.39 pointer
- [Shadbala overview, Thoughts on Jyotish](https://medium.com/thoughts-on-jyotish/shadbala-the-6-sources-of-strength-4c5befc0c59a) — tier C
- [KP significator hierarchy, Jagannath Hora](https://jagannathhora.com/kp-significator-hierarchy-4-level-reading/) — tier C
- [KP vs Vedic comparison, Jagannath Hora](https://jagannathhora.com/kp-vs-vedic-astrology-comparison/) — tier C
- [Kendradhipati dosha, jyotishbootcamp](https://jyotishbootcamp.substack.com/p/kendrathipathi-dosha) — tier C
