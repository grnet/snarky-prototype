import pytest
from snarky_ceremonies import create_context
from snarky_ceremonies.constraints import Poly, toBn, QAP, QAPConstructionError

ctx = create_context()

@pytest.mark.parametrize('coeffs, expected',
    [
        ([], -1),
        ([0], 0),
        ([0, 0], 1),
        ([0, 0, 0], 2),
        ([0, 0, 0, 0], 3),
    ]
)
def test_poly_degree(coeffs, expected):
    assert Poly(coeffs, ctx.p).degree() == expected


@pytest.mark.parametrize('coeffs, p, x, result',
    [
        ([0, 1], 7, 0, 0),
        ([0, 1], 7, 1, 1),
        ([0, 1], 7, -1, 6),
        ([0, 1], 7, 666, 1),
        ([1, 0], 7, 0, 1),
        ([1, 0], 7, 1, 1),
        ([1, 0], 7, -1, 1),
        ([1, 0], 7, 666, 1),
        ([1, 3, 7, 4, 5, 7], 7, 0, 1),
        ([1, 3, 7, 4, 5, 7], ctx.p, 0, 1),
        ([1, 3, 7, 4, 5, 7], ctx.p, 1, 27),
        ([1, 3, 7, 4, 5, 7], ctx.p, -1, toBn(-1) % ctx.p),
        ([1, 3, 7, 4, 5, 7], ctx.p, 666, 918195749349787),
    ]
)
def test_poly_eval(coeffs, p, x, result):
    assert Poly(coeffs, p).eval(x) == toBn(result)

def test_QAP_construction():
    m = 5
    n = 4
    l = 3
    u = [Poly.create(ctx, [i + j + 0 for i in range(0, n)]) for j in range(0, m + 1)]
    v = [Poly.create(ctx, [i + j + 1 for i in range(0, n)]) for j in range(0, m + 1)]
    w = [Poly.create(ctx, [i + j + 2 for i in range(0, n)]) for j in range(0, m + 1)]
    t = Poly.create(ctx, [i for i in range(n + 1)])
    qap = QAP(ctx, u, v, w, t, l)
    assert qap.polynomials() == (u, v, w, t)
    assert qap.dimensions() == (m, n, l)

@pytest.mark.parametrize('u, v, w, t, l', 
    [
        (
            [Poly.create(ctx, [i + j + 0 for i in range(0, 4)]) for j in range(0, 6 + 1)],
            [Poly.create(ctx, [i + j + 1 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 2 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            Poly.create(ctx, [i for i in range(4 + 1)]),
            3,
        ),
        (
            [Poly.create(ctx, [i + j + 0 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 1 for i in range(0, 4)]) for j in range(0, 6 + 1)],
            [Poly.create(ctx, [i + j + 2 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            Poly.create(ctx, [i for i in range(4 + 1)]),
            3,
        ),
        (
            [Poly.create(ctx, [i + j + 0 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 1 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 2 for i in range(0, 4)]) for j in range(0, 6 + 1)],
            Poly.create(ctx, [i for i in range(4 + 1)]),
            3,
        ),
        (
            [Poly.create(ctx, [i + j + 0 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 1 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 2 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            Poly.create(ctx, [i for i in range(4 + 1)]),
            5,
        ),
        (
            [Poly.create(ctx, [i + j + 0 for i in range(0, 3)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 1 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 2 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            Poly.create(ctx, [i for i in range(4 + 1)]),
            3,
        ),
        (
            [Poly.create(ctx, [i + j + 0 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 1 for i in range(0, 3)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 2 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            Poly.create(ctx, [i for i in range(4 + 1)]),
            3,
        ),
        (
            [Poly.create(ctx, [i + j + 0 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 1 for i in range(0, 4)]) for j in range(0, 5 + 1)],
            [Poly.create(ctx, [i + j + 2 for i in range(0, 3)]) for j in range(0, 5 + 1)],
            Poly.create(ctx, [i for i in range(4 + 1)]),
            3,
        ),
    ]
)
def test_QAP_construction_errors(u, v, w, t, l):
    with pytest.raises(QAPConstructionError):
        QAP(ctx, u, v, w, t, l)
