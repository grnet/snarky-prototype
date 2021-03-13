from collections import namedtuple


from snarky_ceremonies.utils import bp, randstar

CTX = namedtuple('CTX', ['p', 'G', 'H'])

def create_algebraic_context():
    group = bp.BpGroup()            # bilinear pairing G_1 x G_2 -> G_T
    p = group.order()               # order of G_T
    G = group.gen1()                # generator of G_1
    H = group.gen2()                # generator of G_2
    return CTX(p, G, H)


from snarky_ceremonies.utils import toBn

Trapdoor = namedtuple('Trapdoor', ['alpha', 'beta', 'delta', 'x'])   # τ = (α, β, δ, x) E (Z_p)*

def generate_trapdoor(ctx, alpha=None, beta=None, delta=None, x=None):
    p = ctx.p
    args = (randstar(p) if num is None else toBn(num) 
        for num in (alpha, beta, delta, x))
    trapdoor = Trapdoor(*args)
    return trapdoor


from snarky_ceremonies.algebra import Poly

class QAP(object):

    def __init__(self, ctx, u, v, w, t, l):
        self.p = ctx.p
        m = len(u) - 1
        assert len(v) == m + 1 
        assert len(w) == m + 1
        self.m = m
        assert l + 1 <= m
        self.l = l
        n = t.degree()
        self.t = t
        self.n = n
        for i in range(0, m + 1):
            assert u[i].degree() == n - 1
            assert v[i].degree() == n - 1
            assert w[i].degree() == n - 1
        self.u = u
        self.v = v
        self.w = w

    @classmethod
    def create_default(cls, ctx, m, n, l):
        u = [Poly([1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        v = [Poly([1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        w = [Poly([1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        t = Poly([1] + n * [0])
        return cls(ctx, u, v, w, t, l)

    def polynomials(self):
        u = self.u
        v = self.v
        w = self.w
        t = self.t
        return u, v, w, t

    def dimensions(self):
        m = self.m
        n = self.n
        l = self.l
        return m, n, l


from snarky_ceremonies.srs import generate_srs_u, generate_srs_s

def setup(ctx, trapdoor, qap):
    srs_u = generate_srs_u(ctx, trapdoor, qap)
    srs_s = generate_srs_s(ctx, trapdoor, qap)
    srs = (srs_u, srs_s)
    return srs, trapdoor
