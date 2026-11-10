# Prior art check: restructuring machine-generated Lean 4 proofs into reusable lemma libraries

Checked 2026-11-09 by web search and direct page fetches. Every claim below carries the URL it came from. Where I only saw an abstract page or a secondary source, I say so. Statistics on the OpenAI repository are my own measurement from a shallow clone (regex-based, so approximate).

## Bottom line

- None of the five table entries is fabricated. All five exist at the cited arXiv IDs or GitHub path. One description is inaccurate in a way that matters (Lean Refactor), and two are slightly off in title or date.
- The earlier table missed the closest prior work: **Proof-Refactor** (arXiv:2606.03743), which is an agentic pipeline that extracts tactic blocks from generated Lean proofs into helper lemmas and scores signature quality and readability. Its pipeline is nearly the one AGENTS.md describes.
- The motivating premise needs correcting. The OpenAI Navier-Stokes Lean repository is **not** a set of monolithic proofs. It is about 644K lines in 2,659 files with roughly 38,500 theorems whose median length is about 10 lines. The comprehension problem there is a flat sea of small lemmas with no hierarchy, not proofs that need chunking.
- What remains open is narrower than the original idea: repository-scale, cross-proof restructuring driven by a deterministic term-level metric, and selecting or building a small readable interface over tens of thousands of existing lemmas.

## 1. Verdicts on the earlier table

| # | Entry as given | Verdict | What it actually is |
|---|---|---|---|
| 1 | "Lean Refactor", Aug 2026, arXiv:2605.20244, agentic refactorer trained on 200K long-short proof pairs | **exists-but-misdescribed** | Real: "Lean Refactor: Multi-Objective Controllable Proof Optimization via Agentic Strategy Search" (Lu, Kong, Stehling, Yang, Wang, Sun, Chen). v1 is 18 May 2026; Aug 2026 is the v2 revision. The refactoring LLM is **frozen**, not trained. The ~200K long-short pairs are distilled into a bank of 9,237 strategies, and only a retrieval embedder is fine-tuned. It shortens proofs in place (token length, compile time, cross-version compatibility). It does not extract reusable lemmas and has no readability metric. https://arxiv.org/abs/2605.20244 , https://arxiv.org/html/2605.20244 |
| 2 | "DreamProver", Apr 2026, arXiv:2604.26311, wake-sleep lemma library learning | **verified** | "DreamProver: Evolving Transferable Lemma Libraries via a Wake-Sleep Theorem-Proving Agent" (Zhang et al., 29 Apr 2026). Wake: prove training theorems, emit `sorry` subgoals. Sleep: cluster by embedding, LLM proposes lemmas, filter by tree similarity, dedupe by tree edit distance, LRU forgetting, library capped under 100 lemmas. Reports ~58% of library lemmas reused on test sets. The library comes from proving attempts, not from refactoring existing long proofs. No anti-unification. https://arxiv.org/abs/2604.26311 , https://arxiv.org/html/2604.26311 |
| 3 | "ProofEvolve", Aug 2026, arXiv:2608.26334 | **verified** (exists; no description was given to check) | "ProofEvolve: Neuro-Symbolic Evolution for Formal Automated Theorem Proving" (Ye et al., 26 Aug 2026). A prover, not a refactorer: evolves partial proof graphs per problem and stores verified sub-proofs in a persistent "schema library" reused on later problems. Evaluated on competition benchmarks. Abstract only. https://arxiv.org/abs/2608.26334 |
| 4 | "LeanArchitect" (hanwenzhu/LeanArchitect), `@[blueprint]` attribute | **verified** | Real repo and paper. `@[blueprint]` tags declarations, infers dependencies from used constants, exports LaTeX blueprint nodes; options include `statement`, `proof`, `uses`, `proofUses`, `notReady`, `latexEnv`. Paper: arXiv:2601.22554 (Zhu, Monticone, Avigad, Welleck), ITP 2026. It documents existing structure; it does not create structure. https://github.com/hanwenzhu/LeanArchitect , https://arxiv.org/abs/2601.22554 , https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2026.25 |
| 5 | "Explorable Theorems", arXiv:2604.02598 | **verified** (title slightly off) | Actual title: "Explorable Proofs: Making Written Proofs Explorable by Grounding Them in Formal Representations" (Kambhamettu, Crichton, Welleck, Goldstein, Head, 3 Apr 2026). The system is called "explorable theorems". HCI work: LLM translates a written proof to Lean and links the two so readers can step through, test examples, and trace dependencies; 16-person study. It goes informal-to-formal for reading, not formal-to-readable-library. https://arxiv.org/abs/2604.02598 |

### Tools named in the table

