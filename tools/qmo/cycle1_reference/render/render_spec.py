from __future__ import annotations
import hashlib, json, math, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "RAEON_QMO_v0_2.sqlite"

COLOR_VALUE = {"RED":1,"ORANGE":2,"YELLOW":3,"GREEN":4,"BLUE":5,"VIOLET":6,"WHITE":7}

def _seed_int(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)

def _load_manifold(manifold_id: str) -> dict:
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    try:
        r=c.execute("SELECT address FROM manifold_qmos WHERE manifold_id=?",(manifold_id,)).fetchone()
        if not r: raise KeyError(manifold_id)
        q=c.execute("SELECT definition_json FROM qmos WHERE address=?",(r["address"],)).fetchone()
        return json.loads(q["definition_json"])
    finally:
        c.close()

def _load_generator(card_id: str) -> dict:
    h="@qmo/raeon/cycle1/"+card_id.lower()
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    try:
        q=c.execute("SELECT definition_json FROM qmos WHERE address=?",(h,)).fetchone()
        if not q: raise KeyError(card_id)
        return json.loads(q["definition_json"])
    finally:
        c.close()

def _compatibility_edges(card_ids: list[str]) -> list[tuple[int,int]]:
    index={c:i for i,c in enumerate(card_ids)}
    hs={c:"@qmo/raeon/cycle1/"+c.lower() for c in card_ids}
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    try:
        out=set()
        for a in card_ids:
            rows=c.execute("""SELECT dst FROM edges
                              WHERE src=? AND relation='CHIRALITY_COMPATIBLE_WITH'""",(hs[a],)).fetchall()
            for r in rows:
                b=r["dst"].split("/")[-1].upper()
                if b in index:
                    i,j=index[a],index[b]
                    if i!=j: out.add(tuple(sorted((i,j))))
        return sorted(out)
    finally:
        c.close()

def build_render_spec(manifold_id: str) -> dict:
    m=_load_manifold(manifold_id)
    cards=m["generators"]
    gs=[_load_generator(c) for c in cards]
    n=len(cards)
    seed=_seed_int(m["id"])

    # deterministic carrier curve
    chirality_sign = 1 if sum(g["chirality_parity"] for g in gs)%2==0 else -1
    avg_res = sum(g["resolution_depth"] for g in gs)/max(1,n)
    avg_bw = sum(g["bandwidth_degree"] for g in gs)/max(1,n)

    r0 = 1.85 + 0.05*n
    r1 = 0.18 + 0.01*(seed%7)
    m_freq = 2 + (seed % 3)
    k_freq = 1 + ((seed >> 5) % 3)
    zeta = 0.35 + 0.03*(seed%5)
    psi = ((seed >> 8) % 360) * math.pi/180.0

    anchors=[]
    for i,g in enumerate(gs):
        theta=2*math.pi*i/n
        rho=r0+r1*math.cos(m_freq*theta+psi)
        phase=((_seed_int(g["id"])%360)*math.pi/180.0)
        x=rho*math.cos(theta)
        y=rho*math.sin(theta)
        z=zeta*math.sin(k_freq*theta+phase)
        anchors.append({
            "generator":cards[i],
            "position":[x,y,z],
            "chirality_parity":g["chirality_parity"],
            "fractal_address":g["fractal_address"]
        })

    edges=_compatibility_edges(cards)
    if not edges:
        # Always include a carrier closure for visualization while keeping it tagged.
        edges=[(i,(i+1)%n) for i in range(n)]

    spline_edges=[]
    for ei,(i,j) in enumerate(edges):
        p0=anchors[i]["position"]; p3=anchors[j]["position"]
        dx=[p3[k]-p0[k] for k in range(3)]
        L=math.sqrt(sum(v*v for v in dx)) or 1.0
        u=[v/L for v in dx]
        # stable normal: cross u with Z unless nearly parallel
        ref=[0.0,0.0,1.0] if abs(u[2])<0.9 else [0.0,1.0,0.0]
        nvec=[
            u[1]*ref[2]-u[2]*ref[1],
            u[2]*ref[0]-u[0]*ref[2],
            u[0]*ref[1]-u[1]*ref[0],
        ]
        nl=math.sqrt(sum(v*v for v in nvec)) or 1.0
        nvec=[v/nl for v in nvec]
        lam=(0.28+0.015*avg_res)*L
        eta=chirality_sign*(0.08+0.002*avg_bw)*L
        p1=[p0[k]+lam*nvec[k]+eta*u[k] for k in range(3)]
        p2=[p3[k]+lam*nvec[k]-eta*u[k] for k in range(3)]
        spline_edges.append({
            "edge_id":ei,
            "a":i,"b":j,
            "p0":p0,"p1":p1,"p2":p2,"p3":p3,
            "curve_samples":int(24+avg_res*6),
            "ring_samples":int(8+avg_res*2),
            "tube_radius":0.045*(1.0+0.01*avg_bw)
        })

    color_name=m["native_color"]
    spec={
        "schema":"raeon.render_spec.v0.3",
        "qmo_address":m["id"],
        "manifold_id":manifold_id,
        "native_color":color_name,
        "native_color_value":COLOR_VALUE[color_name],
        "generator_count":n,
        "generators":cards,
        "anchors":anchors,
        "topological_edges":[list(e) for e in edges],
        "spline_edges":spline_edges,
        "chirality_sign":chirality_sign,
        "resolution":{
            "mean":avg_res,
            "curve_samples":int(24+avg_res*6),
            "ring_samples":int(8+avg_res*2)
        },
        "bandwidth":{
            "mean":avg_bw,
            "tube_radius_scale":1.0+0.01*avg_bw
        },
        "field_shell":{
            "enabled":True,
            "kernel":"gaussian",
            "sigma":0.55+0.02*n,
            "iso_threshold":0.65,
            "grid_resolution":48+4*n
        },
        "animation":{
            "energy_wave_number":2.0+0.15*n,
            "energy_angular_frequency":1.4+0.1*COLOR_VALUE[color_name],
            "emission_power":2.0+0.25*COLOR_VALUE[color_name],
            "tap_pulse_decay":2.5,
            "breath_frequency":0.35+0.03*n,
            "vertex_displacement":0.03+0.005*COLOR_VALUE[color_name]
        },
        "projection_3plus1plus1":{
            "alpha":0.08,
            "beta":0.06,
            "tau_frequency":0.7,
            "chi":float(chirality_sign)
        },
        "deterministic_seed":seed,
        "render_states":["PREVIEW","LOCK","MANIFEST","ACTIVE"],
        "authority":"DOWNSTREAM_RENDER_ADAPTER"
    }
    return spec
