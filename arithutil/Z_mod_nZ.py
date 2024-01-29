from arithutil.BaseField import BaseField, BaseFieldElem
from arithutil.util import euclid
import math


def init_ring_Z_mod_nZ(n):
    """
    Initializes $\mathbb{Z}/n\mathbb{Z}$ as a fake field. `ZeroDivisionError` will be raised when
    a division is attempted on a non-invertible element.
    """
    # This is a fake field, but I don't want to implement another object called "rings"...
    class Z_mod_nZ(BaseField):
        char = n
        card = n

        class FieldElem(BaseFieldElem):
            def __init__(self, x):
                if isinstance(x, int):
                    self.a = x % n
                else:
                    raise TypeError(f'Unknown type {type(x)}')

            @classmethod
            def add(cls, x, y):
                return cls((x.a + y.a) % n)

            @classmethod
            def addinv(cls, x):
                return cls((n - x.a) % n)

            @classmethod
            def mul(cls, x, y):
                return cls((x.a * y.a) % n)

            @classmethod
            def mulinv(cls, x):
                # If xy = kn + 1 for some k, then y corresponds to a in
                # each solution (a, b) to the equation ax + bn = 1.
                g = math.gcd(x, n)
                # If gcd(x, n) != 1, raise a zero div error
                if g != 1:
                    raise ZeroDivisionError(f'{x} is not invertible in Z/{n}Z')
                a, b = euclid(x, n)
                return a

            @classmethod
            def eql(cls, x, y):
                return x.a == y.a

        def __init__(self):
            self.FieldElem.field = self

        def __str__(self):
            return f'Z_mod_{self.card}Z'
    return Z_mod_nZ()
