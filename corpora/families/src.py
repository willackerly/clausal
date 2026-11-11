#!/usr/bin/env python3
"""Print the source of corpus declarations.  usage: src.py NAME [NAME ...]   (read-only)"""
import json, sys, os
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
want = set(sys.argv[1:])
for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
    d = json.loads(l)
    if d['name'] in want or d.get('userName') in want:
        p = os.path.join(REPO, 'corpora/ns', d['module'].replace('.', '/') + '.lean')
        L = open(p).read().split('\n')
        print(f"-- {d['name']}  [{d['module']}:{d['line']}-{d['endLine']}] kind={d['kind']} proofSize={d['proofSize']}")
        print('\n'.join(L[d['line'] - 1:d['endLine']]))
