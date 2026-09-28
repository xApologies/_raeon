# Local peer-to-peer match direction

Authority: PROVISIONAL — ACCEPTED DESIGN DIRECTION from [Block 3](../../provenance/sources/recovery-0003-block-3.txt). Machine-readable direction: [accepted state](../../data/manifests/accepted-state.json).

Device A hosts match state; Device B joins. Devices exchange compact actions/state and each renders locally. A centralized gameplay server should not be required for every local match. Rendered frames are not gameplay state and must not be the exchanged gameplay representation.

Transport remains OPEN. No Bluetooth, Wi-Fi Direct, Multipeer Connectivity, internet relay or platform-specific transport is selected. Synchronization, reconnect, authority enforcement and other implementation contracts remain OPEN. No networking is implemented.

Black cards are legal in ordinary PvP decks and are not restricted to Black Mode. Matchmaking and competitive balance policy remain OPEN. PvP may eventually reward game-generated progression/credits; no player ante/wager transfers are allowed. Exact rewards remain OPEN.
