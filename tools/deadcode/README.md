# deadcode: what a Lean 4 project does not need for its root declarations

Plan node M8. Input: a **built** Lean 4 project and a set of root declarations. Output: the declarations,
modules and cloned modules that the roots do not need, in classes that are safe to delete to different
degrees, and (optionally) a trimmed copy in which the deletions were confirmed by the build.

The tool was written and changed while it was being run on three projects (rules were added after earlier
runs; see `out/deadcode/M8.md`). Read its results as exploratory, not as a frozen procedure.

The tool never edits or rebuilds the project it inspects. It reads the build output with the project's own
toolchain and does all deletions in a copy.

```
tools/deadcode/
  deadcode.py          driver (Python 3, standard library only)
  lean/Export.lean     everything about declarations, read from the built environment (imports only `Lean`)
  lean/Axioms.lean     axioms of the roots (same edges as Lean's `collectAxioms`, one walk for all roots)
  lean/Closure.lean    the kernel's own dependency closure of the roots, to check the graph of Export.lean
  summary.py           several projects side by side (out/deadcode/COMPARE.md)
  projects/*.json      one file per project: ns, pfr, carleson
```

## Use

```sh
export PATH="$HOME/.elan/bin:$PATH"
D=tools/deadcode/deadcode.py; P=tools/deadcode/projects/pfr.json
python3 $D $P export                       # read the build with Lean          -> out/deadcode/<name>/export/
python3 $D $P analyze                      # classes 1-4                       -> analysis.json, unreachable.jsonl, modules.json, clones.json
python3 $D $P check                        # folded graph == kernel closure?   -> graph_check.json
python3 $D $P control -n 20                # negative control                  -> runs/control/result.json
python3 $D $P safe-delete --set term --confirm            # delete, rebuild, trace failures, restore
python3 $D $P safe-delete --set dead --sample 300         # a seeded sample instead of the whole set
python3 $D $P build-all --run term         # default + extra targets in the copy of a finished run -> other_targets.json
python3 $D $P verify --run term            # re-export the trimmed build, compare with the prediction
python3 $D $P timing --run term            # clean builds of the roots, original and trimmed copy, started together
python3 $D $P report                       # REPORT.md from the JSON files
python3 tools/deadcode/summary.py tools/deadcode/projects/ns.json@held tools/deadcode/projects/pfr.json
```

`safe-delete --set`:

| set | what is deleted | what it measures |
|---|---|---|
| `dead` | class 1 | should build first time |
| `held` | class 1 and class 2-attribute | which table entries (simp, instance, ...) are really needed |
| `term` | every unreachable declaration that can be cut | how wrong the term graph is on its own |

Other options: `--sample N --seed S` (seeded sample of the set, plus the unreachable declarations that use the
sampled ones), `--confirm` (re-delete every restored declaration alone and rebuild the module it was blamed for;
a build that passes withdraws the attribution), `--fallback-after K` (after K rounds stop resolving and put
back, as *unresolved*, every table-carrying declaration a failing module can see), `--roots-only` (build only
the root modules; without it the project's default targets and the `extraTargets` of the project file are
built as well and what they need is restored), `--fresh` (recreate the working copy), `--trace-jobs`, `--no-trace`,
`--no-bisect` (for large projects: one bisection step can rebuild much of the project), `--resume` (continue an
interrupted run from its `rounds.json` and working copy), `--copy NAME --clone-from OTHER --keep-from RUN`
(a second run in its own copy, started from the build and the restorations of an earlier run).

## Project file

```json
{ "name": "pfr",
  "project": "corpora/pfr",                    // built project, relative to the repository root
  "prefixes": ["PFR", "PFRPalomar"],           // top-level module names that belong to the project
  "roots": {"blueprint": "out/corpus/pfr/blueprint.json"},
  "groups": [["^PFR\\.ForMathlib\\.", "staging"]], "defaultGroup": "main development",
  "extraTargets": [],                          // Lake targets that are not default targets but must keep building
  "excludeModules": [], "srcDir": ".", "seed": 20261110, "shards": 8 }
```

Roots, one of:

- `{"names": [...]}`: declaration names;
- `{"file": "roots.txt"}`: one name per line;
- `{"blueprint": "blueprint.json"}`: every name in a `\lean{}` tag of a blueprint (list of nodes with a `lean`
  field, as written by `corpora/tools/parse_blueprint.py`);
- `{"modules": [...], "kinds": ["theorem"]}`: every non-private declaration of those kinds in the named modules.

A root that is not a project declaration (a Mathlib name in a blueprint) is listed and ignored.
`groups` only label the report (first matching regular expression on the module name).
Modules that cannot be imported into one environment with the rest (the `ComparatorChallenges` files of `ns`
re-declare project names) must be left out of `prefixes` or listed in `excludeModules`.

