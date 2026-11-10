#!/usr/bin/env python3
"""Corpus selection for the K3 census. Written and run BEFORE any translation result existed.

Inputs: crates.io API snapshots taken 2026-11-10 (work/select/*.json, slimmed copy kept in
data/selection/snapshot.json). Output: data/selection/corpus.json.

Rule for the five "popular" crates
  population : the 200 most-downloaded crates on crates.io (all-time downloads), snapshot above
  excluded   : by name/description only, never by looking at how a crate translates
     E1 proc-macro, derive or build-script helper crates
     E2 OS / FFI bindings, or crates whose main job is system calls, files, sockets, entropy,
        terminals, time-zone lookup, or that link C/assembly
     E3 async runtimes, futures, networking / TLS stacks, logging and tracing infrastructure
     E4 synchronisation primitives and global-state cells
     E5 macro-only, marker-only or data-only crates (nothing to translate)
     E6 already in the business-logic set
  eligible   : everything else, sorted by name
  draw       : random.Random(SEED).sample(eligible, 5), SEED = 20261110
"""
import json, random, sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 20261110
EXCL = {
 'E1': "syn quote proc-macro2 thiserror-impl serde_derive autocfg cc version_check tokio-macros futures-macro rustversion pkg-config clap_derive darling_core darling_macro darling tracing-attributes rustc_version synstructure time-macros async-trait strum_macros displaydoc zerocopy-derive yoke-derive zerovec-derive zerofrom-derive",
 'E2': "getrandom libc windows-sys socket2 rustix linux-raw-sys windows_x86_64_msvc cpufeatures mio windows_x86_64_gnu windows_aarch64_msvc windows-targets windows_i686_msvc windows_i686_gnu windows_aarch64_gnullvm windows_x86_64_gnullvm errno tempfile nix ring signal-hook-registry wasi redox_syscall anstream iana-time-zone anstyle-query walkdir same-file openssl-probe glob",
 'E3': "log tokio futures-core futures-util futures-task hyper rustls http-body futures-sink futures-channel tracing-core tracing futures-io h2 rustls-webpki tokio-util tokio-rustls futures reqwest futures-executor tower hyper-rustls tower-service want tracing-subscriber",
 'E4': "once_cell parking_lot_core parking_lot lock_api lazy_static crossbeam-utils thread_local crossbeam-epoch colorchoice spin sync_wrapper try-lock crossbeam-deque",
 'E5': "thiserror cfg-if pin-project-lite webpki-roots memoffset stable_deref_trait pin-utils tinyvec_macros icu_properties_data icu_normalizer_data",
 'E6': "semver shlex",
}
snap = json.load(open(os.path.join(HERE, 'data/selection/snapshot.json')))
top = snap['top200']
names = [c['name'] for c in top]
why = {}
for code, s in EXCL.items():
    for n in s.split():
        assert n in names, n
        assert n not in why, n
        why[n] = code
eligible = sorted(n for n in names if n not in why)
drawn = random.Random(SEED).sample(eligible, 5)
ver = {c['name']: c['max_stable_version'] for c in top}
out = {
 'seed': SEED, 'population': names, 'excluded': why, 'eligible': eligible,
 'popular': [{'name': n, 'version': ver[n]} for n in drawn],
 'business': snap['business'],
}
json.dump(out, open(os.path.join(HERE, 'data/selection/corpus.json'), 'w'), indent=1)
print(len(names), 'population;', len(why), 'excluded;', len(eligible), 'eligible')
print('eligible:', ' '.join(eligible))
print('drawn:', [(n, ver[n]) for n in drawn])
