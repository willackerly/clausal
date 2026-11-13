# Review sheet: the core Clausebook

Generated from `clausebook/core.yaml` by `clausebook/review_sheet.py`. One row per entry.

**What reviewing an entry means.** Read "How it is written" as an ordinary reader would, read "What the tool takes it to mean", and decide whether they are the same claim. The Lean column is what is actually proved; the definitions are in `lean/Frames/Core.lean` and `lean/Frames/Frames.lean`. `python3 -m clausal show "<a sentence using the entry>"` prints which calls a sentence covers and an allowed and a forbidden case.

**To record your review of one entry** (run from `clausal/`; the id is in the first column):

    python3 -m clausal attest <id> --act reviewed --as human:<your-id> --name "<Your Name>" --scope "read the form, the echo and the Lean definition"

A record is tied to the entry's text as it is now; if the entry changes, the record is void. A model's record never counts as a person's. Entries you doubt: do not attest; note the id and why.

## Frames (26)

The logical shapes a rule can have. Start here: these carry the most meaning.

| id | How it is written | What the tool takes it to mean | Lean |
|---|---|---|---|
| `always_answers` | always answers *(in a Rule)*<br>it answers *(in a Then step)* | the call gives an answer | `Frames.AlwaysAnswers {op}` |
| `never_changes` | never changes {m:measure<T>} *(in a Rule)*<br>{m:measure<T>} is unchanged *(in a Then step)* | {m} after the call equals {m} before it<br>*defaults: D3* | `Frames.NeverChanges {op} {m}` |
| `changes_only` | of {c:parts<T>}, only {x:term<T>} and {y:term<T>} change *(in a Then step)* | {c} are the same after the call, and every one of them other than {xs} has the {part} it had before<br>*defaults: D3* | `Frames.ChangesOnly {op} {c} {xs}` |
| `always` | is always accepted *(in a Rule)*<br>{c:class} *(in a Then step)* | {c} | `Frames.Always {op} {c}` |
| `never` | is always rejected *(in a Rule)* | it is NOT the case that {c} | `Frames.Never {op} {c}` |
| `if_then` | is accepted whenever {k:cond} *(in a Rule)* | if {k}, then {c} (and the call gives an answer whether or not {k}) | `Frames.IfThen {op} {k} {c}` |
| `only_if` | is accepted only if {k:cond} *(in a Rule)* | {c} only if {k} | `Frames.OnlyIf {op} {c} {k}` |
| `exactly_when` | is accepted exactly when {k:cond} *(in a Rule)* | {c} if and only if {k} | `Frames.ExactlyWhen {op} {c} {k}` |
| `rejected_unchanged` | is rejected and changes nothing *(in a Rule)*<br>it is rejected and changes nothing *(in a Then step)* | the answer is a rejection, and the whole state after the call is the state before it<br>*defaults: D3* | `Frames.RejectedUnchanged {op}` |
| `increases_by` | increases {m:measure<num>} by exactly {t:term<num>} *(in a Rule)*<br>{m:measure<num>} is increased by exactly {t:term<num>} *(in a Then step)* | {m} after the call equals {m} before it plus {t}, exactly<br>*defaults: D3* | `Frames.IncreasesBy {op} {m} {t}` |
| `decreases_by` | decreases {m:measure<num>} by exactly {t:term<num>} *(in a Rule)*<br>{m:measure<num>} is decreased by exactly {t:term<num>} *(in a Then step)* | {m} after the call, plus {t}, equals {m} before it, exactly<br>*defaults: D3* | `Frames.DecreasesBy {op} {m} {t}` |
| `becomes` | {m:measure<T>} is now {t:term<T>} *(in a Then step)* | {m} after the call is {t} | `Frames.Becomes {op} {m} {t}` |
| `result_is` | {a:ameasure<T>} is {t:term<T>} *(in a Then step)* | {a} is {t} | `Frames.ResultIs {op} {a} {t}` |
| `result_at_most` | {a:ameasure<num>} is at most {t:term<num>} *(in a Then step)* | {a} is at most {t} | `Frames.ResultAtMost {op} {a} {t}` |
| `result_at_least` | {a:ameasure<num>} is at least {t:term<num>} *(in a Then step)* | {a} is at least {t} | `Frames.ResultAtLeast {op} {a} {t}` |
| `at_most` | never leaves {m:measure<num>} above {t:term<num>} *(in a Rule)*<br>{m:measure<num>} is afterwards at most {t:term<num>} *(in a Then step)* | {m} after the call is at most {t} | `Frames.AtMost {op} {m} {t}` |
| `at_least` | never leaves {m:measure<num>} below {t:term<num>} *(in a Rule)*<br>{m:measure<num>} is afterwards at least {t:term<num>} *(in a Then step)* | {m} after the call is at least {t} | `Frames.AtLeast {op} {m} {t}` |
| `every_of` | every {c:acoll<T>} {p:itempred<T>} afterwards *(in a Then step)* | every {c} {p}, judged on the state after the call<br>*defaults: D7* | `Frames.EveryOf {op} {c} {p}` |
| `none_of` | no {c:acoll<T>} {p:itempred<T>} afterwards *(in a Then step)* | no {c} {p}, judged on the state after the call<br>*defaults: D7* | `Frames.NoneOf {op} {c} {p}` |
| `monotone` | never loses acceptance when {v:variation} *(in a Rule)*<br>never loses that {c:class} when {v:variation} *(in a Rule)* | whenever {v}, and for the first call {c}, then for the second call too {c}<br>*defaults: D10* | `Frames.Monotone {op} {v} {c}` |
| `agrees_with` | agrees with {r:reference} *(in a Rule)* | the answer and the state after the call are exactly what {r} gives for the state before and the input | `Frames.AgreesWith {op} {r}` |
| `same_answer` | gives the same answer when {v:variation} *(in a Rule)* | whenever {v}, the two calls give the same answer<br>*defaults: D10* | `Frames.IndependentOf {op} {v} (fun ans _ => ans)` |
| `within` | every {c:acoll<T>} is a {d:coll<T>} *(in a Then step)* | every {c} is a {d} (the first is read off the answer, the second off the input before the call) | `Frames.Within {op} {c} {d}` |
| `covers` | every {d:coll<T>} is a {c:acoll<T>} *(in a Then step)* | every {d} is a {c} (the first is read off the input before the call, the second off the answer) | `Frames.Covers {op} {c} {d}` |
| `same_answer_if` | gives the same answer when {v:variation}, if {c:class@first} *(in a Rule)* | whenever {v}, and for the first call {c}, the two calls give the same answer<br>*defaults: D10* | `Frames.IndependentGiven {op} {v} {c} (fun ans _ => ans)` |
| `each_at_most` | each of {ns:nums} is afterwards at most {t:term<num>} *(in a Then step)* | every one of {ns} after the call is at most {t} | `Frames.EachAtMost {op} {ns} {t}` |

