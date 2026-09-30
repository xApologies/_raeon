"""Build and execution actions for genesis_runtime.py; no implicit success stubs."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def setup(root):
    for relative in ['game/core/genesis_horizon/bindings/python/src', 'platform/shared/python_hypervisor/src']:
        if 'python_hypervisor' not in relative or not os.environ.get('RAEON_HYPERVISOR_USE_INSTALLED'):
            sys.path.insert(0, str(root / relative))
    from raeon_genesis_horizon.toolchain import initialize
    return initialize(root)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf8')


def artifact_name(relative):
    return Path(relative).stem + '-' + hashlib.sha256(relative.encode()).hexdigest()[:12]


def build(root, output):
    _, upstream, _ = setup(root)
    from raeon_genesis_horizon.values import IntegerInterpreter
    integers = IntegerInterpreter(upstream, root / 'game/core/genesis_horizon/src/values')
    from raeon_genesis_horizon.toolchain import compile_paths
    from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import disassemble
    sources = [*sorted((root / 'game/core/genesis_horizon/src').glob('*.gen')),
               *sorted((root / 'tests/integration/genesis_horizon/application').glob('*.gen')),
               *sorted((root / 'game/core/raeon/application').glob('*.gen')),
               *sorted((root / 'tests/integration/genesis_horizon/pass_01_application').glob('*.gen')),
               *sorted((root / 'game/core/genesis_horizon/src/values').glob('*.gen'))]
    artifacts = {}
    for source in sources:
        relative = source.relative_to(root).as_posix()
        if source.parent.name == 'values':
            from genesis_control import disassemble as control_disassemble
            program = integers.programs[source.stem][0]
            bytecode = integers.encode(program)
            target = output / 'compiled' / artifact_name(relative)
            target.mkdir(parents=True, exist_ok=True)
            (target / 'program.gvm').write_bytes(bytecode)
            (target / 'program.asm').write_text(control_disassemble(program), encoding='utf8')
            write(target / 'receipt.json', {'profile': 'genesis-0.3.0', 'abi': 'typed-int-const-v1',
                                          'verification': integers.verify(program), 'input_registers': integers.programs[source.stem][1]})
            artifacts[relative] = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'bytecode_sha256': hashlib.sha256(bytecode).hexdigest(),
                'artifact_directory': artifact_name(relative), 'artifact_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.iterdir())}}
            continue
        result = compile_paths([source], root, source.stem)
        target = output / 'compiled' / artifact_name(relative)
        target.mkdir(parents=True, exist_ok=True)
        (target / 'program.gvm').write_bytes(result.link.bytecode)
        (target / 'program.asm').write_text(disassemble(result.link.program), encoding='utf8')
        write(target / 'lowered.json', result.modules)
        write(target / 'linked.json', result.link.gir)
        write(target / 'receipt.json', {'compiler': result.receipt, 'linker': result.link.receipt, 'proofs': result.link.proofs})
        artifacts[relative] = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'bytecode_sha256': result.receipt['gvm_sha256'],
                               'artifact_directory': artifact_name(relative), 'artifact_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.iterdir())}}
    write(output / 'evidence/build.json', {'status': 'PASS', 'artifacts': artifacts})
    return {'status': 'PASS', 'compiled_sources': len(sources), 'artifacts': artifacts}


def verify(root, output):
    first = build(root, output)
    from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import decode, verify as verify_bytecode
    for source in first['artifacts']:
        if '/src/values/' in source:
            from genesis_control import decode as control_decode, verify as control_verify
            control_verify(control_decode((output / 'compiled' / artifact_name(source) / 'program.gvm').read_bytes()))
            continue
        result = verify_bytecode(decode((output / 'compiled' / artifact_name(source) / 'program.gvm').read_bytes()))
        if not result['ok']:
            raise RuntimeError('Bytecode verification failed: ' + source)
    with tempfile.TemporaryDirectory(prefix='rebuild space ', dir=root / 'build') as temp:
        second = build(root, Path(temp))
        if first != second:
            raise RuntimeError('Nonreproducible build')
    write(output / 'evidence/verify.json', {'status': 'PASS', 'compiled_sources': len(first['artifacts']), 'deterministic_rebuild': True})
    return {'status': 'PASS', 'compiled_sources': len(first['artifacts']), 'deterministic_rebuild': True}


def demo(root, output):
    setup(root)
    sys.path.insert(0, str(root / 'tests/integration/genesis_horizon'))
    from support import Fixture, Port, port_decode
    start = time.perf_counter()
    f = Fixture('headless-reference-demo')
    try:
        port = Port()
        _, frames = f.send('HELLO', {'protocol': 2})
        for frame in frames:
            port.accept(frame)
        commits = []
        domains = f.horizon.domains()
        fabric_hash = hashlib.sha256(f.horizon._backend.fabric.path.read_bytes()).hexdigest()
        for i, operation in enumerate(['RELATE_A_B', 'TRANSFORM_A']):
            result, frames = f.send('INTENT', f.intent('demo-' + str(i), operation, i))
            if result['status'] != 'PROCESSED':
                raise RuntimeError(str(result))
            for frame in frames:
                port.accept(frame)
            commits.append(port.receipts[-1])
        retry = f.horizon.execute(f.intent('demo-1', 'TRANSFORM_A', 1), f.writer)
        if retry != commits[-1] or f.horizon._state['revision'] != 2:
            raise RuntimeError('Retry failed')
        if port.view != f.horizon._view(f.writer):
            raise RuntimeError('Port projection mismatch')
        checkpoint = f.horizon.checkpoint(f.writer)
        state_root = f.horizon._state['root']
        f.horizon.restore(checkpoint, f.writer)
        if f.horizon._state['root'] != state_root:
            raise RuntimeError('Restore root mismatch')
        result = {'status': 'PASS', 'runtime': 'actual compiled Genesis + native engines', 'domains': domains,
                  'semantic_revision': 2, 'semantic_root': state_root, 'commits': commits,
                  'road_receipts': f.horizon._backend.road_history, 'native_receipts': f.horizon._backend.native_receipts,
                  'fabric_unchanged': hashlib.sha256(f.horizon._backend.fabric.path.read_bytes()).hexdigest() == fabric_hash,
                  'projection_equal': True, 'restart_root_equal': True, 'host_elapsed_seconds': time.perf_counter() - start,
                  'performance_scope': 'single host observation, not native-device benchmark'}
        write(output / 'evidence/demo.json', result)
        return {key: value for key, value in result.items() if key not in ('road_receipts', 'native_receipts', 'commits')}
    finally:
        f.close()


def test(root, output):
    result = {}
    for name, folder in [('unit', 'tests/unit/hypervisor'), ('integration', 'tests/integration/genesis_horizon')]:
        script = '''import json,sys,unittest
from pathlib import Path
class Recorded(unittest.TextTestResult):
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.passed=[]
 def addSuccess(self,test): super().addSuccess(test); self.passed.append(test.id())
suite=unittest.defaultTestLoader.discover(sys.argv[1])
r=unittest.TextTestRunner(verbosity=2,resultclass=Recorded).run(suite)
Path(sys.argv[2]).write_text(json.dumps({'passed':r.passed,'run':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)},indent=2),encoding='utf8')
raise SystemExit(0 if r.wasSuccessful() else 1)
'''
        target = output / 'evidence' / ('tests-' + name + '.json')
        target.parent.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONPATH', None)
        completed = subprocess.run([sys.executable, '-B', '-c', script, folder, str(target)], cwd=root, env=env, capture_output=True, text=True, encoding='utf8')
        (target.with_suffix('.log')).write_text(completed.stdout + completed.stderr, encoding='utf8')
        print(completed.stderr, end='')
        if completed.returncode:
            raise RuntimeError(name + ' tests failed')
        result[name] = json.loads(target.read_text(encoding='utf8'))
    return result


def dialect_test(root, upstream, output):
    programs = {
        'system-io': (upstream / 'language/17 System I-O & BLACKGLASS-BRANE Interface/12_REFERENCE_IMPLEMENTATION', '''
from pathlib import Path
import tempfile,json
from genesis_system_io import compile_source,SystemRuntime
example=Path('language/17 System I-O & BLACKGLASS-BRANE Interface/15_EXAMPLES/01_SOURCE_READ.gen')
p=compile_source(example.read_text(encoding='utf8'),example.as_posix())
with tempfile.TemporaryDirectory() as d:
 r=SystemRuntime(p,Path(d));r.seed('source','input.bin',b'pinned-system-io');result=r.run();assert result.status=='CLOSED'
mixed=Path('language/10 Genesis Surface Language/16_EXAMPLES/RAINBOW_ROAD.gen').read_text(encoding='utf8').replace('genesis 0.1.0','genesis 0.6.0')
try:compile_source(mixed,'unsupported-mixed.gen')
except Exception as error:print(json.dumps({'positive':'CLOSED','mixed_rejected':True,'diagnostic':str(error)}))
else:raise RuntimeError('Mixed dialect falsely accepted')
'''),
        'callables': (upstream / 'language/13 Callable Abstractions, Functions & Generics/12_REFERENCE_IMPLEMENTATION', '''
from pathlib import Path
import json
from genesis_packages.registry import LocalRegistry
from genesis_callable_packages import CallablePackageRuntime
sec=Path('language/13 Callable Abstractions, Functions & Generics')
b=CallablePackageRuntime(LocalRegistry(sec/'17_STANDARD_LIBRARY/REGISTRY')).build(sec/'16_EXAMPLES/PROJECTS/NESTED_CALLABLE')
assert b.execution.receipt['payload']['verified'];print(json.dumps(b.receipt))
'''),
    }
    records = {}
    for name, (implementation, script) in programs.items():
        env = dict(os.environ, PYTHONPATH=str(implementation), PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
        completed = subprocess.run([sys.executable, '-B', '-c', script], cwd=upstream, env=env, capture_output=True, text=True, encoding='utf8')
        write(output / ('evidence/dialect-' + name + '.json'), {'exit_code': completed.returncode, 'stdout': completed.stdout, 'stderr': completed.stderr})
        if completed.returncode:
            raise RuntimeError(name + ': ' + completed.stderr)
        records[name] = json.loads(completed.stdout)
    write(output / 'evidence/dialects.json', {'status': 'PASS', 'records': records})
    return records
