"""Pass-3B positive offline demonstration and exact 85/98-case evidence maps."""
import copy
import hashlib
import json
import subprocess
import sys

from genesis_runtime_tasks import setup, write
from genesis_runtime_distribution import implementation_digest

START='33f4139719c5b4af83610dcb9600be594a50e78c'
MAIN='69a0030805b8c3858c877a514e2f50644421115a'
SPEC='provenance/imports/raeon-pass-03b/handoff/acceptance/PASS_03B_ACCEPTANCE.json'
TESTS={
 'test_pass_03b_math.RealizationMath.test_all_witness_memberships_edges_and_rotation_matrices':[7,8,10,11,24,30],
 'test_pass_03b_math.RealizationMath.test_se2_translation_rotation_exact_and_shared_yaw_targets':[12,13,14,23],
 'test_pass_03b_math.RealizationMath.test_reflection_scale_and_identity_permutation_are_not_equivalence':[15,16,21],
 'test_pass_03b_math.RealizationMath.test_candidate_magnetization_release_and_shape_only_never_lock':[18,19,20],
 'test_pass_03b_math.RealizationMath.test_quaternion_sign_classes_and_thresholds':[22,25,26,27],
 'test_pass_03b_math.RealizationMath.test_simultaneous_edges_tethers_and_no_face_socket_exclusivity':[29,31],
 'test_pass_03b_math.RealizationMath.test_membership_and_authority_tamper_fail_closed':[74,75],
 'test_pass_03b.Pass03B.test_live_base_lock_identity_native_color_and_explicit_reopen':[40,42,44,46,47,48],
 'test_pass_03b.Pass03B.test_shape_orientation_partial_feedback_and_magnetic_hysteresis':[17,28,39],
 'test_pass_03b.AllBaseFields.test_all_60_source_witnesses_resolve_through_actual_package':[32,33,34,35,36,37,38],
 'test_pass_03b.Pass03B.test_resolution_rollback_retry_and_postcommit_delivery':[41,45],
 'test_pass_03b.Pass03B.test_stale_pose_witness_and_concurrent_resolution':[43,73],
 'test_pass_03b.Pass03B.test_positive_fusion_exact_union_frames_width_and_subsumed_provenance':[50,52,53,54,56],
 'test_pass_03b.Pass03B.test_fusion_rollback_source_negative_owner_and_no_recursive_split':[49,51,55],
 'test_pass_03b.Pass03B.test_invalid_source_fusion_preserves_distinct_duplicate_copies':[57],
 'test_pass_03b.Pass03B.test_passive_three_pair_emergents_selective_loss_and_nontargetability':[58,59,60,61,62,63,64,65,66],
 'test_pass_03b.Pass03B.test_configuring_resolved_checkpoint_and_public_byte_reconnect':[67,68,69,70,71],
 'test_pass_03b.Pass03B.test_deterministic_replay_different_paths':[72],
 'test_pass_03b.Pass03B.test_genesis_positive_predicates_transform_and_road_are_required':[76,77],
}
REAUDIT={
 'test_pass_03b_math.RealizationMath.test_quaternion_sign_classes_and_thresholds':[18,20],
 'test_pass_03b_math.RealizationMath.test_simultaneous_edges_tethers_and_no_face_socket_exclusivity':[30,31,33],
 'test_pass_03b_math.RealizationMath.test_membership_and_authority_tamper_fail_closed':[34],
 'test_pass_03b.Pass03B.test_stale_pose_witness_and_concurrent_resolution':[38,84],
 'test_pass_03b.Pass03B.test_live_base_lock_identity_native_color_and_explicit_reopen':[39,42,43,44,45],
 'test_pass_03b.Pass03B.test_shape_orientation_partial_feedback_and_magnetic_hysteresis':[40,41,77],
 'test_pass_03b.AllBaseFields.test_all_60_source_witnesses_resolve_through_actual_package':[48],
 'test_pass_03b.Pass03B.test_passive_three_pair_emergents_selective_loss_and_nontargetability':[49,62,63,66,67,68,69,71,80],
 'test_pass_03b.Pass03B.test_positive_fusion_exact_union_frames_width_and_subsumed_provenance':[51,53,54,59],
 'test_pass_03b.Pass03B.test_invalid_source_fusion_preserves_distinct_duplicate_copies':[52],
 'test_pass_03b.Pass03B.test_fusion_rollback_source_negative_owner_and_no_recursive_split':[56,58,60],
 'test_pass_03b.Pass03B.test_dynamic_nine_spaces_and_fusion_preserve_region_identity':[57,76],
 'test_pass_03b.Pass03B.test_emergent_instances_no_qmo_alias_and_atomic_support_publication':[64,65,70],
 'test_pass_03b.Pass03B.test_configuring_resolved_checkpoint_and_public_byte_reconnect':[75,81,85],
 'test_pass_03b.Pass03B.test_resolution_rollback_retry_and_postcommit_delivery':[82,83],
 'test_pass_03b.Pass03B.test_deterministic_replay_different_paths':[87],
 'test_pass_03.Pass03.test_small_population_duplicates_wrong_family_and_budget':[88],
}


