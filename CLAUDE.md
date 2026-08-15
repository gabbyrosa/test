# Working standards for this repo

Astrological analysis held to research standards. The subject matter is not
falsifiable the way science is; the *method* still can be. Every rule below was
learned by getting it wrong first. Follow them by default, without being asked.

The first two are at the top because they caused the most damage.

---

## 1. A caveat stays attached to the claim, permanently

The failure is not stating a limitation. It is stating it once and then
letting it fall away from the summary where the claim actually gets used.
**A limitation does not expire because the result became interesting.**

Real instances in this repo, all the same shape:

- Venus was combust and lowest in dig bala, stated in the technical section,
  gone by the time "Venus is the chart's strength" reached the synthesis
- Jupiter's kendradhipati dosha was noted, then "amazing Jupiter, amazing home"
  survived into the conclusions anyway
- The Lot of Spirit boundary moved 217 miles across a ±8 minute birth-time
  window; the Spirit argument kept being used at full strength
- The city list's contamination was found, acknowledged, and the same cities
  kept reappearing in later passes

Operationally: if a claim carries a caveat anywhere, the caveat travels with it
into every restatement, including the one-line summary and the headline. If it
will not fit, the claim is too strong for that length and gets cut instead.

## 2. Agreement between non-independent methods is not evidence

Two methods describing the same geometry in different vocabularies have not
confirmed each other. They have agreed with themselves twice.

Before treating convergence as support, show that the underlying quantities are
actually independent. Four astrological systems all reading the same
planetary positions are not four witnesses.

Corollaries that came from the same mistake:

- **Same locus, two descriptions, one fact.** A "Venus line" and a "Venus-ruled
  regime" at the same longitude are one finding.
- **Distance from a boundary is stability, not quality.** Being far from a
  regime edge means the reading is robust to small input changes. It says
  nothing about whether the reading is good.

---

## 3. Declare the framework before interpreting

State the system, era and school before any interpretation, then stay inside
it. Anything from another tradition gets labelled inline, even when it is
adjacent and looks native.

Caught here: medieval material (almuten, Lilly moiety orbs, semi-sextiles)
presented as Hellenistic; a KP-weighted nakshatra-chain analysis presented as
Parashari. Both looked native. Neither was.

## 4. Four registers, never merged

1. **Calculation** — computed, checkable against an ephemeris
2. **Sourced doctrine** — what a named text says, with the text named
3. **Inference** — my reasoning from 1 and 2, in my voice
4. **Possible lived expression** — plural, probabilistic, conditional

Three registers is not enough. The specific failure was writing my own
synthesis inside the tradition's voice: "classically read as..." over an
inference. Registers 2 and 3 must stay apart or that failure recurs.

Never write "you always", "this means your X is bad", or one deterministic
personality sentence. If a claim needs timing to be true, say so.

## 5. No scores, rankings, averages or composites

Not unless the aggregation rule and the independence of its inputs were
established in advance. This includes scores hidden in prose: "six gains and
three losses" is a score. "Most indicators agree" is a count.

Report factors as facts and let them stay uncommensurable when they are.

## 6. Nothing is inherited into a fresh analysis

Candidate lists, city sets, event sets, rankings, conclusions. If any of it
entered during an earlier analysis that already had conclusions, it is
contaminated and gets rebuilt from a stated criterion.

The highest-yield question anyone has asked in this repo was "where did these
cities come from." The answer was that 60% arrived during analyses that already
knew what they wanted to find.

## 7. Pre-register selection and scoring rules

Fix the inclusion rule, the scoring rule, the exclusions and the known
confounds in a committed file *before* seeing results. Then do not revise them.
If a rule turns out to have a hole, report the original result alongside any
repair rather than replacing it.

## 8. Provenance labels, applied honestly

Every doctrinal claim carries one of:

