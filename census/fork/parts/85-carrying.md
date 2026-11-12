## Carrying the fork

The fork is five patch files on top of one upstream commit. Nothing else needs to be kept.

**What was installed on this machine, and how to undo it.**

| what | where | undo |
|:--|:--|:--|
| `opam` 2.6.1 and `pkgconf` 3.0.10, by `brew install opam pkgconf`. Homebrew also installed `json-c`, `popt`, `xxhash` and `rsync` as dependencies of opam and upgraded `libunistring` (1.4.2 to 1.5) and `lz4` (1.10.0 to 1.11.0) | `/opt/homebrew` | `brew uninstall opam pkgconf && brew autoremove`. The two upgrades stay |
| opam root: OCaml 5.3.0 (switch `aeneas`) and the 43 packages Aeneas and charon-ml need, 663 MB | `census/fork/.opam`, git-ignored. Nothing in `~/.opam`; no shell profile mentions opam; `env.sh` sets `OPAMROOT` for one shell | `rm -rf census/fork/.opam` |
| clone of Aeneas with branch `census-fork`, its Charon clone at the pin, build output, six test worktrees | `census/fork/aeneas`, `census/fork/tests-wt`, git-ignored, 1.8 GB | `rm -rf census/fork/aeneas census/fork/tests-wt` |
| binaries `aeneas-base`, `aeneas-p1` … `aeneas-p5` | `census/fork/bin`, git-ignored, 213 MB | `rm -rf census/fork/bin` |
| run directories, private Lake projects (copy-on-write clones of the census's packages), a copy of the Aeneas Lean library | `census/fork/runs` (15 GB), `lean` (58 GB apparent size), `backends-pinned`, `work`, `logs`, git-ignored | `rm -rf` each; all regenerable with the scripts |

Already present and used, not installed here: Homebrew, `gmp`, `coreutils` (for `timeout`), rustup with `nightly-2026-09-17`, elan.

**Rebuild the patched binary from nothing.** The last two steps were re-checked in this pass: the five patch files apply with `git am` to `0d21a9ec` and to `5a392f4b` and give the tree of branch `census-fork`, and `bin/aeneas-p5` is byte-identical to that tree's build output. The opam steps are reconstructed from `logs/opam-*.log` and Aeneas's README and were not executed a second time.

```
brew install opam pkgconf
cd census/fork
git clone https://github.com/AeneasVerif/aeneas.git aeneas
git -C aeneas checkout -b census-fork 0d21a9ec
git -C aeneas am "$PWD"/patches/000*.patch

export OPAMROOT="$PWD/.opam"
opam init --bare --no-setup -y
opam switch create aeneas ocaml-base-compiler.5.3.0 -y
source env.sh

git clone https://github.com/AeneasVerif/charon.git aeneas/charon
git -C aeneas/charon checkout "$(tail -1 aeneas/charon-pin)"      # 454586e9
opam install -y --deps-only aeneas/charon/charon-ml aeneas/src   # about ten minutes
(cd aeneas/charon && make build)                                  # Charon and charon-ml; needs the pinned Rust nightly
(cd aeneas && make build-bin-dir)                                 # 40 s; needs the charon/ directory above
mkdir -p bin && cp aeneas/src/_build/default/main.exe bin/aeneas-p5
bin/aeneas-p5 -version
```

After a change to the patches, only `git am`, `make build-bin-dir` and the `cp` are needed. The binary links Homebrew's `gmp` dynamically, so it runs on this machine and not on one without it.

**Pointing `clausal/translate.sh` at it.** Not done and not tested here: `clausal/` belongs to other work and was not touched. The script has no override; it runs `clausal/.tools/aeneas-nightly-2026.11.09-5a392f4/aeneas`. Two ways, for the owner of `clausal/`:

- **Without editing the script:** swap the binary in the downloaded tool directory (git-ignored). The script only tests that the file is executable, and it keeps using the release's Charon, Lean library and Rust pin.

  ```
  T=clausal/.tools/aeneas-nightly-2026.11.09-5a392f4
  mv $T/aeneas $T/aeneas.release
  cp census/fork/bin/aeneas-p5 $T/aeneas
  # undo:  mv $T/aeneas.release $T/aeneas
  ```

  `bin/aeneas-p5` is built on `0d21a9ec`, one commit after the release `clausal/` pins (`5a392f4b`); the only source difference is three Lean keywords. For an exact match build the patches on `5a392f4b` instead (they apply). `translate.sh` passes `-warnings-as-errors`, and patch (ii) reports a dropped trait method as a warning, so a crate that needs the patch will stop there by design of the script.
- **Cleaner, a two-line change to `translate.sh`:** let an environment variable such as `AENEAS_BIN` replace `$TOOLS/aeneas` in the one line that calls it, and record the variable in `translation.json`.

**Which commit to drop when upstream fixes a defect.** Check with the unpatched release binary and the reproduction: when the unpatched binary gives the "patched" result below, the commit is no longer needed.

| commit (branch `census-fork`) | patch file | issue text | drop when the unpatched release gives |
|:--|:--|:--|:--|
| `5397cc33` | `0001` | `upstream/01-…` | `repro/mixed_group.rs`: `unrelated_b`, `Wrapper.get` and `unrelated_c` are in the Lean file |
| `6f8a82a1` | `0002` | `upstream/02-…` | `repro/abort_copied.rs` and `abort_pattern.rs`: a Lean file is written and `add_one` is in it |
| `1541e6d5` | `0003` | `upstream/03-…` | `repro/crash_stack_of_refs.rs`: a Lean file is written and `add_one` is in it |
| `81c0b10c` | `0004` | `upstream/04-…` | `repro/capture_builtin_name.rs` and `capture_module_name.rs`: the Lean file builds |
| `f638402a` | `0005` | `upstream/05-…` | no single-file check; on `time`, declarations in the generated file are no longer indented |

- **Order matters for two of them.** `0003` is written on top of `0002` (both edit `Translate.ml`) and `0005` on top of `0003` (it edits the handler `0003` rewrote). Dropping `0002` or `0003` alone means a `git rebase` of the later ones; for `0005` that is three lines to re-place in whatever handler upstream ends up with.
- **At each new pin:** `git am` the remaining patches on the new commit, run `repro/run.sh`, `scripts/run_tests.sh` and `scripts/run_variant.sh <variant> shipped`, and compare with `data/summary.json`. If `git am` fails, upstream has touched the same lines: read their change before rebasing, it may be the fix.
- **Upstream formatting.** The patches were not run through `ocamlformat`, which upstream's CI enforces; do that before sending a pull request.
