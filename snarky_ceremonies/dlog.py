"""
Discrete logarithm proof of knowledge (Fig. 4)
"""

def prove_dlog(ctx, phi, w):    # δ * G, δ * H, w
    aux = ctx.RO(phi)           # r * G = hash(bytes(δ * G) + bytes(δ * H))
    out = w * aux               # (w r) * G
    return out

def verify_dlog(ctx, phi, pi):                  # δ * G, δ * H, w
    _, G, H, pair, RO = ctx
    aux = RO(phi)                               # r * G
    # TODO: Improve checks and output
    assert pair(phi[0], H) == pair(G, phi[1])   # ((w r) * G) o H = (G o H) ^ (w r)
    assert pair(pi, H) == pair(aux, phi[1])     # (r * G) o (δ * H) = (G o H) ^ (r δ)
    return True