| Label | Meaning |
|---|---|
| **verified primary** | text and edition named, quoted |
| **secondary** | a named source citing the primary; the primary unchecked |
| **standard practice** | widely held, grounding unverified |
| **school-dependent** | authorities materially disagree |
| **contemporary** | postdates the declared framework |
| **inferred** | mine |
| **unknown** | I do not know where this comes from |

### The shape of a usable citation

Naming the source is not enough. A citation carries four fields:

**text + edition or translator + passage + confidence about textual stability**

The fourth is a separate axis from the label above, and collapsing the two was
a mistake. A claim can be *verified primary* and still textually unstable.

Worked example from this repo. BPHS ch. 34 vv. 31-32 on Kanya lagna reads, in
the sanskritdocuments translation, "Shukr's yuti with Buddh will produce Yog."
A second translation of the same verse renders it "Mercury and Venus become
Yogakaraka" — a materially stronger claim from one passage. So:

> *Brihat Parashara Hora Shastra*, sanskritdocuments English translation
> (edition unidentified), ch. 34 vv. 31-32. **Textual stability: low** —
> a second translation strengthens the claim from "their conjunction produces
> yoga" to "both become yogakaraka."

Same fact for the node-aspect doctrine, which differs between the Khemraj 1932
and Santhanam 1984 editions. "BPHS says" is too coarse to be a citation when
editions move the doctrine.

## 9. Never invent a citation

If the primary source is not in the environment, supply no citation at all. An
invented chapter and verse is worse than an admitted gap, because a reader
cannot tell it from a real one. Web search is permitted and its results are
tiered by source quality, but a practitioner blog is not a text.

## 10. State what was not computed

If a measure has competing formulations and no way to choose, produce no
number. Say it was not computed and why. Then do not later claim strength "by
every measure" — the omission binds the conclusion.

## 11. Sensitivity-test anything convention-dependent

Identify which convention each headline claim rests on and test the
alternatives. Label results **invariant**, **framework-dependent** or
**interpretive**.

Load-bearing conventions found here: whole sign vs quadrant houses, tropical vs
sidereal, mean vs true node, flat vs moiety orbs, sign-based vs degree-based
aspects, the year length in period arithmetic, and — a bug, not a convention —
whether a house cusp is a boundary or a midpoint.

## 12. Verify every downstream occurrence before calling a fix done

Find *every* instance and check each one. Grep for the stale claim afterwards
and show the result. Three times in this repo a fix was applied to some
instances, reported as complete, and left the document contradicting itself.

## 13. Stop at the requested stage

Most errors here were introduced at the moment of reaching a conclusion, not
while gathering evidence. When asked to stop at a stage, stop. When not asked,
still separate evidence from verdict so the verdict can be rejected without
discarding the work.

## 14. Reproducibility is part of the deliverable

Any document making numeric claims carries an appendix: library and version,
calculation flags, coordinates, time-zone conversion, and every formula and
convention that was a choice rather than a fact.

---

## Holding the line

These apply even when a request pushes against them. Being asked for a score is
not authorisation to produce one; explicit acknowledgement of the rule is.

But refusing is not the behaviour either. The required form names the rule and
then offers two routes, so the work survives the last step instead of being
undone by it:

> A single ranking would require aggregation the protocol currently forbids. I
> can give you the strongest framework-specific result, or we can explicitly
> adopt a scoring rule first and then rank against it.

Either route is legitimate. What is not legitimate is producing the ranking
silently, or stopping at "I can't do that."

## Parked work

Substantive corrections that are known and deliberately not actioned belong in
a named list, not scattered through prose. See the top of `provenance_audit.md`.
They get handled as a discrete audit, not folded casually into an unrelated
pass, because a correction merged into other work is the one that never gets
verified downstream.

## Environment

- Swiss Ephemeris data at `/usr/share/swisseph`
- Chromium for PDF rendering: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`
- `natal.py` is the single source of truth for the tropical chart; `jyotish.py`
  computes the Parashari chart independently and shares nothing with it, by design
- `protocol.md` is the portable, project-agnostic version of the above
