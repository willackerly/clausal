# The refinement graph (schema v2)

One data format for two things this project produces:

- **Software side** (`clausal/`): an English scenario, the Lean statement generated from it, the proof of that
  statement, the Lean model of the Rust code the statement is about, and the Rust code itself.
- **Maths side** (repo root): a theorem, the lemmas lifted out of its proof, and the smaller proof that calls them.

Both are graphs of *things someone relies on* connected by *claims about how they relate*, and both need the same
question answered for every claim: what is the evidence, and of what kind?

| What | Where |
|---|---|
| JSON Schema (Draft 2020-12, no unknown fields allowed) | `clausal/schema/refinement-graph.v2.schema.json` |
| Checks the schema cannot express, and staleness | `clausal/clausal/graphlint.py` (`python3 -m clausal.graphlint <graph.json>`, from `clausal/`) |
| Software graph, regenerated on every run | `clausal/out/graph.json` (109 nodes, 275 edges, 15 verdicts) |
| Maths example, built from the root project's real exports | `clausal/schema/maths-example.graph.json`, made by `clausal/schema/maths_fit.py` (11 nodes, 15 edges) |
| Test that invalid graphs are refused | `clausal/schema/selftest.py` (10 of 10 refused) |

Status: the software side emits this format and validates it on every run. The maths side does not emit it; the
maths example was assembled by a script from that side's existing exports. Version 1 of the schema (one
implementation per node, stored `stale` flags) is retired; section 7 lists what changed and why.

## 1. The model in five sentences

1. A **node** is an *interface*: the thing other nodes rely on (a statement, a definition, a function signature,
   an English phrase). It is identified by a digest of its content, not by its name or location.
2. A node has zero or more **implementations**: what makes the interface true or gives it a body (a proof, a
   function body). A theorem with two proofs is one node with two implementations.
