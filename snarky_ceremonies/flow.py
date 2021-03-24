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


from snarky_ceremonies.srs import generate_srs_u, generate_srs_s

def setup(ctx, trapdoor, qap):
    srs_u = generate_srs_u(ctx, trapdoor, qap)
    srs_s = generate_srs_s(ctx, trapdoor, qap)
    srs = (srs_u, srs_s)
    return srs, trapdoor


from snarky_ceremonies.utils import randstar
from snarky_ceremonies.dlog import prove_dlog

def _specialize(ctx, qap, srs_u):
    """
    Specialize, Fig. 6, pg. 19
    """
    # import pdb; pdb.set_trace()
    _, G, H, _, _ = ctx
    m, n, l = qap.dimensions()
    u, v, w, t = qap.polynomials()
    srs_s = [
        G,
        H,
        [],
        [],
    ]
    for i in range(0, m - l):
        # sum_{0<=j<=n-1} [u_ij(β x ^ j) * G + v_ij(β x ^ j) * G + (x ^ j) * G]
        s_i = sum([
            u[i].coeff(j) * srs_u[1][j][1] +            # (u_ij (β x ^ j)) * G  
            v[i].coeff(j) * srs_u[1][j][0] +            # (v_ij (α x ^ j)) * G
            w[i].coeff(j) * srs_u[0][j][0]              # (w_ij (x ^ j)) * G
        for j in range(0, n)], 0 * G)
        srs_s[2].append(s_i)
    for i in range(0, n - 1):
        # sum_{0<=j<=n-1} (t_j x ^ (i + j)) * G
        s_i = sum([
            t.coeff(j) * srs_u[0][i + j][0]     # (t_j x ^ (i + j)) * G
        for j in range(0, n)], 0 * G)
        srs_s[3].append(s_i)
    return srs_s

def update(ctx, qap, phi, srs):
    """
    Update, Fig. 6, pg. 19
    """
    p, G, H, _, _ = ctx
    m, n, l = qap.dimensions()
    if phi == 1:

        # step 1
        srs_u = srs[0]

        # step 2
        alpha_2 = randstar(p)
        beta_2 = randstar(p)
        x_2 = randstar(p)

        # step 3
        pi_alpha_2 = prove_dlog(ctx, (alpha_2 * G, alpha_2 * H), alpha_2)
        pi_beta_2 = prove_dlog(ctx, (beta_2 * G, beta_2 * H), beta_2)
        pi_x_2 = prove_dlog(ctx, (x_2 * G, x_2 * H), x_2)

        # step 4
        # ρ_α' = (α' * (α x ^ 0) * G, α' * G, α' * H, π_α')
        rho_alpha_2 = alpha_2 * srs_u[1][0][0], alpha_2 * G, alpha_2 * H,  pi_alpha_2

        # step 5
        # ρ_β' = (β' * (β x ^ 0) * G, β' * G, β' * H, π_β')
        rho_beta_2 = beta_2 * srs_u[1][0][1], beta_2 * G, beta_2 * H,  pi_beta_2

        # step 6
        # ρ_x' = (x' * (x ^ 1) * G, x' * G, x' * H, π_x')
        rho_x_2 = x_2 * srs_u[0][1][0], x_2 * G, x_2 * H,  pi_x_2

        # step 7
        # ρ = (ρ_α', ρ_β', ρ_x')
        rho = rho_alpha_2, rho_beta_2, rho_x_2

        # step 8
        srs_u_new = [[], []]
        for i in range(0, 2 * n -1):                # 0 <= i <= 2n - 2
            srs_u_new[0].append((
                (x_2 ** i) * srs_u[0][i][0],        # (x' ^ i) * ((x ^ i) * G)
                (x_2 ** i) * srs_u[0][i][1],        # (x' ^ i) * ((x ^ i) * H)
            ))
        for i in range(0, n):                       # 0 <= i <= n - 1
            srs_u_new[1].append((
                (alpha_2 * x_2 ** i) * srs_u[1][i][0],    # (α' x' ^ i) * ((α x ^ i) * G)
                (beta_2  * x_2 ** i) * srs_u[1][i][1],    # (β' x' ^ i) * ((β x ^ i) * G) 
                (alpha_2 * x_2 ** i) * srs_u[1][i][2],    # (α' x' ^ i) * ((α x ^ i) * H)
                (beta_2  * x_2 ** i) * srs_u[1][i][3],    # (β' x' ^ i) * ((β x ^ i) * H) 
            ))

        # step 9
        srs_s_new = _specialize(ctx, qap, srs_u_new)

        # step 10
        return (srs_u_new, srs_s_new), rho

    if phi == 2:
        # step 1
        srs_s = srs[1]

        # step 2
        delta_2 = randstar(p)

        # step 3
        pi_delta_2 = prove_dlog(ctx, (delta_2 * G, delta_2 * H), delta_2)

        # step 4
        # ρ = δ' * δ * G, δ' * G, δ' * H, π_δ'
        rho = delta_2 * srs_s[0], delta_2 * G, delta_2 * H, pi_delta_2

        # step 5
        srs_s_new = [
            delta_2 * srs_s[0],     # δ' * δ * G
            delta_2 * srs_s[1],     # δ' * δ * Η
            [],
            [],
        ]
        for i in range(0, m - l):   # 0 <= i <= m - l - 1
            # (sum ^ (l + i + 1) * G) / δ'
            srs_s_new[2].append(delta_2.mod_inverse(p) * srs_s[2][i])
        for i in range(0, n - 1):   # 0 <= i <= n - 2
            # ((t(x) ^ i) * G) / δ'
            srs_s_new[3].append(delta_2.mod_inverse(p) * srs_s[3][i]) 

        # step 6
        return (srs[0], srs_s_new), rho


