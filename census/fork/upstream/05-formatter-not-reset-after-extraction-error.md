Title: Lean extraction: after an error in one definition the `Format` boxes stay open and every later definition is printed indented, then one token per line

When an exception is caught in the middle of the extraction of a definition (`CFailure`, in the per-declaration-group handler of `Translate.extract_definitions`), the `Format` boxes that were open at that point are never closed. Every later definition in the file is printed inside the unfinished one, so it starts indented. Each further error adds a level. Once the indentation reaches the margin, each token is put on its own line at the column of the `def` keyword, and Lean rejects the definition:

```
error: unexpected token '('; expected ':=', 'where' or '|'
```

Aeneas itself reports nothing: the file is "generated", and the definitions concerned were translated correctly.

Observed on two crates from crates.io, with the handlers of the previous report (exceptions other than `CFailure`) applied so that the runs complete:

- `time` 0.3.55: 1,437 of the 2,680 lines that start a top-level declaration are indented, by up to 34 columns. Lean still accepts the file, so here the defect is cosmetic.
- `cedar-policy-core` 4.14.1 (with 49 functions marked opaque to get past a rustc ICE under Charon): 12,874 of 15,309 such lines are indented, by up to 68 columns, and 178 of the crate's functions end in Lean parse errors.

I do not have a small single-file reproduction: it needs a crate with enough extraction errors (references to a declaration that failed to translate, for instance) to walk the indentation to the margin. Any crate where the log shows `Could not find: type name …` during extraction shows the drift in its output file.

Proposed fix (patch below, 14 lines): in the handler of `extract_definitions`, call `Format.pp_print_newline` (which closes every open box) and re-open the top-level vertical box that `extract_file` expects. With it, 1 of 2,831 declaration lines of `time` is indented (by 2 columns), the same functions compile as before, and the extraction tests (`make extract-tests`) give byte-identical output. I have not measured its effect on the number of `cedar-policy-core` functions that compile.

The patch is written on top of the handler change of the previous report; for the existing `CFailure` arm alone it is the same three lines.

**Versions.** Aeneas `0d21a9ec` (nightly-2026.11.10), built from source; Charon `454586e9` (0.1.315); Rust `nightly-2026-09-17`; macOS arm64. Seen only once the handlers of the previous report are in: the release binary aborts on both crates before it gets this far.

**Commands** for a single-file reproduction:

```
charon rustc --preset=aeneas --dest-file repro.llbc -- repro.rs --crate-name=repro --crate-type=rlib --edition=2021
aeneas -backend lean -dest out repro.llbc
```

<details><summary>Proposed patch (on top of the patches of the previous reports)</summary>

```diff
diff --git a/src/Translate.ml b/src/Translate.ml
index a54e05e8..ce698a77 100644
--- a/src/Translate.ml
+++ b/src/Translate.ml
@@ -1335,18 +1335,30 @@ let extract_definitions (fmt : Format.formatter) (config : gen_config)
           "Mixed-recursive declaration groups are not supported"
   in
 
+  (* When an exception interrupts the extraction of a definition, the
+     formatting boxes which were open at this point are never closed: all the
+     definitions which come after are then indented inside the unfinished one
+     and, past the margin, broken one token per line, which Lean does not parse
+     (the tokens of a signature must be to the right of the [def] keyword).
+     We close all the boxes, go to a new line and re-open the top-level
+     vertical box (the one opened in {!extract_file}). *)
+  let reset_formatter () =
+    Format.pp_print_newline fmt ();
+    Format.pp_open_vbox fmt 0
+  in
   List.iter
     (fun g ->
       try export_decl_group g with
       | CFailure _ ->
           (* An exception was raised: ignore it *)
-          ()
+          reset_formatter ()
       | exn when Errors.exn_is_recoverable exn ->
           (* An exception which is not a [CFailure] (for instance [Not_found]
              when looking up a declaration which we failed to translate):
              register an error and continue with the next declaration group,
              instead of losing the whole file. *)
-          ignore (Errors.save_uncaught_exn __FILE__ __LINE__ None exn))
+          ignore (Errors.save_uncaught_exn __FILE__ __LINE__ None exn);
+          reset_formatter ())
     (Option.get ctx.crate.declarations)
 
 type extract_file_info = {
```

</details>