3. An **edge** is a claim relating two nodes ("this statement formalises that scenario", "this Lean function
   translates that Rust function"). An edge with an empty evidence list is a claim nobody has supported yet.
4. Each piece of **evidence** has one of four kinds, says who or what produced it, and records the digests of the
   node ends it was computed from. Evidence is **stale** when one of those digests no longer matches; this is
   computed, never stored.
5. A **verdict** summarises one node: an outcome, the chain of edges it rests on, the evidence kinds on that
   chain, and which links on it nobody has reviewed.

## 2. The four evidence kinds

There is deliberately no ordering among them. "Tested on 216 inputs" and "translated by a tool we trust" are
different kinds of support, not weaker and stronger versions of one thing, so a verdict lists every kind it rests
on rather than a single "weakest link".

| Kind | What it guarantees | What it does not |
|---|---|---|
| **kernel-checked** | Lean's kernel accepted a proof term for exactly the named theorem, using only the listed axioms. True for every value the theorem quantifies over. The entry must name the theorem (`artifact`) and list its `axioms`; the schema rejects it otherwise. | Nothing about whether the theorem says what anyone meant. Nothing about anything outside Lean: Rust code, English text. It also relies on the code that reported "this theorem exists with this type and these axioms" (here `lean/Bdd/Audit.lean`, about 120 lines). `method` says whether the proof was compiled into a library module or checked inside a one-off script session. |
| **tested** | The claim held on the specific inputs that were run. `scope` records how many and how they were chosen (`examples`, `boundary-grid`, `argument-grid`, `replay`). | Anything about inputs that were not run. A passing test of a false universal claim is the normal case, not an exception: the slice's deliberately false scenario passes both of its example rows. |
| **tool-trusted** | A named program produced or reported this, and its output was not independently proved. Examples: Charon + Aeneas translating Rust to Lean; the generator turning a scenario into a statement; the audit reading which constants a statement mentions; Mathlib's compiled `.olean` files being taken as given. | That the tool is right. The entry names the tool and version (through its `run`) so that a bug in it can be traced to everything that depends on it. |
| **human-asserted** | A named person looked at exactly this content (the digests are recorded) and said it is right. The `by` field must start with `human:`; the schema rejects a tool or model as author. | That the person was right, or that the content is still what they looked at (staleness answers the second). In the slice today **no entry of this kind exists**, because nobody has signed anything. |

Two rules are built into the schema because they are the point of the exercise:

- Edges of relation `binds`, `formalises`, `translates` and `models` can **never** carry kernel-checked evidence.
  These are the links from English to Lean and from Rust to Lean; no proof assistant can check them.
- `binds` (an English phrase means this definition) can carry **only** human-asserted evidence. Until a person
  signs, its evidence list is empty. Version 1 recorded "human-asserted by UNREVIEWED" here, which made every
  verdict claim human support it did not have.

A fifth state is as important as the four kinds: **no evidence**. `clausal/out/graph.json` has 25 such edges (the
14 glossary bindings to Lean and the 11 to the Rust predicates), and the maths example has one (two lemmas that
print identically and may or may not be the same statement).

## 3. The schema

Condensed. The JSON Schema file is the authority; field names here are exact.

```
graph    = { schema: "rosette.refinement-graph/2", generated_at, runs: [run], nodes: [node], edges: [edge], verdicts: [verdict] }

run      = { id, tool, version?, toolchain?: {name: version}, config?, at?, complete?: bool, note? }
           one tool invocation; evidence and node origins point at a run, so a graph can span two toolchains

digest   = { alg, value }
           alg: sha256-text   (sha256 of whitespace-normalised text: Gherkin, English, Rust, printed Lean)
                sha256-file   (raw bytes)
                lean-struct64 (Rosette.statementHash of an elaborated Lean statement), -L1, -L2 (its generalisations)
                lean-proof64  (hash of a proof term)

agent    = "human:<who>" | "tool:<what>" | "model:<which>"         the prefix is mandatory

source   = { file?, line_start?, line_end?, decl?, term_path? }     at least file or decl

node     = { id,
             kind:   group | claim | phrase | definition | statement | function | example,
             status: candidate | proposed | accepted | rejected | retired,     accepted needs an approving review
             origin: { by: agent, run?, at? },
             reviews?: [ { by: agent, decision: approved|rejected, digest, at?, note? } ],
             interface: { language: gherkin|english|latex|lean|rust, text, text_complete?,
                          identity: digest, digests?: [digest], source?, metrics?, budgets? },
             implementations: [ { id, language: lean-proof|lean-term|lean-def|rust, ref?, source?, digest?,
                                  complete: bool, hidden?: bool, metrics?, realises: [evidence] } ],
             labels?: [ { kind: name|explanation|rating|note, text, language?, by: agent, run?, about: digest, reviews? } ],
             attrs? }

metrics  = { size_dag?, size_tree?, size_lines?, num_args?, num_hyp_args?, num_free_vars?, ast_depth?,
             num_external_lemmas?, x_<anything>? }
budget   = { measure, params?, value, max, within: bool, relative_to?: node id }

edge     = { id, from, to, relation, from_end?: interface|implementation, from_implementation?,
             to_end?: interface|implementation, occurrences?: [ { at?: source, role?, implementation?, attrs? } ],
             evidence: [evidence], attrs? }

evidence = { kind: kernel-checked | tested | tool-trusted | human-asserted,
             by: agent, run?, artifact?, axioms?, method?,
             scope?: { quantifier: all | instances | n/a, n?, method? },
             inputs?: [ { node, end?: interface|implementation, implementation?, digest } ],
             witness?, detail? }

verdict  = { node, outcome: pass | fail | open | review | notApplicable, code, expected?, as_expected?,
             flags: [string], chain: [edge id], rests_on: [evidence kind],
             unreviewed?: [node or edge id], stale?: [edge id], counterexample?, detail? }
```

### Node kinds

| Kind | Software side | Maths side |
|---|---|---|
| `group` | a feature file | a module, a blueprint chapter (not used in the example) |
| `claim` | a Gherkin scenario | an English or LaTeX statement that came *before* the Lean (none exists yet) |
| `phrase` | one glossary entry: a step phrase and its argument order | not used |
| `definition` | a glossary definition in Lean; its second reading as a Rust predicate | a definition a statement depends on |
| `statement` | the generated Lean statement of a scenario; derived statements (Givens satisfiable, negation, input coverage) | a theorem; a lifted lemma; a candidate lemma |
| `function` | a Rust function; its Aeneas-generated Lean model; an Aeneas library model of a std operation | not used |
| `example` | one Examples row; a counterexample | not used |

For a `function` the interface is the signature and the body is an implementation. For a `definition` the whole
definition is the interface, because anything that mentions it depends on its body.

### Relations

`graphlint.py` enforces which kinds each relation may connect.

| Relation | From, to | Meaning | Evidence it can carry |
|---|---|---|---|
| `contains` | group to claim | file contains scenario | tool-trusted (parser) |
| `composed_of` | claim to phrase | the scenario uses this phrase; `occurrences` lists each step line | tool-trusted (matcher) |
| `binds` | phrase to definition or function | the phrase means this | **human-asserted only**, or none |
| `formalises` | statement to claim | the Lean statement says what the claim says | tool-trusted, tested, human-asserted; never kernel-checked |
| `uses` | statement, definition or function to another | mentions it. `from_end` is required: `interface` (the statement mentions X) or `implementation` (this proof calls X). `to_end: implementation` when what is relied on is a body | tool-trusted (read from the Lean environment) |
| `requires` | statement to statement | a side condition of a verdict, such as "the Givens are satisfiable" | tool-trusted |
| `translates` | function to function | the Lean model's body is a translation of the Rust body | tool-trusted, tested; never kernel-checked |
| `models` | function to function | a hand-written Lean model stands in for a std operation | tool-trusted; never kernel-checked |
| `instance_of` | example to statement | the row is an instance of the statement | tested |
| `exercises` | example to function | the row was run on this function | tested |
| `refutes` | statement or example to statement | shows the target false, or (`attrs.how: vacuity`) true of nothing | tool-trusted, tested |
| `covers` | statement to function | the statement says no input of the function falls outside a set of scenarios | tool-trusted |
| `lifted_from` | statement to statement | the lemma was cut out of the target's proof; `occurrences` lists where | tool-trusted |
| `generalises` | statement to statement | reserved; no data yet | |
| `equivalent` | definition to definition, statement to statement | the two say the same thing | tested, kernel-checked, or none |

That a statement is *true* is not an edge. It is the `realises` evidence on one of the statement's
implementations: the kernel checked that this proof proves this statement.

### Staleness

Every evidence entry lists the node ends it was computed from, each with its digest at that time. `graphlint.py`
computes, from the graph alone:

- an end is **changed** if some evidence records a digest for it that differs from its current one;
- a node is **suspect** if its interface changed, or if its interface `uses` something changed or suspect (its
  text is the same but it no longer means the same);
- evidence is stale if an input is a changed end or a suspect node. On the purely structural relations
  (`uses`, `composed_of`, `contains`) only a changed end counts;
- an implementation is stale if its `realises` evidence is, or if it `uses` a suspect node (the proof calls a
  lemma whose statement changed);
- a verdict is stale if its node is suspect, an edge on its chain is stale, or an implementation of its node is.

A review or a label carries the digest of the interface it was written about and is void when that differs.

`python3 -m clausal.graphlint out/graph.json --what-if def:Vocab.covers` reports what would go stale if that
definition were edited: 5 statements that use it become suspect, 31 edges and 7 verdicts go stale. The same
question about the body of the Lean model of `withdraw` gives 3 suspect statements and 4 stale verdicts.
Because `run.sh` regenerates everything each time, nothing is ever stale in `out/graph.json` itself; staleness
matters once graphs are kept and updated incrementally, which the maths side will need.

### Verdicts

`outcome` uses SARIF's `result.kind` vocabulary so verdicts can be exported to CI tooling. `code` is an open,
domain-specific rule name.

| Code | Outcome | Meaning |
|---|---|---|
| PROVED-FOR-ALL, PROVED-INSTANCE | `pass`, or `review` if any glossary binding on the chain has no valid sign-off | kernel-checked proof of the generated statement, Givens shown satisfiable |
| REFUTED | `fail` | kernel-checked proof of the negation, with the input |
| COUNTEREXAMPLE | `fail` | failing input found on the model; the kernel confirmation did not go through |
| VACUOUS | `fail` | kernel-checked: no input satisfies the Givens |
| TESTED-ONLY | `open` | examples pass, no proof |
| UNBOUND, AMBIGUOUS, UNSUPPORTED | `notApplicable` | no statement could be generated |
| INPUTS-COVERED, INPUTS-NOT-COVERED | `pass` / `review`, `open` | on a function node: whether every input falls under a proved scenario |
| LIFT-KERNEL-CHECKED | `review` | maths side: a lifted lemma that is kernel-checked and awaits a person's decision |
| CANDIDATE-ONLY | `open` | maths side: enumerated, nothing created or checked |

In the slice today all nine proved scenarios have outcome `review`, not `pass`: the proofs are sound, and nobody
has signed the glossary.

## 4. Worked example: software

From `clausal/out/graph.json`, the scenario "A covered withdrawal succeeds and takes exactly the amount". Hashes are
shortened; `inputs` are shown once and then elided.

The glossary entry, its Lean definition, and the binding between them, which nobody has signed:

```json
{"id": "phrase:T-dec", "kind": "phrase", "status": "proposed", "origin": {"by": "model:slice-build-agent"},
 "interface": {"language": "english",
   "text": "Then {wallet:w}'s balance is decreased by {amount:n}    [applies to: pre(w), post(w), n]",
   "identity": {"alg": "sha256-text", "value": "06fbea13…"}, "source": {"file": "glossary.yaml", "line_start": 116, "line_end": 116}},
 "implementations": []}

{"id": "def:Vocab.decreasedBy", "kind": "definition", "status": "proposed", "origin": {"by": "model:slice-build-agent"},
 "interface": {"language": "lean",
   "text": "Vocab.decreasedBy (pre post : Wallet) (n : U64) : Prop := post.balance.val + n.val = pre.balance.val",
   "identity": {"alg": "sha256-text", "value": "ff7f8d2e…"},
   "metrics": {"size_tree": 45},
   "budgets": [{"measure": "expression nodes of a glossary definition (warning threshold, DESIGN.md 4.1)",
                "value": 45, "max": 40, "within": false}]},
 "implementations": []}

{"id": "binds:phrase:T-dec->def:Vocab.decreasedBy", "relation": "binds", "from": "phrase:T-dec", "to": "def:Vocab.decreasedBy",
 "evidence": [],
 "attrs": {"args": ["pre(w)", "post(w)", "n"], "reading": "Lean (the one statements are generated from)", "signoff": "none"}}
```

(The budget entry is real: this definition is 45 expression nodes against a warning threshold of 40.)

The second reading of the same phrase, a Rust predicate, and the tested claim that the two readings agree:

```json
{"id": "equivalent:def:Vocab.decreasedBy->def:rust:wallet_bdd::decreased_by", "relation": "equivalent",
 "evidence": [{"kind": "tested", "by": "tool:lean-eval+rust-eval", "run": "run:cucumber",
   "scope": {"quantifier": "instances", "n": 216, "method": "argument-grid"},
   "detail": "216 of 216 grid points give the same truth value",
   "inputs": [{"node": "def:Vocab.decreasedBy", "end": "interface", "digest": {"alg": "sha256-text", "value": "ff7f8d2e…"}},
              {"node": "def:rust:wallet_bdd::decreased_by", "end": "interface", "digest": {"alg": "sha256-text", "value": "2e20020a…"}}]}]}
```

The generated statement and its proof. The proof is an implementation; "the kernel accepted it" is its `realises`:

```json
{"id": "stmt:Spec.wallet.withdraw_covered.stmt", "kind": "statement", "status": "proposed",
 "origin": {"by": "tool:clausal", "run": "run:clausal"},
 "interface": {"language": "lean",
   "text": "def Spec.wallet.withdraw_covered.stmt : Prop :=\n  ∀ (a amount : U64) (alice : wallet.Wallet),\n    Vocab.hasBalance alice a →\n    Vocab.covers alice amount →\n    ∃ (outcome : Vocab.Outcome) (alice' : wallet.Wallet),\n      wallet.Wallet.withdraw alice amount = ok (outcome, alice') ∧\n      Vocab.succeeds outcome ∧\n      Vocab.decreasedBy alice alice' amount",
   "identity": {"alg": "sha256-text", "value": "ca7ca750…"},
   "source": {"file": "lean/Wallet/Statements.lean", "line_start": 90, "line_end": 97}},
 "implementations": [{"id": "p1", "language": "lean-proof", "ref": "Spec.wallet.withdraw_covered",
   "source": {"file": "lean/Wallet/Proofs/wallet/withdraw_covered.lean", "line_start": 16, "line_end": 20},
   "digest": {"alg": "sha256-text", "value": "2e371f7f…"}, "complete": true, "hidden": true, "metrics": {"size_lines": 4},
   "realises": [{"kind": "kernel-checked", "by": "tool:lean-kernel", "run": "run:lean",
     "artifact": "Spec.wallet.withdraw_covered", "axioms": ["propext", "Classical.choice", "Quot.sound"],
     "scope": {"quantifier": "all"}, "method": "library-module",
     "detail": "module Wallet.Proofs.wallet.withdraw_covered; the audit checked that the theorem's type is exactly Spec.wallet.withdraw_covered.stmt",
     "inputs": [ "…the statement's interface digest and the proof's digest…" ]}]}]}
```

The statement relies on the *body* of the Lean model, and that body is claimed to translate the Rust body:

```json
{"id": "uses:stmt:Spec.wallet.withdraw_covered.stmt->fn:lean:wallet.Wallet.withdraw", "relation": "uses",
 "from_end": "interface", "to_end": "implementation",
 "evidence": [{"kind": "tool-trusted", "by": "tool:lean-audit", "run": "run:lean",
   "detail": "the When: the constant occurs in the elaborated statement (read from the environment by Bdd.Audit)", "inputs": ["…"]}]}

{"id": "translates:fn:lean:wallet.Wallet.withdraw[body]->fn:rust:wallet::{wallet::Wallet}::withdraw", "relation": "translates",
 "from_end": "implementation", "from_implementation": "body", "to_end": "implementation",
 "evidence": [
   {"kind": "tool-trusted", "by": "tool:charon+aeneas", "run": "run:translate", "artifact": "lean/provenance.json",
    "scope": {"quantifier": "all"}, "detail": "rustc 1.100.0-nightly …; charon 0.1.315 …; aeneas nightly-2026.11.09-5a392f4; the translation is not proved correct"},
   {"kind": "tested", "by": "tool:cucumber-rs+lean-eval", "run": "run:cucumber",
    "scope": {"quantifier": "instances", "n": 6, "method": "examples"},
    "detail": "6 of 6 example rows give the same result on compiled Rust and on the Lean model"}]}
```

The verdict. Proved, and waiting for a person:

```json
{"node": "scenario:Spec.wallet.withdraw_covered", "outcome": "review", "code": "PROVED-FOR-ALL",
 "expected": "PROVED-FOR-ALL", "as_expected": true, "flags": [],
 "chain": ["formalises:stmt:…withdraw_covered.stmt->scenario:…withdraw_covered",
           "binds:phrase:G-balance->def:Vocab.hasBalance", "binds:phrase:G-covers->def:Vocab.covers",
           "binds:phrase:W-withdraw->fn:lean:wallet.Wallet.withdraw", "binds:phrase:T-ok->def:Vocab.succeeds",
           "binds:phrase:T-dec->def:Vocab.decreasedBy",
           "uses:stmt:…withdraw_covered.stmt->fn:lean:wallet.Wallet.withdraw",
           "translates:fn:lean:wallet.Wallet.withdraw[body]->fn:rust:wallet::{wallet::Wallet}::withdraw"],
 "rests_on": ["kernel-checked", "tool-trusted", "tested"],
 "unreviewed": ["binds:phrase:G-balance->def:Vocab.hasBalance", "…the other four binds edges…"],
 "stale": []}
```

A verdict can also sit on a function. This one says the proved scenarios leave no input of `withdraw` out:

```json
{"node": "fn:lean:wallet.Wallet.withdraw", "outcome": "review", "code": "INPUTS-COVERED",
 "flags": ["MUTANTS-SURVIVING-THE-SCENARIOS: 0 of 5"],
 "chain": ["covers:stmt:Coverage.g1->fn:lean:wallet.Wallet.withdraw",
           "requires:stmt:Coverage.g1->stmt:Spec.wallet.withdraw_too_much.stmt",
           "requires:stmt:Coverage.g1->stmt:Spec.wallet.withdraw_covered.stmt"],
 "rests_on": ["kernel-checked", "tool-trusted"], "detail": "every input is covered by the Givens of a proved universal scenario"}
```

## 5. Worked example: maths

From `clausal/schema/maths-example.graph.json`. The data is real: the Pell lift is transcribed from
`out/demo/generated/Pell.exists_of_not_isSquare.filtered.md`, and the recurring statement is read from
`out/reuse/`. The script only reads those files.

A theorem with two proofs. Mathlib's is taken as given; the decomposed one was kernel-checked by the demo:

```json
{"id": "stmt:Pell.exists_of_not_isSquare", "kind": "statement", "status": "accepted",
 "origin": {"by": "human:mathlib-authors"},
 "reviews": [{"by": "human:mathlib-maintainers", "decision": "approved", "digest": {"alg": "sha256-text", "value": "…"},
              "note": "merged in Mathlib (an illustration of an accepted node; the exports do not record reviews)"}],
 "interface": {"language": "lean", "text": "{d : ℤ} (h₀ : 0 < d) (hd : ¬IsSquare d) : ∃ x y, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0", "…": "…"},
 "implementations": [
   {"id": "mathlib", "language": "lean-proof", "ref": "Pell.exists_of_not_isSquare", "complete": true, "hidden": false,
    "metrics": {"size_dag": 7089, "size_tree": 319530},
    "realises": [{"kind": "tool-trusted", "by": "tool:mathlib-olean", "scope": {"quantifier": "all"},
                  "detail": "imported from Mathlib's compiled .olean; not re-checked by the demo, axioms of the original not printed"}]},
   {"id": "filtered", "language": "lean-proof", "ref": "Pell.exists_of_not_isSquare.filtered", "complete": true, "hidden": false,
    "metrics": {"size_dag": 1728},
    "realises": [{"kind": "kernel-checked", "by": "tool:lean-kernel", "run": "run:demo-filtered",
                  "artifact": "Pell.exists_of_not_isSquare.filtered", "axioms": ["propext", "Classical.choice", "Quot.sound"],
                  "scope": {"quantifier": "all"}, "method": "script-session"}]}]}
```

A lifted lemma: proposed by a tool, kernel-checked, proof hidden from readers of the parent, its statement size
checked against a budget, and an English reading and a rating attached afterwards by a model, unreviewed:

```json
{"id": "stmt:Pell.exists_of_not_isSquare.filtered_2", "kind": "statement", "status": "proposed",
 "origin": {"by": "tool:rosette.lift", "run": "run:demo-filtered"}, "reviews": [],
 "interface": {"language": "lean",
   "text": "Pell.exists_of_not_isSquare.filtered_2 {d : ℤ} (h₀ : 0 < d) (hd : ¬IsSquare d) : let ξ := √↑d; Irrational ξ",
   "identity": {"alg": "sha256-text", "value": "…"},
   "metrics": {"size_dag": 38, "num_hyp_args": 2},
   "budgets": [{"measure": "closed statement DAG size (LiftConfig.maxStatementSize)", "value": 38, "max": 150, "within": true}]},
 "implementations": [{"id": "p1", "language": "lean-proof", "ref": "Pell.exists_of_not_isSquare.filtered_2", "complete": true,
   "hidden": true, "metrics": {"size_dag": 104, "x_size_dag_before_lifting_children": 367},
   "realises": [{"kind": "kernel-checked", "…": "…"}]}],
 "labels": [{"kind": "explanation", "text": "√d is irrational (verbatim the author's `have hξ`)", "by": "model:rosette-demo-writeup",
             "about": {"alg": "sha256-text", "value": "…"}, "reviews": []},
            {"kind": "rating", "text": "meaningful", "by": "model:rosette-demo-writeup", "about": {"…": "…"}, "reviews": []}]}
```

The two edges of a lift. The decomposed *proof* of the parent calls the lemma (a dependency of an implementation,
not of the statement), and the lemma was cut out of the parent's proof:

```json
{"id": "uses:stmt:Pell.exists_of_not_isSquare[filtered]->stmt:Pell.exists_of_not_isSquare.filtered_2", "relation": "uses",
 "from_end": "implementation", "from_implementation": "filtered",
 "occurrences": [{"role": "haveValue", "implementation": "filtered", "attrs": {"head": "irrational_nrt_of_notint_nrt", "term_path": "not exported by Rosette/Demo.lean"}}],
 "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.lift", "run": "run:demo-filtered",
               "detail": "the kernel-checked rewritten proof calls Pell.exists_of_not_isSquare.filtered_2"}]}

{"id": "lifted_from:stmt:Pell.exists_of_not_isSquare.filtered_2->stmt:Pell.exists_of_not_isSquare[filtered]", "relation": "lifted_from",
 "to_end": "implementation", "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.lift", "…": "…"}]}
```

If the statement of `filtered_2` is edited, `graphlint` reports as stale: both edges above, the `lifted_from`
edge of its child, the `filtered` proof of the parent (it calls a lemma whose statement changed), the lemma's
verdict, and both labels. The parent's *statement* is not affected. That distinction, between what a statement
depends on and what a proof depends on, is the one a Lean blueprint draws with `\uses` in a statement versus in a
proof.

A statement that recurs: `Complex.re ⁻¹' Set.Ioi 1 ∈ nhds 2` occurs as a sub-proof in 4 Mathlib theorems with 2
distinct proof terms. It is one node, identified by its structural hash, with two implementations and four
`lifted_from` edges. Nothing was created or kernel-checked, so its evidence is tool-trusted and its verdict `open`:

```json
{"id": "stmt:lean-struct64:e603d8e562b66b6b", "kind": "statement", "status": "candidate",
 "origin": {"by": "tool:rosette.reuse", "run": "run:reuse"},
 "interface": {"language": "lean", "text": "Complex.re ⁻¹' Set.Ioi 1 ∈ nhds 2",
   "identity": {"alg": "lean-struct64", "value": "e603d8e562b66b6b"},
   "digests": [{"alg": "lean-struct64-L1", "value": "fd6282eb7a8107ea"}, {"alg": "lean-struct64-L2", "value": "980abac6e3a9f509"}]},
 "implementations": [{"id": "t1", "language": "lean-term", "digest": {"alg": "lean-proof64", "value": "7fbe27e4072401d1"}, "…": "…"},
                     {"id": "t2", "language": "lean-term", "digest": {"alg": "lean-proof64", "value": "fca904aec77d3d18"}, "…": "…"}]}

{"node": "stmt:lean-struct64:e603d8e562b66b6b", "outcome": "open", "code": "CANDIDATE-ONLY",
 "flags": ["RECURS-IN-4-THEOREMS", "2-DISTINCT-PROOFS"], "rests_on": ["tool-trusted"]}
```

And a case that shows why printed text cannot be the identity of a Lean statement. The same lift produced
`filtered_5` and `filtered_2.filtered_2`. Both print as `{d : ℤ} (h₀ : 0 < d) : √↑d ^ 2 = ↑d`, but their closed
statements have 70 and 55 nodes, so the printer is hiding a difference. They are two nodes, joined by an
`equivalent` edge whose evidence list is empty:

```json
{"id": "equivalent:stmt:Pell.exists_of_not_isSquare.filtered_2.filtered_2->stmt:Pell.exists_of_not_isSquare.filtered_5",
 "relation": "equivalent", "evidence": [],
 "attrs": {"why_claimed": "the two statements print identically",
           "why_unsupported": "their closed statements differ in size (55 and 70 DAG nodes) …"}}
```

## 6. How this lines up with existing formats

From knowledge of these formats, not from a fresh check against their current documentation; only the first is
covered by the repo's own `out/prior_art.md`.

- **Lean blueprint / LeanArchitect.** The split between what a statement uses and what its proof uses is
  `from_end`. A blueprint node (label, LaTeX statement, Lean declaration, formalised flags) maps onto a node with
  a `latex` interface and labels, so a graph could be exported as a blueprint.
- **Requirements traceability (Doorstop, sphinx-needs, SysML).** The fingerprint stored with a review and with
  each link, which makes a link "suspect" when its target changes, is `review.digest` and `evidence.inputs`.
- **SARIF 2.1.0.** The runs table, the outcome vocabulary and the location shape are borrowed. SARIF is a format
  for results, not for graphs; verdicts could be exported to it for CI.

## 7. What changed from version 1, and why

The schema review measured each of these on the real version-1 graph.

| Version 1 | Version 2 | Why |
|---|---|---|
| one `implementation` per node | `implementations[]`; where a use occurs is on the edge (`occurrences`) | a theorem with two proofs, and a statement recurring in four proofs, could not each be one node |
| `inputs_sha256` (mostly empty) and a stored `stale: false` | `inputs: [{node, end, digest}]` on every entry; staleness computed | 177 of 205 entries listed no inputs, and only 7 of 66 listed hashes matched anything in the graph |
| `interface.sha256` of printed text | typed `identity` digest; `text_complete` | printed Lean is truncated, and is neither injective nor stable (section 5) |
| no authorship; "human-asserted by UNREVIEWED" | `origin`, `status`, `reviews`; unreviewed means an empty evidence list | 35 of 35 human-asserted entries had no human behind them |
| kernel-checked used for "this constant occurs in that term" | kernel-checked requires a theorem name and axioms; the rest is tool-trusted | 42 of 52 kernel-checked entries had no theorem behind them |
| one `uses` relation | `uses` with `from_end`; `requires` for side conditions | a statement depending on X and a proof depending on X go stale differently |
| sizes in free-form `attrs.size` | `metrics` with fixed names; `budgets` | `size` meant three different things |
| verdict `status` from a Gherkin-specific list | `outcome` (SARIF kinds) and an open `code` | a lemma's state could not be expressed |
| unknown fields accepted | `additionalProperties: false`; lint for ids, endpoints, kinds per relation | the version-1 schema accepted 7 of 8 deliberately broken graphs |
| one graph-wide `toolchain` | `runs[]` | the two sides are on different Lean versions |

Added beyond the review's proposal: the `covers` relation and verdicts on function nodes (input coverage);
`evidence.method`; the second reading of each phrase as its own `definition` node with a tested `equivalent`
edge; the staleness propagation rule, which the review left unwritten.

## 8. Open questions

1. **Identity of a Lean statement.** The software side uses a digest of generated text, which is adequate there
   because the generator is deterministic. The maths side needs a structural hash. `lean-struct64` is 64 bits,
   small for a key across a whole library, and the lifted-lemma export does not include it at all, which is why
   the Pell lemmas in the example fall back to name plus printed text. Decide on one structural hash, wide enough,
   and export it for every statement.
2. **The maths side does not emit this format.** The example was assembled by a script, partly from a Markdown
   report. To generate it mechanically, `Rosette/Demo.lean` and `Rosette/Reuse.lean` need to emit, per candidate
   and per lifted lemma: declaration name, term path, statement hash, proof hash, and the axioms of the original
   theorem. Until then this schema's fit to the maths side is demonstrated on 11 nodes, not on a corpus.
3. **No English-first claims on the maths side.** `claim` and `formalises` have real data only on the software
   side. On the maths side the English is written after the fact and is a `label`. Whether a lemma should ever
   get a `claim` (for example from a paper or a blueprint) is undecided.
4. **`generalises` has no data.** The relation is reserved for the reuse work's generalisation levels (the L1 and
   L2 digests); nothing produces such an edge yet.
5. **Staleness is implemented but not exercised incrementally.** Every slice run rebuilds the whole graph. The
   rule has been tried only as "what if this node changed". It over-approximates: a definition edited without
   changing its meaning still marks everything downstream.
6. **Reviews of edges.** A sign-off is recorded as human-asserted evidence on a `binds` edge, while `reviews`
   exist only on nodes and labels. That asymmetry works but is not principled.
7. **Authorship is coarse.** Hand-written slice files all carry one origin (`model:slice-build-agent`, from
   `glossary.yaml`). Per-file or per-change authorship would need version control, which this repo does not have.
8. **Budgets.** One real budget fires in the software graph (a 45-node definition against a threshold of 40) and
   the maths example carries the lift's statement-size limit. The weighted measure in `AGENTS.md` rule 4 has a
   place to go (`budget.measure`, `params`, `relative_to`) but nothing computes it.
9. **A claim with no scenario.** The feature file's opening paragraph ("an operation that cannot be carried out
   exactly is rejected and leaves every balance as it was") is free text bound to nothing. The schema could hold
   it as a `claim` with no `formalises` edge; the generator does not create such nodes.
