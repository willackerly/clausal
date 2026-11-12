"""Independent rescoring of the V5 generated-echo bank from the stored files (reviewer, step 3)."""
import json, random, collections, sys, math
B = '/Users/will/dev/lean-rosette/trials/meaning/banks/generated-echoes-v1/'
key = json.load(open(B + 'key.json'))
items = json.load(open(B + 'items.json'))
flags = json.load(open(B + 'item_flags.json'))
readers = ['haiku-1', 'sonnet-1', 'opus-1', 'default-1']
resp = {r: json.load(open(B + f'responses/{r}.json')) for r in readers}
K = key['items']
ids = [it['id'] for it in items['items']]
assert set(ids) == set(K), 'item ids differ from key'
for r in readers:
    a = resp[r]
    assert a['material_sha256'] == key['material_sha256'], r
    got = [x['id'] for x in a['answers']]
    assert sorted(got) == sorted(ids) and len(got) == len(set(got)), r
J = {r: {x['id']: x['judgement'] for x in resp[r]['answers']} for r in readers}
mut = [i for i in ids if not K[i]['faithful']]
fai = [i for i in ids if K[i]['faithful']]
print('items', len(ids), 'mutated', len(mut), 'faithful', len(fai))
def caught(r, i): return J[r][i] == 'not-faithful'
tot_c = sum(caught(r, i) for r in readers for i in mut)
tot_f = sum(caught(r, i) for r in readers for i in fai)
print(f'caught {tot_c} of {len(mut)*4} ({tot_c/len(mut)/4:.3f}); false alarms {tot_f} of {len(fai)*4} ({tot_f/len(fai)/4:.3f})')
for r in readers:
    print(r, 'caught', sum(caught(r, i) for i in mut), 'fa', sum(caught(r, i) for i in fai),
          'other judgements', collections.Counter(J[r][i] for i in ids if J[r][i] not in ('faithful', 'not-faithful')))
kinds = collections.defaultdict(list)
for i in mut: kinds[K[i]['error_kind']].append(i)
for kd, its in kinds.items():
    print('kind', kd, its, sum(caught(r, i) for r in readers for i in its), 'of', 4 * len(its))
print('misses:', [(r, i, K[i]['error_kind']) for r in readers for i in mut if not caught(r, i)])
print('false alarms:', [(r, i) for r in readers for i in fai if caught(r, i)])
split = [i for i in ids if len({J[r][i] for r in readers}) > 1]
print('split items', len(split), split, 'unanimous', len(ids) - len(split))
print('flags file:', json.dumps(flags)[:600])
# bootstrap
rng = random.Random(1)
def boot(items_, readers_resample):
    vals = []
    for _ in range(10000):
        its = [rng.choice(items_) for _ in items_]
        rs = [rng.choice(readers) for _ in readers] if readers_resample else readers
        vals.append(sum(caught(r, i) for r in rs for i in its) / (len(its) * len(rs)))
    vals.sort(); return vals[249], vals[9749]
print('catch, items resampled', boot(mut, False), 'items+readers', boot(mut, True))
print('fa, items resampled', boot(fai, False), 'items+readers', boot(fai, True))
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d
print('wilson catch', wilson(tot_c, 60), 'wilson fa', wilson(tot_f, 120), 'wilson 12/12', wilson(12, 12))
