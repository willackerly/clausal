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

**Versions.** Aeneas `0d21a9ec` (nightly-2026.11.10), built from source; Charon `454586e9` (0.1.315); Rust `nightly-2026-09-17`; macOS arm64. The release binary of nightly-2026.11.09 (`5a392f4b`) behaves the same.

**Commands** for a single-file reproduction:

```
charon rustc --preset=aeneas --dest-file repro.llbc -- repro.rs --crate-name=repro --crate-type=rlib --edition=2021
aeneas -backend lean -dest out repro.llbc
```

**Reproduction source.**

`abort_copied.rs`:

```rust
// Aeneas aborts the whole crate (no output) on the signature of `Iterator::copied`.
pub fn copied_max(v: &[u32]) -> Option<u32> {
    v.iter().copied().max()
}

// Unrelated; lost together with the rest of the crate.
pub fn add_one(x: u32) -> u32 {
    x.wrapping_add(1)
}
```

`abort_pattern.rs`:

```rust
// Aeneas aborts the whole crate (no output) on the signature of `core::str::pattern::Pattern::into_searcher`.
pub fn find_colon(s: &str) -> Option<usize> {
    s.find(':')
}

// Unrelated; lost together with the rest of the crate.
pub fn add_one(x: u32) -> u32 {
    x.wrapping_add(1)
}
```

<details><summary>Proposed patch (on top of the patches of the previous reports)</summary>

