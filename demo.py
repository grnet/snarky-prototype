
class Prover(object):
    pass

class Verifier(object):
    pass


# Setup

from collections import namedtuple

Trapdoor = namedtuple('Trapdoor', ['alpha', 'beta', 'delta', 'x'])   # τ = (α, β, δ, x) E (Z_p)*

class Poly(object):

    def __init__(self, coeffs):
        assert len(coeffs) >= 1
        self.coeffs = list(map(toBn, coeffs))

    def degree(self):
        return len(self.coeffs) - 1

    def coeff(self, i):
        return self.coeffs[i]

    def eval(self, x):
        return sum(
            map(
                lambda i: self.coeffs[i] * x ** i,      # TODO: mod p
                range(0, len(self.coeffs))
            ), 
            bnZero()
        )


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
        return QAP(ctx, u, v, w, t, l)

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


def generate_srs_u(ctx, trapdoor, qap):
    _, G, H = ctx
    alpha, beta, _, x = trapdoor
    n = qap.n

    srs_u = [[], []]
    for i in range(0, 2 * n -1):                # 0 <= i <= 2n - 2
        srs_u[0].append((
            (x ** i) * G,                       # (x ^ i) * G
            (x ** i) * H,                       # (x ^ i) * H
        ))
    for i in range(0, n):                       # 0 <= i <= n - 1
        srs_u[1].append((
            (alpha * x ** i) * G,               # (α x ^ i) * G 
            (beta  * x ** i) * G,               # (β x ^ i) * G 
            (alpha * x ** i) * H,               # (α x ^ i) * H
            (beta  * x ** i) * H,               # (β x ^ i) * H 
        ))
    return srs_u


def generate_srs_s(ctx, trapdoor, qap):
    assert ctx.p == qap.p

    p, G, H = ctx
    alpha, beta, delta, x = trapdoor
    u, v, w, t = qap.polynomials()
    m, n, l = qap.dimensions()

    srs_s = [
        delta * G,                                              # δ * G
        delta * H,                                              # δ * Η
        [],
        [],
    ]

    for i in range(l + 1, m + 1):                                                                       # l + 1 <= i <= m
        srs_s[2].append(
            ((beta * u[i].eval(x) + alpha * v[i].eval(x) + w[i].eval(x)) * delta.mod_inverse(p)) * G    # ((β * u_i(x) + α * v_i(x) + w_i(x)) / δ) * G
        )
    for i in range(0, n - 1):                                                                           # 0 <= i <= n - 2
        srs_s[3].append(
            (x ** i * t.eval(x) * delta.mod_inverse(p)) * G                                             # ((x ^ i * t(x)) / δ) * G
        )
    return srs_s

def setup(ctx, trapdoor, qap):
    srs_u = generate_srs_u(ctx, trapdoor, qap)
    srs_s = generate_srs_s(ctx, trapdoor, qap)
    srs = (srs_u, srs_s)
    return srs, trapdoor


# Utils

from bplib import bp
from petlib import bn

def toBn(num):
    return bn.Bn.from_decimal(str(num))

def bnZero():
    return toBn(0)

def randstar(p):
    """
    Generate a random element of the prime field (Z_p)*
    """
    return (p - 1).random()

def generate_trapdoor(ctx, alpha=None, beta=None, delta=None, x=None):
    p = ctx.p
    args = (randstar(p) if num is None else toBn(num) 
        for num in (alpha, beta, delta, x))
    trapdoor = Trapdoor(*args)
    return trapdoor

CTX = namedtuple('CTX', ['p', 'G', 'H'])

def create_algebraic_context():
    group = bp.BpGroup()            # bilinear pairing G_1 x G_2 -> G_T
    p = group.order()               # order of G_T
    G = group.gen1()                # generator of G_1
    H = group.gen2()                # generator of G_2
    return CTX(p, G, H)


if __name__ == '__main__':
    print('Snarky Ceremonies')

    # Context
    ctx = create_algebraic_context()
    trapdoor = generate_trapdoor(ctx)
    qap = QAP.create_default(ctx, m=5, n=4, l=3)

    # SRS generation
    srs, trapdoor = setup(ctx, trapdoor, qap)
    assert trapdoor == trapdoor
    print(srs)
