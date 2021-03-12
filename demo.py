
class Prover(object):
    pass

class Verifier(object):
    pass


# Setup

from collections import namedtuple

Tau = namedtuple('Tau', ['alpha', 'beta', 'delta', 'x'])   # τ = (α, β, δ, x) E (Z_p)^*

def extract_tau(tau):
    return tau.alpha, tau.beta, tau.delta, tau.x

def generate_srs_u(tau, G, H, n):
    srs_u = [[], []]
    alpha, beta, _, x = extract_tau(tau)
    for i in range(0, 2 * N -1):                # 0 <= i <= 2n - 2
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

def generate_srs_s(tau):
    raise NotImplementedError

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

    N = 3
    srs_u = generate_srs_u(tau, G, H, n=N)

