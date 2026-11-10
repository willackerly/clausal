Title: Uncaught `Failure("ty_regions shouldn't be called on erased or body regions")` (and `Not_found` in micro-passes/extraction) aborts the whole crate

```rust
pub enum V { Leaf(u32), Set(Vec<V>) }

impl V {
    pub fn height(&self) -> usize {
        let mut stack: Vec<(&V, usize)> = vec![(self, 0)];
        let mut max_depth: usize = 0;
        while let Some((val, depth)) = stack.pop() {
            if depth > max_depth { max_depth = depth; }
            match val {
                V::Leaf(_) => {}
                V::Set(vs) => { for v in vs { stack.push((v, depth + 1)); } }
            }
        }
        max_depth
    }
}

pub fn add_one(x: u32) -> u32 { x.wrapping_add(1) }   // unrelated, lost too
```

```
Fatal error: exception Failure("ty_regions shouldn't be called on erased or body regions")
Raised at Aeneas__TypesUtils.ty_regions.add_region in file "llbc/TypesUtils.ml", lines 98-99, characters 8-78
...
Called from Aeneas__TypesUtils.ty_regions in file "llbc/TypesUtils.ml", line 116, characters 2-20
```

No Lean file is written, exit code 2, and the log does not say which function was being translated. On `cedar-policy-core` six function bodies do this; finding them took a bisection over the function bodies (129 Aeneas runs).

There are two separate things here:

- the `ty_regions` failure itself (a stack of references into a recursive type, popped in a `while let`), which I have not analysed;
- the handlers. The per-function handlers in `Translate.translate_function_to_pure` and `Interp.evaluate_function_symbolic` match `CFailure` only; `PureMicroPasses.apply_passes_to_pure_fun_translations` has no per-function handler; `PureMicroPassesAnnots.add_type_annotations` and the per-group handler in `Translate.extract_definitions` match `CFailure` only. Once the first is caught on a large crate, the next crate-level aborts are `Not_found` in `PureTypeCheck.get_adt_field_types` (from `add_type_annotations`) and `Not_found` in `Extract.extract_field_projector`, both lookups of a type declaration that failed to translate.

Proposed fix (patch 0003): a predicate `Errors.exn_is_recoverable` (everything except `Out_of_memory` and `Sys.Break`; nothing when `-abort-on-error` is set) and a generic `| exn when exn_is_recoverable exn ->` arm in those five places, which registers an error "Uncaught exception: …" against the function and then does what the `CFailure` arm does. For the micro-passes, the body of the function is replaced with an error node (extracted as `sorry`, like a body the interpreter could not translate), or the function is made opaque if that fails too. With it the reproduction gives a Lean file in which `V.height` is `sorry` and `add_one` is translated. Extraction tests (`make extract-tests`): the only changes are the Aeneas source line numbers quoted in two `.borrow-check.out` files (the handler moved); the patch updates them. The tests run with `-abort-on-error`, under which the new arms are inactive by design.

The reproduction is given in full below (`crash_stack_of_refs.rs`). A related, smaller defect in the extraction's error handler (the formatter is left with open boxes) is reported separately.

{{REPRO:crash_stack_of_refs.rs}}
{{PATCH:0003}}