| Tool | Verdict | Notes |
|---|---|---|
| Kimina Lean Server | **verified** | FastAPI wrapper over a pool of Lean REPLs, default port 8000, `infotree_type` request field. Tech report arXiv:2504.21230. https://github.com/project-numina/kimina-lean-server |
| PyPantograph and `Goal.sibling_dep` | **verified** | The field exists in `pantograph/expr.py`: `sibling_dep: Optional[set[int]] = field(default_factory=lambda: None)`. It has no docstring. Note the default is `None`, so the `len == 0` gate in AGENTS.md section 2 would raise on a goal where it is unset. https://github.com/lenianiva/PyPantograph , https://raw.githubusercontent.com/lenianiva/PyPantograph/main/pantograph/expr.py |
| Mathlib `extract_goal` | **verified, but weaker than AGENTS.md assumes** | It prunes unneeded hypotheses and supports `extract_goal *`, named variables, and `using name`. Its own docs say the output comes from delaboration, may not be equivalent to the original goal, and may fail to type-check (stuck typeclass instances, `sorryAx`). It does not "emit an exact standalone signature" reliably. Proof-Refactor wrote its own `extract` tactic for this reason. https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/ExtractGoal.html |
| LeanDojo-v2 | **verified** | End-to-end training/eval framework extending LeanDojo with LeanAgent; provers run on Pantograph. https://github.com/lean-dojo/LeanDojo-v2 |

## 2. The real closest work

### 2a. Direct overlap: refactoring generated Lean proofs

- **Proof-Refactor: Refactoring Generated Formal Proofs into Modular Artifacts** (Fu, Liu, Wang, Yuan, 2 Jun 2026). Four Claude Code phases: extract tactic blocks into top-level "scaffold" theorems with a custom `lean_extract` tool, design helper declarations (grouping similar scaffolds, with Gemini as external adviser), prove them, repair the owner proof to call the helpers. Scored by an LLM-judge rubric over structure, signature quality, tactic quality, reuse, and human readability (75% agreement with humans on 28 samples). Evaluated on 96 PutnamBench and 12 Putnam2025 generated proofs, median ~160 lines. Stated limits: single self-contained file only, no cross-proof reuse, LLM judge, Putnam-style proofs only. Code: https://github.com/pelicanhere/proof-refactor . https://arxiv.org/abs/2606.03743 , https://arxiv.org/html/2606.03743
- **ImProver** (Ahuja, Avigad, Tetali, Welleck, Oct 2024). LLM agent rewriting Lean proofs for a user-chosen metric: length (tactic count) or readability (declarative style). https://arxiv.org/abs/2410.04753
- **ImProver 2** (Ahuja, Rowney, Avigad, Welleck, 21 May 2026). Defines structural metrics: length, dependencies, and modularity `mu_mod` (count of effective `have`/`calc`-style spawned goals). Restructures inside one proof; no top-level lemma extraction, no cross-proof reuse. https://arxiv.org/abs/2605.22885 , https://arxiv.org/html/2605.22885
- **ProofOptimizer** (Gu, Piotrowski et al., Meta FAIR, Oct 2025; NeurIPS 2025 / ICLR 2026). Model trained by expert iteration to shorten Lean proofs; reported 87% reduction on miniF2F, 57% on PutnamBench, ~50% on Seed-Prover IMO 2025 proofs. Length only. https://arxiv.org/abs/2510.15700
- **AXLE** (Axiom Math, 24 Jun 2026). Cloud service with 14 Lean metaprogramming tools; the abstract lists lemma extraction, declaration metadata extraction, and deterministic proof repair and simplification among the categories. I did not open the tool list. https://arxiv.org/abs/2606.26442
- **LeanLean: Benchmarking Repository-Scale Lean Proof Compression** (Rögnvaldsson, Mündler-Sasahara, Dekoninck, Vechev, ETH; dated 4 Oct 2026). 64 real repositories up to 174K lines; agents get 12 hours to shrink token count while Comparator keeps protected theorems valid. Metric is tokens only, explicitly not readability. **Could not verify on arXiv**: I only saw an alphaXiv listing with a non-standard ID. https://www.alphaxiv.org/abs/2611.leanlean
- **Lean Pool** (Ilin, 21 Sep 2026). Archive of formalization projects "grown, maintained and optimized by AI agents". A secondary summary says accepted changes include library-wide proof shortening; the repository README says the projects are mostly independent of each other. https://arxiv.org/abs/2609.25199 , https://reservoir.lean-lang.org/@Vilin97/lean-pool
- **Sorries Are Not the Hard Part** (Ilin, Nugent, 11 Jun 2026). Expert review of a semi-autonomous formalization of Grothendieck vanishing: sorry-free, yet experts found serious problems in definitions, generality, file organization, and API. Agents fixed local feedback well and were weak at definitions and API design. This is the best evidence for the problem, and a warning that the hard part is design, not slicing. https://arxiv.org/abs/2606.13925

### 2b. Library learning and lemma discovery

