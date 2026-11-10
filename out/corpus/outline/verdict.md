# Outline of the machine-generated Navier–Stokes / Euler proofs from the declaration graph

Corpus: `openai/NavierStokesAndEuler@f9e8bc5b` (52,505 declarations, `out/corpus/ns/decls.jsonl`). Method: dominator tree of the graph "A's statement or proof uses B", from each of the four headline theorems. Script: `bench/outline.py` (no LLM, no source regex). Machine-readable form: `outline.json`; per-declaration dominator data: `dominators_<root>.jsonl`; all numbers: `shape.json`, `relaxations.json`.

## Verdict

**The dominator tree gives a real but partial outline, and most of its statements are not ones a mathematician could take on trust by reading them.** As a map of where the proof's bottlenecks are it works; as a readable interface it does not.

- **Shape: one hub, very wide.** In Navier–Stokes a spine of four statements leads from the headline theorem to `selected_candidate_one_with_initial_rest`, which has 8,599 dominator-tree children. In Euler the headline theorem is itself the hub, with 5,846 children. 87% and 83% of those children dominate nothing but themselves.
- **What sits under non-trivial dominators.** Navier–Stokes: 12 statements each dominating 100+ declarations hold 49% of the proof mass; 59 chapters (20+ declarations) hold 62%. Euler: 7 statements hold 25%; 54 chapters hold 42%.
- **What does not.** 36% of declarations (21% of mass) in Navier–Stokes and 45% (35% of mass) in Euler hang directly off the hub: a shared layer that no single statement cuts off. A further 19% (Navier–Stokes) and 32% (Euler) of mass sits in about 1,000 tiny regions of 2 to 19 declarations.
- **Fraction a reader can skip.** Trusting the outline's top-level statements skips **54%** of the Navier–Stokes proof mass (13 statements) and **33%** of Euler (19 statements). The 40 heaviest dominators would give 61% and 40%. Getting to 82% and 75% needs over 1,000 statements. The remainder is not readable as glue: it is 14,000 and 9,900 declarations.
- **Readability of the 15 heaviest chapter statements** (one reader, source consulted): **2 milestones, 9 technical waypoints, 4 unreadable.** Five of the nine waypoints are of the form `x : SomeStructure` or `SomeProp constants`, where the object is `Classical.choice` of an existence theorem; the printed statement carries no content until the structure is unfolded.
- **Statement length.** 18 of 40 outline statements in Navier–Stokes and 20 of 40 in Euler exceed 1,000 characters (maximum 11,579). Chapter heads are longer than average, not shorter: median 811 characters against 375 for all theorems.
- **Vocabulary.** The 40 Navier–Stokes outline statements mention 390 project declarations directly, and unfolding them fully takes 3,230 definitions (Euler: 250 and 2,126). The definitions, not the lemmas, are the interface a reader cannot skip.

The best part is the Navier–Stokes spine: `theorem_1_1`, `theorem_1_1_with_initial_rest` (a candidate with the stated properties exists, no global finite-energy solution exists for its force, and it vanishes for |t| ≤ 3/8) and `selected_candidate_one_with_initial_rest` (the same at viscosity 1) are short, recognisable statements. Below the hub the quality drops sharply. Euler has no spine at all.

## Do the relaxations help?

| relaxation | Navier–Stokes | Euler | helps? |
|---|---|---|---|
| (a) cut out a library layer (declarations with many users) and recompute | chapter mass falls from 62% to about 41% at every threshold from 20 to 200 users, because 3,400+ declarations reached only through the library drop out | 42% → 43% at 20 to 50 users, then falls | **No.** The hub stays thousands wide until the "library" is a third of the corpus |
| (b) pairs and triples of chapter statements as joint cuts | +5.7% of mass from pairs, +3.9% from triples, spread over 145 distinct cuts; best 5 pairs +2.9% | +4.8% and +4.5% over 95 cuts; best 5 pairs +3.3% | **Marginally.** Most mass outside the chapters (21% and 43% of all mass) is reached from the hub without passing any chapter |
| (c) definitions as dominators | 11 definitions cover 39.5% of mass; the two largest chapters are definitions | 25 definitions cover 11% | **Informative for Navier–Stokes**: the chapter boundaries are chosen objects (`Classical.choice` of a bundled existence result) |
| (c) module quotient graph | 362 children of the hub module, 337 trivial, holding 73% of mass | 1,153 children, 938 trivial, 61% of mass | **No.** Flatter than the declaration graph |
| (d) Louvain clustering (a different method) | about 30 communities, modularity 0.83; median about 120 to 190 entry points | about 28 communities, modularity 0.81; median about 90 to 110 entry points | **Finds topics, not interfaces.** Clusters are real but each is entered through a hundred or more declarations |

## Reading of the result

- The dominator tree recovers the places where the machine proof wrapped a construction into one named object or one existence statement. Those are genuine chapter boundaries, and in Navier–Stokes they carry over half the proof.
- It does not recover a hierarchy for the rest. The shared layer is mostly small definitions and one-off lemmas with a median of 5 to 7 users below the root (9 in 10 have under 50), so it is not a library that can be factored out by a user-count threshold either.
- A dominator's statement is the right thing to trust only when its content is in the statement. Here the content is typically in a structure type defined elsewhere, so an outline has to present the structure's fields (or the paper's prose for them), not the Lean signature. The proof-mass-per-statement-length idea would rank `profile : ProfileData` (100 characters, 23% of the proof) as the best chapter in the corpus; that is true as a boundary and useless as a statement.
- Ratings are by one reader on 15 statements and should be treated as indicative.

## Checks

- `python3 bench/outline.py --test`: the dominator algorithm (Cooper–Harvey–Kennedy) on two hand-made graphs and 300 random DAGs, compared with the definition by node deletion and with `networkx.immediate_dominators`.
- Every top-level outline entry was re-checked on the real graph by deleting it and recounting what the root still reaches: 66 checked across the four roots, no mismatch.

## Limitations

- Proof mass counts distinct subterms of elaborated terms; a few very large proofs can dominate a chapter (`exists_normalized_repair` is 5% of the mass and hides 21 declarations).
- "Skippable" counts proof mass only. It ignores that definitions inside a skipped region may be needed to read later statements (321 such definitions in Navier–Stokes, 128 in Euler).
- Statements are `ppSignature` output cut at 2,000 characters in the export and trimmed further here; nothing was re-printed relative to a parent context.
- The pair/triple table uses a sufficient cut, not always a minimal one, so it slightly understates what small cuts achieve.
- The four roots give two essentially distinct graphs; the periodic and compact-support variants differ from their siblings by about 100 declarations.
