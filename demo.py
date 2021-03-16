"""
Snarky Ceremonies demo script
"""

import sys
import argparse
from snarky_ceremonies import create_algebraic_context
from snarky_ceremonies import generate_trapdoor
from snarky_ceremonies import QAP
from snarky_ceremonies import setup 


if __name__ == '__main__':
    prog = sys.argv[0]
    usage = 'python3 %s [OPTIONS]' % prog
    epilog = '\n'
    description = __doc__
    epilog = ''
    parser = argparse.ArgumentParser(prog=prog,
        usage=usage,
        description=__doc__,
        epilog=epilog)

    parser.add_argument('-m', type=int, default=5, dest='m',
            help="m parameter for QAP (default: 5)")
    parser.add_argument('-n', type=int, default=4, dest='n',
            help="n parameter for QAP (default: 4)")
    parser.add_argument('-l', type=int, default=3, dest='l',
            help="l parameter for QAP (default: 3)")

    args = parser.parse_args()

    m = args.m
    n = args.n
    l = args.l

    ctx = create_algebraic_context()
    trapdoor = generate_trapdoor(ctx)
    qap = QAP.create_default(ctx, m, n, l)

    # Setup (SRS generation)
    srs, trapdoor = setup(ctx, trapdoor, qap)
    # print(srs)

    # Verification, Fig. 7, pg. 20

    _, G, H = ctx

    # Verification Helpers, TODO: Integrate with context

    def isG1Elem(elem):
        import bplib
        return isinstance(elem, bplib.bp.G1Elem)

    def isG2Elem(elem):
        import bplib
        return isinstance(elem, bplib.bp.G2Elem)

    def pair(elem_1, elem_2):
        import bplib
        return bplib.bp.BpGroup().pair(elem_1, elem_2)

    # step 1
    srs_u, srs_s = srs
    # TODO: Parse Q

    # step 2
    assert len(srs_u[0]) == 2 * n - 1
    assert len(srs_u[1]) == n
    for i in range(0, 2 * n - 1):       # 0 <= i <= 2n - 2
        assert all((
            isG1Elem(srs_u[0][i][0]),   # (x ^ i) * G E G_1
            isG2Elem(srs_u[0][i][1]),   # (x ^ i) * H E G_2
        ))
    for i in range(0, n):               # 0 <= i <= n - 1
        assert all((
            isG1Elem(srs_u[1][i][0]),   # (α x ^ i) * G E G_1
            isG1Elem(srs_u[1][i][1]),   # (β x ^ i) * G E G_1
            isG2Elem(srs_u[1][i][2]),   # (α x ^ i) * H E G_2
            isG2Elem(srs_u[1][i][3]),   # (β x ^ i) * H E G_2
        ))

    # step 3
    # TODO: Implement

    # step 4
    # TODO: Implement

    # step 5
    for i in range(1, 2 * n - 1):                           # 1 <= i <= 2n - 2
        assert all((
            # ((x ^ i) * G) o H == G o ((x ^ i) * H)
            pair(srs_u[0][i][0], H).eq(pair(G, srs_u[0][i][1])),
            # # ((x ^ i) * G) o H == ((x ^ (i - 1)) * G) o ((x ^ 1) * H)
            pair(srs_u[0][i][0], H).eq(pair(srs_u[0][i - 1][0], srs_u[0][1][1])),
        ))

    # step 6
    for i in range(0, n):                                   # 0 <= i <= n - 1
        all((
            # ((α x ^ i) * G) o H == G o ((α x ^ i) * H)
            pair(srs_u[1][i][0], H).eq(pair(G, srs_u[1][i][2])),
            # ((α x ^ i) * G) o H == ((x ^ i) * G) o ((α x ^ 0) * H)
            pair(srs_u[1][i][0], H).eq(pair(srs_u[0][i][0], srs_u[1][0][2])),  
            # ((β x ^ i) * G) o H == G o ((β x ^ i) * H)
            pair(srs_u[1][i][1], H).eq(pair(G, srs_u[1][i][3])),
            # ((β x ^ i) * G) o H == ((x ^ i) * G) o ((β x ^ 0) * H)
            pair(srs_u[1][i][1], H).eq(pair(srs_u[0][i][0], srs_u[1][0][3])),  
        ))

