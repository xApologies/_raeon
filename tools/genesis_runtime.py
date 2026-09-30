"""Reproducible Genesis runtime commands. Generated evidence belongs under build/."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / 'data/platform/genesis-runtime-lock.json'
BUILD = ROOT / 'build/genesis_runtime'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf8')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dependency_root():
    return Path(os.environ.get('RAEON_GENESIS_UPSTREAM', ROOT / read_json(LOCK_PATH)['default_dependency_root'])).resolve()


def verify_dependencies():
    lock = read_json(LOCK_PATH)
    upstream = dependency_root()
    failures = []
    for relative, expected in lock['selected_source_paths_and_hashes'].items():
        source = (upstream / relative).resolve()
        if not source.is_relative_to(upstream):
            failures.append({'path': relative, 'reason': 'unsafe dependency path'})
            continue
        if not source.is_file():
            failures.append({'path': relative, 'reason': 'missing source'})
            continue
        content = source.read_bytes()
        if content.startswith(b'version https://git-lfs.github.com/spec/v1'):
            failures.append({'path': relative, 'reason': 'unresolved LFS pointer'})
        elif len(content) != expected['bytes'] or hashlib.sha256(content).hexdigest() != expected['sha256']:
            failures.append({'path': relative, 'reason': 'source digest mismatch'})
    result = {'upstream_commit': lock['upstream_commit'], 'checked': len(lock['selected_source_paths_and_hashes']), 'failures': failures}
    write_json(BUILD / 'evidence/dependencies.json', result)
    if failures:
        raise RuntimeError(json.dumps(result))
    return result


def isolated_command(label, args, cwd, pythonpath=None):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    env.pop('PYTHONPATH', None)
    if pythonpath:
        env['PYTHONPATH'] = str(pythonpath)
    result = subprocess.run([sys.executable, '-B', *args], cwd=cwd, env=env, capture_output=True, text=True, encoding='utf8', errors='replace')
    evidence = BUILD / 'evidence'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / (label + '.stdout.txt')).write_text(result.stdout, encoding='utf8')
    (evidence / (label + '.stderr.txt')).write_text(result.stderr, encoding='utf8')
    record = {'python': sys.version.split()[0], 'arguments': args, 'exit_code': result.returncode,
              'stdout_sha256': digest(evidence / (label + '.stdout.txt')), 'stderr_sha256': digest(evidence / (label + '.stderr.txt'))}
    write_json(evidence / (label + '.json'), record)
    print(f'{label}: exit {result.returncode}', flush=True)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError('Failed command: ' + label)
    return result


def baseline():
    verify_dependencies()
    upstream = dependency_root()
    implementation = upstream / 'language/10 Genesis Surface Language/12_REFERENCE_IMPLEMENTATION'
    example = 'language/10 Genesis Surface Language/16_EXAMPLES/RAINBOW_ROAD.gen'
    BUILD.mkdir(parents=True, exist_ok=True)
    for operation in ['parse', 'lower', 'build', 'run']:
        args = ['-m', 'genesis_frontend', operation, example]
        if operation == 'build':
            args += ['-o', str(BUILD / 'upstream-rainbow-road.gvm')]
        result = isolated_command('baseline-' + operation, args, upstream, implementation)
        readout = json.loads(result.stdout)
        write_json(BUILD / ('upstream-' + operation + '.json'), readout)
    receipt = read_json(BUILD / 'upstream-run.json')['execution']
    if receipt['payload'].get('verified') is not True:
        raise RuntimeError('Baseline did not produce a verified execution receipt')
    return {'status': 'PASS', 'execution_receipt': receipt['resource_id'],
            'artifacts': {p.name: digest(p) for p in sorted(BUILD.glob('upstream-*')) if p.is_file()}}


def upstream_test(domains):
    baseline_result = baseline()
    upstream = dependency_root()
    for number in domains:
        isolated_command(f'upstream-domain-{number}', ['language/tools/run_tests.py', '--domain', str(number)], upstream)
    result = {'status': 'PASS', 'upstream_commit': read_json(LOCK_PATH)['upstream_commit'], 'baseline': baseline_result, 'domains_passed': domains}
    write_json(BUILD / 'evidence/upstream-tests.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('doctor')
    dependencies = commands.add_parser('dependencies').add_subparsers(dest='dependency_command', required=True)
    dependencies.add_parser('verify')
    commands.add_parser('baseline')
    for action in ['build', 'verify', 'test', 'dialect-test', 'package', 'verify-distributions', 'repository-test', 'audit']:
        commands.add_parser(action)
    demo_parser = commands.add_parser('demo')
    demo_parser.add_argument('--headless', action='store_true', required=True)
    demo_parser.add_argument('--scenario', choices=['empty', 'cards'], default='empty')
    demo_parser.add_argument('--application', choices=['horizon-conformance', 'raeon'], default='horizon-conformance')
    tests = commands.add_parser('upstream-test')
    tests.add_argument('--domains', type=int, nargs='+', default=[1, 2, 3, 4, 5, 8, 9, 10, 13, 14, 15, 16, 17])
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError('Pinned reference runtime requires Python 3.12')
    if args.command == 'doctor':
        import numpy
        if numpy.__version__ != read_json(LOCK_PATH)['python']['numpy']:
            raise RuntimeError('NumPy version differs from lock')
        result = {'numpy': numpy.__version__, 'backend': 'raeon-native-bindings 1.0.0', 'python': sys.version, 'root': str(ROOT), 'upstream': str(dependency_root()),
                  'dependency_verification': verify_dependencies(), 'implementation_status': read_json(LOCK_PATH)['status']}
    elif args.command == 'dependencies':
        result = verify_dependencies()
    elif args.command == 'baseline':
        result = baseline()
    elif args.command == 'upstream-test':
        result = upstream_test(args.domains)
    else:
        import genesis_runtime_tasks as tasks
        import genesis_runtime_distribution as distribution
        import genesis_runtime_acceptance as acceptance
        import genesis_runtime_pass01 as pass01
        import genesis_runtime_pass02 as pass02
        if args.command == 'repository-test':
            result = acceptance.repository_test(ROOT, BUILD)
        elif args.command == 'audit':
            result = acceptance.audit(ROOT, BUILD)
            result['pass_02'] = pass02.audit(ROOT, BUILD)
            import genesis_runtime_projection_correction as correction
            result['projection_correction'] = correction.audit(ROOT, BUILD)
            if any(result[key]['status'] != 'PASS' for key in ['pass_02', 'projection_correction']) or result['status'] != 'PASS':
                print(json.dumps(result, indent=2))
                raise RuntimeError('Audit incomplete; inspect named failing acceptance evidence')
        elif args.command == 'package':
            result = distribution.package(ROOT, BUILD)
        elif args.command == 'verify-distributions':
            result = distribution.verify_distributions(ROOT, BUILD)
        elif args.command == 'test':
            (BUILD / 'evidence/tests-source.json').unlink(missing_ok=True)
            result = tasks.test(ROOT, BUILD)
            result['upstream'] = upstream_test([1,2,3,4,5,8,9,10,13,14,15,16,17])
            write_json(BUILD / 'evidence/tests-source.json', {'status': 'PASS', 'implementation_sha256': distribution.implementation_digest(ROOT)})
        elif args.command == 'demo' and args.application == 'raeon':
            result = pass02.demo(ROOT, BUILD, args.scenario)
            if args.scenario == 'empty':
                result['historical_pass_01'] = pass01.demo(ROOT, BUILD)
        elif args.command == 'dialect-test':
            result = tasks.dialect_test(ROOT, dependency_root(), BUILD)
        else:
            result = getattr(tasks, args.command)(ROOT, BUILD)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
