
# Pass 05 Rules — Canonical Human-Readable Contract

## Opening game
Each player draws **7 ordinary cards from the 60-card deck**. Hand maximum is **10**, superseding the prior capacity 7. Admission beyond 10 is forbidden; overflow disposition remains OPEN, so no silent burn/discard/exile is authorized.

Mulligan is allowed, but procedure remains OPEN.

First player is chosen by a fair binary random outcome equivalent to a coin toss; authoritative result is recorded in Genesis State. Exact PRNG is OPEN.

Second player receives one extra single-use **Draw 1 compensation card** in Hand after the seven-card opening draw. It is not drawn from Deck, costs no resource, counts toward the 10-card maximum, and may be held. Final name/ID/flavor and exact play timing remain OPEN.

## Draw cadence
Normal own-turn draw: exactly **1** next/top Deck card. Extra draws come from admitted effects.

## Turn
`REFRESH -> DRAW -> ACTIVE -> END`

At the beginning of your own turn, all your eligible live ordinary USED Configuration Fields become READY. Ending ACTIVE and merely switching players do not refresh.

ACTIVE: friendly Restore + hostile Degrade. No generic action-point budget.

## DEFENSE
A hostile Degrade resolves first. State consequences occur. Terminal condition is checked. If nonterminal and the just-degraded surviving object has a legal Restore response, one short DEFENSE window opens.

The defender may perform **one legal friendly Restore against that object or PASS**. Exact seconds are OPEN/TUNABLE; timeout = PASS. Restore/Pass closes immediately. No legal Restore = no pause.

DEFENSE is recovery, not prevention. A destroyed field cannot be ordinarily restored in the same window. An INACTIVE Prime requires explicit White reactivation. A Prime used as Restore source cannot Restore itself.

## Prime charge nodes
For native Prime rank `r`, intrinsic `H_max=r`.

Stored charge is:
`Q = N*r + R`

- `N >= 0`: completed native-color charge nodes.
- `0 <= R < r`: partial remainder.
- Completed nodes inherit Prime native color.
- Remainder color is the ordinary color of magnitude R.
- No game-rule node cap is accepted.

Restore heals H first, then adds remaining magnitude to Q. Overflow completes nodes and carries into the next node; nothing is discarded.

Degrade consumes Q first, then H.

Prime operations spend from Q. Partial spending and repeated operation remain legal while H is full and Q remains.

Pass-4 migration: `N=C//r`, `R=C%r`.

Canonical Yellow example: `r=3,H=3,N=2,R=2` => two Yellow nodes + Orange remainder, `Q=8`. This total is **not automatically Black**.

## Utility cost
Utilities have **zero resource cost**. Hand/timing/target/math admission still applies. Do not invent mana/energy/color payment.

## Victory
All three owned Prime Fields INACTIVE => immediate loss; opponent wins. Terminal check occurs before any post-Degrade DEFENSE window.

## Deck exhaustion
Failed normal draws escalate forced Degrade magnitude:
Red1, Orange2, Yellow3, Green4, Blue5, Violet6.

Target selection and post-Violet behavior remain OPEN. Encode the accepted direction but do not invent the missing law.
