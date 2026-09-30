# raeon application — Pass 2

Application ID `raeon`, version 0.2.0, package schema 3. Empty realization still
creates the same 37 application Geometrics and 163 explicit relationships at
revision zero. No initial cards or temporary spaces are automatically created.

The Genesis handlers declare admitted inventory creation, deterministic shuffle,
draw, FG commitment, structural Prime binding, retirement, six source-linked
recovery profiles, bounded inspection/reordering/batch transfer, and dynamic
Configuration Space creation. `manifest.json` lists their exact argument shapes.
`catalog.json` indexes the unchanged 120 FG, 14 Prime and 51 Utility sources with
hashes and source pointers. Unassigned printed IDs remain OPEN; provisional
source labels are retained. `collections.json` declares container policies.

`native_instantiate.gen`, `native_relate.gen` and `native_transport.gen` are
bounded verified units composed inside one atomic candidate publication.
Actual native cards travel by the existing Portal/Rainbow Road engine. Logical
copy IDs persist while native versions and membership history advance.

All mutating operations require a trusted grant tied to actor, owner, match,
operation, exact arguments, effect source and revision. Only the conformance
harness receives a grant-issuer capability. Normal startup and the Platform
Port expose no issuer or free gameplay action. Public receipts omit seeds and
native diagnostics. Live views hide future Deck order even from its owner.

Use the canonical runner with Python 3.12:

- `python tools/genesis_runtime.py verify`
- `python tools/genesis_runtime.py demo --headless --application raeon`
- `python tools/genesis_runtime.py demo --headless --application raeon --scenario cards`
- `python tools/genesis_runtime.py test`
- `python tools/genesis_runtime.py repository-test`
- `python tools/genesis_runtime.py audit`

See the current execution record and receipt under `development/modules/core-game/`.
The exact Pass-1 application remains in the historical integration fixture.
Complete Utility play, field/QMO resolution, Prime combat and native Port apps
remain outside Pass 2. Whole-game phase remains PREPRODUCTION.
