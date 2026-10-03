"""Native Pass-06 fixture; all gameplay enters the compiled package/byte fence."""
from pass_05_support import MatchFixture

DRAW='source:data/cycles/cycle_01/utilities/draw_deck.json#/values/slots/'
RECOVERY='source:data/cycles/cycle_01/utilities/recovery.json#/values/slots/'
TRANSDUCTION='source:data/cycles/cycle_01/utilities/transduction.json#/values/'
WHITE='source:data/cycles/cycle_01/utilities/restore_prime.json#'


class HeadlessFixture(MatchFixture):
    def __init__(self, identity='pass06-headless'):
        super().__init__(identity)

    def setup_player(self,player='player_1',primes=('restore_white','degrade_violet','universal_green'),manifolds=(),utilities=()):
        return super().setup_player(player,primes,manifolds,utilities)

    def setup(self,first='player_1'):
        return self.perform('P6_SETUP_MATCH',{'first_player':first},effect={'policy':'TRUSTED_FAIR_BINARY_SETUP','outcome':first})

    def mulligan(self,selected=(),player='player_1',seed='pass06-trusted-shuffle-seed'):
        return self.perform('P6_MULLIGAN',{'cards':list(selected)},player,effect={'policy':'TRUSTED_MULLIGAN_SHUFFLE','seed':seed})

    def keep(self):
        for player in ('player_1','player_2'):self.mulligan(player=player)

    def control(self,op):
        return self.perform('P6_'+op,player=self.color.state['active_player'],effect={'policy':'TRUSTED_MATCH_CONTROL'})

    def generate(self,field,prime,player='player_1'):
        return self.perform('P6_GENERATE_CHARGE',self.generate_args(field,prime),player)

    def spend(self,prime,target,amount,direction,player='player_1'):
        return self.perform('P6_SPEND_CHARGE',self.spend_args(prime,target,amount,direction),player)

    def respond(self,prime,target,amount,field=None):
        return self.perform('P6_DEFENSE_RESTORE',self.response_args(prime,target,amount,field),self.tempo.state['defense']['owner'])

    def pass_defense(self,timeout=False):
        return self.perform('P6_DEFENSE_PASS',{'window':self.tempo.state['defense']['id'],'reason':'TIMEOUT' if timeout else 'PASS'},
            self.tempo.state['defense']['owner'],effect={'policy':'TRUSTED_DEFENSE_TIMEOUT'} if timeout else {})

    def utility_args(self,card,cards=(),target=None,direction='NONE'):
        kind='prime' if target in self.color.state['primes'] else 'field' if target in self.ext.state['fields'] else 'NONE'
        revision=self.color.state['primes'][target]['revision'] if kind=='prime' else self.ext.state['fields'][target]['color_revision'] if kind=='field' else 0
        return {'utility':card,'cards':list(cards),'target':target or 'NONE','target_kind':kind,'target_revision':revision,'direction':direction}

    def play(self,card,cards=(),target=None,direction='NONE',player='player_1'):
        effect=self.effect(card);effect['seed']='pass06-trusted-deep-survey-seed'
        return self.perform('P6_UTILITY',self.utility_args(card,cards,target,direction),player,effect=effect)

    def look(self,card,player='player_1'):
        return self.perform('P6_LOOK_UTILITY',{'utility':card},player,effect=self.effect(card))
