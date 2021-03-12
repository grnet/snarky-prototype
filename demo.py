
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

    def __init__(self, p, u, v, w, t, n, m, l):

        # Compatibility checks

        assert l + 1 <= m
        assert len(u) == m + 1
        assert len(v) == m + 1
        assert len(w) == m + 1
        assert t.degree() == n
        for i in range(0, m + 1):
            assert u[i].degree() == n - 1
            assert v[i].degree() == n - 1
            assert w[i].degree() == n - 1

        # Set parameters

        self.p = p
        self.u = u
        self.v = v
        self.w = w
        self.t = t
        self.n = n
        self.m = m
        self.l = l


def generate_srs_u(tau, G, H, n):
    srs_u = [[], []]
    alpha, beta, _, x = extract_tau(tau)
    for i in range(0, 2 * n -1):                # 0 <= i <= 2n - 2
        srs_u[0].append((
            (x ** i) * G,                       # (x ^ i) * G
            (x ** i) * H,                       # (x ^ i) * H
        ))
    for i in range(0, N):                       # 0 <= i <= n - 1
        srs_u[1].append((
            (alpha * x ** i) * G,               # (α x ^ i) * G 
            (beta  * x ** i) * G,               # (β x ^ i) * G 
            (alpha * x ** i) * H,               # (α x ^ i) * H
            (beta  * x ** i) * H,               # (β x ^ i) * H 
        ))
    return srs_u

def generate_srs_s(tau, G, H, qap):
    alpha, beta, delta, x = extract_tau(tau)

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

def setup(tau, G, H, qap):
    srs_u = generate_srs_u(tau, G, H, n=qap.n)
    srs_s = generate_srs_s(tau, G, H, qap)
    srs = (srs_u, srs_s)
    return srs, tau


# Utils

from petlib import bn

def toBn(num):
    return bn.Bn.from_decimal(str(num))

def bnZero():
    return toBn(0)

def mk_rand(p):
    """
    Generate a random element of the field (Z_p) ^ *, p prime.

    :type p: petlib.bn.Bn
    :rtype: petlib.bn.Bn

    """
    return (p - 1).random()

def mk_random_tau(group):
    p = group.order()
    alpha = mk_rand(p)
    beta = mk_rand(p)
    delta = mk_rand(p)
    x = mk_rand(p)
    tau = Tau(alpha, beta, delta, x)
    return tau


if __name__ == '__main__':
    print('Snarky Ceremonies')

    from bplib import bp

    # Create algebraic context

    G_T = bp.BpGroup()                      # bilinear pairing G_1 x G_2 -> G_T
    p = G_T.order()                         # p = order(G_T)
    G, H = G_T.gen1(), G_T.gen2()           # G_1 = <G>, G_2 = <H>

    # Trapdoor

    tau = mk_random_tau(G_T)                # τ = (α, β, δ, x), α, β, δ, x E (Z_p)^* random

    # QAP

    M = 5
    N = 4
    L = 3

    u = [Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0])]
    v = [Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0])]
    w = [Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0]), Poly([0, 0, 0, 0])]
    t = Poly([0, 0, 0, 0, 0])

    qap = QAP(p, u, v, w, t, n=N, m=M, l=L)

    # SRS generation

    srs, trapdoor = setup(tau, G, H, qap)
    assert trapdoor == tau
    print(srs)