## Modifiers (26)

Words that narrow, combine or compare.

| id | How it is written | What the tool takes it to mean | Lean |
|---|---|---|---|
| `zero` | zero | 0 | `0` |
| `is` | {m:measure<T>} is {t:term<T>} | {m} is {t} | `{m} = {t}` |
| `not_more_than` | {t:term<num>} is at most {m:measure<num>} | {t} is at most {m} | `{t} ≤ {m}` |
| `more_than` | {t:term<num>} is more than {m:measure<num>} | {t} is strictly more than {m} | `{m} < {t}` |
| `exceeds` | {m:measure<num>} is more than {t:term<num>} | {m} is strictly more than {t} | `{t} < {m}` |
| `at_most_value` | {m:measure<num>} is at most {t:term<num>} | {m} is at most {t} | `{m} ≤ {t}` |
| `sum_within` | {m:measure<num>} plus {t:term<num>} is at most {z:term<num>} | {m} plus {t} is at most {z} | `{m} + {t} ≤ {z}` |
| `sum_exceeds` | {m:measure<num>} plus {t:term<num>} exceeds {z:term<num>} | {m} plus {t} is strictly more than {z} | `{z} < {m} + {t}` |
| `equals` | {a:term<T>} equals {b:term<T>}<br>{a:term<T>} differs from {b:term<T>} *(negated)* | {a} is the same value as {b} | `{a} = {b}` |
| `not` |  | it is NOT the case that {p} | `¬ ({p})` |
| `aggregate` | the total of {ns:nums} | the sum of {ns} | `Frames.aggregate ({ns})` |
| `all_of` | all {pm:per_actor} | {pm} | `[{pm}]` |
| `holds_of` | {i:item<T>} {p:itempred<T>} | {i} {p} | `{p}` |
| `every` | every {c:coll<T>} {p:itempred<T>} | every {c} {p} | `Frames.every ({c}) (fun x => {p})` |
| `the_first` | the first {c:coll<T>} {p:itempred<T>} | there is a first {c}, and it {p}<br>*defaults: D6* | `Frames.theFirst ({c}) (fun x => {p})` |
| `no_such` | no {c:coll<T>} {p:itempred<T>} | no {c} {p} | `Frames.noneOf ({c}) (fun x => {p})` |
| `some_of` | some {c:coll<T>} {p:itempred<T>} | at least one {c} {p} | `Frames.someOf ({c}) (fun x => {p})` |
| `given` | {op} for which {c:cond} *(on the subject)* | assuming {c} | `({op}).given (fun st inp => {c})` |
| `rejected` | if it is rejected, {claim} *(as a claim)*<br>rejected {op} *(on the subject)* | rejected calls only | `({op}).rejected` |
| `successful` | if it is accepted, {claim} *(as a claim)*<br>accepted {op} *(on the subject)* | accepted calls only | `({op}).successful` |
| `internal` | internal {op} *(on the subject)* | every party the input names is a member of the state | `({op}).internal {member} {parties}` |
| `and_then` | {op} followed by {op2} *(on the subject)* | then, on the state that leaves, | `({op}).andThen {op2}` |
| `tied` | {op} with {t:tie} *(on the subject)* | (of the tie: the second call is given {t}; the sequence has ONE input, the first call's) | `({op}).tied {t}` |
| `same_input` | the same input | the same input as the first call | `Frames.sameInput` |
| `beside` |  | a bystander, not passed to the operation | `({op}).beside {type}` |
| `accepted` |  | the answer is an acceptance (see `accepted`) | `({opbase}).accepted ans` |

## Defaults (10)

What every sentence means unless it says otherwise. These are the fail-closed choices.

| id | Text |
|---|---|
| `D1` | always answers: the call must return an answer for every input the reading applies to (no panic, no abort, no endless loop) |
| `D2` | rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects it |
| `D3` | before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with the state after it, not states in between |
| `D4` | for all values: every outline <parameter>, every state and every input is universally quantified at the front; the Examples rows are instances |
| `D5` | collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection within the one Given, Then or Rule clause they occur in |
| `D6` | 'the first X of XS is P' requires that there is a first X |
| `D7` | items are judged afterwards: in a Then about a collection read off the answer, each item is judged on the state after the call |
| `D8` | conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly when' say about the state is judged on the state before the call (of a sequence: before its first call), not on any state the call passes through or leaves |
| `D9` | negation binds to the one condition it is written on: 'every X is not P' means that no X is P, never 'not every X is P' |
| `D10` | two calls are compared: the claim is about every pair of calls of the operation related as stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and both must give an answer |

## Coverage (3)

Which calls a claim is about.

| id | Covers | Lean |
|---|---|---|
| `calls.every` | every such call, accepted or rejected [default D2] | `Frames.Calls.every` |
| `calls.accepted` | ONLY accepted calls [asked for] | `Frames.Calls.accepted` |
| `calls.rejected` | ONLY rejected calls [asked for] | `Frames.Calls.rejected` |

## Grammar (7)

| id | How it is written | Meaning |
|---|---|---|
| `g.subject` | a {op}<br>an {op} | every call of the operation (with every state and every input) |
| `g.role` | the {role} | the part of the state, or the input, that the operation gives that role |
| `g.rule_vp` | {subject} {vp} | what the Rule says of its subject |
| `g.rule_for` | for {subject}, {claim} | what a Then would say, said of the subject |
| `g.claims` | {claim} and {claim} | each claim is made of the same subject |
| `g.clauses` | {clause}, and {clause} | each clause is a rule of its own, with its own subject |
| `g.line` | {line} | the Rule line as written, up to the case of its first letter and a final full stop |

Entries on this sheet: 72. The other books (`ledger.yaml` and the `local/` books) hold project words and are reviewed by whoever owns that project.
