
class Prover(object):
    pass

class Verifier(object):
    pass


# Setup

from collections import namedtuple

Tau = namedtuple('Tau', ['alpha', 'beta', 'delta', 'x'])   # τ = (α, β, δ, x) E (Z_p)*

def extract_tau(tau):
    return tau.alpha, tau.beta, tau.delta, tau.x


class QAP(object):

    def __init__(self, p, u, v, w, t, n, m, l):

        # Compatibility checks

        assert l + 1 <= m

        assert len(t) == n + 1      # deg(t) = n

        assert len(u) == m + 1      # u_i, 0 <= i <= m
        assert len(v) == m + 1      # v_i, 0 <= i <= m
        assert len(w) == m + 1      # w_i, 0 <= i <= m

        for i in range(0, m + 1):       # for 0 <= i <= m
            assert len(u[i]) == n       # deg(u_i) = n - 1
            assert len(v[i]) == n       # deg(v_i) = n - 1
            assert len(w[i]) == n       # deg(w_i) = n - 1

        # Set parameters

        self.p = p      # group order

        self.u = u      # u[i][j]: coefficient of X ^ j in u_i
        self.v = v      # v[i][j]: coefficient of X ^ j in v_i
        self.w = w      # w[i][j]: coefficient of X ^ j in w_i
        
        self.t = t      # t[k]: coefficient of X ^ k in t

        self.n = n      # 0 <= j <= n - 1, 0 <= k <= n
        self.m = m      # 0 <= i <= m
        self.l = l      # 0 <= l <= m - 1 arbitrary


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
    u = qap.w
    m = qap.m
    n = qap.n
    l = qap.l

    srs_s = [
        delta * G,                              # δ * G
        delta * H,                              # δ * Η
    ]
    for i in range(l + 1, m + 1):               # l + 1 <= i <= m
        # TODO: Implement
        pass
    for i in range(0, n - 1):                   # 0 <= i <= n - 2
        # TODO: Implement
        pass
    return srs_s

def setup(tau):
    raise NotImplementedError


# Utils

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

    # Create context

    G_T = bp.BpGroup()                      # bilinear pairing G_1 x G_2 -> G_T
    p = G_T.order()                         # p = order(G_T)
    G, H = G_T.gen1(), G_T.gen2()           # G_1 = <G>, G_2 = <H>
    tau = mk_random_tau(G_T)                # τ = (α, β, δ, x), α, β, δ, x E (Z_p)^* random

    # Setup

    M = 5   # 6 = M + 1 length of u, v, w
    N = 4   # 4 = N degree of t, 3 = N - 1 degree of u_i, v_i, w_i, 0 <= i <=5
    L = 3   # l + 1 <= m

    u = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    v = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    w = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    t = [0, 0, 0, 0, 0]

    qap = QAP(p, u, v, w, t, n=N, m=M, l=L)

    srs_u = generate_srs_u(tau, G, H, n=N)
    srs_s = generate_srs_s(tau, G, H, qap)

