"""Pass-06 real headless scenes and 108 mandatory source-bound acceptance cases."""
import copy
import hashlib
import json
import subprocess
import sys

from genesis_runtime_tasks import setup,write
from genesis_runtime_distribution import implementation_digest

START='388a241ba5674c157131601aad677ab52350f2c6'
MAIN='69a0030805b8c3858c877a514e2f50644421115a'
POUCH='1cdc6a070c3492f791a37166bb55ae3b88ce5b03ae7ae1228f72bba8fe977242'
IMPORT='provenance/imports/raeon-pass-06/'
TESTS={
 'test_mulligan_zero_seven_repeat_replay_and_privacy':list(range(10,18)),
 'test_draw_capacity_order_and_compensation_own_active_single_use':list(range(18,30)),
 'test_complete_prime_match_deterministic_replay_restart_and_terminal':[32,90,91,93,94,95,96,99],
 'test_complete_exhaustion_match_stages_order_defense_and_terminal':list(range(33,49))+[92],
 'test_transduction_restore_six_native_amounts':[50],
 'test_transduction_degrade_six_native_amounts_and_zero_cost':[51],
 'test_transduction_universal_six_both_resolution_choices':[52,53],
 'test_draw_deck_survey_selection_open_boundary_exchange_and_deep_survey':[56,57,59,60,62,64,66,67],
 'test_selection_unordered_bottom_cannot_be_drawn_or_observed_inventedly':[61],
 'test_short_deck_effects_and_unresolved_selection_order_guard':[63,65],
 'test_recovery_six_effects_capacity_identity_topology_and_prime_refusal':list(range(68,77)),
 'test_reserved_activation_seven_nonadmitted':[83],
 'test_reserved_sandbox_six_nonadmitted':[84],
 'test_reserved_stability_six_nonadmitted':[85,86,87],
 'test_white_reactivation_identity_own_active_and_open_guards':[30,49,54,55,77,78,79,80,81,82,89,103],
 'test_defense_rollback_restart_timeout_privacy_and_configuration':[88,97,98],
 'test_simultaneous_consequence_boundary_draw_native_candidate':[31],
}


def successor(root,branch):
    if branch!='codex/raeon-pass-06':return False
    path=root/IMPORT/'entry.json'
    if not path.is_file():return False
    entry=json.loads(path.read_text(encoding='utf8'))
    pouch=root/IMPORT/'RAEON_DIPLOMATIC_POUCH_PASS_06_2026-10-03.zip'
    return (entry.get('status')=='PASS' and entry.get('before_implementation') is True and entry.get('starting_sha')==START and
        entry.get('pouch_sha256')==POUCH and pouch.is_file() and hashlib.sha256(pouch.read_bytes()).hexdigest()==POUCH and
        entry.get('results',{}).get('pass-05-acceptance.json',{}).get('passed')==140 and
        subprocess.run(['git','merge-base','--is-ancestor',START,'HEAD'],cwd=root,stdout=subprocess.DEVNULL).returncode==0)


def demo(root,output):
    setup(root);sys.path.insert(0,str(root/'tests/integration/genesis_horizon'))
    from pass_06_support import HeadlessFixture
    from pass_06_matches import prime_match,exhaustion_match
    from genesis_runtime_pass04 import qualification
    scenes={}
    for name,story in [('prime',prime_match),('exhaustion',exhaustion_match)]:
        f=HeadlessFixture('pass06-complete-'+name)
        try:scenes[name]=story(f)
        finally:f.close()
    record={'status':'PASS','implementation_sha256':implementation_digest(root),'scenes':scenes,
            'qualification':qualification(),'whole_game_phase':'PREPRODUCTION'}
    write(output/'evidence/pass-06-demo.json',record)
    return {'status':'PASS','endings':list(scenes),'road_counts':{n:s['road_count'] for n,s in scenes.items()},
            'qualification':record['qualification'],'whole_game_phase':'PREPRODUCTION'}