**Names declared twice.** Lean 4.36 does not always refuse to import two modules that declare the same name:
it keeps one constant and drops the other without a message. `export` therefore reads every project module's
own `.olean` again and writes `clashes.json`; a source-level declaration that was dropped is printed as a
warning and listed in `analysis.json` and `REPORT.md`. Such a declaration is in no count. Its module is never
deleted, its text is never cut, and the names its text uses are held (class 2-command). Found: the six public
theorems of `PFRPalomar/Solution.lean` in `pfr` (same names as in `PFRPalomar/Challenge.lean`) and two anonymous
`local instance : Fact (0 < 2 * π)` in `carleson`; none in `ns`. To have such declarations analysed, leave the
other module out with `excludeModules`.

## What is read, and from where

Declarations, dependencies and tables come from Lean; source text is cut at ranges Lean reports. Five
exceptions, where text or a hand-written list decides something:

1. `BENIGN_ATTRS`: a hand-written list of 31 attribute names that do not hold a declaration back.
2. Commands outside declaration ranges are recognised by their first word (`BENIGN_CMD`). This decides whether
   a file with no declaration left may be deleted.
3. A declaration's range is extended upward over `… in` lines by reading the text.
4. `Export.lean` tells auto-generated constants from declarations partly by name (`eq_…`, a leading `_`,
   `match_`, `proof_`). `check` tests the result against the kernel's closure.
5. A build failure that the error message and Lean's traces do not explain is matched against identifiers in
   the error text, then on the failing source line.

| fact | source |
|---|---|
| declarations, kinds, modules | the built environment (`importModules` on the project's `.olean` files) |
| term dependencies | constants in each declaration's type and value; auto-generated constants (constructors, projections, recursors, equation lemmas, `_proof_N`, `match_N`, ...) are folded into the declaration they belong to. `check` compares the result with the kernel's unfolded closure: the two agree exactly on all three projects |
| where a declaration is in the source | Lean's declaration ranges |
| simp sets | every registered simp extension (`simpExtensionMapRef`): `simp`, `push_cast`, `field_simps`, ... |
| instances | the instance table, plus the `instance` keyword read by Lean's `declModifiers` parser (a `local instance` is not in the table of an importing file) |
| reducibility | the reducibility table (`abbrev`, `@[reducible]`) |
| `@[ext]` | the `ext` theorem table |
| notation targets | `app_unexpander` attribute; names quoted inside compiled notation / macro / elaborator bodies (`Name` literals in the term of the auto-generated constant) |
| any other attribute | Lean's own parser run on the head of the declaration range; an attribute that is not on a short list of attributes without effect on other declarations (`BENIGN_ATTRS` in the driver) holds the declaration |
| names used without a term trace | the reference index Lean writes next to every `.olean` (`.ilean`): every resolved name with its position. Inside a declaration it gives "the source of A names B"; outside every declaration it gives the names used by commands (`variable`, `open … (x)`, `export`, `attribute […] x`, `deriving instance`, `alias`) |
| names declared in two project modules | each module's own `.olean` (`readModuleData`) against the module the combined environment gives for the name (`clashes.json`) |
| footprint of all environment extensions | `extensions.json`: entries per persistent extension contributed by project modules (shows tables the tool does not decode) |

## Classes

Let R be the term-dependency closure of the roots. Unreachable = not in R.

| class | meaning | how established | expected safety |
|---|---|---|---|
| `2-named` | named in the source of a declaration that stays, absent from its term | `.ilean` reference with a kept enclosing declaration (closure over term + source references) | deleting it is predicted to break the build |
| `2-command` | named by a command, notation or macro of a file that stays; or its source range overlaps a declaration that stays (`to_additive` pairs, `simps` output); or needed by one of these | `.ilean` reference outside every declaration; `Name` literals and constants of orphan auto-generated constants; declaration ranges | not deletable without editing the command |
| `2-attribute` | in an elaboration table (simp, instance, reducible, ext, other attribute) **and** something that stays is elaborated after it (later in its file, or in a file that imports its file); or needed by one of these | tables and parser as above; import graph from `.ilean` | usually deletable; only the build can say (`safe-delete --set held`) |
| `1-dead` | everything else unreachable | none of the above applies | deletable; confirmed as a set by `safe-delete --set dead` |
| 3 | whole modules: every declaration unreachable | same graph; `modules.json` | file can be skipped. It is deleted when all its declarations go, unless it has, outside Lean's declaration ranges, a command that can act on other files (`attribute [simp] X`, `notation`, `macro`, `export`, ...) and something that stays imports it; then the file stays with its declarations removed |
| 4 | cloned modules | declarations with the same statement shape (hash of the Lean type, binder names ignored, project constants reduced to their last name component; declaration names not compared) in another module, plus a text ratio. `near-identical`: text ratio ≥ 0.6. `same-statements`: ≥ 80% of the smaller module has a shape twin | a report, not a deletion class: whether a clone is unused is given by its unreachable count |

`analyze --no-scope` drops the "elaborated after it" condition (every table entry is held).

## Safe delete

1. **Copy.** Sources are copied, `.lake/packages` is symlinked, `.lake/build` is cloned copy-on-write
   (`corpora/<name>_trim/m8/{work,pristine,control}`). `lake build --no-build` must report the copy up to date
   before anything is edited, so Lake never rebuilds a dependency.
2. **Delete.** Each declaration is cut at Lean's declaration range (extended upward over `open … in`,
   `omit … in`, `set_option … in` prefixes). A module with no declaration left is deleted and `import M` is
   replaced by M's own imports. `open X` of a namespace that only deleted declarations kept alive is trimmed.
   Declarations whose range overlaps one that stays are not cut.
