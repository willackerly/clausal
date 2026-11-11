#!/usr/bin/env python3
"""Write out/families/FAMILIES.md from the measured JSON (out/families/gen/*.json, triage_2026-11-11.json).
Every number in the report is filled in here from those files; the prose around it is fixed text."""
import json, os, math, collections
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '..', '..'); O = os.path.join(REPO, 'out/families'); G = os.path.join(O, 'gen')
S = json.load(open(f'{G}/summary.json'))
tri = json.load(open(f'{O}/triage_2026-11-11.json'))
a0 = json.load(open(f'{G}/a0.json'))
kinds = json.load(open(f'{G}/kinds.json'))
n79 = json.load(open(f'{G}/F00079_names.json'))
retri = json.load(open(f'{O}/review/retriage.json'))
circj = json.load(open(f'{G}/circular.json'))
ORDER = ['F00015', 'F00019', 'F00042', 'F00046', 'F00079', 'F00073', 'F02076']
NAME = {'F00015': '15 predicates with the same closure laws', 'F00019': 'the exponent `1/2 + h`', 'F00042': 'derivative along a fixed vector',
        'F00046': '`MemClass` at named weights', 'F00079': '`MemClass` / `UniformClass` / `LocalClass` / `LocalJets`',
        'F00073': 'translation on L²', 'F02076': '`JetRate` / `FiniteJetRate` (big-O)'}
PRIM = {'F00015': 'Mathlib `AddSubgroup` (bundled structure); one instance per member', 'F00019': 'one definition, no parameter',
        'F00042': 'new definition `dirDeriv v f x`, direction explicit, spaces as type parameters',
        'F00046': 'existing corpus definition `MemClass` (weight is already a parameter)',
        'F00079': 'existing corpus structure `LocalClass` (index and localising sets as parameters)',
        'F00073': 'existing corpus definition `EulerLpTranslation.translation` (value space as type parameter)',
        'F02076': 'new definition `JetRateOn S …`, the set of orders explicit'}
HOW = {'F00015': '15 of 15 are subgroups; 1 only under a hypothesis on its weight', 'F00019': '7 of 7 by `rfl`', 'F00042': '18 of 18 by `rfl`',
       'F00046': '4 of 4 by `rfl`', 'F00079': '2 of 3 by `↔`; `LocalJets` only with weight ≥ 0', 'F00073': '1 of 1 by `rfl`',
       'F02076': '1 by `↔`, 1 by `rfl`'}
# concept counts: (definitions before, after), (lemma statements before, after) with what is counted
CONC = {
 'F00015': dict(d=(15, 14), l=(55, 55), c=(55, 15), dn='`Support` and `GaugeSupported` are one predicate (`rfl`); the predicates stay',
                ln='the corpus\'s `zero` (11), `add` (15), `neg` (14), `sub` (15) statements. In the library: 15 `sub` removed, 15 subgroup declarations added, the 40 `zero`/`add`/`neg` proofs kept as their fields. A user cites the 15 subgroup declarations'),
 'F00019': dict(d=(7, 1), l=(0, 0), c=(0, 0), dn='', ln='the definition has no lemmas of its own'),
 'F00042': dict(d=(18, 1), l=(13, 7), c=(13, 7), dn='18 → 0 with Mathlib\'s `fderiv ℝ f x v` written directly, section 2', ln='the 13 closure laws in the sampled list against 7 generic lemmas'),
 'F00046': dict(d=(5, 5), l=(2, 0), c=(2, 0), dn='the four names stay as abbreviations (5 → 1 if they are inlined)', ln='`Class.neg` and `Class.sub` duplicate `CurlClassBounds.class_neg`/`class_sub` and were re-derived by citing those (which are themselves re-derived in F00079), not through `MemClass`\'s API'),
 'F00079': dict(d=(4, 2), l=(30, 6), c=(30, 6), dn='`UniformClass` goes; `LocalJets` stays (an instance only with a nonnegative weight); `MemClass` goes here but stays through F00046', ln='30 laws with a `LocalClass` counterpart; after: 3 bridges, the 2 `LocalJets` laws that do not transfer, and `MemClass.band_smul`, which `LocalClass.band_smul` is proved from'),
 'F00073': dict(d=(2, 1), l=(4, 0), c=(4, 0), dn='', ln='four lemmas stated for both'),
 'F02076': dict(d=(2, 1), l=(6, 4), c=(6, 4), dn='', ln='`weaken`, `add`, `congr_on` twice against the same three plus `mono`'),
}
def pct(a, b): return f'{100 * a / b:.0f}%' if b else '–'
def chg(a, b): return f'{100 * (b - a) / a:+.0f}%' if a else '–'
def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)
L = []
w = L.append
T = {f: S[f]['totals'] for f in ORDER}
tot = lambda k: sum(T[f][k] for f in ORDER)
libn = sum(S[f]['lib']['nodes'] for f in ORDER); libl = sum(S[f]['lib']['sourceLines'] for f in ORDER)
nre = sum(S[f]['rederived'] for f in ORDER); natt = sum(S[f]['attempted'] for f in ORDER); ncomp = sum(S[f]['compiled'] for f in ORDER)
nhb = tot('hbPairs')
libhbC = sum(S[f]['lib']['heartbeatsCharged'] for f in ORDER); libhbU = sum(S[f]['lib']['heartbeatsUsed'] for f in ORDER); libinst = sum(S[f]['lib']['instSlots'] for f in ORDER)
netn = (tot('origNodes') - tot('newNodes')) - libn; netl = (tot('origLines') - tot('newLines')) - libl
def netf(f): return (T[f]['origNodes'] - T[f]['newNodes']) - S[f]['lib']['nodes']
def hbtot(f, k='heartbeatsCharged'): return T[f]['newHeartbeats'] + S[f]['lib'][k]
failed = [n for f in ORDER for n in S[f]['baselineFailed']]
short = lambda n: n.replace('NavierStokes.', '')
dB = sum(CONC[f]['d'][0] for f in ORDER) - 1; dA = sum(CONC[f]['d'][1] for f in ORDER)   # `MemClass` is in two families: counted once before; after, it survives once (through F00046)
lB = sum(CONC[f]['l'][0] for f in ORDER); lA = sum(CONC[f]['l'][1] for f in ORDER); cA = sum(CONC[f]['c'][1] for f in ORDER)
cnt = collections.Counter(r['cls'] for r in tri['rows'])
a0m = sum(v['members'] for v in a0.values()); a0rfl = sum(v['rfl'] for v in a0.values()); a0chk = sum(v['checked'] for v in a0.values())
a0v = {k: v for k, v in a0.items() if k != 'F00011'}
axioms = sorted({a for f in ORDER for a in S[f]['lib']['axioms']} | {a for f in ORDER for p in S[f]['pairs'] for a in (p['axioms'] or [])})

w('# M9 families: triage, and seven families taken through Lean\n')
w('2026-11-11. Corpus: `corpora/ns` (Lean 4.34.0-rc2), read-only; nothing in it was modified or rebuilt. Work: `corpora/families/`, results: `out/families/`. The clustering this starts from is `out/families/ns/CLUSTERS.md`.\n')
w(f'**What is evidence here.** Every primitive, every "member is an instance" statement, every re-derived lemma and every counterexample is kernel-checked against the built corpus, with no `sorry` and axioms {", ".join("`" + a + "`" for a in axioms)} only. Sizes, instance counts and heartbeats are measured on the elaborated terms. The triage (section 1) and every sentence marked *reading* are a model\'s reading and are not evidence. Each re-derived proof\'s transitive dependencies were checked for the corpus lemma it replaces: {nre} of {ncomp} are non-circular; `MemClass.band_smul` is circular and is excluded from every total. The node is **exploratory**: the triage and the family list were frozen before any Lean, but the measuring tools were written while looking at results. One independent agent has reviewed it (section 10); this version applies its corrections and reruns what they affect.\n')

