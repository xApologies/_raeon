"""Pass-05 actual scene and exhaustive 140-case evidence audit."""
import copy
import hashlib
import json
import subprocess
import sys

from genesis_runtime_tasks import setup,write
from genesis_runtime_distribution import implementation_digest

START='63771ab37dfec9a0c9de907c60f6f8b2f7a3f670'
MAIN='69a0030805b8c3858c877a514e2f50644421115a'
POUCH='d0c8a763eb0a4901a118611742a8abfd0075227f4f0ad1b3bba4784eead8830a'
SPEC='provenance/imports/raeon-pass-05/handoff/PASS_05_ACCEPTANCE.json'
TESTS={
 'test_setup_hand_draw_compensation_capacity_and_privacy':list(range(11,27))+[126,128],
 'test_nodes_turn_boundaries_partial_repeat_and_current_carryover':[27,28,29,30,31,32,33,34,35,36,39,40,63,64,65,66,68,69,70,71,72,79,80,81,85,86,87,88,89,90,91,96,129],
 'test_defense_stored_sources_pass_timeout_compound_rollback_and_destruction':[37,38,41,42,46,47,48,49,50,51,52,53,54,56,57,59,60,125,127,130],
 'test_field_origin_defense_health_first_and_degrade_mediator_guard':[45,58,61,62,73,77,78,82,83,84],
 'test_zero_cost_utilities_require_hand_timing_target_and_white_exactness':[55,95,97,98,99,100,102],
 'test_three_inactive_terminal_before_defense_and_no_later_gameplay':[43,44,74,104,105,106,107,108,109,110,111],
 'test_real_pass04_checkpoint_upgrade_and_canonical_migration':[92,93,94],
 'test_exhaustion_actual_empty_deck_six_stages_and_open_seventh':list(range(112,121)),
 'test_current_checkpoint_restart_replay_defense_order_and_road_history':[121,122,123,124],
 'test_current_genesis_admission_closure_and_road_cannot_be_bypassed':[9,10,101],
 'test_current_zero_retirement_selective_emergence_and_open_guards':[131],
}
VALUE_TESTS={'test_native_integer_no_node_cap_and_exact_canonical_encoding':[67],
             'test_negative_node_invariants_and_legacy_charge_rejected':[75,76]}

# Exact user-authorized pointer additions, not permission to rewrite these trees.
# The legacy payloads and every FG/QMO/mathematics source remain protected.
AUTHORITY_POINTER_HASHES={
 'data/cycles/cycle_01/primes/working-model.json':('5f2d6ab23fe76d0193bc1185dc401412a8db3cd2781d0d6048c1b69792baf82b','76ea4c6e9c9f2fafb00d41a55eca5481eb7f65d0a3745dfdd80c4f6849059abb'),
 'data/cycles/cycle_01/utilities/overview.json':('884c0f4ccb7f4ff35d3811cf6b7a728012436e96c075e9a6c86b35f5344328e7','ab6dcbd7ce2b735d36ab8b3a237554f89ed6e318026cafbb20ebff1a1b1359f3'),
 'design/cards/cycle_01/utilities/SYSTEM.md':('792866932e52d4e892537f23a946c6a70ae1ad9e22b5661378d533e973a2b5fc','885b0144e66540ef3b6fcd8b2f4ec6bfa7f78c84c2dccf89ed0d2e2233a01006'),
 'design/game/board/SYSTEM.md':('7131cb473e21ade6fce55b772ae6274cf86103d91828aa283229aab95f87fe1f','6a8999ecc09a95d6d3cd7f502c1270493d9a1f4b9f1cbaa4952f88bdf9a6d986'),
 'design/game/match/SYSTEM.md':('80d282e5a204df03b412a360266eb9a7e99114cc79cc15b3d383b4b91a068419','0ce29a259004912255a2c4a401eae47bfcb9b0af65ded072cf77cba368751051'),
}


def approved_authority_pointer(path,before_sha256,after_sha256):
    return AUTHORITY_POINTER_HASHES.get(path)==(before_sha256,after_sha256)


