## Per function (independent audit)

| function | fable | opus |
|---|---|---|
| stock_of | 2/2 done | 2/2 done |
| find_bin | 2/2 done | 2/2 done |
| restock | 2/2 done | 2/2 done |
| take | 3/3 done | 3/3 done |
| fill_orders | 3/3 done | 3/3 done |
| product_count | 2/2 done | 2/2 done |
| dominant_product | 2/2 done | 2/2 done |

 {
 "arm-fable": {
  "scenarios_proved": 16,
  "functions_done": 7,
  "kernel_replay_ok": 23,
  "kernel_replay_modules": 23,
  "axioms": [
   "Classical.choice",
   "Quot.sound",
   "propext"
  ]
 },
 "arm-opus": {
  "scenarios_proved": 16,
  "functions_done": 7,
  "kernel_replay_ok": 24,
  "kernel_replay_modules": 24,
  "axioms": [
   "Classical.choice",
   "Quot.sound",
   "propext"
  ]
 }
}

## Per scenario

| scenario | function | fable verdict | fable proof lines | fable lemmas reached (decls / lines) | opus verdict | opus proof lines | opus lemmas reached (decls / lines) |
|---|---|---|---|---|---|---|---|
| stock_is_sum | stock_of | PROVED-FOR-ALL | 7 | 9 / 58 | PROVED-FOR-ALL | 6 | 13 / 87 |
| stock_too_big | stock_of | PROVED-FOR-ALL | 7 | 9 / 58 | PROVED-FOR-ALL | 9 | 13 / 87 |
| find_first_bin | find_bin | PROVED-FOR-ALL | 14 | 2 / 37 | PROVED-FOR-ALL | 6 | 8 / 67 |
| find_no_bin | find_bin | PROVED-FOR-ALL | 9 | 2 / 37 | PROVED-FOR-ALL | 8 | 8 / 67 |
| restock_adds | restock | PROVED-FOR-ALL | 8 | 18 / 112 | PROVED-FOR-ALL | 10 | 11 / 103 |
| restock_counts | restock | PROVED-FOR-ALL | 3 | 15 / 94 | PROVED-FOR-ALL | 3 | 10 / 93 |
| take_amount | take | PROVED-FOR-ALL | 3 | 13 / 162 | PROVED-FOR-ALL | 3 | 13 / 125 |
| take_stock_down | take | PROVED-FOR-ALL | 7 | 14 / 176 | PROVED-FOR-ALL | 6 | 14 / 136 |
| take_earliest_first | take | PROVED-FOR-ALL | 3 | 13 / 162 | PROVED-FOR-ALL | 3 | 13 / 125 |
| fill_count | fill_orders | PROVED-FOR-ALL | 3 | 26 / 292 | PROVED-FOR-ALL | 3 | 25 / 271 |
| fill_state | fill_orders | PROVED-FOR-ALL | 3 | 26 / 292 | PROVED-FOR-ALL | 3 | 25 / 271 |
| fill_at_most | fill_orders | PROVED-FOR-ALL | 8 | 27 / 302 | PROVED-FOR-ALL | 6 | 26 / 278 |
| count_products | product_count | PROVED-FOR-ALL | 5 | 9 / 90 | PROVED-FOR-ALL | 5 | 10 / 110 |
| count_at_most_bins | product_count | PROVED-FOR-ALL | 6 | 9 / 90 | PROVED-FOR-ALL | 5 | 10 / 110 |
| dominant_found | dominant_product | PROVED-FOR-ALL | 11 | 7 / 128 | PROVED-FOR-ALL | 3 | 15 / 185 |
| dominant_none | dominant_product | PROVED-FOR-ALL | 18 | 7 / 128 | PROVED-FOR-ALL | 14 | 15 / 185 |

## Cost

