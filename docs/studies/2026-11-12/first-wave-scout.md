# Phase 2 first wave: implementation scout

The pipeline directory was renamed from `slice/` to `clausal/` while I was reading (about 23:15). All paths below use the new layout: `clausal/clausal/` is the Python package and `clausal/clausebook.yaml` is the catalogue. When I last looked, file contents were only partly renamed: `clausal/run.sh` still called `python3 -m slicegen` and `clausal/clausal/newrules.py:31` still opened `vocabulary.yaml`.

## 0. Findings that change the briefs

1. **R1 is smaller than planned.** I ran the patched binary `census/fork/bin/aeneas-p5` on the existing `clausal/build/wallet.llbc` and `ledger.llbc`, writing to my scratchpad. `Generated/Wallet.lean` and `Generated/Ledger.lean` are byte-identical to `clausal/lean/Generated/`, with and without `-warnings-as-errors`. The per-crate `translation.json` is identical apart from `aeneas_version`. No Lean was built on the result.
2. **`p2/base/workcopy.sh` is broken by the rename.** `p2/base/.tools` and `p2/base/lean/.lake/packages` are symlinks to `/Users/will/dev/lean-rosette/slice/...` and now dangle, as do those in `p2/arm-opus`, `p2/arm-fable` and `p2/score/work/*`. The script does `cd "$HERE/.tools"` and will fail. Use `clausal/mutation/workcopy.sh`.
3. **The static grammar already has synonyms**, against the "one canonical sentence per meaning" rule:
   - Five entries in `clausebook.yaml` have more than one surface form: `l.balances_of` (4), `l.balance_at` (2), `l.the_transfer` (2), `aggregate` (2), `monotone` (2).
   - `Compiler.rule_part` in `clausal/clausal/vocab.py` (about line 1009) hard-codes four verb phrases for two meanings: "is always accepted", "always succeeds", "is never accepted", "is always rejected".
   - `ARTICLES = ("a ", "an ", "every ", "any ")` at `vocab.py:37`.
   - L1 and C1 each need a ruling on which form is canonical.
4. **The "core" modifiers are not fixture-free in the YAML.**
   - `amount_value`, `index_number`, `index_count`, `balances_value` and `amount_result` have holes typed `amount`, `index`, `balances`. Those literal types are defined in `clausal/glossary.yaml` (`param_types`).
   - `internal` reads a per-operation `internal: {member, parties}` field.
   - The header has `lean_imports: [Wallet.Pieces, Ledger.Pieces, Frames.Lemmas]`, `lean_files`, `literal_lean` and `type_echo`, all fixture-specific.
   - The Lean side is clean: `lean/Frames/Core.lean` has no import, and the other three `Frames` files import only `Frames.*`.
5. **No sign-off file exists.** The code reads `clausal/vocabulary.signoff.json` (`vreport.py:181,198`) and `clausal/glossary.signoff.json` (`report.py:76,1907`); neither is present. `clausal/review/` holds agent review evidence, not sign-offs.
6. **The wallet-versus-ledger choice is silent by construction.** `Compiler.rule` (`vocab.py:913`) tries every domain and reports AMBIGUOUS only if more than one parses. "transfer" is a noun of both `w.transfer` and `l.apply`, but "all balances" without "of the ledger" parses only in the wallet domain.
7. **Disk is 96% full** (84 GB free). Each working copy is 1.3 GB (`compare/rerun.sh`) to 4 GB (`trials/sentences/README.md`) of APFS clones.

## 1. Working copy, timings, concurrency

