"""Pass-4 conformance issuer; all game actions cross the real byte boundary."""
from pass_03b_support import FieldFixture


class PrimeFixture(FieldFixture):
    def __init__(self, identity='pass04-match'):
        super().__init__(identity)
        self.groups = {}

    @property
    def color(self):
        return self.ext.color

    def setup_player(self, player='player_1', primes=(), manifolds=()):
        records = self.horizon._backend.collections.catalog['records']
        keys = {r['record']['identity_key']:h for h,r in records.items() if r['category']=='Prime'}
        roster = [keys[p] for p in primes]+[g for m in manifolds for g in self.ext.corpus.base[m]['generators']]
        for n in range(1,121):
            g=f'FG-{n:03}'
            while roster.count(g)<2 and len(roster)<60:
                roster.append(g)
        self.initialize(roster,player)
        bound = []
        for index,p in enumerate(primes):
            identity = next(i for i in self.members(player+'_deck') if self.horizon._backend.application_values['cards'][i]['catalog']==keys[p])
            self.perform('BIND_PRIME',{'cards':[identity],'destination':player+'_prime_'+str(index+1)},player)
            bound.append(identity)
        fields = []
        for index,mid in enumerate(manifolds):
            space=player+'_config_'+chr(65+index);ids=[]
            for _ in self.ext.corpus.base[mid]['generators']:
                self.perform('DRAW_ONE',player=player)
                identity=self.members(player+'_hand')[0]
                self.perform('COMMIT_FG',{'cards':[identity],'destination':space},player)
                ids.append(identity)
            group=(space,mid,ids);self.groups[space]=group
            self.perform('SET_FG_POSES',self.poses(group),player)
            self.perform('RESOLVE_CONFIGURATION',self.space_args(space),player)
            fields.append(self.ext.state['spaces'][space]['active_field'])
        return bound,fields

    def active(self, player):
        return self.perform('SET_ACTIVE_PLAYER',{'active_player':player},effect={'policy':'TRUSTED_MATCH_CONTROL'})

    def refresh(self, fields, player='player_1'):
        return self.perform('REFRESH_FIELDS',{'fields':fields},player,effect={'policy':'TRUSTED_MATCH_CONTROL'})

    def generate_args(self, field, prime):
        return {'field':field,'field_revision':self.ext.state['fields'][field]['color_revision'],
                'prime':prime,'prime_revision':self.color.state['primes'][prime]['revision']}

    def generate(self, field, prime, player='player_1'):
        return self.perform('GENERATE_FIELD',self.generate_args(field,prime),player)

    def spend_args(self, prime, target, amount, direction):
        target_state=self.color.state['primes'].get(target) or self.ext.state['fields'][target]
        return {'prime':prime,'prime_revision':self.color.state['primes'][prime]['revision'],
                'target':target,'target_revision':target_state.get('revision',target_state.get('color_revision')),
                'amount':amount,'direction':direction}

    def spend(self, prime, target, amount, direction, player='player_1'):
        return self.perform('SPEND_PRIME',self.spend_args(prime,target,amount,direction),player)

    def white(self, prime, player='player_1', admitted=True):
        return self.perform('WHITE_RESTORE_PRIME',{'prime':prime,'prime_revision':self.color.state['primes'][prime]['revision']},
                            player,effect={'policy':'ADMITTED_WHITE_RESTORE_PRIME'} if admitted else {})

    def restart(self):
        result=super().restart()
        self.ext=self.horizon._backend.collections.extension
        return result
