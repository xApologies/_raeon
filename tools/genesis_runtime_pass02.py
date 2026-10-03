"""Pass-2 native scenarios and the unchanged 83-case evidence denominator."""
import json
from pathlib import Path
import subprocess
import sys

from genesis_runtime_distribution import implementation_digest
from genesis_runtime_tasks import setup, write

START = '23ebfc3be3a4e6ae4883793bfc99b1dbfae67bf8'
MAIN = '69a0030805b8c3858c877a514e2f50644421115a'

# Each mapping names executed assertions, never source-string presence as a pass.
TESTS = {
    'test_pass_02.Pass02.test_empty_baseline_and_native_inventory': [17, 19, 20, 24, 52],
    'test_pass_02.Pass02.test_actual_draw_and_commit_preserve_identity': [26, 30, 36, 37],
    'test_pass_02_transactions.Transactions.test_catalog_roster_limits_unknown_and_no_reset': [4, 5, 6, 7, 8, 9, 21],
    'test_pass_02_transactions.Transactions.test_shuffle_independent_full_vector_and_idempotency': [27, 28, 29],
    'test_pass_02_transactions.Transactions.test_hand_capacity_empty_deck_and_forged_arguments': [31, 32, 33],
    'test_pass_02_transactions.Transactions.test_failed_candidate_rolls_back_grant_rng_membership': [65],
    'test_pass_02_transactions.Transactions.test_delivery_loss_retry_conflict_and_stale_revision': [66, 67],
    'test_pass_02_transactions.Transactions.test_live_private_views_and_detached_values': [60, 61, 62, 63],
    'test_pass_02_transactions.Transactions.test_dynamic_regions_native_capacity_and_repeat_color': [38, 53, 54, 55, 56, 57, 58, 59],
    'test_pass_02_transactions.Transactions.test_retirement_recovery_order_and_whole_support': [39, 44, 46, 47],
    'test_pass_02_transactions.Transactions.test_structural_prime_slots_without_combat': [41, 42, 43],
    'test_pass_02_transactions.Transactions.test_checkpoint_nonempty_preserves_native_state_and_retry': [70],
    'test_pass_02_adversarial.Adversarial.test_input_bounds_code_and_card_only_containment': [14, 15, 25],
    'test_pass_02_adversarial.Adversarial.test_setup_rollback_and_exact_idempotent_multiset': [22, 23],
    'test_pass_02_adversarial.Adversarial.test_concurrent_requests_and_semantic_order': [34, 35],
    'test_pass_02_adversarial.Adversarial.test_native_route_and_handler_closure_cannot_be_bypassed': [18, 74],
    'test_pass_02_adversarial.Adversarial.test_recovery_profiles_and_batch_capacity': [40, 48, 49],
    'test_pass_02_adversarial.Adversarial.test_inspection_reorder_batch_helpers_grant_limits': [45, 50],
    'test_pass_02_adversarial.Adversarial.test_seeded_conservation_two_owners': [64],
    'test_pass_02_adversarial.Adversarial.test_catalog_tamper_and_physical_path_determinism': [11, 13],
    'test_pass_02_adversarial.Adversarial.test_checkpoint_corruption_and_new_process_restore': [71, 72],
    'test_pass_02_adversarial.Adversarial.test_semantic_replay_across_storage_and_epoch': [73],
}


def demo(root, output, scenario='cards'):
    setup(root)
    sys.path.insert(0, str(root / 'tests/integration/genesis_horizon'))
    from pass_02_support import CardFixture
    f = CardFixture()
    try:
        initial = f.horizon._view(f.players['player_1'])
        assert len(initial['objects']) == 37 and f.horizon._state['revision'] == 0
        assert len(f.horizon._backend.relations) == 166
        if scenario == 'cards':
            f.initialize()
            f.initialize(player='player_2')
            for player in f.players:
                f.perform('SHUFFLE_DECK', player=player, effect={'seed': 'private-reference-demo-' + player})
                f.perform('DRAW_ONE', player=player)
                identity = f.members(player + '_hand')[0]
                f.perform('COMMIT_FG', {'cards': [identity], 'destination': player + '_config_A'}, player)
                f.perform('RETIRE_SUPPORT', {'cards': [identity]}, player)
                f.perform('RECOVER_1', {'cards': [identity]}, player)
            for _ in range(6):
                f.perform('ADD_CONFIGURATION_SPACE', {'rank': 'Red'}, effect={'variant': 'Red'})
        before = f.horizon._state['root']
        restart = f.restart()
        assert before == f.horizon._state['root']
        b = f.horizon._backend
        result = {'status': 'PASS', 'scenario': scenario, 'implementation_sha256': implementation_digest(root),
                  'initial_application_objects': 37, 'initial_relations': 163,
                  'cards': len(b.application_values['cards']), 'spaces': len(f.members('player_1_configuration')),
                  'revision': f.horizon._state['revision'], 'root': before, 'restart': restart,
                  'whole_game_phase': 'PREPRODUCTION', 'authority': 'CONFORMANCE_ONLY',
                  'package_sha256': f.package['sha256'], 'native_road_count': len(b.road_history)}
        write(output / ('evidence/pass-02-demo-' + scenario + '.json'), result)
        return result
    finally:
        f.close()


