# Ordinary Prime Field constitution

<!-- raeon:current-spec prime-fields -->

Authority: GAME_CANON, accepted 2026-09-29. There are **14 unique ordinary Prime identities**, copy limit one per identity and three fixed active Prime positions. This supersedes the former 30-card OPEN catalog. [Structural catalog](../../../../data/cycles/cycle_01/primes/status.json) and [health/charge rules](../../../../data/cycles/cycle_01/primes/working-model.json) encode this constitution; the latter retains its historical filename.

| Family | Identities and maximum magnitudes | Count |
| --- | --- | ---: |
| Restore | Yellow +3, Green +4, Blue +5, Violet +6, White +7 | 5 |
| Degrade | Yellow -3, Green -4, Blue -5, Violet -6, White -7 | 5 |
| Universal | Red ±1, Orange ±2, Yellow ±3, Green ±4 | 4 |

For rank r, intrinsic maximum health H_max = r and active color-charge/shield maximum C_max = r. Full H and C give effective durability 2r; identity and printed rank never change with current charge. Catalog lookup keys describe family/rank, not finalized printed IDs.

Friendly Restore repairs intrinsic health first. Only after H reaches H_max does excess fill C, up to C_max. Green at (H,C)=(1,0) receiving +4 becomes (4,1). Restore beyond available H/C capacity remains an OPEN overflow-policy question. Ordinary Restore does not silently grant the explicit INACTIVE reactivation effect below.

Charge C is partially spendable. Green C=4 spending 2 leaves C=2, Orange active charge, while its Green identity remains. Restore Primes spend only positively; Degrade only negatively; Universal may spend either way and has a Green ceiling. Spending C reduces shield without changing H. Exact turn/timing and targeting windows remain OPEN.

Hostile degradation removes C first, then H. At (4,2), incoming -3 yields (3,0). H=0 makes the ordinary Prime **INACTIVE** at (0,0); it stays in its fixed Prime position and never moves to Graveyard under this rule. [White Restore Prime](../utilities/restore_prime/SYSTEM.md) reactivates one INACTIVE Prime from (0,0) to (1,0), without full healing or charge.

OPEN: overflow policy, detailed timing/targets, final names/IDs/flavor/wording, balance and implementation. This is accepted design, not a running game system. [Black Prime mechanics](../../black/primes/SYSTEM.md) remain separate and unchanged; no new Black reactivation/cap rule is inferred. [Board](../../../game/board/SYSTEM.md) preserves fixed positions; [transduction](../../../transduction/SYSTEM.md) retains broader mathematical-source boundaries.

## Runtime states and authority — accepted 2026-09-30

Normal start is H=H_max, C=0. A Prime card is a persistent identity-bearing Geometric, distinct from its fixed slot.

| State | Condition | Prime operation |
| --- | --- | --- |
| HEALTHY_UNCHARGED | H=H_max, C=0 | No charge available |
| OPERATIONAL_CHARGED | H=H_max, C>0 | May spend C under family/window/target admission |
| DAMAGED_NON_OPERATIONAL | 0<H<H_max | Cannot operate until H is fully restored |
| INACTIVE | H=C=0 | Explicit accepted reactivation required |

C is both spendable color and the first defensive shield. Primes are charge-limited, not once-per-turn tap-limited: multiple admitted operations may spend partial C while charge remains. Retained C shields H. [ACTIVE authority](../../../game/match/SYSTEM.md) admits friendly Restore and hostile Degrade; DEFENSE admits friendly Restore only. Universal obeys the same window; no defensive Degrade counterattack is permitted.

White Restore Prime still gives only (1,0). Higher-ranked Primes remain damaged until healed; a Red Universal at H_max=1 is healthy but uncharged. Neither may operate without charge. Exact action/reaction ordering, targets and overflow remain OPEN.
