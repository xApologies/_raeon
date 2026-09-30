# Python Hypervisor

The local byte bridge connects a trusted Horizon adapter to an embedded native
host. It creates no listener. The host must supply Python 3.12 and an authenticated
session context. Native Swift/Kotlin/desktop SDK ports and device performance are
not provided or certified by this reference package.

Install this directory with `python -m pip install .`. Call
`raeon_hypervisor.open(adapter, config)`, then `bind_session(trusted_context)`.
The returned opaque handle binds actor, application and view. The host can read
`bridge.epoch` to construct the initial HELLO. Receive bytes with `receive`, execute
one queued request with `step`, and collect bounded output with `drain`.
`receive` never invokes application semantics. All execution is serialized.

The v2 frame is `>8sBBHII`: `RAEONH2!`, 2, 0, zero flags, payload length and CRC32,
followed by strict UTF-8 JSON. CRC32 is corruption detection, not authentication.
Schemas and independent vectors are under `schemas/`. IDs use 1–128 ASCII letters,
digits, dot, underscore, colon or hyphen. JSON numbers are exact integers within
±(2^53−1); counters are nonnegative. Booleans are not integer counters. Nested JSON
has a maximum depth of 24. The fixture declares empty argument objects; the
Horizon owns operation validity. No game rules are evaluated in this library.

HELLO yields WELCOME and SNAPSHOT. INTENT yields a correlated RECEIPT and an
authorized DELTA or SNAPSHOT. Apply a DELTA only to the same view and epoch at its
exact base revision. Its `replace_view` change is a complete replacement of the
authorized projection, never VM memory. A RECEIPT and an ACK do not advance a Port
projection. SYNC_REQUEST replays one retained contiguous delta or supplies a fresh
snapshot; larger/gapped history uses a snapshot. Actor/view changes require a new
trusted session and snapshot. Restore changes epoch and clears boundary queues.

Before execution the bridge reserves space for two maximum frames. Delivery
failure after commit returns COMMITTED_DELIVERY_PENDING and recovery uses the
Horizon's atomically associated outcome. Retry identity is application, trusted
actor and request ID; altered content conflicts. The Horizon retains up to 4096
outcome keys including expired tombstones, then refuses new requests until the
owner starts a new machine. Expiry never makes an old ID reusable.

Call `save_checkpoint(authority)` with an empty ingress queue, or
`restore_checkpoint(reference, authority)`. `close_session(handle)` cancels queued
work for that session. `close('drain', budget)` settles accepted ingress in order;
`close('cancel', budget)` cancels pending work. `close` is idempotent. This Python
boundary is a trusted process API, not hostile-code or operating-system isolation.
