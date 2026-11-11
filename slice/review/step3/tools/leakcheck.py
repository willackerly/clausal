"""Leak check: identifier-like tokens that occur in private/tdflite-pilot and in slice/ text written after HEAD,
but not in slice/ at HEAD, not in the public docs, and not in the slice's Lean/Rust toolchain words.
Prints only counts and the file:line of hits (the token itself is printed only if it is also in public text)."""
import os, re, subprocess, sys, collections
ROOT = '/Users/will/dev/lean-rosette'
TOK = re.compile(r'[A-Za-z_][A-Za-z0-9_]{6,}')
TEXT = ('.md', '.lean', '.json', '.txt', '.py', '.yaml', '.tsv', '.feature', '.rs', '.toml', '.sh')
def toks_of_tree(base, skip=('.lake', 'go-scratch', 'target', 'node_modules', '.git', 'vendor', 'work', '__pycache__', 'raw_first_pass_under_overload')):
    out = collections.defaultdict(set)
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in skip]
        for f in fn:
            if not f.endswith(TEXT): continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 5_000_000: continue
                s = open(p, errors='ignore').read()
            except Exception: continue
            for t in set(TOK.findall(s)): out[t].add(p)
    return out
priv = toks_of_tree(ROOT + '/private/tdflite-pilot')
print('private tokens', len(priv), file=sys.stderr)
# public baseline: slice at HEAD plus docs/README/brainstorm/trials (public, committed) 
pub = set()
ls = subprocess.run(['git', '-C', ROOT, 'ls-files'], capture_output=True, text=True).stdout.split()
for f in ls:
    if not f.endswith(TEXT): continue
    try:
        s = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:' + f], capture_output=True, text=True, errors='ignore').stdout
    except Exception: continue
    pub |= set(TOK.findall(s))
print('public tokens at HEAD', len(pub), file=sys.stderr)
now = toks_of_tree(ROOT + '/slice', skip=('.lake', 'target', 'work', '.tools', 'review', '__pycache__', 'raw', 'raw_first_pass_under_overload', 'logs', 'wallet-shipped', 'probe'))
cand = {t: now[t] for t in now if t in priv and t not in pub}
print('slice tokens', len(now), 'candidates (in private, in slice now, not public at HEAD):', len(cand))
for t, ps in sorted(cand.items()):
    print(repr(t), len(priv[t]), 'private files;', sorted(p.replace(ROOT + '/', '') for p in ps)[:4])
