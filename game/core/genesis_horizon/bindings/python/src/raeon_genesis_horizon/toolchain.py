"""One explicit compiler family and the coherent Section 5 native substrate.

No implicit fallback to symbolic execution is permitted.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
import sys


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def root_path():
    for parent in Path(__file__).resolve().parents:
        if (parent / 'data/platform/genesis-runtime-lock.json').is_file():
            return parent
    raise RuntimeError('Missing installed Horizon data root')


def initialize(root=None, upstream=None):
    root = Path(root or root_path()).resolve()
    lock = json.loads((root / 'data/platform/genesis-runtime-lock.json').read_text(encoding='utf8'))
    upstream = Path(upstream or os.environ.get('RAEON_GENESIS_UPSTREAM', root / lock['default_dependency_root'])).resolve()
    for relative, expected in lock['selected_source_paths_and_hashes'].items():
        source = (upstream / relative).resolve()
        if not source.is_relative_to(upstream) or not source.is_file() or file_hash(source) != expected['sha256']:
            raise RuntimeError('DEPENDENCY_INTEGRITY: ' + relative)
    local_profile = lock.get('required_runtime_data', {}).get('profile')
    if local_profile and file_hash(root / local_profile['path']) != local_profile['sha256']:
        raise RuntimeError('PROFILE_INTEGRITY')
    frontend = upstream / 'language/10 Genesis Surface Language/12_REFERENCE_IMPLEMENTATION'
    road = upstream / 'language/5 Rainbow Road/12_REFERENCE_IMPLEMENTATION'
    paths = [frontend, road, road / 'vendor_section04', road / 'vendor_section04/vendor_section03']
    for path in reversed(paths):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    # Refuse a process already contaminated by another vendored runtime family.
    checks = {
        'genesis_frontend': frontend,
        'genesis_rainbow_road': road,
        'genesis_portal_engine': road / 'vendor_section04',
        'genesis_transform_engine': road / 'vendor_section04/vendor_section03',
        'vendor.genesis_geometric_engine': road / 'vendor_section04/vendor_section03',
        'vendor.genesis_chirality_machine': road / 'vendor_section04/vendor_section03',
    }
    for name, owner in checks.items():
        module = importlib.import_module(name)
        if not Path(module.__file__).resolve().is_relative_to(owner.resolve()):
            raise RuntimeError('RUNTIME_IMPORT_COLLISION: ' + name)
    return root, upstream, lock


def compile_paths(paths, base, name):
    from genesis_frontend.compiler import compile_sources
    # Logical names keep artifacts reproducible after extraction.
    return compile_sources([(Path(p).relative_to(base).as_posix(), Path(p).read_text(encoding='utf8')) for p in paths], name=name)


def execute(build, backend, budget=100000):
    from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import VM, decode
    if type(budget) is not int or not 0 < budget <= 100000:
        raise ValueError('BUDGET_EXCEEDED')
    return VM(backend).run(decode(build.link.bytecode), max_steps=budget)
