"""Pass-4 positive scene and 108-case evidence audit, retaining prior denominators."""
import copy
import ctypes
import hashlib
import json
import subprocess
import sys

from genesis_runtime_tasks import setup, write
from genesis_runtime_distribution import implementation_digest

START='d644a361aa2ce788a1da991b15e3b8e3be5c7cba'
MAIN='69a0030805b8c3858c877a514e2f50644421115a'
SPEC='provenance/imports/raeon-pass-04/handoff/PASS_04_ACCEPTANCE.json'
TESTS={
 'test_catalog_binding_identity_initial_states_and_fixed_slots':[24,25,26,27],
 'test_A_generate_current_color_once_through_road':[6,7,8,9,10,11,12,79],
 'test_B_partial_repeated_spending_keeps_health_and_shield':[28,35,36,37,42,60,80],
 'test_C_D_shield_first_damage_and_health_first_restore':[29,31,32,33,34,41,81,82],
 'test_E_same_topology_carryover_no_implicit_heal_or_refresh':[14,15,16,17,18,83],
 'test_F_zero_color_atomic_graveyard_and_selective_emergence_loss':[19,20,21,22,23,84],
 'test_G_H_authority_windows_reservations_and_no_switch_refresh':[13,38,39,40,49,50,51,52,53,54,55,56,57,58,59,85,86],
 'test_I_inactive_stays_fixed_and_white_restores_only_one_health':[30,43,44,45,46,47,87],
 'test_overflow_and_unsupported_targets_fail_without_consuming':[48],
 'test_atomic_generation_spend_retry_and_lost_delivery':[61,62,64,65],
 'test_concurrent_use_spend_and_stale_object_revisions':[63,66,67],
 'test_J_checkpoint_restart_deterministic_replay_and_filtered_deltas':[68,69,70,71,72,88],
 'test_selected_view_color_deltas_preserve_private_boundaries':[73,74,75,76,77,78],
 'test_Genesis_admission_transform_and_Road_cannot_be_bypassed':[89,90],
}


def qualification():
    mask=None
    if sys.platform=='win32':
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.GetCurrentProcess.restype=ctypes.c_void_p
        kernel.GetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
        process,system=ctypes.c_size_t(),ctypes.c_size_t()
        if not kernel.GetProcessAffinityMask(kernel.GetCurrentProcess(),ctypes.byref(process),ctypes.byref(system)):
            raise RuntimeError('Cannot verify process affinity qualification')
        mask=process.value
    return {'python':sys.version.split()[0],'platform':sys.platform,'processor_mask':mask,
            'host_risk':'HOST-RUNTIME-001','unrestricted_stability':'OPEN'}


def demo(root, output):
    setup(root);sys.path.insert(0,str(root/'tests/integration/genesis_horizon'))
    from pass_04_support import PrimeFixture
    f=PrimeFixture('pass04-offline-scene')
    try:
        (healer,target),fields=f.setup_player(primes=['restore_green','universal_green'],manifolds=['M-G-01','M-R-01'])
        (attacker,),other=f.setup_player('player_2',['degrade_yellow'],['M-Y-01'])
        f.active('player_1');f.generate(fields[0],healer);f.spend(healer,target,2,'RESTORE')
        generated=copy.deepcopy(f.color.state)
        assert generated['primes'][healer]['C']==generated['primes'][target]['C']==2
        f.active('player_2');f.generate(other[0],attacker,'player_2');f.spend(attacker,fields[0],3,'DEGRADE','player_2')
        assert f.ext.state['fields'][fields[0]]['current_magnitude']==1
        assert f.ext.state['fields'][fields[0]]['availability']=='USED'
        f.generate(fields[1],target)  # Reserved READY source used during DEFENSE.
        assert f.color.state['primes'][target]['C']==3
        values=copy.deepcopy(f.horizon._backend.application_values);roads=copy.deepcopy(f.horizon._backend.road_history)
        restart=f.restart()
        assert f.horizon._backend.application_values==values
        restored=f.horizon._backend.road_history
        def preserved(rows):
            return [(f.color.road_commitment(r),r['timestamp_ns'],[p['timestamp_ns'] for p in r['portal_receipts']]) for r in rows]
        assert preserved(restored[:len(roads)])==preserved(roads)
        assert len(restored)>len(roads) and all(r['canonical_mmo_id']=='HORIZON:REFERENCE:request' for r in restored[len(roads):])
        result={'status':'PASS','implementation_sha256':implementation_digest(root),'scope':'real Genesis / Rainbow Road / Hypervisor',
            'generated_and_partial_spend':generated,'final_state':values['color_primes'],
            'field_states':{k:{n:v[n] for n in ('qmo','native_color','native_maximum','current_magnitude','current_color','availability')}
                            for k,v in values['topology']['fields'].items() if v['ordinary']},
            'restart':restart,'road_count':len(roads),'qualification':qualification(),
            'whole_game_phase':'PREPRODUCTION','full_scheduler':'OPEN','native_devices':'NOT_RUN'}
        write(output/'evidence/pass-04-demo.json',result)
        return {k:result[k] for k in ('status','scope','field_states','road_count','qualification','whole_game_phase','full_scheduler')}
    finally:f.close()


