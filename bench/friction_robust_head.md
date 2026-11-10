# Friction census: robustness checks after the adversarial review

Source of this section: `bench/friction_robust_head.md`, hand-written; numbers in braces are filled from `robust.json` by `bench/friction_robust.py report`. Data: three reruns of the Expr-level exporter `corpora/friction/Friction.lean` under variant rules (`corpora/friction/robust_run.sh`), plus the existing `Census.lean` export for the matched stratum. Nothing here parses source or pretty-printed text.

## What changed, finding by finding

| review finding | reproduced? | outcome |
|---|---|---|
| 1. Regularity headline depends on counting derivative-value facts (`HasDerivAt` …) as side conditions | yes: {{r:rows/o.dv/ns}}% of ns proof mass, {{r:rows/root.dv/ns}}% in stand-alone lemmas | regularity reported with and without; excess over Carleson is {{r:rows/o.reg_all/ns-carleson @ d}} with, {{r:rows/o.reg/ns-carleson @ d}} without |
| 2. Headline uses the `outer` label; `inner` roughly halves it | yes: D is {{r:rows/o.D_all/ns @ p}}% outer, {{r:rows/i.D_all/ns @ p}}% inner in ns; {{r:rows/o.D_all/carleson @ p}}% and {{r:rows/i.D_all/carleson @ p}}% in Carleson | both labels in the verdict; D stated as a range |
| 3. "Regularity excess survives the subject controls" and "packet addresses at most 2.2%" fail under a matched stratum | yes: regularity {{r:matched/matched/reg_all/ns @ p}}% against {{r:matched/matched/reg_all/carleson @ p}}%; measurability + integrability {{r:matched/matched/mi/ns @ p}}% against {{r:matched/matched/mi/carleson @ p}}% | both sentences withdrawn; B and the instance excess survive the matched stratum |
| 4. Project predicates are opaque `other`; ns has its own smoothness-plus-constant predicates | yes, and larger than the review's lower bounds: {{r:preds/ns/hyp_pct/reg}}% of ns hypotheses are a predicate containing a smoothness fact, {{r:preds/ns/hyp_pct/exC2}}% one hiding an `∃ C`; {{r:preds/ns/exC_producers_hidden_shallow}} hidden `∃ C` producers | every project predicate opened at Expr level; claim A strengthened; "packets are rare in ns" withdrawn; D given an upper bound of {{r:preds/ns/D_upper_bound}}% |
| 5. Non-theorem declarations hold 18.5% of ns proof content, likely side-condition-heavy | partly: {{r:aux/ns/aux_share_of_all_proof_nodes}}% on the census's node measure once data terms and compiler-generated lemmas are left out; not more side-condition-heavy (D {{r:aux/ns/D_all_aux}}% against {{r:aux/ns/D_all_theorems}}%) | exported and reported; no verdict changes; they are {{r:aux/ns/kind_inst}}% instance arguments |
| 6. Unfolding verdict should be "cannot tell" | yes: the source-level tactic counts reproduce | verdict changed |
| 7. Instance excess is partly proof size and overlaps regularity | yes: {{r:inst_size/excess_raw @ d}} raw, {{r:inst_size/excess_std @ d}} to {{r:inst_size/excess_std_rev @ d}} size-standardised; overlap {{r:inst_size/overlap_inst_in_standalone_regularity @ p}} points | both figures reported; excess is {{r:matched/matched/inst/ns-carleson @ d}} in the matched stratum |
| 8 (minor). Side classes contaminated by instance synthesis and certificates | yes for instances: ns measurability {{r:inst/measurability/ns/with @ p}}% → {{r:inst/measurability/ns/without @ p}}%, PFR finiteness {{r:inst/finiteness/pfr/with @ p}}% → {{r:inst/finiteness/pfr/without @ p}}% | variant export reported; the positivity row is no longer used as evidence on claim A. Certificate output inside positivity was not separated |
| 9–11. Bundles: one lemma family in the top 10; ceiling and "proofs do not shrink" overstated; savings gross of glue | yes | `BUNDLES.md` reworded, net figures added |

## What did not change

- Claim B (casts, finiteness) is absent from the machine corpus under every cut, including the matched stratum and with instance synthesis removed.
- Claim C (domain surgery) is small on every direct measure; no new analysis was needed.
- Proving equations is the largest absolute share of proof mass in all three corpora.
- No difference is attributed to machine authorship.

## What these checks do not cover

- Certificate output (`norm_num`, `linarith`) inside the positivity class, and inequalities written as `0 ≤ b - a`, were not separated; the review's sample put them at 17% and 21% of inline ns positivity.
- "Contains a smoothness fact" for a project predicate is syntactic and unweighted: a predicate with one `ContDiff` field and twenty bounds counts the same as one that is only smoothness. The D upper bound charges whole theorems and is deliberately generous.
- The predicate scan was checked by hand against the source of five predicates (`MemClass`, `MeanClass`, `UniformClass`, `JetRate`, `Certificate`), all correct; it was not sampled further.
- The matched stratum is defined by statement vocabulary. It controls for "is about integrals", not for difficulty or style.
- The proof-size standardisation uses six bins; Lean 4.34 against 4.36 and the Mathlib versions are not controlled.
- The variant exports inherit the limits of the first export: the mass partition on large proofs is checked only through its invariants.
