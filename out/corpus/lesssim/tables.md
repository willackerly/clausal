### Family: statements

| # | theorem | statement nodes: original → native | conclusion nodes | ∀ and ∃ binders in the conclusion | hypotheses | statement source lines |
|---|---|---|---|---|---|---|
| 1 | `weight_uniform_bound` | 131 → 107 | 83 → 59 | 2+1 → 0+0 | 2 → 2 | 4 → 2 |
| 2 | `flat_edge_uniform` | 239 → 219 | 169 → 149 | 2+1 → 0+0 | 3 → 3 | 6 → 3 |
| 3 | `FlatGeometry.uniform` | 247 → 227 | 167 → 147 | 2+1 → 0+0 | 2 → 2 | 4 → 4 |
| 4 | `UniformClass.edge_absorbed` | 627 → 863 (729 with projections) | 409 → 645 | 6+2 → 2+1 | 4 → 4 | 9 → 6 |
| 5 | `LocalSourceBounds.chart_bound` | 525 → 779 (645 with projections) | 427 → 681 | 7+2 → 2+1 | 1 → 1 | 8 → 6 |
| 6 | `commonChart_amplitude_bound` | 2323 → 3147 (2489 with projections) | 2081 → 2905 | 6+2 → 2+1 | 2 → 2 | 8 → 8 |
| 7 | `localStrippedClass_of_weighted` | 517 → 517 | 143 → 143 | 0+4 → 0+4 | 4 → 4 | 11 → 11 |
| 8 | `physical_sum_jet_bound_of_weighted` | 2341 → 2311 | 1767 → 1737 | 3+1 → 0+0 | 11 → 11 | 14 → 12 |
| 9 | `physical_vector_sum_jet_bound_of_weighted` | 3247 → 3217 | 2545 → 2515 | 3+1 → 0+0 | 11 → 11 | 16 → 15 |
| 10 | `WaveData.vector_bound` | 2739 → 2709 | 2589 → 2559 | 3+1 → 0+0 | 2 → 2 | 7 → 4 |
| 11 | `WaveData.vector_bound_with_gain` | 2799 → 2769 | 2535 → 2505 | 3+1 → 0+0 | 3 → 3 | 6 → 4 |
| 12 | `potentialIncrement_bound` | 3619 → 3589 | 2543 → 2513 | 3+1 → 0+0 | 8 → 8 | 12 → 11 |
| 13 | `CycleInputs.potential_bound` | 2887 → 2857 | 2577 → 2547 | 3+1 → 0+0 | 5 → 5 | 6 → 7 |
| | **total** | 22241 → 23311 (22385 with projections) | 18035 → 19105 | 43+19 → 6+7 | 58 → 58 | 111 → 93 |

Statement source tokens: 1515 → 1428.  Distinct subterms of the statements: 5044 → 5190.

### Family: proofs

| # | theorem | proof nodes: original → native | change | proof source lines | proof source tokens | outcome | laws used (Mathlib `Asymptotics.*`; library) |
|---|---|---|---|---|---|---|---|
| 1 | `weight_uniform_bound` | 321 → 356 | +35 (+11%) | 7 → 4 | 45 → 26 | native | IsBigO.trans; isBigO_of_le_on, mono_set |
| 2 | `flat_edge_uniform` | 728 → 575 | -153 (-21%) | 7 → 5 | 52 → 40 | native | –; congr_left_on |
| 3 | `FlatGeometry.uniform` | 504 → 404 | -100 (-20%) | 4 → 2 | 34 → 22 | native | –; comp_mapsTo, congr_left_on |
| 4 | `UniformClass.edge_absorbed` | 2953 → 2300 | -653 (-22%) | 18 → 11 | 179 → 147 | native | IsBigO.congr_right, IsBigO.mul, IsBigO.trans, isBigO_refl; comp_mapsTo, isBigO_of_le_on, uniformClass_isBigO |
| 5 | `LocalSourceBounds.chart_bound` | 3583 → 3027 | -556 (-16%) | 16 → 11 | 147 → 126 | native | IsBigO.congr_right, IsBigO.mul, IsBigO.pow, IsBigO.trans, isBigO_refl; isBigO_of_bound_on, mono_set |
| 6 | `commonChart_amplitude_bound` | 5475 → 6069 | +594 (+11%) | 36 → 34 | 344 → 381 | native | IsBigO.congr_right, IsBigO.smul, isBigO_refl; comp_mapsTo, congr_left_on, isBigO_of_bound_on, jet_comp |
| 7 | `localStrippedClass_of_weighted` | 2137 → 3039 | +902 (+42%) | 20 → 24 | 136 → 174 | escape hatch (statement kept) | –; exists_bound_on_le |
| 8 | `physical_sum_jet_bound_of_weighted` | 2618 → 2548 | -70 (-3%) | 10 → 6 | 75 → 72 | escape hatch (inside the proof) | –; isBigO_of_bound_on |
| 9 | `physical_vector_sum_jet_bound_of_weighted` | 1840 → 1055 | -785 (-43%) | 15 → 6 | 146 → 83 | native | IsBigO.fun_sum, IsBigO.norm_left, IsBigO.trans; isBigO_of_bound_on |
| 10 | `WaveData.vector_bound` | 1150 → 730 | -420 (-37%) | 4 → 3 | 38 → 27 | native | –; mono_set |
| 11 | `WaveData.vector_bound_with_gain` | 1951 → 1621 | -330 (-17%) | 6 → 3 | 37 → 19 | native | IsBigO.trans; isBigO_rpow_of_le |
| 12 | `potentialIncrement_bound` | 1922 → 2385 | +463 (+24%) | 23 → 22 | 216 → 247 | native | IsBigO.trans; isBigO_of_bound_on, isBigO_rpow_of_le, jet_add, mono_set |
| 13 | `CycleInputs.potential_bound` | 514 → 514 | +0 (+0%) | 5 → 5 | 44 → 44 | native | –; – |
| | **total** | 25696 → 24623 | -1073 (-4.2%) | 171 → 136 | 1493 → 1408 | | |

