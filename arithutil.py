import random


class BaseFieldElem:
    def __init__(self, x):
        self.a = x

    def __str__(self):
        return self.a.__str__()

    @classmethod
    def add(cls, x, y):
        return NotImplementedError(f"+ isn't implemented for {cls.__name__}")

    @classmethod
    def addinv(cls, x):
        return NotImplementedError(f"- isn't implemented for {cls.__name__}")

    @classmethod
    def mul(cls, x, y):
        return NotImplementedError(f"* isn't implemented for {cls.__name__}")

    @classmethod
    def mulinv(cls, x):
        return NotImplementedError(f"/ isn't implemented for {cls.__name__}")

    @classmethod
    def eql(cls, x, y):
        return NotImplementedError(f"eql isn't implemented for {cls.__name__}")

    def __add__(self, o):
        return self.add(self, o)

    def __sub__(self, o):
        return self.add(self, self.addinv(o))

    def __neg__(self):
        return self.addinv(self)

    def __mul__(self, o):
        return self.mul(self, o)

    def __truediv__(self, o):
        # print(f'[LOG] {self}/{o}')
        return self.mul(self, self.mulinv(o))

    def __eq__(self, o):
        return self.eql(self, o)


class BaseField:
    class FieldElem:
        def __init__(self):
            raise NotImplementedError(f"FieldElem isn't implemented")

    def __call__(self, x):
        return self.FieldElem(x)

    def __eq__(self, o):
        if not hasattr(self, 'card') or not isinstance(self.card, int):
            raise ValueError(f'card is invalid in {self}')
        if not hasattr(o, 'card') or not isinstance(o.card, int):
            raise ValueError(f'card is invalid in {o}')
        return self.card == o.card


def init_prime_field(p):
    class PrimeField(BaseField):
        char = p
        card = p

        class FieldElem(BaseFieldElem):
            def __init__(self, x):
                if isinstance(x, int):
                    self.a = x % p
                else:
                    raise TypeError(f'Unknown type {type(x)}')

            @classmethod
            def add(cls, x, y):
                return cls((x.a + y.a) % p)

            @classmethod
            def addinv(cls, x):
                return cls((p - x.a) % p)

            @classmethod
            def mul(cls, x, y):
                return cls((x.a * y.a) % p)

            @classmethod
            def mulinv(cls, x):
                return cls((x.a ** (p - 2)) % p)

            @classmethod
            def eql(cls, x, y):
                return x.a == y.a

        def __init__(self):
            self.FieldElem.field = self

        def __str__(self):
            return f'PrimeField({self.card})'
    return PrimeField()


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


def init_extended_field(p, n, modulus=None):  # q = p^n
    gf = init_prime_field(p)
    base_arr = [gf(0) for _ in range(n+1)]
    base_arr[n] = gf(1)
    if modulus is None:
        modulus = Polynomial(base_arr, gf)
        for i in range(n):
            modulus.coeffs[i] = gf(random.randint(0, p-1))
        while not is_irreducible(modulus):
            for i in range(n):
                modulus.coeffs[i] = gf(random.randint(0, p-1))
    else:
        if not is_irreducible(modulus):
            raise ValueError(f'modulus {modulus} is not irreducible')

    class ExtendedField(BaseField):
        char = p
        card = p**n
        base_field = gf
        base_poly = modulus

        def __str__(self):
            return f'ExtendedField({self.card})'

        class FieldElem(BaseFieldElem):
            def __init__(self, x):
                if isinstance(x, Polynomial):
                    self.a = Polynomial(x.coeffs, x.field)
                elif isinstance(x, int):
                    self.a = Polynomial([gf(x)], gf)
                else:
                    raise TypeError(f'Unknown type {type(x)}')

            @classmethod
            def add(cls, x, y):
                return cls((x.a + y.a) % modulus)

            @classmethod
            def addinv(cls, x):
                return cls((-x.a) % modulus)

            @classmethod
            def mul(cls, x, y):
                return cls((x.a * y.a) % modulus)

            @classmethod
            def mulinv(cls, x):
                if x == cls(0):
                    raise ZeroDivisionError(f'zero division in class {cls}')
                # Itoh-Tsujii
                # https://crypto.stackexchange.com/questions/81137/itoh-tsuji-algorithm
                r = (p**n-1)//(p-1)
                l = r.bit_length()
                ts = [Polynomial([x.a.field(0)], x.a.field), x.a.frobj(1)]
                for i in range(2, l):
                    pol = ts[-1] * ts[-1].frobj(2**(i-2))
                    ts.append(pol % modulus)
                g = n-1
                buf = Polynomial([x.a.field(1)], x.a.field)
                while g > 0:
                    buf = buf * ts[g.bit_length()].frobj(g-2 **
                                                         (g.bit_length()-1)) % modulus
                    g -= 2**(g.bit_length()-1)
                den = buf * x.a % modulus
                if 0 not in den.coeffs:
                    # FIXED: Fix this bug!
                    raise ValueError(
                        'field is invalid (check that modulus is irreducible)')
                return cls(buf * Polynomial([gf(1) / den.coeffs[0]], gf) % modulus)

            @classmethod
            def eql(cls, x, y):
                P = Polynomial(((x.a - y.a) % modulus).coeffs, gf)
                return len(P.coeffs) == 1 and next(iter(P.coeffs.values())) == gf(0)
    return ExtendedField()
