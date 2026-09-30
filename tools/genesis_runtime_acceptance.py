"""Join independent requirements to actual test/build/delivery evidence."""
import json
from pathlib import Path
import subprocess

from genesis_runtime_distribution import implementation_digest
from genesis_runtime_tasks import write

GROUPS = {
    'test_native_boot_identities_and_containment': ['H-01', 'H-04', 'H-05', 'H-06', 'H-07', 'H-08', 'H-09'],
    'test_missing_and_tampered_sources': ['H-02', 'H-03', 'H-10'],
    'test_real_joint_trace_and_identity_history': ['H-11', 'H-12', 'H-13', 'H-15', 'H-16', 'R-01', 'R-02', 'R-04', 'R-08', 'V-12', 'S-01', 'S-02'],
    'test_candidate_rollback_and_budget': ['H-14', 'L-01'],
    'test_route_admission_and_open_resource_rejections': ['R-03', 'R-05', 'R-06', 'R-07'],
    'test_retry_conflict_concurrent_scope_and_stale': ['S-04', 'S-05', 'S-06', 'S-07', 'S-08'],
    'test_expired_retry_is_never_reexecuted': ['S-11'],
    'test_privacy_and_scope': ['V-10', 'V-11', 'V-13'],
    'test_output_delivery_failure_retains_committed_outcome': ['S-10'],
    'test_projection_gap_receipt_clock_and_reconnect': ['S-03', 'S-09', 'S-12'],
    'test_backpressure_before_mutation': ['V-14', 'V-15'],
    'test_checkpoint_restart_corruption_and_confinement': ['L-04', 'L-05', 'L-07', 'L-08'],
    'test_quiesce_close_and_replay': ['L-02', 'L-03', 'L-06', 'D-01'],
    'test_independent_vector': ['V-01'],
    'test_versions_direction_and_lengths': ['V-02', 'V-03', 'V-04', 'V-08'],
    'test_json_unicode_duplicates_constants': ['V-05'],
    'test_numeric_and_shape_validation_on_both_paths': ['V-06', 'V-07'],
    'test_fragment_assembly_and_unbound_scope': ['V-09'],
}


def repository_test(root, output):
    import glob
    commands = [['node', 'tools/validators/validate-' + name + '.mjs'] for name in
                ['bootstrap', 'design-state', 'normalization', 'continuity', 'cycle1-import', 'full-migration', 'game-definition']]
    commands += [['node', '--test', *sorted(glob.glob('tests/regression/*.test.mjs', root_dir=root))],
                 ['node', '--test', *sorted(p for folder in ['cards', 'primes', 'sandbox', 'manifolds']
                                         for p in glob.glob('tests/gameplay/' + folder + '/*.test.mjs', root_dir=root))],
                 ['git', 'diff', '--check']]
    results = []
    for index, command in enumerate(commands):
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding='utf8', errors='replace')
        (output / 'evidence' / ('repository-command-' + str(index) + '.log')).write_text(result.stdout + result.stderr, encoding='utf8')
        results.append({'command': command, 'exit_code': result.returncode})
        print('repository check ' + str(index) + ': exit ' + str(result.returncode), flush=True)
    receipt = {'status': 'PASS' if all(r['exit_code'] == 0 for r in results) else 'FAIL',
               'implementation_sha256': implementation_digest(root), 'results': results}
    write(output / 'evidence/repository-validation.json', receipt)
    if receipt['status'] != 'PASS':
        raise RuntimeError('Repository validation failure; inspect recorded command logs')
    return receipt


