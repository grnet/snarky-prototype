from snarky_ceremonies.utils import toBn, bnZero

def get_default_prime():
    from bplib import bp
    return bp.BpGroup().order()


class Poly(object):

    def __init__(self, coeffs, modulus=None):
        self.modulus = get_default_prime() \
            if modulus is None else toBn(modulus)
        self.coeffs = list(map(
            lambda _: toBn(_).mod(self.modulus), coeffs))

    def degree(self):
        return len(self.coeffs) - 1

    def coeff(self, i):
        return self.coeffs[i]

    def eval(self, x):
        # TODO: Use optimized algorithm for polynomial evaluation
        # over finite fields with large order
        x = toBn(x)
        s = bnZero()
        for i, coeff in enumerate(self.coeffs):
            s += coeff * x ** i
        result = s.mod(self.modulus)
        # TODO: Remove this check
        assert result == sum(
            map(
                lambda i: self.coeffs[i] * x ** i,
                range(0, len(self.coeffs))
            ), 
            bnZero()
        ).mod(self.modulus)
        return result

