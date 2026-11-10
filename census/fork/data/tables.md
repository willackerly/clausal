### As shipped (one Charon run, one Aeneas run, nothing removed): functions and code lines that end as compiling Lean

| crate | functions counted | unpatched (source build of 0d21a9ec) | + (i) FunsAnalysis recursion | + (ii) trait method signature guard | + (iii) per-function exception catching | + (iv) Lean name capture | + (v) formatter reset after an extraction error (extra) |
|:--|--:|--:|--:|--:|--:|--:|--:|
| cedar-policy-core | 2503 | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) |
| rust_decimal | 242 | 0 (0%) | 0 (0%) | 213 (88%) | 213 (88%) | 217 (90%) | 217 (90%) |
| semver | 80 | 0 (0%) | 0 (0%) | 54 (68%) | 54 (68%) | 54 (68%) | 54 (68%) |
| shlex | 34 | 22 (65%) | 22 (65%) | 22 (65%) | 22 (65%) | 22 (65%) | 22 (65%) |
| rusty-money | 60 | 0 (0%) | 0 (0%) | 27 (45%) | 27 (45%) | 27 (45%) | 27 (45%) |
| indexmap | 630 | 0 (0%) | 0 (0%) | 378 (60%) | 378 (60%) | 475 (75%) | 475 (75%) |
| untrusted | 26 | 11 (42%) | 11 (42%) | 11 (42%) | 11 (42%) | 20 (77%) | 20 (77%) |
| fnv | 4 | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) |
| time | 774 | 0 (0%) | 0 (0%) | 696 (90%) | 696 (90%) | 703 (91%) | 703 (91%) |
| zeroize | 32 | 27 (84%) | 27 (84%) | 27 (84%) | 27 (84%) | 27 (84%) | 27 (84%) |
| **all ten** | 4385 | **64 (1%)** | **64 (1%)** | **1432 (33%)** | **1432 (33%)** | **1549 (35%)** | **1549 (35%)** |

| crate | code lines counted | unpatched (source build of 0d21a9ec) | + (i) FunsAnalysis recursion | + (ii) trait method signature guard | + (iii) per-function exception catching | + (iv) Lean name capture | + (v) formatter reset after an extraction error (extra) |
|:--|--:|--:|--:|--:|--:|--:|--:|
| cedar-policy-core | 30301 | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) |
| rust_decimal | 3744 | 0 (0%) | 0 (0%) | 2378 (64%) | 2378 (64%) | 2404 (64%) | 2404 (64%) |
| semver | 989 | 0 (0%) | 0 (0%) | 475 (48%) | 475 (48%) | 475 (48%) | 475 (48%) |
| shlex | 310 | 156 (50%) | 156 (50%) | 156 (50%) | 156 (50%) | 156 (50%) | 156 (50%) |
| rusty-money | 589 | 0 (0%) | 0 (0%) | 163 (28%) | 163 (28%) | 163 (28%) | 163 (28%) |
| indexmap | 3486 | 0 (0%) | 0 (0%) | 2090 (60%) | 2090 (60%) | 2570 (74%) | 2570 (74%) |
| untrusted | 133 | 43 (32%) | 43 (32%) | 43 (32%) | 43 (32%) | 75 (56%) | 75 (56%) |
| fnv | 17 | 17 (100%) | 17 (100%) | 17 (100%) | 17 (100%) | 17 (100%) | 17 (100%) |
| time | 5097 | 0 (0%) | 0 (0%) | 4346 (85%) | 4346 (85%) | 4386 (86%) | 4386 (86%) |
| zeroize | 160 | 91 (57%) | 91 (57%) | 91 (57%) | 91 (57%) | 91 (57%) | 91 (57%) |
| **all ten** | 44826 | **307 (1%)** | **307 (1%)** | **9759 (22%)** | **9759 (22%)** | **10337 (23%)** | **10337 (23%)** |

### The same, nine crates without cedar

