"""Frozen runtime realization authority; never generates or edits source QMOs.

Floating point is confined to scoring. Wire values are scaled integers. A lock
stores a symbolic witness + SE(2) transform, so its authoritative geometry is
the transformed witness, not independently rounded presentation coordinates.
"""
import copy
import hashlib
import json
import math
from collections import Counter


SCALE = 1_000_000_000


def within(value, threshold):
    # Inclusive decimal contract boundaries, with only binary64 roundoff slack.
    return value <= threshold or math.isclose(value, threshold, rel_tol=1e-12, abs_tol=1e-12)


def projective(q):
    values=[round(v*SCALE) for v in q]
    divisor=math.gcd(*values)
    if not divisor:raise ValueError('REALIZATION_ROTATION')
    values=[v//divisor for v in values]
    return [-v for v in values] if next(v for v in values if v)<0 else values


def norm(q):
    length = math.sqrt(sum(v*v for v in q))
    if not length or not math.isfinite(length):
        raise ValueError('REALIZATION_ROTATION')
    return [v/length for v in q]


def multiply(a, b):
    w,x,y,z = a
    v,i,j,k = b
    return [w*v-x*i-y*j-z*k, w*i+x*v+y*k-z*j,
            w*j-x*k+y*v+z*i, w*k+x*j-y*i+z*v]


def distance(a, b):
    dot = abs(sum(x*y for x,y in zip(norm(a), norm(b))))
    return math.degrees(2*math.acos(min(1.0, dot)))


def se2(witness, current):
    """Labeled least-squares fit in SE(2), with no scale or permutation search."""
    if len(witness) != len(current) or not witness:
        raise ValueError('REALIZATION_MEMBERSHIP')
    n = len(witness)
    wb = [sum(p[j] for p in witness)/n for j in (0,1)]
    pb = [sum(p[j] for p in current)/n for j in (0,1)]
    w = [[p[j]-wb[j] for j in (0,1)] for p in witness]
    p = [[v[j]-pb[j] for j in (0,1)] for v in current]
    a = sum(x*u+y*v for (x,y),(u,v) in zip(w,p))
    b = sum(x*v-y*u for (x,y),(u,v) in zip(w,p))
    phi = math.atan2(b,a)
    c,s = math.cos(phi),math.sin(phi)
    t = [pb[0]-c*wb[0]+s*wb[1],pb[1]-s*wb[0]-c*wb[1]]
    fitted = [[t[0]+c*x-s*y,t[1]+s*x+c*y] for x,y in witness]
    errors = [math.hypot(x-u,y-v) for (x,y),(u,v) in zip(fitted,current)]
    return {'phi':phi,'translation':t,'fitted':fitted,
            'rms':math.sqrt(sum(e*e for e in errors)/n),'max':max(errors)}


class Realization:
    def __init__(self, root, corpus):
        self.root, self.corpus = root, corpus
        self.path = root/'game/qmo/realization.lock.json'
        self.hash = hashlib.sha256(self.path.read_bytes()).hexdigest()
        self.lock = json.loads(self.path.read_text(encoding='utf8'))
        self.verify()
        data = {p.rsplit('/',1)[-1]:json.loads((root/p).read_text(encoding='utf8')) for p in self.lock['inputs']}
        self.witnesses = data['BASE_MANIFOLD_WITNESSES.json']['witnesses']
        self.rotations = data['ROTATION_CLASS_TABLE.json']['classes']
        self.snap = data['SOFT_SNAP_V1.json']
        self.orientation = data['ORIENTATION_REALIZATION_V1.json']
        self.validate_authority()

    def verify(self):
        if hashlib.sha256(self.path.read_bytes()).hexdigest() != self.hash:
            raise ValueError('REALIZATION_INTEGRITY')
        for p,sha in self.lock['inputs'].items():
            target = (self.root/p).resolve()
            if not target.is_relative_to(self.root.resolve()) or hashlib.sha256(target.read_bytes()).hexdigest() != sha:
                raise ValueError('REALIZATION_INTEGRITY')

    def validate_authority(self):
        if set(self.witnesses) != set(self.corpus.base) or len(self.witnesses) != 60:
            raise ValueError('REALIZATION_MEMBERSHIP')
        total = 0
        for mid,w in self.witnesses.items():
            slots = w['generator_slots']; labels = [s['field_generator'] for s in slots]
            if Counter(labels) != Counter(self.corpus.base[mid]['generators']) or len(set(labels)) != len(labels):
                raise ValueError('REALIZATION_MEMBERSHIP')
            if w['generator_count'] != len(labels) or w['manifold_id'] != mid:
                raise ValueError('REALIZATION_MEMBERSHIP')
            slot_map = {s['slot']:s['field_generator'] for s in slots}
            if len(slot_map) != len(slots) or len({tuple(s['xy']) for s in slots}) != len(slots):
                raise ValueError('REALIZATION_SLOTS')
            degree = Counter(); graph = {g:set() for g in labels}; seen = set()
            for edge in w['required_cycle_edges']:
                a,b = edge['a'],edge['b']; key = tuple(sorted((a,b)))
                row = self.corpus.compatibility.get(key)
                if a == b or key in seen or not row or not row['matches'] or slot_map[edge['a_slot']] != a or slot_map[edge['b_slot']] != b:
                    raise ValueError('REALIZATION_EDGE')
                seen.add(key);degree[a]+=1;degree[b]+=1;graph[a].add(b);graph[b].add(a)
            reached=set();pending=[labels[0]]
            while pending:
                a=pending.pop()
                if a not in reached:reached.add(a);pending.extend(graph[a]-reached)
            if reached != set(labels) or set(degree.values()) != {2}:
                raise ValueError('REALIZATION_CYCLE')
            total += len(seen)
        matrices=set()
        for i,row in enumerate(self.rotations):
            m=row['matrix'];a,b,c=m
            det=a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
            if row['rotation_class'] != i or det != 1 or any(sum(m[k][j]**2 for k in range(3))!=1 for j in range(3)):
                raise ValueError('REALIZATION_ROTATION')
            q=norm(row['quaternion_wxyz']);w,x,y,z=q
            qm=[[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]]
            if any(abs(qm[j][k]-m[j][k])>1e-9 for j in range(3) for k in range(3)):
                raise ValueError('REALIZATION_ROTATION')
            matrices.add(tuple(v for r in m for v in r))
        if total != 295 or len(self.rotations) != 24 or len(matrices) != 24:
            raise ValueError('REALIZATION_AUTHORITY')
        if any(not 0 <= fg['rotation_class'] < 24 for fg in self.corpus.fgs.values()):
            raise ValueError('REALIZATION_ROTATION')

    def target(self, handle, phi):
        q=self.rotations[self.corpus.fgs[handle]['rotation_class']]['quaternion_wxyz']
        return norm(multiply([math.cos(phi/2),0,0,math.sin(phi/2)],q))

    def evaluate(self, mid, copies, poses, previous=None):
        """No mutation. Required edges have independent source and endpoint proofs."""
        self.verify()
        w=self.witnesses[mid]; labels=[s['field_generator'] for s in w['generator_slots']]
        if Counter(copies.values()) != Counter(labels):
            raise ValueError('REALIZATION_MEMBERSHIP')
        ids={handle:identity for identity,handle in copies.items()}
        ordered=[ids[g] for g in labels]
        if any(poses[i]['value'] is None for i in ordered):
            return None
        values=[poses[i]['value'] for i in ordered]
        points=[[v['x']/v['xy_scale'],v['y']/v['xy_scale']] for v in values]
        fit=se2([s['xy'] for s in w['generator_slots']],points)
        targets=[self.target(g,fit['phi']) for g in labels]
        angles=[distance(v['quaternion_wxyz'],t) for v,t in zip(values,targets)]
        sh=self.snap['shape_fit']['thresholds'];oh=self.orientation['thresholds_degrees']
        shape_capture=within(fit['rms'],sh['capture_rms_max']) and within(fit['max'],sh['capture_slot_max'])
        shape_candidate=within(fit['rms'],sh['candidate_rms_max']) and within(fit['max'],sh['candidate_slot_max'])
        retained=previous and previous.get('manifold_id') == mid
        shape_magnetic=shape_capture or (retained and previous.get('shape_stage')=='MAGNETIZED' and within(fit['max'],sh['release_slot_min']))
        orient_capture=all(within(a,oh['capture']) for a in angles)
        orient_magnetic=orient_capture or (retained and previous.get('orientation_stage')=='MAGNETIZED' and within(max(angles),oh['release']))
        orientation_stage='MAGNETIZED' if orient_magnetic else ('CANDIDATE' if within(max(angles),oh['candidate']) else 'FREE')
        shape_stage='MAGNETIZED' if shape_magnetic else ('CANDIDATE' if shape_candidate else 'FREE')
        edge_proofs=[];captured={g:within(a,oh['capture']) for g,a in zip(labels,angles)}
        for edge in w['required_cycle_edges']:
            a,b=edge['a'],edge['b']; row=self.corpus.compatibility[tuple(sorted((a,b)))]
            # Preserve source direction and every supplied match. The selected match
            # is deterministic; no socket consumption or board-bearing constraint.
            edge_proofs.append({'a':ids[a],'b':ids[b],'a_revision':poses[ids[a]]['revision'],
                'b_revision':poses[ids[b]]['revision'],'source':copy.deepcopy(row),
                'selected_match':copy.deepcopy(row['matches'][0]),
                'a_face':row['matches'][0]['a_face' if row['a']==a else 'b_face'],
                'b_face':row['matches'][0]['b_face' if row['b']==b else 'a_face'],
                'signature':row['matches'][0]['signature'],'interaction':edge['interaction'],
                'live':bool(captured[a] and captured[b])})
        transform={'phi_hex':fit['phi'].hex(),'translation_hex':[v.hex() for v in fit['translation']]}
        return {'manifold_id':mid,'authority':self.hash,'shape_stage':shape_stage,'orientation_stage':orientation_stage,
            'stage':'MAGNETIZED' if shape_magnetic and orient_magnetic else ('CANDIDATE' if shape_stage!='FREE' else 'FREE'),
            'shape_capture':shape_capture,'orientation_capture':orient_capture,
            'rms_nano':round(fit['rms']*SCALE),'max_error_nano':round(fit['max']*SCALE),
            'orientation_microdegrees':{i:round(a*1_000_000) for i,a in zip(ordered,angles)},
            'can_lock':shape_capture and orient_capture and all(e['live'] for e in edge_proofs),
            'edges':edge_proofs,'transform':transform,
            'targets':{i:{'x':round(p[0]*SCALE),'y':round(p[1]*SCALE),'xy_scale':SCALE,
                           'quaternion_wxyz':projective(q),
                           'symbolic':{'manifold_id':mid,'slot':s['slot'],'transform':copy.deepcopy(transform),
                                       'rotation_class':self.corpus.fgs[g]['rotation_class'],'authority':self.hash}}
                       for i,g,s,p,q in zip(ordered,labels,w['generator_slots'],fit['fitted'],targets)}}

    def locked_pose(self, target):
        return dict(copy.deepcopy(target),schema='xy-quaternion-integer-v1',
                    frame='configuration-realization-v1',mapping_status='LOCKED')
