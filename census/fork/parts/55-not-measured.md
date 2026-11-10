### Not measured: cedar with (i)-(iii) joined, and cedar with patch (v)

Two cedar runs in this mode were started and **did not finish; they are not measured**, and they were not rerun.

| run | started | stopped | wall clock | state when stopped |
|:--|:--|:--|--:|:--|
| (i)-(iii), joined (`run_variant.sh p3 cw`) | 11:28 | killed 17:56 | 6 h 27 min | {{U_P3_ERR}} errors logged, still translating function bodies, no Lean file written |
| (i)-(v) (`run_variant.sh p5 cw`) | 11:34 | killed 17:56 | 6 h 19 min | {{U_P5_ERR}} errors logged, still translating function bodies, no Lean file written |

- **What happened.** The two runs were started together on the loaded machine, the agent that started them was cut off, and the orchestrator killed both after more than six hours. The system power log (`pmset -g log`) shows the machine asleep with the lid closed from 11:43 to 17:55, so the runs had about 15 and 9 minutes of running time before the sleep. They are unfinished runs, not evidence that Aeneas hangs: the same binary as (i)-(iii) completed on the same LLBC in 73 minutes earlier in the day, and (i)-(iv) in 79 minutes.
- **What is known without them.**
  - (i)-(iii) on cedar: the direct run in the table (completes, {{D_ERR}} errors, {{D_LINES}} lines of Lean), not joined per function and not compiled.
  - (i)-(iv) on cedar: the one joined and compiled measurement, {{P4CW_OK}} of 2503 functions.
  - Patch (v), away from cedar: on `time` as shipped, {{V_T4_IND}} of {{V_T4_N}} lines that start a top-level declaration are indented without (v) (by up to {{V_T4_MAX}} columns) and {{V_T5_IND}} of {{V_T5_N}} with it; the same 703 functions compile either way. In the cedar output of (i)-(iv), {{V_C_IND}} of {{V_C_N}} such lines are indented, by up to {{V_C_MAX}} columns.
- **What is not known.** How many of the {{SYNTAX_P4}} cedar functions that end in a Lean parse error with (i)-(iv) compile with (v). No figure for it appears anywhere in this report.
- **What a bounded rerun needs.** One run at a time (each loads a 1.0 GB LLBC); a machine that stays awake (mains power, `caffeinate`) and is otherwise quiet; a hard time limit, 3 hours being a little over twice the slowest completed run; about 2 GB of disk under `runs/` per variant. `summarise.py` marks a killed or timed-out run "did not finish" and leaves it out of every count.

```
source census/fork/env.sh
caffeinate -is timeout -k 60 3h census/fork/scripts/run_variant.sh p5 cw
caffeinate -is timeout -k 60 3h census/fork/scripts/run_variant.sh p3 cw
python3 census/fork/scripts/summarise.py && python3 census/fork/scripts/build_fork_md.py
```

The evidence for this section is in `data/cedar_cw_unfinished.json`.
