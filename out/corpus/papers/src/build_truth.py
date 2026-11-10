#!/usr/bin/env python3
"""Assemble out/corpus/papers/truth.json from the hand-written item files.

    python3 out/corpus/papers/src/build_truth.py

items_ns.py / items_euler.py hold, per numbered paper item, a paraphrase, the paper's proof steps
and the Lean declarations it is mapped to (with evidence and a confidence).  This script resolves
every mapped name against out/corpus/ns/decls.jsonl (the export from Lean), applies the corrections
that came out of the 20-mapping verification, and writes truth.json.  It fails if a name does not
resolve to exactly one exported declaration.
"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, HERE)
from items_ns import NS
from items_euler import EULER

SEED = 20261110
ORDER = {'certain': 3, 'probable': 2, 'guess': 1}

SOURCES = [
 dict(paper='ns', title='Finite time blowup for Navier-Stokes', authors='OpenAI',
      url='https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf',
      pages=166, bytes=2959204, sha256='0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f',
      pdfCreationDate='2026-09-08 15:06:26 EDT', httpLastModified='Tue, 08 Sep 2026 19:09:35 GMT',
      etag='0x8DF0DDCB8C364FC', fetched='2026-11-10', linkedFrom='corpora/ns/README.md, corpora/ns/formalization.yaml'),
 dict(paper='euler', title='Finite time blowup for the Euler equation', authors='OpenAI',
      url='https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf',
      pages=57, bytes=535142, sha256='a0c234518e6c489e16996805023eb2e75c00b7c03455f7a3a5be2c124954bfdd',
      pdfCreationDate='2026-09-08 15:07:51 EDT', httpLastModified='Tue, 08 Sep 2026 19:13:09 GMT',
      etag='0x8DF0DDD3828C8B8', fetched='2026-11-10', linkedFrom='corpora/ns/README.md, corpora/ns/formalization.yaml'),
]

# Old manuscript numbering cited in Lean docstrings -> numbering of the published paper.
# basis: 'statement' = Lean statement read against the paper; 'content' = docstring/module text
# matched to the paper's content; 'topic' = module topic only.
RENUMBERING = {
 'ns': [
  dict(old='Candidate Theorem 1.1', new='Theorem 1.1 / Corollary 10.6', lean='NavierStokes/ProblemStatement.lean (periodic candidate target); NavierStokes/R3/* cite the current numbering', basis='content', confidence='certain'),
  dict(old='equations (3)-(5)', new='(3.2), (4.2), (4.7)', lean='NavierStokes/CoordinateAlgebra.lean, SimilarityCoordinates.lean', basis='content', confidence='probable'),
  dict(old='Proposition 3.2', new='Proposition 4.2', lean='NavierStokes/LeadingStress.lean', basis='content', confidence='probable'),
  dict(old='equations (6)-(9); Lemma 3.3', new='(4.9)-(4.16); Lemma 4.3', lean='NavierStokes/StressAlgebra.lean, ProfileHistories.lean, OutgoingHistories.lean', basis='content', confidence='probable'),
  dict(old='Lemma 3.5; equations (10), (11)', new='Lemma 4.5; (4.20)-(4.22)', lean='NavierStokes/ConeAlgebra.lean, UniformCone.lean; restated under the TeX label seed:cone-test in SeedConePaper.lean', basis='statement', confidence='certain'),
  dict(old='Lemma 3.6', new='Lemma 4.7 (first part) = Lemma A.1', lean='NavierStokes/PowerMomentMatrix.lean', basis='statement', confidence='certain'),
  dict(old='Lemma 3.7', new='Lemma 4.7 (second part) = Lemma A.2', lean='NavierStokes/MomentRepair.lean', basis='content', confidence='probable'),
  dict(old='Sections 4.4, 4.6; equation (13)', new='Appendix A.2-A.3 (outer schedule), A.6-A.7 (flat edge)', lean='NavierStokes/RadialSchedule.lean, FlatCutoff.lean', basis='topic', confidence='guess'),
  dict(old='Proposition 5.1; equation (17)', new='Proposition B.2', lean='NavierStokes/AxisProfile.lean, AxisSeries.lean, NaturalAxisBridge.lean', basis='content', confidence='probable'),
  dict(old='Lemma 5.2', new='Lemma B.4', lean='NavierStokes/ReferenceBounds.lean', basis='content', confidence='probable'),
  dict(old='Lemma 6.1', new='Lemma C.1 (used through Lemma 4.11)', lean='NavierStokes/LoopMoments.lean, LoopVariance.lean', basis='content', confidence='probable'),
  dict(old='Proposition 6.2', new='Proposition C.2', lean='NavierStokes/RadialModulation.lean', basis='content', confidence='probable'),
  dict(old='equation (20)', new='Theorem 4.6(ii) weighted bound; weight (C.18)', lean='NavierStokes/LeadingStressWeights.lean, ActiveAnnulusWeight.lean', basis='statement', confidence='probable'),
  dict(old='equations (21), (22)', new='(5.2)-(5.6)', lean='NavierStokes/SlowDivergence.lean, SlowExpansionResidual.lean, PositiveAxisSystem.lean', basis='topic', confidence='guess'),
  dict(old='equation (24)', new='(5.41)', lean='NavierStokes/MeanResidual.lean, CorrectionState.lean', basis='content', confidence='probable'),
  dict(old='Definition 8.1; Section 8.1; equation (25)', new='Section 6.1, phase map (6.3), operators (6.4)-(6.6)', lean='NavierStokes/GraphCalculus.lean, PhysicalGraphBounds.lean', basis='content', confidence='probable'),
  dict(old='equation (26)', new='(7.3)', lean='NavierStokes/PhaseCalculus.lean', basis='statement', confidence='certain'),
  dict(old='Section 8.2', new='Section 6.2 (slow cutoffs and rectangles)', lean='NavierStokes/GaussianTailFlat.lean', basis='topic', confidence='guess'),
  dict(old='Lemma 8.3', new='Lemma 6.1', lean='NavierStokes/SlotGeometry.lean, SlotColoring.lean', basis='content', confidence='probable'),
  dict(old='Lemma 8.4; equation (27); Appendix A.3', new='amplitude equation (7.5) and Proposition 7.2', lean='NavierStokes/TangentProjection.lean, TangentODE.lean, PrimaryODE.lean', basis='content', confidence='probable'),
  dict(old='Lemma 8.5; Proposition A.4; equation (28)', new='Lemma 7.4; (7.21)', lean='NavierStokes/PulseGrowth.lean, GrowingMode.lean', basis='content', confidence='probable'),
  dict(old='Remark 8.6; Proposition A.2', new='no numbered counterpart (scaling of the carrier frequency, near (7.2))', lean='NavierStokes/Scaling.lean', basis='topic', confidence='guess'),
  dict(old='Lemma 8.7; Section 8.3; equation (29)', new='Proposition 7.5; (7.22)-(7.24)', lean='NavierStokes/Covariance.lean, TorusAverages.lean, PulseCovariance.lean', basis='content', confidence='probable'),
  dict(old='Lemma 8.8', new='Lemma 7.7', lean='NavierStokes/CurlGeometry.lean', basis='content', confidence='probable'),
  dict(old='Lemma 9.2', new='Lemma 7.7', lean='NavierStokes/CurlClassBounds.lean:757', basis='content: the module bounds the curl potential, normal coefficient and remainder classes of (7.38)-(7.39); published Lemma 9.2 is about interaction products', confidence='probable'),
  dict(old='Proposition 9.3', new='Proposition 9.1', lean='NavierStokes/LinearWaveBounds.lean', basis='content', confidence='probable'),
  dict(old='equations (32), (33), (34), (35)', new='(8.3), (8.12), (8.16), (8.25)', lean='NavierStokes/MeanIncrementBounds.lean, IntegratedMeanBalances.lean, MeanRankUpdate.lean, FiveRowRank.lean', basis='content', confidence='probable'),
  dict(old='Section 10.2', new='Section 7.3 (Proposition 7.6)', lean='NavierStokes/SignedCovariance.lean', basis='topic', confidence='guess'),
  dict(old='Proposition 10.3', new='Proposition 9.6', lean='NavierStokes/ExponentLedger.lean', basis='content', confidence='probable'),
  dict(old='Lemma 11.3', new='Lemma 5.4', lean='NavierStokes/DiagonalScale.lean', basis='content', confidence='probable'),
  dict(old='Proposition 11.4', new='Proposition 10.1 and Lemma 10.3', lean='NavierStokes/TimeLocalization.lean', basis='content', confidence='probable'),
  dict(old='Proposition 11.7', new='Section 10.4 (growth) and Theorem 1.1', lean='NavierStokes/BlowupImplication.lean', basis='content', confidence='probable'),
  dict(old='Theorem 1.1, Lemma 10.4 as cited in NavierStokes/R3/', new='unchanged (current numbering)', lean='NavierStokes/R3/Theorem.lean, R3/IntegratedDissipation.lean, R3/ProblemStatement.lean', basis='statement', confidence='certain'),
 ],
 'euler': [
  dict(old='equation (9)', new='mean problem (3.19)-(3.21)', lean='Euler/MeanStrongEquation.lean', basis='content', confidence='probable'),
  dict(old='equations (10)-(12)', new='transverse problem (3.27)-(3.29)', lean='Euler/TransverseStrongEquation.lean, SourceCylinderEquation.lean, TransverseForwardInverse.lean', basis='topic', confidence='guess'),
  dict(old='equation (13)', new='truncated expansion (3.34)', lean='Euler/FiniteGradeAssembly.lean', basis='topic', confidence='guess'),
  dict(old='equations (16), (17)', new='lifted equation and correction of Section 3.6 (Lemma 3.3)', lean='Euler/EulerProof.lean:12816, EulerCorrectionEquation.lean', basis='content', confidence='probable'),
  dict(old='equations (18), (19)', new='weight ratios of the norm (3.43)', lean='Euler/EulerProof.lean:513-528', basis='topic', confidence='guess'),
  dict(old='equations (26)-(27)', new='Section 4.2 (choice at the activation time)', lean='Euler/EulerProof.lean:10522', basis='topic', confidence='guess'),
  dict(old='equation (30)', new='(4.21), scalar form of the ideal system (4.20)', lean='Euler/EulerProof.lean:13042-13365', basis='statement', confidence='certain'),
  dict(old='equation (35)', new='(4.11)', lean='Euler/EulerProof.lean:17719', basis='content', confidence='probable'),
  dict(old='equation (36)', new='(4.12)', lean='Euler/EulerProof.lean:18563', basis='content', confidence='probable'),
  dict(old='equation (37)', new='(5.3)', lean='Euler/PacketSourceScaleChoice.lean', basis='content', confidence='probable'),
  dict(old='equation (39)', new='first scale requirement of Section 5.5 (P_j^Q <= k_j^{theta/100})', lean='Euler/PacketSourceScaleGuards.lean', basis='content', confidence='probable'),
 ],
}

# Outcome of reading 20 sampled mappings (random.Random(20261110).sample over all mappings in
# file order) against the paper.  verdict: match = Lean statement says what the paper item says
# (possibly in a more general form); partial = matches one clause, or statement too long to check
# every clause; weak = related object only.  'set' applies a correction to the mapping.
VERIFY = [
 ('ns','9.7','NavierStokes.WholeDomainStageBounds.commonQ_pos','partial','Lean: 0 < commonQ B N0. The paper also asserts every finite partial sum is defined below this scale; in Lean that is not a statement (functions are total). Relation changed from states to part.', dict(relation='part')),
 ('euler','6.3','OrdinaryEulerBKM:FiniteLifespan.vorticity_lintegral_eq_top','match','Lean: for any FiniteLifespan, the extended integral over [0, duration) of the vorticity sup norm is top. This is the second assertion of Theorem 1.1 in general form.', dict(confidence='certain')),
 ('ns','6.6','NavierStokes.WeightedClasses.MemClass.mul','partial','Lean: MemClass w alpha a and MemClass v beta b give MemClass (w v) (alpha+beta) (a b). Covers (6.30); the harmonic rule (6.31) and distinct-label vanishing are not in this statement.', {}),
 ('euler','(4.3)','EulerParentPacketFrames.SmoothState','weak','A record bundling evolution, Sobolev data, label data and oddness of a parent. It does not contain the shear decomposition M = B + h q p^T + E. Downgraded to guess.', dict(confidence='guess')),
 ('ns','C.3','NavierStokes.LeadingStressWeights.physical_jet_bound','match','Lean: every derivative of the stress on the open active interval is at most C zeta(X)/distance(X)^N, the weighted bound of Theorem 4.6(ii)/(C.18).', dict(confidence='certain')),
 ('ns','A.5','NavierStokes.PressureDatum.manuscript_prefix_bound','match','Lean conclusion: pressure g a eta <= -(5/2) P^2 ((1+eta^2)^-1)^2, which is (A.22) with f(eta) = 1/(1+eta^2).', dict(confidence='certain', relation='states')),
 ('ns','10.2','NavierStokes.JointResidualLimits.exists_smooth_compatible_limits','match','Abstract form: for f smooth before t = 1 with vanishing joint jets at the origin and extensions away from it, all derivatives converge locally uniformly to smooth limits L with L(0) = 0 and compatible derivatives. The paper states it for the force; the application is elsewhere.', {}),
 ('ns','(7.3)','NavierStokes.PhaseCalculus.phase','match','Signature (eps p pz x0 F G) and docstring agree with Phi = p theta + pz Z/eps + x0 R - v(pF + pz G). Establishes old (26) = new (7.3).', dict(confidence='certain')),
 ('euler','3.3','EulerLiftedEulerAlgebra.lifted_euler_residual','partial','An exact algebraic identity for the lifted velocity kappa F z; consistent with the lifted velocity z^a of Section 3.6 but not checked term by term.', {}),
 ('ns','10.3','NavierStokes.BorelExtension.exists_smooth_compact_extension','match','Lean: a smooth compactly supported function with prescribed derivatives at 0 (Borel). This is the series step of the proof, not the lemma.', {}),
 ('ns','8.2','NavierStokes.WeightedRadialPrimitive.supported_meanClass_canonical_transport','partial','Lean: the compact integral of a radially supported MeanClass alpha family is smooth, radially supported and MeanClass alpha. Matches the support and class clauses; identity (8.7) is not in this statement.', {}),
 ('euler','(3.19)','MeanStrongInverse:meanSolver_strong','match','Hypotheses include H <= K, the boundary form with L, and K T^2/2 + B T <= 1/2, i.e. (3.11) with B_c = 0; conclusion is a strong mean evolution with the projected equation and initial condition.', dict(confidence='certain')),
 ('euler','3.2','MeanStrongGevrey:StrongMeanEvolution.continuousVelocity_spatial_gevrey','partial','Factorial bound with fixed radius R for the mean velocity; statement is 2,216 characters and was read only to its hypotheses.', {}),
 ('ns','A.10','NavierStokes.TerminalCone.full_interval_direction_margin','match','Lean: 2 + h < profileSpeed <= 2 + 2h and cone gap >= 3/2 on the terminal interval; the paper has 2 + h < a <= 2 + 2h and a positive lower bound for 2 - (a-2)(Tz/Ttheta)^2 (Lemma 4.9, Proposition A.10).', dict(confidence='certain')),
 ('euler','(3.19)','EulerMeanVariationalInverse.StrongMeanEvolution','match','Record with label (displacement), velocity and L2 acceleration and the projected equation: the auxiliary displacement formulation of Section 3.3.', {}),
 ('ns','5.4','NavierStokes.GenericTupleRealization.exists_angular_realization','partial','Hypotheses (scale q with derivative bounds, base field, sequences of potentials A, direct angular parts B and scalars R with jet rates) match the lemma; the conclusion lies beyond the 2,000-character export limit.', {}),
 ('ns','A.1','NavierStokes.PowerMomentMatrix.powerEvaluationMatrix_det_ne_zero','match','Lean: distinct exponents and ordered positive nodes give a nonzero evaluation determinant, the pointwise fact integrated in the proof.', {}),
 ('euler','(4.20)','EulerPacketGrowth.equation30_cosh_lower','match','Lean ODE ((1+(beta s^2)^2) V\')\' = 2(1 - beta (beta t^2)) V with V(0) = 1, V\'(0) >= 0 is (4.21); conclusion V >= cosh(t/sqrt 2) is the growth estimate of Section 4.4. Establishes old (30) = new (4.21).', dict(confidence='certain')),
 ('ns','B.8','NavierStokes.MatchingDebtBounds.exists_ordered_matching_threshold','partial','Nested thresholds in the order j, Lambda, T, C agree with Remark B.9; the matching conclusion is beyond the export limit.', {}),
 ('ns','A.10','NavierStokes.TerminalCone.profile_cone_margin','match','Same three inequalities for 0 <= delta <= 5/2, i.e. on .5 <= y <= 3 including the edge.', dict(confidence='certain')),
]

CONF_DEF = {
 'certain': 'A docstring cites the item in the published numbering or by its TeX label, or the README/formalization.yaml names the declaration, or the Lean statement was read against the paper statement and says the same thing.',
 'probable': 'A docstring cites the item in the earlier manuscript numbering and the content was matched to the published item, or the docstring/statement describes the item\'s content without a citation.',
 'guess': 'Module or declaration name only.',
}
REL_DEF = {
 'states': 'the declaration is (a form of) the item\'s statement or its closing theorem',
 'part': 'the declaration proves one clause, step or algebraic identity of the item',
 'defines': 'the declaration defines the objects the item is about',
}


def load_decls():
    D = {}
    with open(os.path.join(REPO, 'out', 'corpus', 'ns', 'decls.jsonl')) as f:
        for line in f:
            d = json.loads(line)
            D[d['name']] = d
    return D


def make_resolver(D):
    byuser, bymod = {}, {}
    for d in D.values():
        byuser.setdefault(d['userName'], []).append(d)
        bymod.setdefault(d['module'], []).append(d)

    def resolve(s, paper):
        if ':' in s:
            mod, suf = s.split(':', 1)
            ds = bymod.get(('Euler.' if paper == 'euler' else 'NavierStokes.') + mod, [])
            if suf == '':            # module-level mapping: the last public theorem of the module
                th = sorted((d for d in ds if d['kind'] == 'theorem' and not d['isPrivate']), key=lambda d: d['line'] or 0)
                return (th[-1], True) if th else (None, False)
            c = [d for d in ds if d['userName'].endswith('.' + suf)]
            return (c[0], False) if len(c) == 1 else (None, False)
        c = byuser.get(s, [])
        if len(c) > 1:
            c = [x for x in c if not x['isPrivate']]
        if len(c) == 1:
            return c[0], False
        c = [d for d in D.values() if d['userName'].endswith('.' + s)]
        return (c[0], False) if len(c) == 1 else (None, False)
    return resolve


# (paper, item now, item at the time of the verification draw, mapping source name)
MOVED_AFTER_DRAW = [('ns', '7.7', '9.2', 'NavierStokes.CurlClassBounds.physical_normalCoefficient_class')]


def main():
    D = load_decls()
    resolve = make_resolver(D)
    flat = []                                   # all mappings in file order, for the seeded draw
    items = []
    for paper, src in (('ns', NS), ('euler', EULER)):
        for it in src:
            maps = []
            for (s, rel, conf, ev) in it['maps']:
                d, modlevel = resolve(s, paper)
                if d is None:
                    sys.exit(f'unresolved mapping {paper} {it["num"]} {s}')
                if modlevel:
                    ev += ' (module-level mapping; the declaration recorded is the last public theorem of the module)'
                m = dict(decl=d['name'], userName=d['userName'], module=d['module'], line=d['line'], declKind=d['kind'],
                         relation=rel, confidence=conf, evidence=ev, verified=None)
                maps.append(m)
                flat.append((paper, it['num'], s, m))
            items.append(dict(id=f'{paper}:{it["num"]}', paper=paper, number=it['num'], kind=it['kind'], section=it['sec'],
                              title=it['title'], paraphrase=it['para'], proofSteps=it['steps'], mappings=maps,
                              note=it.get('note')))
    # the seeded draw must reproduce the list that was verified
    # The draw was made before the independent check of 2026-11-10 moved one mapping from item 9.2
    # to item 7.7.  To reproduce it, that mapping is put back at its position at the time of the
    # draw (last mapping of ns 9.2).  Only the order used for the draw is affected.
    flat_at_draw = list(flat)
    for (paper, new_num, old_num, name) in MOVED_AFTER_DRAW:
        k = next(i for i, x in enumerate(flat_at_draw) if x[:3] == (paper, new_num, name))
        moved = flat_at_draw.pop(k)
        last = max(i for i, x in enumerate(flat_at_draw) if x[:2] == (paper, old_num))
        flat_at_draw.insert(last + 1, moved)
    drawn = [flat_at_draw[i][:3] for i in random.Random(SEED).sample(range(len(flat_at_draw)), 20)]
    if [tuple(x) for x in drawn] != [v[:3] for v in VERIFY]:
        sys.exit('verification list does not match the seeded draw; re-verify before publishing')
    index = {(p, n, s): m for (p, n, s, m) in flat}
    ver = []
    for (p, n, s, verdict, note, change) in VERIFY:
        m = index[(p, n, s)]
        before = dict(relation=m['relation'], confidence=m['confidence'])
        m.update(change)
        m['verified'] = verdict
        ver.append(dict(item=f'{p}:{n}', decl=m['decl'], verdict=verdict, note=note, before=before,
                        after=dict(relation=m['relation'], confidence=m['confidence'])))
    for it in items:
        best = max((ORDER[m['confidence']] for m in it['mappings']), default=0)
        it['confidence'] = {3: 'certain', 2: 'probable', 1: 'guess', 0: 'none'}[best]
        it['noCounterpart'] = None if it['mappings'] else (it['note'] or 'not found')
    tally = {}
    for v in ver:
        tally[v['verdict']] = tally.get(v['verdict'], 0) + 1
    out = dict(
        schema='lean-rosette/paper-truth/1',
        generated='2026-11-10',
        corpus=dict(repo='openai/NavierStokesAndEuler', commit='f9e8bc5b38b6e212696e8a30e3e91517af887bbd',
                    export='out/corpus/ns/decls.jsonl'),
        sources=SOURCES,
        builder='model (Claude), not a mathematician; paraphrases and mappings are unreviewed by a human',
        confidenceLevels=CONF_DEF, relations=REL_DEF,
        renumbering=RENUMBERING,
        items=items,
        verification=dict(method='random.Random(%d).sample over all mappings in file order (ns then euler; order as of the draw, before one mapping was moved from 9.2 to 7.7 by the independent check of 2026-11-10), 20 drawn; '
                                 'each Lean statement (as exported, up to 2,000 characters) read against the paper statement by the builder' % SEED,
                          seed=SEED, reader='the same model that built the mapping (not independent)', tally=tally, sample=ver),
    )
    path = os.path.join(REPO, 'out', 'corpus', 'papers', 'truth.json')
    with open(path, 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    n = sum(len(i['mappings']) for i in items)
    print(f'wrote {path}: {len(items)} items, {n} mappings, verification {tally}')


if __name__ == '__main__':
    main()
