from arithutil.Polynomial import *


class RationalFunction:
    """
    Structure for fraction of polynomials over a field.
    """

    def __init__(self, x, field):
        self.field = field
        if isinstance(x, tuple) and isinstance(x[0], Polynomial) and isinstance(x[1], Polynomial):
            self.numerator, self.denominator = x
        elif isinstance(x, Polynomial):
            self.numerator = x
            self.denominator = field(1)
        elif isinstance(x, int):
            self.numerator = field(x)
            self.denominator = field(1)
        elif isinstance(x, field):
            self.numerator = x
            self.denominator = field(1)

    def reduce(self):
        """
        Reduces the fraction. Warning: this function mutates the object!
        """
        g = self.numerator.gcd(self.denominator)
        self.numerator /= g
        self.denominator /= g
        return self

    def __add__(self, other):
        return RationalFunction((self.numerator * other.denominator + self.denominator * other.numerator,
                                 self.denominator * other.denominator), self.field).reduce()

    def __sub__(self, other):
        return (self + RationalFunction((-other.numerator, other.denominator), self.field)).reduce()

    def __mul__(self, other):
        return RationalFunction((self.numerator * other.numerator, self.denominator * other.denominator),
                                self.field).reduce()

    def __truediv__(self, other):
        return RationalFunction((self.numerator * other.denominator, self.denominator * other.numerator),
                                self.field).reduce()

    def __eq__(self, other):
        return self.numerator * other.denominator == self.denominator * other.numerator
