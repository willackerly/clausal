"""Independent recount of the V4 proxy-author numbers from trials/sentences/results.json (reviewer, step 3)."""
import json, collections, statistics, math
R = json.load(open('/Users/will/dev/lean-rosette/trials/sentences/results.json'))
rules = R['rules']
authors = ['opus-1', 'sonnet-1', 'haiku-1', 'default-1']
print('rules', len(rules), collections.Counter(r['author'] for r in rules))
print('meant true/false', sum(r['meantToBeTrue'] for r in rules), sum(not r['meantToBeTrue'] for r in rules))
print('as written', collections.Counter(r['as_written']['status'] for r in rules))
print('hint kinds', collections.Counter(r['as_written'].get('hint_kind') for r in rules),
      'nearest begins like rewording', sum(bool(r['as_written'].get('a_nearest_form_begins_like_the_rewording')) for r in rules))
fit = collections.Counter((r.get('rewording') or {}).get('fit') for r in rules)
print('fit', fit)
for a in authors:
    rs = [r for r in rules if r['author'] == a]
    f = collections.Counter((r.get('rewording') or {}).get('fit') for r in rs)
    print(a, len(rs), 'true', sum(r['meantToBeTrue'] for r in rs), dict(f))
whole = [r for r in rules if (r.get('rewording') or {}).get('fit') in ('exact', 'more')]
print('compile whole (exact+more)', len(whole))
miss = [r for r in rules if (r.get('rewording') or {}).get('missing')]
print('need a missing piece (any)', len(miss))
ed = [r['rewording']['edit_distance_words'] for r in rules if r.get('rewording') and r['rewording'].get('edit_distance_words') is not None and r['rewording'].get('fit') in ('exact','more','less')]
wo = [r['rewording']['words_original'] for r in rules if r.get('rewording') and r['rewording'].get('words_original') is not None]
print('edit distance n', len(ed), 'median', statistics.median(ed) if ed else None, 'min', min(ed), 'max', max(ed))
print('words original median (all 48?)', len(wo), statistics.median(wo))
wo_c = [r['rewording']['words_original'] for r in rules if r.get('rewording') and r['rewording'].get('fit') in ('exact','more','less')]
print('words original median over compiled', statistics.median(wo_c))
J = collections.Counter(); per = collections.defaultdict(collections.Counter)
for r in rules:
    for c in r.get('cases') or []:
        J[c.get('judgement')] += 1; per[r['author']][c.get('judgement')] += 1
print('case judgements', J, {a: dict(per[a]) for a in authors})
# found true/false as labelled
U = R['units']
ok = 0; n = 0; detail = []
for r in rules:
    rw = r.get('rewording') or {}
    if rw.get('fit') not in ('exact', 'more', 'less'): continue
    us = rw.get('units') or []
    found = [U[u]['found'] for u in us if u in U]
    n += 1
    false_found = any('false' in f and 'true-as-far' not in f for f in found)
    lab = r['meantToBeTrue']
    good = (lab and not false_found) or ((not lab) and false_found)
    ok += good
    detail.append((r['key'], lab, found, good))
print('found as labelled', ok, 'of', n)
print([d for d in detail if not d[3]])
print('unit found', collections.Counter(u['found'] for u in U.values()))
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return round((c - h) / d, 3), round((c + h) / d, 3)
print('wilson 27/48', wilson(27, 48))
