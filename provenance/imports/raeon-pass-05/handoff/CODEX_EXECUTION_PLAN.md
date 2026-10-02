
# Codex Execution Plan — Pass 05

## Branch
Create `codex/raeon-pass-05` from exact sealed Pass-4 head `63771ab37dfec9a0c9de907c60f6f8b2f7a3f670`.

## A — Entry/preservation
Run full Pass-4 audit; hash inherited fixtures; verify QMO locks; verify `_bricked` read-only; verify pouch; record evidence.

## B — Canonical authority/data
Update canonical design/data for: 7-card opening, 10-card max, draw 1, first-player outcome, compensation design, own-turn refresh, turn/DEFENSE ordering, charge nodes, zero-cost Utilities, three-Prime loss, partial deck-exhaustion table.

Design-accepted but incomplete rules must stay explicitly incomplete.

## C — Prime migration
Replace bounded active `C<=rank` authority with canonical `N/R` storage.
Migration: `N=C//rank`, `R=C%rank`.
Preserve H/identity/slot/family/owner/revision/provenance.

## D — Turn engine
Implement deterministic `REFRESH -> DRAW -> ACTIVE -> END`. REFRESH uses existing trusted primitive. Switching/end ACTIVE never refreshes.

## E — DEFENSE
Implement post-Degrade recovery exactly. Degrade commits first. If nonterminal and legal, one response bound to degraded surviving target. PASS/timeout closes. Do not hard-code seconds. Compound field-assisted mediation is one atomic response and uses Rainbow Road.

## F — Victory
After state-changing actions, three owned INACTIVE Primes => terminal loss. Reject later gameplay mutations.

## G — Setup/draw
Implement seven-card opening draw, max Hand 10, normal draw 1. Record trusted binary first-player outcome; do not invent PRNG. Represent second-player Draw-1 compensation without inventing its unresolved play timing.

## H — Deck exhaustion guard
Encode stages Red1..Violet6 and counter/design scaffolding only. Do not apply damage without target authority.

## I — Tests
Close every mandatory case in `PASS_05_ACCEPTANCE.json`. OPEN guards pass only when Codex refuses to invent missing law.

## J — Delivery
Produce execution doc, progress JSON, receipt, host-risk ledger update, offline archives, hashes, final Git SHA. No main merge.
