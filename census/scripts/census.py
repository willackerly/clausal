#!/usr/bin/env python3
"""K3 translation census driver.

    census.py run <crate>-<version> [--max-rounds N] [--no-lean]
    census.py all

For one crate (sources in crates/<crate>-<version>, never modified):
  1. copy the sources to work/run/<crate>/src         (the copy may get `#[charon::opaque]` marks)
  2. syntactic inventory of every `fn` (tools/fninv)  (the denominator, independent of Charon)
  3. round 0 = the tools as they are: charon cargo --preset=aeneas, then aeneas -backend lean
  4. "peel" rounds, only if round 0 produced no Lean at all:
       - rustc ICE under the Charon driver  -> mark the enclosing functions opaque, rerun
       - Aeneas fatal exception             -> exclude the declaration it names (Charon --exclude), rerun
     every mark and exclusion is recorded with the message that caused it
  5. lake build of the generated Lean (lean-pinned/, one module per crate)
  6. join everything per function and write data/results/<crate>.json

Nothing here needs network access once crates/ and the tools are in place.
"""
import json, os, re, shutil, subprocess, sys, time, collections

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(HERE, '.tools', 'aeneas-nightly-2026.11.09-5a392f4')
CHARON = os.path.join(TOOLS, 'charon')
AENEAS = os.path.join(TOOLS, 'aeneas')
FNINV = os.path.join(HERE, 'tools', 'fninv', 'target', 'release', 'fninv')
LEAN = os.path.join(HERE, 'lean-pinned')
ENV = dict(os.environ)
ENV['PATH'] = os.path.expanduser('~/.elan/bin') + ':' + os.path.expanduser('~/.cargo/bin') + ':' + ENV['PATH']
ANSI = re.compile(r'\x1b\[[0-9;]*m')
# Rewrite experiments (rewrites/run.py) reuse this driver on patched copies of a crate:
#   CENSUS_CRATES = directory holding <crate>-<version>/   CENSUS_TAG = suffix for work dir, LLBC and result names
CRATES_DIR = os.environ.get('CENSUS_CRATES') or os.path.join(HERE, 'crates')
TAG = os.environ.get('CENSUS_TAG', '')
# extra Aeneas flags for a side run (e.g. CENSUS_AENEAS_FLAGS=-filter-trait-methods with CENSUS_TAG=_ftm)
AENEAS_FLAGS = os.environ.get('CENSUS_AENEAS_FLAGS', '').split()
# Experiment, off by default and not part of the reported numbers: move declaration groups that mix functions with
# types/trait impls to the end of the order (emulates "skip the group and go on" in Aeneas's function analysis).
# On cedar-policy-core this exposed further crate-level crashes and did not converge (see CENSUS.md).
MOVE_MIXED = bool(os.environ.get('CENSUS_MOVE_MIXED'))
RESULTS = os.path.join(HERE, 'data', ('flags' if AENEAS_FLAGS else 'rewrites') if TAG else 'results')
REGISTER = ['--rustc-arg=-Zcrate-attr=feature(register_tool)', '--rustc-arg=-Zcrate-attr=register_tool(charon)']


def sh(cmd, cwd, log, env=None, timeout=3600):
    t = time.time()
    with open(log, 'w') as f:
        try:
            rc = subprocess.call(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, env=env or ENV, timeout=timeout)
        except subprocess.TimeoutExpired:
            rc = 'timeout'
    return rc, round(time.time() - t, 1)


def read(p):
    return ANSI.sub('', open(p, errors='replace').read())


# ----------------------------------------------------------------------------- inventory
def rs_files(root):
    out = []
    for d, dirs, files in os.walk(root):
        rel = os.path.relpath(d, root)
        top = rel.split(os.sep)[0]
        if top in ('tests', 'benches', 'examples', 'target', 'fuzz'):
            dirs[:] = []
            continue
        for f in files:
            if f.endswith('.rs') and not (rel == '.' and f == 'build.rs'):
                out.append(os.path.normpath(os.path.join(rel, f)))
    return sorted(out)


def code_lines(lines, a, b):
    """non-blank, non-comment-only lines in [a, b] (1-based, inclusive)"""
    n = 0
    in_block = False
    for s in lines[a - 1:b]:
        t = s.strip()
        if in_block:
            if '*/' in t:
                in_block = False
            continue
        if not t or t.startswith('//'):
            continue
        if t.startswith('/*'):
            if '*/' not in t:
                in_block = True
            continue
        n += 1
    return n


def inventory(src):
    files = rs_files(src)
    out = subprocess.check_output([FNINV, src] + files)
    inv = json.loads(out)
    cache = {}
    for i, f in enumerate(inv['functions']):
        f['id'] = i
        if f['file'] not in cache:
            cache[f['file']] = open(os.path.join(src, f['file']), errors='replace').read().split('\n')
        f['loc'] = code_lines(cache[f['file']], f['sig_line'], f['line_end'])
    # subtract nested fns from their parents' line counts
    byfile = collections.defaultdict(list)
    for f in inv['functions']:
        byfile[f['file']].append(f)
    for fs in byfile.values():
        for f in fs:
            if f['nested_in_fn']:
                par = [g for g in fs if g is not f and g['line_start'] <= f['line_start'] and g['line_end'] >= f['line_end']]
                if par:
                    p = min(par, key=lambda g: g['line_end'] - g['line_start'])
                    p['loc'] = max(1, p['loc'] - f['loc'])
    return inv


def fn_at(inv, file, line, line_end=None):
    """innermost inventory function containing file:line"""
    best = None
    for f in inv['functions']:
        if f['file'] == file and f['line_start'] <= line <= f['line_end'] and (line_end is None or line_end <= f['line_end']):
            if best is None or (f['line_end'] - f['line_start']) < (best['line_end'] - best['line_start']):
                best = f
    return best


# ----------------------------------------------------------------------------- LLBC
def name_str(n):
    out = []
    for e in n:
        if 'Ident' in e:
            out.append(e['Ident'][0])
        elif 'Impl' in e:
            i = e['Impl']
            out.append('{impl#%s}' % i['Trait'] if isinstance(i, dict) and isinstance(i.get('Trait'), int) else '{impl}')
        elif 'Monomorphized' in e:
            out.append('<mono>')
        else:
            out.append('{' + list(e.keys())[0].lower() + '}')
    return '::'.join(out)


def span_of(meta, files):
    sp = meta['span']
    while isinstance(sp, dict) and 'data' not in sp:
        if 'Untagged' in sp:
            sp = sp['Untagged']
        elif 'Value' in sp:
            sp = sp['Value'][1]
        else:
            return None
    d = sp['data']
    f = files[d['file_id']]
    nm = f['name']
    local = 'Local' in nm
    path = nm.get('Local') or nm.get('Virtual') or nm.get('NotReal') or str(nm)
    g = sp.get('generated_from_span')
    return {'file': path, 'local': local, 'beg': d['beg']['line'], 'begc': d['beg']['col'], 'end': d['end']['line'],
            'endc': d['end']['col'], 'macro': bool(g)}


def load_llbc(path):
    D = json.load(open(path)) if isinstance(path, str) else path
    t = D['translated']
    files = {f['id']: f for f in t['files'] if f}
    # Deduplicated spans: build the table of span values on the fly
    spans = {}

    def collect(x):
        if isinstance(x, dict):
            if 'Value' in x and isinstance(x['Value'], list) and len(x['Value']) == 2 and isinstance(x['Value'][1], dict) and 'data' in x['Value'][1] and 'file_id' in x['Value'][1].get('data', {}):
                spans[x['Value'][0]] = x['Value'][1]
            for v in x.values():
                collect(v)
        elif isinstance(x, list):
            for v in x:
                collect(v)
    decls = []
    for kind in ('fun_decls', 'type_decls', 'global_decls', 'trait_decls', 'trait_impls'):
        for x in t[kind]:
            if not x:
                continue
            m = x['item_meta']
            if 'Deduplicated' in m['span'] or 'Value' in m['span']:
                if not spans:
                    collect(t)
                if 'Deduplicated' in m['span']:
                    m = dict(m, span=spans.get(m['span']['Deduplicated'], None) or m['span'])
            try:
                sp = span_of(m, files)
            except Exception:
                sp = None
            body = None
            if kind == 'fun_decls':
                b = x['body']
                body = b if isinstance(b, str) else list(b.keys())[0]
            decls.append({'kind': kind, 'id': x['def_id'], 'name': name_str(m['name']), 'raw_name': m['name'], 'span': sp,
                          'local': m['is_local'], 'opacity': m['opacity'], 'has_errors': m.get('has_errors', False),
                          'body': body, 'src': (list(x['src'].keys())[0] if kind == 'fun_decls' and isinstance(x.get('src'), dict) else (x.get('src') if kind == 'fun_decls' else None))})
    names = {}
    for e in t.get('item_names', []):
        try:
            k = e['key']
            kk = list(k.keys())[0]
            names[(kk, k[kk])] = name_str(e['value'])
        except Exception:
            pass
    return {'has_errors': D['has_errors'], 'decls': decls, 'item_names': names, 'crate': t['crate_name']}


