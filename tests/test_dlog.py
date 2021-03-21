import pytest
from snarky_ceremonies import create_context
from snarky_ceremonies.dlog import prove_dlog, verify_dlog
from snarky_ceremonies.utils import toBn

@pytest.mark.parametrize('y1, y2, w, success',
    [
        (100, 100, 100, True),
        (666, 100, 100, False),
        (100, 666, 100, False),
        (100, 100, 666, False),
    ]
)
def test_dlog_proof(y1, y2, w, success):
    ctx = create_context()

    y1 = toBn(y1)
    y2 = toBn(y2)
    phi = (y1 * ctx.G, y2 * ctx.H)
    w = toBn(w)
    pi = prove_dlog(ctx, phi, w)
    if success:
        assert verify_dlog(ctx, phi, pi)
    else:
        with pytest.raises(AssertionError):
            verify_dlog(ctx, phi, pi)
