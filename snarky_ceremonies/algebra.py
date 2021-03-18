from snarky_ceremonies.utils import toBn, bnZero


class Poly(object):

    def __init__(self, coeffs, modulus):
        self.modulus = toBn(modulus)
        self.coeffs = list(map(
            lambda _: toBn(_).mod(self.modulus), 
            coeffs))

    @classmethod
    def create(cls, ctx, coeffs):
        return cls(coeffs, ctx.p)

    def degree(self):
        return len(self.coeffs) - 1

    def coeff(self, i):
        return self.coeffs[i]

    def eval(self, x):
        # x = toBn(x)
        # s = bnZero()
        # for i, coeff in enumerate(self.coeffs):
        #     s += coeff * x ** i
        # result = s.mod(self.modulus)
        #
        # TODO: Use optimized algorithm for polynomial evaluation
        # over finite fields with large order
        #
        x = toBn(x)
        result = sum(map(
            lambda i: self.coeffs[i] * x ** i,
            range(0, len(self.coeffs))
        ), bnZero()).mod(self.modulus)
        return result

