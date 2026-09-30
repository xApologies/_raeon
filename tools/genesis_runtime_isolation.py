"""Independent offline verification interceptor for trusted reference Python runs.

Installed as sitecustomize in the fresh verification venv. Denies socket/DNS,
shell/Git and non-Python child processes; confines Python-audited file accesses
to the extraction and declared interpreter/OS prerequisites. This is not an
OS sandbox for malicious native extensions; pinned engines are trusted code.
"""
import json
import os
from pathlib import Path
import sys

_probe = False
_installed = False


def install():
    global _installed
    if _installed:
        return
    root = Path(os.environ['RAEON_ISOLATION_ROOT']).resolve()
    prerequisite = Path(sys.base_prefix).resolve()
    os_root = Path(os.environ.get('SystemRoot', 'C:/Windows')).resolve()
    allowed = [root, prerequisite, os_root]
    traces = root / 'isolation traces'
    traces.mkdir(exist_ok=True)
    descriptor = os.open(traces / (str(os.getpid()) + '.jsonl'), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    def record(event, target, denied):
        data = {'event': event, 'target': str(target), 'denied': denied, 'probe': _probe}
        os.write(descriptor, (json.dumps(data) + '\n').encode())
    def confined(value):
        if isinstance(value, int) or value is None or str(value).lower() in {'nul', 'nul:', os.devnull.lower()}:
            return True
        path = Path(os.path.abspath(os.fsdecode(value)))
        return any(path.is_relative_to(base) for base in allowed)
    def audit(event, args):
        target, denied = None, False
        if event.startswith('socket.'):
            target, denied = event, True
        elif event in {'os.system', 'os.exec', 'os.posix_spawn'}:
            target, denied = args[0], True
        elif event == 'subprocess.Popen':
            target = args[0] or args[1][0]
            executable = Path(target)
            denied = executable.name.lower() not in {'python.exe', 'pythonw.exe', 'python', 'python3'} or not executable.is_absolute() or not confined(executable)
        elif event in {'open', 'os.listdir', 'os.scandir'}:
            target = args[0]
            denied = not confined(target)
        if target is not None:
            record(event, target, denied)
            if denied:
                raise PermissionError('OFFLINE_ISOLATION_DENIED: ' + event)
    sys.addaudithook(audit)
    _installed = True


def probes():
    global _probe
    import socket
    import subprocess
    _probe = True
    checks = {}
    for name, action in {
        'network_socket': lambda: socket.socket(),
        'network_dns': lambda: socket.getaddrinfo('example.com', 443),
        'git': lambda: subprocess.run(['git', '--version'], check=True),
        'external_checkout': lambda: Path(os.environ['RAEON_FORBIDDEN_CHECKOUT']).joinpath('README.md').read_bytes(),
    }.items():
        try:
            action()
        except PermissionError:
            checks[name] = True
        else:
            checks[name] = False
    _probe = False
    assert all(checks.values()), checks
    print(json.dumps(checks))
