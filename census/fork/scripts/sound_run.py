#!/usr/bin/env python3
"""Soundness check: run sampled functions in Rust and in the generated Lean on the same generated inputs and compare.

    sound_run.py gen      write the Rust harnesses (work/sound/) and the Lean files (lean/sound/Generated/Sound<Crate>.lean)
    sound_run.py rust     build and run the Rust side          -> data/sound/rust.<crate>.txt
    sound_run.py lean     `lake build` the Lean side (one batch build per crate; `#eval` output is read from the log)
                                                              -> data/sound/lean.<crate>.txt
    sound_run.py compare  -> data/sound_results.json

Rust side. A copy of the crate gets, at the end of the source file of each sampled function, a module with one
`#[unsafe(no_mangle)] extern "C"` function per case (inside the function's own module, so private items are reachable).
A small binary crate links the copy and calls them. Built in the dev profile: integer overflow panics, as in the
semantics Aeneas models. A panic is caught and printed as PANIC.

Lean side. `lake` writes no .olean for a module with an error, so the generated file itself cannot be imported. The Lean
file for a crate holds the header of the generated file, then, verbatim and in the original order, the declarations in
the dependency closure of the sampled functions (found by scanning identifiers), then one `#eval` per input. `Result` is observed with the
library's `Result.match` (as its own `Repr` instance does): `fail` is printed as PANIC, `div` as DIV. One deviation from verbatim: the line `noncomputable section` of the header is dropped
when `#eval` needs compiled code (recorded in the output).

Inputs: random.Random(20261110) per case, a mix of edge values and uniform values of each type.
"""
import importlib.util, json, os, random, re, shutil, subprocess, sys

FORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.dirname(FORK)
spec = importlib.util.spec_from_file_location('census', os.path.join(CENSUS, 'scripts', 'census.py'))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
SV = os.environ.get('SOUND_VARIANT', 'p4')     # which build's generated Lean is evaluated (the samples were drawn on p4)
OUT = os.path.join(FORK, 'data', 'sound' if SV == 'p4' else 'sound_' + SV)
WORK = os.path.join(FORK, 'work', 'sound' if SV == 'p4' else 'sound_' + SV)
LEAN = os.path.join(FORK, 'lean', 'sound')
N = 40
CRATES = {'rust_decimal': ('rust_decimal-1.43.0', 'RustDecimal', 'rust_decimal'), 'time': ('time-0.3.55', 'Time', 'time'),
          'untrusted': ('untrusted-0.9.0', 'Untrusted', 'untrusted'), 'indexmap': ('indexmap-2.14.2', 'Indexmap', 'indexmap')}

WD = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
LEAN_PRE = r'''
def sR {α : Type} (f : α → String) (r : Result α) : String :=
  match Result.match r with | .ok v => f v | .div => "DIV" | .vis _ _ => "PANIC"
def sU {ty : UScalarTy} (x : UScalar ty) : String := toString x.val
def sI {ty : IScalarTy} (x : IScalar ty) : String := toString x.val
def sAU {ty : UScalarTy} {n : Usize} (a : Aeneas.Std.Array (UScalar ty) n) : String := toString (a.val.map (·.val))
def sSU {ty : UScalarTy} (a : Aeneas.Std.Slice (UScalar ty)) : String := toString (a.val.map (·.val))
def le4 (x : Nat) : List Nat := [x % 256, x / 256 % 256, x / 65536 % 256, x / 16777216 % 256]
'''
SDEC_LEAN = 'def sDec (d : decimal.Decimal) : String := toString (le4 d.flags.val ++ le4 d.lo.val ++ le4 d.mid.val ++ le4 d.hi.val)\n'
SWD_LEAN = 'def sWd (w : weekday.Weekday) : String := match w with\n' + ''.join('  | .%s => "%s"\n' % (d, d) for d in WD)