3. **Build** the modules of the roots. Lake rebuilds only what changed. When they build, **build the rest**:
   Lake's default targets and the project file's `extraTargets` (for example comparator `Challenge` /
   `Solution` libraries). A failure there is traced like any other, but what is restored is recorded
   separately (`neededByOtherTargets`): it is used by a build target outside the roots, it is not a hidden
   dependency of the roots. A deleted file that the Lake configuration names as a target comes back whole.
   With `--roots-only` this step is skipped and such targets can be left broken.
4. **Trace failures back**, per failing module, in this order:
   - the error names a deleted declaration (`Unknown identifier`, `Invalid field`, ...). An unknown identifier
     that is the name of a declaration *kept* earlier in the same file is a cascade and is skipped;
   - Lean's own traces: the **original** file is elaborated once in the untouched copy with
     `trace.Meta.Tactic.simp.rewrite` and `trace.Meta.synthInstance` on; simp lemmas and instances used inside
     the failing declarations that are in the deleted set are the culprits;
   - an identifier in the first messages equals a deleted name;
   - bisection: rebuild the failing module with halves of the candidate set restored.

   For a failing file that is not among the analysed modules (a target the original project had not built)
   only the first tier is used.
5. **Restore** the culprits (*hidden dependencies*) and everything they depend on, and repeat from 3 until
   the roots and the other targets build.
6. **Check**: `Axioms.lean` on the trimmed build must give, for every root, the axioms of the original build.
   `verify` re-exports the trimmed build and compares names, reachable set and term dependencies with the
   prediction.

The **negative control** (`control`) deletes, one at a time, declarations drawn uniformly from the *reachable*
ones that have a user, rebuilds the nearest module that uses each, and expects a failure.

## Version tolerance

The Lean files import only `Lean` and are run with `lean --run` under the inspected project's own toolchain
(`lean-toolchain`), with `LEAN_PATH` set to its build output; no Lake call, no package of their own, nothing
written into the project. Run on Lean 4.34.0-rc2 (`ns`), 4.36.0-rc2 (`pfr`) and 4.36.0-rc1 (`carleson`, which
uses the module system) without changes to those projects.

## Limits

- A declaration that Lean's `isInternalDetail` takes for auto-generated and that has no parent is not a
  source-level declaration for the tool (it is never deleted, and its uses are folded into its users).
- The trace step attributes a failure to every deleted simp lemma or instance that the original elaboration
  of the failing declarations used; one of them may not be necessary. `--confirm` tests each one. Traces print
  names as the file's open namespaces abbreviate them; a printed name that also fits a declaration that stays
  is not attributed, and only declarations with a table entry or a source reference are candidates.
- Commands outside declarations (`attribute`, `notation`, `export`, ...) are recognised by their first word
  in the text outside Lean's declaration ranges (`BENIGN_CMD` lists the ones without outward effect).
- Deleting an anonymous instance renumbers the later anonymous instances of the file (`inst…_3`); `verify`
  compares names with and without that number.
- Declarations restored because a hidden dependency needs them are not tested separately.
- The scope rule assumes a table entry only matters to code elaborated after it in the import order. Lean has
  no other channel, but an attribute whose handler writes to a file or a global reference would escape it.
- `lake build` of a copy is used for every check, and the trace step runs `lake lean <file>` once per failing
  module inside the restore loop. That is a cold start inside a loop, which AGENTS.md rule 1 is written
  against; it is used because the object under test is each project's own build under its own toolchain
  (three toolchains here), which the warm bridge does not serve.
- The roots decide what is deleted. A project's other deliverables (comparator files, examples) survive only
  because the other targets are built too; a file that no target builds is not protected.
- Build times are whatever the machine gave; module-seconds are the sum of Lake's per-module times.
