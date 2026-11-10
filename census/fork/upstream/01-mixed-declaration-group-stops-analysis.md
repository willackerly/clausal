Title: `FunsAnalysis.analyze_decl_groups` stops at the first mixed declaration group; all functions after it fail

When a crate contains a declaration group that mixes functions with trait impls (for example two types whose `Display` impls format each other), Aeneas reports

```
[Error] Mixed declaration groups (which contain both type and function declarations or functions and traits, for instance) are not supported yet: [7, 25, 8, 26]
```

and then every function that comes *after* that group in the declaration order fails, whatever it contains:

```
[Error] Internal error: please file an issue
Source: 'mixed_group.rs', lines 55:0-57:1
Compiler source: symbolic/SymbolicToPureTypes.ml, line 724
[Warn ] Could not translate the function signature of 'mixed_group::unrelated_b because of previous error
```

Cause: in `src/llbc/FunsAnalysis.ml`, `analyze_decl_groups` recurses on the remaining groups in every case except `MixedGroup`, where it saves the error and returns. The functions after the group have no entry in the analysis result, and `compute_raw_fun_effect_info` fails for each of them.

Reproduction (`mixed_group.rs`, 69 lines, in full below): two types `Term`/`Group` whose `Display` impls format each other, and three unrelated one-line functions declared after them. With the release binary 13 errors are logged, 10 of them "Internal error"; `unrelated_b`, `Wrapper::get` and `unrelated_c` are missing from the generated Lean file although they have nothing to do with the group.

Proposed fix (one line): recurse after the error.

```diff
-    | MixedGroup ids :: _ ->
+    | MixedGroup ids :: decls' ->
         [%save_error_opt_span] None
           ("Mixed declaration groups ... are not supported yet: [" ^ ... ^ "]");
+        analyze_decl_groups decls'
```

With it the reproduction logs 7 errors, all about the two `fmt` functions of the group, and `unrelated_b`, `Wrapper.get` and `unrelated_c` are emitted. On a larger crate (`cedar-policy-core` 4.14.1, 85 such groups, the first one early in the order) the "Internal error" raised at `SymbolicToPureTypes.ml`, line 724 goes from 8,632 occurrences in the log to 874: what remains is the members of the groups and the functions that call into them. The extraction tests (`make extract-tests`) give byte-identical output. Supporting mixed groups themselves is a separate matter; this only stops one group from taking the rest of the crate with it.

**Versions.** Aeneas `0d21a9ec` (nightly-2026.11.10), built from source; Charon `454586e9` (0.1.315); Rust `nightly-2026-09-17`; macOS arm64. The release binary of nightly-2026.11.09 (`5a392f4b`) behaves the same.

**Commands** for a single-file reproduction:

```
charon rustc --preset=aeneas --dest-file repro.llbc -- repro.rs --crate-name=repro --crate-type=rlib --edition=2021
aeneas -backend lean -dest out repro.llbc
```

**Reproduction source.**

`mixed_group.rs`:

```rust
// Reproduction of "one mixed declaration group makes every later function fail".
// Two types whose `Display` impls format each other (`Term`, `Group`) put trait impls and functions
// in one declaration group. Aeneas's function analysis stops at that group, and the functions
// declared after it (`unrelated_b`, `Wrapper::get`, `unrelated_c`) fail with "Internal error"
// although they have nothing to do with it.
#![allow(dead_code)]

use core::fmt;

pub enum Expr {
    Lit(u32),
    Neg(Box<Expr>),
}

pub fn unrelated_a(x: u32) -> u32 {
    x.wrapping_add(1)
}

/// The recursion goes through the trait (`{}` on a child of the same type).
impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Expr::Lit(n) => write!(f, "{}", n),
            Expr::Neg(e) => write!(f, "-{}", e),
        }
    }
}

/// Two types whose `Display` impls use each other.
pub enum Term {
    Num(u32),
    Paren(Box<Group>),
}

pub struct Group {
    pub inner: Term,
}

impl fmt::Display for Term {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Term::Num(n) => write!(f, "{}", n),
            Term::Paren(g) => write!(f, "({})", g),
        }
    }
}

impl fmt::Display for Group {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}]", self.inner)
    }
}

pub fn unrelated_b(x: u32) -> u32 {
    x.wrapping_mul(3)
}

pub struct Wrapper(pub u32);

impl Wrapper {
    pub fn get(&self) -> u32 {
        self.0
    }
}

pub fn unrelated_c(w: &Wrapper) -> u32 {
    w.get().wrapping_sub(1)
}
```

<details><summary>Proposed patch (on top of Aeneas `0d21a9ec`)</summary>

```diff
diff --git a/src/llbc/FunsAnalysis.ml b/src/llbc/FunsAnalysis.ml
index 850d9643..11f4b9b6 100644
--- a/src/llbc/FunsAnalysis.ml
+++ b/src/llbc/FunsAnalysis.ml
@@ -295,7 +295,7 @@ let analyze_module (m : crate) (funs_map : fun_decl FunDeclId.Map.t) :
                declaration group:\n" ^ decls ^ "\n\nInitial error:\n"
             ^ error.msg));
         analyze_decl_groups decls'
-    | MixedGroup ids :: _ ->
+    | MixedGroup ids :: decls' ->
         [%save_error_opt_span] None
           ("Mixed declaration groups (which contain both type and function \
             declarations or functions and traits, for instance) are not \
@@ -303,7 +303,11 @@ let analyze_module (m : crate) (funs_map : fun_decl FunDeclId.Map.t) :
           ^ String.concat ", "
               (List.map Charon.Print.item_id_to_string
                  (Charon.GAstUtils.g_declaration_group_to_list ids))
-          ^ "]")
+          ^ "]");
+        (* Do not stop here: the functions of this group get no analysis
+           information (and fail later, one by one), but the groups which come
+           after it in the declaration order must still be analyzed. *)
+        analyze_decl_groups decls'
   in
 
   analyze_decl_groups (Option.get m.declarations);
```

</details>
