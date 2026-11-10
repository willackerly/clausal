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

In the ten-crate census this takes `indexmap` from 378 to 475 of 630 functions that end as compiling Lean, `untrusted` from 11 to 20 of 26, `time` from 696 to 703 of 774 and `rust_decimal` from 213 to 217 of 242 (parameters named `str` next to the module `str`). Two single-file reproductions are given in full below (`capture_builtin_name.rs`, `capture_module_name.rs`). A check that would catch this class in CI: run `lake build` on the generated Lean of a few real crates, since Aeneas itself reports no error here.

**Versions.** Aeneas `0d21a9ec` (nightly-2026.11.10), built from source; Charon `454586e9` (0.1.315); Rust `nightly-2026-09-17`; macOS arm64. The release binary of nightly-2026.11.09 (`5a392f4b`) behaves the same.

**Commands** for a single-file reproduction:

```
charon rustc --preset=aeneas --dest-file repro.llbc -- repro.rs --crate-name=repro --crate-type=rlib --edition=2021
aeneas -backend lean -dest out repro.llbc
```

**Reproduction source.**

`capture_builtin_name.rs`:

```rust
// A user type whose last name component is the name of an Aeneas builtin type (`Slice`) and which holds that builtin.
// The generated Lean declares `structure names.Slice ... where bytes : Slice Std.U8`: inside the declaration `Slice`
// resolves to the structure being declared, and every function mentioning the type compiles only "using sorry".
pub mod names {
    pub struct Slice<'a> {
        pub bytes: &'a [u8],
    }
    impl<'a> Slice<'a> {
        pub fn len(&self) -> usize {
            self.bytes.len()
        }
    }
}
```

`capture_module_name.rs`:

```rust
// A parameter named like a module of the crate. The generated Lean contains `input.Input.get input`, which Lean
// elaborates as a field access on the parameter `input`.
pub mod input {
    pub struct Input {
        pub value: u32,
    }
    impl Input {
        pub fn get(&self) -> u32 {
            self.value
        }
    }
}
pub mod shadow {
    use crate::input;
    pub fn param_like_module(input: input::Input) -> u32 {
        input.get()
    }
}
```

<details><summary>Proposed patch (on top of the patches of the previous reports)</summary>

