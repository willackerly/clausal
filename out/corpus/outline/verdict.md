# Outline of the machine-generated Navier–Stokes / Euler proofs from the declaration graph

Corpus: `openai/NavierStokesAndEuler@f9e8bc5b` (52,505 declarations, `out/corpus/ns/decls.jsonl`). Method: dominator tree of the graph "A's statement or proof uses B", from each of the four headline theorems. Script: `bench/outline.py` (no LLM, no source regex). Machine-readable form: `outline.json`; per-declaration dominator data: `dominators_<root>.jsonl`; all numbers: `shape.json`, `relaxations.json`. Revised 2026-11-10 after a second reader's review; the changes are listed at the end of this section.

## Verdict

**The dominator tree gives a real but partial outline, and most of its statements are not ones a mathematician could take on trust by reading them.** As a map of where the proof's bottlenecks are it works; as a readable interface it does not.

- **Shape: one hub, very wide.** In Navier–Stokes a spine of four statements leads from the headline theorem to `selected_candidate_one_with_initial_rest`, which has 8,599 dominator-tree children. In Euler the headline theorem is itself the hub, with 5,846 children. 87% and 83% of those children dominate nothing but themselves.
- **Where the proof mass sits** (a partition; the parts sum to 100%):

  | | Navier–Stokes | Euler |
  |---|---|---|
  | under chapters (a statement that is the only way into 20+ declarations) | 65.0% (61 chapters) | 42.1% (54 chapters) |
  | ... of which under statements dominating 100+ declarations | 51.6% (13 statements) | 25.0% (7 statements) |
  | in small regions of 2 to 19 declarations | 19.6% (1,104 regions) | 32.4% (963 regions) |
  | in declarations that no single statement cuts off (the shared layer) | 15.4% (7,520 declarations, 31.7% of all) | 25.5% (4,829 declarations, 36.8% of all) |
  | the spine's own proofs | 0.01% | 0% |

- **Fraction a reader can skip, and what kind of statement has to be trusted for it.** Trusting the outline's top-level statements skips 56.5% of the Navier–Stokes proof mass (13 statements) and 33.2% of Euler (19 statements). That is a fact about the graph, not a reading contract:

  | level-1 statements, by how they read | Navier–Stokes | Euler |
  |---|---|---|
  | intermediate milestone, readable as printed | 3.7% | 0% |
  | technical waypoint, readable as printed | 6.5% | 0% |
  | waypoint whose content is in a structure defined elsewhere (`x : SomeStructure`) | 42.6% | 11.6% |
  | restatement of the headline theorem | 0% | 3.9% |
  | unreadable or arbitrary | 1.1% | 10.4% |
  | not rated | 2.5% | 7.3% |
  | **total skipped** | **56.5%** | **33.2%** |

  So about 10% of the Navier–Stokes proof, and none of Euler's, sits under a statement that can be read and trusted as printed. Unfolding just the level-1 statements takes 2,880 definitions in Navier–Stokes (43% of all non-theorem declarations below the root) and 2,003 in Euler (47%).
- **More statements do not fix it.** The 40 heaviest dominators give 63% and 40%. Getting to 85% and 75% needs 1,165 and 1,017 statements. What the printed outline leaves uncovered is 13,661 and 9,898 declarations, which is not readable as glue.
- **Readability of the 16 heaviest chapter statements** (first reader, source consulted): **2 intermediate milestones, 1 restatement of the headline theorem, 2 readable waypoints, 7 opaque waypoints, 4 unreadable.** By mass the milestones are small: `no_global_solution_one` 2.7% and `state_runInvariant` 1.0% of Navier–Stokes; Euler has none. The seven opaque waypoints are of the form `x : SomeStructure` or `SomeProp constants`, where the object is `Classical.choice` of an existence theorem; the printed statement carries no content until the structure is unfolded.
- **Second reader.** An independent reviewing agent recomputed the trees with networkx and re-read the source for the 15 statements first rated; its labels matched on all 15. That agreement is weaker than it looks: the reviewer had already seen the tally and the opening words of each rationale, and considered `step` and `selected_witness` borderline. Its two substantive corrections are adopted here: the Euler "milestone" is the headline theorem minus a side condition, and a readable paper-named step had been left out by the chapter definition.
- **Statement length.** 19 of 40 outline statements in Navier–Stokes and 20 of 40 in Euler exceed 1,000 characters (maximum 11,579). Chapter heads are longer than average, not shorter: median 756 characters against 375 for all theorems in Navier–Stokes, 643 against 406 in Euler.
- **Vocabulary.** The 40 Navier–Stokes outline statements mention 369 project declarations directly, and unfolding them fully takes 3,240 definitions (Euler: 250 and 2,126). The definitions, not the lemmas, are the interface a reader cannot skip.

