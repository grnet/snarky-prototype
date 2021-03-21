def generate_srs_u(ctx, trapdoor, qap):
    _, G, H, _, _ = ctx
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

    p, G, H, _, _ = ctx
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
