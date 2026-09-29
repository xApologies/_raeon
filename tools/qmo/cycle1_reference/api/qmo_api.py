#!/usr/bin/env python3
import json, sqlite3
from pathlib import Path
DB=Path(__file__).resolve().parent.parent/'database'/'RAEON_QMO_v0_2.sqlite'
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def qmo(card_or_handle):
    h=card_or_handle if card_or_handle.startswith('@') else '@qmo/raeon/cycle1/'+card_or_handle.lower()
    c=conn()
    try:
        r=c.execute('SELECT * FROM qmos WHERE address=?',(h,)).fetchone()
        if not r: return None
        d=dict(r); d['definition']=json.loads(d.pop('definition_json')); return d
    finally: c.close()
def compatibility(card_id):
    h='@qmo/raeon/cycle1/'+card_id.lower(); c=conn()
    try:
        rows=c.execute("SELECT dst,metadata_json FROM edges WHERE src=? AND relation='CHIRALITY_COMPATIBLE_WITH'",(h,)).fetchall()
        return [{'dst':r['dst'],'matches':json.loads(r['metadata_json'])} for r in rows]
    finally: c.close()
def manifolds_for(card_id):
    h='@qmo/raeon/cycle1/'+card_id.lower(); c=conn()
    try:
        rows=c.execute("SELECT dst FROM edges WHERE src=? AND relation='PARTICIPATES_IN'",(h,)).fetchall()
        return [qmo(r['dst']) for r in rows]
    finally: c.close()
def manifold(manifold_id):
    c=conn()
    try:
        r=c.execute('SELECT address FROM manifold_qmos WHERE manifold_id=?',(manifold_id,)).fetchone()
        return qmo(r['address']) if r else None
    finally: c.close()
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('qmo'); p.add_argument('id')
    p=sp.add_parser('compatibility'); p.add_argument('card')
    p=sp.add_parser('manifolds'); p.add_argument('card')
    p=sp.add_parser('manifold'); p.add_argument('id')
    a=ap.parse_args()
    if a.cmd=='qmo': out=qmo(a.id)
    elif a.cmd=='compatibility': out=compatibility(a.card)
    elif a.cmd=='manifolds': out=manifolds_for(a.card)
    else: out=manifold(a.id)
    print(json.dumps(out,indent=2))
