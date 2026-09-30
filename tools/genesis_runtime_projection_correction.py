"""Separate evidence for Vera V-P2-01; runtime 74 and Pass-2 83 stay unchanged."""
import json

from genesis_runtime_distribution import implementation_digest
from genesis_runtime_tasks import write


TESTS = [
    'test_audited_public_view_cannot_inherit_private_hand',
    'test_audited_same_actor_public_cannot_inherit_inspection',
    'test_audited_live_merge_cannot_restore_private_relations',
    'test_owner_opponent_and_public_controls',
    'test_public_live_geometry_delta_and_reconnect',
    'test_private_inspection_delta_reconnect_restore_and_expiry',
    'test_inspection_scope_includes_application_view_owner_and_actor',
    'test_public_inspect_admission_rejected_atomically',
]


def audit(root, output):
    def read(name):
        path = output / 'evidence' / name
        return json.loads(path.read_text(encoding='utf8')) if path.is_file() else {}

    implementation = implementation_digest(root)
    current = read('tests-source.json') == {'status': 'PASS', 'implementation_sha256': implementation}
    tests = read('tests-integration.json')
    passed = tests.get('passed', []) if current and tests.get('failures') == tests.get('errors') == 0 else []
    cases = [{'id': 'V-P2-01-' + str(i + 1), 'test': name,
              'kind': 'audited_failure' if i < 3 else 'additional_control',
              'status': 'PASS' if 'test_pass_02_projection_privacy.ProjectionPrivacy.' + name in passed else 'FAIL'}
             for i, name in enumerate(TESTS)]
    distributions = read('distribution-verification.json')
    archives = distributions.get('archives', {})
    fresh = (distributions.get('status') == 'PASS' and len(archives) == 2
             and all(a.get('implementation_sha256') == implementation for a in archives.values()))
    result = {'finding': 'V-P2-01', 'status': 'PASS' if fresh and all(c['status'] == 'PASS' for c in cases) else 'INCOMPLETE',
              'passed': sum(c['status'] == 'PASS' for c in cases), 'total': len(cases), 'cases': cases,
              'fresh_distribution_verified': fresh, 'implementation_sha256': implementation,
              'evidence': ['tests-integration.json', 'tests-integration.log', 'tests-source.json',
                           'distribution-verification.json', 'distribution-integration-tests.log'],
              'original_denominators': {'runtime': 74, 'pass_02': 83}}
    write(output / 'evidence/projection-correction-acceptance.json', result)
    return result
