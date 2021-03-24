"""
Snarky Ceremonies demo script
"""

import sys
import argparse
from snarky_ceremonies import create_context, \
    generate_trapdoor, QAP, QAPConstructionError, setup, update, verify


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

    parser.add_argument('-m', type=int, default=5, dest='m', metavar='',
            help="m parameter for QAP (default: 5)")
    parser.add_argument('-n', type=int, default=4, dest='n', metavar='',
            help="n parameter for QAP (default: 4)")
    parser.add_argument('-l', type=int, default=3, dest='l', metavar='',
            help="l parameter for QAP (default: 3)")
    parser.add_argument('--phases', nargs='+', type=int,
            default=(3, 2,), dest='phases', metavar='',
            help="φ1 and φ2 phase parameters for update (default: 3, 2)")

    args = parser.parse_args()

    m = args.m
    n = args.n
    l = args.l
    phases = args.phases

    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    try:
        qap = QAP.create_default(ctx, m, n, l)
    except QAPConstructionError as err:
        print('[-] Could not create QAP: %s' % err)
        sys.exit(1)

    # Setup (SRS generation)
    srs, trapdoor = setup(ctx, trapdoor, qap)

    # Store proofs
    Q = [[], []]

    # Updates
    phases = [1] * phases[0] + [2] * phases[1]
    for phase in phases:
        srs, rho = update(ctx, qap, phase, srs)
        if phase == 1:
            Q[0].append(rho)
        else:
            Q[1].append(rho)

    # Verify SRS
    result = verify(ctx, qap, srs, Q)