```diff
diff --git a/src/Translate.ml b/src/Translate.ml
index 52e846ba..c37a4782 100644
--- a/src/Translate.ml
+++ b/src/Translate.ml
@@ -366,6 +366,11 @@ let translate_crate_to_pure (crate : crate) (marked_ids : marked_ids) :
       (List.map (fun (d : Pure.global_decl) -> (d.def_id, d)) global_decls)
   in
 
+  (* The trait methods whose signature we failed to translate *)
+  let failed_method_sigs : (TraitDeclId.id * TraitMethodId.id) list ref =
+    ref []
+  in
+
   (* Compute the function signatures for the whole crate *)
   let fun_sigs =
     let fun_decl_sigs =
@@ -398,21 +403,43 @@ let translate_crate_to_pure (crate : crate) (marked_ids : marked_ids) :
     in
 
     let method_sigs =
+      (* Translating the signature of a trait method can fail (for instance:
+         signatures with trait-type constraints, generic associated types,
+         [dyn] types). As for the function declarations above, we catch the
+         error so that one method does not abort the translation of the whole
+         crate: the method is registered in [failed_method_sigs] and is later
+         left out of the trait declaration and of its implementations. *)
       let translate_method_sig (trait_decl : LlbcAst.trait_decl)
           (method_id : TraitMethodId.id)
           (bound_method : LlbcAst.trait_method Types.binder) =
-        let sg =
-          SymbolicToPureTypes.translate_flat_trait_method_sigs trans_ctx
-            trait_decl method_id bound_method
-        in
-        (FunOrMethodId.Method (trait_decl.def_id, method_id), sg)
+        try
+          let sg =
+            SymbolicToPureTypes.translate_flat_trait_method_sigs trans_ctx
+              trait_decl method_id bound_method
+          in
+          Some (FunOrMethodId.Method (trait_decl.def_id, method_id), sg)
+        with CFailure error ->
+          let name = name_to_string trans_ctx trait_decl.item_meta.name in
+          let method_name = bound_method.binder_value.name in
+          [%warn_opt_span] error.span
+            ("Could not translate the signature of the trait method '" ^ name
+           ^ "::" ^ method_name
+           ^ "' because of previous error. The method is ignored: it is left \
+              out of the translated trait declaration and of its \
+              implementations, and the functions which use it will fail to \
+              translate.\nDefinition span: "
+            ^ Errors.raw_span_to_string
+                bound_method.binder_value.item_meta.span);
+          failed_method_sigs :=
+            (trait_decl.def_id, method_id) :: !failed_method_sigs;
+          None
       in
       let translate_trait_methods (trait_decl : LlbcAst.trait_decl) =
         let methods =
           TraitDeclId.Map.find trait_decl.def_id
             trans_ctx.trait_methods_to_extract
         in
-        List.map
+        List.filter_map
           (fun (method_id, bound_method) ->
             translate_method_sig trait_decl method_id bound_method)
           (TraitMethodId.Map.to_list methods)
@@ -429,6 +456,26 @@ let translate_crate_to_pure (crate : crate) (marked_ids : marked_ids) :
       (FunOrMethodId.Map.bindings method_sigs @ fun_decl_sigs)
   in
 
+  (* Remove the methods whose signature we could not translate from the methods
+     to extract, so that the translation of the trait declarations and of the
+     trait implementations ignores them. *)
+  let trans_ctx =
+    if !failed_method_sigs = [] then trans_ctx
+    else
+      let trait_methods_to_extract =
+        TraitDeclId.Map.filter_map
+          (fun trait_decl_id methods ->
+            Some
+              (TraitMethodId.Map.filter
+                 (fun method_id _ ->
+                   not
+                     (List.mem (trait_decl_id, method_id) !failed_method_sigs))
+                 methods))
+          trans_ctx.trait_methods_to_extract
+      in
+      { trans_ctx with trait_methods_to_extract }
+  in
+
   (* Translate all the functions.
 
      Remark: [translate_function_to_pure] catches errors of type [CFailure]
@@ -560,13 +607,25 @@ let translate_crate_to_pure (crate : crate) (marked_ids : marked_ids) :
   in
 
   (* Translate the trait implementations *)
+  let translated_trait_decl_ids =
+    TraitDeclId.Set.of_list
+      (List.map (fun (d : Pure.trait_decl) -> d.def_id) trait_decls)
+  in
   let trait_impls =
     let num_decls = TraitImplId.Map.cardinal crate.trait_impls in
     ProgressBar.with_reporter num_decls "Translated trait impls: "
       (fun report ->
         List.filter_map
-          (fun d ->
+          (fun (d : LlbcAst.trait_impl) ->
             try
+              (* If we failed to translate the trait declaration, we can not
+                 extract its implementations: ignore them here (rather than
+                 failing with [Not_found] at extraction time, which aborts the
+                 whole crate). *)
+              [%cassert] d.item_meta.span
+                (TraitDeclId.Set.mem d.impl_trait.id translated_trait_decl_ids)
+                "Can not translate this trait implementation because the \
+                 translation of the corresponding trait declaration failed";
               let d = SymbolicToPure.translate_trait_impl trans_ctx d in
               report 1;
               Some d
diff --git a/src/symbolic/SymbolicToPure.ml b/src/symbolic/SymbolicToPure.ml
index 38ec2bba..7085fd1c 100644
--- a/src/symbolic/SymbolicToPure.ml
+++ b/src/symbolic/SymbolicToPure.ml
@@ -334,7 +334,18 @@ let translate_trait_impl (ctx : Contexts.decls_ctx) (trait_impl : A.trait_impl)
         ( method_id,
           name,
           translate_binder span (translate_fun_decl_ref span translate_ty) m ))
-      (TraitMethodId.Map.to_list methods)
+      (List.filter
+         (fun ((method_id, _) : TraitMethodId.id * _) ->
+           (* Ignore the methods which were removed from the methods to extract
+              (this happens when we fail to translate the signature of a trait
+              method: the method is then left out of the trait declaration). *)
+           match
+             TraitDeclId.Map.find_opt trait_impl.impl_trait.id
+               ctx.trait_methods_to_extract
+           with
+           | None -> true
+           | Some decl_methods -> TraitMethodId.Map.mem method_id decl_methods)
+         (TraitMethodId.Map.to_list methods))
   in
   (* Lookup the builtin information, if there is *)
   let builtin_info =
```

</details>
