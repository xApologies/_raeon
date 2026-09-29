from __future__ import annotations
import json, sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"database"/"RAEON_QMO_v0_2.sqlite"

def _c():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def pair(a:str,b:str)->dict:
    x,y=sorted([a,b])
    c=_c()
    try:
        r=c.execute("SELECT * FROM manifold_pair_relations WHERE a_manifold=? AND b_manifold=?",(x,y)).fetchone()
        if not r: raise KeyError((a,b))
        d=dict(r)
        d["shared_generators"]=json.loads(d.pop("shared_generators_json"))
        d["cross_edges"]=json.loads(d.pop("cross_edges_json"))
        return d
    finally:c.close()

def can_fuse(a:str,b:str)->bool:
    return pair(a,b)["fusion_status"]=="VALID"

def fusion(a:str,b:str):
    p=pair(a,b)
    if p["fusion_status"]!="VALID":
        return {"status":p["fusion_status"],"reason":p["fusion_reason"],"result":None}
    return {"status":"VALID","color":p["fusion_result_color"],"result":derived(p["fusion_result_qmo"])}

def coupling(a:str,b:str):
    p=pair(a,b)
    if p["emergent_status"]!="VALID":
        return {"status":"TERMINATES","reason":p["emergent_reason"],"result":None}
    return {"status":"VALID","color":p["emergent_color"],"score":p["emergent_score"],"result":derived(p["emergent_qmo"])}

def derived(address:str):
    c=_c()
    try:
        r=c.execute("SELECT * FROM derived_qmos WHERE address=?",(address,)).fetchone()
        if not r:return None
        d=dict(r); d["support"]=json.loads(d.pop("support_json")); d["definition"]=json.loads(d.pop("definition_json")); return d
    finally:c.close()

def valid_fusions(color_a=None,color_b=None):
    c=_c()
    try:
        rows=c.execute("SELECT * FROM manifold_pair_relations WHERE fusion_status='VALID'").fetchall()
        out=[]
        for r in rows:
            d=dict(r)
            if color_a or color_b:
                def col(mid):
                    rr=c.execute("SELECT native_color FROM manifold_qmos WHERE manifold_id=?",(mid,)).fetchone()
                    return rr["native_color"]
                ca,cb=col(d["a_manifold"]),col(d["b_manifold"])
                wanted=[x for x in [color_a,color_b] if x]
                if wanted and not all(w in [ca,cb] for w in wanted): continue
            out.append(d)
        return out
    finally:c.close()

def atlas_entry(a:str,b:str)->dict:
    p=pair(a,b)
    return {
        "pair":[a,b],
        "fusion":{"status":p["fusion_status"],"color":p["fusion_result_color"],"reason":p["fusion_reason"]},
        "emergent":{"status":p["emergent_status"],"color":p["emergent_color"],"score":p["emergent_score"],"reason":p["emergent_reason"]}
    }
