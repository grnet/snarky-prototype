"""
Snarky Ceremonies demo script
"""

import sys
import argparse
from snarky_ceremonies import create_context, \
    generate_trapdoor, QAP, QAPConstructionError, setup, update, verify
import time

def _round(number, ndigits=6):
    return round(number, ndigits)

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

    parser.add_argument('--m', type=int, default=5, dest='m', metavar='',
            help="m parameter for QAP (default: 5)")
    parser.add_argument('--n', type=int, default=4, dest='n', metavar='',
            help="n parameter for QAP (default: 4)")
    parser.add_argument('--l', type=int, default=3, dest='l', metavar='',
            help="l parameter for QAP (default: 3)")
    parser.add_argument('--phases', nargs='+', type=int,
            default=(3, 2,), dest='phases', metavar='',
            help="number of phase 1 resp. 2 updates (default: 3, 2)")

    args = parser.parse_args()

    m = args.m
    n = args.n
    l = args.l
    phases = args.phases

    ctx = create_context()

    print()
    start = time.time()

    # QAP creation
    curr = start
    try:
        qap = QAP.create_default(ctx, m, n, l)
    except QAPConstructionError as err:
        print('[-] Could not create QAP: %s' % err)
        sys.exit(1)
    next_curr = time.time()
    print('[+] Created QAP with m:%d n:%d l:%d  (%s sec)' % (m, n, l, _round(next_curr - curr)))
    curr = next_curr

    # Setup (SRS generation)
    trapdoor = generate_trapdoor(ctx, 1, 1, 1, 1)
    srs, trapdoor = setup(ctx, trapdoor, qap)
    next_curr = time.time()
    print('[+] Initialized SRS  (%s sec)' % _round(next_curr - curr))
    curr = next_curr

    # Updates
    Q = [[], []]
    phases = [1] * phases[0] + [2] * phases[1]
    for phase in phases:
        srs, rho = update(ctx, qap, phase, srs)
        Q[0 if phase == 1 else 1].append(rho)
        next_curr = time.time()
        print('[+] Updated SRS phase %d (%s sec)' % (phase, _round(next_curr - curr)))
        curr = next_curr

    # Verify SRS
    verified = verify(ctx, qap, srs, Q)
    next_curr = time.time()
    if verified:
        print('[+] VERIFICATION SUCCESS (%s sec)' % _round(next_curr - curr))
    else:
        print('[-] FAILED to verify SRS')
    end = next_curr
    print('\nTotal time elapsed: %s seconds' % _round(end - start))