from snarky_ceremonies.utils import isG1Elem, isG2Elem
from snarky_ceremonies.dlog import verify_dlog

class VerificationFailure(BaseException):
    pass

def _assert(condition, exception, message):
    if not condition: raise exception(message)

def _verify(ctx, qap, srs, Q):
    """
    Verification, Fig. 7, pg. 20
    """

    _, G, H, pair, _ = ctx
    m, n, l = qap.dimensions()
    u, v, w, _ = qap.polynomials()

    # step 1
    srs_u, srs_s = srs
    Q_u, Q_s = Q

    # step 2
    assert len(srs_u[0]) == 2 * n - 1
    assert len(srs_u[1]) == n
    for i in range(0, 2 * n - 1):       # 0 <= i <= 2n - 2
        # _assert(
        #     isG1Elem(srs_u[0][i][0]), VerificationFailure, 
        #     '(0, %d, 0)-component of srs_u is not a G1 element' % i,
        # )
        # _assert(
        #     isG2Elem(srs_u[0][i][1]), VerificationFailure, 
        #     '(0, %d, 1)-component of srs_u is not a G2 element' % i,
        # )
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
    # for i, rho_u in enumerate(Q_u):
    for i in range(len(Q_u)):           # ρ = Q_u[i]
        for j in range(0, 3):           # ι Ε {α, β, x}
            # A, B, C, D = rho_u[j]   
            A, B, C, D = Q_u[i][j]   
            assert verify_dlog(ctx, (B, C), D)
            if i != 0:
                assert pair(A, H).eq(pair(Q_u[i - 1][j][0], C))

    # step 4
    if len(Q_u) > 0:
        assert all((
            srs_u[0][1][0].eq(Q_u[-1][2][0]),               # x * G = x * G ^ k_u
            not Q_u[-1][2][0].eq(0 * G),                    # x * G ^ k_u != 0
        ))
        assert all((
            srs_u[1][0][0].eq(Q_u[-1][0][0]),               # α * G ^ (x ^ 0) = α * G ^ k_u
            not Q_u[-1][0][0].eq(0 * G),                    # α * G ^ k_u != 0 
        ))
        assert all((
            srs_u[1][0][1].eq(Q_u[-1][1][0]),               # β * G ^ (x ^ 0) = β * G ^ k_u
            not Q_u[-1][1][0].eq(0 * G),                    # β * G ^ k_u != 0
        ))

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
    for i in range(len(Q_s)):           # ρ = Q_s[i]
        A, B, C, D = Q_s[i]
        assert verify_dlog(ctx, (B, C), D)
        if i != 0:
            assert pair(A, H).eq(pair(Q_s[i - 1][0], C))    # TODO

    # step 9
    assert pair(srs_s[0], H).eq(pair(G, srs_s[1]))          # (δ * G) o H = G o (δ o H)
    if len(Q_s) > 0:
        assert all((
            srs_s[0].eq(Q_s[-1][0]),                        # δ * G = δ * G ^ k_s
            not Q_s[-1][0].eq(0 * G),                       # δ * G ^ k_s != 0
        )) 

    # step 10
    # u, v, w, _ = qap.polynomials()
    for i in range(0, m - l):
        # sum_{0 <=j<=n-1} [u_ij(β x ^ j) * G + v_ij(β x ^ j) * G + w_ij(x ^ j) * G]
        S_i = sum([
            u[i].coeff(j) * srs_u[1][j][1] +            # (u_ij (β x ^ j)) * G  
            v[i].coeff(j) * srs_u[1][j][0] +            # (v_ij (α x ^ j)) * G
            w[i].coeff(j) * srs_u[0][j][0]              # (w_ij (x ^ j)) * G
        for j in range(0, n)], 0 * G)
        # ((sum ^ (l + i + 1)) * G) o (δ o H) == S_i o H
        assert pair(srs_s[2][i], srs_s[1]).eq(pair(S_i, H))

    # step 11

    # Compute Gt = sum_{0<=j<=n} (t_j x ^ j) * G
    t = qap.t
    Gt = sum([t.coeff(j) * srs_u[0][j][0] for j in range(0, n + 1)], 0 * G)

    for i in range(0, n - 1):   # 0 <= i <= n - 2
        # ((t(x) ^ i) * G) o (δ * Η) == Gt o ((x ^ i) * H)
        assert pair(srs_s[3][i], srs_s[1]).eq(pair(Gt, srs_u[0][i][1]))


def verify(ctx, qap, srs, Q):
    try:
        _verify(ctx, qap, srs, Q)
    # except VerificationFailure as err:
    except AssertionError as err:
        return False
    return True
