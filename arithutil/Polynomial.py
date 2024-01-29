class Polynomial:
    def __init__(self, arr, field):
        if isinstance(arr, list):
            self.field = field
            self.coeffs = {}
            for coeff in arr:
                if not isinstance(coeff, self.field.FieldElem):
                    raise TypeError('Coefficient is not in the base field')
            for i in range(len(arr)):
                if not arr[i] == self.field(0):
                    self.coeffs[i] = arr[i]
            if len(self.coeffs) == 0:
                self.coeffs[0] = self.field(0)
        elif isinstance(arr, dict):
            self.field = field
            self.coeffs = {}
            for i in arr:
                if not arr[i] == self.field(0):
                    self.coeffs[i] = arr[i]
            if len(self.coeffs) == 0:
                self.coeffs[0] = self.field(0)

    def eval(self, x):
        if not isinstance(x, self.field.FieldElem):
            raise TypeError('x is not in the base field')
        res = self.field(0)
        for i in sorted(self.coeffs.keys()):
            xpowi = self.field(1)
            q = x
            g = i
            for j in range(i.bit_length()):
                if g & (1 << j):
                    xpowi = xpowi * q
                    g -= 2**j
                q = q*q
            res = res + self.coeffs[i] * xpowi
        return res

    def __add__(self, o):
        P = self if len(self.coeffs) < len(o.coeffs) else o
        Q = o if len(self.coeffs) < len(o.coeffs) else self
        sum_dict = Q.coeffs.copy()
        for k, v in P.coeffs.items():
            if k in sum_dict:
                sum_dict[k] = sum_dict[k] + v
            else:
                sum_dict[k] = v
        ret = Polynomial(sum_dict, self.field)
        return ret

    def __neg__(self):
        return Polynomial({i: -self.coeffs[i] for i in self.coeffs}, self.field)

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        # This can even be speeded up faster using FFT but we're not doing it here
        P = self if len(self.coeffs) < len(o.coeffs) else o
        Q = o if len(self.coeffs) < len(o.coeffs) else self
        sum_dict = {}
        for i in P.coeffs.keys():
            for j in Q.coeffs.keys():
                if i+j in sum_dict:
                    sum_dict[i+j] = sum_dict[i+j] + P.coeffs[i] * Q.coeffs[j]
                else:
                    sum_dict[i+j] = P.coeffs[i] * Q.coeffs[j]
        return Polynomial(sum_dict, self.field)

    def __mod__(A, B):
        # synthetic long division: A = BQ + R, return R (may not be monic)
        if B.deg == 0 and B.coeffs[0] == 0:
            raise ZeroDivisionError('modulo by zero')
        while A.deg >= B.deg:
            shf = A.deg - B.deg
            mul = A.coeffs[A.deg] / B.coeffs[B.deg]
            Q = Polynomial({shf: mul}, A.field)
            A = A - B*Q
        return Polynomial(A.coeffs, A.field)

    def frobj(self, j):
        # sends sum a_ix^i to sum (a_i)^(p^j)x^(i*p^j) = sum a_i x^(i*p^j)
        p = self.field.char
        return Polynomial({i*p**j: self.coeffs[i] for i in self.coeffs}, self.field)

    def __str__(self):
        return ' + '.join([f'{str(self.coeffs[i])}*x^{i}' for i in sorted(self.coeffs)])

    @property
    def deg(self):
        return max(self.coeffs.keys())


def is_irreducible(poly):
    n = len(poly.coeffs)-1
    p = poly.field.char
    if n <= 3:
        for i in range(p):
            if poly.eval(poly.field(i)) == poly.field(0):
                return False
        return True
    else:
        raise NotImplementedError()
