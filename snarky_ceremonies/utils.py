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

def _isGXElem(elem, X):
    return isinstance(elem, getattr(bp,'G%dElem' % X))

def isG1Elem(elem):
    return _isGXElem(elem, X=1)

def isG2Elem(elem):
    return _isGXElem(elem, X=2)