- **REFACTOR** (Zhou, Wu, Li, Grosse, ICLR 2024). GNN trained to extract reusable theorems from Metamath proofs; 16 new theorems used 733.5 times on average, library shrank by ~400K nodes. The closest precedent for "extract theorems from existing proofs and measure reuse and compression", but in Metamath. https://arxiv.org/abs/2402.17032
- **TacMiner** (Xin, Xin, Poesia, Goodman, Chen, Dillig, Mar 2025). Tactic Dependence Graphs to mine reusable tactics across Rocq proofs; 26% proof size reduction; beats an anti-unification baseline (Peano) 3x. Tactics, not lemmas; Rocq, not Lean. https://arxiv.org/abs/2503.24036
- **Automatically Generalizing Proofs and Statements** (Gandhi, Tadipatri, Gowers, ITP 2025). Lean algorithm generalizing a proof by abstracting repeated and related constants. One proof at a time. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2025.12
- **DreamCoder** https://arxiv.org/abs/2006.08381 , **Stitch** https://arxiv.org/abs/2211.16605 , **babble** (e-graph anti-unification) https://arxiv.org/abs/2212.04596 . Compression-driven library learning over program corpora. I found no application of Stitch or babble to Lean proof terms.
- **LEGO-Prover** (Wang et al.) https://arxiv.org/abs/2310.00656 , and the negative results: **Library Learning Doesn't** https://arxiv.org/abs/2410.20274 and **LLM Library Learning Fails: A LEGO-Prover Case Study** https://arxiv.org/abs/2504.03048 . In LEGO-Prover's logs, one lemma was reused, once. Any reuse claim must be measured, not assumed.
- **Lemmanaid** (Alhessi et al., Apr 2025). Neuro-symbolic lemma conjecturing for Isabelle; recovers 29-39.5% of human lemmas. Conjecturing, not refactoring. https://arxiv.org/abs/2504.04942
- **Older proof refactoring**: Levity (relocates lemmas in Isabelle/HOL), Tactician (HOL Light), POLAR, CoqPIE, as surveyed in "QED at Large". I read these only through the search summary of the survey. https://arxiv.org/abs/2003.06458
- **Coq lemma extraction at failure points** (Prasad, ICLR 2025 workshop). Proof-search aid, not refactoring. https://github.com/mtarunpr/coq-prover

### 2c. Metrics close to the proposed information-hiding score

- **Compression is all you need: Modeling Mathematics** (Aksenov, Bodnia, Freedman, Mulligan, Mar 2026). Measures Mathlib by wrapped versus unwrapped length, and defines "deductive compression" as the ratio of proof length to statement length. That is essentially the proposed score. They use it descriptively and as a search heuristic, not to drive refactoring. I read a secondary overview, not the paper body. https://arxiv.org/abs/2603.20396 , https://www.alphaxiv.org/overview/2603.20396
- Stitch and babble optimize corpus compression including the cost of the abstraction itself, which is the same MDL idea. ImProver 2's `mu_mod` and REFACTOR's node savings are the nearest proof-specific metrics.
- **The Network Structure of Mathlib** (graph modularity of the dependency network). Surfaced in search only; not opened. https://arxiv.org/abs/2604.24797

### 2d. Blueprint tooling

- leanblueprint (Massot): plasTeX plugin, human-written dependency graph. https://github.com/PatrickMassot/leanblueprint
- LeanArchitect: blueprint generated from `@[blueprint]` attributes (above).
- **LeanMarathon** (Zhang et al., 3 Jun 2026): multi-agent autoformalization organized around an evolving Lean blueprint file; 258 lemmas across four Erdős problems. Structure is imposed during generation. https://arxiv.org/abs/2606.05400
- Anthropic's FLT effort coordinated agents on a DAG of theorem statements with statements and proofs in separate files (below).

## 3. The large AI-generated formalizations, and how they are actually structured

- **OpenAI, Navier-Stokes and Euler blow-up** (announced 8 Sep 2026). Repo: https://github.com/openai/NavierStokesAndEuler . Lean 4.34.0-rc2 plus Mathlib, checked with Comparator against DeepMind's formal-conjectures statements. My measurement at commit f9e8bc5 (the same commit the audit cites): 2,659 `.lean` files, 643,991 lines, 33.7 MB; about 38,500 `theorem`/`lemma` declarations and 12,400 definitions; only about 485 theorems marked `private`; about 12,700 docstrings. Theorem length including statement: median 10 lines, 90th percentile 27, 99th percentile 61, maximum 205. The `NavierStokes/` directory is flat: 708 entries. The largest file, `Euler/EulerProof.lean`, is 20,756 lines holding 983 theorems.
  - So the proofs are already small. What is missing is hierarchy, visibility control, and a small named interface.