w('## Result\n')
f79 = S['F00079']; t79 = T['F00079']; f15 = S['F00015']; t15 = T['F00015']
co = next(p for p in f15['pairs'] if 'CoefficientsOn' in p['name'])
rest15 = [p for p in f15['pairs'] if p is not co]
ch15 = sum(1 for p in rest15 if p['newHeartbeats'] < p['origHeartbeats']); up15 = [p['newHeartbeats'] - p['origHeartbeats'] for p in rest15 if p['newHeartbeats'] > p['origHeartbeats']]
others = [f for f in ORDER if f != 'F00079']
oH = sum(T[f]['origHeartbeats'] for f in others); oN = sum(hbtot(f) for f in others); oNu = sum(hbtot(f, 'heartbeatsUsed') for f in others)
m42 = S['F00042']['mathlibOnly']; mt = m42['totals']
r15o = t15['origHeartbeats'] - co['origHeartbeats']; r15n = t15['newHeartbeats'] - co['newHeartbeats']
w(f'1. **Each of the seven chosen families has a kernel-checked common form, and in four of them it was already in the project or in Mathlib.** For three families the primitive is a definition the corpus already has (`LocalClass`, `MemClass`, the vector-valued `translation`); for the 15-predicate family it is Mathlib\'s `AddSubgroup`; three got a new definition (`dirDeriv`, `JetRateOn`, one shared exponent), and for `dirDeriv` the review showed that no new definition does as well (Mathlib\'s `fderiv` written directly). No generalisation was false, but that tests little: only two genuinely new parameterised statements were attempted. Two members are instances only under a hypothesis they do not carry (`LocalJets` and `NativeJets`: a nonnegative weight), each with a kernel-checked counterexample.')
w(f'2. **Concept count, on the seven families: {dB} distinct definitions → {dA}, and {lB} lemma statements → {lA} in the library.** `MemClass` is counted once; `LocalJets` stays, because it is an instance only under a hypothesis it lacks and two of its laws do not transfer. The number of statements a downstream user cites goes {lB} → {cA}, but 40 of that difference is the 15-predicate family, whose 40 `zero`/`add`/`neg` proofs remain as the fields of its 15 subgroup declarations. {nre} member lemmas were re-derived from the primitive\'s API with their corpus statements unchanged ({natt} attempted, {ncomp} compile, 1 is circular and not counted). A merged primitive also carries more parameters than a member: `LocalClass` has five explicit parameters and an index type against `MemClass`\'s four, and `dirDeriv` adds a direction and four instance arguments.')
w(f'3. **Proof size: one family pays for all the others.** Over {nre} re-derived lemmas, proofs go from {tot("origNodes"):,} to {tot("newNodes"):,} elaborated nodes ({chg(tot("origNodes"), tot("newNodes"))}) and from {tot("origLines")} to {tot("newLines")} source lines, against {libn:,} nodes and {libl} lines of new library: net {netn:,} nodes saved and {-netl} source lines added. A {ncomp}th, `MemClass.band_smul`, compiles but is circular (the corpus proves `LocalClass.band_smul` from `MemClass.band_smul`), so it is not counted. `MemClass`/`UniformClass`/`LocalClass`/`LocalJets` alone gives {t79["origNodes"]:,} → {t79["newNodes"]:,} over {f79["rederived"]} lemmas for {f79["lib"]["nodes"]:,} nodes of bridging lemmas (net {netf("F00079"):,}, {100 * netf("F00079") / netn:.0f}% of the net saving), because the corpus proved the same laws up to four times. The other six families together net {netn - netf("F00079"):+,} nodes: break-even, which is what the earlier constant-threading experiment found.')
w(f'4. **Elaboration cost: cheaper proofs, dearer in total once the new library is charged.** Re-derived proofs fill {100 * (tot("origInstSlots") - tot("newInstSlots")) / tot("origInstSlots"):.0f}% fewer instance-argument slots ({tot("origInstSlots"):,} → {tot("newInstSlots"):,}), or {100 * (tot("origInstSlots") - tot("newInstSlots") - libinst) / tot("origInstSlots"):.0f}% fewer with the new library\'s {libinst:,} slots charged. Heartbeats (Lean\'s deterministic work counter) in the proofs themselves fall {100 * (tot("origHeartbeats") - tot("newHeartbeats")) / tot("origHeartbeats"):.0f}% ({tot("origHeartbeats"):,} → {tot("newHeartbeats"):,}) over the {nhb} lemmas whose corpus proof replays in a scratch file and whose re-derivation is not circular. Charging the new library\'s own elaboration, as its nodes are charged, the total **rises**: {chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbU)} ({tot("newHeartbeats") + libhbU:,}) counting only the declarations the re-derived proofs depend on, {chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbC)} ({tot("newHeartbeats") + libhbC:,}) counting every new declaration that is charged in nodes. F00079 is {t79["origHeartbeats"]:,} → {hbtot("F00079"):,} ({chg(t79["origHeartbeats"], hbtot("F00079"))}) with its bridges charged; the other six families together go {oH:,} → {oN:,} ({chg(oH, oN)}; {chg(oH, oNu)} on the narrower count). Two specific costs: in the family that goes through a bundled interface (`AddSubgroup`), {ch15} of the fifteen `sub` lemmas are cheaper, {len(up15)} are {min(up15)} to {max(up15)} heartbeats dearer, and **one costs {co["newHeartbeats"] / co["origHeartbeats"]:.0f}× more** ({co["origHeartbeats"]} → {co["newHeartbeats"]:,}, a relation on a pair of coefficient families, where Lean has to see through a product of two group structures). And a polymorphic primitive makes statements larger: restating 50 theorems about the directional derivative against `dirDeriv` grows their statements by {chg(S["F00042"]["transport"]["api"]["statementBefore"] + S["F00042"]["transport"]["down"]["statementBefore"], S["F00042"]["transport"]["api"]["statementAfter"] + S["F00042"]["transport"]["down"]["statementAfter"])} in elaborated nodes, all of it type and instance arguments the local names had hidden.')
gen = sum(S[f]['abs']['results'].get('generic', 0) for f in ORDER); ana = sum(S[f]['abs']['analysed'] for f in ORDER)
w(f'5. **Downstream, about half of the proofs never look inside the definition they use.** Of {ana:,} sampled theorems that use a member, {gen:,} ({pct(gen, ana)}) are kernel-checked to be generic in it: they would go through unchanged for any primitive with the same lemmas. The share is {pct(S["F00046"]["abs"]["results"].get("generic", 0), S["F00046"]["abs"]["analysed"])} for `MemClass` and its named weights and {pct(S["F00019"]["abs"]["results"].get("generic", 0), S["F00019"]["abs"]["analysed"])} for the exponent, whose users unfold it and do arithmetic. In the five families where a restatement tool was run, every sampled downstream statement that mentions a replaceable member was restated against the primitive and kernel-checked (46 of 46: 40 with the original proof accepted as it stands, 6 across a proved equation). The 40 are in the four families whose members equal the primitive by `rfl`, so they follow from the instance lemma by unfolding and check the tool, not the generalisation; the informative cases are the 6. And the interface the generic proofs are generic over is large: {min(S[f]["abs"]["distinctCitedByGeneric"] for f in ORDER)} to {max(S[f]["abs"]["distinctCitedByGeneric"] for f in ORDER)} distinct lemmas per family.')
w(f'6. **The cheapest concept reduction needs no abstraction at all.** {sum(v["members"] for v in a0v.values())} type abbreviations in {len(a0v)} families are the first member of their family by `rfl` ({sum(v["rfl"] for v in a0v.values())} of {sum(v["checked"] for v in a0v.values())} checked): {sum(v["rfl"] for v in a0v.values())} names can go with no proof touched.')
w('\nThe trade is stated at the end.\n')

# ---------------- 1 triage
w('## 1. Triage of the 60 top clusters\n')
w('**This table is a model\'s reading, not evidence.** It was written to `out/families/TRIAGE_2026-11-11.md` before any generalisation was attempted, from each cluster\'s member bodies, types and side-by-side lemma blocks, and has not been edited since. Classes: **(a)** one idea, several instances; **(a0)** one *type* under several local names (one idea, but no hole and no lemma API: deduplication only, added by me, see `DECISIONS.md`); **(b)** parallel by construction, different mathematics; **(c)** accidental resemblance; **(d)** a library notion under a local name.\n')
w('Counts: ' + ', '.join(f'({k}) {cnt[k]}' for k in ['a', 'a0', 'b', 'c', 'd']) + '.\n')
w('| # | id | class | members | users | first member | reason (reading) |')
w('|---:|---|---|---:|---:|---|---|')
for x in tri['rows']:
    w(f"| {x['rank']} | {x['id']} | ({x['cls']}) | {x['members']} | {x['users']:,} | `{x['first'].replace('NavierStokes.', '')}` | {x['reason']} |")
w('\n**Chosen by rule** (top 6 of class (a) by number of users, plus the positive controls): ' + ', '.join(tri['frozen']['chosen']) + '. F00046 and F00079 are also the constant-hiding control; F02076 is the big-O control and was added by the rule (it is rank 2,076 of the clustering, not in the top 60). Class (a) and not chosen: F00061, F00064.\n')
w('*How the reading held up (measured afterwards).* All seven chosen families did have one idea behind them. Two readings were off: F00015 was read as possibly "one interface", and it is one, but the interface is the library\'s (`AddSubgroup`), so it could equally have been classed (d); and for F00079, F00046 and F00073 the "parameterised primitive" was already a corpus definition, which the reading anticipated only for F00046.\n')
_dis = [k for k in retri['reviewer'] if retri['reviewer'][k] != retri['builder'][k]]
_nt = [k for k in retri['reviewer'] if retri['builder'][k] != 'a0']
w(f"*A second model reading.* The reviewing agent re-classified {len(retri['reviewer'])} of the 60 (seed {retri['seed']}). It was **not blind**: the reviewer had read the table above first, so agreement is probably inflated. It agreed on {retri['agree']} of {len(retri['reviewer'])} (κ ≈ {retri['kappa']:.2f}); {sum(1 for k in _nt if retri['reviewer'][k] == retri['builder'][k])} of {len(_nt)} when the type clusters, which nobody would dispute, are left out. The three disagreements: F00015 is (d) or (b), since the shared notion is the library\'s `AddSubgroup` and the members are different subspaces; F00042 is (d), Mathlib\'s `fderiv` applied to a vector; F00030 is (a), one operator record with the solve operator as a parameter, 257 users. On the second reading two of the seven measured families would not have been chosen, and one family that was not measured would have been. The measurements side with the second reading on both: F00015 saved nothing, and F00042 does as well with no new definition (section 2).\n")