Proof source characters (leading whitespace stripped): 8555 → 8484.  Proof nodes without the leading binders (body only): 23833 → 22363.

### Library

| lemma | statement nodes | proof nodes | source lines (statement + proof) | family theorems using it |
|---|---|---|---|---|
| `isBigO_of_bound_on` | 105 | 219 | 1 + 2 | 5 |
| `exists_bound_on` | 171 | 364 | 2 + 4 | 0 |
| `isBigO_on_iff` | 173 | 447 | 2 + 1 | 0 |
| `mono_set` | 103 | 108 | 1 + 1 | 4 |
| `congr_on` | 117 | 132 | 1 + 1 | 0 |
| `congr_left_on` | 101 | 88 | 1 + 1 | 3 |
| `congr_right_on` | 101 | 88 | 1 + 1 | 0 |
| `comp_mapsTo` | 119 | 127 | 2 + 1 | 3 |
| `isBigO_of_le_on` | 107 | 123 | 1 + 1 | 2 |
| `exists_bound_on_finset` | 221 | 481 | 3 + 4 | 0 |
| `exists_bound_on_le` | 223 | 453 | 3 + 4 | 1 |
| `isBigO_rpow_of_le` | 153 | 245 | 2 + 3 | 2 |
| `jet_add` | 939 | 745 | 5 + 2 | 1 |
| `jet_comp` | 1317 | 3175 | 10 + 14 | 1 |
| `uniformClass_isBigO` | 763 | 1808 | 4 + 4 | 1 |
| **total (15)** | 4713 | 8603 | 39 + 44 | |

Library source tokens: 1273.

Equivalence proofs (not part of the library a native corpus would keep): 13 `Back` theorems 9643 proof nodes, 12 `Fwd` theorems 7563, 4 shape lemmas 2161; source lines 123.

Checks from Lean: `Back.X` type structurally equal to the original for 13 of 13; `Fwd.X` type equal to `Native.X` for 12 of 12; native proofs using an original family theorem: 0; `Back` proofs using one: 0.
Axioms over all new declarations: Classical.choice, Quot.sound, propext.

### Sample: measured rows

| theorem | statement nodes: original → native | proof nodes: original → native | proof source lines | proof source tokens |
|---|---|---|---|---|
| `correction_weighted_jets` | 1129 → 1119 | 1727 → 2087 (+21%) | 17 → 13 | 124 → 101 |
| `potential_physical_bound` | 3939 → 3909 | 1307 → 874 (-33%) | 7 → 5 | 58 → 42 |
| `exists_uniform_coefficient_bound` | 349 → 395 | 1194 → 2659 (+123%) | 24 → 24 | 210 → 229 |
| `uniform_multiplied_coeff_bound` | 387 → 407 | 583 → 893 (+53%) | 4 → 4 | 39 → 50 |
| `profile_comp_derivative_bound` (universe 0 only) | 1437 → 1627 | 4690 → 2404 (-49%) | 25 → 13 | 260 → 207 |
