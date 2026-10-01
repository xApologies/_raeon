"""Exact private handoff archives and offline installation from fresh extraction."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

VERSION = '0.3.0'
PREFIXES = {
    'hypervisor': ['platform/shared/python_hypervisor/', 'tests/unit/hypervisor/'],
    'horizon': ['game/qmo/', 'game/sandbox/', 'data/qmo/', 'data/render_specs/cycle_01/',
                'tools/genesis_runtime_pass03.py', 'provenance/decisions/raeon-pass-03.json',
                'provenance/imports/raeon-pass-03/handoff/acceptance/PASS_03_ACCEPTANCE.json',
                'provenance/imports/raeon-pass-03/entry.json',
                'development/modules/core-game/PASS_03_POLICY_GATES.json',
                'development/modules/core-game/PASS_03_EXECUTION.md', 'development/modules/core-game/PASS_03_RECEIPT.md', 'tools/genesis_runtime_projection_correction.py',
                'provenance/decisions/raeon-pass-02-projection-correction.json',
                'development/modules/core-game/PASS_02_PROJECTION_CORRECTION.md', 'tools/genesis_runtime_pass02.py', 'tools/genesis_runtime_catalog.py', 'tools/genesis_runtime_isolation.py',
                'data/cycles/cycle_01/', 'data/game/', 'provenance/decisions/raeon-pass-02.json',
                'provenance/decisions/raeon-pass-02.md', 'development/modules/core-game/PASS_02_POLICY_GATES.json',
                'development/modules/core-game/PASS_02_EXECUTION.md', 'development/modules/core-game/PASS_02_RECEIPT.md',
                'game/core/genesis_horizon/', 'game/core/raeon/', 'tools/genesis_runtime_pass01.py',
                'provenance/decisions/raeon-pass-01.json', 'data/manifests/current-files.json', 'tests/integration/genesis_horizon/',
                'data/platform/genesis-runtime-lock.json', 'data/platform/genesis-horizon-profile.json',
                'tools/genesis_runtime.py', 'tools/genesis_runtime_tasks.py', 'tools/genesis_runtime_distribution.py', 'tools/genesis_runtime_acceptance.py',
                'development/modules/core-game/GENESIS_RUNTIME_EXECUTION.md',
                'development/modules/core-game/PASS_01_BUILD_ORDER.md',
                'development/modules/core-game/PASS_01_RECEIPT.md', 'provenance/decisions/raeon-pass-01.md',
                'development/modules/core-game/GENESIS_RUNTIME_BUILD_ORDER.md',
                'provenance/decisions/genesis-runtime-build.json', 'provenance/decisions/genesis-runtime-build.md'],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode('utf8')


def maintained(root):
    inventory = json.loads((root / 'data/manifests/current-files.json').read_text(encoding='utf8'))['files']
    return {family: sorted(p for p in inventory if any(p == prefix or p.startswith(prefix) for prefix in prefixes))
            for family, prefixes in PREFIXES.items()}


def implementation_digest(root):
    # Tests bind all executable source and authority inputs, not commentary timestamps.
    candidates = []
    for family in maintained(root).values():
        candidates.extend(p for p in family if not p.endswith('.md'))
    return sha(json_bytes({p: sha((root / p).read_bytes()) for p in sorted(set(candidates))}))


def package(root, output):
    from genesis_runtime_tasks import verify
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True).strip():
        raise RuntimeError('Packaging requires one clean committed source revision')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    lock = json.loads((root / 'data/platform/genesis-runtime-lock.json').read_text(encoding='utf8'))
    verify(root, output)
    receipt = json.loads((output / 'evidence/tests-source.json').read_text(encoding='utf8'))
    if receipt != {'status': 'PASS', 'implementation_sha256': implementation_digest(root)}:
        raise RuntimeError('Required tests are stale or failed')
    for test_file in ['tests-unit.json', 'tests-integration.json']:
        tests = json.loads((output / 'evidence' / test_file).read_text(encoding='utf8'))
        if tests['errors'] or tests['failures'] or not tests['run']:
            raise RuntimeError('Required local test failure: ' + test_file)
    upstream_receipt = json.loads((output / 'evidence/upstream-tests.json').read_text(encoding='utf8'))
    if upstream_receipt['status'] != 'PASS' or upstream_receipt['upstream_commit'] != lock['upstream_commit']:
        raise RuntimeError('Upstream regression evidence missing')
    upstream = Path(os.environ.get('RAEON_GENESIS_UPSTREAM', root / lock['default_dependency_root'])).resolve()
    distributions = output / 'distributions'
    distributions.mkdir(parents=True, exist_ok=True)
    result = {}
    for family, files in maintained(root).items():
        entries = {p: (root / p).read_bytes() for p in files}
        if family == 'horizon':
            # Ship exactly the verified runtime subset, not the giant research repository.
            for relative, expected in lock['selected_source_paths_and_hashes'].items():
                payload = (upstream / relative).read_bytes()
                if sha(payload) != expected['sha256']:
                    raise RuntimeError('Dependency drift while packaging: ' + relative)
                entries[lock['default_dependency_root'] + '/' + relative] = payload
            entries['distribution/UPSTREAM_NOTICE.txt'] = (
                'Private development handoff to the repository owner.\n'
                'Upstream: ' + lock['upstream_repository'] + '\nCommit: ' + lock['upstream_commit'] + '\n'
                'No upstream LICENSE, COPYING or NOTICE file was found in the pinned Git tree.\n'
                'No public redistribution license is inferred or granted by this archive.\n'
                'NumPy and setuptools wheels retain their own embedded license notices.\n').encode()
            wheels = list((output / 'wheels').glob('*.whl'))
            expected_wheels = lock['python']['wheels']
            if {p.name for p in wheels} != set(expected_wheels):
                raise RuntimeError('Exact offline dependency wheels are missing')
            for wheel in wheels:
                payload = wheel.read_bytes()
                if sha(payload) != expected_wheels[wheel.name]:
                    raise RuntimeError('Offline wheel integrity: ' + wheel.name)
                entries['distribution/wheels/' + wheel.name] = payload
            compiled = json.loads((output / 'evidence/build.json').read_text())['artifacts']
            for record in compiled.values():
                for name, expected in record['artifact_hashes'].items():
                    artifact = output / 'compiled' / record['artifact_directory'] / name
                    if sha(artifact.read_bytes()) != expected:
                        raise RuntimeError('Compiled artifact integrity: ' + str(artifact))
                    entries['build/genesis_runtime/compiled/' + artifact.relative_to(output / 'compiled').as_posix()] = artifact.read_bytes()
            for name in ['build.json', 'verify.json', 'tests-unit.json', 'tests-integration.json', 'tests-source.json', 'upstream-tests.json', 'dialects.json']:
                entries['distribution/evidence/' + name] = (output / 'evidence' / name).read_bytes()
        else:
            entries['distribution/hypervisor-test-receipt.json'] = (output / 'evidence/tests-unit.json').read_bytes()
        entries['distribution/' + family + '-source.json'] = json_bytes({
            'source_commit': revision, 'version': VERSION, 'whole_game_phase': 'PREPRODUCTION',
            'runtime_scope': 'host reference', 'native_device_tests': 'NOT_RUN',
            'offline_policy': 'Both archives together include runtime sources and Windows x64 CPython 3.12 wheels. Python itself is an explicit prerequisite.',
            'python': '3.12', 'numpy': '2.3.5', 'setuptools': '84.0.0',
            'supported_distribution_host': 'Windows x64, CPython 3.12; native/mobile ports not shipped',
        })
        if any('__pycache__' in p or p.endswith(('.pyc', '.pyo')) for p in entries):
            raise RuntimeError('Cache in archive')
        manifest_path = 'distribution/' + family + '-manifest.json'
        entries[manifest_path] = json_bytes({'schema_version': 1, 'source_commit': revision,
                                           'files': {p: {'sha256': sha(data), 'bytes': len(data)} for p, data in sorted(entries.items())}})
        name = ('raeon-python-hypervisor-' if family == 'hypervisor' else 'genesis-horizon-') + VERSION + '.zip'
        target = distributions / name
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path, payload in sorted(entries.items()):
                item = zipfile.ZipInfo(path, (2026, 9, 30, 0, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o644 << 16
                archive.writestr(item, payload)
        digest = sha(target.read_bytes())
        target.with_suffix('.zip.sha256').write_text(digest + '  ' + name + '\n', encoding='utf8', newline='\n')
        result[family] = {'implementation_sha256': implementation_digest(root), 'path': str(target), 'sha256': digest, 'bytes': target.stat().st_size, 'source_commit': revision,
                          'manifest': manifest_path, 'files': len(entries)}
    (output / 'evidence/distributions.json').write_bytes(json_bytes(result))
    return result


def check_archive(path, manifest_name):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError('Duplicate ZIP members')
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or '__pycache__' in name or name.endswith(('.pyc', '.pyo')):
                raise RuntimeError('Unsafe archive member: ' + name)
        manifest = json.loads(archive.read(manifest_name))
        if set(names) - {manifest_name} != set(manifest['files']):
            raise RuntimeError('Manifest inventory mismatch')
        for name, expected in manifest['files'].items():
            payload = archive.read(name)
            if len(payload) != expected['bytes'] or sha(payload) != expected['sha256']:
                raise RuntimeError('Manifest content mismatch: ' + name)
        return manifest


def verify_distributions(root, output):
    distributions = json.loads((output / 'evidence/distributions.json').read_text(encoding='utf8'))
    extraction = Path(tempfile.mkdtemp(prefix='RAEON clean extraction ')).resolve()
    extracted = set()
    manifests = {}
    for family, record in distributions.items():
        path = Path(record['path'])
        if sha(path.read_bytes()) != record['sha256']:
            raise RuntimeError('Archive hash mismatch')
        manifests[family] = check_archive(path, record['manifest'])
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                target = (extraction / member.filename).resolve()
                if not target.is_relative_to(extraction) or member.filename in extracted:
                    raise RuntimeError('Extraction collision or path escape')
                extracted.add(member.filename)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(member))
    if len({m['source_commit'] for m in manifests.values()}) != 1:
        raise RuntimeError('Archives have different source revisions')
    commands = []
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', PIP_NO_INDEX='1', PIP_DISABLE_PIP_VERSION_CHECK='1', RAEON_HYPERVISOR_USE_INSTALLED='1')
    for name in ['PYTHONPATH', 'RAEON_GENESIS_UPSTREAM', 'PYTHONHOME']:
        env.pop(name, None)

    def run(label, command, expected_exit=0):
        result = subprocess.run(command, cwd=extraction, env=env, capture_output=True, text=True, encoding='utf8', errors='replace')
        logs = output / 'evidence'
        (logs / ('distribution-' + label + '.log')).write_text(result.stdout + result.stderr, encoding='utf8', newline='\n')
        commands.append({'label': label, 'exit_code': 0 if result.returncode == expected_exit else result.returncode or -1,
                         'process_exit_code': result.returncode, 'expected_exit_code': expected_exit, 'arguments': command})
        print('clean extraction ' + label + ': exit ' + str(result.returncode), flush=True)
        if result.returncode != expected_exit:
            raise RuntimeError(label + ': ' + result.stdout + result.stderr)
        return result
    run('venv', [sys.executable, '-B', '-m', 'venv', str(extraction / 'isolated python')])
    python = extraction / 'isolated python/Scripts/python.exe'
    # Every venv child loads this hook, even children that clear PYTHONPATH or
    # use isolated mode. The original checkout is never renamed or modified.
    site = extraction / 'isolated python/Lib/site-packages'
    (site / 'sitecustomize.py').write_text(
        'import sys,os\nfrom pathlib import Path\n'
        'sys.path.insert(0,str(Path(os.environ["RAEON_ISOLATION_ROOT"])/"tools"))\n'
        'import genesis_runtime_isolation;genesis_runtime_isolation.install()\n', encoding='utf8')
    env['RAEON_ISOLATION_ROOT'] = str(extraction)
    env['RAEON_FORBIDDEN_CHECKOUT'] = str(root.parent / '_bricked')
    temp = extraction / 'temporary files'
    temp.mkdir()
    env.update(TEMP=str(temp), TMP=str(temp), PIP_CONFIG_FILE=os.devnull, PIP_NO_CACHE_DIR='1', PYTHONNOUSERSITE='1')
    run('isolation-probes', [str(python), '-B', '-c', 'import genesis_runtime_isolation;genesis_runtime_isolation.probes()'])
    wheels = extraction / 'distribution/wheels'
    run('dependencies', [str(python), '-B', '-m', 'pip', 'install', '--no-index', '--find-links', str(wheels), 'numpy==2.3.5', 'setuptools==84.0.0'])
    run('install', [str(python), '-B', '-m', 'pip', 'install', '--no-index', '--no-build-isolation', str(extraction / 'platform/shared/python_hypervisor')])
    run('installed-import', [str(python), '-B', '-c', "import raeon_hypervisor,numpy;from pathlib import Path;assert 'site-packages' in str(Path(raeon_hypervisor.__file__));assert numpy.__version__=='2.3.5';print(raeon_hypervisor.__file__)"])
    run('doctor', [str(python), '-B', 'tools/genesis_runtime.py', 'doctor'])
    run('build', [str(python), '-B', 'tools/genesis_runtime.py', 'verify'])
    run('demo', [str(python), '-B', 'tools/genesis_runtime.py', 'demo', '--headless'])
    run('pass-01-demo', [str(python), '-B', 'tools/genesis_runtime.py', 'demo', '--headless', '--application', 'raeon'])
    run('pass-02-demo', [str(python), '-B', 'tools/genesis_runtime.py', 'demo', '--headless', '--application', 'raeon', '--scenario', 'cards'])
    # Exercise local software tests in isolation; the selected upstream regression
    # sources are also shipped and remain runnable with the test command.
    run('pass-03-demo', [str(python), '-B', 'tools/genesis_runtime.py', 'demo', '--headless', '--application', 'raeon', '--scenario', 'topology'])
    run('unit-tests', [str(python), '-B', '-m', 'unittest', 'discover', '-s', 'tests/unit/hypervisor', '-v'])
    run('integration-tests', [str(python), '-B', '-m', 'unittest', 'discover', '-s', 'tests/integration/genesis_horizon', '-v'])
    lock = json.loads((extraction / 'data/platform/genesis-runtime-lock.json').read_text())
    relative = next(iter(lock['selected_source_paths_and_hashes']))
    missing = extraction / lock['default_dependency_root'] / relative
    held = missing.with_name(missing.name + '.held-for-negative-test')
    missing.rename(held)
    try:
        negative = run('missing-dependency', [str(python), '-B', 'tools/genesis_runtime.py', 'doctor'], expected_exit=1)
        if 'missing source' not in negative.stderr and 'DEPENDENCY_INTEGRITY' not in negative.stderr:
            raise RuntimeError('Missing source failed for an unrelated reason')
    finally:
        held.rename(missing)
    missing = extraction / 'data/qmo/cycle1/manifold_pair_relations.json'
    held = missing.with_name(missing.name + '.held-for-negative-test')
    missing.rename(held)
    try:
        negative = run('missing-qmo', [str(python), '-B', 'tools/genesis_runtime.py', 'demo', '--headless', '--application', 'raeon', '--scenario', 'topology'], expected_exit=1)
        if 'manifold_pair_relations.json' not in negative.stderr and 'QMO_CORPUS_INTEGRITY' not in negative.stderr:
            raise RuntimeError('Missing QMO failed for an unrelated reason')
    finally:
        held.rename(missing)
    original_build = json.loads((output / 'evidence/build.json').read_text())
    relocated_build = json.loads((extraction / 'build/genesis_runtime/evidence/build.json').read_text())
    if original_build != relocated_build:
        raise RuntimeError('Bytecode changed after offline relocation')
    traces = [json.loads(line) for path in (extraction / 'isolation traces').glob('*.jsonl') for line in path.read_text().splitlines()]
    violations = [event for event in traces if event['denied'] and not event['probe']]
    if violations:
        raise RuntimeError('Offline isolation violations: ' + str(violations[:10]))
    isolation = {'method': 'independent Python audit interception in every fresh-venv child; denial probes executed',
                 'scope': 'trusted pinned Python reference engines; not an OS sandbox for arbitrary native code',
                 'probes_passed': True, 'violations': violations, 'events_recorded': len(traces),
                 'trace_directory': str(extraction / 'isolation traces'),
                 'file_closure': ['bundle and writable extraction', 'declared Python installation', 'Windows OS prerequisite']}
    result = {'status': 'PASS', 'isolation': isolation, 'missing_dependency_negative': 'PASS', 'missing_qmo_negative': 'PASS',
              'physical_path_bytecode_equal': True, 'extraction': str(extraction), 'offline_install': True, 'python_prerequisite': sys.version.split()[0],
              'source_commit': next(iter(manifests.values()))['source_commit'], 'commands': commands,
              'archives': distributions, 'archive_manifest_files_verified': sum(len(m['files']) for m in manifests.values())}
    (output / 'evidence/distribution-verification.json').write_bytes(json_bytes(result))
    return result
