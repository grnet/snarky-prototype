from snarky_ceremonies.utils import toBn, bnZero

class Poly(object):

    def __init__(self, coeffs):
        assert len(coeffs) >= 1
        self.coeffs = list(map(toBn, coeffs))

    def degree(self):
        return len(self.coeffs) - 1

    def coeff(self, i):
        return self.coeffs[i]

    def eval(self, x):
        return sum(
            map(
                lambda i: self.coeffs[i] * x ** i,      # TODO: mod p
                range(0, len(self.coeffs))
            ), 
            bnZero()
        )
