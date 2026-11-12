# Decision study: should the mathematics strand move to its own repository?

All paths are relative to `/Users/will/dev/lean-rosette/`. The `slice/` to `clausal/` rename landed in the working tree while I worked (uncommitted), so I cite `clausal/...`; at HEAD `f6f3895` the same files are under `slice/...`. Nothing was modified, built or deleted.

## 1. Recommendation

**Split later, on a stated trigger: the first quiet window after the X5 rename commit is on `main` and no agent has a dirty working copy, and in any case before the public `clausal` 0.1 release or any name registration.**

- **Not now:** the rename is in flight and other agents are editing `README.md`, `AGENTS.md` and `docs/*`, which the split must also touch.
- **Not "keep together":** the repo root is the strand's Lake project (`lakefile.toml` name `rosette`, Mathlib), and `AGENTS.md` lines 5 and 10 are mathematics rules. A repository called `clausal` would open on a library called Rosette, and the strand is 70% of tracked bytes.
- **The split is cheap:** I found one script pair, one example file, two schema description strings and some doc sections as the only real couplings.

Three findings that correct the existing record:

- **The "frees about 150 GB" claim is wrong.** `TODO.md:16`, `README.md:162` and `docs/HANDOFF_CLAUSAL.md:67-69` attribute it to the mathematics strand, which is about 70 GB on disk. The largest directory is `census/` at 93 GB, which is Clausal-side.
- **A split frees no disk by itself.** Everything large is git-ignored; reclaiming space is a separate act (section 6).
- **The dead-code tool is not used by the Clausal audit.** `docs/HANDOFF_CLAUSAL.md:69` and `docs/PLAN.md:118` (X4) say to keep `tools/deadcode/` because it supports the proof audit. No Clausal file imports or calls it, so I recommend it moves with the strand (section 4).

## 2. Inventory and sizes

### Tracked (`git ls-files` piped to `du -ck`)

| Path | Files | Tracked size |
|---|---|---|
| `Rosette/`, `Rosette.lean` (7 modules, 2,835 lines) | 8 | 144 KB |
| `lakefile.toml`, `lake-manifest.json`, `lean-toolchain` (root project) | 3 | under 10 KB |
| `bench/` | 26 | 920 KB |
| `corpora/` (`families` 118, `lesssim` 21, `ns_reuse` 16, `friction` 14, `ns_export` 7, `tools` 4, `outline2` 2) | 182 | 4.0 MB |
| `tools/` (`deadcode` 9, `families` 17, `reinvent` 16) | 42 | 532 KB |
| `out/` | 804 | 148.7 MB |
| **Strand total** | **1,065 of 3,066** | **about 154 MB of 221 MB (70%)** |

- `out/` by size: `corpus` 71.7 MB, `review_benchmark-validity` 33.1 MB, `review_claims-vs-evidence` 16.6 MB, `bench` 8.3 MB, `reuse` 7.2 MB, `deadcode` 6.4 MB, `families` 4.0 MB, `reinvent` 0.6 MB.
- Largest single tracked file: `out/review_benchmark-validity/rows.pkl` (16.9 MB).
- One Clausal-side file sits in `out/`: `out/prior_art_vocabulary.md`, cited by `docs/ARCHITECTURE.md:150`, `docs/VOCABULARY.md:123` and `docs/PLAN.md:303`.
- For comparison: `clausal/` 1,110 files and 44 MB, `p2/` 632 files and 9.4 MB, `census/` 175 files and 9.7 MB. `.git` is 226 MB, all loose objects.

### On disk (`du -sh`, includes ignored)

| Path | Size | Mostly |
|---|---|---|
| `corpora/` | 58 GB | `ns` 16 GB, `ns_trim` 23 GB, `carleson` 7.5 GB, `pfr` 7.4 GB, `friction` 1.6 GB |
| `.lake/` (root) | 7.3 GB | Mathlib 6.8 GB |
| `out/` | 2.7 GB | `corpus` 1.5 GB, `reinvent` 501 MB, `families` 341 MB |
| `tools/` | 2.2 GB | `reinvent` 1.5 GB, `families` 529 MB, `deadcode` 141 MB |
| **Strand total** | **about 70 GB** | |
| `census/` | 93 GB | `fork/lean` 58 GB, `fork/runs` 15 GB, `work` 8.2 GB, `lean-pinned` 7.2 GB |
| `p2/` | 13 GB | `score` 11 GB |
| `clausal/` | 11 GB | `lean/.lake` 7.3 GB, `evidence` 2.6 GB |
| `private/` | 2.0 GB | |
| Whole directory | 190 GB | `docs/HANDOFF.md` says 170 GB; `docs/SETUP.md` says 55 GB |