# ----------------------------------------------------------------------------- Aeneas log
SRC_RE = re.compile(r"Source: '([^']+)', lines (\d+):(\d+)-(\d+):(\d+)(?:; this code is generated from a macro invocation at: '([^']+)', lines (\d+):(\d+)-(\d+):(\d+))?")
DEF_RE = re.compile(r"Definition span: '([^']+)', lines (\d+):(\d+)-(\d+):(\d+)")


def parse_aeneas_log(text):
    """-> (entries, fatal). entry = {level,msg,source,def_span,name}"""
    lines = [l for l in text.split('\n') if not re.match(r'^(Called from|Raised |Re-raised )', l)]
    entries = []
    cur = None
    fatal = None
    for l in lines:
        m = re.match(r'^\[(Error|Warn ?|Info ?)\] ?(.*)', l)
        if m:
            cur = {'level': m.group(1).strip(), 'msg': m.group(2), 'more': [], 'source': None, 'def_span': None, 'name': None}
            entries.append(cur)
            continue
        if l.startswith('Fatal error:'):
            fatal = l[len('Fatal error:'):].strip()
            cur = None
            continue
        if cur is None:
            continue
        s = SRC_RE.match(l)
        if s:
            if cur['source'] is None:
                g = s.groups()
                cur['source'] = {'file': g[0], 'beg': int(g[1]), 'begc': int(g[2]), 'end': int(g[3]), 'endc': int(g[4])}
                if g[5]:
                    cur['source']['macro_site'] = {'file': g[5], 'beg': int(g[6]), 'end': int(g[8])}
            continue
        d = DEF_RE.match(l)
        if d:
            g = d.groups()
            cur['def_span'] = {'file': g[0], 'beg': int(g[1]), 'end': int(g[3])}
            continue
        if l.startswith('Name pattern:'):
            cur['name'] = l[len('Name pattern:'):].strip().strip("'")
            continue
        if l.startswith('Compiler source:'):
            cur['compiler_source'] = l[len('Compiler source:'):].strip()
            continue
        if len(cur['more']) < 3 and l.strip():
            cur['more'].append(l.strip()[:200])
    # "[Error] msg / [Warn] Could not translate ... 'NAME because of previous error": give the error the
    # name and definition span of the declaration it was raised for
    for i in range(1, len(entries)):
        w, e = entries[i], entries[i - 1]
        if w['level'].startswith('Warn') and 'previous error' in w['msg'] and e['level'] == 'Error':
            e['decl_name'] = w['name'] or w['msg']
            if e['def_span'] is None:
                e['def_span'] = w['def_span']
            w['decl_name'] = w['name'] or w['msg']
            w['cause'] = e['msg']
            w['cause_emitter'] = e.get('compiler_source')
    return entries, fatal


SHIM_NAME = re.compile(r"core::ops::function::Fn(Once|Mut)?<.*\}(::call(_once|_mut)?)?'?( because of previous error.*)?$", re.S)
KIND = {'trait_impl_id': 'TraitImpl', 'trait_decl_id': 'TraitDecl', 'fun_decl_id': 'Fun', 'type_decl_id': 'Type', 'global_decl_id': 'Global'}
NAMES = {}


def resolve(msg):
    """'Could not find: trait_impl_id: 116' -> name of the declaration that was excluded"""
    def rep(m):
        n = NAMES.get((KIND.get(m.group(1), m.group(1)), int(m.group(2))))
        return 'uses excluded declaration ' + (n or m.group(0))
    return re.sub(r'Could not find: (\w+_id): (\d+)', rep, msg)


def short(msg, n=220):
    msg = msg.strip()
    return msg if len(msg) <= n else msg[:n] + ' ...'


# ----------------------------------------------------------------------------- generated Lean
# a declaration starts at its doc comment; after an extraction error Aeneas leaves the rest of the file indented
BLOCK_START = re.compile(r'^\s*/-- (\[|Trait )')
DECL_RE = re.compile(r'\s*(?:@\[.*?\]\s*)*?(?:(?:noncomputable|private|protected|partial|unsafe)\s+)*(def|axiom|structure|inductive|impl_def|abbrev|instance|theorem|opaque|class)\s+([^\s:({\[]+)', re.S)


def parse_lean(path):
    lines = open(path, errors='replace').read().split('\n')
    blocks = []
    cur = None
    for i, l in enumerate(lines, 1):
        if BLOCK_START.match(l):
            cur = {'start': i, 'end': i, 'doc': l, 'kind': None, 'lean_name': None, 'text': []}
            blocks.append(cur)
        if cur is not None:
            cur['end'] = i
            cur['text'].append(l)
    for b in blocks:
        txt = '\n'.join(b['text'])
        body = txt.split('-/', 1)[1] if '-/' in txt else txt
        m = DECL_RE.match(body)
        if m:
            b['kind'], b['lean_name'] = m.group(1), m.group(2)
        b['has_sorry'] = bool(re.search(r'\bsorry\b', body))
        sm = re.findall(r'sorry /-\s*(.*?)\s*-/', body)
        b['sorry_msgs'] = sorted(set(short(s, 160) for s in sm))[:5]
        m = re.match(r'^\s*/-- (?:Trait (?:implementation|declaration): )?\[(.*?)\]:?\s*$', b['doc'])
        b['rust_name'] = m.group(1) if m else None
        b['body'] = body
        del b['text']
    return blocks, len(lines)


LAKE_RE = re.compile(r'^(error|warning): (?:\./)?([^:]+\.lean):(\d+):(\d+): (.*)')


def parse_lake(text, relfile):
    errs = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        m = LAKE_RE.match(lines[i])
        if m and m.group(2).endswith(relfile):
            msg = [m.group(5)]
            j = i + 1
            while j < len(lines) and not LAKE_RE.match(lines[j]) and not lines[j].startswith(('⚠', '✖', '✔', 'Some required', 'error: build failed', 'info:')) and len(msg) < 4:
                if lines[j].strip():
                    msg.append(lines[j].strip())
                j += 1
            errs.append({'level': m.group(1), 'line': int(m.group(3)), 'col': int(m.group(4)), 'msg': short(' '.join(msg), 300)})
        i += 1
    return errs


IDENT = re.compile(r"«[^»]*»(?:\.[A-Za-z_][A-Za-z0-9_'!?]*)*|[A-Za-z_][A-Za-z0-9_'!?]*(?:\.(?:«[^»]*»|[A-Za-z_][A-Za-z0-9_'!?]*))*")
LIB_PREFIX = ('core.', 'alloc.', 'std.', 'Vec.', 'Slice.', 'Array.', 'Str.', 'String.', 'Box.', 'Option.', 'Result.', 'UScalar.', 'IScalar.', 'Usize.', 'Isize.',
              'U8.', 'U16.', 'U32.', 'U64.', 'U128.', 'I8.', 'I16.', 'I32.', 'I64.', 'I128.', 'Bool.', 'Char.')


# ----------------------------------------------------------------------------- main per-crate run
def charon_run(src, out_llbc, log, marks, tgt, extra_args=()):
    # --no-dedup-serialized-ast: every value is written in full, so a declaration can be removed
    # from the file without breaking back-references (needed by the surgery below)
    cmd = [CHARON, 'cargo', '--preset=aeneas', '--no-dedup-serialized-ast']
    if marks:
        cmd += REGISTER
    cmd += list(extra_args)
    cmd += ['--dest-file', out_llbc]
    if os.path.exists(out_llbc):
        os.remove(out_llbc)
    env = dict(ENV, CARGO_TARGET_DIR=tgt)
    rc, secs = sh(cmd, src, log, env)
    return rc, secs, os.path.exists(out_llbc) and os.path.getsize(out_llbc) > 0


