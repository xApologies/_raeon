#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

root=Path(__file__).resolve().parent
m=json.loads((root/"MANIFEST.json").read_text(encoding="utf-8"))
errors=[]
for rel,meta in m["payloads"].items():
    p=root/rel
    if not p.is_file():
        errors.append("MISSING "+rel); continue
    b=p.read_bytes()
    if len(b)!=meta["bytes"]: errors.append("SIZE "+rel)
    if hashlib.sha256(b).hexdigest()!=meta["sha256"]: errors.append("HASH "+rel)

a=json.loads((root/"PASS_05_ACCEPTANCE.json").read_text(encoding="utf-8"))
ids=[c["id"] for c in a["cases"]]
if len(ids)!=len(set(ids)): errors.append("DUPLICATE acceptance IDs")
if a["total"]!=len(ids): errors.append("ACCEPTANCE total mismatch")
if m["acceptance_case_count"]!=len(ids): errors.append("MANIFEST acceptance count mismatch")
if any(not c.get("mandatory") for c in a["cases"]): errors.append("NON-MANDATORY case")

r=json.loads((root/"PASS_05_RULES.json").read_text(encoding="utf-8"))
if r["baseline"]["required_base_sha"]!=m["required_base_sha"]: errors.append("BASE SHA mismatch")
if r["match_setup"]["opening_hand_cards_from_deck"]!=7: errors.append("opening hand mismatch")
if r["match_setup"]["hand_maximum"]!=10: errors.append("hand max mismatch")
if r["prime_charge_nodes"]["canonical_example"]["Q"]!=8: errors.append("Yellow example mismatch")
if r["victory"]["loss_condition"]!="ALL_THREE_OWNED_PRIME_FIELDS_ARE_INACTIVE": errors.append("victory mismatch")

if errors:
    print("RAEON PASS 05 POUCH VERIFY: FAIL")
    for e in errors: print(" -",e)
    sys.exit(1)
print("RAEON PASS 05 POUCH VERIFY: PASS")
print("payloads:",len(m["payloads"]))
print("acceptance cases:",len(ids))
print("required base:",m["required_base_sha"])
print("target branch:",m["target_branch"])