def protected_sources_preserved(root,baseline,changed,prefixes):
    protected=[p for p in changed if p.startswith(prefixes)]
    if not protected:return True
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
    if not successor(root,branch):return False
    pouch=root/'provenance/imports/raeon-pass-05/RAEON_DIPLOMATIC_POUCH_PASS_05_2026-10-01.zip'
    if hashlib.sha256(pouch.read_bytes()).hexdigest()!=POUCH:return False
    for path in protected:
        if path not in AUTHORITY_POINTER_HASHES:return False
        before=subprocess.check_output(['git','show',baseline+':'+path],cwd=root)
        after=(root/path).read_bytes()
        if not approved_authority_pointer(path,hashlib.sha256(before).hexdigest(),hashlib.sha256(after).hexdigest()):return False
    return True


def successor(root,branch):
    if branch=='codex/raeon-pass-06':
        from genesis_runtime_pass06 import successor as pass06_successor
        if not pass06_successor(root,branch):return False
        branch='codex/raeon-pass-05'
    if branch!='codex/raeon-pass-05':return False
    entry=root/'provenance/imports/raeon-pass-05/entry.json'
    if not entry.is_file():return False
    value=json.loads(entry.read_text(encoding='utf8'))
    return (value.get('status')=='PASS' and value.get('before_implementation') is True and value.get('starting_sha')==START and
            value.get('results',{}).get('pass-04-acceptance.json',{}).get('passed')==108 and
            subprocess.run(['git','merge-base','--is-ancestor',START,'HEAD'],cwd=root,stdout=subprocess.DEVNULL).returncode==0)


def demo(root,output):
    setup(root);sys.path.insert(0,str(root/'tests/integration/genesis_horizon'))
    from pass_05_support import MatchFixture
    from genesis_runtime_pass04 import qualification
    f=MatchFixture('pass05-offline-scene')
    try:
        (prime,),fields=f.setup_player(primes=['restore_yellow'],manifolds=['M-G-01','M-G-02'])
        f.setup_player('player_2');f.setup();f.start()
        for field in fields:f.generate(field,prime)
        p=f.color.state['primes'][prime]
        assert (p['H'],p['N'],p['R'],f.q(prime))==(3,2,2,8)
        f.control('END_ACTIVE');f.control('ADVANCE_TURN')
        assert all(f.ext.state['fields'][i]['availability']=='USED' for i in fields)
        values=copy.deepcopy(f.horizon._backend.application_values)
        result=f.restart();assert f.horizon._backend.application_values==values
        record={'status':'PASS','implementation_sha256':implementation_digest(root),'prime':p,
                'turn':values['match_tempo'],'restart':result,'qualification':qualification(),
                'road_count':len(f.horizon._backend.road_history),'whole_game_phase':'PREPRODUCTION'}
        write(output/'evidence/pass-05-demo.json',record)
        return {k:record[k] for k in ('status','prime','road_count','qualification','whole_game_phase')}
    finally:f.close()


