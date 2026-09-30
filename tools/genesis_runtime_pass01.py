"""Pass-1 production demonstration and evidence joined by the canonical runner."""
import json
from pathlib import Path
import subprocess
import sys

from genesis_runtime_distribution import implementation_digest
from genesis_runtime_tasks import setup, write

START = '71b3a3fbdbce7eece25076a0fd303887cc70d4f1'
MAIN = '69a0030805b8c3858c877a514e2f50644421115a'
RECEIPT = 'development/modules/core-game/PASS_01_RECEIPT'
GROUPS = {
    'test_production_manifest_and_real_genesis': [1, 2],
    'test_production_bytecode_is_deterministic': [3],
    'test_exact_topology_and_empty_containers': [4, 5, 6, 8, 9, 10, 11],
    'test_explicit_relations_and_stable_unique_identity': [7, 12, 13],
    'test_owner_opponent_privacy_and_no_native_leak': [14, 15, 16],
    'test_observation_and_idempotence_do_not_duplicate': [17, 18],
    'test_conflicting_application_rejected': [19],
    'test_unauthorized_realization_rejected': [20],
    'test_package_and_source_hash_tamper_rejected': [21, 22],
    'test_path_escape_rejected': [23],
    'test_undeclared_and_malformed_source_rejected': [24],
    'test_duplicate_and_conflicting_identity_rejected': [25],
    'test_prepublication_failure_and_budget_roll_back': [26],
    'test_application_cannot_inherit_or_mutate_machine_domains': [27],
    'test_checkpoint_restart_and_two_player_sessions': [28, 29, 30],
    'test_no_pass_two_rules_exposed': [36],
}


def demo(root, output):
    setup(root)
    sys.path.insert(0, str(root / 'tests/integration/genesis_horizon'))
    from pass_01_support import ProductionFixture
    f = ProductionFixture()
    try:
        f.connect()
        views = {p: f.hello(p).view for p in f.players}
        objects = views['player_1']['objects']
        counts = {kind: sum(o['kind'] == kind for o in objects.values()) for kind in sorted({o['kind'] for o in objects.values()})}
        native = f.horizon._backend
        proof = {'instantiations': [r for r in native.native_receipts if r['operation'] == 'instantiate'],
                 'road_receipts': native.road_history}
        restart = f.restart()
        for authority in f.players.values():
            f.horizon.observe(authority)
        assert f.horizon._state['revision'] == restart['revision'] == 0
        assert f.horizon._state['root'] == restart['root']
        result = {'status': 'PASS', 'implementation_sha256': implementation_digest(root),
                  'package': f.package, 'native_object_count': len(objects), 'counts': counts,
                  'explicit_application_relations': len(f.realization['manifest']['realization_relations']),
                  'views': views, 'restart': restart, 'native_proof': proof,
                  'observation_preserves_revision': True, 'whole_game_phase': 'PREPRODUCTION'}
        write(output / 'evidence/pass-01-demo.json', result)
        return {k: v for k, v in result.items() if k not in ('views', 'native_proof')}
    finally:
        f.close()


def audit(root, output):
    evidence = output / 'evidence'
    def read(name):
        p = evidence / name
        return json.loads(p.read_text(encoding='utf8')) if p.is_file() else {}
    specification = json.loads((root / 'tests/integration/genesis_horizon/cases/pass_01_acceptance.json').read_text(encoding='utf8'))
    cases = {case['id']: dict(case, evidence=[]) for case in specification['cases']}
    def mark(numbers, condition, sources):
        for number in numbers:
            cases[f'P1-{number:02}'].update(status='PASS' if condition else 'FAIL', evidence=sources)
    implementation = implementation_digest(root)
    tests = read('tests-integration.json')
    current = read('tests-source.json') == {'status': 'PASS', 'implementation_sha256': implementation}
    passed = tests.get('passed', []) if not tests.get('errors', 1) and not tests.get('failures', 1) else []
    for method, ids in GROUPS.items():
        mark(ids, current and 'test_pass_01.Pass01Tests.' + method in passed, [method, 'tests-integration.json', 'tests-source.json'])
    mark([16], cases['P1-16']['status'] == 'PASS' and 'test_pass_01.Pass01Tests.test_observation_operation_receipt_has_no_native_diagnostics' in passed,
         ['test_owner_opponent_privacy_and_no_native_leak', 'test_observation_operation_receipt_has_no_native_diagnostics', 'tests-integration.json'])
    demo_result = read('pass-01-demo.json')
    mark([31], demo_result.get('status') == 'PASS' and demo_result.get('implementation_sha256') == implementation, ['pass-01-demo.json'])
    runtime = read('acceptance.json')
    mark([32], current and runtime.get('status') == 'PASS', ['acceptance.json', 'tests-unit.json', 'tests-integration.json'])
    repository = read('repository-validation.json')
    repository_ok = repository.get('status') == 'PASS' and repository.get('implementation_sha256') == implementation
    mark([33, 34], repository_ok, ['repository-validation.json', 'repository-command-4.log', 'repository-command-7.log', 'repository-command-8.log'])
    mark([35], read('upstream-readonly.json').get('status') == 'PASS', ['upstream-readonly.json', 'dependencies.json'])
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
    head, branch = git('rev-parse', 'HEAD'), git('branch', '--show-current')
    remote = git('ls-remote', 'origin', 'refs/heads/' + branch).split()
    main = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
    clean = not git('status', '--porcelain')
    ancestry = subprocess.run(['git', 'merge-base', '--is-ancestor', START, 'HEAD'], cwd=root).returncode == 0
    not_merged = subprocess.run(['git', 'merge-base', '--is-ancestor', 'HEAD', 'origin/main'], cwd=root).returncode == 1
    changed = git('diff', '--name-only', START, 'HEAD').splitlines()
    preserved = not any(p.startswith(('data/cycles/', 'data/qmo/', 'mathematics/', 'design/')) for p in changed)
    mark([36], cases['P1-36']['status'] == 'PASS' and preserved,
         ['test_no_pass_two_rules_exposed', 'Git changed-path comparison against starting milestone'])
    receipts = all((root / (RECEIPT + suffix)).is_file() for suffix in ['.md', '.json'])
    if receipts:
        maintained = json.loads((root / (RECEIPT + '.json')).read_text(encoding='utf8'))
        receipts = maintained.get('status') == 'COMPLETE' and maintained.get('starting_sha') == START and maintained.get('branch') == branch
    mark([37], receipts and current and repository_ok, [RECEIPT + '.md', RECEIPT + '.json', 'pass-01-acceptance.json'])
    mark([38], branch == 'codex/raeon-pass-01' and bool(remote and remote[0] == head) and clean and main == MAIN and ancestry and not_merged,
         ['Git local/remote comparison', 'starting milestone ancestry', 'unchanged remote main'])
    result = {'schema_version': 1, 'status': 'PASS' if all(c['status'] == 'PASS' for c in cases.values()) else 'INCOMPLETE',
              'passed': sum(c['status'] == 'PASS' for c in cases.values()), 'total': len(cases),
              'branch': branch, 'starting_sha': START, 'ending_sha': head, 'remote_sha': remote[0] if remote else None,
              'main_starting_sha': MAIN, 'main_ending_sha': main, 'main_unmerged': not_merged, 'clean': clean,
              'implementation_sha256': implementation, 'cases': list(cases.values())}
    write(evidence / 'pass-01-acceptance.json', result)
    return result