The volume is 96% full with 84 GB free (`df -h .`).

### Plan nodes

- **Done:** M1, M2, M4, M7, M8, M9 (`docs/PLAN.md:156-161`, `186-188`, `356-359`).
- **Open:** M3 and M6 (`docs/PLAN.md:358`, `360`, listed "Later" at `:370`); M10 and M11 (`docs/PLAN.md:116-117`).
- No M5 appeared in my search of the plan.

### Strand documents

- Findings: `out/FINDINGS.md`, `out/corpus/FINDINGS.md`, `out/deadcode/M8.md`, `out/reinvent/REPORT.md`, `out/families/FAMILIES.md`, `out/reuse/REUSE.md`, `out/prior_art.md`, `out/demo/README.md`.
- Method: `bench/CORPUS.md`, `tools/deadcode/README.md`, `out/corpus/*/README.md`.
- Shared docs: `docs/ARCHITECTURE.md` section 13 (lines 253-265) and the table in section 14.

## 3. Couplings to the Clausal side, as file-level facts

**Shared code: none in either direction.**
- A grep of `Rosette/`, `bench/` and `tools/` for `slice/`, `slicegen`, `census/`, `p2/`, `trials/` hit only `bench/friction_robust.py` and `bench/friction_census.py`, both on the phrase "friction census".
- Three tracked files under `corpora/` and `out/` also matched and were not inspected: `corpora/families/report.py`, `out/families/FAMILIES.md`, `out/prior_art_vocabulary.md`.
- Nothing in `clausal/`, `census/`, `p2/` or `trials/` imports `Rosette` or calls `bench/` or `tools/`, except the schema scripts below.

**Evidence-graph schema: the one real coupling.**
- `clausal/schema/maths_fit.py` reads `out/demo/generated/Pell.exists_of_not_isSquare.filtered.md` and `out/reuse/{candidates.jsonl,statements.jsonl,clusters.json,run.json}` (lines 5-6, 30).
- It imports `graphlint` from the compiler package (`from slicegen import graphlint`, line 28; that import is now stale after the rename to `clausal/clausal/`).
- It writes `clausal/schema/maths-example.graph.json` (11 nodes, 15 edges).
- Two of its inputs are git-ignored (`/out/reuse/candidates.jsonl`, `/out/reuse/statements.jsonl`), so it already cannot run from a fresh clone.
- `clausal/review/schema/fit.py` (lines 70, 245-382) does the same for the review copy, `clausal/review/schema/maths.v2.graph.json`.
- `clausal/schema/refinement-graph.v2.schema.json` names the strand in two description strings: line 90 (`'lean-struct64' = Rosette.statementHash`) and line 135 (`Rosette.Path`). The hash is defined at `Rosette/Candidates.lean:184`.
- The schema id is `rosette.refinement-graph/2` (first line of `clausal/schema/maths-example.graph.json`).
- `docs/SCHEMA.md` lines 6, 17, 20-21, 76, 190-191, section 5 (301 onward) and 432-453 describe the mathematics side.
- `docs/SCHEMA.md:20` and `:436` state that the mathematics side does not emit the format. Plan node X1b is "Deferred until M2 needs it" (`docs/PLAN.md:284`).
- `run.sh` does not call `maths_fit.py`; only `clausal/clausal/graphlint.py:6` mentions it, in a comment.

**Dead-code, axiom and closure tooling: no use by the Clausal audit.**
- `clausal/lean/Bdd/Audit.lean` imports only `Lean` (line 20) and has its own `closure` (line 40) and its own `collectAxioms` call (line 76).
- `clausal/lean/Bdd/AuditLinks.lean` imports `Lean` and `Bdd.Audit` (lines 26-27).
- `clausal/lean/Run/Audit.lean` is generated and imports only `Wallet.Proofs.*`.
- `tools/deadcode/README.md` says `lean/Export.lean` imports only `Lean` and describes `Axioms.lean` and `Closure.lean`. I did not open the three Lean files; none matched a grep for the Clausal side.
- The two sides implement similar ideas independently. `private/` (excluding its source copy and `.lake`) has no reference to `tools/deadcode`, `Rosette` or `out/deadcode`.

