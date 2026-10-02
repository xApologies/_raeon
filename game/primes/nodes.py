"""Canonical Pass-05 Prime value ABI, bound to verified native INT programs.

N/R encode Q; they are not extra health or new QMO identities. Decomposition
uses integer quotient/remainder as a representation codec and verifies its
reconstruction through native INT add/equal, with at most seven rank additions.
No loop or allocation scales with the number of charge nodes.
"""

ABI = 'raeon-prime-charge-nodes-v1'
COLORS = [None, 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'WHITE']


def reject():
    raise ValueError('ADMISSION_REJECTED')


def quantity(p):
    return p['N'] * p['H_max'] + p['R']


def state(h, q, rank):
    if h == 0:
        return 'INACTIVE'
    if h < rank:
        return 'DAMAGED_NON_OPERATIONAL'
    return 'OPERATIONAL_CHARGED' if q else 'HEALTHY_UNCHARGED'


class Values:
    def __init__(self, interpreter):
        self.vm = interpreter

    def add(self, a, b):
        return self.vm.run_integer('add', a, b)

    def encode(self, h, q, rank):
        if (any(type(v) is not int for v in (h, q, rank)) or not 1 <= rank <= 7 or
                not 0 <= h <= rank or q < 0 or (h < rank and q)):
            reject()
        n, remainder = divmod(q, rank)
        reconstructed = remainder
        for _ in range(rank):
            reconstructed = self.add(reconstructed, n)
        if not self.vm.run_integer('equal', reconstructed, q):
            reject()
        return h, n, remainder

    def validate(self, p):
        if ('C' in p or 'C_max' in p or any(type(p.get(k)) is not int for k in ('H','N','R','H_max','revision')) or
                p['N'] < 0 or not 0 <= p['R'] < p['H_max'] or p['revision'] < 0):
            reject()
        q = quantity(p)
        if self.encode(p['H'],q,p['H_max']) != (p['H'],p['N'],p['R']) or p['state'] != state(p['H'],q,p['H_max']):
            reject()

    def restore(self, p, amount):
        if type(amount) is not int or amount <= 0 or p['H'] == 0:
            reject()
        heal = min(amount, p['H_max']-p['H'])
        h = self.add(p['H'], heal)
        q = self.add(quantity(p), self.add(amount, -heal))
        return self.encode(h,q,p['H_max'])

    def degrade(self, p, amount):
        if type(amount) is not int or amount <= 0 or p['H'] == 0:
            reject()
        q = quantity(p)
        shield = min(amount,q)
        remaining = self.add(amount,-shield)
        return self.encode(self.add(p['H'],-min(p['H'],remaining)),self.add(q,-shield),p['H_max'])

    def spend(self, p, amount):
        q = quantity(p)
        if type(amount) is not int or not 0 < amount <= q or p['H'] != p['H_max']:
            reject()
        return self.encode(p['H'],self.add(q,-amount),p['H_max'])

    def migrate(self, p):
        h,n,r = self.encode(p['H'],p['C'],p['H_max'])
        p.pop('C'); p.pop('C_max')
        p.update(H=h,N=n,R=r,state=state(h,n*p['H_max']+r,p['H_max']))

    @staticmethod
    def assign(p, result):
        h,n,r = result
        p.update(H=h,N=n,R=r,state=state(h,n*p['H_max']+r,p['H_max']),revision=p['revision']+1)

    @staticmethod
    def projection(p):
        fields = {k:p[k] for k in ('slot','identity_key','family','rank','H_max','H','R','state','revision')}
        # These are exact decimal encodings, not lossy JavaScript numbers.
        fields.update(N=str(p['N']),Q=str(quantity(p)),node_color=COLORS[p['H_max']],
                      remainder_color=COLORS[p['R']],charge_encoding='DECIMAL_INTEGER')
        return fields
