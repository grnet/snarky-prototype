import pytest
from snarky_ceremonies import create_context
from snarky_ceremonies.algebra import Poly, toBn
from snarky_ceremonies import QAP, QAPConstructionError

ctx = create_context()

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
        qap = QAP(ctx, u, v, w, t, l)

def test_QAP_create_default():
    assert 1