def aeneas_run(llbc, dest, log, binary=AENEAS, timeout=7200, extra=()):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    rc, secs = sh([binary, '-backend', 'lean', '-dest', dest, '-subdir', 'Generated', '-emit-json', '-no-progress-bar', '-print-error-emitters'] + AENEAS_FLAGS + list(extra) + [llbc], os.path.dirname(llbc), log, timeout=timeout)
    gen = [f for f in os.listdir(os.path.join(dest, 'Generated'))] if os.path.isdir(os.path.join(dest, 'Generated')) else []
    return rc, secs, gen


ICE_RE = re.compile(r'^error: internal compiler error: (.*)\n\s+--> ([^:\n]+):(\d+):(\d+)', re.M)


def mark_opaque(src, f, attr='#[charon::opaque]'):
    p = os.path.join(src, f['file'])
    lines = open(p).read().split('\n')
    i = f['sig_line'] - 1
    if attr in lines[i]:
        return False
    ind = len(lines[i]) - len(lines[i].lstrip())
    lines[i] = lines[i][:ind] + attr + ' ' + lines[i][ind:]
    open(p, 'w').write('\n'.join(lines))
    return True


def find_culprit(llbc, source):
    """LLBC declaration whose span is the Aeneas 'Source' of a fatal error"""
    best = None
    for d in llbc['decls']:
        sp = d['span']
        if not sp:
            continue
        if not (sp['file'].endswith(source['file']) or source['file'].endswith(sp['file'])):
            continue
        exact = (sp['beg'], sp['begc'], sp['end'], sp['endc']) == (source['beg'], source['begc'], source['end'], source['endc'])
        contains = sp['beg'] <= source['beg'] and sp['end'] >= source['end']
        if not (exact or contains):
            continue
        rank = (0 if exact else 1, {'trait_decls': 0, 'fun_decls': 1, 'trait_impls': 2, 'type_decls': 3, 'global_decls': 4}[d['kind']], sp['end'] - sp['beg'])
        if best is None or rank < best[0]:
            best = (rank, d)
    return best[1] if best else None


def has_ttc(method):
    return bool(re.search(r'"trait_type_constraints": \[[^\]]', json.dumps(method['params'])))


def sig_problems(method):
    """Static reasons for which Aeneas's translate_method_sig raises on a trait method signature
    (the cases seen in this corpus; see SymbolicToPureTypes.ml translate_fwd_ty and translate_fun_sigs)."""
    out = []
    if has_ttc(method):
        out.append('ttc')

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == 'DynTrait':
                    out.append('dyn')
                elif k == 'FnPtr':
                    out.append('fnptr')
                elif k == 'TraitType' and isinstance(v, list) and len(v) == 3 and isinstance(v[2], dict) and any(v[2].get(g) for g in ('regions', 'types', 'const_generics', 'trait_refs')):
                    out.append('gat')
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(method['skip_binder'].get('signature'))
    return sorted(set(out))


def predict_surgery(D):
    """[(trait def_id, trait name, method name, reasons)] for every trait method in the LLBC whose signature
    Aeneas will abort on. Used to remove them in one go on the largest crate instead of one Aeneas run each."""
    out = []
    for t in D['translated']['trait_decls']:
        if not t:
            continue
        for m in t['methods']:
            if m:
                why = sig_problems(m)
                if why:
                    out.append((t['def_id'], name_str(t['item_meta']['name']), m['skip_binder']['name'], why))
    return out


def strip_groups(name):
    """'a::{impl X<Y::Z> for W}::f::{closure#1}' -> ['a', 'f']: the identifiers outside any {...} or <...> group"""
    out, cur, depth = [], '', 0
    i = 0
    while i < len(name):
        c = name[i]
        if name.startswith('->', i):
            i += 2
            continue
        if c in '{<':
            depth += 1
        elif c in '}>':
            depth -= 1
        elif depth == 0:
            if name.startswith('::', i):
                if cur:
                    out.append(cur)
                cur = ''
                i += 2
                continue
            cur += c
        i += 1
    if cur:
        out.append(cur)
    return [x.strip() for x in out if x.strip()]


def ident_seq(raw_name):
    return [e['Ident'][0] for e in raw_name if 'Ident' in e]


TRACE_FN = re.compile(r'^\[Trace\] Aeneas__Translate\.translate_function_to_symbolics, line \d+:\n(.+)$', re.M)


def traced_functions(log_text):
    """names of the functions whose symbolic execution was started, in log order, up to the fatal error"""
    cut = log_text.find('Fatal error:')
    txt = log_text if cut < 0 else log_text[:cut]
    return [m.group(1).strip() for m in TRACE_FN.finditer(txt)]