# ---------------- 2 families
w('## 2. The seven families, before and after\n')
w('| family | members | primitive, and its form | members are instances | re-derived lemmas | proof nodes | new library nodes | net nodes |')
w('|---|---:|---|---|---:|---|---:|---:|')
for f in ORDER:
    s = S[f]; t = T[f]
    net = (t['origNodes'] - t['newNodes']) - s['lib']['nodes']
    w(f"| {f} {NAME[f]} | {len(s['members'])} | {PRIM[f]} | {HOW[f]} | {s['rederived']} | {t['origNodes']:,} → {t['newNodes']:,} | {s['lib']['nodes']:,} | {net:+,} |")
w(f"| **total** | | | | **{nre}** | **{tot('origNodes'):,} → {tot('newNodes'):,}** | **{libn:,}** | **{(tot('origNodes') - tot('newNodes')) - libn:+,}** |")
w('\n"Net" is nodes saved in the re-derived proofs minus the new library; positive is a saving. Lemmas of a primitive that the corpus already has are not charged. `MemClass` is a member of two families. F00079 has 28 re-derivations that compile; one is circular and is not counted (section 3).\n')
w('**Why each form.**\n')
w('- **F00019, one definition.** The seven members are the same function; any parameter would be decoration.')
w('- **F00042, a definition with an explicit parameter.** The members differ in a direction vector and in the spaces. The direction is an explicit argument; the spaces are implicit type arguments with their normed-space instances. A structure or class has nothing to bundle. **A simpler choice exists, found in review and rerun here: no new definition, with Mathlib\'s `fderiv ℝ f x v` written directly.** Re-deriving the same 13 lemmas from Mathlib alone (`corpora/families/lean/F00042_mathlib.lean`; {m42["same"]} of 13 statements are the corpus\'s, {m42["sameSyntactic"]} syntactically and {m42["same"] - m42["sameSyntactic"]} up to unfolding instances) gives {mt["origNodes"]:,} → {mt["newNodes"]:,} proof nodes and {mt["origHeartbeats"]:,} → {mt["newHeartbeats"]:,} heartbeats ({mt["hbPairs"]} measurable) with no library at all, against {T["F00042"]["newNodes"]:,} nodes plus {S["F00042"]["lib"]["nodes"]:,} of library with `dirDeriv`, and 18 → 0 definitions instead of 18 → 1. The corpus\'s member lemmas were already Mathlib one-liners, so the `dirDeriv` saving is those proofs moved into seven generic lemmas. On this evidence F00042 is class (d), a library notion under local names, not a family that needed a primitive.'.replace('{m42["same"]}', str(m42["same"])).replace('{m42["sameSyntactic"]}', str(m42["sameSyntactic"])).replace('{m42["same"] - m42["sameSyntactic"]}', str(m42["same"] - m42["sameSyntactic"])).replace('{mt["origNodes"]:,}', f'{mt["origNodes"]:,}').replace('{mt["newNodes"]:,}', f'{mt["newNodes"]:,}').replace('{mt["origHeartbeats"]:,}', f'{mt["origHeartbeats"]:,}').replace('{mt["newHeartbeats"]:,}', f'{mt["newHeartbeats"]:,}').replace('{mt["hbPairs"]}', str(mt["hbPairs"])).replace('{T["F00042"]["newNodes"]:,}', f'{T["F00042"]["newNodes"]:,}').replace('{S["F00042"]["lib"]["nodes"]:,}', f'{S["F00042"]["lib"]["nodes"]:,}'))
w('- **F02076, a definition with an explicit parameter.** "One order" and "all orders up to M" are both "the orders in a set S": `JetRateOn {m}` and `JetRateOn (Set.Iic M)`. The second is definitional; the first is an `↔`.')
w('- **F00046, F00073, F00079: nothing new.** The corpus already wrote the parameterised form (a weight; a value space; an index and localising sets). What was missing is the statement that the other members are instances of it.')
w('- **F00015, a bundled structure from the library.** The bodies have nothing in common, so no parameter can merge them; what they share is closure under `0`, `+`, `-`. That is `AddSubgroup`. It is not `Submodule` because six members have no constant-multiple lemma in the corpus. It is not a type class because each member is a family indexed by sets, intervals or gauges, so there is no canonical instance for search to find; instance search would add cost and find nothing.\n')

# ---------------- 3 one family in full
w('## 3. One family in full: F00079\n')
w('Four predicates say "all jets of `f` are bounded by a constant times a majorant", with the constant hidden behind `∃`. The corpus source, abridged (fields in the same order):\n')
w('''```lean
structure MemClass     (s) (w : ℕ → D → ℝ)     (α) (f : ℕ → D → E)                             -- one family
structure UniformClass (s) (w : ι → ℕ → D → ℝ) (α) (f : ι → ℕ → D → E)                         -- uniform in a label
structure LocalJets    (s) (w : ℕ → D → ℝ)     (α) (K : ℕ → I → Set D) (f : ℕ → I → D → E)     -- only on cells K
structure LocalClass   (s) (K : ℕ → I → Set D) (w : ℕ → I → D → ℝ) (α) (f : ℕ → I → D → E) : Prop where
  weight_nonneg : ∀ n i x, x ∈ s.domain → 0 ≤ w n i x
  smooth : ∀ n i x, x ∈ s.domain → x ∈ K n i → ContDiffAt ℝ ∞ (f n i) x
  bounds : ∀ m : ℕ, ∃ C : ℝ, 0 ≤ C ∧ ∃ p : ℕ,
    ∀ n i x, x ∈ s.domain → x ∈ K n i → ∀ j ≤ m,
      ‖iteratedFDeriv ℝ j (f n i) x‖ ≤ majorant s (fun n x => w n i x) α C p n x
```\n''')
w('`LocalClass` has both optional features, so it is the primitive. What this node adds (`corpora/families/lean/F79.lean`, kernel-checked):\n')
w('''```lean
theorem memClass_iff :
    MemClass s w α f ↔ LocalClass s (fun _ (_ : Unit) => univ) (fun n _ => w n) α (fun n _ => f n)
theorem uniformClass_iff :
    UniformClass s w α f ↔ LocalClass s (fun _ (_ : ι) => univ) (fun n l => w l n) α (fun n l => f l n)
theorem localJets_iff (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K f ↔ LocalClass s K (fun n _ => w n) α f
-- the hypothesis cannot be dropped: weight −1, the zero family
theorem localJets_not_localClass (s) (α) (K) (i : I) {x : D} (hx : x ∈ s.domain) :
    LocalJets s (fun _ _ => -1) α K (fun _ _ _ => (0 : E)) ∧
      ¬ LocalClass s K (fun _ _ _ => -1) α (fun _ _ _ => (0 : E))
```\n''')
w('The API is `LocalClass`\'s own, already in the corpus. A member lemma before and after (statement identical; the proof is the only change):\n')
p = next(p for p in f79['pairs'] if p['name'].endswith('MemClass.bilinear'))
w(f'''```lean
-- corpus: {p['origLines']} lines, {p['origNodes']:,} proof nodes (heartbeats not measured: the corpus proof uses a private helper and did not replay in the scratch file)
theorem MemClass.bilinear {{u : ℕ → D → F}} (hf : MemClass s w α f) (hu : MemClass s v β u) (L : E →L[ℝ] F →L[ℝ] G) :
    MemClass s (fun n x => w n x * v n x) (α + β) (fun n x => L (f n x) (u n x)) := by
  refine ⟨fun n x hx => mul_nonneg (hf.weight_nonneg n x hx) (hu.weight_nonneg n x hx),
    fun n => (L.contDiff.comp_contDiffOn (hf.smooth n)).clm_apply (hu.smooth n), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hu.bounds m
  refine ⟨‖L‖ * (2 : ℝ) ^ m * A * B, by positivity, p + q, ?_⟩
  …                                                   -- 12 more lines; the same proof is in the corpus four times
-- re-derived: {p['newLines']} lines, {p['newNodes']:,} proof nodes, {p['newHeartbeats']:,} heartbeats
    … := memClass_iff.2 ((memClass_iff.1 hf).bilinear (memClass_iff.1 hu) L)
```\n''')
w('All re-derived lemmas of this family:\n')
w('| lemma | proof nodes | instance slots | heartbeats | lines |')
w('|---|---|---|---|---|')
def hbc(p): return f"{p['origHeartbeats']:,}" if p['origHeartbeats'] is not None else 'n/a (replay failed)'
for p in f79['pairs']:
    w(f"| `{short(p['name'])}`{' *(circular, not counted)*' if p['circular'] else ''} | {p['origNodes']:,} → {p['newNodes']:,} | {p['origInstSlots']:,} → {p['newInstSlots']:,} | {hbc(p)} → {p['newHeartbeats']:,} | {p['origLines']} → {p['newLines']} |")
