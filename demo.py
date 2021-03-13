from snarky_ceremonies import create_algebraic_context
from snarky_ceremonies import generate_trapdoor
from snarky_ceremonies import QAP
from snarky_ceremonies import setup 


if __name__ == '__main__':
    print('Snarky Ceremonies')

    ctx = create_algebraic_context()
    trapdoor = generate_trapdoor(ctx)
    qap = QAP.create_default(ctx, m=5, n=4, l=3)

    # Setup (SRS generation)
    srs, trapdoor = setup(ctx, trapdoor, qap)
    print(srs)
