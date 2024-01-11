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
        return self.mul(self, self.mulinv(o))
    def __eq__(self, o):
        return self.eql(self, o)

class BaseField:
    class FieldElem:
        def __init__(self):
            raise NotImplementedError(f"FieldElem isn't implemented")
    def __call__(self, x):
        return self.FieldElem(x)

def init_prime_field(p):
    class PrimeField(BaseField):
        char = p
        card = p
        class FieldElem(BaseFieldElem):
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
                if g >= 2**j:
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
        return Polynomial(sum_dict, self.field)
    def __neg__(self):
        return Polynomial({i : -self.coeffs[i] for i in self.coeffs}, self.field)
    def __sub__(self, o):
        return self + (-o)
    def __mul__(self, o):
        # This can even be speeded up faster using FFT but we're not doing it here
        P = self if len(self.coeffs) < len(o.coeffs) else o
        Q = o if len(self.coeffs) < len(o.coeffs) else self
        degP = max(P.coeffs.keys())
        degQ = max(Q.coeffs.keys())
        # print('MUL', P, Q)
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
        degA = max(A.coeffs.keys())
        degB = max(B.coeffs.keys())
        if degA < degB:
            return A
        shf = degA - degB
        mul = A.coeffs[degA] / B.coeffs[degB]
        Q = Polynomial({shf: mul}, A.field)
        # print('rec', A, ':', B, ':', Q, ':', B*Q)
        return Polynomial((A - B*Q).coeffs, A.field) % B
    def frobj(self, j):
        # sends sum a_ix^i to sum (a_i)^(p^j)x^(i*p^j) = sum a_i x^(i*p^j)
        p = self.field.char
        return Polynomial({i*p**j: self.coeffs[i] for i in self.coeffs}, self.field)
    def __str__(self):
        return ' + '.join([f'{str(self.coeffs[i])}*x^{i}' for i in sorted(self.coeffs)])

def is_irreducible(poly):
    n = len(poly.coeffs)-1
    p = poly.field.char
    if n <= 3:
        for i in range(p):
            if poly.eval(poly.field(i)) == poly.field(0):
                print('DBG', i, poly.eval(poly.field(i)))
                return False
        return True
    else:
        raise NotImplementedError()

def init_extended_field(p, n): # q = p^n
    gf = init_prime_field(p)
    base_arr = [gf(0) for _ in range(n+1)]
    base_arr[n] = gf(1)
    base_poly = Polynomial(base_arr, gf)
    for i in range(n):
        base_poly.coeffs[i] = gf(random.randint(0, p-1))
    while not is_irreducible(base_poly):
        for i in range(n):
            base_poly.coeffs[i] = gf(random.randint(0, p-1))
    print('MOD', base_poly)
    return
    class ExtendedField(BaseField):
        char = p
        card = p**n
        base_field = gf
        class FieldElem(BaseFieldElem):
            @classmethod
            def add(cls, x, y):
                return cls((x.a + y.a) % base_poly)
            @classmethod
            def addinv(cls, x):
                return cls((p - x.a) % base_poly)
            @classmethod
            def mul(cls, x, y):
                return cls((x.a * y.a) % base_poly)
            @classmethod
            def mulinv(cls, x):
                # Itoh-Tsujii
                # https://crypto.stackexchange.com/questions/81137/itoh-tsuji-algorithm
                # r = (p**n-1)//(p-1)
                # l = r.bit_length()
                # ts = [Polynomial([x.a.field(0)], x.a.field), x.a.frobj(1)]
                # for i in range(2, l+1):
                #     ts.append(ts[-1] * ts[-1].frobj(2**(i-2)))
                # g = n-1
                # buf = Polynomial([x.a.field(0)], x.a.field)
                # while g >= 0:
                #     buf = buf + x.a.frobj(g-2**(g.bit_length()-1)) * ts[g.bit_length()]
                #     g -= 2**(g.bit_length()-1)
                # den = buf * x.a
                # return cls((x.a ** (p - 2)) % p)
                pass
            @classmethod
            def eql(cls, x, y):
                return x.a == y.a