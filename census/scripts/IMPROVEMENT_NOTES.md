<!-- Blocks for IMPROVEMENTS.md. scripts/tables.py splices them in rank order: the five highest-ranked ids
     that have a block go under "The top five", the others under "Further candidates".
     A block starts at `@@ <id>` and runs to the next `@@`. {{...}} placeholders are filled as in the templates. -->

@@ abort
### `abort`: skip a trait method whose signature fails, instead of aborting the crate (Aeneas)

- **Unlocks.** {{imp:abort}}: every function that compiles in the peeled runs of the five crates Aeneas aborts on as shipped. The peel emulates this fix (for a trait it removes the whole trait where the fix would drop single methods, so the fix should do no worse).
- **What happens.** `translate_crate_to_pure` computes all signatures first. For function declarations the loop catches the error and logs "Could not translate the function signature of …" (`src/Translate.ml`, lines 370–398). For trait methods, `translate_method_sig` (lines 400–425) has no handler, so one `CFailure` ends the run with no output.
- **Triggers seen.** (a) a trait method whose signature has a trait-type constraint (`Iterator::copied`, `cloned`, `try_fold`: `where Self: Iterator<Item = &T>`), stopped by the sanity check `sg.item_binder_params.trait_type_constraints = []` in `translate_fun_sigs` (`src/symbolic/SymbolicToPureTypes.ml`, line 1005); (b) `Pattern::into_searcher`, whose return type is a generic associated type (`Self::Searcher<'a>`), stopped at line 392; (c) on cedar, local traits with `dyn` in a method signature (line 132/190).
- **The change.** Wrap the body of `translate_method_sig` in the same `try … with CFailure` as the function case and leave the method out of `method_sigs`. Then make the lookups of a missing method signature raise a located, recoverable error instead of `Not_found`; the removal experiment shows users of the method already fail one by one with "Could not find: trait_decl: …, method …" when the method entry is absent. The trait declaration extraction (`src/extract/Extract.ml`, `extract_trait_decl_*`) must skip the same methods.
- **Size.** Small: tens of lines in two or three places, plus regenerating the test outputs. A day or two for someone who can build Aeneas.
- **Risk.** A removed required method leaves impls of the trait with a method the trait no longer declares; on `Pattern` this made extraction raise `Not_found` in `trait_impl_is_builtin` (`Translate.ml`, line 1066) until the impls were dropped too. The fix has to drop or stub the impl method consistently.
- **Second half of the same problem.** An error during extraction (after translation) can leave the output file unbalanced: a float cast raises inside an open formatting box (`Extract.ml`, line 487) and every later definition is emitted indented inside an unfinished `ok (`. Lean still recovers; a reader does not. Closing the boxes in the handler belongs to the same patch.

@@ ice
### `ice`: a failed type-annotation recovery must not become a rustc ICE (Charon)

- **Unlocks.** {{imp:ice}}. All of `cedar-policy-core`: as shipped, Charon produces no LLBC for it.
- **What happens.** For every user type annotation in a body (`collect::<Vec<_>>()`, `let x: T = …`), Charon re-runs rustc's `AscribeUserType` type operation to recover the annotated type (`charon/src/bin/charon-driver/hax/rustc_utils.rs`, `translate_user_annotation`, line 26; called from `translate/user_type_annotations.rs`, line 159). When `fully_perform` fails, Charon maps the error to the warning "could not recover user type ascription", but rustc has already recorded a delayed bug ("error performing operation: fully_perform"), and rustc panics on exit. Cedar has 49 such sites.
- **Age.** The code is from commits `b2fddb3a3` and `6b752bef5` (2026-11-07) and `454586e9b` (2026-11-08). hax 0.5.0 pins Charon nightly-2026.10.31 and gets through Charon on cedar.
- **The change.** Either perform the operation in a way that does not register a delayed bug (run it inside a probe / use the obligation context directly and discard errors), or pin a Charon from before 2026-11-07 until upstream fixes it.
- **Size.** Small in lines, but it needs someone who knows rustc's trait-query API. As a user, the zero-code route is the older pin.
- **Workaround used here.** The functions containing the 49 sites were marked `#[charon::opaque]`; they are the `charon_ice` class.