def reaudit(root, output, result, passed, current):
    name='test_pass_04.Pass04.test_E_same_topology_carryover_no_implicit_heal_or_refresh'
    case=next(c for c in result['cases'] if c['id']=='P3-047')
    ok=current and name in passed
    case.update(status='PASS' if ok else 'FAIL',reason=None if ok else 'Current Pass-4 carryover evidence absent',
                evidence=[name,'tests-integration.json','tests-source.json','PASS_04_EXECUTION.md'])
    result.update(passed=sum(c['status']=='PASS' for c in result['cases']),
                  blocked=sum(c['status']=='BLOCKED' for c in result['cases']),failed=sum(c['status']=='FAIL' for c in result['cases']))
    result['status']='PASS' if result['passed']==98 else 'PARTIAL'
    result['ready_for_pass_04']=result['passed']==98
    result['supplemental']['color_availability']='PASS' if ok else 'INCOMPLETE'
    return result


def audit(root, output):
    evidence=output/'evidence'
    def read(n):
        p=evidence/n
        return json.loads(p.read_text(encoding='utf8')) if p.is_file() else {}
    def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
    sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
    spec=json.loads((root/SPEC).read_text());cases={c['id']:copy.deepcopy(c) for c in spec['cases']}
    assert len(cases)==spec['required_cases']==108
    digest=implementation_digest(root)
    current=read('tests-source.json')=={'status':'PASS','implementation_sha256':digest}
    tests=read('tests-integration.json');passed=tests.get('passed',[]) if current and tests.get('failures')==tests.get('errors')==0 else []
    def mark(numbers, condition, records):
        for n in numbers:cases[f'P4-{n:03}'].update(status='PASS' if condition else 'FAIL',evidence=records)
    for name,numbers in TESTS.items():
        identity='test_pass_04.Pass04.'+name
        mark(numbers,identity in passed,[identity,'tests-integration.json','tests-source.json'])
    entry=json.loads((root/'provenance/imports/raeon-pass-04/entry.json').read_text())
    ancestry=subprocess.run(['git','merge-base','--is-ancestor',START,'HEAD'],cwd=root).returncode==0
    mark([1],ancestry and entry['before_implementation'] and entry['starting_sha']==START and
         entry['results']['pass-03b-acceptance.json']['passed']==85,['entry.json','verified Pass-3B ancestor'])
    branch,head=git('branch','--show-current'),git('rev-parse','HEAD')
    remote=git('ls-remote','origin','refs/heads/'+branch).split()
    main=git('ls-remote','origin','refs/heads/main').split()[0];clean=not git('status','--porcelain')
    mark([2],main==MAIN,['remote main SHA'])
    mark([3],read('upstream-readonly.json').get('status')=='PASS',['upstream-readonly.json'])
    mark([4],read('projection-correction-acceptance.json').get('status')=='PASS',['eight original privacy regressions'])
    host=json.loads((root/'development/modules/core-game/HOST_RUNTIME_RISKS.json').read_text());environment=qualification()
    mark([5],host['risks'][0]['id']=='HOST-RUNTIME-001' and host['risks'][0]['status']=='OPEN_QUALIFIED' and
         environment['python']=='3.12.10' and environment['processor_mask']==65536,['HOST_RUNTIME_RISKS.json','current qualified audit process'])
    mark([91],not git('diff','--name-only',START,'--','platform/shared/python_hypervisor'),['Hypervisor unchanged'])
    p3b=read('pass-03b-acceptance.json');p3=read('pass-03-acceptance.json')
    mark([92],p3b.get('status')=='PASS' and p3b.get('passed')==85,['pass-03b-acceptance.json'])
    mark([93],p3.get('passed')==98 and p3.get('blocked')==p3.get('failed')==0,['pass-03-acceptance.json','P3-047 current carryover test'])
    base=read('pass-03b-all-base-fields.json')
    mark([94],current and base.get('status')=='PASS' and base.get('run')==60 and
         'test_pass_03b.AllBaseFields.test_all_60_source_witnesses_resolve_through_actual_package' in passed,['pass-03b-all-base-fields.json'])
    for number,name in [(95,'test_positive_fusion_exact_union_frames_width_and_subsumed_provenance'),
                        (96,'test_passive_three_pair_emergents_selective_loss_and_nontargetability'),
                        (97,'test_dynamic_nine_spaces_and_fusion_preserve_region_identity')]:
        mark([number],'test_pass_03b.Pass03B.'+name in passed,[name,'tests-integration.json'])
    decision=json.loads((root/'provenance/decisions/raeon-pass-04.json').read_text())
    mark([98],all(sha(p)==v for p,v in decision['qmo_sources'].items()),['unchanged original QMO SHA256'])
    repo=read('repository-validation.json')
    repo_ok=repo.get('status')=='PASS' and repo.get('implementation_sha256')==digest
    mark([99,100,101],repo_ok,['repository-validation.json','all validators / regression tests / gameplay specs'])
    mark([102],read('verify.json').get('deterministic_rebuild') is True and read('verify.json').get('compiled_sources')==46,
         ['46-source deterministic Genesis verify.json'])
    dist=read('distribution-verification.json')
    fresh=dist.get('status')=='PASS' and dist.get('pass04_scene')=='PASS' and len(dist.get('archives',{}))==2 and all(
        a['implementation_sha256']==digest and sha(a['path'])==a['sha256'] for a in dist['archives'].values())
    mark([103],fresh and dist.get('missing_pass04_input_negative')=='PASS',['distribution-verification.json','distribution-pass-04-demo.log'])
    mark([104],fresh and dist.get('isolation',{}).get('violations')==[] and dist['isolation']['probes_passed'],
         ['independent isolated-process audit traces','explicit original-checkout/network/DNS/Git denial probes'])
    receipt_path=root/'development/modules/core-game/PASS_04_PROGRESS.json'
    receipt=json.loads(receipt_path.read_text()) if receipt_path.is_file() else {}
    archive_commit=dist.get('archives',{}).get('horizon',{}).get('source_commit')
    exact_receipt=(receipt.get('status') in ('IMPLEMENTATION_VALIDATED','PASS') and
        receipt.get('starting_sha')==START and receipt.get('main_sha')==MAIN and
        receipt.get('ending_sha')==receipt.get('remote_sha')==archive_commit and
        receipt.get('implementation_sha256')==digest and receipt.get('receipt_scope')=='VALIDATED_IMPLEMENTATION_AND_ARCHIVES')
    mark([105],ancestry and branch=='codex/raeon-pass-04' and remote and remote[0]==head and clean and main==MAIN and
         exact_receipt and (root/'development/modules/core-game/PASS_04_RECEIPT.md').is_file(),
         ['exact implementation start/end/remote/main SHA; live final HEAD/remote in this audit','PASS_04_RECEIPT.md','PASS_04_PROGRESS.json'])
    contract=json.loads((root/'data/game/pass-04-runtime.json').read_text())
    mark([106],contract['initial_active_player'] is None and not contract['automatic_refresh'] and len(contract['open_items'])>=8 and
         'test_pass_04_math.PrimeMath.test_open_scheduler_overflow_and_nonordinary_production_not_invented' in passed,
         ['pass-04-runtime.json','explicit OPEN policy regression'])
    accepted=json.loads((root/'data/manifests/accepted-state.json').read_text())
    mark([107],accepted['production']['phase']==decision['whole_game_phase']=='PREPRODUCTION',['accepted-state.json','raeon-pass-04.json'])
    mark([108],all(sha(p)==v for p,v in entry['preserved_tests'].items()) and host['risks'][0]['status']=='OPEN_QUALIFIED' and
         all(read(n).get('status')=='PASS' for n in ['acceptance.json','pass-02-acceptance.json','projection-correction-acceptance.json']),
         ['all 63 prior test/fixture hashes unchanged','74 runtime / 83 Pass-2 / 8 privacy','qualified host and OPEN scheduler'])
    result={'schema_version':1,'status':'PASS' if all(c['status']=='PASS' for c in cases.values()) else 'INCOMPLETE',
        'branch':branch,'starting_sha':START,'ending_sha':head,'remote_sha':remote[0] if remote else None,'main_sha':main,'clean':clean,
        'implementation_sha256':digest,'total':108,'passed':sum(c['status']=='PASS' for c in cases.values()),'cases':list(cases.values()),
        'pass03_reaudit':{k:p3.get(k) for k in ('passed','blocked','failed','total')},'pass03b':p3b.get('passed'),
        'tests':{n:read(n) for n in ['tests-unit.json','tests-integration.json','upstream-tests.json','repository-validation.json','verify.json']},
        'offline_distributions':dist.get('archives',{}),'qualification':environment,'open_items':contract['open_items'],
        'whole_game_phase':'PREPRODUCTION','native_devices':'NOT_RUN'}
    write(evidence/'pass-04-acceptance.json',result)
    return result
