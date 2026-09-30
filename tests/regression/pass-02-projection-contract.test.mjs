import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {validateProjectionCorrection, projectionCorrectionDecision} from '../../tools/validators/pass-02-contract.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const decision = JSON.parse(fs.readFileSync(path.join(root, projectionCorrectionDecision), 'utf8'));
const files = [...Object.keys(decision.corrected_sources), ...Object.keys(decision.evidence_files), decision.additive_regression_source];
test('projection correction retains exact source and reproduction evidence', () => {
  assert.doesNotThrow(() => validateProjectionCorrection(root, [projectionCorrectionDecision]));
});
for (const mutation of ['binding', 'evidence', 'decision']) {
  test('projection correction rejects modified ' + mutation, () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'raeon-projection-contract-'));
    try {
      for (const file of [...files, projectionCorrectionDecision]) {
        fs.mkdirSync(path.dirname(path.join(tmp, file)), {recursive: true});
        fs.copyFileSync(path.join(root, file), path.join(tmp, file));
      }
      const changed = mutation === 'binding' ? Object.keys(decision.corrected_sources)[0]
        : mutation === 'evidence' ? Object.keys(decision.evidence_files)[0] : projectionCorrectionDecision;
      fs.appendFileSync(path.join(tmp, changed), ' ');
      assert.throws(() => validateProjectionCorrection(tmp, [projectionCorrectionDecision]), /projection correction/i);
    } finally {
      if (!path.resolve(tmp).startsWith(path.resolve(os.tmpdir()) + path.sep)) throw new Error('Unsafe temporary cleanup');
      fs.rmSync(tmp, {recursive: true, force: true});
    }
  });
}
