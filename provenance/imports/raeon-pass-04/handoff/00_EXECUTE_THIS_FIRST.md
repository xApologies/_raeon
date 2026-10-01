# RAEON DIPLOMATIC POUCH — PASS 4
## EXECUTE THIS FIRST
Implement, test, commit and push Pass 4. Do not return another plan.

WRITE: xApologies/_raeon only. READ-ONLY: _bricked.
Recover latest valid `codex/raeon-pass-03b`; pouch checkpoint is d644a361aa2ce788a1da991b15e3b8e3be5c7cba.
Create/continue `codex/raeon-pass-04`. Main stays unmerged.

### Preserve
Pass 3B 85/85; original Pass 3 97 PASS/1 BLOCKED/0 FAIL; 60/60 base fields; soft snap/orientation; fusion; emergence; dynamic Configuration Region 3 permanent + 6 additional = 9 max; Pass-2 privacy correction; source QMO hashes; Rainbow Road; Genesis handlers; host-risk ledger for Windows CPython repeated-runtime instability.

### Color
Magnitude: 0=None, Red1, Orange2, Yellow3, Green4, Blue5, Violet6, White7.
Ordinary resolved field stores immutable native QMO/native maximum plus mutable current_magnitude/current_color and availability READY|USED.
New resolved field: current=native, READY.
READY generates CURRENT magnitude once per refresh cycle through Rainbow Road, then USED; it stays resolved. USED cannot generate. Availability persists ACTIVE->DEFENSE. Ending ACTIVE never refreshes.
Exact refresh boundary is OPEN. Implement only a trusted/policy REFRESH_FIELDS primitive for tests/future scheduler integration; never auto-call it at a guessed boundary.

RESTORE field: increase current magnitude, never above native max.
DEGRADE field: decrease current magnitude.
At zero: destroy live ordinary field; supporting FG copies -> Graveyard via existing transfer law; Configuration Space updates; incident emergents collapse; source cannot generate. Never mutate source manifold QMO/native identity.

### Ordinary Primes
Current Git 14-identity catalog is authority; do not revive obsolete 30-card model.
Restore: Yellow3 Green4 Blue5 Violet6 White7.
Degrade: Yellow3 Green4 Blue5 Violet6 White7.
Universal: Red1 Orange2 Yellow3 Green4.
Copy limit 1; three fixed Prime positions/player. Prime identity != slot identity.

Rank r: Hmax=Cmax=r. Initial bound state H=r,C=0.
HEALTHY_UNCHARGED: H=Hmax,C=0.
OPERATIONAL_CHARGED: H=Hmax,C>0.
DAMAGED_NON_OPERATIONAL: 0<H<Hmax; cannot spend.
INACTIVE: H=C=0; remains same fixed slot; never Graveyard.

Friendly RESTORE amount a: heal=min(a,Hmax-H), then charge=min(a-heal,Cmax-C).
Overflow beyond H/C capacity remains OPEN: reject any request that requires undefined overflow or require a smaller explicit admitted amount. Never silently discard/redirect excess.
Hostile DEGRADE a: remove C first, then H. H=0 => (0,0) INACTIVE.
SPEND uses C only, 0<amount<=C. Restore family RESTORE only; Degrade family DEGRADE only; Universal either direction if window admits. Partial repeated spending allowed while healthy/charged. Spending never directly changes source H.

White Restore Prime bounded effect: INACTIVE (0,0)->(1,0), same identity/slot, no charge/full heal. Generic Utility timing/cost stays OPEN; expose only as admitted/test-policy effect.

### Authority
Implement explicit active_player and derive ACTIVE/DEFENSE.
ACTIVE owner: friendly RESTORE; hostile DEGRADE.
DEFENSE player: friendly RESTORE only. No Degrade counterattack; Universal obeys direction.
Trusted match-control may switch active_player for integration tests. Switching never refreshes.
This is NOT a complete turn/phase/priority/reaction scheduler.

### Transport
No second bus:
resolved source -> Rainbow Road -> Prime -> admitted target -> Nexus-mediated State successor.
Ordinary Configuration Field cannot directly hostile-attack; hostile action requires Prime.
Transactions atomic, revision-guarded, retry-idempotent, delivery-loss recoverable, Road-provenanced.

### Required positive/negative scenarios
A resolve field -> generate current color -> USED -> Road -> healthy Prime charge.
B charge Prime -> partial spend -> retain C/shield -> spend again.
C Prime (4,3), Degrade5 -> (2,0), DAMAGED_NON_OPERATIONAL.
D Green Prime (1,0), Restore4 -> (4,1).
E Green field4, Degrade3 -> Red1; Restore3 -> Green4; native identity remains Green.
F field ->0 -> FGs Graveyard, source unusable, space updated, incident emergents collapse.
G ACTIVE uses fields; DEFENSE uses reserved READY field through Restore; switch active player without refresh and prove availability persists.
H DEFENSE Degrade and Universal->Degrade hostile target rejected.
I Prime ->0 INACTIVE; ordinary Restore does not reactivate; White Restore effect ->(1,0), same identity/slot, higher-rank still damaged.
J checkpoint/restart/retry preserve H/C, current field magnitude, READY/USED, active authority, identities, Road history, privacy, deterministic root.

### OPEN — DO NOT INVENT
Exact refresh boundary; full turn phases/order/priority/reactions; starting hand/draw/mulligan/first player; overflow; generic Utility timing/cost; exhaustive targeting beyond accepted side/direction; victory/loss/deck exhaustion; match timer; temporary-space expiry; derived additions/splitting/recursive fusion-emergence; native UI/graphics.
Search current Git first; if newer accepted authority resolves an item, cite it. Otherwise leave OPEN.

### Validation/delivery
Add real Genesis source/handlers for Pass-4 mechanics; Python host binding may validate/orchestrate but Hypervisor remains game-agnostic. Prove Genesis and Rainbow Road participation with negative mutation/bypass tests.
Re-run all current runtime acceptance, Pass2/privacy, Pass3/3B, 60-field positives, validators, regressions, gameplay specs, deterministic Genesis compilation, and fresh-extraction offline verification.
Offline distribution must contain all new Prime/color/match-state inputs and run without Git/network/original _raeon/_bricked checkout dependency under the currently qualified host-reference environment.
Preserve HOST-RUNTIME-001 qualification unless genuinely resolved.
Write maintained PASS_04_RECEIPT.md + machine receipt with exact start/end/remote/main SHA, tests, hashes, open gates and distribution hashes. Push branch; clean tree; do not merge main. Whole-game phase remains PREPRODUCTION.