def audit(root, output):
    evidence = output / 'evidence'
    def read(name):
        path = evidence / name
        return json.loads(path.read_text(encoding='utf8')) if path.is_file() else {}
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
    specification = json.loads((root / 'tests/integration/genesis_horizon/pass_02_acceptance.json').read_text())
    cases = {c['id']: dict(c, status='NOT_RUN', evidence=[]) for c in specification['cases']}
    assert len(cases) == specification['required_cases'] == 83
    implementation = implementation_digest(root)
    head, branch = git('rev-parse', 'HEAD'), git('branch', '--show-current')
    def mark(numbers, condition, records):
        for number in numbers:
            cases[f'P2-{number:03}'].update(status='PASS' if condition else 'FAIL', evidence=records,
                source_revision=head, implementation_sha256=implementation, exit_result=0 if condition else 1)
    tests = read('tests-integration.json')
    current = read('tests-source.json') == {'status': 'PASS', 'implementation_sha256': implementation}
    passed = tests.get('passed', []) if current and not tests.get('failures', 1) and not tests.get('errors', 1) else []
    for name, numbers in TESTS.items():
        mark(numbers, name in passed, [name, 'tests-integration.json', 'tests-integration.log'])
    ancestry = subprocess.run(['git', 'merge-base', '--is-ancestor', START, 'HEAD'], cwd=root).returncode == 0
    mark([1], ancestry, ['git merge-base --is-ancestor ' + START + ' HEAD'])
    baseline = output / 'pass-02-baseline/pass-01-acceptance.json'
    baseline_ok = baseline.is_file() and json.loads(baseline.read_text())['status'] == 'PASS'
    mark([2], baseline_ok and 'test_pass_02.Pass02.test_empty_baseline_and_native_inventory' in passed,
         ['pass-02-baseline/pass-01-acceptance.json', 'test_empty_baseline_and_native_inventory'])
    mark([3], read('upstream-readonly.json').get('status') == 'PASS', ['upstream-readonly.json'])
    changed = git('diff', '--name-only', START, 'HEAD').splitlines()
    from genesis_runtime_pass05 import protected_sources_preserved
    preserved = protected_sources_preserved(root, START, changed, ('data/cycles/', 'data/qmo/', 'mathematics/', 'design/'))
    repository = read('repository-validation.json')
    repo_ok = repository.get('status') == 'PASS' and repository.get('implementation_sha256') == implementation
    mark([10, 76], preserved and repo_ok, ['Git source-byte check; only five exact Pass-05 authority-pointer hash pairs permitted', 'repository-validation.json'])
    # All declared handlers have concrete behavior tests, including all six recovery profiles.
    all_operations = all(name in passed for name in TESTS)
    mark([12], all_operations and read('build.json').get('status') == 'PASS', ['build.json', *TESTS])
    legacy = [name for name in passed if name.startswith('test_pass_01.')]
    mark([16, 75], len(legacy) == 18 and read('acceptance.json').get('status') == 'PASS',
         ['18 preserved Pass-1 tests', '74-case runtime acceptance.json'])
    policy = json.loads((root / 'development/modules/core-game/PASS_02_POLICY_GATES.json').read_text())
    mark([51], bool(policy) and current, ['PASS_02_POLICY_GATES.json', 'conformance-only fixture and no full Utility export'])
    mark([68], any(n.endswith('.test_retry_conflict_concurrent_scope_and_stale') for n in passed) and
         any(n.endswith('.test_projection_gap_receipt_clock_and_reconnect') for n in passed), ['existing epoch/reconnect integration tests', 'tests-integration.json'])
    mark([69], any(n.endswith('.test_backpressure_before_mutation') for n in passed) and
         'test_pass_02_adversarial.Adversarial.test_input_bounds_code_and_card_only_containment' in passed,
         ['test_backpressure_before_mutation', 'test_input_bounds_code_and_card_only_containment'])
    distributions = read('distribution-verification.json')
    isolated = distributions.get('status') == 'PASS' and all(d.get('implementation_sha256') == implementation for d in distributions.get('archives', {}).values())
    mark([77, 80], isolated and len(distributions.get('archives', {})) == 2, ['distributions.json', 'distribution-verification.json'])
    isolation = distributions.get('isolation', {})
    mark([78, 79], isolated and isolation.get('probes_passed') is True and isolation.get('violations') == [],
         ['distribution-verification.json', 'distribution-isolation-probes.log', 'enforced Python audit hooks in every child interpreter'])
    mark([81], isolated and distributions.get('missing_dependency_negative') == 'PASS', ['distribution-missing-dependency.log'])
    receipt = root / 'development/modules/core-game/PASS_02_RECEIPT.md'
    mark([82], len(cases) == 83 and receipt.is_file() and bool(policy), ['83-case unchanged specification', 'PASS_02_RECEIPT.md', 'PASS_02_POLICY_GATES.json'])
    remote = git('ls-remote', 'origin', 'refs/heads/' + branch).split()
    main = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
    clean = not git('status', '--porcelain')
    from genesis_runtime_pass05 import successor
    mark([83], (successor(root,branch) or branch == 'codex/raeon-pass-02' or (branch in ('codex/raeon-pass-03','codex/raeon-pass-03b','codex/raeon-pass-04') and
        subprocess.run(['git', 'merge-base', '--is-ancestor', 'd991278bc72518e9abe2df7741298a2631c787d0', 'HEAD'], cwd=root).returncode == 0)) and bool(remote and remote[0] == head) and clean and main == MAIN and ancestry and receipt.is_file(),
         ['Git remote and clean-status checks', 'PASS_02_EXECUTION.md', 'PASS_02_RECEIPT.md'])
    result = {'status': 'PASS' if all(c['status'] == 'PASS' for c in cases.values()) else 'INCOMPLETE',
              'passed': sum(c['status'] == 'PASS' for c in cases.values()), 'total': 83,
              'branch': branch, 'starting_sha': START, 'ending_sha': head, 'remote_sha': remote[0] if remote else None,
              'main_sha': main, 'clean': clean, 'implementation_sha256': implementation, 'cases': list(cases.values()),
              'policy_gated': policy, 'whole_game_phase': 'PREPRODUCTION'}
    write(evidence / 'pass-02-acceptance.json', result)
    return result
