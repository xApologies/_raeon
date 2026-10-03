from pathlib import Path
import hashlib,json,sys
r=Path(__file__).resolve().parent;m=json.loads((r/"MANIFEST.json").read_text());errs=[]
for n,x in m["payloads"].items():
 p=r/n
 if not p.exists():errs.append("missing "+n);continue
 b=p.read_bytes()
 if len(b)!=x["bytes"] or hashlib.sha256(b).hexdigest()!=x["sha256"]:errs.append("mismatch "+n)
a=json.loads((r/"PASS_06_ACCEPTANCE.json").read_text())
if a["total"]!=m["acceptance_case_count"]:errs.append("acceptance count")
if errs:
 print("RAEON PASS 06 POUCH VERIFY: FAIL");[print(" -",e) for e in errs];sys.exit(1)
print("RAEON PASS 06 POUCH VERIFY: PASS")
print("acceptance cases:",a["total"])
print("base:",m["required_base_sha"])
print("target:",m["target_branch"])