**The dead-code tool is tied to the strand's layout.**
- `tools/deadcode/deadcode.py:140-142` defaults to `out/deadcode/<name>` and `corpora/<name>_trim/m8`.
- Its project files are `tools/deadcode/projects/{ns,pfr,carleson}.json`.
- `tools/families/run.sh:3` reads `out/deadcode/`.
- `tools/reinvent/env.sh` and `tools/families/env.sh` set `SRC=$REPO/corpora/$PROJECT`.

**Toolchain pins: none shared.**
- Root: `leanprover/lean4:v4.36.0-rc2` with Mathlib `v4.36.0-rc2`.
- `clausal/lean/lean-toolchain`: `v4.35.0`, requiring Aeneas by path under `clausal/.tools/`, with its own Mathlib copy in `clausal/lean/.lake` (7.3 GB).
- `corpora/ns`: 4.34.0-rc2; `corpora/carleson`: 4.36.0-rc1; `corpora/pfr`: 4.36.0-rc2.
- `p2/*/lean` and `census/lean-pinned` follow the Aeneas pin.
- `private/tdflite-pilot/*/lean` uses 4.36.0-rc2 with its own lakefiles and no `require` line in the one I read.
- No project uses the root `.lake`. Only `~/.elan/toolchains` and `~/.cache/mathlib` (2.2 GB) are shared, and both sit outside the repo.

**Shared documents.**
- `docs/RESULTS.md`: 16 of 26 rows are mathematics (rows 1-6, 17-23, and three placed after the closing paragraph).
- `docs/EXPERIMENTS.md`: about 18 of 32 numbered entries (0-6, 9-11, 13-17, 27-29). Entry 8 (schema) is joint.
- `docs/PLAN.md`: the M nodes, plus X4.
- `docs/SETUP.md`: 15 of 71 lines.
- `DECISIONS.md`: one append-only log of 1,430 lines; 113 lines mention strand terms.
- `AGENTS.md`: line 5 (root is the `Rosette` project) and line 10 (read `out/FINDINGS.md` before proposing a scoring idea).
- `README.md`: line 149 (strand summary) and line 162.

**Plan-level links, both untested.**
- M6 runs the outline and the dead-code report on a software proof development (`docs/PLAN.md:360`). `docs/PLAN.md:352` says the claim that the strand serves software verification is untested.
- X1b would have the mathematics tools write the shared graph format.
- These two nodes are the only places the strands are meant to meet.

**CI: none in effect.** `.github/` is git-ignored (`.gitignore`: "template CI from `lake new`; not wanted yet"). The three untracked workflows build only the root Lake project.

**History.** 38 commits: 8 touch strand paths, 11 touch `slice`/`census`/`p2`/`trials`, 2 touch both, 21 touch neither.

## 4. Split mechanics

### Which paths go where