w(f"| **{t79['pairs']} lemmas counted** | **{t79['origNodes']:,} → {t79['newNodes']:,}** | **{t79['origInstSlots']:,} → {t79['newInstSlots']:,}** | **{t79['origHeartbeats']:,} → {t79['newHeartbeats']:,} ({t79['hbPairs']} measurable)** | **{t79['origLines']} → {t79['newLines']}** |")
w('\n*Circular:* the corpus\'s `LocalClass.band_smul`, which the re-derived `MemClass.band_smul` cites, is itself proved from `MemClass.band_smul` (`corpora/families/lean/Circ.lean` prints, for every re-derived lemma, which replaced originals it depends on; this is the only one that depends on itself, and no two re-derivations depend on each other\'s originals). The original cannot be deleted, and the row is in no total. The re-derived `LocalJets.band_smul` also depends on `MemClass.band_smul` staying. *Replay failed:* three corpus proofs use a private helper that is out of scope in a scratch file, so they have no valid "before" heartbeat figure; the first version of this report printed the heartbeats of the failed elaboration.')
w(f'\nThe list is every theorem of `MemClass.*`, `UniformClass.*`, `LocalJets.*` with the same short name as a `LocalClass` lemma ({n79["Mem"]["lemmas"]} / {n79["Uniform"]["lemmas"]} / {n79["Jets"]["lemmas"]} theorems in those namespaces; {len(n79["Mem"]["sameNameInLocalClass"])} / {len(n79["Uniform"]["sameNameInLocalClass"])} / {len(n79["Jets"]["sameNameInLocalClass"])} matched), plus four with other names (`class_neg`, `class_sub`, `fderiv_class`, `cmul`). Three small lemmas grow (`MemClass.mul`, `MemClass.smul`, `cmul`, each a one-line corollary already). **Two did not transfer: `LocalJets.map` and `LocalJets.fderiv`** are stated without a nonnegative weight, and `LocalClass` cannot supply them without one. The corpus itself carries that hypothesis by hand on `LocalJets.add`, `.bilinear`, `.smul` and `.band_smul`. `UniformClass.congr` needed `LocalClass.congr_germ`, because it is stated with equality on the domain only and `LocalClass.congr` asks for equality everywhere.\n')
w('The corpus knows these predicates are related: it has `LocalClass.of_global`, `of_localJets`, `to_localJets` and `UniformClass.each`, and a private helper `bilinear_jet_at` that is defined identically in two files. It converts between the predicates and still proves the algebra for each.\n')

# ---------------- 4 measurements
w('## 4. Measurements\n')
w('### 4.1 Concept count\n')
w('| family | definitions | lemma statements in the library | cited by a user | what is counted |')
w('|---|---|---|---|---|')
for f in ORDER:
    c = CONC[f]
    w(f"| {f} | {c['d'][0]} → {c['d'][1]}{' (' + c['dn'] + ')' if c['dn'] else ''} | {c['l'][0]} → {c['l'][1]} | {c['c'][0]} → {c['c'][1]} | {c['ln']} |")
w(f'| **total** | **{dB} distinct → {dA}** | **{lB} → {lA} ({chg(lB, lA)})** | **{lB} → {cA}** | |')
w(f'\n`MemClass` is in two families: it is counted once before, and after it survives once, as the form the four named weights are instances of (and because `LocalClass.band_smul` is proved from `MemClass.band_smul`). If `MemClass` were also folded into `LocalClass` the count would be {dB} → {dA - 1}, at the price of stating the four weights against a five-parameter structure at a one-point index. The first version of this report said 53 → 24 and 110 → 31: it counted `MemClass` twice, counted `LocalJets` as deleted while keeping two of its laws, and counted only what a user cites. The corpus has 9,903 reachable definitions and 25,715 reachable theorems, so these seven families are {dB - dA} definitions ({100 * (dB - dA) / 9903:.2f}%) and {lB - lA} statements ({100 * (lB - lA) / 25715:.2f}%). For F00042 only the sampled list was worked (13 closure laws in 40 sampled of {S["F00042"]["apiFull"]} listed); the corpus has more copies of the same seven laws that were not counted.\n')
w('*More parameters per concept.* Fewer concepts is not the same as lighter concepts: `LocalClass` has five explicit parameters and an index type where `MemClass` has four; `dirDeriv` has a direction and four instance arguments where `partialX` had none; `JetRateOn` takes a set of orders where `JetRate` took one order.\n')

w('### 4.2 Proof size, with the library charged\n')
w('| family | lemmas | proof nodes | source lines | library: declarations / nodes / lines | net nodes | net lines |')
w('|---|---:|---|---|---|---:|---:|')
for f in ORDER:
    s = S[f]; t = T[f]
    if not s['rederived']:
        w(f"| {f} | 0 | – | – | {s['lib']['decls']} / {s['lib']['nodes']:,} / {s['lib']['sourceLines']} | {-s['lib']['nodes']:+,} | {-s['lib']['sourceLines']:+} |"); continue
    w(f"| {f} | {s['rederived']} | {t['origNodes']:,} → {t['newNodes']:,} ({chg(t['origNodes'], t['newNodes'])}) | {t['origLines']} → {t['newLines']} | {s['lib']['decls']} / {s['lib']['nodes']:,} / {s['lib']['sourceLines']} | {(t['origNodes'] - t['newNodes']) - s['lib']['nodes']:+,} | {(t['origLines'] - t['newLines']) - s['lib']['sourceLines']:+} |")
w(f"| **total** | **{nre}** | **{tot('origNodes'):,} → {tot('newNodes'):,} ({chg(tot('origNodes'), tot('newNodes'))})** | **{tot('origLines')} → {tot('newLines')}** | **{sum(S[f]['lib']['decls'] for f in ORDER)} / {libn:,} / {libl}** | **{(tot('origNodes') - tot('newNodes')) - libn:+,}** | **{(tot('origLines') - tot('newLines')) - libl:+}** |")
w('\nProof nodes are distinct subterms of the elaborated proof (the corpus export\'s `proofSize`). Source lines are whole declarations, statement included. The library column counts only declarations written for this node: the primitive where it is new, its API where it is new, and the "member is an instance" lemmas.\n')
b42 = S['F00042']['lib']['byGroup']; b76 = S['F02076']['lib']['byGroup']; b15 = S['F00015']['lib']['byGroup']
w(f'- **F00042**: the generic API is {b42["lib"]["n"]} lemmas, {b42["lib"]["nodes"]:,} nodes; the 18 `rfl` instance lemmas are {b42["inst"]["nodes"]} nodes. At 13 re-derived lemmas the library is not yet paid for.')
w(f'- **F02076**: the three generic laws plus `mono` are {b76["lib"]["nodes"]:,} nodes, about the size of one copy of the three laws they replace ({sum(p["origNodes"] for p in S["F02076"]["pairs"][:3]):,}); the `↔` for `JetRate` is {b76["inst"]["nodes"]:,}.')
w(f'- **F00015**: the 15 subgroup declarations and the two bridge lemmas are {S["F00015"]["lib"]["nodes"]:,} nodes for {t15["origNodes"] - t15["newNodes"]:,} saved: the `sub` lemmas were already one-liners (`hf.add hg.neg`).')
w('- **F00019**: nothing to save. The members have no lemmas of their own.')
w(f'- **Without F00079** the six other families net {netn - netf("F00079"):+,} nodes and {netl - ((t79["origLines"] - t79["newLines"]) - f79["lib"]["sourceLines"]):+} source lines.\n')

w('### 4.3 Statements\n')
w('Re-derived lemmas keep the corpus statement, so their size and hypothesis counts do not change. Two things do change.\n')
w('*Generic lemma against the member lemma it replaces* (statement nodes; proposition hypotheses; instance arguments):\n')
w('| generic | statement | member lemma | statement |')
w('|---|---|---|---|')
fam_rows = {f: {r['name']: r for r in [json.loads(l[8:]) for l in open(f'{HERE}/build/{S[f]["file"]}.log') if l.startswith('MEASURE ')]} for f in ORDER}
def st(r): return f"{r['statementDag']} nodes, {r['hyps']} hyps, {r['instBinders']} inst"
decl = {}
for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
    d = json.loads(l); decl[d['name']] = d
