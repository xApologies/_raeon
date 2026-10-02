
# Prime Charge Node Contract

For immutable native rank `r`:

- `H`: intrinsic health, `0..r`.
- `N`: completed native-color charge nodes, integer `>=0`.
- `R`: partial remainder, `0..r-1`.
- `Q=N*r+R` (derived).

## Invariants
- `H=0 => N=0,R=0`.
- `0<H<r => N=0,R=0`.
- `H=r,Q=0 => HEALTHY_UNCHARGED`.
- `H=r,Q>0 => OPERATIONAL_CHARGED`.
- Completed node color = Prime native color.
- `R=0` => no partial color; `R>0` => color of magnitude R.
- Q never changes identity/rank/family.
- No game-rule node cap.

## Restore
For admitted Restore `x>0` to non-INACTIVE Prime:
1. `heal=min(x,r-H)`.
2. `H'=H+heal`.
3. `left=x-heal`.
4. If `H'=r`, `Q'=Q+left`.
5. `N'=floor(Q'/r)`.
6. `R'=Q' mod r`.

No overflow loss.

## Degrade
1. consume `min(d,Q)` from Q;
2. remaining d reduces H;
3. re-decompose Q into N/R.

## Spend
Require H full, Q>0, admitted family/window/target, and `0<s<=Q`.
Set `Q'=Q-s`; H unchanged; recompute N/R. No tap/once-per-turn limit.

## Self-Restore
If the Restore source is a Prime, source and target Prime IDs must differ. A field source may restore/charge a Prime when otherwise legal.

## White reactivation
INACTIVE -> `(H,N,R)=(1,0,0)`, identity/slot unchanged.

## Pass-4 migration
Old `(H,C)` -> `N=C//r`, `R=C%r`. Preserve stored magnitude exactly. Old full C becomes one completed node.

## Projection
Expose intrinsic health, N, remainder color, and derived Q for future dot/orb UI. No native graphics in Pass 5.
