Title: A `CFailure` in `translate_method_sig` (trait method signatures) is not caught: `Iterator::copied`, `str::find` abort the crate

Any crate that calls `Iterator::copied`, `Iterator::cloned`, `Iterator::try_fold` or one of the `str` search methods built on `core::str::pattern::Pattern` (`find`, `split`, `starts_with`, `strip_prefix`, …) produces no output at all:

```rust
pub fn copied_max(v: &[u32]) -> Option<u32> { v.iter().copied().max() }
pub fn add_one(x: u32) -> u32 { x.wrapping_add(1) }   // unrelated, lost too
```

```
[Error] Internal error, please file an issue
Source: '/rustc/library/core/src/iter/traits/iterator.rs', lines 42:0-42:24
Compiler source: symbolic/SymbolicToPureTypes.ml, line 1005
Fatal error: exception Aeneas.Errors.CFailure(_)
Called from Aeneas__Translate.translate_crate_to_pure.translate_method_sig in file "Translate.ml", lines 405-406
```

and for `pub fn find_colon(s: &str) -> Option<usize> { s.find(':') }`:

```
[Error] Unimplemented
Source: '/rustc/library/core/src/str/pattern.rs', lines 99:0-99:24
Compiler source: symbolic/SymbolicToPureTypes.ml, line 392
Fatal error: exception Aeneas.Errors.CFailure(_)
```

Cause: `translate_crate_to_pure` (`src/Translate.ml`) computes all signatures up front. The loop over function declarations catches `CFailure` and reports "Could not translate the function signature of …"; `translate_method_sig`, a few lines below, has no handler. The two triggers above are the sanity check on `trait_type_constraints` in `translate_fun_sigs` (the methods have `where Self: Iterator<Item = &T>`) and the generic associated type `Pattern::Searcher<'a>`. A local trait with `dyn` in a method signature does the same.

In a census of ten crates from crates.io this was the single most expensive defect: five of the ten (`rust_decimal`, `semver`, `rusty-money`, `indexmap`, `time`) give no output with the release binary; with the handler below the same five give 1,368 functions (of 1,786) that end as Lean that compiles, with no other change.

Proposed fix (patch 0002, about 80 lines):

1. catch `CFailure` in `translate_method_sig`, warn, and remove the method from `trait_methods_to_extract`, so that the trait declaration is translated without it;
2. in `SymbolicToPure.translate_trait_impl`, ignore the impl methods that are no longer extracted for the trait;
3. when the translation of a trait *declaration* fails (already caught today), skip its impls with a located error instead of raising `Not_found` in `Translate.trait_impl_is_builtin` at extraction time — otherwise `Pattern` trades one crate-level abort for another.

Functions that use a removed impl then fail one by one (`Could not find: trait_impl_id …`); a call that resolves to the default implementation of a removed method is emitted as a call to that (opaque) function. The extraction tests (`make extract-tests`) give byte-identical output. Two single-file reproductions are given in full below (`abort_copied.rs`, `abort_pattern.rs`).

{{REPRO:abort_copied.rs}}
{{REPRO:abort_pattern.rs}}
{{PATCH:0002}}