@@ shadow
### `shadow`: names in the generated Lean that resolve to the wrong thing (Aeneas, Lean backend)

- **Unlocks.** {{imp:shadow}}.
- **Two defects.**
  1. Builtin types are printed by bare name (`src/extract/ExtractBase.ml`, `builtin_adts`, lines 1137–1150: `(TSlice, "Slice")`, `"Array"`, `"Str"`, `"Result"`). Inside `structure map.slice.Slice … where entries : Slice (Bucket K V)` Lean resolves `Slice` to the structure being declared. The declaration fails, Lean recovers with `sorry`, and every function mentioning the type compiles only "using sorry". The comment above the table already notes the same hazard for `Error`.
  2. Local variable names are checked for collision against full declaration names only (`ExtractBase.ml`, `basename_to_unique`, line 2118). A parameter `input` next to a module `input` gives `input.Input.into_value input`, which Lean parses as a field access on the parameter.
- **The change.** (1) Emit builtin types fully qualified (`Aeneas.Std.Slice`), or rename a user type whose last component is a builtin name. (2) In `basename_to_unique`, also reject a variable name equal to the first component of any registered declaration name (keep a set of first components next to `names_set`).
- **Size.** Small: one table and one predicate, plus test output churn. No change to the translation itself.
- **Until then.** Renaming in the Rust source works (profile rule 13; rewrite experiment in `CENSUS.md`).

@@ loops
### `loops`: early exit from loops in general (Aeneas)

- **Unlocks.** {{imp:loops}}. Few functions, but long ones: parsers and formatters.
- **What happens.** `update_loops` in `src/PrePasses.ml` (lines 489–660) rewrites a `return` inside a loop into a `break` followed by the statements after the loop. `decompose_after` (line 571) needs those statements to end in `return` or a panic in the same block, otherwise "Early returns inside of loops are not supported yet" (line 575). A `for` loop desugars to a `loop` inside a `match` on the iterator, so a `?` or `return` in a `for` body is often already one level too deep. `Break i` with `i > 0` is rejected at lines 592 and 637, a `return` at depth 2 at line 647.
- **The change.** Replace the syntactic rewrite by the standard one: give each loop a result of type "continue | break | return value" (the Lean library already has `ControlFlow` for loop bodies) and thread it through enclosing loops. That removes all three restrictions at once.
- **Size.** Medium: one pre-pass of about 170 lines to redesign, and the loop translation (`src/interp/InterpLoops*.ml`, 930 lines) has to accept the new shape. One to three weeks, with the regression suite.
- **Until then.** The source rewrite is mechanical (profile rule 2).

@@ float
### `float`: floating-point operations, constants and casts (Aeneas + Lean library)