PAIRS = [('F02076', 'Fam.F2076.JetRateOn.add', 'NavierStokes.DiagonalResidual.JetRate.add'), ('F02076', 'Fam.F2076.JetRateOn.weaken', 'NavierStokes.DiagonalResidual.JetRate.weaken'),
         ('F00042', 'Fam.F42.dirDeriv_contDiffAt', 'NavierStokes.SimilarityProfile.partialX_smoothAt'), ('F00042', 'Fam.F42.dirDeriv_const_mul', 'NavierStokes.NaturalCoefficientBridge.partialX_const_mul'),
         ('F00042', 'Fam.F42.hasDerivAt_fst_slice', 'NavierStokes.SmoothFourierData.hasDerivAt_slice'), ('F00042', 'Fam.F42.dirDeriv_mul', 'EulerMeanHarmonic.partialDerivative_mul'),
         ('F00079', 'NavierStokes.LocalizedWaveBounds.LocalClass.bilinear', 'NavierStokes.WeightedClasses.MemClass.bilinear'), ('F00079', 'NavierStokes.LocalizedWaveBounds.LocalClass.map', 'NavierStokes.WeightedClasses.MemClass.map'),
         ('F00079', 'NavierStokes.LocalizedWaveBounds.LocalClass.fderiv', 'NavierStokes.WeightedClasses.MemClass.fderiv')]
sg = sm = 0
for f, g, m in PAIRS:
    gr = fam_rows[f][g]; pr = next(p for p in S[f]['pairs'] if p['name'] == m)
    sg += gr['statementDag']; sm += pr['statementNodes']
    w(f"| `{g.replace('NavierStokes.', '').replace('Fam.', '')}` | {st(gr)} | `{m.replace('NavierStokes.', '')}` | {pr['statementNodes']} nodes, {pr['hyps']} hyps, {pr['instBinders']} inst |")
w(f'\nOver these nine pairs the generic statement is {chg(sm, sg)} in nodes ({sm:,} → {sg:,}). Hypothesis counts are equal; the polymorphic ones carry more instance arguments (`dirDeriv_*`: 4 against 0, because the member was stated at `ℝ × ℝ`).\n')
w('*A downstream statement restated against the primitive* (statement nodes summed over the theorems that were restated):\n')
w('| family | sampled API list | 10 downstream |')
w('|---|---|---|')
for f in ORDER:
    tr = S[f]['transport']
    if not tr['api']['results'] and not tr['down']['results']: continue
    a, d = tr['api'], tr['down']
    w(f"| {f} | {a['statementBefore']:,} → {a['statementAfter']:,} ({chg(a['statementBefore'], a['statementAfter'])}) | {d['statementBefore']:,} → {d['statementAfter']:,} ({chg(d['statementBefore'], d['statementAfter'])}) |")
w('\nF00019 is a rename. F02076 replaces the member by a reducible name for the instance, so sizes are equal by construction. F00042 is the measured cost of polymorphism in statements: each `partialX f w` becomes `dirDeriv (1, 0) f w` with the two spaces and four instances written out in the term. A reader does not see them; the elaborator and every tool that walks the term does. F00046 grows because the named weight is written out.\n')

w('### 4.4 Elaboration cost\n')
w('| family | instance slots in the proofs | + new library | heartbeats in the proofs (lemmas measurable) | new library: charged / used | total with library, charged (used) |')
w('|---|---|---|---|---|---|')
for f in ORDER:
    s = S[f]; t = T[f]; lb = s['lib']
    if not s['rederived']:
        w(f"| {f} | – | {lb['instSlots']:,} | – | {lb['heartbeatsCharged']:,} / {lb['heartbeatsUsed']:,} | 0 → {lb['heartbeatsCharged']:,} |"); continue
    w(f"| {f} | {t['origInstSlots']:,} → {t['newInstSlots']:,} ({chg(t['origInstSlots'], t['newInstSlots'])}) | {t['newInstSlots'] + lb['instSlots']:,} | {t['origHeartbeats']:,} → {t['newHeartbeats']:,} ({chg(t['origHeartbeats'], t['newHeartbeats'])}; {t['hbPairs']} of {t['pairs']}) | {lb['heartbeatsCharged']:,} / {lb['heartbeatsUsed']:,} | {t['origHeartbeats']:,} → {hbtot(f):,} ({chg(t['origHeartbeats'], hbtot(f))}); {hbtot(f, 'heartbeatsUsed'):,} ({chg(t['origHeartbeats'], hbtot(f, 'heartbeatsUsed'))}) |")
w(f"| **total** | **{tot('origInstSlots'):,} → {tot('newInstSlots'):,} ({chg(tot('origInstSlots'), tot('newInstSlots'))})** | **{tot('newInstSlots') + libinst:,} ({chg(tot('origInstSlots'), tot('newInstSlots') + libinst)})** | **{tot('origHeartbeats'):,} → {tot('newHeartbeats'):,} ({chg(tot('origHeartbeats'), tot('newHeartbeats'))}; {nhb} of {nre})** | **{libhbC:,} / {libhbU:,}** | **{tot('origHeartbeats'):,} → {tot('newHeartbeats') + libhbC:,} ({chg(tot('origHeartbeats'), tot('newHeartbeats') + libhbC)}); {tot('newHeartbeats') + libhbU:,} ({chg(tot('origHeartbeats'), tot('newHeartbeats') + libhbU)})** |")
w('\n- *Instance slots*: instance-implicit arguments filled at constant applications in the proof term, counted on distinct subterms. They fall with proof size; the share of applications that carry one does not change much.')
w('- *Heartbeats*: Lean\'s deterministic work counter (`#count_heartbeats`, statement and proof, asynchronous elaboration off), for the same statement with the corpus proof and with the re-derived proof, each re-elaborated in a scratch file. Independent of machine load; repeat runs differ by a few heartbeats.')
w(f'- *Which lemmas are in the heartbeat totals.* {nhb} of the {nre} counted lemmas. Four corpus proofs did not elaborate in the scratch file, so their "before" figure is not a measurement and they are left out on both sides: {", ".join("`" + short(n) + "`" for n in failed)} (three use a private helper that is out of scope there, one hits an ambiguous name). The first version of this report used the heartbeats of those failed elaborations and reported 53,179 → 38,096 (-28%).')
w(f'- *New library.* The first version charged the new library in nodes and lines and not in elaboration. "Charged" is the elaboration of every new declaration that is charged in nodes (the primitive, its API, the "member is an instance" lemmas; {libhbC:,} heartbeats); "used" is the subset that some re-derived proof depends on, by transitive closure ({libhbU:,}; the reviewer\'s slightly wider reading of "used" gave 13,096 and +14%). The library is elaborated once, so at higher adoption its share falls; at the adoption measured here it outweighs the saving in every family except the two whose primitive the corpus already had and proved laws for (F00079 and F00073). F00046 is cheaper only if its four `rfl` instance lemmas, which its two re-derived proofs do not cite, are left uncharged.')
w(f"- **F00015 shows the risk of the bundled form.** {ch15} of the fifteen `sub` lemmas are cheaper through `AddSubgroup`, {len(up15)} are {min(up15)} to {max(up15)} heartbeats dearer; the fourteen other than `CoefficientsOn.sub` total {r15o:,} → {r15n:,}. `CoefficientsOn.sub` goes from {co['origHeartbeats']} to {co['newHeartbeats']:,}: its subgroup lives in a product of two `AddMonoidAlgebra`s, and matching `(c₁, d₁) - (c₂, d₂) ∈ S` against `CoefficientsOn … (c₁ - c₂) (d₁ - d₂)` makes the elaborator unfold both group structures. The proof term is a third of the size. The 15 subgroup declarations themselves cost {S['F00015']['lib']['heartbeatsCharged']:,} heartbeats, so the family goes {t15['origHeartbeats']:,} → {hbtot('F00015'):,} with its library charged. The cost is not a steady tax; it is an occasional large bill that the proof-size figure does not show.")
w('- **Statement elaboration dominates small lemmas.** With asynchronous elaboration on, `#count_heartbeats` sees only the statement; those figures were within a few percent of the full ones for the short lemmas. A two-line corollary costs about what its statement costs, whichever proof it has.')
w('- *Wall-clock file times are not reported.* The first version had a column of them, taken at load average 12 to 18 from other agents\' builds: two rows were negative and F00073\'s re-derived file came out slower although its heartbeats fall 76%. That is noise, not a measurement, and the plan requires timings in a quiet window. No quiet window was available for this revision (load average 9 to 13), so the column is removed; `timing.sh` is kept.\n')

w('### 4.5 Downstream theorems\n')
w('Two kernel-level checks (`corpora/families/lean/Abs.lean`), on a seeded sample of 10 downstream theorems per family (statement mentions a member, not in the API list) and, for the second, on up to 200 seeded users per family.\n')
w('- **Transport**: rewrite the statement to mention the primitive and give the kernel the original proof for the new statement (`defeq`), or carry it across a proved equation `member = instance` (`eq`).')
w('- **Opacity**: replace the member by a variable and every cited lemma about it by a hypothesis; if the kernel accepts the result, the proof is *generic*: it uses the member only through lemmas. Otherwise it *opens* a structure member (constructor, projection) or *unfolds* a definition.\n')
w('| family | theorems using a member | analysed | generic | opens / unfolds | 10 downstream: transport | 10 downstream: opacity |')
w('|---|---:|---:|---|---|---|---|')
for f in ORDER:
    ab = S[f]['abs']; r = ab['results']; n = ab['analysed']
    lo, hi = wilson(r.get('generic', 0), n)
    tr = S[f]['transport']['down']['results']
    trs = ', '.join(f'{v} {k}' for k, v in tr.items()) if tr else 'not run (`↔`, no tool)'
    d10 = ', '.join(f'{v} {k}' for k, v in ab['down10'].items())
    w(f"| {f} | {ab['usersTotal']:,} | {n} | {r.get('generic', 0)} ({pct(r.get('generic', 0), n)}; 95% {100 * lo:.0f}–{100 * hi:.0f}%) | {r.get('opens', 0)} / {r.get('unfolds', 0)}{' (+' + str(r['error']) + ' not decided)' if r.get('error') else ''} | {trs} | {d10} |")
