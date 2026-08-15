# Working standards for this repo

This project is astrological analysis held to research standards. The subject
matter is not falsifiable in the way science is; the *method* still can be.
Everything below was learned by getting it wrong first. Follow it by default,
without being asked.

## Declare the framework before using it

State the system, the era and the school before any interpretation. Then stay
inside it. If a technique comes from a different tradition than the one
declared, label it inline — do not let it pass because it is adjacent.

Real failures this prevents: medieval material (almuten, Lilly moiety orbs,
semi-sextiles) presented as Hellenistic; a KP-style nakshatra-chain analysis
presented as Parashari. Both looked native to the framework. Neither was.

## Provenance of inputs, not just outputs

Be able to say where every input came from. A candidate list, a city set, a
set of events — if any of it entered during an earlier analysis that already
had conclusions, it is contaminated and must be rebuilt from a stated
criterion.

The single highest-yield question anyone has asked in this repo was "where did
these cities come from." The answer was that 60% arrived during analyses that
already knew what they wanted to find.

## No scores, no counting, no composites

Never produce a ranking, a score out of ten, a weighted index, or a count of
positives unless explicitly asked. This includes scores hiding inside prose:
"six gains and three losses" is a score. "Most indicators agree" is a count.

Report factors as facts and let them stay uncommensurable when they are.

## Three registers, kept apart

1. **Technical fact** — computed, checkable against an ephemeris
2. **Traditional delineation** — what the sources hold, in their voice
3. **Possible lived expressions** — plural, probabilistic, and mine

Never put an inference in the tradition's register. Writing "classically read
as..." over your own synthesis is the specific failure to watch for.

Never write "you always", "this means your X is bad", or a single deterministic
personality sentence. If a claim needs timing to be true, say that it does.

## Say what was not computed

If a measure has competing formulations and no way to choose, do not produce a
number. Say it was not computed and why. Then do not later claim strength "by
every measure" — the omission is binding on the conclusion.

## Never cite what cannot be verified

If the primary source is not available in the environment, supply no citation
at all. An invented chapter and verse is worse than an admitted gap, because a
reader cannot tell it from a real one. Say plainly that the claim is
unsourced and mark whether it is standard practice, school-dependent, or your
own synthesis.

## Sensitivity-test every conclusion

Identify which convention each headline claim depends on, then test it against
the alternatives. Label results as **invariant**, **framework-dependent**, or
**interpretive**.

Conventions that turned out to be load-bearing here: whole sign vs quadrant
houses, tropical vs sidereal, mean vs true node, flat vs moiety orbs, sign-based
vs degree-based aspects, and the year-length used for period arithmetic.

## Verify a correction before claiming it

When fixing an error, find *every* instance and check each one. Twice in this
repo a fix was applied in two places out of four, reported as done, and left
the document contradicting itself. Grep for the stale claim afterwards and show
the result.

## Stop before the verdict

Most errors here were introduced at the moment of reaching a conclusion, not
while gathering evidence. When asked to stop at a stage, stop there. When not
asked, still separate the evidence from the verdict so the verdict can be
rejected without discarding the work.

## Pre-register anything predictive

Fix the scoring rule, the exclusions, and the known confounds in a committed
file *before* seeing the data. Then do not revise them. If a rule turns out to
have a hole, say so and report the original result alongside any repair.

## Reproducibility is part of the deliverable

Any document making numeric claims carries an appendix with: library and
version, calculation flags, coordinates, time-zone conversion, and every
formula and convention that was a choice rather than a fact.

## Environment

- Swiss Ephemeris data lives at `/usr/share/swisseph`
- Chromium for PDF rendering: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`
- `natal.py` is the single source of truth for the tropical chart; `jyotish.py`
  computes the Parashari chart independently and shares nothing with it, by design
