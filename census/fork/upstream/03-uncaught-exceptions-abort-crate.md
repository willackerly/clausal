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

**Versions.** Aeneas `0d21a9ec` (nightly-2026.11.10), built from source; Charon `454586e9` (0.1.315); Rust `nightly-2026-09-17`; macOS arm64. The release binary of nightly-2026.11.09 (`5a392f4b`) behaves the same.

**Commands** for a single-file reproduction:

```
charon rustc --preset=aeneas --dest-file repro.llbc -- repro.rs --crate-name=repro --crate-type=rlib --edition=2021
aeneas -backend lean -dest out repro.llbc
```

**Reproduction source.**

`crash_stack_of_refs.rs`:

```rust
// Candidate reproduction of the uncaught `Failure("ty_regions shouldn't be called on erased or body regions")`
// (shape of cedar-policy-core's `CedarValueJson::height`).
pub enum V {
    Leaf(u32),
    Set(Vec<V>),
}

impl V {
    pub fn height(&self) -> usize {
        let mut stack: Vec<(&V, usize)> = vec![(self, 0)];
        let mut max_depth: usize = 0;
        while let Some((val, depth)) = stack.pop() {
            if depth > max_depth {
                max_depth = depth;
            }
            match val {
                V::Leaf(_) => {}
                V::Set(vs) => {
                    for v in vs {
                        stack.push((v, depth + 1));
                    }
                }
            }
        }
        max_depth
    }
}

// Unrelated; lost together with the rest of the crate.
pub fn add_one(x: u32) -> u32 {
    x.wrapping_add(1)
}
```

<details><summary>Proposed patch (on top of the patches of the previous reports)</summary>