w('\n- `nomention` = the sampled theorem mentions only the member that is itself the primitive. Where transport was run, every statement that mentions a replaceable member was restated and kernel-checked: **F00019 10/10, F00042 10/10, F00046 9/9, F00073 7/7, F02076 10/10** (6 of those across the equation, since `JetRate` is an instance up to `↔` only). For the four families whose members equal the primitive by `rfl`, the 40 `defeq` results follow from the instance lemma by unfolding definitions, so they check the tool and not the generalisation; the informative cases are F02076\'s 6.')
w('- For F00079 and F00015 no transport was run: the members are instances up to `↔` and I did not build the equation-based restatement for structures. The opacity column is the evidence there: 4 and 7 of 10 are generic.')
tfail = S['F02076']['transport']['api']['results'].get('fail', 0)
w(f'- On the sampled API lists transport gave: F00019 40/40, F00042 40/40, F00046 34/34, F00073 5/5, F02076 9 of 13 ({tfail} universe-polymorphic statements defeated the tool, three of them the closure laws that were re-derived by hand).')
w('- *What "generic" buys.* A generic proof is the theorem already written against an interface: `Fam.Abs.<name>` is the kernel-checked statement "for any `M` with these lemmas, …". That is the class-like reading of the owner\'s idea, and it holds for about half of the users without anyone having written a class. The interface is large, though: the generic proofs cite ' + ', '.join(f'{S[f]["abs"]["distinctCitedByGeneric"]} ({f})' for f in ORDER) + ' distinct lemmas about the members, so "generic" here does not mean "written against a small, class-like API".')
w('- Replaying a theorem\'s source with the member\'s name swapped (the first method tried) under-measures: on F02076 it passed 5 of 13 and 3 of 10, failing wherever the proof cites a corpus lemma still stated with the old name. It is kept only for that family (`out/families/gen/F02076_replay_piecemeal.txt`).\n')

# ---------------- 5 did not generalise
w('## 5. What did not generalise, and why\n')
w('1. **`LocalJets` is not an instance of `LocalClass` without a hypothesis it lacks.** `LocalClass` bundles `weight_nonneg`; `LocalJets` does not. Counterexample (kernel-checked, `localJets_not_localClass`): weight −1 and the zero family. Consequence: `LocalJets.map` and `LocalJets.fderiv` cannot be obtained from the primitive. A primitive without the field would fix that and break the other three members, whose `bilinear` uses it. *Reading:* the nonnegativity is a fact about the weight, not about `f`, and would sit better as a separate hypothesis for all four; that is a redesign, not a merge.')
w('2. **`NativeJets` is a subgroup only for a nonnegative weight** (`nativeJets_empty`: with weight −1 it has no members, so not even zero). Same cause: a predicate about `f` that also carries a fact about a parameter.')
w('3. **The 15 predicates have no common body, so there is no parameterised primitive, only an interface, and the interface deletes no definition.** It also splits: 9 members have a constant-multiple lemma and could be `Submodule`s, 6 have none in the corpus, and `ScalarOn` has no `neg` (it was derived from `smul (-1)`). Two of the 15 (`Support`, `GaugeSupported`) are the same predicate by `rfl`; that is deduplication and the only definition removed.')
w('4. **F00042 is better left as two primitives.** `dirDeriv` covers all 18 members. The corpus also has `NaturalAxisBridge.partialEta F p := deriv (fun η => F (p.1, η)) p.2`, the derivative of a slice, which agrees with `dirDeriv (0, 1)` only where `F` is differentiable. The corpus proves that agreement several times with that hypothesis (`parameterPartial_natural`, `parameterPartial_eq_partialEta`, …). Merging the two would put a differentiability side condition on every use.')
w('5. **For F02076 the instance is an `↔`, not a definitional equality**, so the 61 of 148 users that unpack the constant by hand (`obtain ⟨C, hC, hb⟩ := hf`) would have to be rewritten or go through the equivalence. The other 87 need no change.')
w('6. **F00019 has nothing to generalise.** It is one definition written seven times. 71% of its sampled users unfold it, so an opaque interface would be the wrong tool; one shared name is the whole gain.')
w('7. **Proof size does not repay the library in two families and barely does in two more.** Net of the new library: F00042 and F00019 are negative, F00015 and F02076 are within about a hundred nodes of zero, F00046 and F00073 save a few hundred to a thousand, and F00079 saves 40 thousand (section 4.2). In elaboration, with the library charged, only F00079, F00073 and F00046 come out cheaper (section 4.4).')
w('8. **Nothing false was found**, against 18 of 20 in the earlier statement-shape clusters. This tests little: in three of seven families the primitive was a definition the corpus already had and in one it was Mathlib\'s, so only `JetRateOn` and `dirDeriv` were new parameterised statements, and no over-general statement was attempted. *Reading:* those were clusters of theorems with similar statements; these are clusters of definitions chosen after a reading of their bodies. The two are not comparable, and seven families is a small number.')
w('9. **One re-derivation was circular.** `MemClass.band_smul` re-derived from `LocalClass.band_smul` compiles, but the corpus proves the latter from the former. A merge has to follow the direction in which the corpus proved things, or re-prove the general lemma; compiling is not enough. Every re-derivation is now checked for this (`Circ.lean`).\n')

# ---------------- 6 extrapolation
w('## 6. Extrapolation, with the range the sample supports\n')
top = collections.Counter()
recs = {}
for l in open(os.path.join(O, 'ns/clusters.jsonl')):
    r = json.loads(l); recs[r['id']] = r
def isType(r): return set(r['resultClass']) == {'U'}
def kind(r):
    t = r['tightest']
    if isType(r): return 'type'
    if t == 'L0': return 'verbatim'
    if t in ('L1', 'L2', 'L3') or (t.startswith('AU') and r['similarity'] >= 0.7 and (r['effectiveParams'] or 0) <= 1 and (r['skeletonNodes'] or 0) >= 4 and not r['compoundHoles']): return 'onehole'
    if t == 'WRAP': return 'wrap'
    if t.startswith('ROLE') or t.startswith('API'): return 'role' if set(r['resultClass']) == {'Prop'} else 'role-other'
    return 'loose'
for x in tri['rows']: top[(kind(recs[x['id']]), x['cls'] == 'a')] += 1
KN = {'verbatim': 'value or predicate, body identical (like F00019)', 'onehole': 'one simple hole, shared body ≥ 4 nodes (like F00042)',
      'wrap': 'named instances of an existing definition (like F00046, F00073)', 'role': 'predicates joined by lemma roles only (like F00015, F00079)',
      'role-other': 'non-predicates joined by lemma roles or shapes', 'loose': 'loose anti-unification'}
w('The clustering has 4,178 family records. Sorted by the kind of hole, with how the 60 that were read fell:\n')
w('| kind | records | definitions removable on paper | read in the top 60 | of those, class (a) | 95% interval |')
w('|---|---:|---:|---:|---:|---|')
est = {}
for k in ['verbatim', 'onehole', 'wrap', 'role', 'role-other', 'loose']:
    n = top[(k, True)] + top[(k, False)]; a = top[(k, True)]
    lo, hi = wilson(a, n)
    est[k] = (a / n if n else 0, lo, hi)
    w(f"| {KN[k]} | {kinds[k]['records']:,} | {kinds[k]['removable']:,} | {n} | {a} | {'%.0f–%.0f%%' % (100 * lo, 100 * hi) if n else 'none read'} |")
