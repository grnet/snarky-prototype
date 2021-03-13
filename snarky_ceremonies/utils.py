def randstar(p):
    """
    Generate a random element of the prime field (Z_p)*
    """
    return (p - 1).random()


from bplib import bp
from petlib import bn

def toBn(num):
    return bn.Bn.from_decimal(str(num))

def bnZero():
    return toBn(0)