| measure | fable | opus |
|---|---|---|
| attempts_proof | 27 | 16 |
| failed_proof | 14 | 8 |
| failed_real | 6 | 8 |
| failed_mixed | 4 | 0 |
| failed_probe | 4 | 0 |
| post_hoc_probe_attempts | 0 | 3 |
| minutes_first_to_last_proof_attempt | 14.1 | 10.3 |
| minutes_copy_to_last_proof_attempt | 15.4 | 14.0 |
| minutes_copy_to_final_report | 16.3 | 17.4 |
| build_seconds_proof | 201 | 120 |
| hand_written_lean | 783 | 766 |
| lemma_code_lines | 668 | 673 |
| lemma_boilerplate_lines | 41 | 51 |
| scenario_proof_lines | 115 | 93 |
| lean_per_rust_code_line | 6.12 | 5.98 |
| lean_per_rust_code_line_with_glossary | 6.72 | 6.59 |
| declarations | 61 | 48 |
| theorems | 54 | 46 |
| definitions | 7 | 2 |
| loop_lemmas | 10 | 9 |
| loop lemma: decls / statement / proof lines | 10 / 55 / 349 | 9 / 51 / 420 |
| function spec: decls / statement / proof lines | 8 / 25 / 48 | 8 / 28 / 53 |
| pure helper: decls / statement / proof lines | 33 / 68 / 97 | 16 / 30 / 35 |
| Aeneas/scalar helper: decls / statement / proof lines | 3 / 6 / 12 | 13 / 27 / 26 |
| definition: decls / statement / proof lines | 7 / 7 / 1 | 2 / 2 / 1 |

## Per function and kind of loop

| function | kind of loop | arm | Rust lines | loop lemmas: stmt + proof lines | spec | helpers (own) | helpers (shared) | scenario proofs | own total | own Lean/Rust | builds / FAILED | active min | increment min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stock_of | accumulation, early return on overflow | fable | 14 | 1: 4 + 22 | 6 | 2 | 24 | 14 | 48 | 3.4 | 5 / 1 (0 real, 0 mixed, 1 probe) | 1.3 | 2.7 |
|  |  | opus | 14 | 1: 5 + 37 | 7 | 0 | 38 | 15 | 64 | 4.6 | 4 / 2 (2 real, 0 mixed, 0 probe) | 0.9 | 4.6 |
| find_bin | search, early exit | fable | 10 | 1: 4 + 26 | 7 | 0 | 0 | 23 | 60 | 6.0 | 2 / 1 (1 real, 0 mixed, 0 probe) | 0.3 | 0.8 |
|  |  | opus | 10 | 1: 7 + 35 | 6 | 3 | 16 | 14 | 65 | 6.5 | 2 / 1 (1 real, 0 mixed, 0 probe) | 0.3 | 0.8 |
| restock | in-place update of every match | fable | 12 | 1: 6 + 41 | 8 | 42 | 15 | 11 | 108 | 9.0 | 8 / 7 (4 real, 3 mixed, 0 probe) | 2.9 | 3.7 |
|  |  | opus | 12 | 1: 7 + 52 | 6 | 12 | 26 | 13 | 90 | 7.5 | 2 / 1 (1 real, 0 mixed, 0 probe) | 0.3 | 1.4 |
| take | in-place update, two-part condition, early stop | fable | 14 | 1: 10 + 78 | 11 | 14 | 63 | 13 | 126 | 9.0 | 5 / 2 (1 real, 0 mixed, 1 probe) | 2.0 | 3.1 |
|  |  | opus | 14 | 1: 5 + 74 | 8 | 11 | 38 | 12 | 110 | 7.9 | 3 / 2 (2 real, 0 mixed, 0 probe) | 1.1 | 2.4 |
| fill_orders | loop calling two looping functions | fable | 19 | 1: 9 + 46 | 15 | 18 | 83 | 14 | 102 | 5.4 | 2 / 1 (0 real, 0 mixed, 1 probe) | 0.6 | 1.1 |
|  |  | opus | 19 | 1: 6 + 45 | 20 | 14 | 57 | 12 | 97 | 5.1 | 1 / 0 (0 real, 0 mixed, 0 probe) | 0.0 | 0.9 |
| product_count | nested loop | fable | 15 | 3: 12 + 52 | 3 | 19 | 4 | 11 | 97 | 6.5 | 2 / 1 (0 real, 1 mixed, 0 probe) | 0.7 | 1.1 |
|  |  | opus | 15 | 2: 11 + 70 | 4 | 6 | 19 | 10 | 101 | 6.7 | 3 / 2 (2 real, 0 mixed, 0 probe) | 0.6 | 2.2 |
| dominant_product | non-obvious invariant (two passes) | fable | 31 | 2: 10 + 84 | 23 | 0 | 11 | 29 | 146 | 4.7 | 3 / 1 (0 real, 0 mixed, 1 probe) | 1.7 | 2.9 |
|  |  | opus | 31 | 2: 10 + 107 | 30 | 9 | 29 | 17 | 173 | 5.6 | 1 / 0 (0 real, 0 mixed, 0 probe) | 0.0 | 1.6 |

