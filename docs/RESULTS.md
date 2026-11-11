# Results so far

One row per question tested. Detail for each is in `docs/EXPERIMENTS.md`; the plan they belong to is `docs/PLAN.md`.

| Question | Answer | Status | Detail |
|---|---|---|---|
| Does "proof hidden per unit of statement" find the lemma boundaries humans choose inside a proof? | No. First pick 7.7%; at chance for small helpers; worse than random at choosing where to stop | Final, reviewed | `out/FINDINGS.md` |
| Does the original "small goal state" idea find them? | No. Worse than random | Final, reviewed | `out/FINDINGS.md` |
| Do statements recur across proofs in human-written Mathlib? | Not usefully: 0.2% of proof size after removing trivia | Final, reviewed | `out/reuse/REUSE.md` |
| Can pieces of a proof be lifted into real lemmas soundly? | Yes. Kernel-checked, no failures on 1,274 theorems | Final, reviewed | `Rosette/Lift.lean` |
| Are the lifted statements readable? | Sometimes: good for Pell and Erdős–Ginzburg–Ziv, poor for a Sobolev inequality | One rater, three theorems | `out/demo/README.md` |
| Was the idea new? | Partly not. Single-proof extraction is published (Proof-Refactor); the ratio is published as a descriptive measure | Checked by web search | `out/prior_art.md` |
| Can English scenarios be bound to proofs about real Rust? | Yes on a 45-line wallet: 7 proved for all inputs, a false claim refuted with a counterexample | Final, reviewed | `slice/FINDINGS.md` |
| Does that survive loops and collections? | Yes, at a price: about 6 lines of hand-written Lean per line of Rust (1.6 for straight-line code); nothing about a loop is automatic. Viable with an agent writing proofs, not push-button | Final, reviewed; two loops only | `slice/FINDINGS.md` |
| Does the chain find real problems on a real target? | On TDFLite's decision code: a Lean model matching the Go on 400k cases; all six known edge cases surfaced (the search was guided) and 15 further behaviours reproduced on the real code | Final; details private | `docs/EXPERIMENTS.md` (18) |
| What does each kind of evidence catch? | On the fixtures, edge-weighted property tests and bounded model checking catch nearly all injected bugs; proofs add the guarantee for all inputs and sizes | Final, reviewed; two toy crates | `slice/compare/TRADES.md` |
| How much real Rust translates to Lean today? | 1% of functions in ten real crates as shipped; 35% with five small patches to the translator (two of them do the measured work) (82% excluding one crate blocked earlier in the toolchain) | Final | `census/CENSUS.md`, `census/fork/FORK.md` |
| Can an agent write loop proofs unaided? | On a new crate with rules by a separate author, two models each proved all 7 loop functions in under 15 minutes; cost stays near 6 Lean lines per Rust line | Final, independently scored; textbook loops | `p2/RESULTS.md` |
| Does a composable vocabulary work? | Built: 23 frames, every old statement proved equivalent, rule lines compile and are echoed in English. New sentences cannot yet run on compiled Rust | Review in progress | `docs/EXPERIMENTS.md` (24) |
| Do readers catch a wrong reading when it is echoed back? | Model readers caught 93%; the trial is ready for people | Proxy only | `trials/meaning/REPORT.md` |
| Do dominators in the lemma graph predict what humans put in a blueprint? | No. Dominator features add +0.001 to a graph model; the signal is mostly proof size. Plain reachability recovers 87–94% of the human dependency edges | Final, reviewed | `out/corpus/FINDINGS.md` |
| Does the machine-generated Navier–Stokes proof have a recoverable outline? | Partly: 13 statements guard 56% of the proof, but only about 10% sits behind a statement readable as printed; the content is in definitions | Final, reviewed; one reader | `out/corpus/FINDINGS.md` |
| Is there more redundancy in machine proofs than in Mathlib? | No (0.15% vs 0.20% of proof size). What stands out is dead code: 32% of theorems are used by no headline result | Final, reviewed | `out/corpus/FINDINGS.md` |
| Where do analysis proofs spend their bulk? Do "packets" help? | Mostly on proving equations (54%). Constant threading is real (about 9% of machine proof mass); the cast tax is not present in the machine corpus. Packets: marginal on a mechanical port | Final, reviewed; one machine and one comparable human corpus | `out/corpus/FINDINGS.md` |
| How much of a machine-generated corpus can a reader ignore? | About a quarter: 24.7% of source lines deleted in a copy and the headline theorems still check | Final, reviewed | `out/corpus/FINDINGS.md` |
| Does an outline built around definitions read better? | More followable, not more meaningful: no more milestones, and model readers split | Proxy readers only | `out/corpus/FINDINGS.md` |
| Does a better abstraction compress hand-threaded constants? | Barely: proofs shrink 2–4% on the best-case family and the library costs more than it saves | Final, reviewed; one family | `out/corpus/FINDINGS.md` |

The recurring lesson: sizes and graph positions are measurable but do not by themselves identify what a mathematician finds meaningful. In the machine corpus the content sits in definitions, so an outline has to present those, not lemma signatures.
| Can "what a reader need not read" be a tool for any Lean project? | Yes: run on three projects, roots still build with the same axioms. The share unneeded depends on the choice of roots, so it does not compare machine with human | Final, reviewed | `out/deadcode/M8.md` |
| Can re-invented library notions be found automatically? | Partly: the known case is found unaided, but most matches are trivial and one large case was missed | Exploratory | `out/reinvent/REPORT.md` |
