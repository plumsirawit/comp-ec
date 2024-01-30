class BaseField:
    """
    A basic structure for a field. This structure should contain card, char,
    and another class FieldElem inside it. Calling this class with `x` should
    mean creating an element with value `x`.
    """
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


class BaseFieldElem:
    """
    A basic structure for an element of a field. Addition, additive inverse,
    multiplication, and multiplicative inverse should all be well-defined.
    """

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

    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError(f'Invalid type {type(n)} for __pow__')
        q = self
        t = n.bit_length() - 1
        r = self if n % 2 == 1 else self.__class__(1)
        for i in range(1, t+1):
            q = q * q
            if (n & (1 << i)) != 0:
                r = r * q
        return r