def audit(root,output):
    from genesis_runtime_pass04 import qualification
    evidence=output/'evidence'
    def read(name):
        p=evidence/name
        return json.loads(p.read_text(encoding='utf8')) if p.is_file() else {}
    def data(name):return json.loads((root/name).read_text(encoding='utf8'))
    def sha(name):return hashlib.sha256((root/name).read_bytes()).hexdigest()
    def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
    spec=data(SPEC);cases={row['id']:dict(copy.deepcopy(row),status='NOT_RUN',evidence=[]) for row in spec['cases']}
    assert len(cases)==spec['total']==140
    implementation=implementation_digest(root)
    current=read('tests-source.json')=={'status':'PASS','implementation_sha256':implementation}
    tests=read('tests-integration.json')
    passed=tests.get('passed',[]) if current and tests.get('failures')==tests.get('errors')==0 else []
    def mark(numbers,condition,records):
        for n in numbers:cases[f'P5-{n:03}'].update(status='PASS' if condition else 'FAIL',evidence=records)
    for name,numbers in TESTS.items():
        identity='test_pass_05.Pass05.'+name
        mark(numbers,identity in passed,[identity,'tests-integration.json','tests-source.json'])
    for name,numbers in VALUE_TESTS.items():
        identity='test_pass_05_values.NodeValues.'+name
        mark(numbers,identity in passed and 'test_pass_05.Pass05.test_nodes_turn_boundaries_partial_repeat_and_current_carryover' in passed,
             [identity,'actual native charge-node gameplay','tests-integration.json','tests-source.json'])
    entry=data('provenance/imports/raeon-pass-05/entry.json')
    decision=data('provenance/decisions/raeon-pass-05.json')
    branch,head=git('branch','--show-current'),git('rev-parse','HEAD')
    remote=git('ls-remote','origin','refs/heads/'+branch).split()
    main=git('ls-remote','origin','refs/heads/main').split()[0]
    clean=not git('status','--porcelain')
    ancestry=successor(root,branch)
    mark([1],ancestry,['exact sealed ancestor','entry.json','fresh complete inherited gate before implementation'])
    mark([2],entry['results']['pass-04-acceptance.json']['passed']==108 and all(sha(p)==v for p,v in decision['sealed_receipts'].items()),
         ['sealed Pass-04 receipts byte-identical','fresh 108/108 entry audit'])
    mark([3],main==MAIN and git('rev-parse','main')==MAIN,['local and remote main SHA'])
    mark([4],read('upstream-readonly.json').get('status')=='PASS',['upstream-readonly.json'])
    mark([5],all(sha(p)==v for p,v in decision['qmo_sources'].items()),['eleven unchanged original QMO source hashes'])
    mark([6],read('projection-correction-acceptance.json').get('passed')==8,['all eight original privacy regressions'])
    mark([7],all(sha(p)==v for p,v in entry['preserved_tests'].items()),['67 inherited test/fixture hashes unchanged'])
    host=data('development/modules/core-game/HOST_RUNTIME_RISKS.json');environment=qualification()
    mark([8],host['risks'][0]['status']=='OPEN_QUALIFIED' and environment['python']=='3.12.10' and environment['processor_mask']==65536,
         ['HOST_RUNTIME_RISKS.json','current qualified process'])
    catalog=data('game/core/raeon/application/catalog.json')['records']
    mark([103],len(catalog)==185 and sum(r['category']=='Utility' for r in catalog.values())==51 and
         sha('game/core/raeon/application/catalog.json')==decision['catalog_sha256'],['unchanged source-derived 185-record / 51-Utility catalog'])
    dist=read('distribution-verification.json')
    fresh=(dist.get('status')=='PASS' and dist.get('pass05_scene')=='PASS' and dist.get('missing_pass05_input_negative')=='PASS' and
           len(dist.get('archives',{}))==2 and all(a['implementation_sha256']==implementation and sha(a['path'])==a['sha256'] for a in dist['archives'].values()))
    mark([132],fresh and dist.get('isolation',{}).get('violations')==[] and dist.get('isolation',{}).get('probes_passed') is True,
         ['distribution-verification.json','self-contained migration fixture','fresh extraction / Git-network-original-checkout denial probes'])
    repo=read('repository-validation.json');verify=read('verify.json');build=read('build.json').get('artifacts',{})
    original=entry['compiled_sources']
    original_preserved=len(original)==46 and all(all(build.get(p,{}).get(k)==v[k] for k in ('source_sha256','bytecode_sha256')) for p,v in original.items())
    inherited=all(read(name).get('status')=='PASS' and read(name).get('passed')==count for name,count in [
        ('acceptance.json',74),('pass-02-acceptance.json',83),('projection-correction-acceptance.json',8),
        ('pass-03-acceptance.json',98),('pass-03b-acceptance.json',85),('pass-04-acceptance.json',108)])
    expected_compiled,expected_tests=60,136
    if branch=='codex/raeon-pass-06' and ancestry:
        following=data('provenance/decisions/raeon-pass-06.json')
        expected_compiled,expected_tests=following['compiled_total'],following['integration_total']
        preserved=data('provenance/imports/raeon-pass-06/entry.json')['compiled_sources']
        original_preserved=original_preserved and len(preserved)==60 and all(all(build.get(p,{}).get(k)==v[k] for k in ('source_sha256','bytecode_sha256')) for p,v in preserved.items())
    mark([133],current and inherited and original_preserved and repo.get('status')=='PASS' and repo.get('implementation_sha256')==implementation and
         verify.get('deterministic_rebuild') is True and verify.get('compiled_sources')==expected_compiled and read('upstream-tests.json').get('status')=='PASS' and
         read('tests-unit.json').get('run')==6 and read('tests-unit.json').get('failures')==read('tests-unit.json').get('errors')==0 and
         tests.get('run')==len(passed)==len(tests.get('discovered',[]))==expected_tests and all(p['status']=='PASS' and p['process_exit_code']==0 for p in tests.get('processes',[])),
         ['all inherited denominators unchanged','all discovered native cases executed','repository / compiler / dialect / upstream evidence'])
    mark([135],current and (root/'development/modules/core-game/PASS_05_RECEIPT.md').is_file() and
         all(row['evidence'] for key,row in cases.items() if row['status']=='PASS'),['source-bound execution receipts; absent or failed cases never promoted'])
    contract=data('data/game/pass-05-runtime.json');open_items=data('provenance/imports/raeon-pass-05/handoff/OPEN_ITEMS.json')['open']
    mark([136],contract['open_items']==decision['open_items']==open_items and len(open_items)==16,
         ['all sixteen original OPEN items emitted; actual refusal tests mapped above'])
    changed=git('diff','--name-only',START,'HEAD').splitlines()
    inventory=data('data/manifests/current-files.json')['files']
    hashes={p:sha(p) for p in changed if (root/p).is_file()}
    mark([137],bool(changed) and set(changed)<=set(inventory) and len(hashes)==len(changed),['complete sealed-base-to-HEAD changed-file inventory and SHA256 map'])
    mark([138],entry['pouch_sha256']==POUCH and sha('provenance/imports/raeon-pass-05/RAEON_DIPLOMATIC_POUCH_PASS_05_2026-10-01.zip')==POUCH and current,
         ['pouch SHA256','current implementation digest','changed-file SHA256 map'])
    mark([139],ancestry and clean and bool(remote) and remote[0]==head and main==MAIN,['exact branch / local HEAD / remote SHA / clean status'])
    mark([140],data('data/manifests/accepted-state.json')['production']['phase']==decision['whole_game_phase']=='PREPRODUCTION',
         ['accepted-state.json','unchanged module gates'])
    mark([134],len(cases)==140 and all(row['status']!='NOT_RUN' for key,row in cases.items() if key!='P5-134'),
         ['all 140 mandatory IDs accounted with explicit execution or guard evidence'])
    result={'schema_version':1,'status':'PASS' if all(c['status']=='PASS' for c in cases.values()) else 'INCOMPLETE',
        'branch':branch,'base_sha':START,'ending_sha':head,'remote_sha':remote[0] if remote else None,'main_sha':main,'clean':clean,
        'implementation_sha256':implementation,'total':140,'passed':sum(c['status']=='PASS' for c in cases.values()),
        'failed':sum(c['status']=='FAIL' for c in cases.values()),'blocked':sum(c['status']=='NOT_RUN' for c in cases.values()),
        'cases':list(cases.values()),'changed_files':changed,'changed_file_sha256':hashes,'pouch_sha256':POUCH,
        'tests':{n:read(n) for n in ('tests-unit.json','tests-integration.json','upstream-tests.json','repository-validation.json','verify.json')},
        'offline_distributions':dist.get('archives',{}),'open_items':open_items,'qualification':environment,
        'HOST-RUNTIME-001':'OPEN_QUALIFIED','whole_game_phase':'PREPRODUCTION','native_devices':'NOT_RUN'}
    write(evidence/'pass-05-acceptance.json',result)
    return result
