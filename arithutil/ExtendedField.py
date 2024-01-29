from .PrimeField import init_prime_field
from .Polynomial import Polynomial, is_irreducible
from .BaseField import BaseField, BaseFieldElem
import random


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
