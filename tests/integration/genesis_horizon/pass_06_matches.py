"""Reproducible complete matches for tests, offline scene, and Vera evidence."""
import copy
from pass_06_support import DRAW,TRANSDUCTION

RESTORE6=TRANSDUCTION+'restore/5'


def prime_match(f, checkpoint_last=False):
    primes,fields=f.setup_player(utilities=[RESTORE6,DRAW+'0'],manifolds=['M-G-01'])
    enemy,defenders=f.setup_player('player_2',manifolds=['M-G-01'])
    f.setup();f.keep();f.start()
    restore=f.utility(RESTORE6);attack=primes[1]
    f.generate(fields[0],attack);f.play(restore,target=attack,direction='RESTORE')
    f.spend(attack,enemy[0],1,'DEGRADE')
    assert f.tempo.defense_open
    assert f.color.state['primes'][enemy[0]]['H']==6
    f.respond(enemy[0],enemy[0],4,defenders[0])
    assert (f.color.state['primes'][enemy[0]]['H'],f.q(enemy[0]))==(7,3)
    f.play(restore,target=attack,direction='RESTORE')
    f.spend(attack,enemy[0],10,'DEGRADE')
    assert f.color.state['primes'][enemy[0]]['state']=='INACTIVE'
    f.play(restore,target=attack,direction='RESTORE')
    f.spend(attack,enemy[1],6,'DEGRADE')
    assert f.tempo.state['status']=='RUNNING'
    request=f.request('P6_SPEND_CHARGE',f.spend_args(attack,enemy[2],4,'DEGRADE'))
    before=copy.deepcopy(f.horizon._backend.application_values)
    checkpoint=f.restart() if checkpoint_last else None
    if checkpoint_last:assert f.horizon._backend.application_values==before
    else:
        # Restart reconnects both Port views through HELLO/OBSERVE. Replay the
        # same observable inputs on the uninterrupted run so Road indices and
        # the native transport transcript are being compared like-for-like.
        for player in ('player_1','player_2'):f.hello(player)
    f.horizon.execute(request,f.players['player_1'])
    assert f.tempo.state['status']=='MATCH_COMPLETE' and f.tempo.state['winner']=='player_1'
    return {'ending':'PRIME_ATTACK','checkpoint':checkpoint,'root':f.horizon._state['root'],
            'history':copy.deepcopy(f.tempo.state['history']),'road_count':len(f.horizon._backend.road_history),
            'all_road_audits':all(f.color.audit_road(r)['pass'] for r in f.horizon._backend.road_history)}


def exhaustion_match(f):
    primes,fields=f.setup_player(utilities=[RESTORE6,DRAW+'0',DRAW+'5'],manifolds=['M-G-01'])
    f.setup_player('player_2');f.setup();f.keep();f.start()
    restore=f.utility(RESTORE6);exchange=f.utility(DRAW+'5');draw=f.utility(DRAW+'0')
    for _ in range(4):f.play(restore,target=primes[0],direction='RESTORE')
    # Empty a real constructed Deck through accepted Exchange, preserving all
    # 60 native identities. No collection/state injection or draw bypass.
    while f.members('player_1_deck'):
        ids=[i for i in f.members('player_1_hand') if f.horizon._backend.application_values['cards'][i]['category']=='Field Generator']
        ids=ids[:min(len(ids),len(f.members('player_1_deck')))]
        assert ids
        f.play(exchange,ids)
    stages=[]
    while f.tempo.state['status']!='MATCH_COMPLETE':
        hand=list(f.members('player_1_hand'))
        if not stages:
            f.next_turn();f.next_turn()  # First exhaustion is an actual own-turn normal draw.
        else:f.play(draw)
        assert f.members('player_1_hand')==hand
        stages.append(copy.deepcopy(f.tempo.state['exhaustion']['player_1']))
        if f.tempo.defense_open:
            if len(stages)==7:f.respond(primes[0],primes[0],4,fields[0])
            else:f.pass_defense(timeout=len(stages)==2)
        assert len(stages)<20
    assert f.tempo.state['winner']=='player_2'
    assert f.tempo.state['history'][-1]['event']=='MATCH_COMPLETE'
    assert sum(row['event']=='MATCH_COMPLETE' for row in f.tempo.state['history'])==1
    assert [s['color'] for s in stages[:7]]==['RED','ORANGE','YELLOW','GREEN','BLUE','VIOLET','WHITE']
    assert [s['magnitude'] for s in stages[:7]]==list(range(1,8))
    assert len(stages)>=10 and all(s['magnitude']==7 and s['color']=='WHITE' for s in stages[7:])
    assert list(dict.fromkeys(s['target'] for s in stages))==primes
    return {'ending':'EXHAUSTION','root':f.horizon._state['root'],'stages':stages,
            'history':copy.deepcopy(f.tempo.state['history']),'road_count':len(f.horizon._backend.road_history),
            'all_road_audits':all(f.color.audit_road(r)['pass'] for r in f.horizon._backend.road_history)}
