
# 00 — EXECUTE THIS FIRST

## Mandatory entry gate
1. Fetch `xApologies/_raeon`.
2. Verify `codex/raeon-pass-04` resolves exactly to `63771ab37dfec9a0c9de907c60f6f8b2f7a3f670`.
3. Verify that commit contains the sealed 108/108 Pass-4 receipt.
4. Verify `main` remains `69a0030805b8c3858c877a514e2f50644421115a` unless a newer user-authorized main change exists. If divergent, STOP and report.
5. Verify `_bricked` is read-only at `c89676fc26000ae6f5fdad66a56e118b285d9b1d` or an explicitly user-authorized successor.
6. Create/use `codex/raeon-pass-05` from the verified Pass-4 sealed head.
7. Run the complete inherited Pass-4 entry/audit suite before editing.
8. Run `VERIFY_POUCH.py`.

## Authority rule
Git is the implementation ledger. This pouch is new user-authorized design authority for Pass 5. It supersedes only `SUPERSESSION_LEDGER.json`. Everything else from Passes 1–4 remains inherited.

## Do not
- regenerate QMO mathematics;
- weaken or delete prior tests;
- merge to `main`;
- write to `_bricked`;
- invent OPEN rules;
- jump to graphics/native presentation;
- move gameplay authority from Genesis State to Python;
- bypass Rainbow Road;
- collapse Prime nodes into generic HP;
- reinterpret aggregate magnitude 8 as automatic Black;
- impose an artificial node cap;
- allow Prime self-Restore;
- treat DEFENSE as prevention;
- open DEFENSE after terminal loss.

## Required output
Produce a Pass-5 receipt with exact Git SHAs, case-by-case evidence, inherited-test preservation, migration/replay evidence, offline validation, remaining OPEN ledger, and HOST-RUNTIME-001 retained unless independently resolved.