**To the new repository** (working name `rosette`):
- `Rosette/`, `Rosette.lean`, `lakefile.toml`, `lake-manifest.json`, `lean-toolchain`
- `bench/`, `corpora/`, `tools/` (all three tools)
- `out/` except `out/prior_art_vocabulary.md`
- `clausal/schema/maths_fit.py`
- Copies, with history, of `LICENSE`, `.gitignore`, `AGENTS.md`, `DECISIONS.md`, `docs/RESULTS.md`, `docs/EXPERIMENTS.md`, `docs/PLAN.md`, `docs/SETUP.md`, `docs/SCHEMA.md`
- By hand: the ignored PDF `Decompiling Lean Proofs Like Code.pdf` and the untracked `.github/` (it is the root project's CI template)

**Stays in Clausal:**
- `clausal/`, `census/`, `p2/`, `trials/`, `brainstorm/`, `tdflite-ideas/`, `private/`
- `docs/` and `README.md`
- `clausal/schema/refinement-graph.v2.schema.json`, `clausal/schema/selftest.py`
- `clausal/schema/maths-example.graph.json` as a frozen fixture
- `clausal/review/schema/` as review evidence
- `out/prior_art_vocabulary.md`, moved to `docs/` first with its three citations updated

**Naming caution:** do not reuse the GitHub name `lean-rosette` for the new repository. Once X5 renames it to `clausal`, a new repository under the old name would break GitHub's redirect.

### Steps (not run; I did not check that `git filter-repo` is installed)

1. In the Clausal repo, commit `git mv out/prior_art_vocabulary.md docs/` with the citation updates.
2. Make a fresh clone and filter it. Both old and new names are needed for the schema script's history:
   ```sh
   git clone https://github.com/willackerly/lean-rosette.git ../rosette && cd ../rosette
   git filter-repo \
     --path Rosette --path Rosette.lean --path lakefile.toml --path lake-manifest.json --path lean-toolchain \
     --path bench --path corpora --path tools --path out \
     --path slice/schema/maths_fit.py --path clausal/schema/maths_fit.py \
     --path LICENSE --path .gitignore --path AGENTS.md --path DECISIONS.md \
     --path docs/RESULTS.md --path docs/EXPERIMENTS.md --path docs/PLAN.md --path docs/SETUP.md --path docs/SCHEMA.md
   ```
   Then move `maths_fit.py` to `schema/maths_fit.py`, remove the Clausal rows and sections from the copied docs, and trim `.gitignore` to the strand's lines.
3. Carry the ignored data across by moving directories on this machine. A clone alone loses it. For each of `corpora`, `out`, `tools`, `.lake`:
   ```sh
   rm -rf ../rosette/<dir> && mv <dir> ../rosette/<dir>
   ```
   Then `git -C ../rosette status` must be clean. `mv` is instant on the same volume.
4. In the Clausal repo, make one ordinary commit: `git rm -r Rosette Rosette.lean lakefile.toml lake-manifest.json lean-toolchain bench corpora tools out clausal/schema/maths_fit.py`, plus the doc edits below.
5. Do not rewrite Clausal's history. It is pushed, and leaving it means nothing is lost; the cost is that its `.git` keeps the 148 MB of `out/` blobs.

### How the two repositories keep track of each other

- **READMEs.** Each gets a "Companion repository" section with the other's URL, one paragraph on what it holds, and the two joint nodes (M6, X1b) by name. Clausal's `README.md:149` becomes that section.
- **Clausal `AGENTS.md`.**
  - Line 5 becomes "the Lean project is `clausal/lean`; there is no root Lake project".
  - Line 10 becomes "before proposing a proof-structure scoring or navigation idea, read the companion's `out/FINDINGS.md`".
  - Add: "a change to `clausal/schema/refinement-graph.v2.schema.json` must still validate `clausal/schema/maths-example.graph.json`, and must be recorded in the companion's `schema/SOURCE`".
- **Rosette `AGENTS.md`.**
  - Keep the Lean, negative-results and scoring rules.
  - Add: "the evidence-graph schema is owned by the Clausal repository; never edit the vendored copy".
  - Add: "M6 and X1b are joint nodes; update both `TODO.md` files when either moves".
- **Schema.**
  - The Clausal file is canonical.
  - Rosette vendors it at `schema/refinement-graph.v2.schema.json`, with `schema/SOURCE` recording the Clausal commit and the file's sha256.
  - `schema/check_sync.sh` compares that sha256 with `../clausal/clausal/schema/refinement-graph.v2.schema.json` when the sibling checkout exists, and exits non-zero on mismatch.
  - `maths_fit.py` takes the linter from the sibling checkout (`PYTHONPATH=../clausal/clausal`), since `graphlint.py` is compiler code.
  - Clausal's `selftest.py` should also validate the frozen `maths-example.graph.json`, so a schema change cannot silently drop the mathematics case. I did not check whether it does so today.
- **`docs/RESULTS.md`.**
  - Each repository keeps its own rows.
  - Each ends with a "Companion results" section of three or four headline rows linking to the other's file at a pinned commit.
  - For Clausal, those rows are: scoring ideas failed, the dead-code tool works on three projects, families paid once.
- **`docs/EXPERIMENTS.md`.** Keep the existing numbers in both, with gaps and a note. `DECISIONS.md` and the plans cite experiments by number.
- **`DECISIONS.md`.** Both keep the full log to the split point, and each appends one entry recording the split (what, why, how to undo: `git revert` in Clausal, `mv` the directories back).
- **Plans and TODOs.** M nodes move to Rosette's plan. Clausal's `docs/PLAN.md` keeps one row for M6 and X1b, and both `TODO.md` files list them under "Joint with companion".

## 5. What could be lost in a split

- **Reviewer evidence that no script regenerates.** These are git-ignored and exist only on this machine: `tools/reinvent/review/` (1.0 GB), `tools/deadcode/review/` (141 MB, cited by `out/deadcode/M8.md:3`), `out/corpus/review_*/`, `out/families/review/`, `out/review_claims-vs-evidence/reuse_*`. They survive only if moved as in step 3.
- **Absolute paths.** 30 tracked strand files contain `/Users/will/dev/lean-rosette`: 12 under `corpora/families`, 12 under `out/families`, and others under `corpora/ns_export`, `out/corpus`, `out/deadcode`, `out/demo`. I did not classify which are scripts and which are logs.
- **Moved builds.** Whether the Lake builds under `corpora/*/.lake` and the dead-code working copies stay valid after `mv` was not tested. Worst case is a rebuild at the costs in section 6.
- **Citations.** Every `out/...` path in Clausal's `docs/RESULTS.md`, `docs/EXPERIMENTS.md`, `docs/ARCHITECTURE.md`, `docs/HANDOFF.md` and `AGENTS.md` breaks unless rewritten to companion links.
- **The schema example.** `maths_fit.py` can no longer run from inside Clausal, so the example becomes a frozen fixture.
- **The stated condition.** The only planned contact points (M6, X1b) are deferred and untested. Without the joint-node rows, the split makes "forgetting" the default.

## 6. Disk that can be reclaimed today without a split

Nothing here was run. Timings are the repository's own figures where cited, and "not measured" otherwise.

### Mathematics strand, regenerable

| Path | Size | Cost to regenerate |
|---|---|---|
| `corpora/ns_trim/m8` | 15 GB | About 3 h of builds with four restarts (`out/deadcode/M8.md:191`). The unmeasured clean-timing item (`out/deadcode/M8.md:270`) needs this copy |
| `corpora/ns_trim/work` | 8.1 GB | Recipe at `out/corpus/deadcode/DEADCODE.md:300`; a clean ns build of the roots was 4,607 s (`out/deadcode/M8.md:192`) |
| `corpora/carleson_trim`, `corpora/pfr_trim` | 908 MB, 494 MB | Whole runs: 12 min and 28 min (`out/deadcode/M8.md:191`) |
| `corpora/ns/.lake` | 16 GB | `lake exe cache get && lake build`, 18 min (`docs/SETUP.md`) |
| `corpora/pfr/.lake`, `corpora/carleson/.lake` | 7.4 GB, 7.5 GB | About 1 min and 2.5 min after the cache download |
| `.lake` (root) | 7.3 GB | `lake exe cache get && lake build Rosette`, 1 min after cache; the build rewrites files under `out/` (`docs/SETUP.md`) |
| `corpora/friction/build` | 1.6 GB | Not measured |
| `tools/reinvent/build`, `tools/families/build` | 537 MB, 529 MB | Not measured |
| `corpora/outline2/build`, `corpora/ns_export/export`, `corpora/ns_reuse/stmtkeys` | 172 MB, 171 MB, 171 MB | Not measured |

- **Lowest-risk set, 9.5 GB:** `rm -rf corpora/ns_trim/work corpora/carleson_trim corpora/pfr_trim`
- **Next, 15 GB, if the clean-timing measurement is dropped or accepted as a 3 h rerun:** `rm -rf corpora/ns_trim/m8`
- **About 31 GB, only while the strand is idle:** `rm -rf corpora/ns/.lake corpora/pfr/.lake corpora/carleson/.lake`. Every exporter and all three tools read these builds, and M10 and M11 need them.
- **Do not delete:** the review directories in section 5, `corpora/{ns,pfr,carleson}/.git`, and the ignored `out/**/*.jsonl` inputs unless the matching `out/corpus/*/README.md` recipe has been checked first.

### Outside the strand, where most of the space is

| Path | Size |
|---|---|
| `census/fork/lean` (eight Lake trees of about 7.2 GB each) | 58 GB |
| `census/fork/runs` | 15 GB |
| `p2/score` | 11 GB |
| `census/work` | 8.2 GB |
| `census/lean-pinned` | 7.2 GB |
| `clausal/evidence` | 2.6 GB |

I did not check regeneration costs or commands for any of these. R1 needs the patched translator (`census/fork/aeneas`, `census/fork/bin`, `census/fork/.opam`), so those must stay.

## 7. Not checked

- No build, no `lake` command, and no test that a moved Lake project still builds.
- `git filter-repo` availability and a dry run of the filter.
- The contents of `tools/deadcode/lean/*.lean`, `clausal/schema/selftest.py`, `DECISIONS.md` entries and `brainstorm/`.
- `private/` beyond toolchain files, one lakefile's key names and a grep for strand references.
- Whether another agent's rename leaves `maths_fit.py` and `clausal/clausal/graphlint.py` with stale `slicegen` references in the final commit.
- Packed size of `.git` after `git gc`.
- Whether the tracked 148 MB under `out/` contains files that should have been ignored (for example `out/review_benchmark-validity/rows.pkl`).