- **Unlocks.** {{imp:float}}.
- **What happens.** `eval_binary_op_symbolic` accepts integers and booleans only and raises "Invalid inputs for binop" otherwise (`src/interp/InterpExpressions.ml`, line 1189); the literal conversion accepts booleans, chars and integers only (line 120, "Improperly typed constant value"); the cast printer covers integer and boolean casts only (`src/extract/Extract.ml`, line 487, "Unreachable", which also unbalances the output file).
- **The change.** Treat `f32`/`f64` as opaque scalar types: allow the binary operators and comparisons on them as uninterpreted (total) operations, accept float literals, add the four cast directions, and declare the operations in the Lean library (as axioms or over Lean's `Float`).
- **Size.** Small to medium on the Aeneas side (three match arms and their printing), plus a library file. The open question is semantic, not technical: which float model proofs should see.
- **Until then.** Keep floats out of translated code (profile rule 9).

@@ fnitem
### `fnitem`: function items passed as values (Aeneas)

- **Unlocks.** {{imp:fnitem}}.
- **What happens.** `x.map(Type::method)` gives the argument the type of the function item (`TFnDef`). Both `explore_ty` in `src/llbc/RegionsHierarchy.ml` (lines 295–315) and `translate_fwd_ty` in `src/symbolic/SymbolicToPureTypes.ml` (lines 396–398) assert that such a type has no bound regions and no region arguments, and raise "Unimplemented" otherwise. Any method with `&self` has a late-bound lifetime, so the wrapper rustc builds (`impl FnOnce for <fn item>`) fails for almost every method passed by name.
- **The change.** Open the binder of the function-item type and treat its regions like those of a closure signature (closures with the same shape are translated today). The comment at `RegionsHierarchy.ml` line 296 describes the intended approach.
- **Size.** Medium: the region-hierarchy analysis is delicate; one to two weeks.
- **Until then.** Call the method inside a `match` (profile rule 7). A closure wrapper is not a fix when the method returns a reference.

@@ dyn
### `dyn`: trait objects (Charon + Aeneas)

- **Unlocks.** {{imp:dyn}}. Most of these ({{n:classes.trait_removed.any}}) are methods of impls of the local cedar traits that were removed in the peel because a method signature mentions `dyn` (`TCNode::out_edges` returns `Box<dyn Iterator>`), plus the impls of `miette::Diagnostic`; {{n:classes.dyn_trait.any}} functions use a trait object directly.
- **What happens.** Charon already translates vtables (`charon/src/bin/charon-driver/translate/translate_trait_objects.rs`, 1,424 lines). Aeneas rejects `dyn` at every level: in types ("Dynamic trait types are not supported yet", `src/symbolic/SymbolicToPureTypes.ml`, lines 132, 190, 540, 675), in the region analysis (guarded by `type_analysis_ignore_dyn`, `src/Config.ml`, line 515) and at calls ("Function pointers are not supported yet", `src/interp/InterpStatements.ml`, line 1249, raised on the vtable call).
- **The change.** A design decision before code: model `dyn Trait` as an existential package (a type plus its trait instance) in the pure translation, then implement type translation, unsizing coercions, vtable calls and the borrow reasoning through them.
- **Size.** Large: a feature, not a patch. Months, and best done with upstream.
- **Until then.** Generics or an enum of the cases (profile rule 10).

@@ pattern
### `pattern`: `core::str::pattern::Pattern` and the `str` search functions (Aeneas + Lean library)

- **Unlocks.** {{imp:pattern}}, and it removes the most common trigger of the whole-crate abort.
- **What happens.** `Pattern::into_searcher` returns the generic associated type `Self::Searcher<'a>`. `translate_fwd_ty` asserts that an associated type has no generic arguments (`src/symbolic/SymbolicToPureTypes.ml`, lines 390–394, "Unimplemented"). The only argument here is a lifetime, and lifetimes are erased by that very function (`TRef (_, rty, _) -> translate rty`, line 381).
- **The change.** Accept associated types whose generic arguments are regions only. `str::split`, `find`, `starts_with` and the rest would then be emitted as opaque declarations (axioms) instead of aborting; models of the common ones over byte slices can follow in the library.
- **Size.** Small for the assertion; medium for useful models (each search function needs a specification).
- **Until then.** Byte loops (profile rule 5).

@@ itersig
### `itersig`: trait methods with trait-type constraints, and iterator models (Aeneas + Lean library)

- **Unlocks.** {{imp:itersig}}; together with `abort` this is what stops `Iterator::copied`/`cloned`/`try_fold` from costing a crate.
- **What happens.** The sanity check `sg.item_binder_params.trait_type_constraints = []` in `translate_fun_sigs` (`src/symbolic/SymbolicToPureTypes.ml`, line 1005). The Lean model of `Iterator` (`backends/lean/Aeneas/Std/Core/Iter.lean` and neighbours) has `next` and a few adaptors; the census log lists `all`, `zip`, `peekable`, `rev`, `map`, `collect`, `fold` … as "could not find the information for item".
- **The change.** Translate the constraint as an equality hypothesis on the associated type (Charon can already lift associated types to parameters: `--lift-associated-types`), and extend the library model of `Iterator`.
- **Size.** Medium for the constraint; the models are open-ended.

@@ borrow
### `borrow`: borrow patterns outside the supported fragment (Aeneas)

- **Unlocks.** {{imp:borrow}}.
- **What it is.** Not one defect. The raising sites are spread over the symbolic interpreter: nested borrows (`src/interp/InterpAbs.ml`, `InterpMatchCtxs.ml`, about 40 sites), abstractions that may not be ended (`InterpBorrows.ml`, line 1213), projections Aeneas considers inconsistent (`InterpPaths.ml`, line 258: slice patterns, references into `Option<&T>`), joins of borrow states after a branch or loop (`InterpJoin.ml`, line 1571; `SymbolicToPureCore.ml`, line 519), and the translation of ended projections (`SymbolicToPureValues.ml`, lines 870 and 888).
- **The change.** This is the core of Aeneas's borrow reasoning; the messages themselves say "not supported yet". Individual cases may be patchable; the class is not a contribution a newcomer makes in a week.
- **Size.** Large and uncertain.
- **Until then.** Return owned values or indices instead of references into containers of references; avoid closures that return a borrow of their argument.

@@ rawptr
### `rawptr`: raw pointers and pointer casts (Aeneas)

- **Unlocks.** {{imp:rawptr}}.
- **What happens.** "Aeneas does not yet support dereferencing raw pointers" (`src/interp/InterpPaths.ml`, line 197); `&raw const`/`&raw mut` (`InterpExpressions.ml`, line 1495); pointer/integer casts (line 994); pointer-to-pointer casts between non-literal types (`src/symbolic/SymbolicToPureExpressions.ml`, line 604).
- **The change.** Outside the design: Aeneas's model is of safe Rust. A realistic step is to make such functions opaque automatically (emit an axiom for the function and continue) instead of an error.
- **Size.** The automatic-opaque fallback is small; real support is not on the table.

@@ match
### `match`: `match` on `char`, signed literal patterns, enum expansion (Aeneas, partly Lean backend)

- **Unlocks.** {{imp:match}}.
- **What happens.** A switch on a symbolic value is implemented for booleans and integers only (`src/interp/InterpStatements.ml`, lines 927–988, "Unsupported switch scrutinee"): `char` is not an integer type there. Separately, a `match` on a signed integer with negative literal patterns is emitted as a Lean `match` on scalar literals that Lean cannot compile ("Failed to compile pattern matching: Stuck at … BitVec").
- **The change.** Add the `TChar` case next to the integer case (`expand_symbolic_int` generalised to chars); emit `if`/`else` chains for signed literal matches in the Lean backend.
- **Size.** Small for both.

@@ hrtb
### `hrtb`: higher-ranked lifetimes related to free lifetimes (Aeneas)

- **Unlocks.** {{imp:hrtb}}.
- **What happens.** `src/llbc/TypesAnalysis.ml`, line 990: a constraint between a locally bound region and a free one in a signature (`impl for<'b> FnOnce(&'b mut Reader<'a>)`) is rejected.
- **Size.** Medium to large; same area as `fnitem`.

@@ leanmisc
### `leanmisc`: remaining failures of the generated Lean (Aeneas, Lean backend and library)

- **Unlocks.** {{imp:leanmisc}}. A bag of distinct defects, each small; the main ones in this corpus:
  - **Impl of a modelled trait with more methods than the model.** "`size_hint` is not a field of structure `core.iter.traits.iterator.Iterator`". The flag `-filter-trait-methods` already removes these errors (see below); the failed declarations are trait instances, and no function of this corpus was failing only because of one.
  - **Universe level metavariables** in definitions mentioning `core::num::nonzero::NonZero` (semver's identifier, time's `Date`): the declaration of `ZeroablePrimitive` fails first ("Field `markerCopyInst` has already been declared"), and its users cannot be elaborated.
  - **Implicit arguments that cannot be inferred** ("don't know how to synthesize implicit argument"): a type parameter that appears only in a trait-instance argument.
  - **Unresolved names** for a declaration that is present in the file (`money.Money` in rusty-money, used inside `money.Money.Insts.…`): the same family as `shadow`.
  - **Two Rust items mapped to one Lean name** ("Name clash detected", `src/extract/ExtractBase.ml`, line 246).
- **Size.** Each is a small backend fix; together a few weeks. They share one property: Aeneas reported success for these functions, and only compiling the output shows the failure. Running `lake build` on the generated file in Aeneas's own test suite for a few real crates would catch the class.

@@ internal
### `internal`: internal errors without a message (Aeneas)

- **Unlocks.** {{imp:internal}}. "Internal error, please file an issue", "Unreachable", "Unimplemented" with no text. The raising lines are in `data/summary.json` (`emitters`); the most frequent are `llbc/ValuesUtils.ml` 43, `symbolic/SymbolicToPureTypes.ml` 724, `Translate.ml` 192 and `interp/InterpPaths.ml` 172. Not analysed further.

@@ mixed
### `mixed`: go on after a declaration group that mixes functions with types or trait impls (Aeneas)

- **Unlocks.** {{imp:mixed}} by the message count. The measured bound is lower: when the peel was extended to emulate this fix on `cedar-policy-core` (mixed groups moved to the end of the declaration order), 1,559 of its 2,503 counted functions logged no Aeneas error, against 37 in the reported run; the run then died in a pure micro-pass and wrote no Lean (`data/cedar_before_mixed_group_fix.summary.json`). So: up to about 1,500 functions at the Aeneas stage, none confirmed through Lean, and the `crash` item below stands between the two.
- **What happens.** `analyze_decl_groups` in `src/llbc/FunsAnalysis.ml` (lines 273–305) walks the declaration groups in order. A group of functions that fails is logged and the walk continues (`analyze_decl_groups decls'`, line 296). A `MixedGroup` is logged ("Mixed declaration groups … are not supported yet", line 299) and the walk ends there: there is no recursive call. Every function after it has no analysis result, and `compute_raw_fun_effect_info` (`src/symbolic/SymbolicToPureTypes.ml`, line 724) fails for each with "Internal error: please file an issue".
- **Reproduction.** `census/probes/mixed-group-probe-0.1.0` (about 100 lines): two types whose `Display` impls format each other. {{mixed_probe_before_ok}} functions compile; every function declared after the pair fails. Ready to attach to an upstream issue.
- **Where it bites.** It depends on where the group falls in the order. On cedar it is early; on `rust_decimal` it is fifth from the end and costs four functions. The error message names the group, not the functions that silently follow it.
- **The change.** Add the missing `analyze_decl_groups decls'` after the mixed-group error, so that only the functions of the group and their users are lost. One line, plus a test.
- **Size.** Trivial for the line. What it exposes is not: on cedar the next failures were uncaught exceptions in `src/pure/PureMicroPassesGeneral.ml` (`simplify_trait_calls`, line 2331; `let_to_match` via `PureUtils.tpat_decomposes_enum`, line 2711), in many functions. Supporting mixed groups themselves (types that are mutually recursive with functions through trait impls) is a larger matter again.

@@ crash
### `crash`: catch every exception per function, not only Aeneas's own error type (Aeneas)

- **Unlocks.** {{imp:crash}} directly; and, like `abort`, it is a precondition for getting anything out of the crate they are in.
- **What happens.** The per-function handlers in `src/Translate.ml` (lines 289, 344, 381, 541, 573) and `src/interp/Interp.ml` (line 676) catch `CFailure` only, and the pure micro-passes (`src/pure/PureMicroPasses.ml`, `apply_passes_to_def`) have no per-function handler at all. On six function bodies of `cedar-policy-core` the symbolic interpreter raises an OCaml `Failure` instead (`ty_regions shouldn't be called on erased or body regions`, `src/llbc/TypesUtils.ml` line 98, reached from `symbolic_value_has_ended_regions`, `src/interp/InterpUtils.ml` line 489). It is not caught, and the run ends with no output and no indication of which function it was. Finding the six took 129 Aeneas runs of bisection.
- **The change.** Catch all exceptions at the per-function boundary and turn them into the same "Could not translate the body of function …" report; print the function name when re-raising anything.
- **Size.** Small.
