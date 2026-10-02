"""Actual package/byte-fence fixture with an explicit conformance effect issuer."""
from pass_04_support import PrimeFixture


class MatchFixture(PrimeFixture):
    def __init__(self, identity='pass05-match'):
        super().__init__(identity)

    @property
    def tempo(self):
        return self.ext.tempo

    def perform(self,*args,**kwargs):
        request,messages=super().perform(*args,**kwargs)
        assert messages[0]['payload']['status']=='COMMITTED',messages
        return request,messages

    def setup_player(self,player='player_1',primes=(),manifolds=(),utilities=()):
        if not utilities:
            return super().setup_player(player,primes,manifolds)
        records=self.horizon._backend.collections.catalog['records']
        keys={r['record']['identity_key']:h for h,r in records.items() if r['category']=='Prime'}
        roster=[keys[p] for p in primes]+[g for m in manifolds for g in self.ext.corpus.base[m]['generators']]+list(utilities)
        for n in range(1,121):
            g=f'FG-{n:03}'
            while roster.count(g)<2 and len(roster)<60:roster.append(g)
        self.initialize(roster,player);bound=[];fields=[]
        for index,p in enumerate(primes):
            identity=next(i for i in self.members(player+'_deck') if self.horizon._backend.application_values['cards'][i]['catalog']==keys[p])
            self.perform('BIND_PRIME',{'cards':[identity],'destination':player+'_prime_'+str(index+1)},player)
            bound.append(identity)
        for index,mid in enumerate(manifolds):
            space=player+'_config_'+chr(65+index);ids=[]
            for _ in self.ext.corpus.base[mid]['generators']:
                self.perform('DRAW_ONE',player=player);identity=self.members(player+'_hand')[0]
                self.perform('COMMIT_FG',{'cards':[identity],'destination':space},player);ids.append(identity)
            group=(space,mid,ids);self.groups[space]=group
            self.perform('SET_FG_POSES',self.poses(group),player)
            self.perform('RESOLVE_CONFIGURATION',self.space_args(space),player)
            fields.append(self.ext.state['spaces'][space]['active_field'])
        return bound,fields

    def setup(self,first='player_1'):
        return self.perform('SETUP_MATCH',{'first_player':first},effect={'policy':'TRUSTED_FAIR_BINARY_SETUP','outcome':first})

    def control(self,op):
        return self.perform(op,player=self.color.state['active_player'],effect={'policy':'TRUSTED_MATCH_CONTROL'})

    def start(self):
        self.control('BEGIN_TURN');self.control('NORMAL_DRAW')

    def next_turn(self):
        self.control('END_ACTIVE');self.control('ADVANCE_TURN');self.start()

    def generate(self,field,prime,player='player_1'):
        return self.perform('GENERATE_CHARGE',self.generate_args(field,prime),player)

    def spend_args(self,prime,target,amount,direction):
        args=super().spend_args(prime,target,amount,direction);args['amount']=str(amount)
        return args

    def spend(self,prime,target,amount,direction,player='player_1'):
        return self.perform('SPEND_CHARGE',self.spend_args(prime,target,amount,direction),player)

    def response_args(self,prime,target,amount,field=None):
        args=self.spend_args(prime,target,amount,'RESTORE');args.pop('direction')
        return dict(args,window=self.tempo.state['defense']['id'],field=field or 'NONE',
                    field_revision=self.ext.state['fields'][field]['color_revision'] if field else 0)

    def respond(self,prime,target,amount,field=None):
        return self.perform('DEFENSE_RESTORE',self.response_args(prime,target,amount,field),self.tempo.state['defense']['owner'])

    def pass_defense(self,timeout=False):
        return self.perform('DEFENSE_PASS',{'window':self.tempo.state['defense']['id'],'reason':'TIMEOUT' if timeout else 'PASS'},
            self.tempo.state['defense']['owner'],effect={'policy':'TRUSTED_DEFENSE_TIMEOUT'} if timeout else {})

    def effect(self,card):
        return {'policy':'ADMITTED_CARD_EFFECT','card':card,'timing':{'phase':self.tempo.state['phase'],
                'turn':self.tempo.state['turn'],'window':self.tempo.state['defense']['id'] if self.tempo.defense_open else None}}

    def utility(self,handle,player='player_1'):
        return next(i for i in self.members(player+'_hand') if self.horizon._backend.application_values['cards'][i]['catalog']==handle)

    def q(self,prime):
        return self.tempo.nodes.quantity(self.color.state['primes'][prime])
