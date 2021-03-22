"""
Snarky Ceremonies demo script
"""

import sys
import argparse
from snarky_ceremonies import create_context, \
    generate_trapdoor, QAP, setup, update, verify


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
    parser.add_argument('--verbose', action='store_true', default=False,
            help="Display info while running (default: False)")

    args = parser.parse_args()

    m = args.m
    n = args.n
    l = args.l
    verbose = args.verbose  # TODO: Use it

    # Context creation: order, generators and pairing
    ctx = create_context()
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    qap = QAP.create_default(ctx, m, n, l)

    # Setup (SRS generation)
    srs, trapdoor = setup(ctx, trapdoor, qap)

    # Update
    update(ctx, qap, 1, srs, [])
    update(ctx, qap, 2, srs, [])


    # Verify (SRS verification)
    assert verify(ctx, qap, srs)
