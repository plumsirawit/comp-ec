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