# id, sample, crate, rust source file, input types, rust body (a String expression), lean expression (a String), extra lean defs
CASES = [
    dict(id='A4', crate='time', file='src/weekday.rs', fn='Weekday::number_days_from_sunday', ins=['wd'],
         rust='format!("{}", {0}.number_days_from_sunday())', lean='sR sU (weekday.Weekday.number_days_from_sunday {0})',
         names=['weekday.Weekday.number_days_from_sunday']),
    dict(id='A5', crate='untrusted', file='src/no_panic.rs', fn='no_panic::Slice::as_slice_less_safe', ins=['bytes'],
         rust='format!("{:?}", Slice::new(&{0}).as_slice_less_safe())', lean='sR sSU (no_panic.Slice.as_slice_less_safe { bytes := {0} })',
         names=['no_panic.Slice.as_slice_less_safe']),
    dict(id='A9', crate='rust_decimal', file='src/ops/common.rs', fn='Buf24::low64', ins=['u32'] * 6,
         rust='format!("{}", Buf24 { data: [{0}, {1}, {2}, {3}, {4}, {5}] }.low64())',
         lean='sR sU (ops.common.Buf24.low64 { data := Aeneas.Std.Array.make 6#usize [{0}, {1}, {2}, {3}, {4}, {5}] })', names=['ops.common.Buf24.low64']),
    dict(id='A12', crate='rust_decimal', file='src/ops/div.rs', fn='ops::div::increase_scale64', ins=['u32'] * 4 + ['u64pow'],
         rust='{ let mut n = Buf16 { data: [{0}, {1}, {2}, {3}] }; increase_scale64(&mut n, {4}); format!("{:?}", n.data) }',
         lean='sR (fun b => sAU b.data) (ops.div.increase_scale64 { data := Aeneas.Std.Array.make 4#usize [{0}, {1}, {2}, {3}] } {4})', names=['ops.div.increase_scale64']),
    dict(id='A14', crate='rust_decimal', file='src/ops/div.rs', fn='ops::div::unscale_from_overflow', ins=['u32'] * 3 + ['i32scale', 'bool'],
         rust='{ let mut n = Buf12 { data: [{0}, {1}, {2}] }; let r = unscale_from_overflow(&mut n, {3}, {4}); '
              'format!("{} {:?}", match r { Ok(v) => format!("Ok({})", v), Err(_) => String::from("Err") }, n.data) }',
         lean='sR (fun (r, b) => (match r with | .Ok v => s!"Ok({v.val})" | .Err _ => "Err") ++ " " ++ sAU b.data) '
              '(ops.div.unscale_from_overflow { data := Aeneas.Std.Array.make 3#usize [{0}, {1}, {2}] } {3} {4})', names=['ops.div.unscale_from_overflow']),
    dict(id='A24', crate='time', file='src/error/component_range.rs', fn='ComponentRange::unconditional', ins=['str'],
         rust='{ let c = ComponentRange::unconditional({0}); format!("{:?} {}", c.name.as_bytes(), c.is_conditional) }',
         lean='sR (fun c => sSU (c.«name» : Aeneas.Std.Slice Std.U8) ++ " " ++ toString c.is_conditional) (error.component_range.ComponentRange.unconditional {0})',
         names=['error.component_range.ComponentRange.unconditional']),
    dict(id='B1', crate='rust_decimal', file='src/decimal.rs', fn='Decimal::scale', ins=['u32'] * 4,
         rust='format!("{}", Decimal { flags: {0}, hi: {1}, lo: {2}, mid: {3} }.scale())',
         lean='sR sU (decimal.Decimal.scale { flags := {0}, hi := {1}, lo := {2}, mid := {3} })', names=['decimal.Decimal.scale']),
    dict(id='B2', crate='rust_decimal', file='src/decimal.rs', fn='Decimal::max_value', ins=[],
         rust='format!("{:?}", Decimal::max_value().serialize())', lean='sR sDec decimal.Decimal.max_value', names=['decimal.Decimal.max_value'], pre=SDEC_LEAN),
    dict(id='B6', crate='rust_decimal', file='src/ops/common.rs', fn='Buf16::low64', ins=['u32'] * 4,
         rust='format!("{}", Buf16 { data: [{0}, {1}, {2}, {3}] }.low64())',
         lean='sR sU (ops.common.Buf16.low64 { data := Aeneas.Std.Array.make 4#usize [{0}, {1}, {2}, {3}] })', names=['ops.common.Buf16.low64']),
    dict(id='B10', crate='rust_decimal', file='src/ops/common.rs', fn='Dec64::to_decimal', ins=['bool', 'u32scale', 'u32', 'u64'],
         rust='format!("{:?}", Dec64 { negative: {0}, scale: {1}, hi: {2}, low64: {3} }.to_decimal().serialize())',
         lean='sR sDec (ops.common.Dec64.to_decimal { negative := {0}, scale := {1}, hi := {2}, low64 := {3} })', names=['ops.common.Dec64.to_decimal'], pre=SDEC_LEAN),
    dict(id='B12', crate='rust_decimal', file='src/ops/array.rs', fn='ops::array::sub_by_internal', ins=['u32s', 'u32s'],
         rust='{ let mut v = {0}; let o = sub_by_internal(&mut v, &{1}); format!("{} {:?}", o, v) }',
         lean='sR (fun (o, s) => s!"{o.val} " ++ sSU s) (ops.array.sub_by_internal {0} {1})', names=['ops.array.sub_by_internal']),
    dict(id='B14', crate='rust_decimal', file='src/ops/common.rs', fn='Buf12::lo', ins=['u32'] * 3,
         rust='format!("{}", Buf12 { data: [{0}, {1}, {2}] }.lo())',
         lean='sR sU (ops.common.Buf12.lo { data := Aeneas.Std.Array.make 3#usize [{0}, {1}, {2}] })', names=['ops.common.Buf12.lo']),
    dict(id='B19', crate='rust_decimal', file='src/str.rs', fn='str::handle_separator', ins=['bool', 'bool', 'bool', 'bool', 'numbytes', 'u64small', 'u8scale'],
         rust='match handle_separator::<{0}, {1}, {2}, {3}>(&{4}, {5}, {6}) { Ok(d) => format!("Ok {:?}", d.serialize()), Err(_) => String::from("Err") }',
         lean='sR (fun r => match r with | .Ok d => "Ok " ++ sDec d | .Err _ => "Err") (str.handle_separator {0} {1} {2} {3} {4} {5} {6})',
         names=['str.handle_separator'], pre=SDEC_LEAN),
    dict(id='B21', crate='rust_decimal', file='src/ops/common.rs', fn='Buf24::upper_word', ins=['u32z'] * 6,
         rust='format!("{}", Buf24 { data: [{0}, {1}, {2}, {3}, {4}, {5}] }.upper_word())',
         lean='sR sU (ops.common.Buf24.upper_word { data := Aeneas.Std.Array.make 6#usize [{0}, {1}, {2}, {3}, {4}, {5}] })', names=['ops.common.Buf24.upper_word']),
    dict(id='B22', crate='rust_decimal', file='src/ops/common.rs', fn='Buf12::from_dec64', ins=['bool', 'u32scale', 'u32', 'u64'],
         rust='format!("{:?}", Buf12::from_dec64(&Dec64 { negative: {0}, scale: {1}, hi: {2}, low64: {3} }).data)',
         lean='sR (fun b => sAU b.data) (ops.common.Buf12.from_dec64 { negative := {0}, scale := {1}, hi := {2}, low64 := {3} })', names=['ops.common.Buf12.from_dec64']),
    dict(id='B28', crate='rust_decimal', file='src/ops/common.rs', fn='Buf24::high64', ins=['u32'] * 6,
         rust='format!("{}", Buf24 { data: [{0}, {1}, {2}, {3}, {4}, {5}] }.high64())',
         lean='sR sU (ops.common.Buf24.high64 { data := Aeneas.Std.Array.make 6#usize [{0}, {1}, {2}, {3}, {4}, {5}] })', names=['ops.common.Buf24.high64']),
    # stratum C: functions that compile only with patch (iv) (data/sound_sample_C.json)
    dict(id='C0', crate='indexmap', file='src/lib.rs', fn='set::slice::Slice::is_empty', ins=['u32set'],
         rust='{ let s = {0}.into_iter().collect::<IndexSet<u32>>(); format!("{}", s.as_slice().is_empty()) }',
         lean='sR toString (set.slice.Slice.is_empty { entries := {0} })', names=['set.slice.Slice.is_empty']),
    dict(id='C4', crate='untrusted', file='src/input.rs', fn='<Input as From<&[u8]>>::from', ins=['bytes'],
         rust='format!("{:?}", <Input as From<&[u8]>>::from(&{0}[..]).value.as_slice_less_safe())',
         lean='sR (fun i => sSU i.value.bytes) (input.Input.Insts.CoreConvertFromSharedASliceU8.from {0})', names=['input.Input.Insts.CoreConvertFromSharedASliceU8.from']),
    dict(id='C6', crate='indexmap', file='src/lib.rs', fn='<set::slice::Slice<T> as Index<usize>>::index', ins=['u32set', 'usizeidx'],
         rust='{ let s = {0}.into_iter().collect::<IndexSet<u32>>(); format!("{}", s.as_slice()[{1}]) }',
         lean='sR sU (set.slice.Slice.Insts.CoreOpsIndexIndexUsizeT.index { entries := {0} } {1})', names=['set.slice.Slice.Insts.CoreOpsIndexIndexUsizeT.index']),
    dict(id='C9', crate='untrusted', file='src/no_panic.rs', fn='no_panic::Slice::new', ins=['bytes'],
         rust='format!("{:?}", Slice::new(&{0}).bytes)', lean='sR (fun s => sSU s.bytes) (no_panic.Slice.new {0})', names=['no_panic.Slice.new']),
    dict(id='C11', crate='indexmap', file='src/lib.rs', fn='<map::slice::Slice<K, V> as Index<usize>>::index', ins=['u32pairs', 'usizeidx'],
         rust='{ let m = {0}.into_iter().collect::<IndexMap<u32, u32>>(); format!("{}", m.as_slice()[{1}]) }',
         lean='sR sU (map.slice.Slice.Insts.CoreOpsIndexIndexUsizeV.index { entries := {0} } {1})', names=['map.slice.Slice.Insts.CoreOpsIndexIndexUsizeV.index']),
    dict(id='C12', crate='untrusted', file='src/reader.rs', fn='Reader::new', ins=['bytes'],
         rust='{ let r = Reader::new(crate::Input::from(&{0})); format!("{:?} {}", r.input.as_slice_less_safe(), r.i) }',
         lean='sR (fun r => sSU r.input.bytes ++ " " ++ sU r.i) (reader.Reader.new { value := { bytes := {0} } })', names=['reader.Reader.new']),
    dict(id='C14', crate='untrusted', file='src/input.rs', fn='Input::from', ins=['bytes'],
         rust='format!("{:?}", Input::from(&{0}).value.as_slice_less_safe())', lean='sR (fun i => sSU i.value.bytes) (input.Input.from {0})', names=['input.Input.from']),
    dict(id='C16', crate='indexmap', file='src/lib.rs', fn='set::slice::Slice::len', ins=['u32set'],
         rust='{ let s = {0}.into_iter().collect::<IndexSet<u32>>(); format!("{}", s.as_slice().len()) }',
         lean='sR sU (set.slice.Slice.len { entries := {0} })', names=['set.slice.Slice.len']),
    dict(id='C21', crate='untrusted', file='src/input.rs', fn='Input::as_slice_less_safe', ins=['bytes'],
         rust='format!("{:?}", Input::from(&{0}).as_slice_less_safe())', lean='sR sSU (input.Input.as_slice_less_safe { value := { bytes := {0} } })',
         names=['input.Input.as_slice_less_safe']),
    dict(id='B29', crate='time', file='src/weekday.rs', fn='Weekday::previous', ins=['wd'],
         rust='format!("{:?}", {0}.previous())', lean='sR sWd (weekday.Weekday.previous {0})', names=['weekday.Weekday.previous'], pre=SWD_LEAN),
]