- **The audit**: Bastounis, Circelli, Hansen, "Navier-Stokes lost in translation" (6 Oct 2026). Finds Lean statements that differ from the manuscript, for example `norm_derivativeWord_inverse_le` uses m+5 derivatives where the paper's (8.19) uses m+4, and a pressure-flux bound with an extra dependence. Says mathematicians are unlikely to read millions of lines of Lean and that a correct but incomprehensible Lean proof has less value. Offers no technique for comprehensibility. https://arxiv.org/abs/2610.08144 , https://arxiv.org/html/2610.08144v1
- Press: research groups are using LLMs over the Lean code and paper to get a bird's-eye view. https://www.scientificamerican.com/article/openais-blockbuster-navier-stokes-proof-isnt-what-we-thought-it-was/ . King's College summary: https://www.kcl.ac.uk/news/openais-navier-stokes-proof-called-into-question
- **Anthropic, Fermat's Last Theorem** (4 Sep 2026). About 13 million lines, 30,300 intermediate theorems proved and 29,500 used, over 5x Mathlib; the post says it is "likely much longer than it needs to be" and about 7% of non-boilerplate lines come from failed early attempts. https://www.anthropic.com/research/formalizing-fermats-last-theorem , repo https://github.com/anthropics/fermats-last-theorem
- **Atlas / AutoformBot** (Meta, 28 May 2026): 26 textbooks, over 45,000 declarations, about 500K lines. https://arxiv.org/abs/2605.29955
- **2D Navier-Stokes Galerkin construction in Lean** (Wang, 27 Sep 2026): Leray-Hopf weak solutions on bounded domains. The abstract does not say how it was produced. https://arxiv.org/abs/2609.33033

## 4. What is actually new here, if anything

Not new:
- Slicing a sub-proof out with `extract_goal` or a custom tactic into a helper lemma, then repairing the parent. Proof-Refactor does exactly this, with a better extraction tactic, and AXLE ships lemma extraction as a service.
- Shortening or golfing generated proofs. ProofOptimizer, Lean Refactor, ImProver 1 and 2, and LeanLean cover it.
- Growing a lemma library during proving. LEGO-Prover, DreamProver, ProofEvolve.
- "Proof size per unit of statement size" as a quantity. Freedman et al. define it; Stitch and babble optimize the general form.

Plausibly new, in decreasing order of confidence:
1. **Repository-scale, cross-proof restructuring.** Proof-Refactor is limited to one self-contained file and lists that as a limitation. LeanLean works at repository scale but rewards token deletion only. Nobody I found detects near-duplicate lemmas across a 38K-lemma corpus and merges them into parameterized ones.
2. **A deterministic, kernel-level objective in place of an LLM-judge rubric.** Using elaborated term size hidden behind a statement, summed over call sites, as the thing to optimize is the Stitch/babble utility transplanted to Lean `Expr`. I found no one doing symbolic anti-unification over Lean proof terms for lemma discovery; REFACTOR did the learned version on Metamath and TacMiner the tactic version on Rocq.
3. **Interface selection instead of chunking.** Given that the big artifacts are already tens of thousands of 10-line lemmas, the useful output is the small set of statements a mathematician must read, with everything else demoted to private. Ranking existing declarations by hidden proof mass per statement token, and reporting how many statements cover what fraction of the proof, appears undone. It needs no proof rewriting, so it is cheap and cannot break the build.
4. **Readability evidence from mathematicians.** Proof-Refactor's human check is 28 samples; nobody has run a comprehension study on restructured research-scale Lean.

Risks to state plainly:
- Reuse may be rare. The LEGO-Prover post-mortems found almost none on competition problems. A single large PDE development is a more favourable setting, but that is a hypothesis to measure first.
- The audit's complaint is statement fidelity to the paper, which restructuring does not address.
- Expert review found the hard failures are definitions and API design, which a compression score does not see.
- Term-level size is distorted by automation: one `simp` call can elaborate to a huge term, so the score needs a defined normalization.

## 5. Who we would be duplicating

- **Proof-Refactor** if we build an extract, design, prove, repair pipeline over single proofs. This is the plan in AGENTS.md sections 2 and 3.
- **Lean Refactor, ProofOptimizer, ImProver 2** if the measured outcome is shorter proofs or faster compilation.
- **LeanLean** if we build a benchmark of repository compression.
- **DreamProver, LEGO-Prover, ProofEvolve** if the library is learned while proving new theorems.
- **LeanArchitect, leanblueprint, LeanMarathon** if the output is a dependency graph or blueprint of existing declarations.
- **AXLE, Kimina, PyPantograph** for infrastructure; these should be used, not rebuilt.
- **Freedman et al.** if the contribution is only the ratio metric as a descriptive statistic.

The defensible gap is items 1 to 3 in section 4 applied to the public OpenAI and Anthropic repositories, starting with the measurement in item 3.