## Mutants per function

| function mutated | mutants | shown false by a scenario | pipeline stopped | not shown false | fable: proofs lost per mutant (own + other) | opus: proofs lost per mutant (own + other) |
|---|---|---|---|---|---|---|
| stock_of | 9 | 8 | 1 | 0 | 5.0 + 9.0 | 5.0 + 5.0 |
| find_bin | 11 | 10 | 1 | 0 | 2.0 + 0.0 | 2.0 + 4.0 |
| restock | 10 | 9 | 1 | 0 | 2.0 + 2.0 | 2.0 + 2.0 |
| take | 21 | 17 | 2 | 2 | 6.0 + 0.5 | 6.0 + 2.4 |
| fill_orders (incl. can_fill) | 12 | 11 | 1 | 0 | 3.0 + 0.0 | 3.0 + 0.0 |
| product_count | 17 | 14 | 2 | 1 | 2.0 + 0.0 | 2.0 + 0.0 |
| dominant_product | 27 | 23 | 2 | 2 | 2.0 + 0.0 | 2.0 + 0.0 |

## Unit tests (cargo-mutants) against scenarios

| unit tests | scenarios | mutants |
|---|---|---|
| CaughtMutant | shown false | 92 |
| CaughtMutant | stopped | 1 |
| MissedMutant | not shown | 5 |
| Timeout | stopped | 9 |

## Strength of the evidence for shown-false mutants

| strongest evidence | mutants |
|---|---|
| kernel-checked refutation (REFUTED) | 17 |
| counterexample on the model, replayed on Rust | 75 |
| only an Examples row failing on Rust | 0 |

## Mutants

