from collections import namedtuple

CTX = namedtuple('CTX', ['p', 'G', 'H', 'pair', 'RO'])

def create_context():
    from bplib import bp

    group = bp.BpGroup()            # bilinear pairing o: G_1 x G_2 -> G_T
    p = group.order()               # order of G_T
    G = group.gen1()                # generator of G_1
    H = group.gen2()                # generator of G_2
    pair = group.pair               # pairing operator o

    # Hash functionality in place of theoretical random oracle
    def RO(phi):
        out = group.hashG1(phi[0].export() + phi[1].export())
        return out

    return CTX(p, G, H, pair, RO)


from collections import namedtuple
from snarky_ceremonies.utils import toBn, randstar

Trapdoor = namedtuple('Trapdoor', 
    ['alpha', 'beta', 'delta', 'x'])   # τ = (α, β, δ, x) E (Z_p)*

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
        u = [Poly.create(ctx, [1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        v = [Poly.create(ctx, [1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        w = [Poly.create(ctx, [1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        t = Poly.create(ctx, [1] + n * [0])
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


from snarky_ceremonies.utils import isG1Elem, isG2Elem

def verify(ctx, qap, srs):   # TODO: Include Q in arguments
    """
    Verification, Fig. 7, pg. 20
    """

    _, G, H, pair, _ = ctx
    m, n, l = qap.dimensions()
    u, v, w, _ = qap.polynomials()

    # step 1
    srs_u, srs_s = srs
    # TODO: Parse Q

    # step 2
    assert len(srs_u[0]) == 2 * n - 1
    assert len(srs_u[1]) == n
    for i in range(0, 2 * n - 1):       # 0 <= i <= 2n - 2
        assert all((
            isG1Elem(srs_u[0][i][0]),   # (x ^ i) * G E G_1
            isG2Elem(srs_u[0][i][1]),   # (x ^ i) * H E G_2
        ))
    for i in range(0, n):               # 0 <= i <= n - 1
        assert all((
            isG1Elem(srs_u[1][i][0]),   # (α x ^ i) * G E G_1
            isG1Elem(srs_u[1][i][1]),   # (β x ^ i) * G E G_1
            isG2Elem(srs_u[1][i][2]),   # (α x ^ i) * H E G_2
            isG2Elem(srs_u[1][i][3]),   # (β x ^ i) * H E G_2
        ))

    # step 3
    # TODO: Implement

    # step 4
    # TODO: Implement

    # step 5
    for i in range(1, 2 * n - 1):                           # 1 <= i <= 2n - 2
        assert all((
            # ((x ^ i) * G) o H == G o ((x ^ i) * H)
            pair(srs_u[0][i][0], H).eq(pair(G, srs_u[0][i][1])),
            # # ((x ^ i) * G) o H == ((x ^ (i - 1)) * G) o ((x ^ 1) * H)
            pair(srs_u[0][i][0], H).eq(pair(srs_u[0][i - 1][0], srs_u[0][1][1])),
        ))

    # step 6
    for i in range(0, n):                                   # 0 <= i <= n - 1
        all((
            # ((α x ^ i) * G) o H == G o ((α x ^ i) * H)
            pair(srs_u[1][i][0], H).eq(pair(G, srs_u[1][i][2])),
            # ((α x ^ i) * G) o H == ((x ^ i) * G) o ((α x ^ 0) * H)
            pair(srs_u[1][i][0], H).eq(pair(srs_u[0][i][0], srs_u[1][0][2])),  
            # ((β x ^ i) * G) o H == G o ((β x ^ i) * H)
            pair(srs_u[1][i][1], H).eq(pair(G, srs_u[1][i][3])),
            # ((β x ^ i) * G) o H == ((x ^ i) * G) o ((β x ^ 0) * H)
            pair(srs_u[1][i][1], H).eq(pair(srs_u[0][i][0], srs_u[1][0][3])),  
        ))

    # step 7
    assert all((
        isG1Elem(srs_s[0]),             # δ * G E G_1
        isG2Elem(srs_s[1]),             # δ * H E G_2
    ))
    assert len(srs_s[2]) == m - l       # ((sum ^ i) * G)_{l + 1 <= i <= m}
    assert len(srs_s[3]) == n - 1       # ((t(x) ^ i) * G)_{0 <= i <= n - 2}

    for i in range(0, m - l):           # 0 <= i <= m - l - 1
        assert isG1Elem(srs_s[2][i])    # (sum ^ (l + i + 1)) * G E G_1

    for i in range(0, n - 1):           # 0 <= i <= n - 2
        assert isG1Elem(srs_s[3][i])    # (t(x) ^ i) * G E G_1

    # step 8
    # TODO: Implement

    # step 9
    assert pair(srs_s[0], H).eq(pair(G, srs_s[1]))      # (δ * G) o H = G o (δ o H)
    # TODO: Implement second condition                  # δ * G = δ * G ^ k_s != 1

    # step 10
    # u, v, w, _ = qap.polynomials()
    for i in range(0, m - l):
        # sum_{0 <=j<=n-1} [u_ij(β x ^ j) * G + v_ij(β x ^ j) * G + (x ^ j) * G]
        S_i = sum([
            u[i].coeff(j) * srs_u[1][j][1] +            # (u_ij (β x ^ j)) * G  
            v[i].coeff(j) * srs_u[1][j][0] +            # (v_ij (α x ^ j)) * G
            w[i].coeff(j) * srs_u[0][j][0]              # (x ^ j) * G
        for j in range(0, n)], 0 * G)
        # ((sum ^ (l + i + 1)) * G) o (δ o H) == S_i o H
        assert pair(srs_s[2][i], srs_s[1]).eq(pair(S_i, H))

    # step 11

    # Compute Gt = sum_{0<=j<=n} (t_j (x ^ j)) G
    t = qap.t
    Gt = sum([t.coeff(j) * srs_u[0][j][0] for j in range(0, n + 1)], 0 * G)

    for i in range(0, n - 1):   # 0 <= i <= n - 2
        # ((t(x) ^ i) * G) o (δ * Η) == Gt o ((x ^ i) * H)
        pair(srs_s[3][i], srs_s[1]).eq(pair(Gt, srs_u[0][i][1]))

    return True
