import pytest
from snarky_ceremonies.constraints import QAP
from snarky_ceremonies.flow import create_context
from snarky_ceremonies.flow import generate_trapdoor
from snarky_ceremonies.flow import setup as _setup
from snarky_ceremonies.flow import update
from snarky_ceremonies.flow import verify


ctx = create_context()

@pytest.mark.parametrize('m, n, l', [
    (2, 2, 1),
    (2, 3, 1),
    (2, 4, 1),
    (3, 2, 1),
    (3, 2, 2),
    (3, 3, 1),
    (3, 3, 2),
    (3, 4, 1),
    (3, 4, 2),
    (4, 2, 1),
    (4, 2, 2),
    (4, 2, 3),
    (4, 3, 1),
    (4, 3, 2),
    (4, 3, 3),
    (4, 4, 1),
    (4, 4, 2),
    (4, 4, 3),
    (5, 2, 1),
    (5, 2, 2),
    (5, 2, 3),
    (5, 2, 4),
    (5, 3, 1),
    (5, 3, 2),
    (5, 3, 3),
    (5, 3, 4),
    (5, 4, 1),
    (5, 4, 2),
    (5, 4, 3),
    (5, 4, 4),
])
def test_flow_with_variable_dimensions(m, n, l):
    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    qap = QAP.create_default(ctx, m, n, l)
    srs, trapdoor = _setup(ctx, trapdoor, qap)
    Q = [[], []]
    for phase in [1, 1, 1, 2, 2]:
        srs, rho = update(ctx, qap, phase, srs)
        if phase == 1:
            Q[0].append(rho)
        else:
            Q[1].append(rho)
    assert verify(ctx, qap, srs, Q)

@pytest.mark.parametrize('phases', [
    [],
    [1],
    [1, 1],
    [1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 2],
    [1, 1, 2, 2],
    [1, 2, 2, 2],
    [2, 2, 2, 2],
    [2, 2, 2],
    [2, 2],
    [2],
])
def test_flow_with_variable_phases(phases):
    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    qap = QAP.create_default(ctx, 5, 4, 3)
    srs, trapdoor = _setup(ctx, trapdoor, qap)
    Q = [[], []]
    for phase in phases:
        srs, rho = update(ctx, qap, phase, srs)
        if phase == 1:
            Q[0].append(rho)
        else:
            Q[1].append(rho)
    assert verify(ctx, qap, srs, Q)


@pytest.mark.parametrize('phases', [
    [2, 1],
    [2, 1, 2],
])
def test_flow_with_forbidden_phases(phases):
    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    qap = QAP.create_default(ctx, 5, 4, 3)
    srs, trapdoor = _setup(ctx, trapdoor, qap)
    Q = [[], []]
    for phase in phases:
        srs, rho = update(ctx, qap, phase, srs)
        if phase == 1:
            Q[0].append(rho)
        else:
            Q[1].append(rho)
    assert not verify(ctx, qap, srs, Q)
    # with pytest.raises(AssertionError):
    #     verify(ctx, qap, srs, Q)

