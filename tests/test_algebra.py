import pytest
from snarky_ceremonies.algebra import Poly, toBn, get_default_prime


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
    assert Poly(coeffs).degree() == expected


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
        ([1, 3, 7, 4, 5, 7], None, 0, 1),
        ([1, 3, 7, 4, 5, 7], None, 1, 27),
        ([1, 3, 7, 4, 5, 7], None, -1, toBn(-1) % get_default_prime()),
        ([1, 3, 7, 4, 5, 7], None, 666, 918195749349787),
    ]
)
def test_poly_eval(coeffs, p, x, result):
    assert Poly(coeffs, p).eval(x) == toBn(result)
