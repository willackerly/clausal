# census/ — which real Rust reaches Lean today (plan node K3)

Ten pinned crates run through Charon → Aeneas → `lake build`, judged per function.

| Read | For |
|:--|:--|
| [`CENSUS.md`](CENSUS.md) | the numbers, the method, the failure causes, the side columns (newer Aeneas, hax), the rewrite-cost experiment |
| [`PROFILE.md`](PROFILE.md) | the supported Rust profile: what to write, what to avoid, with a before/after for each rule |
| [`IMPROVEMENTS.md`](IMPROVEMENTS.md) | tool improvements ranked by what they would unlock, with source locations in Charon and Aeneas |

All three are generated from `data/` by `scripts/tables.py`; edit the templates in `scripts/`, not the `.md` files here.

## Layout

    rerun.sh                      setup | census | probes | side | rewrites | tables | all
    scripts/select_corpus.py      corpus rule and seed (run before any translation)
    scripts/census.py             the driver: inventory, Charon, Aeneas (with the peel), lake build, per-function join
    scripts/report.py             cause classes, aggregates  -> data/summary.json, data/functions.jsonl
    scripts/tables.py             tables + templates         -> CENSUS.md, PROFILE.md, IMPROVEMENTS.md
    scripts/compare_new.py        newer Aeneas on the same LLBC
    scripts/run_hax.sh            hax 0.5.0, crate level
    scripts/std_models.py         what the Aeneas Lean library models
    tools/fninv/                  syn-based function inventory (the denominator)
    probes/profile-probes-0.1.0/  tiny before/after functions behind PROFILE.md
    probes/mixed-group-probe-0.1.0/ and mixed-group-fixed-probe-0.1.0/   100-line reproduction of cedar's dominant failure, and its rewrite
    rewrites/                     patches for the rewrite-cost experiment, and its runner
    lean-pinned/                  Lake project that compiles the generated Lean (Aeneas library and Mathlib cloned from ../slice)
    data/selection/               crates.io snapshot, exclusions, draw, pins (versions + sha256)
    data/results/<crate>.json     one record per function: stages, messages, dependencies, features
    data/                         summary.json, functions.jsonl, hax.json, newer_aeneas.json, rewrites.json, probes.json, std_models.json
    data/overrides.json           per-crate extra Charon arguments (cedar: the two generated parsers opaque)
    data/crash_cache/             function bodies found by bisection to crash Aeneas (cedar), so a rerun need not search again
    data/flags/, data/rewrites/   results of the side runs (extra Aeneas flag; patched crates and probe crates)

Not in git (see `.gitignore`): `crates/` (the unpacked crates), `.tools/`, `upstream/` (Charon and Aeneas sources, read-only), `work/` (logs, LLBC files, build output), `lean-pinned/.lake`, `lean-pinned/Generated/`.

## Run

    ../slice/translate.sh --setup     # once: the pinned Charon/Aeneas and Rust nightly
    ./rerun.sh setup                  # fetch crates (sha256-checked), build fninv, clone the Lean packages from ../slice
    ./rerun.sh census                 # about 20 minutes on an idle machine, half of it cedar-policy-core (needs ~20 GB of memory)
    ./rerun.sh probes && ./rerun.sh side && ./rerun.sh rewrites && ./rerun.sh tables

One crate: `python3 scripts/census.py run semver-1.0.28`. Re-join without re-running the tools: `python3 scripts/census.py rejoin semver-1.0.28`.
