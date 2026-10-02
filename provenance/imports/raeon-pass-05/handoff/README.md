
# RAEON Diplomatic Pouch — Pass 05
Date: 2026-10-01

Authoritative design-to-Codex handoff for Pass 5.

## Repository targets
- Write repository: `xApologies/_raeon`
- Required starting point: `63771ab37dfec9a0c9de907c60f6f8b2f7a3f670` (`codex/raeon-pass-04` sealed head)
- New implementation branch: `codex/raeon-pass-05`
- Main stays unmerged.
- Read-only upstream: `xApologies/_bricked` pinned at `c89676fc26000ae6f5fdad66a56e118b285d9b1d`.
- `_bricked` must not become a shipped runtime dependency.

## Pass-5 theme
**Match Tempo / Prime Charge / Turn Authority**

Pass 5 advances the headless game into a temporal economy: opening draw constraints, beginning-of-own-turn refresh, active/defending authority, post-Degrade DEFENSE, accumulated Prime charge nodes, zero-cost Utility law, and the three-Prime loss condition.

Every OPEN item remains OPEN. Do not fill gaps from conventional TCG assumptions.

## Read order
1. `00_EXECUTE_THIS_FIRST.md`
2. `CURRENT_STATE.json`
3. `PASS_05_RULES.md`
4. `PRIME_CHARGE_NODE_CONTRACT.md`
5. `TURN_AND_DEFENSE_CONTRACT.md`
6. `HAND_SETUP_DRAW_CONTRACT.md`
7. `UTILITY_COST_CONTRACT.md`
8. `VICTORY_AND_DECK_EXHAUSTION.md`
9. `SUPERSESSION_LEDGER.json`
10. `OPEN_ITEMS.json`
11. `PASS_05_ACCEPTANCE.json`
12. `CODEX_EXECUTION_PLAN.md`
13. `VERA_AUDIT_RUBRIC.md`
14. `SOURCE_ANCHORS.json`
15. `MANIFEST.json`

Run `python VERIFY_POUCH.py` before implementation.
