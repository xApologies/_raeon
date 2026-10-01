"""Checked per-case process isolation for the pinned native Python reference.

Discovery, assertions and denominators are unchanged. A crash, missing receipt,
skip, wrong test identity or nonzero child exit is a failure, never a PASS.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT=Path(__file__).resolve().parents[1]


def flatten(suite):
    for test in suite:
        if isinstance(test,unittest.TestSuite):yield from flatten(test)
        else:yield test.id()


def run_case(folder, identity, output):
    sys.path.insert(0,str((ROOT/folder).resolve()))
    class Recorded(unittest.TextTestResult):
        def __init__(self,*a,**kw):super().__init__(*a,**kw);self.passed=[]
        def addSuccess(self,test):super().addSuccess(test);self.passed.append(test.id())
    suite=unittest.defaultTestLoader.loadTestsFromName(identity)
    result=unittest.TextTestRunner(verbosity=2,resultclass=Recorded).run(suite)
    record={'run':result.testsRun,'passed':result.passed,'failures':len(result.failures),
            'errors':len(result.errors),'skipped':len(result.skipped)}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf8')
    return 0 if result.wasSuccessful() and result.testsRun==1 and result.passed==[identity] and not result.skipped else 1


def run_suite(root, folder, output):
    """Execute every discovered case and retain each independent process result."""
    root=Path(root);output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONFAULTHANDLER='1')
    env.pop('PYTHONPATH',None)
    worker=root/'tools/genesis_runtime_test_worker.py'
    discovery=subprocess.run([sys.executable,'-B',str(worker),'discover',folder],cwd=root,env=env,
                             capture_output=True,text=True,encoding='utf8')
    if discovery.returncode:raise RuntimeError('Test discovery failed: '+discovery.stderr)
    identifiers=json.loads(discovery.stdout)
    if not identifiers or len(set(identifiers))!=len(identifiers):
        raise RuntimeError('Empty or duplicate test discovery')
    records=[];passed=[];failures=0;logs=[]
    directory=output.parent/(output.stem+'-cases');directory.mkdir(exist_ok=True)
    for index,identity in enumerate(identifiers):
        report=directory/(str(index).zfill(3)+'.json')
        report.unlink(missing_ok=True)
        child=subprocess.run([sys.executable,'-B',str(worker),'case',folder,identity,str(report)],
                             cwd=root,env=env,capture_output=True,text=True,encoding='utf8',errors='replace')
        log=child.stdout+child.stderr
        logs.append(log)
        (directory/(str(index).zfill(3)+'.log')).write_text(log,encoding='utf8')
        record=json.loads(report.read_text(encoding='utf8')) if report.is_file() else {}
        ok=child.returncode==0 and record=={'run':1,'passed':[identity],'failures':0,'errors':0,'skipped':0}
        if ok:passed.append(identity)
        else:failures+=1
        records.append({'test':identity,'process_exit_code':child.returncode,'status':'PASS' if ok else 'FAIL'})
        print(f'{index+1}/{len(identifiers)} {identity}: '+('PASS' if ok else 'FAIL'),flush=True)
        if not ok:print(log,flush=True)
    result={'run':len(identifiers),'passed':passed,'failures':failures,'errors':0,
            'discovered':identifiers,'process_isolation':True,'processes':records}
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    output.with_suffix('.log').write_text('\n'.join(logs),encoding='utf8')
    if failures:raise RuntimeError(f'{failures} isolated test cases failed; no cases omitted')
    return result


if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='discover':
        print(json.dumps(list(flatten(unittest.defaultTestLoader.discover(sys.argv[2])))))
    elif mode=='case':
        raise SystemExit(run_case(sys.argv[2],sys.argv[3],Path(sys.argv[4])))
    elif mode=='suite':
        run_suite(ROOT,sys.argv[2],Path(sys.argv[3]))
    else:raise ValueError('Unknown test worker mode')