```diff
diff --git a/src/Errors.ml b/src/Errors.ml
index 0b479938..6d205699 100644
--- a/src/Errors.ml
+++ b/src/Errors.ml
@@ -113,6 +113,27 @@ let save_error_opt_span (file : string) (line : int) (span : Meta.span option)
 let save_error (file : string) (line : int) (span : Meta.span) (msg : string) =
   save_error_opt_span file line (Some span) msg
 
+(** Return [true] if, upon catching [exn] while processing one item (a function
+    body for instance), we can report an error for this item and continue with
+    the others.
+
+    Most of the code signals errors with {!CFailure}, but some helpers use
+    [failwith], [assert], [Option.get], [List.find], etc.: when such an
+    exception escapes, we do not want to lose the whole crate. *)
+let exn_is_recoverable (exn : exn) : bool =
+  (not !Config.fail_hard)
+  &&
+  match exn with
+  | Out_of_memory | Sys.Break -> false
+  | _ -> true
+
+(** Convert an uncaught exception to an error (which gets registered) *)
+let save_uncaught_exn (file : string) (line : int) (span : Meta.span option)
+    (exn : exn) : cfailure =
+  let msg = "Uncaught exception: " ^ Printexc.to_string exn in
+  save_error_opt_span file line span msg;
+  { span; file; line; msg }
+
 let add_loc (file : string) (line : int) (x : string -> int -> 'a) : 'a =
   x file line
 
diff --git a/src/Translate.ml b/src/Translate.ml
index c37a4782..0ba57265 100644
--- a/src/Translate.ml
+++ b/src/Translate.ml
@@ -282,11 +282,7 @@ let translate_function_to_pure (trans_ctx : trans_ctx) (marked_ids : marked_ids)
     (pure_global_decls : Pure.global_decl Pure.GlobalDeclId.Map.t)
     (fun_sigs : SymbolicToPureCore.fun_sigs FunOrMethodId.Map.t)
     (fdef : fun_decl) : pure_fun_translation_no_loops option =
-  try
-    Some
-      (translate_function_to_pure_aux trans_ctx marked_ids pure_type_decls
-         pure_global_decls fun_sigs fdef)
-  with CFailure error ->
+  let on_failure (error : Errors.cfailure) =
     let name = name_to_string trans_ctx fdef.item_meta.name in
     let name_pattern =
       try
@@ -302,6 +298,18 @@ let translate_function_to_pure (trans_ctx : trans_ctx) (marked_ids : marked_ids)
       ^ Errors.raw_span_to_string fdef.item_meta.span
       ^ compute_local_uses_error_message trans_ctx (IdFun fdef.def_id));
     None
+  in
+  try
+    Some
+      (translate_function_to_pure_aux trans_ctx marked_ids pure_type_decls
+         pure_global_decls fun_sigs fdef)
+  with
+  | CFailure error -> on_failure error
+  | exn when Errors.exn_is_recoverable exn ->
+      (* See the comment in {!Interp.evaluate_function_symbolic} *)
+      on_failure
+        (Errors.save_uncaught_exn __FILE__ __LINE__ (Some fdef.item_meta.span)
+           exn)
 
 type translated_crate = {
   type_decls : Pure.type_decl list;
@@ -1329,10 +1337,16 @@ let extract_definitions (fmt : Format.formatter) (config : gen_config)
 
   List.iter
     (fun g ->
-      try export_decl_group g
-      with CFailure _ ->
-        (* An exception was raised: ignore it *)
-        ())
+      try export_decl_group g with
+      | CFailure _ ->
+          (* An exception was raised: ignore it *)
+          ()
+      | exn when Errors.exn_is_recoverable exn ->
+          (* An exception which is not a [CFailure] (for instance [Not_found]
+             when looking up a declaration which we failed to translate):
+             register an error and continue with the next declaration group,
+             instead of losing the whole file. *)
+          ignore (Errors.save_uncaught_exn __FILE__ __LINE__ None exn))
     (Option.get ctx.crate.declarations)
 
 type extract_file_info = {
diff --git a/src/interp/Interp.ml b/src/interp/Interp.ml
index 6c6cc982..e8dd6b32 100644
--- a/src/interp/Interp.ml
+++ b/src/interp/Interp.ml
@@ -667,13 +667,7 @@ let evaluate_function_symbolic (synthesize : bool) (decls_ctx : decls_ctx)
 
   (* Evaluate the function *)
   let symbolic =
-    try
-      let body = [%add_loc] body_as_body_exn fdef.body in
-      let ctx_resl, cc = eval_function_body config body.body ctx in
-      let el = List.map (fun (ctx, res) -> finish res ctx) ctx_resl in
-      (* Finish synthesizing *)
-      if synthesize then Some (cc el) else None
-    with CFailure error ->
+    let on_failure (error : Errors.cfailure) : SA.expr option =
       let name = name_to_string () in
       let name_pattern =
         try
@@ -690,6 +684,22 @@ let evaluate_function_symbolic (synthesize : bool) (decls_ctx : decls_ctx)
         ^ Errors.raw_span_to_string fdef.item_meta.span
         ^ compute_local_uses_error_message decls_ctx (IdFun fdef.def_id));
       if synthesize then Some (Error (error.span, error.msg)) else None
+    in
+    try
+      let body = [%add_loc] body_as_body_exn fdef.body in
+      let ctx_resl, cc = eval_function_body config body.body ctx in
+      let el = List.map (fun (ctx, res) -> finish res ctx) ctx_resl in
+      (* Finish synthesizing *)
+      if synthesize then Some (cc el) else None
+    with
+    | CFailure error -> on_failure error
+    | exn when Errors.exn_is_recoverable exn ->
+        (* An exception which is not a [CFailure] escaped from the symbolic
+           execution of this body: report it against this function instead of
+           aborting the translation of the whole crate. *)
+        on_failure
+          (Errors.save_uncaught_exn __FILE__ __LINE__ (Some fdef.item_meta.span)
+             exn)
   in
   (* Return *)
   (input_svs, symbolic)
diff --git a/src/pure/PureMicroPasses.ml b/src/pure/PureMicroPasses.ml
index e2f2c4a0..4f6e2425 100644
--- a/src/pure/PureMicroPasses.ml
+++ b/src/pure/PureMicroPasses.ml
@@ -514,6 +514,42 @@ let apply_passes_to_pure_fun_translations (crate : LlbcAst.crate)
 
     trans
   in
+  (* Apply the micro-passes to one function, catching the errors.
+
+     The micro-passes raise exceptions on the functions they do not support
+     (failed lookups, internal invariants, etc.). Those used to escape and abort
+     the translation of the whole crate, without any output. We now report the
+     error against the function, and replace its body with an error node (which
+     gets extracted as a hole, like the bodies we fail to translate in the
+     symbolic interpreter). If even this fails, we make the function opaque. *)
+  let apply (rank : int) (f : fun_decl) : pure_fun_translation =
+    try apply rank f
+    with exn when Errors.exn_is_recoverable exn -> (
+      let span = f.item_meta.span in
+      let msg =
+        match exn with
+        | Errors.CFailure error -> error.msg
+        | _ ->
+            (Errors.save_uncaught_exn __FILE__ __LINE__ (Some span) exn).msg
+      in
+      [%warn] span
+        ("Could not post-process (micro-passes) the function '" ^ f.name
+       ^ "' because of previous error: its body is replaced with an error");
+      let opaque : pure_fun_translation =
+        { f = { f with body = None }; loops = []; bodies = [] }
+      in
+      match f.body with
+      | None -> opaque
+      | Some body -> (
+          let body =
+            {
+              body with
+              body = { e = EError (Some span, msg); ty = body.body.ty };
+            }
+          in
+          try apply rank { f with body = Some body }
+          with exn when Errors.exn_is_recoverable exn -> opaque))
+  in
   let transl =
     (* Partition the opaque and transparent functions *)
     let opaque, transparent =
diff --git a/src/pure/PureMicroPassesAnnots.ml b/src/pure/PureMicroPassesAnnots.ml
index d85cc0fc..a0de04f4 100644
--- a/src/pure/PureMicroPassesAnnots.ml
+++ b/src/pure/PureMicroPassesAnnots.ml
@@ -416,21 +416,7 @@ let add_type_annotations (trans_ctx : trans_ctx)
          trans_funs)
   in
   let add_annot (decl : fun_decl) =
-    try
-      [%ltrace
-        let fmt = trans_ctx_to_pure_fmt_env trans_ctx in
-        "About to add type annotations to:\n\n"
-        ^ PrintPure.fun_decl_to_string fmt decl];
-      let decl =
-        add_type_annotations_to_fun_decl trans_ctx trans_funs_map type_decls
-          decl
-      in
-      [%ltrace
-        let fmt = trans_ctx_to_pure_fmt_env trans_ctx in
-        "After adding type annotations:\n\n"
-        ^ PrintPure.fun_decl_to_string fmt decl];
-      decl
-    with Errors.CFailure error ->
+    let on_failure (error : Errors.cfailure) =
       let name = name_to_string trans_ctx decl.item_meta.name in
       let name_pattern =
         try
@@ -447,6 +433,29 @@ let add_type_annotations (trans_ctx : trans_ctx)
         );
       (* Keep the unchanged decl *)
       decl
+    in
+    try
+      [%ltrace
+        let fmt = trans_ctx_to_pure_fmt_env trans_ctx in
+        "About to add type annotations to:\n\n"
+        ^ PrintPure.fun_decl_to_string fmt decl];
+      let decl =
+        add_type_annotations_to_fun_decl trans_ctx trans_funs_map type_decls
+          decl
+      in
+      [%ltrace
+        let fmt = trans_ctx_to_pure_fmt_env trans_ctx in
+        "After adding type annotations:\n\n"
+        ^ PrintPure.fun_decl_to_string fmt decl];
+      decl
+    with
+    | Errors.CFailure error -> on_failure error
+    | exn when Errors.exn_is_recoverable exn ->
+        (* For instance: [Not_found] when looking up a type declaration which
+           we failed to translate *)
+        on_failure
+          (Errors.save_uncaught_exn __FILE__ __LINE__
+             (Some decl.item_meta.span) exn)
   in
   List.map
     (fun (fl : pure_fun_translation) ->
diff --git a/tests/src/borrow-check-negative.borrow-check.out b/tests/src/borrow-check-negative.borrow-check.out
index 2d8c6d23..959f4860 100644
--- a/tests/src/borrow-check-negative.borrow-check.out
+++ b/tests/src/borrow-check-negative.borrow-check.out
@@ -5,7 +5,7 @@ Compiler source: interp/InterpPaths.ml, line 253
 Name pattern: 'borrow_check_negative::choose_test'
 Definition span: 'tests/src/borrow-check-negative.rs', lines 16:0-26:1
 Source: 'tests/src/borrow-check-negative.rs', lines 25:12-25:14
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
 [[91mError[39m] Can't end abstraction 8 as it is set as non-endable
 Source: 'tests/src/borrow-check-negative.rs', lines 28:0-34:1
@@ -14,7 +14,7 @@ Compiler source: interp/InterpBorrows.ml, line 1213
 Name pattern: 'borrow_check_negative::choose_wrong'
 Definition span: 'tests/src/borrow-check-negative.rs', lines 28:0-34:1
 Source: 'tests/src/borrow-check-negative.rs', lines 28:0-34:1
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
 [[91mError[39m] Can not apply a projection to the ⊥ value
 Source: 'tests/src/borrow-check-negative.rs', lines 42:4-42:11
@@ -23,7 +23,7 @@ Compiler source: interp/InterpPaths.ml, line 253
 Name pattern: 'borrow_check_negative::test_mut1'
 Definition span: 'tests/src/borrow-check-negative.rs', lines 36:0-43:1
 Source: 'tests/src/borrow-check-negative.rs', lines 42:4-42:11
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
 [[91mError[39m] Can not apply a projection to the ⊥ value
 Source: 'tests/src/borrow-check-negative.rs', lines 51:12-51:14
@@ -32,7 +32,7 @@ Compiler source: interp/InterpPaths.ml, line 253
 Name pattern: 'borrow_check_negative::test_mut2'
 Definition span: 'tests/src/borrow-check-negative.rs', lines 46:0-52:1
 Source: 'tests/src/borrow-check-negative.rs', lines 51:12-51:14
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
 [[91mError[39m] Can not apply a projection to the ⊥ value
 Source: 'tests/src/borrow-check-negative.rs', lines 65:12-65:17
@@ -41,7 +41,7 @@ Compiler source: interp/InterpPaths.ml, line 253
 Name pattern: 'borrow_check_negative::refs_test1'
 Definition span: 'tests/src/borrow-check-negative.rs', lines 59:0-66:1
 Source: 'tests/src/borrow-check-negative.rs', lines 65:12-65:17
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
 [[91mError[39m] Can not apply a projection to the ⊥ value
 Source: 'tests/src/borrow-check-negative.rs', lines 80:12-80:17
@@ -50,7 +50,7 @@ Compiler source: interp/InterpPaths.ml, line 253
 Name pattern: 'borrow_check_negative::refs_test2'
 Definition span: 'tests/src/borrow-check-negative.rs', lines 68:0-81:1
 Source: 'tests/src/borrow-check-negative.rs', lines 80:12-80:17
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
 [[91mError[39m] Can not apply a projection to the ⊥ value
 Source: 'tests/src/borrow-check-negative.rs', lines 91:12-91:15
@@ -59,5 +59,5 @@ Compiler source: interp/InterpPaths.ml, line 253
 Name pattern: 'borrow_check_negative::test_box1'
 Definition span: 'tests/src/borrow-check-negative.rs', lines 83:0-92:1
 Source: 'tests/src/borrow-check-negative.rs', lines 91:12-91:15
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
diff --git a/tests/src/loops-borrow-check-negative.borrow-check.out b/tests/src/loops-borrow-check-negative.borrow-check.out
index 183fe9b7..c3a7da21 100644
--- a/tests/src/loops-borrow-check-negative.borrow-check.out
+++ b/tests/src/loops-borrow-check-negative.borrow-check.out
@@ -5,5 +5,5 @@ Compiler source: interp/InterpBorrows.ml, line 1213
 Name pattern: 'loops_borrow_check_negative::loop_a_b'
 Definition span: 'tests/src/loops-borrow-check-negative.rs', lines 20:0-30:1
 Source: 'tests/src/loops-borrow-check-negative.rs', lines 20:0-30:1
-Compiler source: interp/Interp.ml, line 686
+Compiler source: interp/Interp.ml, line 680
 
```

</details>