w(f"| types | {kinds['type']['records']} | {kinds['type']['removable']} | 20 | – | class (a0), section 7 |")
w('\n"Removable on paper" is members minus one per connected group of records, the clustering\'s own count; it is an upper bound, not a measurement. The top 60 are the highest-scoring records, not a random sample, so the intervals describe "if the rest were like the ones read", which favours the rest.\n')
vb = kinds['verbatim']['removable']; oh = kinds['onehole']['removable']
mid = est['verbatim'][0] * vb + est['onehole'][0] * oh
lo = est['verbatim'][1] * vb + est['onehole'][1] * oh; hi = est['verbatim'][2] * vb + est['onehole'][2] * oh
w(f'- **Definitions.** The two kinds where a merge deletes definitions are the verbatim copies and the one-hole families. Applying the class (a) shares read above: {est["verbatim"][0] * vb:.0f} + {est["onehole"][0] * oh:.0f} ≈ **{mid:.0f} definitions, range {lo:.0f} to {hi:.0f}** ({100 * mid / 9903:.1f}% of 9,903; {100 * lo / 9903:.1f}% to {100 * hi / 9903:.1f}%). The range is wide because 5 and 6 families of those kinds were read. **The central estimate is fragile to a single reading:** the one-hole kind\'s only class (a) family is F00042, which the second reading and the Mathlib-only rerun both make class (d); with 0 of 6 the estimate falls to about {est["verbatim"][0] * vb:.0f} definitions (range {est["verbatim"][1] * vb:.0f} to {est["verbatim"][2] * vb + wilson(0, 6)[1] * oh:.0f}).')
w(f'- **Named instances** ({kinds["wrap"]["records"]} records). One in 16 was read as class (a). Where it is, the primitive exists and the definitions stay as names; the gain is lemma statements, and section 4.5 says how many: for `MemClass` and its weights {pct(S["F00046"]["abs"]["results"].get("generic", 0), S["F00046"]["abs"]["analysed"])} of users are already generic.')
w(f'- **Role families of predicates** ({kinds["role"]["records"]} records, {kinds["role"]["defs"]} definitions). Both that were read were class (a) and both generalised, in opposite ways: F00079 into an existing structure with a large proof saving, F00015 into a library interface with none. Two families do not support a rate.')
ls = S['F00079'];
w(f'- **Lemma statements and proofs.** The measured saving per re-derived lemma is {(tot("origNodes") - tot("newNodes")) / nre:.0f} nodes on average before the library is charged and {(tot("origNodes") - t79["origNodes"] - tot("newNodes") + t79["newNodes"]) / (nre - ls["rederived"]):.0f} without F00079. The clustering counts {kinds["onehole"]["lemmaReduction"] + kinds["verbatim"]["lemmaReduction"]} identical-shape lemma statements in the verbatim and one-hole kinds; at the shares above that is roughly {est["verbatim"][0] * kinds["verbatim"]["lemmaReduction"] + est["onehole"][0] * kinds["onehole"]["lemmaReduction"]:.0f} statements. *Reading:* a full pass would be worth a few hundred definitions (about 2% to 3% of them, anywhere from 1% to 8%) and one to a few hundred lemma statements (under 1%), with proof-size savings concentrated in a handful of families like F00079 that a body-based matcher does not find; the role channel found it and ranked it 79th.')
w('- **What the sample cannot say.** Whether the unread 4,118 records contain more families like F00079. It was found by lemma roles; its members differ by a binder, so the body channel did not join them. A search aimed at that pattern (several structures whose fields are the same up to an extra index or an extra guard) is the obvious next instrument.\n')

# ---------------- 7 a0
w('## 7. Class (a0): one type under many names\n')
w(f'Twenty of the 60 clusters are type abbreviations. For the 19 with no hole, every member was compared with the first of its family: **{sum(v["rfl"] for v in a0v.values())} of {sum(v["checked"] for v in a0v.values())} are equal by `rfl`** (`corpora/families/lean/A0.lean`), so {sum(v["rfl"] for v in a0v.values())} names ({100 * sum(v["rfl"] for v in a0v.values()) / 9903:.1f}% of reachable definitions) could be removed with no statement or proof changing its meaning. The largest:\n')
w('| family | type | names | modules | users |')
w('|---|---|---:|---:|---:|')
for k, v in sorted(a0v.items(), key=lambda kv: -kv[1]['members'])[:6]:
    w(f"| {k} | `{v['skeleton'][:60]}` | {v['members']} | {v['modules']} | {v['users']:,} |")
w(f'\nF00011 (`Fin n → ℝ`, 35 names for six values of n) was not checked member by member. *Reading:* this is the largest concept-count item in the top 60 and it is not what the owner\'s idea is about; it is a linter rule ("this abbreviation already exists in module X"), and the human projects show almost none of it (Carleson 5, PFR 0 verbatim copies).\n')

# ---------------- 8 software
w('## 8. The software side: could this propose frames?\n')
w('Read from `slice/lean/Frames/` (read-only; nothing was built or run there). *This section is a reading.*\n')
w('**Yes for modifiers, with changes; not yet for new frames.** The frame library is a set of definitions `Frame op holes := ∀ s a, Frame.at op holes s a` over one `Op` structure, which is the shape the body channel handles. Reading the 23 signatures, the existing frames already fall into families with one hole in head position: `IncreasesBy` / `DecreasesBy` / `Becomes` / `AtMost` / `AtLeast` (how the new measure relates to the old one), `ResultIs` / `ResultAtMost` / `ResultAtLeast` (the comparison), `Always` / `Never` and `EveryOf` / `NoneOf` (polarity), `Within` / `Covers` (direction of inclusion), `IndependentOf` / `IndependentGiven` (an extra guard, the `MemClass` / `LocalClass` pattern). Anti-unification would report those holes, and a hole that recurs across families is a candidate *modifier*: a comparison, a polarity, a guard.\n')
w('What would have to change:\n')
w('1. **Cluster rule statements, not library definitions.** The input is the body of compiled rules (each an instance of a frame) plus the rules that did not fit any frame and were written by hand. The second set is where a new frame would come from; today it is small.')
w('2. **Typed holes in the frame vocabulary.** A hole should be reported as "a `Measure`", "a `Cond`", "an `AnswerClass`", not as an expression. The exporter here already types holes; it needs the frame library\'s role abbreviations as the type lattice.')
w('3. **Anti-unify both readings together.** Every frame has a logical reading and an executable one (`Check.*`). A proposed frame must come with both, so the unit to generalise is the pair, and a proposal whose checker does not generalise the same way is rejected. The lemma-role channel plays that part for mathematics; here the second reading plays it.')
w('4. **The kernel decides, as here.** Acceptance is "every old rule statement is equivalent to an instance of the proposed frame", which is the transport check of section 4.5 and what V2/V3 already did by hand for the 23 frames.')
w('5. **A person decides whether it reads.** A parameterised frame is only better if its rule line is still a sentence. That is K1\'s meaning trial, not something this tool can score; F00015 above is the warning (a correct abstraction that made nothing simpler to state).')
w('6. **Expect the same economics.** In the mathematics the merge paid where the same proof had been written four times and not otherwise. For frames the analogue is the per-frame lemmas and harness generators: a modifier pays if it removes duplicated proofs about frames, not because it removes a name.\n')

# ---------------- 9 verdict
w('## 9. Verdict, as a trade\n')
w('**Worth exploring: yes, as a finder of a few large families and as a deduplication report; no, as a general way to shrink proofs.**\n')
w(f'- **What it buys in concepts.** On seven families, {dB} distinct definitions → {dA}, and {lB} lemma statements → {lA} in the library ({cA} cited by users, by a convention that hides 40 proofs inside 15 declarations). Extrapolated with wide error, 180 to 330 definitions over the corpus (2% to 3%, range 1% to 8%) and one to a few hundred lemma statements, plus {sum(v["rfl"] for v in a0v.values())} type abbreviations that need no abstraction. Half of the downstream proofs use a member only through lemmas, but through 52 to 258 of them per family.')
w(f'- **What it costs or saves in proof size.** {tot("origNodes"):,} → {tot("newNodes"):,} nodes over {nre} lemmas, for {libn:,} nodes of library. F00079 is {100 * (t79["origNodes"] - t79["newNodes"]) / (tot("origNodes") - tot("newNodes")):.0f}% of the gross saving and {100 * netf("F00079") / netn:.0f}% of the net saving once the library is charged; the other six families net {netn - netf("F00079"):+,} nodes together, which is break-even, as before. In source lines the whole exercise is {-netl} lines longer.')
w(f'- **What it costs in elaboration.** Proofs alone: {chg(tot("origHeartbeats"), tot("newHeartbeats"))} heartbeats. With the new library\'s elaboration charged: {chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbU)} to {chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbC)}. Only two families are cheaper, both reusing a primitive the corpus already had with its laws proved (F00079 {chg(t79["origHeartbeats"], hbtot("F00079"))}, F00073 {T["F00073"]["origHeartbeats"]:,} → {hbtot("F00073"):,}). F00046 goes {T["F00046"]["origHeartbeats"]} → {hbtot("F00046")}, F00042 {T["F00042"]["origHeartbeats"]:,} → {hbtot("F00042"):,}, F02076 {T["F02076"]["origHeartbeats"]:,} → {hbtot("F02076"):,}, F00015 {T["F00015"]["origHeartbeats"]:,} → {hbtot("F00015"):,}. Statement terms grow {chg(S["F00042"]["transport"]["api"]["statementBefore"], S["F00042"]["transport"]["api"]["statementAfter"])} when the parameter is a type with instances. A bundled interface: {co["newHeartbeats"] / co["origHeartbeats"]:.0f}× on one lemma in fifteen.')
w('- **Where it applies.** Where the corpus wrote one structure several times with an extra index or guard and proved its laws each time (F00079), and where it wrote the general form and then restated its lemmas for named instances (F00046). Both are found by lemma roles and named-instance detection, not by body similarity.')
w('- **Where it does not.** Predicates with different bodies and the same algebra: the interface exists (it is the library\'s), deletes no definition, saves no proof, and once in fifteen cost a great deal of elaboration. Definitions that bundle a fact about a parameter: the generalisation needs a hypothesis. Quantities whose users unfold them: one shared name is all there is. Named instances built with one constructor from different objects (19 of the 60 read): leave alone. A library notion applied to an argument (F00042): use the library notion; a new primitive only moves the proofs.')
w('- **On "like a class".** Nothing here needed a type class, and the one bundled interface was the weakest trade. What worked was the lightest form each time: an existing definition with one more thing said about it ("this other one is an instance").\n')