def demo(root, output):
    setup(root);sys.path.insert(0,str(root/'tests/integration/genesis_horizon'))
    from pass_03b_support import FieldFixture
    f=FieldFixture('pass03b-offline-scene')
    try:
        groups=f.prepare(['M-O-01','M-O-02'])
        captures=[]
        for group in groups:
            f.position(group)
            query=f.ext.query(group[0]);assert query['realizations'][0]['stage']=='MAGNETIZED'
            captures.append(query)
            f.resolve(group)
        supports=copy.deepcopy(f.ext.state)
        assert len([s for s in supports['spaces'].values() if s['lifecycle']=='RESOLVED'])==2
        assert len(supports['emergents'])==1
        f.perform('MERGE_CONFIGURATION',f.merge_args(groups[0][0],groups[1][0]))
        merged=copy.deepcopy(f.ext.state)
        assert len(f.members('player_1_configuration'))==2 and not merged['emergents']
        derived=[v for v in merged['fields'].values() if v['active']]
        assert len(derived)==1 and derived[0]['qmo']=='@qmo/raeon/derived/fusion/m-o-01+m-o-02'
        restart=f.restart()
        assert f.horizon._backend.collections.extension.state==merged
        result={'status':'PASS','scope':'actual Genesis package / Hypervisor byte boundary',
                'query_magnetization':captures,'resolved_supports':supports,'fusion':merged,
                'restart':restart,'whole_game_phase':'PREPRODUCTION','native_devices':'NOT_RUN'}
        write(output/'evidence/pass-03b-demo.json',result)
        return {'status':'PASS','query':True,'magnetized':True,'resolved':2,'emergents':1,'fusion':derived[0]['qmo'],'restart':True}
    finally:f.close()


def reaudit(root, output, result, passed, current):
    cases={c['id']:c for c in result['cases']}
    for name,numbers in REAUDIT.items():
        for number in numbers:
            success=current and name in passed
            cases[f'P3-{number:03}'].update(status='PASS' if success else 'FAIL',
                evidence=[name,'tests-integration.json','tests-source.json'],reason=None if success else 'Current executable positive evidence absent')
    cases['P3-047'].update(status='BLOCKED',reason='G-COLOR: mutable current-output/availability carryover belongs to Pass 4 and is not supplied by Pass 3B.',
        evidence=['PASS_03_POLICY_GATES.json: G-COLOR','PASS_03B_EXECUTION.md'])
    dist=json.loads((output/'evidence/distribution-verification.json').read_text())
    fresh=dist.get('status')=='PASS' and dist.get('pass03b_scene')=='PASS' and all(
        a['implementation_sha256']==implementation_digest(root) for a in dist.get('archives',{}).values())
    for number in (93,95):
        cases[f'P3-{number:03}'].update(status='PASS' if fresh else 'FAIL',
            evidence=['distribution-pass-03b-demo.log','distribution-integration-tests.log','distribution-verification.json'],
            reason=None if fresh else 'Fresh positive live scene not demonstrated')
    result.update(passed=sum(c['status']=='PASS' for c in cases.values()),
                  blocked=sum(c['status']=='BLOCKED' for c in cases.values()),failed=sum(c['status']=='FAIL' for c in cases.values()))
    result['status']='PASS' if result['passed']==98 else 'PARTIAL'
    result['ready_for_pass_04']=result['passed']==98
    result['supplemental'].update(field_creation='PASS' if 'test_pass_03b.AllBaseFields.test_all_60_source_witnesses_resolve_through_actual_package' in passed else 'INCOMPLETE',
                                  pass03b_authority='game/qmo/realization.lock.json')
    return result


