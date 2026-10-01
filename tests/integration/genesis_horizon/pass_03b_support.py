"""Real package/Hypervisor fixture; authority is the existing conformance issuer."""
import copy
import math

from pass_02_support import CardFixture


class FieldFixture(CardFixture):
    def __init__(self, identity='pass03b-match'):
        super().__init__(identity)
        self.ext = self.horizon._backend.collections.extension

    def prepare(self, manifolds):
        handles=[g for mid in manifolds for g in self.ext.corpus.base[mid]['generators']]
        roster=list(handles)
        for n in range(1,121):
            g=f'FG-{n:03}'
            while roster.count(g)<2 and len(roster)<60:roster.append(g)
        self.initialize(roster)
        groups=[]
        for index,mid in enumerate(manifolds):
            space='player_1_config_'+chr(65+index)
            ids=[]
            for _ in self.ext.corpus.base[mid]['generators']:
                self.perform('DRAW_ONE')
                card=self.members('player_1_hand')[0]
                self.perform('COMMIT_FG',{'cards':[card],'destination':space})
                ids.append(card)
            groups.append((space,mid,ids))
        return groups

    def space_args(self, space):
        return {'space':space,'membership_revision':self.ext.state['spaces'][space]['membership_revision']}

    def poses(self, group, phi=0.0, translation=(0,0), distort=None, angle=0):
        space,mid,ids=group
        by_handle={self.horizon._backend.application_values['cards'][i]['catalog']:i for i in ids}
        rows=[]
        for slot in self.ext.realization.witnesses[mid]['generator_slots']:
            x,y=slot['xy'];g=slot['field_generator'];identity=by_handle[g]
            x,y=math.cos(phi)*x-math.sin(phi)*y+translation[0],math.sin(phi)*x+math.cos(phi)*y+translation[1]
            if distort:x,y=distort(slot,x,y)
            q=self.ext.realization.target(g,phi+math.radians(angle))
            rows.append(dict(card=identity,x=round(x*1000),y=round(y*1000),
                **dict(zip(('qw','qx','qy','qz'),[round(v*1_000_000) for v in q])),
                pose_revision=self.ext.state['poses'][identity]['revision']))
        return dict(self.space_args(space),poses=rows)

    def position(self, group, **kwargs):
        return self.perform('SET_FG_POSES',self.poses(group,**kwargs))

    def resolve(self, group):
        return self.perform('RESOLVE_CONFIGURATION',self.space_args(group[0]))

    def ready(self, manifolds):
        groups=self.prepare(manifolds)
        for group in groups:self.position(group);self.resolve(group)
        return groups

    def merge_args(self, left, right):
        return dict(self.space_args(left),other=right,
                    other_membership_revision=self.ext.state['spaces'][right]['membership_revision'])

    def snapshot(self):
        return copy.deepcopy((self.horizon._record(),self.horizon._state))