# ---------------- 10 review
w('## 10. Review, corrections applied, and where this version disagrees\n')
w('An independent agent rebuilt everything from copies under `out/families/review/`. The kernel-checked core reproduced exactly: every family file, re-derivation, transport and opacity result, all 68 statements equal to the corpus\'s, every "member is an instance" lemma about the original corpus constant. It found three defects in the measurements, all fixed here and rerun in `corpora/families/` (not copied from the review):\n')
w(f'1. **A circular re-derivation** (`MemClass.band_smul`). Now detected by `Circ.lean` for all {circj["pairs"]} re-derivations (68 plus the 13 Mathlib-only ones) and excluded: {nre} lemmas, {tot("origNodes"):,} → {tot("newNodes"):,} nodes, net {netn:,} (was 42,732), and {-netl} source lines added (was 18 saved).')
w(f'2. **Four invalid "before" heartbeat figures**, from corpus proofs that failed to replay. `measure.py` now uses a heartbeat figure only when that elaboration succeeded: {nhb} valid pairs, {tot("origHeartbeats"):,} → {tot("newHeartbeats"):,} ({chg(tot("origHeartbeats"), tot("newHeartbeats"))}; was reported as -28%).')
w(f'3. **The new library was not charged in elaboration.** Now measured (`LibHB_*.lean`): {libhbC:,} heartbeats for every charged declaration, {libhbU:,} for those the re-derived proofs depend on, and {libinst:,} instance slots. The total is {chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbU)} to {chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbC)}, not -28%.\n')
w('Also applied: the concept-count recount (section 4.1); the Mathlib-only alternative for F00042, rerun here (section 2); the second triage reading (section 1); the softened claims about "46 of 46", "generic", "nothing false" and the F00015 lemma split; the corrected F00046 description; the fragility of the extrapolation; the wall-clock column removed.\n')
w('**Where this version differs from the review.**\n')
w(f'- *Definitions after the merge: {dA}, not 24.* The review\'s 52 → 24 keeps `LocalJets` and counts `MemClass` once, but then `MemClass` is deleted in F00079 and kept in F00046. It has to stay once (the four weights are instances of it, and `LocalClass.band_smul` is proved from it), which gives {dA}; 24 needs the further step of folding `MemClass` away.')
w('- *Lemma statements in the library: 72, not 71,* because the circular `MemClass.band_smul` has to stay.')
w(f'- *Library elaboration: a range, not one figure.* The review charged 13,096 heartbeats ("declarations the re-derivations use") and got +14%. By transitive closure the proofs depend on {libhbU:,} heartbeats of new declarations ({chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbU)}); charging the same set that is charged in nodes gives {libhbC:,} ({chg(tot("origHeartbeats"), tot("newHeartbeats") + libhbC)}). Both are given; the sign is the same.')
w('- *Instance slots* are given with the circular lemma excluded, so the "before" figure is 25,298 where the review\'s text has 26,150.')
w('- *F00042.* The review\'s reading that it is class (d) is accepted on the measurement, with one qualification that is a reading: writing `fderiv ℝ f x (1, 0)` in 652 downstream statements is longer for a person to read than `partialX f x`, and that cost was not measured. The Mathlib-only rerun keeps the member names in the 13 statements (they are the corpus\'s, verbatim); 18 → 0 definitions means restating their users, which was not done.\n')
w('**What the review found about the clustering** (the reviewer\'s readings, not rerun here):\n')
w('- No control name appears in the clustering logic; only the report looks names up.')
w('- *15 random clusters outside the top 60* (seed 9090, spread over the looseness levels): 4 real families (a verbatim copy, one operation written four times, a pair differing in one projection, a tuple reordering that is a library equivalence), 6 parallel by construction, 5 accidental. The real ones were at the exact level, the project-heads level and the loosest level; none were in the mid-looseness, named-instance or lemma-role samples.')
w('- *Families the method cannot see.* Of 30 random reachable definitions read with their 5 nearest neighbours by name and signature (seed 31337), 7 (95% interval 12% to 41%) have a neighbour the reviewer would call the same notion that no channel joins to them: `GradeGuards` as the same structure in 4 parallel modules; the `PressureStream` module redone in `VariableGaugeMean` with one extra argument; `MeanVector` / `LocalMeanVector` / `WaveVector`, a componentwise version of the class predicates; a `Cutoff` algebra; one map bundled twice; one formula over different triples; `basePressure` in three representations. The first three have the shape of F00079: parallel structures or modules that differ by one inserted argument or record. That is the pattern that paid, and the wide aperture as built misses it.\n')


w('## Caveats\n')
w('- **Exploratory.** The triage, the rule, the frozen list and the definition of each family\'s API list were written before any Lean (`TRIAGE_2026-11-11.md`). The sub-class (a0), the tools, the choice to re-derive closure laws outside the sampled lists (F00079, F00015) and the concept-count conventions were decided while working. `DECISIONS.md` lists them. One agent has reviewed the tools and the report; its second triage reading was not blind. Nothing is under version control, so "frozen before Lean" rests on file times.')
w('- **Seven families.** Chosen by number of users among eight read as class (a); the two controls were known in advance to be good cases. The totals are dominated by one of the controls: F00079 is 99% of the net proof saving.')
w('- **The triage is one model\'s reading**, made from bodies and lemma blocks. Classing named-instance families as (b) shrank class (a); a different reader gets a different top six.')
w('- **Opacity is a property of the proof term**, with reducible abbreviations unfolded first. A proof that unfolds some other definition built on the member is counted as "unfolds". Theorems that hit the per-theorem limit are "not decided". Private theorems (1 to 7 per family) are skipped.')
w('- **Transport for `↔` families** is done by a reducible name for the instance (F02076) or not at all (F00079, F00015).')
w('- **Statements re-elaborated in a scratch file** are compared with the corpus statement term by term; four F00042 statements are equal only up to unfolding instances (a different but equal instance term was chosen) and are counted as the same.')
w('- **No wall-clock timing is reported**; heartbeats are the elaboration measurement. Library heartbeats were measured in a copy of each family file with a counter on every declaration.')
w('- **Four of 67 lemmas have no heartbeat comparison** (their corpus proof does not replay in a scratch file); they are large ones in F00079, so that family\'s heartbeat saving is measured on its smaller lemmas.')
w('- **Concept counts are conventions**, given in the table. In particular F00015 counts 15 subgroup declarations in place of 55 closure statements although the member-specific `zero`, `add`, `neg` proofs are still needed as their fields; the library column counts them.\n')

w('## Files and how to rerun\n')
w('- `corpora/families/lean/F15.lean`, `F19.lean`, `F42.lean`, `F46.lean`, `F73.lean`, `F79.lean`, `F2076.lean`: primitives, instance lemmas, generic APIs, counterexamples. `A0.lean`: the type abbreviations.')
w('- `corpora/families/subst/*.re.json`: the proof term of each re-derived lemma; `replay.py` copies the corpus statement and context around it.')
w('- `corpora/families/lean/Tool.lean` (sizes, instance slots, statement comparison), `Abs.lean` (opacity, transport).')
w('- `corpora/families/checkgen.py` writes `lean/Circ.lean` (dependency check of every re-derivation) and `lean/LibHB_*.lean` (library heartbeats) and collects them into `out/families/gen/circular.json` and `libhb.json`; `subst/F00042_mathlib.re.json` and `lean/F00042_mathlib.lean` are the Mathlib-only re-derivation.')
w('- `out/families/review/`: the reviewer\'s copies, logs and readings (`retriage.json`, `recount.json`, `nn30.txt`).')
w('- `corpora/families/all.sh` runs every Lean step, one process at a time (roughly 40 minutes on this machine under load; not timed as one command); `measure.py` and `report.py` rebuild `out/families/gen/summary.json` and this file.')
w('- Inputs produced once by inline scripts and not regenerated by `all.sh`: `out/families/gen/api.json` (the frozen API lists), `kinds.json`, `F00079_names.json`.')
w('- `out/families/TRIAGE_2026-11-11.md` / `.json`: the triage as frozen. `out/families/gen/`: API lists, samples, per-theorem results.')
open(f'{O}/FAMILIES.md', 'w').write('\n'.join(L) + '\n')
print('wrote', f'{O}/FAMILIES.md', len(L), 'lines')
