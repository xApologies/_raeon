import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from genesis_runtime_distribution import check_archive


class ArchiveIntegrityTests(unittest.TestCase):
    def test_exact_manifest_and_negative_cases(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'build') as directory:
            archive = Path(directory) / 'fixture.zip'
            payload = b'verified source'
            manifest = {'source_commit': 'fixture', 'files': {'src/a.py': {'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}}}
            def write(entries):
                with zipfile.ZipFile(archive, 'w') as z:
                    z.writestr('manifest.json', json.dumps(manifest))
                    for name, content in entries:
                        z.writestr(name, content)
            write([('src/a.py', payload)])
            self.assertEqual(check_archive(archive, 'manifest.json'), manifest)
            for entries in [[('src/a.py', b'tampered')], [('src/a.py', payload), ('extra', b'x')], [],
                            [('src/a.py', payload), ('../escape', b'x')], [('src/a.py', payload), ('__pycache__/a.pyc', b'x')]]:
                with self.subTest(entries=entries):
                    write(entries)
                    with self.assertRaises(RuntimeError):
                        check_archive(archive, 'manifest.json')


if __name__ == '__main__':
    unittest.main()
