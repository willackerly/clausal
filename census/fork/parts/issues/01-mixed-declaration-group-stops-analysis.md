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

{{REPRO:mixed_group.rs}}
{{PATCH:0001}}