def audit(root, output):
    evidence=output/'evidence'
    def read(name):
        path=evidence/name
        return json.loads(path.read_text(encoding='utf8')) if path.is_file() else {}
    def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
    spec=json.loads((root/SPEC).read_text());cases={c['id']:copy.deepcopy(c) for c in spec['cases']}
    assert len(cases)==spec['required_cases']==85
    implementation=implementation_digest(root)
    current=read('tests-source.json')=={'status':'PASS','implementation_sha256':implementation}
    tests=read('tests-integration.json');passed=tests.get('passed',[]) if current and tests.get('failures')==tests.get('errors')==0 else []
    def mark(numbers,condition,records):
        for n in numbers:cases[f'P3B-{n:03}'].update(status='PASS' if condition else 'FAIL',evidence=records)
    for name,numbers in TESTS.items():mark(numbers,name in passed,[name,'tests-integration.json','tests-source.json'])
    entry=json.loads((root/'provenance/imports/raeon-pass-03b/entry.json').read_text())
    ancestry=subprocess.run(['git','merge-base','--is-ancestor',START,'HEAD'],cwd=root).returncode==0
    mark([1,2],ancestry and entry['before_implementation'] and
        all(entry['results']['pass-03-acceptance.json'][k]==v for k,v in [('passed',49),('blocked',49),('failed',0)]),
        ['provenance/imports/raeon-pass-03b/entry.json','verified Pass-3 ancestor'])
    mark([3],entry['privacy_rerun']['run']==8 and read('projection-correction-acceptance.json').get('status')=='PASS',
         ['entry.json','projection-correction-acceptance.json'])
    mark([4],read('upstream-readonly.json').get('status')=='PASS',['upstream-readonly.json'])
    branch,head=git('branch','--show-current'),git('rev-parse','HEAD')
    remote=git('ls-remote','origin','refs/heads/'+branch).split()
    main=git('ls-remote','origin','refs/heads/main').split()[0];clean=not git('status','--porcelain')
    mark([5],main==MAIN,['remote main SHA and no merge'])
    decision=json.loads((root/'provenance/decisions/raeon-pass-03b.json').read_text())
    sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
    mark([6],all(sha(p)==v for p,v in decision['authority_hashes'].items()),['exact authority hashes','realization.lock.json'])
    mark([9],all(sha(p)==v for p,v in decision['qmo_sources'].items()),['cycle1.lock.json','preserved source SHA256'])
    mark([78],not git('diff','--name-only',START,'--','platform/shared/python_hypervisor'),['Hypervisor unchanged from '+START])
    dist=read('distribution-verification.json')
    fresh=dist.get('status')=='PASS' and dist.get('pass03b_scene')=='PASS' and len(dist.get('archives',{}))==2 and all(
        a['implementation_sha256']==implementation for a in dist['archives'].values())
    mark([79,80],fresh and dist.get('isolation',{}).get('violations')==[],['distribution-verification.json','distribution-pass-03b-demo.log'])
    previous=read('pass-03-acceptance.json')
    mark([81],current and all(read(n).get('status')=='PASS' for n in ['acceptance.json','pass-02-acceptance.json','projection-correction-acceptance.json'])
         and read('repository-validation.json').get('implementation_sha256')==implementation,
         ['runtime 74 / Pass-2 83 / privacy 8','repository-validation.json','tests-integration.json'])
    mark([82],previous.get('total')==98 and previous.get('failed')==0,['pass-03-acceptance.json'])
    mark([83],ancestry and branch=='codex/raeon-pass-03b' and bool(remote) and remote[0]==head and clean and main==MAIN
         and (root/'development/modules/core-game/PASS_03B_RECEIPT.md').is_file(),['Git ancestry/HEAD/remote/clean/main','PASS_03B_RECEIPT.md'])
    mark([84],decision['whole_game_phase']=='PREPRODUCTION',['raeon-pass-03b.json'])
    mark([85],previous.get('total')==98 and previous.get('failed')==0 and not previous.get('ready_for_pass_04') and 'test_pass_03b.AllBaseFields.test_all_60_source_witnesses_resolve_through_actual_package' in passed,
         ['pass-03-acceptance.json','pass-03b-all-base-fields.json'])
    result={'schema_version':1,'status':'PASS' if all(c['status']=='PASS' for c in cases.values()) else 'INCOMPLETE',
        'repository':'xApologies/_raeon','branch':branch,'starting_sha':START,'ending_sha':head,'remote_sha':remote[0] if remote else None,
        'main_sha':main,'clean':clean,'implementation_sha256':implementation,'passed':sum(c['status']=='PASS' for c in cases.values()),
        'total':85,'cases':list(cases.values()),'pass03_reaudit':{k:previous.get(k) for k in ('passed','blocked','failed','total')},
        'authority_hashes':decision['authority_hashes'],'tests':{n:read(n) for n in ['tests-unit.json','tests-integration.json','upstream-tests.json','repository-validation.json']},
        'offline_distributions':read('distributions.json'),'open_items':decision['open_items'],'whole_game_phase':'PREPRODUCTION'}
    write(evidence/'pass-03b-acceptance.json',result)
    return result