The best part is the top of the Navier–Stokes tree: `theorem_1_1`, `theorem_1_1_with_initial_rest` (a candidate with the stated properties exists, no global finite-energy solution exists for its force, and it vanishes for |t| ≤ 3/8), `selected_candidate_one_with_initial_rest` (the same at viscosity 1) and, beside it, `no_global_solution_one` (any such candidate excludes a global finite-energy solution) are short, recognisable statements that match the paper's last section. Below the hub the quality drops sharply. Euler has no spine at all.

## Against the paper's own outline (Navier–Stokes)

The second reader compared the chapters with Section 3 of the Navier–Stokes paper. The table below is that reading, updated for the corrected chapter definition; the generated table "where the paper's steps sit" further down gives the mass figures. The module-to-step mapping is by filename keyword and is rough. The Euler paper was not compared.

| paper step | in the outline? |
|---|---|
| leading profile (Theorem 4.6, Appendices A to C) | yes, as `profile : ProfileData`, 23% of mass, statement empty until unfolded |
| moment matching (A.1 / B.8) | yes, `exists_normalized_repair`, the one readable lemma |
| coefficient induction (Prop. 5.3) | partly, `hierarchy`; about half of the keyword-matched mass is outside every chapter |
| realised base field (Prop. 5.5) | no single chapter |
| torus charts (Section 6) | no; 68% of that mass is outside every chapter |
| oscillatory realisation of the stress (Prop. 7.5) | partly, hidden inside `choice : Choice B N0` |
| mean corrections (Section 8, 5.7% of mass) | no; 55% outside every chapter |
| correction cycle (Prop. 9.6) | partly, `step` and `state_runInvariant`; 55% outside every chapter |
| sum, localise, extend the force (Props. 9.9, 10.1, Lemma 10.3) | yes, but only as `selected_witness`, a near-restatement of the hub |
| energy and comparison, no global solution (Section 10.3) | yes after the fix: `no_global_solution_one` holds 89% of that mass |
| viscosity rescaling (Section 10.4) | visible only in the spine statement |

In Euler the central constructed object, `EulerPacketInduction.initialDatum`, dominates only itself: the headline theorem uses it together with its property lemmas (`initialDatum_compact`, `initialDatum_divergence`, ...), so the object and its lemmas form a multi-entry interface that a single dominator cannot see.

