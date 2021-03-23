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


class QAPConstructionError(BaseException):
    pass

class QAP(object):

    def __init__(self, ctx, u, v, w, t, l):
        self.p = ctx.p
        m = len(u) - 1
        if len(v) != m + 1 or len(w) != m + 1:
            err = 'Incompatible sizes: u:%d, v:%d, w:%d' \
                % (len(u), len(v), len(w))
            raise QAPConstructionError(err)
        self.m = m
        if l + 1 > m:
            err = 'l is not < m: l=%d, m=%d' % (l, m)
            raise QAPConstructionError(err)
        self.l = l
        n = t.degree()
        self.t = t
        self.n = n
        for a, b in ((u, 'u'), (v, 'v'), (w, 'w')):
            for i in range(0, m + 1):
                if a[i].degree() != n - 1:
                    err = 'Degree of %s_%d is %d, different from n-1=%d' \
                        % (b, i, a[i].degree(), n - 1)
                    raise QAPConstructionError(err)
        self.u = u
        self.v = v
        self.w = w

    @classmethod
    def create_default(cls, ctx, m, n, l):
        u = [Poly.create(ctx, [1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        v = [Poly.create(ctx, [1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        w = [Poly.create(ctx, [1] + (n - 1) * [0]) for _ in range(0, m + 1)]
        t = Poly.create(ctx, [1] + n * [0])
        return cls(ctx, u, v, w, t, l)

    def polynomials(self):
        u = self.u
        v = self.v
        w = self.w
        t = self.t
        return u, v, w, t

    def dimensions(self):
        m = self.m
        n = self.n
        l = self.l
        return m, n, l