def bisect_crash(D, W, base, fatal, k=8):
    """Which local function bodies make Aeneas die with the uncaught exception `fatal`?
    All local bodies are made opaque (the 'skeleton'), then bodies are put back for one subset at a time and Aeneas is
    run on it; a subset that reproduces the exception is split again (k parts per split, k runs at once) until single
    functions are left. Assumes the crash depends on one body alone; returns ([fun_decl], number of Aeneas runs)."""
    funs = [x for x in D['translated']['fun_decls'] if x and x['item_meta']['is_local'] and isinstance(x['body'], dict)]
    bodies = {x['def_id']: x['body'] for x in funs}
    byid = {x['def_id']: x for x in funs}
    for x in funs:
        x['body'] = 'Opaque'
    key = 'Fatal error: ' + fatal.strip()
    root = os.path.join(W, 'bisect')

    def test(batch):
        procs = []
        for j, ids in enumerate(batch):
            for i in ids:
                byid[i]['body'] = bodies[i]
            d = os.path.join(root, str(j))
            if os.path.exists(d):
                shutil.rmtree(d)
            os.makedirs(d)
            p = os.path.join(d, base + '.llbc')
            open(p, 'w').write(json.dumps(D))
            for i in ids:
                byid[i]['body'] = 'Opaque'
            f = open(os.path.join(d, 'aeneas.log'), 'w')
            procs.append((subprocess.Popen([AENEAS, '-backend', 'lean', '-dest', os.path.join(d, 'out'), '-subdir', 'Generated', '-no-progress-bar', p],
                                           cwd=d, stdout=f, stderr=subprocess.STDOUT, env=ENV), f, d, p))
        res = []
        for pr, f, d, p in procs:
            try:
                pr.wait(timeout=5400)
            except subprocess.TimeoutExpired:
                pr.kill()
            f.close()
            res.append(key in read(os.path.join(d, 'aeneas.log')))
            os.remove(p)
            shutil.rmtree(os.path.join(d, 'out'), ignore_errors=True)
        return res
    queue, culprits, ntests = [sorted(bodies)], [], 0
    try:
        if test([[]])[0]:
            # the exception appears with no local body at all: it does not come from a function body
            return [], 1
        while queue:
            parts = []
            for ids in queue:
                if len(ids) == 1:
                    culprits.append(ids[0])
                    continue
                n = min(k, len(ids))
                sz = -(-len(ids) // n)
                parts += [ids[i:i + sz] for i in range(0, len(ids), sz)]
            queue = []
            for b in range(0, len(parts), k):
                batch = parts[b:b + k]
                out = test(batch)
                ntests += len(batch)
                queue += [ids for ids, bad in zip(batch, out) if bad]
            json.dump({'pending': [len(q) for q in queue], 'culprits': culprits, 'runs': ntests}, open(os.path.join(root, 'progress.json'), 'w'))
    finally:
        for i, x in byid.items():
            x['body'] = bodies[i]
    return [byid[i] for i in culprits], ntests


def remove_impls_of(D, llbc_idx, gone, files, tid):
    """Remove every impl of trait `tid` and every declaration named under such an impl (its methods, their closures,
    types declared inside). Aeneas cannot even print the name of something nested in an impl that is gone.
    Returns (number of impls, [removed local functions with their spans])."""
    impl_ids = set()
    for k, x in enumerate(D['translated']['trait_impls']):
        if x and x['impl_trait']['id'] == tid:
            impl_ids.add(x['def_id'])
            D['translated']['trait_impls'][k] = None
            gone.add(('trait_impls', x['def_id']))
    removed = []
    if not impl_ids:
        return 0, removed

    def under(raw_name):
        return any('Impl' in e and isinstance(e['Impl'], dict) and e['Impl'].get('Trait') in impl_ids for e in raw_name)
    for kind in ('fun_decls', 'type_decls', 'global_decls', 'trait_impls', 'trait_decls'):
        tab = D['translated'][kind]
        for k, x in enumerate(tab):
            if x and under(x['item_meta']['name']):
                if kind == 'fun_decls' and x['item_meta']['is_local']:
                    try:
                        sp = span_of(x['item_meta'], files)
                    except Exception:
                        sp = None
                    removed.append({'id': x['def_id'], 'name': name_str(x['item_meta']['name']), 'file': sp and sp['file'], 'beg': sp and sp['beg'], 'end': sp and sp['end']})
                tab[k] = None
                gone.add((kind, x['def_id']))
    return len(impl_ids), removed


ORDERED_KIND = {'Type': 'type_decls', 'Fun': 'fun_decls', 'TraitDecl': 'trait_decls', 'TraitImpl': 'trait_impls', 'Global': 'global_decls'}


def clean_ordered(D, gone):
    """drop removed declarations from the `ordered_decls` groups (a pre-pass of Aeneas looks every listed id up)"""
    out = []
    for g in D['translated']['ordered_decls']:
        (kind, body), = g.items()
        if kind in ORDERED_KIND:
            tab = ORDERED_KIND[kind]
            if 'NonRec' in body:
                if (tab, body['NonRec']) in gone:
                    continue
            elif 'Rec' in body:
                ids = [i for i in body['Rec'] if (tab, i) not in gone]
                if not ids:
                    continue
                g = {kind: {'Rec': ids}}
        elif isinstance(body, dict) and isinstance(body.get('Rec'), list):
            # mixed group: [{"Fun": id}, {"Type": id}, ...]
            items = []
            for it in body['Rec']:
                if isinstance(it, dict) and len(it) == 1:
                    (k2, i2), = it.items()
                    if k2 in ORDERED_KIND and (ORDERED_KIND[k2], i2) in gone:
                        continue
                items.append(it)
            if not items:
                continue
            g = {kind: {'Rec': items}}
        out.append(g)
    D['translated']['ordered_decls'] = out


def opaque_at_sites(D, llbc_idx, gone, sites, why, r, surgery, note=None):
    """make opaque the body of the innermost local function declaration around each source site"""
    funs = {'decls': [d for d in llbc_idx['decls'] if d['kind'] == 'fun_decls' and d['local'] and ('fun_decls', d['id']) not in gone]}
    fd = {x['def_id']: x for x in D['translated']['fun_decls'] if x}
    n = 0
    for src in sites:
        cul = find_culprit(funs, src)
        x = cul and fd.get(cul['id'])
        if x is not None and isinstance(x['body'], dict):
            x['body'] = 'Opaque'
            surgery.append({'kind': 'fun_body_opaque', 'id': x['def_id'], 'name': cul['name'], 'round': r, 'why': why, 'note': note})
            n += 1
    return n


def raw_decl(D, kind, did):
    tab = D['translated'][kind]
    for i, x in enumerate(tab):
        if x and x['def_id'] == did:
            return tab, i
    return tab, None


def run_crate(cdir, max_rounds=200, do_lean=True, overrides=None):
    name = re.sub(r'-\d+\.\d+\.\d+.*$', '', cdir)
    version = cdir[len(name) + 1:]
    W = os.path.join(HERE, 'work', 'run', name + TAG)
    if os.path.exists(W):
        shutil.rmtree(W)
    os.makedirs(W)
    src = os.path.join(W, 'src')
    shutil.copytree(os.path.join(CRATES_DIR, cdir), src, symlinks=True)
    tgt = os.path.join(HERE, 'work', 'target', name + TAG)
    inv = inventory(src)
    json.dump(inv, open(os.path.join(W, 'inventory.json'), 'w'))
    marks = []        # functions marked #[charon::opaque] in the source copy (rustc ICE under Charon)
    surgery = []      # declarations / trait methods removed from the LLBC (Aeneas aborts on them)
    rounds = []
    llbc_path = os.path.join(W, (name + TAG).replace('-', '_') + '.llbc')
    as_is = None
    # ---- Charon (with an ICE peel)
    ok = False
    for r in range(12):
        clog = os.path.join(W, f'charon.{r}.log')
        # round 0 is always the tool as shipped; per-crate extra Charon arguments (data/overrides.json) apply from round 1
        extra_args = (overrides or {}).get('charon_args', []) if r > 0 else []
        rc, csecs, ok = charon_run(src, llbc_path, clog, marks, tgt, extra_args)
        ctext = read(clog)
        rd = {'stage': 'charon', 'round': r, 'rc': rc, 'secs': csecs, 'llbc': ok, 'n_marks': len(marks), 'extra_args': extra_args}
        rounds.append(rd)
        if ok:
            break
        ices = ICE_RE.findall(ctext)
        rd['ices'] = len(ices)
        rd['tail'] = [l[:300] for l in ctext.strip().split('\n')[-6:]]
        if r == 0:
            as_is = {'stage': 'charon', 'msg': (('rustc internal compiler error under the Charon driver: ' + ices[0][0]) if ices else 'charon produced no LLBC: ' + rd['tail'][-1]), 'n_ice_sites': len(ices)}
        new = 0
        for msg, file, line, col in ices:
            f = fn_at(inv, file, int(line))
            if f is not None and mark_opaque(src, f):
                marks.append({'fn': f['id'], 'why': 'rustc ICE under the Charon driver: ' + msg, 'site': f'{file}:{line}', 'round': r})
                new += 1
        rd['new_marks'] = new
        if new == 0:
            rd['stuck'] = 'charon failed and no new function could be marked'
            break
    final = None
    if ok:
        D = json.load(open(llbc_path))
        work_llbc = llbc_path
        removed = set()

        def remove_methods(cul, names, why, r, note=None):
            tab, i = raw_decl(D, 'trait_decls', cul['id'])
            n = 0
            for j, m in enumerate(tab[i]['methods']):
                if m and m['skip_binder']['name'] in names:
                    tab[i]['methods'][j] = None
                    removed.add((cul['name'], m['skip_binder']['name']))
                    surgery.append({'kind': 'trait_method', 'name': cul['name'] + '::' + m['skip_binder']['name'], 'why': why, 'round': r, 'note': note})
                    n += 1
            return n

        llbc_idx = load_llbc(D)          # declaration index (names, spans); built once, removals tracked in `gone`
        files_idx = {f['id']: f for f in D['translated']['files'] if f}
        gone = set()
        big = os.path.getsize(llbc_path) > 500_000_000
        if big:
            # Largest crate only: one Aeneas run costs minutes here, so the trait methods whose signature Aeneas
            # aborts on are removed up front from the signature itself instead of one run each. On every other
            # crate this prediction equals what the one-at-a-time procedure removed (checked in CENSUS.md).
            by_id = {d['id']: d for d in llbc_idx['decls'] if d['kind'] == 'trait_decls'}
            # traits the Aeneas library models are not translated from their Rust signature (`core::error::Error`
            # has `dyn` in `source` and does not abort): leave them alone
            builtin_traits = set(x['rust'] for x in json.load(open(os.path.join(HERE, 'data', 'std_models.json'))).get('trait', []))
            for tid, tname, mname, why in predict_surgery(D):
                cul = by_id[tid]
                if ('trait_decls', tid) in gone:
                    continue
                if why == ['ttc']:
                    remove_methods(cul, {mname}, 'Aeneas aborts the crate on this signature (trait-type constraint)', -1, 'predicted from the signature')
                elif 'gat' in why or cul['local'] or tname not in builtin_traits:
                    tab, i = raw_decl(D, 'trait_decls', tid)
                    n_impl, rem = remove_impls_of(D, llbc_idx, gone, files_idx, tid)
                    tab[i] = None
                    gone.add(('trait_decls', tid))
                    surgery.append({'kind': 'trait_decl_and_impls', 'name': tname, 'why': 'Aeneas aborts the crate on the signature of method `%s` (%s)' % (mname, '/'.join(why)),
                                    'round': -1, 'local': cul['local'], 'impls_removed': n_impl, 'removed_funs': rem, 'note': 'predicted from the signature'})
        if big and MOVE_MIXED:
            # mixed declaration groups go last from the start (on the other crates this is done after the first complete
            # run shows the "Mixed declaration groups" error; on cedar that run alone costs five minutes)
            od = D['translated']['ordered_decls']
            mixed = [g for g in od if 'Mixed' in g]
            if mixed and od[-len(mixed):] != mixed:
                D['translated']['ordered_decls'] = [g for g in od if 'Mixed' not in g] + mixed
                surgery.append({'kind': 'mixed_groups_moved_last', 'name': '%d mixed declaration group(s)' % len(mixed), 'round': -1,
                                'why': 'Aeneas stops its function analysis at a declaration group mixing functions with types or trait impls; '
                                       'every function after it in the declaration order then fails',
                                'groups': len(mixed), 'first_position': min(i for i, g in enumerate(od) if 'Mixed' in g), 'of': len(od),
                                'note': 'applied up front; a run without it left 2,151 source functions with "Internal error" (work/cedar_result_before_mixed_fix.json)'})
        cc = os.path.join(HERE, 'data', 'crash_cache', name + '.json')
        if big and os.path.exists(cc):
            # function bodies an earlier bisection of this same input found to crash Aeneas with an uncaught exception
            # (data/crash_cache/): applied directly, after checking that id and name still agree
            cache = json.load(open(cc))
            fd = {x['def_id']: x for x in D['translated']['fun_decls'] if x}
            for c in cache['culprits']:
                x = fd.get(c['id'])
                if x is not None and name_str(x['item_meta']['name']) == c['name'] and isinstance(x['body'], dict):
                    x['body'] = 'Opaque'
                    surgery.append({'kind': 'fun_body_opaque', 'id': x['def_id'], 'name': c['name'], 'round': -1,
                                    'why': 'Aeneas crashes on the body of this function with an uncaught exception (%s), which aborts the crate' % cache['fatal'].replace('exception ', ''),
                                    'aeneas_runs_to_find': cache.get('aeneas_runs'), 'note': 'from data/crash_cache (found by bisection in an earlier run on the same input)'})
            if MOVE_MIXED and cache.get('lookup_sites'):
                opaque_at_sites(D, llbc_idx, gone, cache['lookup_sites'], cache['lookup_why'], -1, surgery,
                                'from data/crash_cache (sites logged by an earlier run on the same input)')
        for r in range(max_rounds):
            if surgery:
                os.makedirs(os.path.join(W, 'peeled'), exist_ok=True)
                clean_ordered(D, gone)
                work_llbc = os.path.join(W, 'peeled', (name + TAG).replace('-', '_') + '.llbc')
                open(work_llbc, 'w').write(json.dumps(D))   # dumps() uses the C encoder; dump() to a file does not
            alog = os.path.join(W, f'aeneas.{r}.log')
            arc, asecs, gen = aeneas_run(work_llbc, os.path.join(W, 'lean'), alog)
            entries, fatal = parse_aeneas_log(read(alog))
            rd = {'stage': 'aeneas', 'round': r, 'rc': arc, 'secs': asecs, 'fatal': fatal, 'generated': gen, 'n_surgery': len(surgery),
                  'errors': sum(1 for e in entries if e['level'] == 'Error')}
            rounds.append(rd)
            lean_files = [g for g in gen if g.endswith('.lean')]
            errs = [e for e in entries if e['level'] == 'Error']
            if r == 0 and not lean_files and as_is is None:
                as_is = {'stage': 'aeneas', 'msg': 'Aeneas aborted the whole crate (fatal exception): ' + (short(errs[-1]['msg']) if errs else str(fatal)),
                         'source': errs[-1]['source'] if errs else None}
            if MOVE_MIXED and lean_files and any(e['level'] == 'Error' and e['msg'].startswith('Mixed declaration groups') for e in entries):
                # Aeneas's function analysis (llbc/FunsAnalysis.ml) stops at the first declaration group that mixes
                # functions with types or trait impls, and every function that comes after it in the declaration order
                # is then untranslatable ("Internal error", SymbolicToPureTypes.ml line 724). Emulate "skip the group and
                # go on": move such groups to the end of the order, once, and rerun.
                od = D['translated']['ordered_decls']
                mixed = [g for g in od if 'Mixed' in g]
                if mixed and od[-len(mixed):] != mixed:
                    D['translated']['ordered_decls'] = [g for g in od if 'Mixed' not in g] + mixed
                    after = len(od) - 1 - max(i for i, g in enumerate(od) if 'Mixed' in g)
                    surgery.append({'kind': 'mixed_groups_moved_last', 'name': '%d mixed declaration group(s)' % len(mixed), 'round': r,
                                    'why': 'Aeneas stops its function analysis at a declaration group mixing functions with types or trait impls; '
                                           'every function after it in the declaration order then fails',
                                    'groups': len(mixed), 'first_position': min(i for i, g in enumerate(od) if 'Mixed' in g), 'of': len(od),
                                    'errors_before': sum(1 for e in entries if e['level'] == 'Error')})
                    rd['mixed_groups'] = len(mixed)
                    continue
            if lean_files:
                final = {'round': r, 'lean_file': lean_files[0]}
                break
            if fatal and 'CFailure' not in fatal:
                # An OCaml exception other than Aeneas's own error type escaped from the translation of one function body
                # and took the crate with it. The log does not say which function: find it by bisection (bisect_crash).
                # Its body is then made opaque (signature kept, so callers are not affected) and it counts as failed.
                culprits, ntests = bisect_crash(D, W, (name + TAG).replace('-', '_'), fatal)
                rd['crash'] = {'exception': fatal, 'aeneas_runs': ntests, 'culprits': [name_str(x['item_meta']['name']) for x in culprits]}
                if not culprits:
                    rd['stuck'] = 'aeneas crashed (%s) and no single function body reproduces it' % fatal
                    break
                for x in culprits:
                    x['body'] = 'Opaque'
                    surgery.append({'kind': 'fun_body_opaque', 'id': x['def_id'], 'name': name_str(x['item_meta']['name']), 'round': r,
                                    'why': 'Aeneas crashes on the body of this function with an uncaught exception (%s), which aborts the crate' % fatal.replace('exception ', ''),
                                    'aeneas_runs_to_find': ntests})
                continue
            errs = [e for e in errs if e['source']]
            if not errs:
                rd['stuck'] = 'aeneas fatal without a source location'
                break
            e = errs[-1]
            if e['msg'].startswith('Could not lookup a fun declaration'):
                # a pure micro-pass (simplify_trait_calls) aborts the crate when a call refers to a function that is gone
                # (here: a method of an impl removed with its trait). All such call sites are in the log: the functions
                # around them lose their body in one step.
                sites = [x['source'] for x in errs if x['msg'].startswith('Could not lookup a fun declaration')]
                n = opaque_at_sites(D, llbc_idx, gone, sites,
                                    "calls a method of an impl that was removed with its trait (a trait Aeneas aborts the crate on); Aeneas's simplify_trait_calls pass "
                                    "(pure/PureMicroPassesGeneral.ml, line 2331) then raises an error that is not caught per function and aborts the crate", r, surgery)
                rd['lookup_sites'] = len(sites)
                if n:
                    continue
            cul = find_culprit({'decls': [d for d in llbc_idx['decls'] if (d['kind'], d['id']) not in gone]}, e['source'])
            rd['culprit'] = {'msg': short(e['msg']), 'source': e['source'], 'decl': cul and {'kind': cul['kind'], 'name': cul['name'], 'local': cul['local']}}
            if cul is None:
                rd['stuck'] = 'aeneas fatal: no declaration at the reported source span'
                break
            why = 'Aeneas aborts the crate on this signature: ' + short(e['msg'])
            done = 0
            if cul['kind'] == 'trait_decls':
                tab, i = raw_decl(D, 'trait_decls', cul['id'])
                present = [m for m in tab[i]['methods'] if m]
                ttc = [m['skip_binder']['name'] for m in present if has_ttc(m)]
                if ttc:
                    done = remove_methods(cul, set(ttc), why, r, 'signature has trait-type constraints (the sanity check in translate_fun_sigs)')
                else:
                    # a required method (or the trait's own signature) is the problem: remove the trait
                    # declaration together with all its impls, which is what skipping it would amount to
                    n_impl, rem = remove_impls_of(D, llbc_idx, gone, files_idx, cul['id'])
                    tab[i] = None
                    gone.add(('trait_decls', cul['id']))
                    surgery.append({'kind': 'trait_decl_and_impls', 'name': cul['name'], 'why': why, 'round': r, 'local': cul['local'],
                                    'methods_in_use': [m['skip_binder']['name'] for m in present], 'impls_removed': n_impl, 'removed_funs': rem})
                    done = 1
            elif cul['kind'] == 'trait_impls':
                # an impl Aeneas cannot handle: if its trait is local, the other impls of that trait fail the same way
                # (seen on cedar's TCNode), so the trait goes with all its impls in one step
                tab, i = raw_decl(D, 'trait_impls', cul['id'])
                tid = tab[i]['impl_trait']['id']
                tdecl = next((d for d in llbc_idx['decls'] if d['kind'] == 'trait_decls' and d['id'] == tid), None)
                if tdecl is not None and tdecl['local']:
                    n_impl, rem = remove_impls_of(D, llbc_idx, gone, files_idx, tid)
                    tt, ti = raw_decl(D, 'trait_decls', tid)
                    if ti is not None:
                        tt[ti] = None
                        gone.add(('trait_decls', tid))
                    surgery.append({'kind': 'trait_decl_and_impls', 'name': tdecl['name'], 'why': why + ' (raised on impl ' + cul['name'] + ')', 'round': r, 'local': True, 'impls_removed': n_impl, 'removed_funs': rem})
                    done = 1
            if not done:
                tab, i = raw_decl(D, cul['kind'], cul['id'])
                if i is not None:
                    tab[i] = None
                    gone.add((cul['kind'], cul['id']))
                    surgery.append({'kind': cul['kind'], 'name': cul['name'], 'why': why, 'round': r, 'local': cul['local'],
                                    'span': cul['span'] and (cul['span']['file'], cul['span']['beg'], cul['span']['end'])})
                    done = 1
            if not done:
                rd['stuck'] = 'aeneas fatal: nothing left to remove for ' + cul['name']
                break
    state = {'crate': name, 'version': version, 'rounds': rounds, 'surgery': surgery, 'opaque_marks': marks, 'as_is': as_is,
             'parse_errors': inv['parse_errors'], 'final_round': final and final['round'], 'lean_file': final and final['lean_file'],
             'llbc': os.path.relpath(work_llbc, W) if ok else None}
    json.dump(state, open(os.path.join(W, 'state.json'), 'w'), indent=1)
    return finish(name, do_lean=do_lean, build=True)


def finish(name, do_lean=True, build=True):
    """join the artefacts of a finished run (work/run/<name>) into data/results/<name>.json"""
    W = os.path.join(HERE, 'work', 'run', name + TAG)
    state = json.load(open(os.path.join(W, 'state.json')))
    inv = json.load(open(os.path.join(W, 'inventory.json')))
    marks = state['opaque_marks']
    res = {k: state[k] for k in ('crate', 'version', 'rounds', 'surgery', 'opaque_marks', 'as_is', 'parse_errors')}
    res['tools'] = {'aeneas': 'nightly-2026.11.09-5a392f4', 'charon': '0.1.315 (454586e)', 'rust': 'nightly-2026-09-17', 'lean': 'v4.35.0'}
    os.makedirs(RESULTS, exist_ok=True)
    out = os.path.join(RESULTS, name + TAG + '.json')
    if state['final_round'] is None:
        res['peeled'] = False
        res['functions'] = join(inv, None, [], None, [], [], marks, res)
        json.dump(res, open(out, 'w'), indent=1)
        return res
    res['peeled'] = True
    llbc = load_llbc(os.path.join(W, state['llbc']))
    NAMES.clear()
    NAMES.update(llbc['item_names'])
    entries, _ = parse_aeneas_log(read(os.path.join(W, 'aeneas.%d.log' % state['final_round'])))
    lf = state['lean_file']
    mod = lf[:-5]
    gen_dir = os.path.join(LEAN, 'Generated')
    os.makedirs(gen_dir, exist_ok=True)
    if build:
        shutil.copy(os.path.join(W, 'lean', 'Generated', lf), os.path.join(gen_dir, lf))
    blocks, nlines = parse_lean(os.path.join(W, 'lean', 'Generated', lf))
    res['lean_lines'] = nlines
    lake_errs = []
    llog = os.path.join(W, 'lake.log')
    if do_lean:
        if build:
            rc, lsecs = sh(['lake', 'build', 'Generated.' + mod], LEAN, llog, timeout=7200)
            json.dump({'rc': rc, 'secs': lsecs}, open(os.path.join(W, 'lake.json'), 'w'))
        res['lake'] = json.load(open(os.path.join(W, 'lake.json')))
        lake_errs = parse_lake(read(llog), 'Generated/' + lf)
        if res['lake']['rc'] != 0 and not any(e['level'] == 'error' for e in lake_errs):
            raise SystemExit('lake failed without a parsable error for %s: see %s' % (name, llog))
    tj = json.load(open(os.path.join(W, 'lean', 'translation.json')))
    res['functions'] = join(inv, llbc, entries, tj, blocks, lake_errs, marks, res)
    json.dump(res, open(out, 'w'), indent=1)
    return res


# ----------------------------------------------------------------------------- join
def join(inv, llbc, entries, tj, blocks, lake_errs, marks, res):
    fns = inv['functions']
    recs = {}
    for f in fns:
        if f['is_test']:
            continue
        recs[f['id']] = {'id': f['id'], 'file': f['file'], 'name': f['name'], 'path': f['path'], 'kind': f['kind'], 'origin': 'source',
                         'line_start': f['sig_line'], 'line_end': f['line_end'], 'loc': f['loc'], 'cfgs': f['cfgs'], 'public': f['public'],
                         'feat': f['feat'], 'macros': f['macros'], 'methods': f['methods'],
                         'decls': [], 'charon': None, 'aeneas': None, 'lean': None, 'msgs': [], 'lean_names': []}
    mark_by = {m['fn']: m for m in marks}
    crash_opaque = {x['id']: x for x in res.get('surgery', []) if x.get('kind') == 'fun_body_opaque'}
    # functions that went out with an impl of a trait Aeneas aborts on: they have no declaration left in the LLBC
    for sg in res.get('surgery', []):
        for rf in sg.get('removed_funs', []) or []:
            if rf.get('file') and rf.get('beg'):
                f = fn_at(inv, rf['file'], rf['beg'], rf['end'])
                if f is not None and f['id'] in recs and recs[f['id']]['aeneas'] is None:
                    r0 = recs[f['id']]
                    r0['charon'] = 'ok'
                    r0['aeneas'] = 'fail'
                    r0['removed_with_trait'] = sg['name']
                    r0['msgs'].append({'stage': 'aeneas', 'msg': 'in an impl of `%s`, a trait Aeneas aborts the crate on: %s' % (sg['name'], sg['why'])})
    if llbc is None:
        for r in recs.values():
            r['charon'] = 'fail'
            r['msgs'].append({'stage': 'charon', 'msg': (res.get('as_is') or {}).get('msg', 'no LLBC')})
        return list(recs.values())
    # --- LLBC declarations -> inventory functions
    extra = {}      # macro/derive generated functions: key = def_id
    decl_owner = {}
    crate_decl_problems = []
    for d in llbc['decls']:
        if d['kind'] != 'fun_decls' or not d['local']:
            continue
        sp = d['span']
        f = None
        if sp and sp['local']:
            f = fn_at(inv, sp['file'], sp['beg'], sp['end'])
            if f is not None and f['is_test']:
                continue
        shim = False
        if f is not None and d['src'] == 'TraitImpl':
            # `{impl FnOnce<..> for <fn item>}::call_once`: the wrapper rustc makes when a function is passed by
            # name. It carries the span of the function it wraps but is not part of it. A closure's impl is
            # named under its parent function; a shim is not.
            rn = d['raw_name']
            li = max((i for i, e in enumerate(rn) if 'Impl' in e), default=None)
            last = rn[-1]['Ident'][0] if 'Ident' in rn[-1] else None
            if (li is not None and last in ('call', 'call_mut', 'call_once') and f['name'] != last
                    and not (li > 0 and 'Ident' in rn[li - 1] and rn[li - 1]['Ident'][0] == f['name'])):
                shim = True
        if f is not None and not sp['macro'] and not shim:
            recs[f['id']]['decls'].append(d)
            decl_owner[d['id']] = ('src', f['id'])
        else:
            extra[d['id']] = {'id': 'x%d' % d['id'], 'file': sp['file'] if sp else None, 'name': d['name'], 'path': '', 'kind': 'generated', 'origin': 'fn-item-shim' if shim else 'macro-or-derive',
                              'wraps': f['id'] if shim else None,
                              'line_start': sp['beg'] if sp else None, 'line_end': sp['end'] if sp else None, 'loc': 0, 'cfgs': [], 'public': False,
                              'feat': {}, 'macros': {}, 'methods': {}, 'decls': [d], 'charon': None, 'aeneas': None, 'lean': None, 'msgs': [], 'lean_names': []}
            decl_owner[d['id']] = ('extra', d['id'])

    def owner(key):
        return recs[key[1]] if key[0] == 'src' else extra[key[1]]
    # --- translation.json and Lean blocks
    tfun = collections.defaultdict(list)
    for t in tj['functions']:
        tfun[t['def_id']].append(t)
    by_lean = {}
    for b in blocks:
        if b['lean_name']:
            by_lean[b['lean_name']] = b
    lean_owner = {}     # lean_name -> owner key
    for did, ts in tfun.items():
        if did in decl_owner:
            for t in ts:
                ln = t['lean_name']
                ln = ln.split('.', 1)[1] if '.' in ln else ln   # drop the crate namespace
                lean_owner[ln] = decl_owner[did]
                t['_short'] = ln
    # --- Lean errors per block
    def block_at(line):
        lo, hi = 0, len(blocks) - 1
        ans = None
        while lo <= hi:
            mid = (lo + hi) // 2
            if blocks[mid]['start'] <= line:
                ans = blocks[mid]
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
    for b in blocks:
        b['errors'] = []
    orphan_lean = []
    for b in blocks:
        b['sorry_warn'] = False
    for e in lake_errs:
        if e['level'] == 'warning' and 'declaration uses `sorry`' in e['msg']:
            # Lean recovers from an error in a type or callee by putting `sorry` there; the definitions that
            # depend on it then compile with only this warning. They are not usable and are counted as failed.
            b = block_at(e['line'])
            if b is not None:
                b['sorry_warn'] = True
            continue
        if e['level'] != 'error':
            continue
        if 'maximum number of errors' in e['msg']:
            res['lean_max_errors_hit'] = True
            continue
        b = block_at(e['line'])
        if b is not None and e['line'] == b['start'] and "unexpected token '/--'" in e['msg']:
            # the previous definition was left unfinished by Aeneas: the parse error lands on the next doc comment
            i = blocks.index(b)
            if i > 0:
                b = blocks[i - 1]
        if b is None:
            orphan_lean.append(e)
        else:
            b['errors'].append(e['msg'])
    failed_blocks = {b['lean_name']: b for b in blocks if b['errors'] and b['lean_name']}
    tainted = {b['lean_name']: b for b in blocks if b['sorry_warn'] and not b['errors'] and not b['has_sorry'] and b['lean_name']}

    def taint_root(b, seen=()):
        """a block that compiles only 'using sorry': find the failed declaration it depends on"""
        toks = set(IDENT.findall(b['body']))
        for t in toks:
            if t in failed_blocks and failed_blocks[t] is not b:
                r = lean_root(failed_blocks[t])
                return {'msg': r['msg'], 'cascade': r.get('cascade') or t, 'aeneas_hole': r.get('aeneas_hole', False)}
        for t in toks:
            if t in tainted and tainted[t] is not b and t not in seen:
                r = taint_root(tainted[t], seen + (t,))
                if r['cascade']:
                    return r
        return {'msg': 'compiles only with `sorry`: Lean recovered from an error in something it depends on (not located)', 'cascade': None}
    # root cause of a Lean failure: follow "Unknown identifier/constant X" to another failed block
    UNK = re.compile(r"[Uu]nknown (?:identifier|constant) [`'«]+([^`'»]+)")

    def lean_root(b, seen=()):
        for msg in b['errors']:
            m = UNK.search(msg)
            if m:
                x = m.group(1)
                if x.startswith('sorry /-'):
                    return {'msg': 'Aeneas emitted a hole: ' + resolve(x), 'cascade': None, 'aeneas_hole': True}
                cand = [x] + [x.split('.', i)[-1] for i in range(1, x.count('.') + 1)]
                for c in cand:
                    if c in failed_blocks and c not in seen and failed_blocks[c] is not b:
                        r = lean_root(failed_blocks[c], seen + (c,))
                        return {'msg': r['msg'], 'cascade': c, 'aeneas_hole': r.get('aeneas_hole', False)}
                continue
            return {'msg': msg, 'cascade': None}
        return {'msg': b['errors'][0], 'cascade': None}
    # --- Aeneas log entries -> owners
    lfiles = set(f['file'] for f in fns)
    ent_by_owner = collections.defaultdict(list)
    extra_span = {}
    for did, x in extra.items():
        if x['file'] and x['line_start']:
            extra_span.setdefault((x['file'], x['line_start'], x['line_end']), did)
    ext_errors = []
    shim_by_fn = collections.defaultdict(list)
    for did, x in extra.items():
        if x['origin'] == 'fn-item-shim':
            shim_by_fn[x['wraps']].append(did)
    for e in entries:
        if e['level'] not in ('Error', 'Warn'):
            continue
        key = None
        if e.get('decl_name') and SHIM_NAME.search(e['decl_name']) and e['def_span'] and e['def_span']['file'] in lfiles:
            f = fn_at(inv, e['def_span']['file'], e['def_span']['beg'], e['def_span']['end'])
            if f is not None and shim_by_fn.get(f['id']) and e['def_span']['beg'] == f['sig_line'] and e['def_span']['end'] == f['line_end']:
                ent_by_owner[('extra', shim_by_fn[f['id']][0])].append(e)
                continue
        for sp in (e['def_span'], e['source'], (e['source'] or {}).get('macro_site')):
            if sp and sp['file'] in lfiles:
                f = fn_at(inv, sp['file'], sp['beg'], sp['end'])
                if f is not None and f['id'] in recs:
                    key = ('src', f['id'])
                    break
        if key is None:
            for sp in (e['def_span'], e['source']):
                if sp and (sp['file'], sp['beg'], sp['end']) in extra_span:
                    key = ('extra', extra_span[(sp['file'], sp['beg'], sp['end'])])
                    break
        if key is None:
            ext_errors.append({'level': e['level'], 'msg': short(e['msg']), 'source': e['source'], 'name': e['name'], 'emitter': e.get('compiler_source')})
        else:
            ent_by_owner[key].append(e)
    res['aeneas_unattributed'] = ext_errors[:400]
    res['aeneas_unattributed_n'] = len(ext_errors)
    # --- per function status
    axioms = {b['lean_name']: b for b in blocks if b['kind'] == 'axiom'}
    all_names = set(by_lean)
    for key in [('src', i) for i in recs] + [('extra', i) for i in extra]:
        r = owner(key)
        ds = r['decls']
        if r.get('removed_with_trait'):
            continue
        if key[0] == 'src' and r['id'] in mark_by:
            r['charon'] = 'fail'
            r['msgs'].append({'stage': 'charon' if 'rustc ICE' in mark_by[r['id']]['why'] else 'aeneas', 'msg': mark_by[r['id']]['why']})
            if 'Aeneas fatal' in mark_by[r['id']]['why']:
                r['charon'] = 'ok'
                r['aeneas'] = 'fail'
            continue
        if not ds:
            r['charon'] = 'absent'
            continue
        crashed = [d for d in ds if d['id'] in crash_opaque]
        if crashed:
            r['charon'] = 'ok'
            r['aeneas'] = 'fail'
            r['msgs'].append({'stage': 'aeneas', 'msg': crash_opaque[crashed[0]['id']]['why'], 'crash': True})
            r['lean_names'] = []
            continue
        bad = [d for d in ds if d['has_errors'] or d['body'] not in ('Structured', 'Unstructured')]
        if bad:
            r['charon'] = 'fail'
            r['msgs'].append({'stage': 'charon', 'msg': 'no body in LLBC (%s%s)' % (bad[0]['body'], ', has_errors' if bad[0]['has_errors'] else '')})
            continue
        r['charon'] = 'ok'
        # Aeneas
        a_ok = True
        myblocks = []
        for d in ds:
            ts = tfun.get(d['id'], [])
            if not ts and (d['src'] == 'GlobalInitializer' or d['name'].endswith('{builtin}')):
                continue    # promoted constant / inline const (a Lean global), or compiler-made drop glue: not a function
            if not ts and d['src'] == 'TraitImpl' and d['name'].rsplit('::', 1)[-1] in ('call', 'call_mut', 'call_once') and len(ds) > 1:
                continue    # a closure's unused Fn/FnMut/FnOnce variant: Aeneas only emits the ones that are called
                            # (if it failed instead, the error is logged against the function and caught below)
            if not ts:
                a_ok = False
                r['msgs'].append({'stage': 'aeneas', 'msg': 'not emitted (absent from translation.json)', 'decl': d['name']})
                continue
            for t in ts:
                if t.get('is_opaque'):
                    a_ok = False
                b = by_lean.get(t.get('_short'))
                if b is None:
                    a_ok = False
                    r['msgs'].append({'stage': 'aeneas', 'msg': 'no Lean definition emitted', 'decl': d['name']})
                else:
                    myblocks.append(b)
                    if b['kind'] == 'axiom':
                        a_ok = False
                    if b['has_sorry']:
                        a_ok = False
                        for s in b['sorry_msgs']:
                            r['msgs'].append({'stage': 'aeneas', 'msg': 'hole in output: ' + resolve(s)})
        for e in ent_by_owner.get(key, []):
            if e['level'] == 'Error' and not e['msg'].startswith('Ignoring the body') :
                r['msgs'].append({'stage': 'aeneas', 'msg': resolve(short(e['msg'])), 'emitter': e.get('compiler_source'), 'src_line': e['source'] and e['source']['beg'], 'ext_src': (e['source']['file'] if e['source'] and e['source']['file'] not in lfiles else None)})
                a_ok = False
            elif e['level'] == 'Warn' and 'Could not translate' in e['msg']:
                a_ok = False
                dn = e.get('name') or ''
                if dn and not dn.startswith(llbc['crate'] + '::') and e.get('cause'):
                    # an external item this function uses could not be translated
                    r['msgs'].append({'stage': 'aeneas', 'msg': 'uses external `%s`, which Aeneas cannot translate: %s' % (short(dn, 90), short(e['cause'], 100)),
                                      'emitter': e.get('cause_emitter'), 'external_item': dn})
        r['lean_names'] = [b['lean_name'] for b in myblocks]
        spec = [m for m in r['msgs'] if m['stage'] == 'aeneas' and not m['msg'].startswith(('not emitted', 'no Lean definition'))]
        if spec:
            r['msgs'] = [m for m in r['msgs'] if m['stage'] != 'aeneas'] + sorted(spec, key=lambda m: m['msg'].startswith('hole in output'))
        if not a_ok:
            r['aeneas'] = 'fail'
            if not any(m['stage'] == 'aeneas' for m in r['msgs']):
                r['msgs'].append({'stage': 'aeneas', 'msg': 'emitted as opaque/axiom without a logged error'})
            continue
        r['aeneas'] = 'ok'
        if 'lake' not in res:
            continue
        l_ok = True
        for b in myblocks:
            if b['errors']:
                l_ok = False
                root = lean_root(b)
                r['msgs'].append({'stage': 'lean', 'msg': root['msg'], 'cascade_from': root['cascade'], 'aeneas_hole': root.get('aeneas_hole', False)})
            elif b['sorry_warn']:
                l_ok = False
                root = taint_root(b)
                r['msgs'].append({'stage': 'lean', 'msg': root['msg'], 'cascade_from': root['cascade'], 'aeneas_hole': root.get('aeneas_hole', False), 'via_sorry': True})
        r['lean'] = 'ok' if l_ok else 'fail'
    # --- dependencies (Lean-level): for every function that has Lean text
    def deps_of(r):
        loc, ax, lib = set(), set(), set()
        mine = set(r['lean_names'])
        for ln in r['lean_names']:
            b = by_lean[ln]
            for tok in set(IDENT.findall(b['body'])):
                if tok in mine:
                    continue
                if tok in all_names:
                    if tok in lean_owner:
                        loc.add(tok)        # a function of this crate (if Aeneas failed on it, it is an axiom here: still a local callee)
                    elif tok in axioms:
                        ax.add(tok)
                    else:
                        # non-function declaration of this file (type, trait impl, global) or an external def
                        b2 = by_lean[tok]
                        if b2['kind'] in ('def',) and b2['rust_name'] and not b2['rust_name'].startswith(llbc['crate'] + '::'):
                            lib.add('extracted:' + tok)
                elif tok.startswith(LIB_PREFIX) and '.' in tok:
                    lib.add(tok)
        return loc, ax, lib
    for key in [('src', i) for i in recs] + [('extra', i) for i in extra]:
        r = owner(key)
        if r['lean_names']:
            loc, ax, lib = deps_of(r)
            r['dep_local'] = sorted(set(str(owner(lean_owner[x])['id']) for x in loc if owner(lean_owner[x]) is not r))
            r['dep_axioms'] = sorted(ax)
            r['dep_lib'] = sorted(lib)
        else:
            r['dep_local'], r['dep_axioms'], r['dep_lib'] = [], [], []
    allr = {str(r['id']): r for r in list(recs.values()) + list(extra.values())}
    # transitive cleanliness: the function and everything local it calls compile, and no axiom is used
    memo = {}

    def clean(i, stack=()):
        if i in memo:
            return memo[i]
        r = allr[i]
        if not (r['charon'] == 'ok' and r['aeneas'] == 'ok' and r['lean'] == 'ok'):
            memo[i] = (False, False)
            return memo[i]
        ok, noax = True, not r['dep_axioms']
        memo[i] = (True, noax)   # provisional (recursion)
        for j in r['dep_local']:
            if j in stack:
                continue
            o, n = clean(j, stack + (i,))
            ok, noax = ok and o, noax and n
        memo[i] = (ok, ok and noax)
        return memo[i]
    sys.setrecursionlimit(100000)
    for i, r in allr.items():
        o, n = clean(i)
        r['ok'] = bool(r['charon'] == 'ok' and r['aeneas'] == 'ok' and r['lean'] == 'ok')
        r['ok_closure'] = o
        r['ok_closure_no_axiom'] = n
    for r in allr.values():
        r['decls'] = [{'id': d['id'], 'name': d['name'], 'body': d['body'], 'src': d['src'] if isinstance(d['src'], str) else None} for d in r['decls']]
    # crate-level: non-function declarations that fail in Lean
    nf = []
    for b in blocks:
        if b['errors'] and (b['lean_name'] not in lean_owner):
            nf.append({'lean_name': b['lean_name'], 'kind': b['kind'], 'rust_name': b['rust_name'], 'msg': lean_root(b)})
    res['lean_failed_nonfunction_decls'] = nf
    res['lean_orphan_errors'] = orphan_lean[:50]
    res['lean_blocks'] = collections.Counter(b['kind'] for b in blocks)
    res['axioms'] = [{'lean_name': b['lean_name'], 'rust_name': b['rust_name']} for b in blocks if b['kind'] == 'axiom']
    return list(allr.values())


if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'data', 'results'), exist_ok=True)
    ov = {}
    op = os.path.join(HERE, 'data', 'overrides.json')
    if os.path.exists(op):
        ov = json.load(open(op))
    if sys.argv[1] in ('run', 'rejoin', 'build'):
        cdir = sys.argv[2]
        name = re.sub(r'-\d+\.\d+\.\d+.*$', '', cdir)
        if sys.argv[1] == 'run':
            res = run_crate(cdir, do_lean='--no-lean' not in sys.argv, overrides=ov.get(name))
        else:
            res = finish(name, do_lean='--no-lean' not in sys.argv, build=(sys.argv[1] == 'build'))
        fs = [f for f in res['functions'] if f['origin'] == 'source']
        c = collections.Counter((f['charon'], f['aeneas'], f['lean']) for f in fs)
        print(name, 'rounds', len(res['rounds']), 'surgery', [e['name'] for e in res['surgery']], 'marks', len(res['opaque_marks']))
        print('  as_is:', res['as_is'])
        for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
            print('  ', k, v)
        print('  lake', res.get('lake'), 'lean_lines', res.get('lean_lines'), 'stuck', [r.get('stuck') for r in res['rounds'] if r.get('stuck')])
    elif sys.argv[1] == 'all':
        pins = json.load(open(os.path.join(HERE, 'data', 'selection', 'pins.json')))
        for p in pins:
            subprocess.call([sys.executable, os.path.abspath(__file__), 'run', f"{p['name']}-{p['version']}"])