def audit(root, output):
    specification = json.loads((root / 'tests/integration/genesis_horizon/cases/acceptance.json').read_text(encoding='utf8'))
    cases = {case['id']: {'id': case['id'], 'title': case['title'], 'status': 'NOT_RUN', 'evidence': []} for case in specification['cases']}
    evidence = output / 'evidence'

    def read(name):
        p = evidence / name
        return json.loads(p.read_text(encoding='utf8')) if p.is_file() else None

    def mark(ids, ok, records):
        for case in ids:
            cases[case]['status'] = 'PASS' if ok else 'FAIL'
            cases[case]['evidence'] = records

    passed = set()
    for name in ['tests-unit.json', 'tests-integration.json']:
        record = read(name)
        if record and not record['failures'] and not record['errors']:
            passed.update(record['passed'])
    source_test = read('tests-source.json')
    tests_current = source_test == {'status': 'PASS', 'implementation_sha256': implementation_digest(root)}
    for method, ids in GROUPS.items():
        mark(ids, tests_current and any(test.endswith('.' + method) for test in passed), [method, 'tests-source.json'])
    dependencies = read('dependencies.json')
    mark(['SRC-02'], bool(dependencies and not dependencies['failures']), ['dependencies.json'])
    mark(['SRC-03'], bool(read('baseline-run.json') and read('baseline-run.json')['exit_code'] == 0), ['baseline-parse.json', 'baseline-lower.json', 'baseline-build.json', 'baseline-run.json'])
    mark(['SRC-04'], bool(read('dialects.json') and read('dialects.json')['status'] == 'PASS'), ['dialects.json'])
    mark(['SRC-05'], bool(read('upstream-tests.json') and read('upstream-tests.json')['status'] == 'PASS'), ['upstream-tests.json'])
    start = '711ad7485c8cd58a87ec03ff59d6daf8b6498487'
    ancestry = subprocess.run(['git', 'merge-base', '--is-ancestor', start, 'HEAD'], cwd=root, capture_output=True).returncode == 0
    mark(['SRC-01'], ancestry, ['Git starting commit remains ancestor', 'GENESIS_RUNTIME_EXECUTION.md'])
    original = root.parent / '_bricked'
    upstream_head = subprocess.check_output(['git', '-C', str(original), 'rev-parse', 'HEAD'], text=True).strip()
    upstream_status = subprocess.check_output(['git', '-C', str(original), 'status', '--porcelain'], text=True).strip()
    lock = json.loads((root / 'data/platform/genesis-runtime-lock.json').read_text(encoding='utf8'))
    untouched = upstream_head == lock['upstream_commit'] and not upstream_status
    write(evidence / 'upstream-readonly.json', {'status': 'PASS' if untouched else 'FAIL', 'head': upstream_head, 'git_status': upstream_status,
                                             'comparison': 'Initial clean tracked source at pinned HEAD versus final clean tracked source at identical HEAD; runtime executed only in ignored copy'})
    mark(['SRC-06'], untouched, ['upstream-readonly.json'])
    repository = read('repository-validation.json')
    mark(['D-02'], bool(repository and repository['status'] == 'PASS' and repository['implementation_sha256'] == implementation_digest(root)), ['repository-validation.json'])
    distributions = read('distributions.json')
    verified = read('distribution-verification.json')
    if distributions:
        mark(['D-03'], len(distributions) == 2, ['distributions.json'])
    if verified:
        okay = verified['status'] == 'PASS' and all(c['exit_code'] == 0 for c in verified['commands'])
        mark(['D-04', 'D-05', 'D-06', 'V-16'], okay, ['distribution-verification.json'])
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=root, text=True).strip()
    remote = subprocess.check_output(['git', 'ls-remote', 'origin', 'refs/heads/' + branch], cwd=root, text=True).split()
    clean = not subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True).strip()
    remote_matches = bool(remote and remote[0] == head and clean)
    write(evidence / 'remote.json', {'branch': branch, 'local': head, 'remote': remote[0] if remote else None, 'clean': clean})
    mark(['D-07'], remote_matches, ['remote.json'])
    accepted = json.loads((root / 'data/manifests/accepted-state.json').read_text(encoding='utf8'))
    mark(['D-08'], accepted['production']['phase'] == 'PREPRODUCTION' and verified is not None,
         ['accepted-state.json', 'distribution labels: host reference / native-device NOT_RUN', 'GENESIS_RUNTIME_EXECUTION.md'])
    result = {'status': 'PASS' if all(c['status'] == 'PASS' for c in cases.values()) else 'INCOMPLETE',
              'passed': sum(c['status'] == 'PASS' for c in cases.values()), 'total': len(cases),
              'source_revision': head, 'cases': list(cases.values())}
    write(evidence / 'acceptance.json', result)
    return result
