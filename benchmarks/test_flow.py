import time
from snarky_ceremonies.constraints import QAP
from snarky_ceremonies.flow import create_context
from snarky_ceremonies.flow import generate_trapdoor
from snarky_ceremonies.flow import setup as _setup
from snarky_ceremonies.flow import update
from snarky_ceremonies.flow import verify

# TODO: Include iterations and rounds in arguments?


def test_qap_creation(benchmark):
    m, n, l = 5, 4, 3
    ctx = create_context()
    benchmark.pedantic(QAP.create_default, args=(ctx, m, n, l))

def test_setup(benchmark):
    m, n, l = 5, 4, 3
    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    qap = QAP.create_default(ctx, m, n, l)
    benchmark.pedantic(_setup, args=(ctx, trapdoor, qap))

def update_context(m, n, l):
    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    qap = QAP.create_default(ctx, m, n, l)
    srs, trapdoor = _setup(ctx, trapdoor, qap)
    srs, rho = update(ctx, qap, 1, srs)
    return ctx, qap, srs, rho

def test_phase_1(benchmark):
    ctx, qap, srs, _ = update_context(5, 4, 3)
    benchmark.pedantic(update, args=(ctx, qap, 1, srs))

def test_phase_2(benchmark):
    ctx, qap, srs, _ = update_context(5, 4, 3)
    benchmark.pedantic(update, args=(ctx, qap, 2, srs))

def test_verification(benchmark):
    phases = [1, 1, 1, 2, 2]
    m, n, l = 5, 4, 3
    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    qap = QAP.create_default(ctx, m, n, l)
    srs, trapdoor = _setup(ctx, trapdoor, qap)
    Q = [[], []]
    for phase in phases:
        srs, rho = update(ctx, qap, phase, srs)
        Q[0 if phase == 1 else 1].append(rho)
    benchmark.pedantic(verify, args=(ctx, qap, srs, Q))