| crate | functions counted | unpatched (source build of 0d21a9ec) | + (i) FunsAnalysis recursion | + (ii) trait method signature guard | + (iii) per-function exception catching | + (iv) Lean name capture | + (v) formatter reset after an extraction error (extra) |
|:--|--:|--:|--:|--:|--:|--:|--:|
| rust_decimal | 242 | 0 (0%) | 0 (0%) | 213 (88%) | 213 (88%) | 217 (90%) | 217 (90%) |
| semver | 80 | 0 (0%) | 0 (0%) | 54 (68%) | 54 (68%) | 54 (68%) | 54 (68%) |
| shlex | 34 | 22 (65%) | 22 (65%) | 22 (65%) | 22 (65%) | 22 (65%) | 22 (65%) |
| rusty-money | 60 | 0 (0%) | 0 (0%) | 27 (45%) | 27 (45%) | 27 (45%) | 27 (45%) |
| indexmap | 630 | 0 (0%) | 0 (0%) | 378 (60%) | 378 (60%) | 475 (75%) | 475 (75%) |
| untrusted | 26 | 11 (42%) | 11 (42%) | 11 (42%) | 11 (42%) | 20 (77%) | 20 (77%) |
| fnv | 4 | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) |
| time | 774 | 0 (0%) | 0 (0%) | 696 (90%) | 696 (90%) | 703 (91%) | 703 (91%) |
| zeroize | 32 | 27 (84%) | 27 (84%) | 27 (84%) | 27 (84%) | 27 (84%) | 27 (84%) |
| **nine crates** | 1882 | **64 (3%)** | **64 (3%)** | **1432 (76%)** | **1432 (76%)** | **1549 (82%)** | **1549 (82%)** |

| crate | code lines counted | unpatched (source build of 0d21a9ec) | + (i) FunsAnalysis recursion | + (ii) trait method signature guard | + (iii) per-function exception catching | + (iv) Lean name capture | + (v) formatter reset after an extraction error (extra) |
|:--|--:|--:|--:|--:|--:|--:|--:|
| rust_decimal | 3744 | 0 (0%) | 0 (0%) | 2378 (64%) | 2378 (64%) | 2404 (64%) | 2404 (64%) |
| semver | 989 | 0 (0%) | 0 (0%) | 475 (48%) | 475 (48%) | 475 (48%) | 475 (48%) |
| shlex | 310 | 156 (50%) | 156 (50%) | 156 (50%) | 156 (50%) | 156 (50%) | 156 (50%) |
| rusty-money | 589 | 0 (0%) | 0 (0%) | 163 (28%) | 163 (28%) | 163 (28%) | 163 (28%) |
| indexmap | 3486 | 0 (0%) | 0 (0%) | 2090 (60%) | 2090 (60%) | 2570 (74%) | 2570 (74%) |
| untrusted | 133 | 43 (32%) | 43 (32%) | 43 (32%) | 43 (32%) | 75 (56%) | 75 (56%) |
| fnv | 17 | 17 (100%) | 17 (100%) | 17 (100%) | 17 (100%) | 17 (100%) | 17 (100%) |
| time | 5097 | 0 (0%) | 0 (0%) | 4346 (85%) | 4346 (85%) | 4386 (86%) | 4386 (86%) |
| zeroize | 160 | 91 (57%) | 91 (57%) | 91 (57%) | 91 (57%) | 91 (57%) | 91 (57%) |
| **nine crates** | 14525 | **307 (2%)** | **307 (2%)** | **9759 (67%)** | **9759 (67%)** | **10337 (71%)** | **10337 (71%)** |

### cedar-policy-core with the Charon-side workarounds only (49 functions opaque for the rustc ICE, two generated parsers opaque), nothing removed on the Aeneas side

| crate | functions counted | unpatched (source build of 0d21a9ec) | + (i) FunsAnalysis recursion | + (iii) per-function exception catching | + (iv) Lean name capture | + (v) formatter reset after an extraction error (extra) |
|:--|--:|--:|--:|--:|--:|--:|
| cedar-policy-core | 2503 | 0 (0%) | 0 (0%) | did not finish | 996 (40%) | did not finish |

| crate | code lines counted | unpatched (source build of 0d21a9ec) | + (i) FunsAnalysis recursion | + (iii) per-function exception catching | + (iv) Lean name capture | + (v) formatter reset after an extraction error (extra) |
|:--|--:|--:|--:|--:|--:|--:|
| cedar-policy-core | 30301 | 0 (0%) | 0 (0%) | did not finish | 6269 (21%) | did not finish |