{
 "mutants": 107,
 "pipeline_stopped": 10,
 "shown_false": 92,
 "translate_failed": 0
}
{
 "arm-fable": {
  "only_lose_proof": 5,
  "all_proofs_kept": 0,
  "refuted_but_proof_kept": [],
  "kept_list": [],
  "only_lose_list": [
   38,
   42,
   71,
   88,
   89
  ],
  "collateral_proofs_lost_total": 111,
  "own_proofs_lost_total": 337
 },
 "arm-opus": {
  "only_lose_proof": 5,
  "all_proofs_kept": 0,
  "refuted_but_proof_kept": [],
  "kept_list": [],
  "only_lose_list": [
   38,
   42,
   71,
   88,
   89
  ],
  "collateral_proofs_lost_total": 159,
  "own_proofs_lost_total": 337
 }
}
| # | mutant | unit tests | shown false by | fable proofs lost | opus proofs lost |
|---|---|---|---|---|---|
| 0 | replace Warehouse::stock_of -> Option<u64> with None | CaughtMutant | fill_count,fill_state,stock_is_sum | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 1 | replace Warehouse::stock_of -> Option<u64> with Some(0) | CaughtMutant | fill_count,fill_state,stock_is_sum,stock_too_big | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 2 | replace Warehouse::stock_of -> Option<u64> with Some(1) | CaughtMutant | fill_count,fill_state,stock_is_sum,stock_too_big | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 3 | replace < with == in Warehouse::stock_of | CaughtMutant | fill_at_most,fill_count,fill_state,stock_is_sum,stock_too_big | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 4 | replace < with > in Warehouse::stock_of | CaughtMutant | fill_count,fill_state,stock_is_sum,stock_too_big | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 5 | replace < with <= in Warehouse::stock_of | CaughtMutant | fill_at_most,fill_count,fill_state,stock_is_sum | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 6 | replace == with != in Warehouse::stock_of | CaughtMutant | fill_count,fill_state,stock_is_sum,stock_too_big | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 7 | replace += with -= in Warehouse::stock_of | CaughtMutant | fill_at_most,fill_count,fill_state,stock_is_sum,stock_too_big | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 8 | replace += with *= in Warehouse::stock_of | Timeout | STOPPED | 14 (5 own, 9 other) | 10 (5 own, 5 other) |
| 9 | replace Warehouse::find_bin -> Option<usize> with None | CaughtMutant | find_first_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 10 | replace Warehouse::find_bin -> Option<usize> with Some(0) | CaughtMutant | find_first_bin,find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 11 | replace Warehouse::find_bin -> Option<usize> with Some(1) | CaughtMutant | find_first_bin,find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 12 | replace < with == in Warehouse::find_bin | CaughtMutant | find_first_bin,find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 13 | replace < with > in Warehouse::find_bin | CaughtMutant | find_first_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 14 | replace < with <= in Warehouse::find_bin | CaughtMutant | find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 15 | replace && with || in Warehouse::find_bin | CaughtMutant | find_first_bin,find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 16 | replace == with != in Warehouse::find_bin | CaughtMutant | find_first_bin,find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 17 | replace >= with < in Warehouse::find_bin | CaughtMutant | find_first_bin,find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 18 | replace += with -= in Warehouse::find_bin | CaughtMutant | find_first_bin,find_no_bin | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 19 | replace += with *= in Warehouse::find_bin | Timeout | STOPPED | 2 (2 own, 0 other) | 6 (2 own, 4 other) |
| 20 | replace Warehouse::restock -> usize with 0 | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 21 | replace Warehouse::restock -> usize with 1 | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 22 | replace < with == in Warehouse::restock | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 23 | replace < with > in Warehouse::restock | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 24 | replace < with <= in Warehouse::restock | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 25 | replace == with != in Warehouse::restock | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 26 | replace += with -= in Warehouse::restock | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 27 | replace += with *= in Warehouse::restock | CaughtMutant | restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 28 | replace += with -= in Warehouse::restock | CaughtMutant | restock_adds,restock_counts | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 29 | replace += with *= in Warehouse::restock | Timeout | STOPPED | 4 (2 own, 2 other) | 4 (2 own, 2 other) |
| 30 | replace Warehouse::take -> u64 with 0 | CaughtMutant | fill_count,fill_state,take_amount,take_earliest_first | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 31 | replace Warehouse::take -> u64 with 1 | CaughtMutant | fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 32 | replace && with || in Warehouse::take | CaughtMutant | take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 33 | replace < with == in Warehouse::take | CaughtMutant | fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 34 | replace < with > in Warehouse::take | CaughtMutant | fill_count,fill_state,take_amount,take_earliest_first | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 35 | replace < with <= in Warehouse::take | CaughtMutant | take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 36 | replace > with == in Warehouse::take | CaughtMutant | fill_count,fill_state,take_amount,take_earliest_first | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 37 | replace > with < in Warehouse::take | CaughtMutant | fill_count,fill_state,take_amount,take_earliest_first | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 38 | replace > with >= in Warehouse::take | MissedMutant | - | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 39 | replace == with != in Warehouse::take | CaughtMutant | fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 40 | replace < with == in Warehouse::take | CaughtMutant | fill_at_most,fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 41 | replace < with > in Warehouse::take | CaughtMutant | fill_at_most,fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 42 | replace < with <= in Warehouse::take | MissedMutant | - | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 43 | replace - with + in Warehouse::take | CaughtMutant | fill_at_most,fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 44 | replace - with / in Warehouse::take | CaughtMutant | STOPPED | 16 (6 own, 10 other) | 16 (6 own, 10 other) |
| 45 | replace -= with += in Warehouse::take | CaughtMutant | fill_at_most,fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 46 | replace -= with /= in Warehouse::take | CaughtMutant | fill_at_most,fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 47 | replace += with -= in Warehouse::take | CaughtMutant | fill_at_most,fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 48 | replace += with *= in Warehouse::take | Timeout | STOPPED | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 49 | replace - with + in Warehouse::take | CaughtMutant | take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 50 | replace - with / in Warehouse::take | CaughtMutant | fill_at_most,fill_count,fill_state,take_amount,take_earliest_first,take_stock_down | 6 (6 own, 0 other) | 8 (6 own, 2 other) |
| 51 | replace Warehouse::can_fill -> bool with true | CaughtMutant | fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 52 | replace Warehouse::can_fill -> bool with false | CaughtMutant | fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 53 | replace >= with < in Warehouse::can_fill | CaughtMutant | fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 54 | replace Warehouse::fill_orders -> usize with 0 | CaughtMutant | fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 55 | replace Warehouse::fill_orders -> usize with 1 | CaughtMutant | fill_at_most,fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 56 | replace < with == in Warehouse::fill_orders | CaughtMutant | fill_at_most,fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 57 | replace < with > in Warehouse::fill_orders | CaughtMutant | fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 58 | replace < with <= in Warehouse::fill_orders | CaughtMutant | fill_at_most,fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 59 | replace += with -= in Warehouse::fill_orders | CaughtMutant | fill_at_most,fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 60 | replace += with *= in Warehouse::fill_orders | CaughtMutant | fill_count | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 61 | replace += with -= in Warehouse::fill_orders | CaughtMutant | fill_at_most,fill_count,fill_state | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 62 | replace += with *= in Warehouse::fill_orders | Timeout | STOPPED | 3 (3 own, 0 other) | 3 (3 own, 0 other) |
| 63 | replace Warehouse::product_count -> usize with 0 | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 64 | replace Warehouse::product_count -> usize with 1 | CaughtMutant | count_at_most_bins,count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 65 | replace < with == in Warehouse::product_count | CaughtMutant | count_at_most_bins,count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 66 | replace < with > in Warehouse::product_count | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 67 | replace < with <= in Warehouse::product_count | CaughtMutant | count_at_most_bins,count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 68 | replace && with || in Warehouse::product_count | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 69 | replace < with == in Warehouse::product_count | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 70 | replace < with > in Warehouse::product_count | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 71 | replace < with <= in Warehouse::product_count | MissedMutant | - | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 72 | replace != with == in Warehouse::product_count | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 73 | replace += with -= in Warehouse::product_count | CaughtMutant | count_at_most_bins,count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 74 | replace += with *= in Warehouse::product_count | Timeout | STOPPED | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 75 | replace == with != in Warehouse::product_count | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 76 | replace += with -= in Warehouse::product_count | CaughtMutant | count_at_most_bins,count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 77 | replace += with *= in Warehouse::product_count | CaughtMutant | count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 78 | replace += with -= in Warehouse::product_count | CaughtMutant | count_at_most_bins,count_products | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 79 | replace += with *= in Warehouse::product_count | Timeout | STOPPED | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 80 | replace Warehouse::dominant_product -> Option<u32> with None | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 81 | replace Warehouse::dominant_product -> Option<u32> with Some(0) | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 82 | replace Warehouse::dominant_product -> Option<u32> with Some(1) | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 83 | replace < with == in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 84 | replace < with > in Warehouse::dominant_product | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 85 | replace < with <= in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 86 | replace == with != in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 87 | replace == with != in Warehouse::dominant_product | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 88 | replace += with -= in Warehouse::dominant_product | MissedMutant | - | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 89 | replace += with *= in Warehouse::dominant_product | MissedMutant | - | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 90 | replace -= with += in Warehouse::dominant_product | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 91 | replace -= with /= in Warehouse::dominant_product | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 92 | replace += with -= in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 93 | replace += with *= in Warehouse::dominant_product | Timeout | STOPPED | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 94 | replace < with == in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 95 | replace < with > in Warehouse::dominant_product | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 96 | replace < with <= in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 97 | replace == with != in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 98 | replace += with -= in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 99 | replace += with *= in Warehouse::dominant_product | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 100 | replace += with -= in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 101 | replace += with *= in Warehouse::dominant_product | Timeout | STOPPED | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 102 | replace > with == in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 103 | replace > with < in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 104 | replace > with >= in Warehouse::dominant_product | CaughtMutant | dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 105 | replace - with + in Warehouse::dominant_product | CaughtMutant | dominant_found | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
| 106 | replace - with / in Warehouse::dominant_product | CaughtMutant | dominant_found,dominant_none | 2 (2 own, 0 other) | 2 (2 own, 0 other) |
