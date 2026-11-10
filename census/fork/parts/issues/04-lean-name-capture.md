Title: Lean: `Slice` resolves to a user type named `Slice`; a parameter named like a module captures `module.Type.method`

Two cases where Aeneas reports success and the generated Lean does not elaborate.

(a) A user type whose last name component is the name of a builtin type:

```rust
pub mod names {
    pub struct Slice<'a> { pub bytes: &'a [u8] }
    impl<'a> Slice<'a> { pub fn len(&self) -> usize { self.bytes.len() } }
}
```

```lean
structure names.Slice where
  bytes : Slice Std.U8            -- `Slice` is the structure being declared
def names.Slice.len (self : names.Slice) : Result Std.Usize := do
  ok (Slice.len self.bytes)       -- `Slice.len` is this very function
```

```
error: Function expected at
  Slice
but this term has type
  Sort ?u.2
```

Builtin types and the functions in their namespace are printed by short name (`ExtractBase.builtin_adts`: `Slice`, `Array`, `Str`, `Result`, …; `Slice.len`, `Array.index_usize`, …) and resolved through `open Aeneas.Std`. A declaration `X.Slice` wins over the opened name in every definition whose name starts with `X.`. In `indexmap` (`map::slice::Slice`, `set::slice::Slice`) this makes two structure declarations fail and 80 functions compile only "using sorry". The comment above `builtin_adts` already mentions the hazard for `Error`.

(b) A parameter named like a module of the crate:

```rust
pub mod input { pub struct Input { pub value: u32 } impl Input { pub fn get(&self) -> u32 { self.value } } }
pub mod shadow { use crate::input; pub fn param_like_module(input: input::Input) -> u32 { input.get() } }
```

```lean
def shadow.param_like_module (input : input.Input) : Result Std.U32 := do
  input.Input.get input           -- parsed as a field access on the parameter `input`
```

```
error: Invalid field `Input`: The environment does not contain `capture_module_name.input.Input.Input` ...
```

`ExtractBase.basename_to_unique` checks a local name against full declaration names only. `untrusted` (module `input`, parameters `input`) loses 9 functions to this, `time` 7, `rust_decimal` 4.

Proposed fix (patch 0004):

- (a) collect the last name component of the crate's own type and trait declarations; a builtin type or builtin function whose first name component is in that set is printed fully qualified (`Aeneas.Std.Slice`, `Aeneas.Std.Slice.len`). Crates without such a declaration get byte-identical output (the extraction tests, `make extract-tests`, do not change). Only local declarations are considered: `core::result::Result` is in almost every crate and would otherwise qualify every `Result`. The same capture can in principle happen for definitions that Aeneas emits inside the `core.result.` namespace; I did not look for a case.
- (b) keep the set of first components of all registered dotted names (`names_maps.name_heads`) and make `basename_to_unique` treat those as collisions too (Lean only), so the parameter becomes `input1`.

In the ten-crate census this takes `indexmap` from 378 to {{INDEXMAP_P4}} of 630 functions that end as compiling Lean, `untrusted` from 11 to 20 of 26, `time` from 696 to 703 of 774 and `rust_decimal` from 213 to 217 of 242 (parameters named `str` next to the module `str`). Two single-file reproductions are given in full below (`capture_builtin_name.rs`, `capture_module_name.rs`). A check that would catch this class in CI: run `lake build` on the generated Lean of a few real crates, since Aeneas itself reports no error here.

{{REPRO:capture_builtin_name.rs}}
{{REPRO:capture_module_name.rs}}
{{PATCH:0004}}
