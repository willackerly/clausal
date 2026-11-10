## The patches

Branch `census-fork` in the local clone `census/fork/aeneas` (git-ignored): the four commits asked for, in the order asked, and a fifth that the cedar run showed was needed, on top of `0d21a9ec`. The same commits are `git am`-ready files in `census/fork/patches/`; they also apply to `5a392f4b`, the commit of the census's main binary. In all {{DIFFSTAT}}, in 9 source files and 2 expected-output files. The code was not run through `ocamlformat` (not installed), which upstream's CI enforces.

### (i) `FunsAnalysis`: go on after a mixed declaration group — 6 lines

- **Defect.** `analyze_decl_groups` walks the declaration groups in order and recurses in every case except `MixedGroup`, where it logs "Mixed declaration groups … are not supported yet" and returns. Every function after the first such group has no analysis result and fails with "Internal error" when its signature is computed.
- **Change.** Recurse on the remaining groups after logging the error.
- **What it does not do.** The functions *in* a mixed group still get no analysis result, and so does every function that calls one of them, directly or not (Aeneas's analysis fails a function whose callee has no result). On cedar that cascade is the largest remaining blocker (see "What still blocks cedar").

{{PATCH:0001}}

### (ii) `Translate`: a trait method signature that fails marks that method, not the crate — 78 lines

- **Defect.** All signatures are computed before any body. The loop over function declarations catches Aeneas's error type (`CFailure`); the one over trait methods (`translate_method_sig`) does not, so one method signature ends the run with no output. Seen triggers: `Iterator::copied`/`cloned`/`try_fold` (trait-type constraint), `Pattern::into_searcher` (generic associated type), local traits with `dyn` in a method.
- **Change, three parts.**
  1. Catch the error per trait method, log a warning that names the trait and the method, and remove the method from the set of methods to extract, so that the trait declaration is translated without it.
  2. When translating a trait impl, ignore the methods that are no longer extracted for its trait. Without this the impl would define a field the declaration lacks.
  3. When a trait *declaration* fails to translate (this was already caught), skip its impls with a located error. Before, the impl was kept and the extraction raised `Not_found` looking for its declaration, which aborted the crate at a later point: on `Pattern`, part 1 alone only moves the abort.
- **Behaviour for users of a removed method or impl.** A use of a removed impl is logged ("Could not find: trait_impl_id …") and emitted as `sorry`, so that function fails by itself (`s.find(':')`). A call that resolves to the *default implementation* of a removed method is still emitted, as a call to that function, which for a standard-library method is an axiom (`v.iter().copied()` becomes a call to `Iterator.copied.default`): the caller compiles and rests on an unmodelled external, as any caller of an unmodelled library function does. No case was seen where a removed item is replaced by something else.
- **Difference from the census's peel.** The peel removed a whole trait with all its impls where this removes one method, and yet the counts on the five crates are identical function for function (table below). The methods of impls of a trait whose declaration fails (`Pattern`) are still translated as plain functions here.

{{PATCH:0002}}

### (iii) Catch exceptions that are not `CFailure`, per function and per declaration group — 129 lines

- **Defect.** Aeneas signals errors with `CFailure`, and its per-item handlers match only that. Helper code also raises `Failure`, `Not_found` and `Invalid_argument`; one of those in one function ends the run with no output and no function name.
- **Change.** A predicate `Errors.exn_is_recoverable` (every exception except `Out_of_memory` and `Sys.Break`; none at all under `-abort-on-error`) and `Errors.save_uncaught_exn`, which registers an error "Uncaught exception: …" against the item. Handlers added in five places:
  1. `Interp.evaluate_function_symbolic` (symbolic execution of one body): the function is kept with an error body, as for `CFailure`.
  2. `Translate.translate_function_to_pure`: the function is dropped, as for `CFailure`.
  3. `PureMicroPasses.apply_passes_to_pure_fun_translations`: the micro-passes had no per-function handler at all. On failure the body is replaced by an error node and the passes are applied to that (the function is then extracted as `def … := sorry`); if that fails too the function is made opaque (an `axiom`).
  4. `PureMicroPassesAnnots.add_type_annotations`: same arm as its existing `CFailure` handler (the declaration is kept without annotations and an error is registered).
  5. `Translate.extract_definitions`: an uncaught exception in one declaration group no longer loses the file.
- **Wider than the task's wording.** The task names the micro-passes. On cedar the first uncaught exception is in the symbolic interpreter (1), the next in the micro-passes (3), then in `add_type_annotations` (4), then in the extraction (5); each was found by running cedar and reading where it died. All five are in the one commit because any one of them alone leaves cedar with no output.
- **What a caught function looks like.** `sorry` or `axiom`, plus an error in the log. The census join counts both as "failed at Aeneas", so this patch cannot add a function to the "compiles" column by hiding a failure; it adds the functions *around* the failed one.
- **Left to patch (v).** After an exception in the middle of printing a definition the open formatting boxes are not closed. That is the existing `CFailure` behaviour, and this patch makes it reachable more often.
- **Expected-output churn.** Two `.borrow-check.out` files quote the Aeneas source line of a warning that moved (`Interp.ml, line 686` to `680`); the commit updates them.

{{PATCH:0003}}

### (iv) Lean backend: two kinds of name capture — 109 lines

- **Defect 1.** Builtin types and the functions in their namespace are printed by short name (`Slice`, `Slice.len`, `Array.index_usize`, `Result` …) and found through `open Aeneas.Std`. A user declaration `X.Slice` takes precedence in every definition whose name starts with `X.`, beginning with `structure X.Slice … where entries : Slice …` itself.
- **Change 1.** Collect the last name component of the crate's own type and trait declarations. A builtin type, builtin pure function or library function whose first name component is in that set is printed as `Aeneas.Std.<name>`. Crates with no such declaration get identical output, which is why Aeneas's test outputs do not change. A first version qualified on any declaration, external ones included; `core::result::Result` is in nearly every crate, so that rewrote `Result` in 39 test outputs and was narrowed.
- **Defect 2.** A local variable named like the first component of a declaration name captures it: with a parameter `input` in scope, `input.Input.get input` is a field access on the parameter.
- **Change 2.** The names map keeps the set of first components of all registered dotted names, and `basename_to_unique` treats those as collisions too (Lean only), so the parameter is printed `input1`.
- **Limits.** Only short names beginning with a builtin *type* name are covered, and only when the shadowing declaration is local. Names of the form `core.…`/`alloc.…` printed by Aeneas are not qualified; a crate with its own module called `core` would capture them.

{{PATCH:0004}}


### (v) Extraction: reset the formatter after an error — 14 lines (extra, not in the task)

- **Defect.** Aeneas prints through OCaml's `Format` boxes. When an exception interrupts the printing of a definition, the boxes open at that point are never closed. Every later definition is printed indented inside the unfinished one; after enough of them the indentation reaches the margin and each token goes on its own line, at the column of the `def` keyword. Lean requires the tokens of a signature to be to the right of `def`, so from that point on every definition is a parse error ("unexpected token '('; expected ':=', 'where' or '|'"). The census had noted the indentation as cosmetic on `time`; on cedar, with patches (i)-(iv), {{SYNTAX_P4}} counted functions end in a Lean parse error and most declaration lines of the file are indented.
- **How it was found.** Parse errors are one of the three large Lean-stage classes of the cedar run with patches (i)-(iv). It existed before (the handler for `CFailure` has the same gap), but only a crate with many extraction errors gets far enough to the right.
- **Change.** In the per-declaration-group handler of `extract_definitions`, for both the existing `CFailure` arm and the new one: `Format.pp_print_newline` (which closes every open box) and re-open the top-level vertical box that `extract_file` expects.
- **Effect.** None on Aeneas's test outputs and none on the counts of the nine other crates as shipped. On `time` the generated file is no longer indented (see "Not measured" above for the figures). **On cedar its effect was not measured:** the run with (i)-(v) did not finish.

{{PATCH:0005}}
