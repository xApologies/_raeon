# Match tempo — Pass 05

[Current authority](../../data/game/pass-05-runtime.json) implements opening draw 7, Hand maximum 10, one normal own-turn draw, trusted fair binary first-player outcome, and the accepted non-Deck Draw-1 compensation object.

`SETUP_MATCH` enters the first player's REFRESH. `BEGIN_TURN` refreshes only that player's eligible live ordinary USED fields and enters DRAW. `NORMAL_DRAW` enters ACTIVE; `END_ACTIVE` enters END; `ADVANCE_TURN` switches to the opponent's REFRESH without refreshing any field.

Degrade resolves through Rainbow Road, then destruction/emergent consequences and immediate terminal checks resolve. Only a surviving target with an actual legal Restore option opens one DEFENSE opportunity. Stored Restore/Universal charge or one READY field through legal Prime mediation can respond; compound mediation is atomic. Pass or an explicit trusted timeout closes the window. Exact seconds remain OPEN.

Three owned bound inactive Primes immediately lose. Terminal State rejects further gameplay. Failed normal draws record Red1 through Violet6; target selection and stage7+ remain OPEN and no damage is applied without that authority.

`game/match/state.py` is the source-pinned value binding for the compiled Genesis contract. All actions retain admission, transform, closure, native State publication and actual Rainbow Road transport. The existing conformance issuer is test-only. Unresolved generic Utility/compensation timing requires explicit effect-specific admission; there is no default play window.

The historical Pass-04 color ABI remains executable for unchanged conformance tests before adoption. `ADOPT_PASS05` migrates canonical values atomically, and current live matches reject historical manual-authority, refresh and bounded-charge operations. See [execution record](../../development/modules/core-game/PASS_05_EXECUTION.md).
