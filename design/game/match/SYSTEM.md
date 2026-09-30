# Match and turn design

<!-- raeon:current-spec match -->

Authority: GAME_CANON for the 2026-09-30 rules below. [Structured match rules](../../../data/game/match.json) distinguish accepted constraints from unresolved sequencing.

Hand normal capacity is **7**. Normal admission cannot exceed capacity; check the destination before committing card movement. Starting hand size, normal draw cadence, mulligan, first-player rule, short-deck resolution and overflow/multi-card effect resolution remain OPEN. Normal draw takes the next/top Deck card; this defines access, not frequency.

| Authority window | Admitted Prime direction and side |
| --- | --- |
| ACTIVE — owner's active window | Friendly Restore; hostile Degrade |
| DEFENSE — opponent's active window | Friendly Restore only |

Universal uses only the direction admitted by the current window. DEFENSE cannot charge/use Degrade to counterattack. These are direction/side constraints, not a complete action or reaction scheduler. Detailed ordering, response windows, target eligibility, costs, Prime/Utility/merge/reconfiguration timing and turn phases remain OPEN.

A READY ordinary Configuration Field generates its **current color** once per refresh cycle and becomes USED without unresolving. USED cannot generate again until an admitted refresh. Availability carries from ACTIVE into DEFENSE; ending ACTIVE never refreshes it by itself. The exact common refresh boundary remains OPEN. Reserving READY fields preserves defensive restoration capacity; using them during ACTIVE spends that shared availability.

Primes can operate repeatedly while healthy and charged, subject to admission, and are not field-style taps. Ordinary fields route hostile action through the Prime system, using existing Rainbow Road transport. See [Prime constitution](../../cards/cycle_01/primes/SYSTEM.md) and [transduction](../../transduction/SYSTEM.md).

A roughly 15-minute session is a design target, not a hard timer. Victory/loss, deck exhaustion, surrender/timeout, temporary Configuration Space expiry and field-destruction transaction ordering remain OPEN. Ordinary Prime H=0 means INACTIVE in place, not an inferred loss condition. Destruction of all opposing Primes remains only a PROVISIONAL victory proposal.

These accepted rules have focused specification tests; complete match gameplay and Genesis implementation remain OPEN / UNIMPLEMENTED.
