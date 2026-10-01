"""Pass-3 topology demo and unchanged 98-case evidence map; no false closure PASS."""
import copy
import json
import subprocess
import sys

from genesis_runtime_tasks import setup, write
from genesis_runtime_distribution import implementation_digest

CORRECTED = 'd991278bc72518e9abe2df7741298a2631c787d0'
MAIN = '69a0030805b8c3858c877a514e2f50644421115a'
SPEC = 'provenance/imports/raeon-pass-03/handoff/acceptance/PASS_03_ACCEPTANCE.json'
TESTS = {
    'test_corpus_full_sqlite_and_json_agree': [6,7],
    'test_pair_lookup_preserves_all_outcomes_and_addresses': [8,9,10,61],
    'test_source_integrity_missing_corpus_and_exact_render_integer': [11,13],
    'test_native_hydration_duplicate_copies_and_source_bytes': [15,16],
    'test_numeric_bounds_zero_rotation_and_no_z_or_reflection_input': [17,19,21],
    'test_owner_membership_stale_and_no_individual_extraction': [22,23],
    'test_batch_atomic_rollback_retry_and_post_commit_delivery': [24],
    'test_concurrent_stale_pose_and_nonempty_checkpoint': [25],
    'test_handler_predicate_omission_and_road_closure_matter': [26],
    'test_small_population_duplicates_wrong_family_and_budget': [27,29,37],
    'test_catalog_not_live_closure_and_read_only_exhaustive_query': [28,32,35,36],
    'test_reopen_merge_preview_and_gated_mutations_preserve_copies': [46,50,55],
    'test_public_view_only_exposes_deployed_source_and_no_inventory_hints': [72,73,74,78],
    'test_public_byte_delta_and_reconnect_with_topology': [79],
    'test_source_extension_and_checkpoint_abi_tamper_rejected': [86],
}


def demo(root, output):
    setup(root)
    sys.path.insert(0, str(root / 'tests/integration/genesis_horizon'))
    from pass_02_support import CardFixture
    f = CardFixture('pass03-headless')
    try:
        f.initialize(['FG-001','FG-044','FG-117'] + [f'FG-{i:03}' for i in range(2,59)])
        cards = []
        for _ in range(3):
            f.perform('DRAW_ONE')
            card = f.members('player_1_hand')[0]
            f.perform('COMMIT_FG', dict(cards=[card],destination='player_1_config_A'))
            cards.append(card)
        f.perform('SET_FG_POSES', {'space':'player_1_config_A','membership_revision':3,
            'poses':[dict(card=c,x=i*1000,y=-100,qw=1,qx=2,qy=3,qz=4,pose_revision=0) for i,c in enumerate(cards)]})
        query = f.horizon._backend.collections.extension.query('player_1_config_A')
        assert query['membership'] == 'MATCH' and query['pose_closure'] == 'UNRESOLVED'
        assert query['witness'] is None
        restart = f.restart()
        result = {'status':'PASS', 'scope':'SOURCE_QUERY_POSE_AND_NONEMPTY_RECOVERY_ONLY',
            'pass_status':'PARTIAL', 'field_realization':'BLOCKED_G-POSE', 'merge':'BLOCKED_G-MERGE',
            'link':'BLOCKED_G-LINK', 'cards':cards, 'query':query, 'restart':restart,
            'whole_game_phase':'PREPRODUCTION', 'native_device_tests':'NOT_RUN'}
        write(output / 'evidence/pass-03-demo.json',result)
        return result
    finally:
        f.close()