**Against what a reader already has** (second reader's measurements, made with the first chapter definition):
- **File listing:** the outline adds information. Chapters cut across files: in Navier–Stokes 32% of mass lies in modules that sit 90% or more inside one chapter and 52% in mixed modules.
- **Unfolding the top theorem a few levels:** does not find the chapters; heads sit at shortest-path depth 1 to 18 from the hub.
- **Docstrings:** 4,422 documented declarations below the Navier–Stokes root are too many to serve as a list. Module docstrings exist in 2,595 of 2,655 files.
- **Net:** the paper's Section 3 plus the module docstrings remain a better reading map than the outline. What the outline adds is which declarations are bottlenecks and which files belong beneath them.

## Do the relaxations help?

| relaxation | Navier–Stokes | Euler | helps? |
|---|---|---|---|
| (a) cut out a library layer (declarations with many users) and recompute | chapter mass falls from 65% to about 44% at every threshold from 20 to 200 users, because 3,400+ declarations reached only through the library drop out | 42% → 43% at 20 to 50 users, then falls | **No.** The hub stays thousands wide until the "library" is a third of the corpus |
| (b) pairs and triples of chapter statements as joint cuts | +5.8% of mass from pairs, +3.9% from triples, spread over 149 distinct cuts; best 5 pairs +2.9% | +4.8% and +4.5% over 95 cuts; best 5 pairs +3.3% | **Marginal among chapter heads.** Most mass outside the chapters (21% and 43% of all mass) is reached from the hub without passing any chapter |
| (b') a constructed object plus the up-to-10 statements that mention it, as a joint cut (added after review) | 516 such interfaces cut off something outside the chapters; all together 6.3% of mass; the best 5 add 1.6% (42 statements to trust), the best 20 add 3.4% (167 statements) | 556 interfaces; all together 14.7%; the best 5 add 5.0% (42 statements), the best 20 add 9.1% (156 statements) | **A little in Euler, not in Navier–Stokes, and at about 8 statements per interface.** Objects mentioned by more than 10 statements were not tested |
| (c) definitions as dominators | 11 definitions cover 39.5% of mass; the largest chapter (`profile`) and the largest section (`estimates`, under `selected_witness`) are definitions | 25 definitions cover 11% | **Informative for Navier–Stokes**: the chapter boundaries are chosen objects (`Classical.choice` of a bundled existence result) |
| (c) module quotient graph | 362 children of the hub module, 337 trivial, holding 73% of mass | 1,153 children, 938 trivial, 61% of mass | **No.** Flatter than the declaration graph |
| (d) Louvain clustering (a different method) | about 30 communities, modularity 0.83; median about 120 to 190 entry points | about 30 communities, modularity 0.81; median about 85 to 110 entry points | **Finds topics, not interfaces.** Clusters are real but each is entered through a hundred or so declarations |

## Reading of the result

- The dominator tree recovers the places where the machine proof wrapped a construction into one named object or one existence statement. Those are genuine chapter boundaries, and in Navier–Stokes they carry over half the proof.
- It does not recover a hierarchy for the rest. The shared layer is mostly small definitions and one-off lemmas with a median of 5 to 7 users below the root (9 in 10 have under 50), so it is not a library that can be factored out by a user-count threshold either.
- A dominator's statement is the right thing to trust only when its content is in the statement. Here the content is typically in a structure type defined elsewhere, so an outline has to present the structure's fields (or the paper's prose for them), not the Lean signature. The proof-mass-per-statement-length idea would rank `profile : ProfileData` (100 characters, 23% of the proof) as the best chapter in the corpus; that is true as a boundary and useless as a statement.
- Ratings are by one reader on 16 statements, with a non-blind second reading, and should be treated as indicative.

## What changed after the review

- **Chapter definition.** A chapter was a child of the hub only. It is now a child of the hub or a side branch of any spine node. This adds `no_global_solution_one` (656 declarations, 2.7% of Navier–Stokes mass, the paper's Section 10.3 step) and one smaller chapter; Navier–Stokes goes from 59 chapters and 62.2% to 61 and 65.0%, and the level-1 skip from 54.2% to 56.5%. Euler is unchanged (its root is the hub).
- **Ratings.** The Euler lemma `initialDatum_no_global_solution` is now counted as a restatement of the headline theorem, not a milestone. Ratings are also reported by mass.
- **Skip fraction.** Reported split by how the trusted statements read, with the number of definitions needed to unfold them, instead of as one number.
- **Mass accounting.** The earlier figures (62.2 + 19.5 + 21.0) double-counted; the partition above replaces them.
- **Relaxation (b).** Reworded, and the object-plus-statements variant (b') was run.
- **Paper comparison and trivial baselines** added from the second reader's report.

## Checks

- `python3 bench/outline.py --test`: the dominator algorithm (Cooper–Harvey–Kennedy) on two hand-made graphs and 300 random DAGs, compared with the definition by node deletion and with `networkx.immediate_dominators`.
- Every top-level outline entry was re-checked on the real graph by deleting it and recounting what the root still reaches: 66 checked across the four roots, no mismatch.
- The second reader recomputed the trees for the two primary roots with networkx; every headline figure of the first version reproduced.

## Limitations

- Proof mass counts distinct subterms of elaborated terms; a few very large proofs can dominate a chapter (`exists_normalized_repair` is 5% of the mass and hides 21 declarations).
- "Skippable" counts proof mass only. It ignores that definitions inside a skipped region may be needed to read later statements (343 such definitions in Navier–Stokes, 128 in Euler).
- Statements are `ppSignature` output cut at 2,000 characters in the export and trimmed further here; nothing was re-printed relative to a parent context.
- When a chapter head sits on a chain of single-child dominators (`profile` → `actualProfile` → `profileData_nonempty` → `exists_nominal_cone`), the outline prints the top one and lists the rest as "passes through"; a lower link may have the more informative statement.
- The pair/triple table uses a sufficient cut, not always a minimal one, so it slightly understates what small cuts achieve. The object-plus-statements test is limited to objects mentioned in at most 10 statements, and "mentioned in the statement" includes uses that are not properties of the object.
- The four roots give two essentially distinct graphs; the periodic and compact-support variants differ from their siblings by about 100 declarations.
- In the export, 103 structures carry value-side edges that appear neither in the structure's type nor in its constructor (reviewer's finding, cause not identified). Dropping them changes no immediate dominator below the Navier–Stokes root and 5 below the Euler root, so they were left in.
- The numbers in this hand-written section were copied from `shape.json` and `relaxations.json` after the final run; the generated tables below are authoritative if the two ever disagree.