### Making an isolated copy

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
bash /Users/will/dev/lean-rosette/clausal/mutation/workcopy.sh /abs/path/to/<builder>/clausal
```

What `clausal/mutation/workcopy.sh` does:

- **Copies** the tree with `rsync -a --delete`, excluding `.tools`, `lean/.lake`, `out`, `review`, `probe`, `compare`, `build`, every `target/`, `__pycache__` and `mutation/results*`.
- **Symlinks** `.tools` and `lean/.lake/packages` (7.2 GB) to the real tree by absolute path.
- **Clones** (`cp -c`) `lean/.lake/build` (100 MB) and five cargo `target` directories: `wallet-bdd` 776 MB, `evidence` 188 MB, `evidence/kani`, `wallet`, `ledger`.
- **Touches every `.rs`**, so the local crates recompile on first run; dependencies do not.

Caveats for builders:

- **A refresh deletes work.** `--delete` removes anything the builder added. Never rerun it on a copy that holds work. The non-deleting variant is the `p2/base/workcopy.sh` pattern (first-time-only copy of proofs and lemmas).
- **`build/` starts empty**, so step 2 of `run.sh` (Charon and Aeneas) must run; `gen` needs `lean/translation.json`, which is copied.
- **The copy is not a git checkout.** Porting back is a diff against a pristine copy, applied by one owner. No script for this exists.
- **Every copy shares `.tools`**, so R1 must not change `.tools` in place while other copies run.
- **`trials/sentences/try_compile.py` and `run_v4.py` use one fixed path**, `trials/sentences/work/clausal`. Two builders using them at once collide. Each should copy `trials/sentences/` or parameterise `WORK`.
- **Put copies outside `clausal/out`**, which the script refuses. `clausal/build/` is git-ignored and is what the mutation harness uses.

### Timings (recorded in the repository; I ran no pipeline)

| What | Time | Source |
|---|---|---|
| `./run.sh` full, warm | about 11 min (10 min 39 s, 11 min 16 s) | `clausal/FINDINGS.md` lines 534, 636, 686 |
| of which Kani | 463 s bounded, 99 s witness replay, 25 s property tests | `clausal/out/evidence.json` `cost` (last run, 6 jobs, 30 s per harness) |
| `./run.sh --quick`, warm | about 2.5 min (2 min 23 s) | `clausal/FINDINGS.md:534` |
| `./run.sh` before the evidence step existed, load 4 | 66 s | `clausal/FINDINGS.md:417` |
| `python3 run_v4.py` (compile, one Lean run, property tests, replay) | about 15 s warm; 2.5 min with `--kani` | `trials/sentences/README.md` |
| Mutation harness, 61 quick runs, 8 jobs, idle machine | about 16 min | `clausal/mutation/run_mutants.py:28` |
| Mutation harness, 83 runs, 2 jobs, load 8 to 20 | 2 h 2 min | `clausal/FINDINGS.md` (about line 693) |
| One warm `lake build <module>` | about 5 s | `clausal/effort/attempts.tsv` |
| Patched Aeneas on one crate | 0.6 to 0.8 s | my scratch run |

- **Cold `./run.sh` is not recorded anywhere I found, and I did not measure it.** The only first-time figures are from the one-function stage in `clausal/TOOLCHAIN.md` (lines 56 to 100): `lake update` with the Mathlib cache 1 min 46 s, first Charon 12.7 s, first `lake build` 9 s.
- **The first run after the rename may be slower** than warm, because cargo target directories moved with their paths. Not verified.

### Concurrency on 18 cores (6 + 12, 128 GB)

- **A full run is not single-threaded.** Kani runs 6 harnesses at a time (`evidence.py:147`), step 5 starts three Lean interpreters, and `lake build` is parallel.
- **Bounded-check results depend on load.** "Which rungs answer varies with the load" (`FINDINGS.md:543`): 36 or 37 of 269 harnesses give no answer in 30 s.
- **Measured or compared runs** (any "every verdict identical" check that includes Kani rungs, any timing): one at a time, on a quiet machine.
- **Correctness-only iteration with `--quick`:** the mutation harness ran 8 copies at once on an idle machine at about 2 min per run, so 4 at once is conservative. That is my inference from the harness header, not a measurement.
- **Full Kani runs:** at most two at once, and not when rung results are being compared.

### Tests that exist

| Test | Command (in a copy) | Needs |
|---|---|---|
| Rule parser, tag inheritance, adequacy bookkeeping | `python3 -m clausal.selftest` | no Lean, no Rust (not timed by me) |
| Schema and lint rejections | `python3 schema/selftest.py` | a finished `./run.sh` |
| Whole pipeline; exit 0 iff every scenario has its expected verdict | `./run.sh [--quick]` | everything |
| 45 mutants and 27 controls, including sign-off controls with a test reviewer | `python3 mutation/run_mutants.py --jobs N` | scratch copies under `build/mutation/` |
| The 48 frozen sentences, as written | `python3 check_author.py authors.json --compile` in `trials/sentences/` | `work/clausal` copy |
| The sentence trial | `python3 run_v4.py [--kani]` | same |
| Echo trial chain | `python3 run_tests.py --bank banks/generated-echoes-v1` in `trials/meaning/` | — |

For "every existing verdict identical", `observe()` and `observe_rules()` in `clausal/mutation/run_mutants.py` (lines 527 to 549) already extract scenario and rule verdict codes from `out/graph.json`. The last run has 105 verdicts: 39 scenarios, 46 rule groups, 20 functions.

## 2. Node briefs

### C1: split the catalogue

**Files to change**

- `clausal/clausebook.yaml`: one file with a fixture-specific header, `operations` (8), `pieces` (32 domain, 28 modifier, 25 frame), `frames_without_surface` (1) and `idioms` (3). The counts match the plan's 96.
- `clausal/clausal/vocab.py`, `Vocabulary.__init__` (line 114): takes one path. `line_of` (150) and `vreport.entry_text` (147) find an entry by scanning that file's lines, and error messages print `rel:line`.
- Loader call sites: `pipeline.py:147`, `newrules.py:31`, `pipeline.spec_digest` (87 to 102, which lists the catalogue, `Wallet/Pieces.lean`, `Ledger/**` and `Frames/**` by path).
- `clausal/clausal/vreport.py`: `lean_defs` (125) reads the `lean_files` map; `load_piece_signoff`, `reviewed_pieces` and `review` (180 to 199) use one sign-off file.
- `clausal/lean/lakefile.toml`: `Frames` is already its own `lean_lib` with a comment saying it can be lifted into a package. `lake build Frames` is the "build core alone" check on the Lean side.
- Hard-coded fixture imports in generators: `rsearch.py:215`, `links.py:498-501`, plus `L.mkBatch` and `Vocab.mkWallet` in `links.py:75,83,444` and `oblig.py:373`.

**What helps**

- A piece's digest is its entry text with comments stripped plus the text of its Lean definitions (`vreport.piece_digest`, 174). Moving an entry verbatim to another file keeps its digest.
- `Parser.forms_for` (245) already filters by `domain in ("shared", self.domain)`.

**Open questions for the builder (not decided anywhere I found)**

- Where the literal types `amount`, `index`, `balances` live once core may not name a fixture noun (finding 4).
- Whether the Rust per-piece readings are split too. `wallet-bdd/src/pieces.rs` (668 lines, about 95 match arms), `evidence/src/typed.rs` (395 lines) and the per-piece `if p == ...` chain in `evgen.py` (about lines 150 to 330) mix core and fixture pieces. The plan's target only says core is "checked by building it alone".
- Which form is canonical for the five multi-form pieces (finding 3).

**Tests and freeze**

- Before starting, freeze a baseline in a pristine copy: one quiet full `./run.sh`, the `observe()` and `observe_rules()` dumps, and the commit hash.
- After the split, compare verdict codes and the `RBITS` strings in `out/rsearch.log`.
- The plan requires the pack-or-local assignment of each domain entry, with its reason, to be written down before the split.

**Conflicts:** L2 (same YAML, `vocab.py`), L1 (reads the loader), E2 (`report.py`, `vreport.py`).

### L2: the missing pieces

Source: `trials/sentences/rewordings.py` (the `R` dictionary; `text=None` means no rewording keeps the meaning). The authors' sentences are in `trials/sentences/authors.json` and `results.json`.

**The 18 sentences with no rewording, by piece**

| Piece (name in `rewordings.py`) | Sentences |
|---|---|
| Comparison of two values known before the call (`P_TERM_EQ`) | `opus-1/r3`, `haiku-1/R03`, `default-1/R04`, `default-1/R10`; `sonnet-1/R10` also needs a conjunction of conditions (`P_COND_AND`) |
| "Every balance" inside a claim about a quantity (`P_EVERY_PART`) | `sonnet-1/R5`, `default-1/R05`; `opus-1/r5` and `haiku-1/R04` also need an invariant over any sequence of operations (`P_INVARIANT`) |
| Sequence of calls with tied inputs (`P_SEQ_TIED`) | `opus-1/r9`, `opus-1/r12`, `sonnet-1/R12`; `sonnet-1/R11` and `default-1/R12` also need a comparison of two sequences (`P_SEQ_COMPARE`) |
| A condition naming another operation's answer (`P_OTHER_OP_COND`) | `opus-1/r10` |
| A further reference function (`P_REFERENCE`) | `haiku-1/R11` |
| A further measure of the state, the number of accounts (`P_MEASURE`) | `default-1/R08` |
| A claim scoped by an answer class, "stopped early" (`P_ANSWER_COND`, `P_ANSWER_CLASS`) | `default-1/R11` |

- **Four more compile only in part and need a piece:** `opus-1/r11` (`P_EVERY_PART`, the fifth rule for that piece), `sonnet-1/R8` (a condition "every transfer of the batch can be applied in order"), `sonnet-1/R9` (`P_RESULT_TERM`), `haiku-1/R10` (`P_SUM_IS`, `P_COND_AND`).
- **So the three first pieces alone could fully serve 9 of the 18**, upgrade `opus-1/r11`, and leave 5 needing a second piece. I did not check by compiling that the rest of each sentence composes.
- **Five `P_EVERY_PART` rules cannot be false on the fixtures** (u64 balances, maximum 2^64 − 1; noted in `rewordings.py`). The required "toy case where it is false" has to come from `lean/Run/FrameToyTests.lean`.

**What each new piece touches**

1. `clausebook.yaml`: the entry (`forms` or `then_forms`/`vp_forms`, `lean`, `echo`, `defs`; frames also need `at`, `check`, `flat`, `number`).
2. Lean: `lean/Frames/Core.lean` (modifiers), or `lean/Frames/Frames.lean` plus the executable reading in `lean/Frames/Check.lean` (frames).
3. Rust tree evaluator: `wallet-bdd/src/pieces.rs` (`eval` at 194, `frame_content` at 451).
4. Typed Rust generation: `clausal/clausal/evgen.py` (`gen`) and `evidence/src/typed.rs`.
5. Hand-written frame instances: `lean/Run/FrameTests.lean` and `FrameToyTests.lean`.
6. A fixture sentence in `clausal/features/`. This changes rule counts, which the mutation control texts depend on (`FINDINGS.md`, "Still open from the review").

**Existing code per piece**

- **Comparison of two values:** `is` is `{m:measure<T>} is {t:term<T>}`; `more_than` and `exceeds` are term against measure. No term-against-term condition exists. `l.sender`, `l.receiver` (`term<acct>`) and `l.amount_of` (`term<num>`) are the operands. Likely YAML plus the Rust arms, with no parser change.
- **Every balance:** `every`, `no_such`, `some_of` exist as conditions over `coll<T>` with `itempred<T>`. The only collection is `l.transfers` and the only item predicate is `l.valid`. The claim-side frame `every_of` ranges over a collection read off the answer (`acoll<T>`), not over the state. A state collection in a claim means a new frame or a change to `Frames.EveryOf`, which is a core change.
- **Tied sequence:** sequences exist (`and_then`; `follow_splits` at `vocab.py:1234`). `Compiler.subjects` (1031) drops a sequence whose operations share an input role name, with the comment "two operations of a sequence give the same role name: which is meant?" That is why "a deposit followed by a withdrawal" is refused. This piece needs a code change in `subjects`, in the `rsearch.grid` input pairing and in the Rust `run_seq`, not only YAML.

**Tests:** `./run.sh --quick` while iterating and one full run at the end; `check_author.py authors.json --compile` for the as-written trend. The 48 sentences and their cases are frozen.

**Conflicts:** C1 (the plan says C1 first or one owner); E2 (`evgen.py`, `features/`); L3 (`rsearch.py`, if sequence grids change).

### L3: separating inputs

**What search exists**

- **`lean/Run/Search.lean`** (generated by `emit.search_file`, `emit.py:276`): the boundary-grid search for flat glossary statements only. It is not useful for comparing two readings.
- **`lean/Run/ReadingSearch.lean`** (generated by `rsearch.search_file`, `rsearch.py:209`; 84 search functions):
  - Per reading, nested loops over a grid from `glossary.yaml` `param_types.*.sample`: six u64 values, five indexes, ledgers of at most four accounts, batches of at most four transfers.
  - Prints `RSEARCH` (tried, in scope, first false point) and `RBITS`, one bit string per grid point. The sidecar `layout` says what each bit is (scope per unit, relation, claim).
  - `rsearch.parse` (327) and `point_terms` (380) turn an index back into values.
- **`newrules.script` and `cmd_compile`** (`newrules.py:57,69`): compile any feature file and write `lean/Run/NewReadings.lean` through the same generator. This is the entry point for arbitrary candidate sentences.
- **Rust side:**
  - `wallet-bdd/tests/grid.rs` prints the same bits on compiled Rust.
  - `evidence/src/main.rs` has `--only` and `--replay inputs.jsonl`, which evaluates a reading at given inputs.
  - `evgen.kani_file` (645) writes one harness per reading and rung.

**How to build it**

- **Same operation, same state and input types** ("accepted only" against "accepted or rejected"; `>` against `>=`): `rsearch.grid` (55) names variables from the operation's roles, so both readings get the same grid. A separating input is the first grid point where (scope and all claims) differ between the two `RBITS` strings. That is a Python comparison over existing output with no new Lean.
- **Stronger "none found within stated bounds":**
  - A property test in which the two generated checks disagree, with shrinking. `main.rs` already compares `check_<n>` against the tree evaluator at every case, so the comparison shape exists.
  - A Kani harness asserting the two checks agree, per rung.
  - Both are new code in `evgen.py` and `main.rs`.
- **Wallet against ledger:** the two readings have different state types, and `same_grid` (139) already skips a rule whose clauses differ in type. No common input exists. The report has to be "this noun names operations in two systems", with an input in each; how to present that is a design decision. Detection is a check of `voc.ops[*].nouns` across domains. Per the plan, the compiler keeps its behaviour and the check lives in the L3 tool or the composer.

**Tests:** none exist for this. The targets are the three cases in the plan row.

**Freeze:** the grid samples and the Kani ladder are the "stated bounds".

**Conflicts:** low if written as a new module (`clausal/clausal/separate.py`) with one new line in `pipeline.main` (488). `evgen.py` is shared with E2 and L2 if the Kani variant is built.

### L1: `clausal compose`, suggest mode

**What exists**

- **Recognition only.** `Vocabulary.forms` (`vocab.py:113`) maps (category, voice) to `Form` objects with literal and typed-hole segments. `Parser.parse` and `_match` (254, 266) return every tree for a text. `_build` applies idioms.
- **Rule skeleton by string splitting, not by forms.** `Compiler.rule` (913), `clause` (952), `subjects` (1031), `rule_part` (1006), `clause_splits`, `and_splits`, `follow_splits` (1205 to 1236). The shape is: article, optional successful/rejected/internal, operation noun, optional "followed by", optional "for which", then a verb phrase; or "for <subject>, <claim>".
- **Hints.** `nearest` (572) uses `difflib.get_close_matches` over form texts. On the 48 sentences it produced only the operation-noun list in 35 of 48 refusals (`trials/sentences/RESULTS.md`).
- **Tree utilities.** `describe` (599) gives a stable key per tree; `say` and `echo_rule` give the English reading; `Reading.lean_def` gives the Lean statement; `trees.tj` (`trees.py:37`) gives JSON trees.
- **Compile API.** `newrules.compile_files(paths)` and `trials/sentences/try_compile.py:compile_lines(lines)` return status, message, hint, echo, Lean text, pieces and frames, with no Lean run.
- **Scoring material for L4(b).** `trials/sentences/cases.py` (the authors' cases encoded as inputs) and `run_v4.py` (replay through `rule-evidence --replay`). `rewordings.py` holds 30 expert rewordings; using them to tune the composer would break the freeze rule.

**What does not exist**

- No tree-to-sentence renderer for the canonical surface. `Node.form` records the matched form, but nothing fills a form's holes recursively.
- No generator over forms.
- No `compose` subcommand.

**Enumerating candidates without a model**

1. **Anchor.** Find operation nouns from `voc.ops[*].nouns` in the rough text, with a stem and synonym table kept in the composer only. Take every domain where a noun matches. That also yields the wallet-versus-ledger question for L3.
2. **Generate.** For each subject (operation; none, successful or rejected; optional "for which" condition), enumerate verb phrases top-down from `voc.forms[("claim","vp")]` and `("claim","then")`. Fill holes by category from forms of that category, to a small depth. Leaves are the operation's roles (`op_roles`, 607). There are 25 frames, of which 13 have a `vp` form, so the typed space is small.
3. **Render and verify.** Render with the first form of each piece and round-trip through `Compiler.rule`. Keep a candidate only if it compiles to exactly the generated tree (same `describe` key), which gives "every sentence it writes compiles as written" by construction.
4. **Rank.** Score by word overlap between the rough text and the candidate's form literals and `echo`. Deduplicate by key. Cap the list.
5. **Separate.** For the top candidates that differ, call L3.

**Where a model could sit:** proposing piece ids or whole candidate sentences (each accepted only if step 3 passes), or reordering the list from step 4. It is never the source of a reading, and the shown reading is always `echo_rule` output.

**Freeze before L4(b):** the ranking rule, the candidate cap, the depth bound, the synonym table and any prompt, in a commit.

**Conflicts:** none if it is a new module (`clausal/clausal/compose.py`) plus one line in `pipeline.main`. It depends on C1's loader signature and on the canonical-form ruling.

### R1: wire the patched translator

**How the pipeline pins and finds Aeneas today**

- `clausal/translate.sh` lines 17 to 21: `AENEAS_TAG="nightly-2026.11.09-5a392f4"`, asset name, sha256, `RUST_NIGHTLY="nightly-2026-09-17"`, `CRATES="wallet ledger"`.
- The tarball is unpacked to `clausal/.tools/aeneas-<tag>/` (`aeneas`, `charon`, `charon-driver`, `backends/`, `rust-toolchain`). `TOOLS="$HERE/.tools/aeneas-$AENEAS_TAG"`.
- The script calls `"$TOOLS/charon" cargo --preset=aeneas`, then `"$TOOLS/aeneas" -backend lean ... -warnings-as-errors` (line 78).
- `clausal/lean/lakefile.toml:9` and `lake-manifest.json:9` require the Aeneas Lean library by path `../.tools/aeneas-nightly-2026.11.09-5a392f4/backends/lean`.
- `lean/provenance.json` records `aeneas -version`; `report.py:222,839` reads it.
- `clausal/TOOLCHAIN.md` documents the pins (table at lines 25 to 30).

**The fork** (`census/fork/FORK.md`)

- Source at `census/fork/aeneas`, base `0d21a9ec` (one commit after the pipeline's `5a392f4b`), five patch commits on top; patches in `census/fork/patches/0001` to `0005`.
- Binaries `census/fork/bin/aeneas-{base,p1..p5}` are git-ignored. `aeneas-p5 -version` prints `81c0b10c-dirty`, so it was built before the fifth commit was made.
- Build: `source census/fork/env.sh` (opam root in `census/fork/.opam`), then `dune build` in `census/fork/aeneas/src`, 40 s. First-time opam setup is about ten minutes.
- `FORK.md` says the generated Lean was compiled against the 11.09 Lean library on Lean v4.35.0, because the 11.10 library needs a newer Lean and Mathlib. So only the `aeneas` binary changes: keep the release `charon`, the lakefile path and the Lean toolchain.

**Change needed**

- `translate.sh`: a pinned path or sha256 for the patched binary, used in place of `$TOOLS/aeneas` at lines 60 and 77 to 79; drop `-warnings-as-errors` as the plan says.
- `TOOLCHAIN.md` and a `DECISIONS.md` entry.

**Open for the builder**

- The binary is not reproducible from a clean checkout without the opam build.
- The version string in `provenance.json` and `out/graph.json` will change. Decide whether "identical verdicts" excludes that field, and rebuild a clean binary so the string is a commit and not `-dirty`.
- `p2/base/translate.sh` is a separate copy with its own pin; I did not diff it.

**Tests:** full `./run.sh` in a copy, verdict comparison through `observe()`, and `diff -r lean/Generated`.

**Conflicts:** none in files. The opam build writes under `census/fork/`, which needs one owner.

### E2: flag rules whose subject can exceed every size tried

**Where the bounds live**

- **Kani ladder:** `clausal/clausal/evgen.py:33`, `LADDER = [(2, 1), (2, 2), (4, 1), (2, 3), (6, 4)]` (accounts, transfers per batch).
  - `Plan.uses()` (575) says whether a reading has a free list of balances or a free batch.
  - `rungs_of` (625) returns `("no size bound", None, None)` when it has neither.
  - `kani_file` (645) writes `kani::assume(n <= A)` and an `unwind` of the largest size plus 2.
  - Generated output: `clausal/evidence/kani/src/harnesses.rs` (4,276 lines).
- **Property test:** `clausal/evidence/src/main.rs`, `--size 6` (line 4); `free_pick` (212) uses `vec(..., 0..=size)`. `evidence.py:176` records `"size": 6`.
- **Lean and Rust grid:** `clausal/glossary.yaml` `param_types.*.sample` (lines 36 to 68): ledgers of at most four accounts, batches of at most four transfers.
- **Wording:** `evidence.ladder` (`evidence.py:463`) builds "holds for every input with up to ..." or "no size bound". `rules.py:263-281` prints the bounded rung with "it says nothing beyond those sizes". `vreport.py:377,433` assigns TESTED-ONLY.

**What to extend**

- `Plan.uses()` already identifies the readings with an unbounded collection. The flag is: uses a collection, and the verdict is not kernel-proved. Add a field in `evidence.ladder`, a line in `rules.py` and `vreport.py`, and a count in the report summary.
- **The probe fixture:** "For a batch, the number of transfers applied is at most 4", in `clausal/review/step3/my_sentences_with_probe.feature:52-53`, tagged `@expect-refuted` there.
  - It is false at ledger `[0, 0]` with five zero-amount transfers (`compare/e1/E1_TRADES.md:243-248`).
  - As a standing fixture it goes in `clausal/features/ledger_rules.feature` with `@expect-unproved`; `vreport.py:282` maps that tag to an expected TESTED-ONLY.
  - **Risk:** the property test goes up to six items and may find it on some seed. The reviewer's run did not find it in 10,000 cases at seed 20261111, but if it does, the fixture is REFUTED and the control fails. Freeze the seed, case count, size and ladder first.
  - **Baseline:** adding it changes the rule counts the mutation control texts depend on (`FINDINGS.md`, "Still open from the review").

**Tests:** `./run.sh` (the fixture needs the full Kani run once to show the ladder cannot reach it), then the mutation harness, because the counts change.

**Conflicts:** L2 (`evgen.py`, `features/`), C1 (`report.py`, `vreport.py`), and R1's and C1's baselines.

## 3. Shared files

| File | C1 | L2 | L3 | L1 | R1 | E2 |
|---|---|---|---|---|---|---|
| `clausebook.yaml` | restructure | add entries | read | read | – | – |
| `clausal/vocab.py` | loader | `subjects` | – (if kept out of the compiler) | read | – | – |
| `clausal/pipeline.py` (`main`, paths, `spec_digest`) | yes | – | one line | one line | – | – |
| `clausal/rsearch.py` | import lines | sequence grid | reuse or extend | – | – | – |
| `clausal/evgen.py`, `evidence/src/*`, `wallet-bdd/src/pieces.rs` | open question | new arms | optional | – | – | flag |
| `clausal/report.py`, `vreport.py`, `rules.py`, `evidence.py` | sign-off paths | – | – | – | provenance | wording |
| `lean/Frames/*` | move | add | – | – | – | – |
| `features/*.feature` (changes counts) | – | add | – | – | – | add probe |
| `translate.sh`, `TOOLCHAIN.md` | – | – | – | – | yes | – |

## 4. Proposed order

0. **Baseline, serial, after the rename is complete.** One quiet full `./run.sh` in a pristine copy. Save the `observe()` and `observe_rules()` dumps, the `RBITS` lines and the commit hash. Everything that says "identical" compares against this.
1. **Truly parallel, no shared edits:**
   - R1 (`translate.sh` only).
   - C1 (catalogue, loader, sign-off paths).
   - L3 as a new module.
   - L1 as a new module on today's pieces.
   - The code half of E2 (flag and wording).
   - Pipeline runs are still queued: at most two copies running at once, and measured runs alone.
2. **After C1 lands: L2.** It edits the same YAML and `vocab.py`, and each new piece has to be placed in core or the ledger pack. The Lean definitions, second readings and toy false cases for the three pieces can be drafted in a copy during step 1.
3. **After R1's and C1's identical-verdict checks: the fixture additions.** That is the E2 probe and the L2 sentences. Both change rule counts, so they re-baseline and need a mutation-harness rerun.
4. **Then L1 complete** (wired to L3, canonical forms settled), with a freeze commit before L4.

Not parallel: C1 with L2; E2's fixture with any baseline comparison; two builders using `trials/sentences/work/`.

## 5. What I did not check

- I ran no pipeline, build or test. Every timing is quoted from the repository except the 0.6 to 0.8 s Aeneas runs. Cold `./run.sh` is unmeasured and unrecorded.
- The patched-Aeneas output was compared as text only, not built with Lean, and no verdicts were regenerated.
- I did not read `clausal/DESIGN.md` (131 KB), `links.py`, `oblig.py`, `adequacy.py` or `report.py` beyond searches, nor the bodies of `lean/Frames/*.lean`, `Wallet/Pieces.lean` and `Ledger/Pieces.lean`.
- Whether the three L2 pieces are enough for the nine sentences is inferred from `rewordings.py`, not from compiling.
- Whether adding a term-against-term condition creates ambiguities with `is` was not tested.
- I did not check how far the content rename had got when builders start, or whether cargo and Lake caches survive the directory move.
- `p2/base/translate.sh`, the `compare/` harness and `trials/meaning/` were not read beyond listings.
- The sign-off controls in `mutation/run_mutants.py` (`signed()`, line 284) were found but not read, so I cannot say how much of the staleness machinery they exercise.
- Nothing under `private/`, `tdflite-ideas/` or `docs/TDFLITE.md` was opened.