def gen_value(t, rng, k):
    """-> (rust literal, lean literal)"""
    def u(bits, v):
        return ('%du%d' % (v, bits), '%d#u%d' % (v, bits))
    if t in ('u32', 'u32z'):
        edge = [0, 1, 5, 9, 10, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF, 0xFFFF, 0x10000]
        if t == 'u32z':
            v = 0 if rng.random() < 0.6 else rng.choice(edge + [rng.getrandbits(32)])
        else:
            v = rng.choice(edge) if rng.random() < 0.35 else rng.getrandbits(32)
        return u(32, v)
    if t == 'u64':
        edge = [0, 1, 10, 0xFFFFFFFF, 0x100000000, 0xFFFFFFFFFFFFFFFF, 0x8000000000000000]
        return u(64, rng.choice(edge) if rng.random() < 0.35 else rng.getrandbits(64))
    if t == 'u64pow':     # powers of ten (the documented use) and arbitrary values (which overflow and must panic)
        return u(64, rng.choice([10 ** rng.randint(0, 9), 10 ** rng.randint(0, 19), rng.getrandbits(64), rng.getrandbits(33), 0, 1]))
    if t == 'u64small':
        return u(64, rng.choice([0, 1, 9, 12345, 10 ** rng.randint(0, 18), rng.getrandbits(40), 0xFFFFFFFFFFFFFFFF // 10, rng.getrandbits(64)]))
    if t == 'u32scale':
        return u(32, rng.choice([0, 1, 5, 28, 29, 255, rng.randint(0, 28), rng.getrandbits(32)]))
    if t == 'u8scale':
        return u(8, rng.choice([0, 1, 5, 27, 28, 29, 255, rng.randint(0, 28)]))
    if t == 'i32scale':
        v = rng.choice([0, 1, 2, 28, -1, -2147483648, 2147483647, rng.randint(-5, 40), rng.randint(-2 ** 31, 2 ** 31 - 1)])
        return ('%di32' % v if v >= 0 else '(%di32)' % v, '%d#i32' % v if v >= 0 else '(%d)#i32' % v)
    if t == 'bool':
        b = rng.random() < 0.5
        return ('true' if b else 'false', 'true' if b else 'false')
    if t == 'wd':
        d = WD[k % 7]
        return ('Weekday::' + d, 'weekday.Weekday.' + d)
    if t == 'usizeidx':
        v = rng.randint(0, 6)
        return ('%dusize' % v, '%d#usize' % v)
    if t in ('u32set', 'u32pairs'):
        keys = rng.sample([0, 1, 2, 7, 0xFFFFFFFF, rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(16)], rng.randint(0, 5))
        keys = list(dict.fromkeys(keys))
        vals = [rng.getrandbits(32) for _ in keys]
        if t == 'u32set':
            rust = '[%s]' % ', '.join('%du32' % k for k in keys) if keys else '[0u32; 0]'
            elems = ['({ hash := 0#usize, key := %d#u32, value := () } : Bucket Std.U32 Unit)' % k for k in keys]
            ety = 'Bucket Std.U32 Unit'
        else:
            rust = '[%s]' % ', '.join('(%du32, %du32)' % kv for kv in zip(keys, vals)) if keys else '[(0u32, 0u32); 0]'
            elems = ['({ hash := 0#usize, key := %d#u32, value := %d#u32 } : Bucket Std.U32 Std.U32)' % kv for kv in zip(keys, vals)]
            ety = 'Bucket Std.U32 Std.U32'
        lean = '(Aeneas.Std.Array.to_slice (Aeneas.Std.Array.make %d#usize [%s]))' % (len(elems), ', '.join(elems)) if elems else '(Aeneas.Std.Slice.new (%s))' % ety
        return (rust, lean)
    if t in ('bytes', 'numbytes', 'u32s', 'str'):
        n = rng.randint(0, 6)
        if t == 'u32s':
            vals = [rng.choice([0, 1, 0xFFFFFFFF, rng.getrandbits(32)]) for _ in range(rng.randint(0, 4))]
            rust = 'vec![%s]' % ', '.join('%du32' % v for v in vals) if vals else 'Vec::<u32>::new()'
            ty = 'u32'
        else:
            if t == 'numbytes':
                vals = [rng.choice(list(b'0123456789') * 3 + list(b'._-+ex')) for _ in range(n)]
            elif t == 'str':
                vals = [rng.choice(list(b'abcdefghijklmnopqrstuvwxyz_ ')) for _ in range(n)]
            else:
                vals = [rng.getrandbits(8) for _ in range(n)]
            ty = 'u8'
            if t == 'str':
                rust = '"%s"' % bytes(vals).decode()
            else:
                rust = '[%s]' % ', '.join('%du8' % v for v in vals) if vals else '[0u8; 0]'
        lean = '(Aeneas.Std.Array.to_slice (Aeneas.Std.Array.make %d#usize [%s]))' % (len(vals), ', '.join('%d#%s' % (v, ty) for v in vals))
        if not vals:
            lean = '(Aeneas.Std.Slice.new Std.%s)' % ty.upper()
        return (rust, lean)
    raise SystemExit('type? ' + t)


def fill(tpl, vals):
    return re.sub(r'\{(\d+)\}', lambda m: vals[int(m.group(1))], tpl)


def inputs():
    out = {}
    for ci, c in enumerate(CASES):
        rng = random.Random(20261110 * 1000 + ci)
        n = 1 if not c['ins'] else (7 if c['ins'] == ['wd'] else N)
        out[c['id']] = [[gen_value(t, rng, k) for t in c['ins']] for k in range(n)]
    return out


def closure(crate, names):
    """header, the declarations in the dependency closure of `names` (verbatim, original order), footer"""
    cdir, mod, ns = CRATES[crate]
    path = os.path.join(FORK, 'runs', SV + '-shipped', 'work', 'run', crate, 'lean', 'Generated', mod + '.lean')
    lines = open(path).read().split('\n')
    blocks, _ = C.parse_lean(path)
    # mutual groups: a bare `mutual` line ... a bare `end` line
    groups, cur = [], None
    for i, l in enumerate(lines, 1):
        if l.strip() == 'mutual' and not l.startswith(' '):
            cur = i
        elif l.strip() == 'end' and not l.startswith(' ') and cur is not None:
            groups.append((cur, i))
            cur = None
    def group_of(b):
        return next((g for g in groups if g[0] < b['start'] and b['end'] <= g[1] + 0 or (g[0] < b['start'] <= g[1])), None)
    by_name = {}
    for b in blocks:
        if b['lean_name']:
            by_name.setdefault(b['lean_name'], b)
    need, todo = set(), list(names)
    missing = [n for n in names if n not in by_name]
    if missing:
        raise SystemExit('not in the generated file: %s' % missing)
    while todo:
        n = todo.pop()
        b = by_name[n]
        if b['start'] in need:
            continue
        need.add(b['start'])
        g = group_of(b)
        members = [x for x in blocks if g and g[0] < x['start'] <= g[1]] if g else [b]
        for x in members:
            need.add(x['start'])
            for tok in C.IDENT.findall(x['body']):
                parts = tok.split('.')
                for j in range(len(parts), 0, -1):
                    cand = '.'.join(parts[:j])
                    if cand in by_name and by_name[cand]['start'] not in need:
                        todo.append(cand)
    first = blocks[0]['start']
    header = lines[:first - 1]
    body, done_groups = [], set()
    for b in blocks:
        if b['start'] not in need:
            continue
        g = group_of(b)
        if g:
            if g not in done_groups:
                done_groups.add(g)
                body += lines[g[0] - 1:g[1]] + ['']
            continue
        txt = lines[b['start'] - 1:b['end']]
        while txt and (txt[-1].strip() in ('', 'mutual') or re.match(r'^end \S+$', txt[-1])):
            txt.pop()
        body += txt + ['']
    return header, body, 'end ' + ns, len([b for b in blocks if b['start'] in need])


def gen():
    ins = inputs()
    os.makedirs(OUT, exist_ok=True)
    json.dump({k: [[r for r, _ in row] for row in v] for k, v in ins.items()}, open(os.path.join(OUT, 'inputs.json'), 'w'), indent=0)
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    for crate, (cdir, mod, ns) in CRATES.items():
        cases = [c for c in CASES if c['crate'] == crate]
        # ---- Rust
        dst = os.path.join(WORK, crate)
        shutil.copytree(os.path.join(CENSUS, 'crates', cdir), dst, symlinks=True)
        byfile = {}
        for c in cases:
            byfile.setdefault(c['file'], []).append(c)
        for k, (f, cs) in enumerate(byfile.items()):
            blk = ['', '#[allow(warnings)]', 'mod __sound_%d {' % k, '    extern crate std;', '    use super::*;',
                   '    use self::std::{format, println, string::String, vec, vec::Vec};',
                   '    fn guard<F: FnOnce() -> String + self::std::panic::UnwindSafe>(f: F) -> String {',
                   '        match self::std::panic::catch_unwind(f) { Ok(s) => s, Err(_) => String::from("PANIC") }', '    }']
            for c in cs:
                blk.append('    #[unsafe(no_mangle)] pub extern "C" fn sound_%s_%s() {' % (crate, c['id'].lower()))
                for i, row in enumerate(ins[c['id']]):
                    blk.append('        println!("SOUND %s %d {}", guard(|| %s));' % (c['id'], i, fill(c['rust'], [r for r, _ in row])))
                blk.append('    }')
            blk.append('}')
            open(os.path.join(dst, f), 'a').write('\n'.join(blk) + '\n')
        b = os.path.join(WORK, 'bin_' + crate)
        os.makedirs(os.path.join(b, 'src'))
        open(os.path.join(b, 'Cargo.toml'), 'w').write('[package]\nname = "soundbin_%s"\nversion = "0.0.0"\nedition = "2021"\n\n[dependencies]\n%s = { path = "../%s" }\n\n[workspace]\n'
                                                       % (crate, cdir.rsplit('-', 1)[0], crate))
        syms = ['sound_%s_%s' % (crate, c['id'].lower()) for c in cases]
        open(os.path.join(b, 'src', 'main.rs'), 'w').write('extern crate %s;\nextern "C" {\n%s}\nfn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n%s}\n' % (
            ns, ''.join('    fn %s();\n' % s for s in syms), ''.join('    unsafe { %s() };\n' % s for s in syms)))
        # ---- Lean
        names = sorted(set(n for c in cases for n in c['names']))
        header, body, footer, nblocks = closure(crate, names)
        pre = LEAN_PRE + ''.join(sorted(set(c.get('pre', '') for c in cases)))
        ev = []
        for c in cases:
            for i, row in enumerate(ins[c['id']]):
                ev.append('#eval IO.println ("SOUND %s %d " ++ %s)' % (c['id'], i, fill(c['lean'], [l for _, l in row])))
        os.makedirs(os.path.join(LEAN, 'Generated'), exist_ok=True)
        for variant, hdr in (('', header), ('C', [l for l in header if l.strip() != 'noncomputable section'])):
            open(os.path.join(LEAN, 'Generated', 'Sound%s%s.lean' % (mod, variant)), 'w').write('\n'.join(hdr + body + [pre] + ev + ['', footer, '']))
        print(crate, 'cases', len(cases), 'closure blocks', nblocks, 'evals', len(ev))


def run_rust():
    env = dict(C.ENV, RUSTFLAGS='--cap-lints allow', CARGO_TARGET_DIR=os.path.join(WORK, 'target'))
    for crate in CRATES:
        b = os.path.join(WORK, 'bin_' + crate)
        log = os.path.join(OUT, 'rust.%s.log' % crate)
        with open(os.path.join(OUT, 'rust.%s.txt' % crate), 'w') as o, open(log, 'w') as e:
            rc = subprocess.call(['cargo', 'run', '-q'], cwd=b, stdout=o, stderr=e, env=env)
        print(crate, 'cargo rc', rc, 'lines', sum(1 for l in open(os.path.join(OUT, 'rust.%s.txt' % crate)) if l.startswith('SOUND')))


def run_lean():
    for crate, (cdir, mod, ns) in CRATES.items():
        res = None
        for variant in ('', 'C'):
            log = os.path.join(OUT, 'lean.%s%s.log' % (crate, variant))
            rc, secs = C.sh(['lake', 'build', 'Generated.Sound%s%s' % (mod, variant)], LEAN, log, timeout=3600)
            txt = C.read(log)
            got = re.findall(r'^(?:info: [^\n]*?: )?(SOUND \S+ \d+ .*)$', txt, re.M)
            errs = len(re.findall(r'^error: ', txt, re.M))
            print(crate, 'variant', repr(variant), 'lake rc', rc, 'secs', secs, 'SOUND lines', len(got), 'errors', errs)
            if res is None or len(got) > len(res[1]):
                res = (variant, got, errs)
            if errs == 0:
                break
        open(os.path.join(OUT, 'lean.%s.txt' % crate), 'w').write('\n'.join(res[1]) + '\n')
        json.dump({'header_variant': 'verbatim' if res[0] == '' else 'without `noncomputable section`', 'errors': res[2]}, open(os.path.join(OUT, 'lean.%s.json' % crate), 'w'))


def compare():
    ins = json.load(open(os.path.join(OUT, 'inputs.json')))
    res = []
    for c in CASES:
        def load(side):
            d = {}
            for l in open(os.path.join(OUT, '%s.%s.txt' % (side, c['crate']))):
                m = re.match(r'SOUND (\S+) (\d+) (.*)$', l.rstrip('\n'))
                if m and m.group(1) == c['id']:
                    d[int(m.group(2))] = m.group(3)
            return d
        r, l = load('rust'), load('lean')
        n = len(ins[c['id']])
        mism = [{'input': ins[c['id']][i], 'rust': r.get(i), 'lean': l.get(i)} for i in range(n) if r.get(i) != l.get(i)]
        res.append({'id': c['id'], 'crate': c['crate'], 'fn': c['fn'], 'file': c['file'], 'inputs': n, 'rust_ran': len(r), 'lean_ran': len(l),
                    'agree': n - len(mism), 'panics_rust': sum(1 for v in r.values() if v == 'PANIC'), 'panics_lean': sum(1 for v in l.values() if v == 'PANIC'),
                    'mismatches': mism[:10], 'n_mismatches': len(mism)})
        print('%-4s %-13s %-36s inputs %2d  rust %2d  lean %2d  agree %2d  panics rust/lean %d/%d' % (c['id'], c['crate'], c['fn'], n, len(r), len(l), n - len(mism),
              res[-1]['panics_rust'], res[-1]['panics_lean']))
    json.dump(res, open(os.path.join(FORK, 'data', 'sound_results.json' if SV == 'p4' else 'sound_results_%s.json' % SV), 'w'), indent=1)


if __name__ == '__main__':
    {'gen': gen, 'rust': run_rust, 'lean': run_lean, 'compare': compare}[sys.argv[1]]()
