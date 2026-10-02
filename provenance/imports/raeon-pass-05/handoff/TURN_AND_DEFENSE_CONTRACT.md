
# Turn and DEFENSE Contract

## Turn
Live phases: `REFRESH | DRAW | ACTIVE | END`.

### REFRESH
At beginning of owner's turn:
- all owned live ordinary USED fields -> READY;
- no color healing;
- no topology/QMO change;
- no destroyed-field restoration;
- no opponent refresh.

### DRAW
Attempt one normal top-deck draw, respecting Hand max 10.

### ACTIVE
Active player: friendly Restore, hostile Degrade, and other admitted actions.

### END
No refresh. Advance player, enter that player's REFRESH.

## Hostile Degrade state machine
`ACTIVE`
-> admit Degrade
-> spend/route source
-> resolve target degradation
-> resolve zero/destruction/inactivation
-> terminal check
-> if terminal: MATCH_COMPLETE
-> else evaluate legal defense
-> none: ACTIVE
-> legal: DEFENSE_OPEN
-> defender Restore or PASS
-> DEFENSE_CLOSED
-> ACTIVE

## Response binding
Ordinary DEFENSE Restore targets the surviving object just degraded, not an unrelated friendly object.

## Sources
Response may use:
1. stored charge in a legal Restore/Universal Prime; or
2. one READY field via existing Prime/Rainbow Road mediation.

If field generation + Prime spend is required, it counts as the single defense response and must be atomic for rollback.

## Timing
Rule engine owns OPEN/CLOSED/legal-option state. Exact wall-clock seconds remain OPEN. Platform may deliver timeout/PASS; it may not decide legality.

## Ordering evidence
Replay/logs must show Degrade committed before Restore.
