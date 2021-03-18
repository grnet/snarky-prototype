from bplib import bp
from petlib import bn
from collections import namedtuple

def randstar(p):
    """
    Generate a random element of the prime field (Z_p)*
    """
    return (p - 1).random()


def toBn(num):
    return bn.Bn.from_decimal(str(num))

def bnZero():
    return toBn(0)


CTX = namedtuple('CTX', ['p', 'G', 'H', 'pair'])

def create_context():
    group = bp.BpGroup()            # bilinear pairing o: G_1 x G_2 -> G_T
    p = group.order()               # order of G_T
    G = group.gen1()                # generator of G_1
    H = group.gen2()                # generator of G_2
    pair = group.pair               # pairing operator o
    return CTX(p, G, H, pair)


def _isGXElem(elem, X):
    return isinstance(elem, getattr(bp,'G%dElem' % X))

def isG1Elem(elem):
    return _isGXElem(elem, X=1)

def isG2Elem(elem):
    return _isGXElem(elem, X=2)
