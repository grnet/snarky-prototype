import time
from snarky_ceremonies.constraints import QAP
from snarky_ceremonies.flow import create_context
from snarky_ceremonies.flow import generate_trapdoor
from snarky_ceremonies.flow import setup as _setup
from snarky_ceremonies.flow import update
from snarky_ceremonies.flow import verify

def run_flow():
    m, n, l = 5, 4, 3
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

def test_run_flow(benchmark):
    benchmark(run_flow)
