# The five patches

`git am`-ready, in order, on top of Aeneas `0d21a9ec` (nightly-2026.11.10); they also apply to `5a392f4b` (nightly-2026.11.09). 334 lines added, 53 removed, 9 source files and 2 expected-output files. Each file starts with its commit message. The first four were asked for; the fifth was found while running cedar.

```
git -C aeneas checkout -b census-fork 0d21a9ec && git -C aeneas am "$PWD"/patches/000*.patch
```

| file | in plain words | reproduction | issue text |
|:--|:--|:--|:--|
| `0001-FunsAnalysis-…` | Aeneas analyses functions group by group. On a group that mixes functions with trait impls it logged an error and **stopped**, so every function after that group failed. The patch makes it carry on with the next group. One recursive call. | `repro/mixed_group.rs` | `upstream/01-…` |
| `0002-Translate-a-trait-method-signature-…` | If the signature of one trait method could not be translated (for example `Iterator::copied`, or anything using `str::find`), Aeneas **aborted the whole crate** with no output. The patch drops that one method with a warning and keeps going; functions that need it fail one by one. | `repro/abort_copied.rs`, `repro/abort_pattern.rs` | `upstream/02-…` |
| `0003-Catch-non-CFailure-exceptions-…` | Aeneas catches its own error type per function, but other OCaml exceptions (`Failure`, `Not_found`) escaped and **ended the run without naming the function**. The patch catches them in five places and reports them against the function, which becomes `sorry` or an `axiom`. | `repro/crash_stack_of_refs.rs` | `upstream/03-…` |
| `0004-Lean-backend-avoid-two-kinds-of-name-capture` | Two cases where the generated Lean **means something else than intended**: a user type called `Slice` hides the library's `Slice`, and a parameter called `input` hides the module `input`. The patch prints the library name in full in the first case and renames the parameter in the second. | `repro/capture_builtin_name.rs`, `repro/capture_module_name.rs` | `upstream/04-…` |
| `0005-Extraction-reset-the-formatter-…` | After an error while printing one definition, the pretty-printer was left half-open, so **every later definition was printed indented**, and far enough to the right Lean can no longer parse the file. The patch resets the printer after an error. Extra, not in the original task. | none; seen on `time` and cedar | `upstream/05-…` |

What each one does and does not do, with measurements, is in `../FORK.md` ("The patches"). `0003` is written on top of `0002`, and `0005` on top of `0003`.