def audit(root,output):
    from genesis_runtime_pass04 import qualification
    def data(path):return json.loads((root/path).read_text(encoding='utf8'))
    def read(name):
        path=output/'evidence'/name
        return json.loads(path.read_text(encoding='utf8')) if path.is_file() else {}
    def sha(path):return hashlib.sha256((root/path).read_bytes()).hexdigest()
    def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
    spec=data(IMPORT+'handoff/PASS_06_ACCEPTANCE.json')
    cases={row['id']:dict(copy.deepcopy(row),status='NOT_RUN',evidence=[]) for row in spec['cases']}
    assert len(cases)==spec['total']==108
    implementation=implementation_digest(root)
    current=read('tests-source.json')=={'status':'PASS','implementation_sha256':implementation}
    tests=read('tests-integration.json')
    passed=tests.get('passed',[]) if current and tests.get('failures')==tests.get('errors')==0 else []
    def mark(numbers,okay,evidence):
        for n in numbers:cases[f'P6-{n:03}'].update(status='PASS' if okay else 'FAIL',evidence=evidence)
    for name,numbers in TESTS.items():
        identity='test_pass_06.Pass06.'+name
        mark(numbers,identity in passed,[identity,'tests-integration.json','tests-source.json'])
    mark([58], 'test_pass_06.Pass06.test_draw_capacity_order_and_compensation_own_active_single_use' in passed,
         ['actual 8+Draw3 transfers two; full Hand transfers zero; preserved Deck order'])
    entry=data(IMPORT+'entry.json');decision=data('provenance/decisions/raeon-pass-06.json')
    branch=git('branch','--show-current');head=git('rev-parse','HEAD');remote=git('ls-remote','origin','refs/heads/'+branch).split()
    main=git('ls-remote','origin','refs/heads/main').split()[0];clean=not git('status','--porcelain')
    ancestry=successor(root,branch)
    mark([1],ancestry and entry['remote_sha']==START,['entry.json','sealed base and fetched predecessor branch','Git ancestor'])
    mark([2],read('pass-05-acceptance.json').get('passed')==140 and read('pass-05-acceptance.json').get('status')=='PASS' and
         all(sha(p)==v for p,v in entry['sealed_receipts'].items()),['fresh inherited 140/140 audit','sealed Pass05 receipts unchanged'])
    mark([3],all(sha(p)==v for p,v in decision['qmo_sources'].items()),['unchanged original QMO SHA256 map'])
    mark([4],read('projection-correction-acceptance.json').get('passed')==8,['all eight original projection privacy cases'])
    mark([5],read('upstream-readonly.json').get('status')=='PASS',['clean pinned _bricked read-only comparison'])
    security='test_pass_06_security.Pass06Security.test_compiled_admission_closure_and_road_are_required'
    mark([6,7],security in passed,['compiled admission/closure mutation and Road bypass rejections',security])
    host=data('development/modules/core-game/HOST_RUNTIME_RISKS.json');environment=qualification()
    mark([8],host['risks'][0]['status']=='OPEN_QUALIFIED' and environment['python']=='3.12.10' and environment['processor_mask']==65536,
         ['HOST-RUNTIME-001 preserved','actual qualified host process'])
    mark([9],main==git('rev-parse','main')==MAIN,['local and remote main unchanged'])
    dist=read('distribution-verification.json')
    fresh=(dist.get('status')=='PASS' and dist.get('pass06_scene')=='PASS' and dist.get('missing_pass06_input_negative')=='PASS' and
        len(dist.get('archives',{}))==2 and all(r['implementation_sha256']==implementation and sha(r['path'])==r['sha256'] for r in dist['archives'].values()))
    mark([100],fresh and dist.get('isolation',{}).get('violations')==[] and dist.get('isolation',{}).get('probes_passed') is True,
         ['fresh offline extraction','all inherited and Pass06 native suites','both complete endings','independent isolation probes and audit traces'])
    prior={'acceptance.json':74,'pass-02-acceptance.json':83,'projection-correction-acceptance.json':8,'pass-03-acceptance.json':98,
           'pass-03b-acceptance.json':85,'pass-04-acceptance.json':108,'pass-05-acceptance.json':140}
    inherited=all(read(n).get('status')=='PASS' and read(n).get('passed')==c for n,c in prior.items())
    build=read('build.json').get('artifacts',{});original=entry['compiled_sources']
    unchanged=len(original)==60 and all(all(build.get(p,{}).get(k)==v[k] for k in ('source_sha256','bytecode_sha256')) for p,v in original.items())
    repo=read('repository-validation.json');verify=read('verify.json')
    suites=(current and tests.get('run')==len(passed)==len(tests.get('discovered',[]))==decision['integration_total'] and
        all(r['status']=='PASS' and r['process_exit_code']==0 for r in tests.get('processes',[])) and
        read('tests-unit.json').get('run')==6 and read('tests-unit.json').get('failures')==read('tests-unit.json').get('errors')==0 and
        read('upstream-tests.json').get('status')=='PASS' and read('dialects.json').get('status')=='PASS')
    mark([101],suites and inherited and unchanged and all(sha(p)==v for p,v in entry['preserved_tests'].items()) and
        repo.get('status')=='PASS' and repo.get('implementation_sha256')==implementation and
        verify.get('deterministic_rebuild') is True and verify.get('compiled_sources')==decision['compiled_total'],
        ['all discovered suites actually rerun','all inherited test/fixture bytes unchanged','60 inherited compiler commitments unchanged','repository/dialect/upstream evidence'])
    changed=git('diff','--name-only',START,'HEAD').splitlines();hashes={p:sha(p) for p in changed if (root/p).is_file()}
    inventory=data('data/manifests/current-files.json')['files']
    mark([104],bool(changed) and set(changed)<=set(inventory) and len(changed)==len(hashes),['exact sealed-base-to-HEAD changed-file list and SHA256 map'])
    mark([105],entry['pouch_sha256']==POUCH and sha(IMPORT+'RAEON_DIPLOMATIC_POUCH_PASS_06_2026-10-03.zip')==POUCH and current,
         ['pouch manifest/hashes','current executable/authority digest','changed-file hashes'])
    mark([106],ancestry and clean and bool(remote) and remote[0]==head,['exact branch / final SHA / remote SHA / clean tree'])
    mark([107],data('data/manifests/accepted-state.json')['production']['phase']==decision['whole_game_phase']=='PREPRODUCTION',
         ['accepted-state.json','unchanged unaccepted module gates'])
    mark([108],decision['pass07_implemented'] is False and all('pass-07' not in p.lower() and 'telemetry' not in p.lower() for p in changed),
         ['Pass07 explicitly deferred','exact changed-file inventory'])
    mark([102],all(c['status']!='NOT_RUN' for k,c in cases.items() if k!='P6-102') and
         (root/'development/modules/core-game/PASS_06_RECEIPT.md').is_file(),['108 mandatory IDs accounted with actual executed evidence or preserved OPEN guard'])
    result={'schema_version':1,'status':'PASS' if all(c['status']=='PASS' for c in cases.values()) else 'INCOMPLETE',
      'branch':branch,'base_sha':START,'ending_sha':head,'remote_sha':remote[0] if remote else None,'main_sha':main,'clean':clean,
      'implementation_sha256':implementation,'total':108,'passed':sum(c['status']=='PASS' for c in cases.values()),
      'failed':sum(c['status']=='FAIL' for c in cases.values()),'blocked':sum(c['status']=='NOT_RUN' for c in cases.values()),
      'cases':list(cases.values()),'changed_files':changed,'changed_file_sha256':hashes,'pouch_sha256':POUCH,
      'tests':{n:read(n) for n in ('tests-unit.json','tests-integration.json','upstream-tests.json','repository-validation.json','verify.json')},
      'offline_distributions':dist.get('archives',{}),'open_items':data(IMPORT+'handoff/OPEN_ITEMS.json')['open'],
      'qualification':environment,'HOST-RUNTIME-001':'OPEN_QUALIFIED','whole_game_phase':'PREPRODUCTION','native_devices':'NOT_RUN',
      'simultaneous_fixture_scope':'controlled native consequence boundary; no invented public tie-causing action',
      'utility_disposition':'inherited unspecified; no generic post-effect consumption invented'}
    write(output/'evidence/pass-06-acceptance.json',result)
    return result