```diff
diff --git a/src/Translate.ml b/src/Translate.ml
index 0ba57265..a54e05e8 100644
--- a/src/Translate.ml
+++ b/src/Translate.ml
@@ -1553,7 +1553,38 @@ let extract_translated_crate (filename : string) (dest_dir : string)
   (* Initialize the names map by registering the keywords used in the
      language, as well as some primitive names ("u32", etc.).
      We insert the names of the local declarations later. *)
-  let names_maps = Extract.initialize_names_maps () in
+  let names_maps =
+    (* The last name component of all the type and trait declarations of the
+       crate itself: a builtin type whose short name is in this set gets
+       printed with its fully qualified name (see
+       {!ExtractBase.initialize_names_maps}).
+
+       We only consider the local declarations: [core::result::Result] is
+       used by most crates, and taking it into account would qualify
+       [Result] everywhere. *)
+    let last_ident (name : Types.name) : string option =
+      match List.rev name with
+      | PeIdent (s, _) :: _ -> Some s
+      | _ -> None
+    in
+    let add_name (set : Collections.StringSet.t) (meta : Types.item_meta) =
+      match last_ident meta.name with
+      | Some s when meta.is_local -> Collections.StringSet.add s set
+      | _ -> set
+    in
+    let shadowed_builtin_adts = Collections.StringSet.empty in
+    let shadowed_builtin_adts =
+      TypeDeclId.Map.fold
+        (fun _ (d : Types.type_decl) set -> add_name set d.item_meta)
+        crate.type_decls shadowed_builtin_adts
+    in
+    let shadowed_builtin_adts =
+      TraitDeclId.Map.fold
+        (fun _ (d : LlbcAst.trait_decl) set -> add_name set d.item_meta)
+        crate.trait_decls shadowed_builtin_adts
+    in
+    Extract.initialize_names_maps ~shadowed_builtin_adts ()
+  in
 
   (* We need to compute which functions are recursive, in order to know
    * whether we should generate a decrease clause or not. *)
diff --git a/src/extract/Extract.ml b/src/extract/Extract.ml
index 018541a6..26c51d90 100644
--- a/src/extract/Extract.ml
+++ b/src/extract/Extract.ml
@@ -56,7 +56,12 @@ let extract_fun_decl_register_names (ctx : extraction_ctx)
       in
       let f = def.f in
       let fun_id = (Pure.FunId f.def_id, f.loop_id) in
-      ctx_add f.item_meta.span (FunId (FromLlbc fun_id)) info.extract_name ctx
+      (* Lean: see the comments in {!initialize_names_maps} *)
+      let extract_name =
+        qualify_shadowed_builtin_name ctx.names_maps.shadowed_builtin_adts
+          info.extract_name
+      in
+      ctx_add f.item_meta.span (FunId (FromLlbc fun_id)) extract_name ctx
   | None ->
       (* Not builtin *)
       (* Register the decrease clauses, if necessary *)
diff --git a/src/extract/ExtractBase.ml b/src/extract/ExtractBase.ml
index fecf97ba..48bc1760 100644
--- a/src/extract/ExtractBase.ml
+++ b/src/extract/ExtractBase.ml
@@ -364,6 +364,21 @@ type names_maps = {
           dependently typed language, we might have an issue if the field of a
           record has, say, the name "u32", and another field of the same record
           refers to "u32" (for instance in its type). *)
+  name_heads : StringSet.t;
+      (** The first component of all the (non-local) names which contain a dot
+          (for instance, ["input"] for ["input.Input.into_value"]).
+
+          For Lean: if a local variable has the same name as the first component
+          of a declaration name, it captures the references to this declaration:
+          with a parameter [input] in scope, [input.Input.into_value x] is
+          elaborated as a field access on the parameter, not as a reference to
+          the global declaration. We thus forbid local names which are equal to
+          one of those components (see {!basename_to_unique}). *)
+  shadowed_builtin_adts : StringSet.t;
+      (** For Lean: the short names of the builtin types ([Slice], [Array]...)
+          which are also the last name component of a type or trait declared
+          by the crate. The builtin definitions whose name starts with one of
+          those are printed fully qualified (see {!initialize_names_maps}). *)
   adt_projectors : StringSet.t;
       (** For Lean, we store the set of fully qualifed field projectors to check
           if some names are shared between methods and fields. If this happens,
@@ -444,7 +459,12 @@ let names_maps_add (id_to_string : id -> string) (id : id)
       else nm.strict_names_map
     in
     let names_map = names_map_add id_to_string (id, span) name nm.names_map in
-    { nm with strict_names_map; names_map }
+    let name_heads =
+      match String.index_opt name '.' with
+      | Some i when i > 0 -> StringSet.add (String.sub name 0 i) nm.name_heads
+      | _ -> nm.name_heads
+    in
+    { nm with strict_names_map; names_map; name_heads }
 
 (** The [id_to_string] function to print nice debugging messages if there are
     collisions *)
@@ -1289,8 +1309,51 @@ let names_map_init () : names_map_init =
 
 (** Initialize names maps with a proper set of keywords/names coming from the
     target language/prover. *)
-let initialize_names_maps () : names_maps =
+(** Lean: if the first component of the name of a builtin definition of the
+    standard library ([Slice], [Slice.len], [Array.index_usize]...) is in
+    [shadowed], return the fully qualified name ([Aeneas.Std.Slice.len]).
+
+    See the comments in {!initialize_names_maps}. *)
+let qualify_shadowed_builtin_name (shadowed : StringSet.t) (name : string) :
+    string =
+  let head =
+    match String.index_opt name '.' with
+    | Some i -> String.sub name 0 i
+    | None -> name
+  in
+  if StringSet.mem head shadowed then "Aeneas.Std." ^ name else name
+
+let initialize_names_maps ?(shadowed_builtin_adts : StringSet.t = StringSet.empty)
+    () : names_maps =
   let init = names_map_init () in
+  (* Lean: the builtin types are printed with their short name ([Slice],
+     [Array], [Result]...) which is resolved through [open Aeneas.Std]. If the
+     crate declares a type or a trait whose last name component is the same
+     (for instance [indexmap::map::slice::Slice]), the short name resolves to
+     the user declaration in all the definitions which live in the same
+     namespace (including the declaration of the user type itself), and the
+     generated code does not type-check. In this case we print the builtin type
+     with its fully qualified name. *)
+  let init =
+    if backend () = Lean then
+      let qualify_ty ((id, name) : builtin_ty * string) =
+        match id with
+        | TFuel -> (id, name)
+        | _ -> (id, qualify_shadowed_builtin_name shadowed_builtin_adts name)
+      in
+      (* The functions defined in the namespace of a builtin type
+         ([Slice.update], [Array.index_usize]...) are captured in the same way *)
+      let qualify_fun ((id, name) : pure_builtin_fun_id * string) =
+        (id, qualify_shadowed_builtin_name shadowed_builtin_adts name)
+      in
+      {
+        init with
+        builtin_adts = List.map qualify_ty init.builtin_adts;
+        builtin_pure_functions =
+          List.map qualify_fun init.builtin_pure_functions;
+      }
+    else init
+  in
   let prefix = if backend () = Lean then "Std." else "" in
   let mk_int_name s = prefix ^ int_name s in
   let int_names = List.map mk_int_name T.all_int_types in
@@ -1325,6 +1388,9 @@ let initialize_names_maps () : names_maps =
       names_map;
       unsafe_names_map;
       strict_names_map;
+      name_heads = StringSet.empty;
+      shadowed_builtin_adts =
+        (if backend () = Lean then shadowed_builtin_adts else StringSet.empty);
       adt_projectors = StringSet.empty;
     }
   in
@@ -2122,6 +2188,9 @@ let basename_to_unique (ctx : extraction_ctx) (name : string) =
        the backend allows such collisions *)
     StringSet.mem s ctx.names_maps.names_map.names_set
     || StringSet.mem s ctx.names_maps.strict_names_map.names_set
+    (* Lean: a local name must not capture the first component of a
+       declaration name (see the comments for [name_heads]) *)
+    || (backend () = Lean && StringSet.mem s ctx.names_maps.name_heads)
   in
   basename_to_unique_aux collision name_append_index name
 
```

</details>
