from arithutil.BaseField import BaseField, BaseFieldElem
import random

def init_prime_field(p):
    """
    Initializes a prime field $\mathbb{F}_p$.
    """
    class PrimeField(BaseField):
        char = p
        card = p

        @classmethod
        def random_element(cls):
            return cls(random.randint(0, p-1))

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
                return x ** (p - 2)

            @classmethod
            def eql(cls, x, y):
                return x.a == y.a

        def __init__(self):
            self.FieldElem.field = self

        def __str__(self):
            return f'PrimeField({self.card})'
    return PrimeField()