def audit(root, output):
    evidence = output / 'evidence'
    def read(name):
        path = evidence / name
        return json.loads(path.read_text(encoding='utf8')) if path.is_file() else {}
    def git(*args):
        return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
    specification = json.loads((root/SPEC).read_text(encoding='utf8'))
    cases = {c['id']: copy.deepcopy(c) for c in specification['cases']}
    assert len(cases) == specification['required_cases'] == 98
    implementation = implementation_digest(root)
    tests = read('tests-integration.json')
    current = read('tests-source.json') == {'status':'PASS','implementation_sha256':implementation}
    passed = tests.get('passed',[]) if current and tests.get('failures') == tests.get('errors') == 0 else []
    for case in cases.values():
        case.update(status='BLOCKED', evidence=['development/modules/core-game/PASS_03_POLICY_GATES.json'],
            reason=case['source_or_policy_gate'] or 'Dependent live field/support behavior has not been demonstrated.')
    def mark(numbers, condition, records):
        for number in numbers:
            cases[f'P3-{number:03}'].update(status='PASS' if condition else 'FAIL', evidence=records,
                                         reason=None if condition else 'Current evidence absent or failed')
    entry = json.loads((root/'provenance/imports/raeon-pass-03/entry.json').read_text(encoding='utf8'))
    ancestry = subprocess.run(['git','merge-base','--is-ancestor',CORRECTED,'HEAD'],cwd=root).returncode == 0
    mark([1,2,3,4], ancestry and entry['before_implementation'] and
         entry['results']['tests-integration.json']['run'] == 64 and entry['results']['projection-correction-acceptance.json']['passed'] == 8,
         ['provenance/imports/raeon-pass-03/entry.json','corrected Git ancestor'])
    mark([5],read('upstream-readonly.json').get('status')=='PASS',['upstream-readonly.json'])
    for name,numbers in TESTS.items():
        mark(numbers,'test_pass_03.Pass03.'+name in passed,[name,'tests-integration.json','tests-integration.log'])
    mark([12],(root/'development/modules/core-game/PASS_03_POLICY_GATES.json').is_file(),
         ['PASS_03_POLICY_GATES.json','PASS_03_EXECUTION.md','original nested v0.2 mathematics and generator skeleton'])
    changed = git('diff','--name-only',CORRECTED,'HEAD').splitlines()
    preserved = not any(p.startswith(('data/cycles/','data/qmo/','data/render_specs/','mathematics/','design/','provenance/sources/')) for p in changed)
    mark([14],preserved,['Git source-byte preservation comparison with '+CORRECTED])
    legacy = json.loads((root/'provenance/decisions/raeon-pass-03.json').read_text())['preserved_tests']
    import hashlib
    unchanged = all(hashlib.sha256((root/p).read_bytes()).hexdigest()==sha for p,sha in legacy.items())
    mark([89],current and unchanged and read('pass-02-acceptance.json').get('status')=='PASS'
         and read('projection-correction-acceptance.json').get('status')=='PASS',
         ['tests-source.json','tests-integration.json','74 runtime / 83 Pass-2 / 8 privacy acceptance; exact preserved test hashes'])
    mark([90],read('verify.json').get('deterministic_rebuild') is True,['build.json','verify.json'])
    repository = read('repository-validation.json')
    mark([91],preserved and repository.get('status')=='PASS' and repository.get('implementation_sha256')==implementation,
         ['repository-validation.json','source corpus integration tests'])
    dist = read('distribution-verification.json')
    fresh = dist.get('status')=='PASS' and len(dist.get('archives',{}))==2 and all(a['implementation_sha256']==implementation for a in dist.get('archives',{}).values())
    mark([92],fresh,['distributions.json','distribution-verification.json'])
    mark([94],fresh and dist.get('missing_qmo_negative')=='PASS' and dist.get('missing_dependency_negative')=='PASS',
         ['distribution-missing-qmo.log','distribution-missing-dependency.log'])
    # Cold pose/query/recovery passes are supplemental: full live-field positives 93/95 stay BLOCKED.
    head,branch = git('rev-parse','HEAD'),git('branch','--show-current')
    remote = git('ls-remote','origin','refs/heads/'+branch).split()
    main = git('ls-remote','origin','refs/heads/main').split()[0]
    clean = not git('status','--porcelain')
    mark([97],ancestry and branch in ('codex/raeon-pass-03','codex/raeon-pass-03b','codex/raeon-pass-04') and remote and remote[0]==head and clean and main==MAIN,
         ['Git ancestry, remote SHA, main SHA, clean working-tree checks'])
    mark([96,98],len(cases)==98 and (root/'development/modules/core-game/PASS_03_RECEIPT.md').is_file(),
         ['unchanged 98 requirement IDs','PASS_03_RECEIPT.md','PASS_03_EXECUTION.md'])
    result = {'status':'PARTIAL','ready_for_pass_04':False,'whole_game_phase':'PREPRODUCTION',
        'PASS2_CORRECTED_SHA':CORRECTED,'head':head,'remote':remote[0] if remote else None,'main':main,
        'clean':clean,'implementation_sha256':implementation,'total':98,
        'passed':sum(c['status']=='PASS' for c in cases.values()),
        'blocked':sum(c['status']=='BLOCKED' for c in cases.values()),
        'failed':sum(c['status']=='FAIL' for c in cases.values()),'cases':list(cases.values()),
        'supplemental':{'pose_query_recovery_demo':read('pass-03-demo.json').get('status'),
                        'offline_partial_topology':fresh,'field_creation':'BLOCKED','native_devices':'NOT_RUN'}}
    if (root/'provenance/decisions/raeon-pass-03b.json').is_file():
        from genesis_runtime_pass03b import reaudit
        result = reaudit(root, output, result, passed, current)
    if (root/'provenance/decisions/raeon-pass-04.json').is_file():
        from genesis_runtime_pass04 import reaudit as color_reaudit
        result = color_reaudit(root, output, result, passed, current)
    write(evidence/'pass-03-acceptance.json',result)
    if result['failed']:
        raise RuntimeError('Pass-3 implemented-scope evidence failed; inspect pass-03-acceptance.json')
    return result
