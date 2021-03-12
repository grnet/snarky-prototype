
class Prover(object):
    pass

class Verifier(object):
    pass


# Setup

from collections import namedtuple

Tau = namedtuple('Tau', ['alpha', 'beta', 'delta', 'x'])   # τ = (α, β, δ, x) E (Z_p)*

def extract_tau(tau):
    return tau.alpha, tau.beta, tau.delta, tau.x


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
            map(lambda i: self.coeffs[i] * x ** i, range(0, len(self.coeffs))), 
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


def generate_srs_u(ctx, tau, n):
    srs_u = [[], []]

    G = ctx.G
    H = ctx.H

    alpha, beta, _, x = extract_tau(tau)
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

def generate_srs_s(ctx, tau, qap):
    assert ctx.p == qap.p
    p = ctx.p
    G = ctx.G
    H = ctx.H
    

    alpha, beta, delta, x = extract_tau(tau)

    # TODO: Implement and apply QAP extraction
    u = qap.u
    v = qap.u
    w = qap.v
    t = qap.t
    m = qap.m
    n = qap.n
    l = qap.l

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

def setup(ctx, tau, qap):
    srs_u = generate_srs_u(ctx, tau, n=qap.n)
    srs_s = generate_srs_s(ctx, tau, qap)
    srs = (srs_u, srs_s)
    return srs, tau


# Utils

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

def generate_trapdoor(ctx):
    # TODO: Provide default values for alpha, beta, delta, x
    p = ctx.p
    alpha = randstar(p)
    beta = randstar(p)
    delta = randstar(p)
    x = randstar(p)
    tau = Tau(alpha, beta, delta, x)
    return tau

CTX = namedtuple('CTX', ['p', 'G', 'H'])

def create_algebraic_context():
    from bplib import bp
    G_T = bp.BpGroup()                      # bilinear pairing G_1 x G_2 -> G_T
    ctx = CTX(
        p=G_T.order(),                      # order of G_T
        G=G_T.gen1(),                       # generator of G_1
        H=G_T.gen2(),                       # generator of G_2
    )
    return ctx



if __name__ == '__main__':
    print('Snarky Ceremonies')

    ctx = create_algebraic_context()
    tau = generate_trapdoor(ctx)                # τ = (α, β, δ, x), α, β, δ, x E (Z_p)* random

    # QAP

    # m=5, n=4, l=3

    u = [Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0])]
    v = [Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0])]
    w = [Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0]), Poly([1, 0, 0, 0])]
    t = Poly([1, 0, 0, 0, 0])
    L = 3

    qap = QAP(ctx, u, v, w, t, l=L)

    # SRS generation

    srs, trapdoor = setup(ctx, tau, qap)
    assert trapdoor == tau
    print(srs)
