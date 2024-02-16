import arithutil


class WeierstrassEquation:
    def __init__(self, field, a1, a2, a3, a4, a6):
        # these values must be field elements
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a6 = a6
        self.field = field
        if not isinstance(a1, field.FieldElem):
            raise TypeError('a1 is not a field element')
        if not isinstance(a2, field.FieldElem):
            raise TypeError('a2 is not a field element')
        if not isinstance(a3, field.FieldElem):
            raise TypeError('a3 is not a field element')
        if not isinstance(a4, field.FieldElem):
            raise TypeError('a4 is not a field element')
        if not isinstance(a6, field.FieldElem):
            raise TypeError('a6 is not a field element')
        if self.disc == field(0):
            raise ValueError('The curve is not smooth')

    @property
    def b2(self):
        return self.a1*self.a1 + self.field(4)*self.a2

    @property
    def b4(self):
        return self.field(2)*self.a4 + self.a1*self.a3

    @property
    def b6(self):
        return self.a3*self.a3 + self.field(4)*self.a6

    @property
    def b8(self):
        return self.a1*self.a1*self.a6 + self.field(4)*self.a2*self.a6 - self.a1*self.a3*self.a4 + self.a2*self.a3*self.a3 - self.a4*self.a4

    @property
    def disc(self):
        return -self.b2*self.b2*self.b8 - self.field(8)*self.b4*self.b4*self.b4 - self.field(27)*self.b6*self.b6 + self.field(9)*self.b2*self.b4*self.b6

    def eval(self, x, y):
        if not isinstance(x, self.field.FieldElem):
            raise TypeError('x is not a field element')
        if not isinstance(y, self.field.FieldElem):
            raise TypeError('y is not a field element')
        return y*y + self.a1*x*y + self.a3*y - x*x*x - self.a2*x*x - self.a4*x - self.a6

    def __str__(self):
        return f'E: Y^2Z + {self.a1}XYZ + {self.a3}YZ^2 = X^3 + {self.a2}X^2Z + {self.a4}XZ^2 + {self.a6}Z^3'
    
    def random_element(self):
        while True:
            x = self.field.random_element()
            if self.a1 != self.field(0) or self.a3 != self.field(0):
                raise NotImplementedError('The general case hasn\'t yet been implemented')
            ysq = x*x*x + self.a2*x*x + self.a4*x + self.a6
            try:
                y = arithutil.sqrt_cyclic(self.field, ysq)
                return WeierstrassCoord(self.field, self, x, y)
            except ValueError:
                pass


class WeierstrassCoord:
    # Treat this (x, y) as a point [x, y, 1] in P^2.

    def __init__(self, field, eqn, x, y):
        self.field = field
        self.eqn = eqn
        if x is None and y is None:
            self.x = self.y = None
            return
        if eqn.field != field:
            raise TypeError('Field mismatched between field and eqn')
        self.x = x
        if not isinstance(x, field.FieldElem):
            raise TypeError('x is not a field element')
        self.y = y
        if not isinstance(y, field.FieldElem):
            raise TypeError('y is not a field element')

    @property
    def is_infty(self):
        return self.x is None and self.y is None

    def __add__(P, Q):
        if P.field != Q.field:
            raise ValueError('Base field for P and Q mismatched')
        if P.eqn != Q.eqn:
            raise ValueError('Base eqn for P and Q mismatched')
        if P.is_infty:
            return WeierstrassCoord(Q.field, Q.eqn, Q.x, Q.y)
        elif Q.is_infty:
            return WeierstrassCoord(P.field, P.eqn, P.x, P.y)
        elif P.x == Q.x and P.y == Q.y:
            # duplicate this point
            lmb = (P.field(3)*P.x*P.x + P.field(2)*P.eqn.a2*P.x + P.eqn.a4 -
                   P.eqn.a1*P.y)/(P.field(2)*P.y + P.eqn.a1*P.x + P.eqn.a3)
            nx = lmb*lmb + P.eqn.a1*lmb - P.eqn.a2 - P.x - P.x
            nu = (P.field(-1)*P.x*P.x*P.x + P.eqn.a4*P.x + P.field(2) *
                  P.eqn.a6 - P.eqn.a3*P.y)/(P.field(2)*P.y + P.eqn.a1*P.x + P.eqn.a3)
            ny = P.field(-1)*(lmb + P.eqn.a1)*nx - nu - P.eqn.a3
            return WeierstrassCoord(P.field, P.eqn, nx, ny)
        elif P.x == Q.x:
            return WeierstrassCoord(P.field, P.eqn, None, None)
        else:
            # add points with different x's
            lmb = (Q.y - P.y)/(Q.x - P.x)
            nx = lmb*lmb + P.eqn.a1*lmb - P.eqn.a2 - P.x - Q.x
            nu = (P.y*Q.x - Q.y*P.x)/(Q.x - P.x)
            ny = P.field(-1)*(lmb + P.eqn.a1)*nx - nu - P.eqn.a3
            return WeierstrassCoord(P.field, P.eqn, nx, ny)
        
    def __sub__(self, o):
        return self.__add__(o.__neg__())

    def __neg__(self):
        return WeierstrassCoord(self.field, self.eqn, self.x, -self.y)

    def mul(self, n):
        """
        Returns [n](P) where P is the current point. Uses double-and-add algorithm.
        This implementation follows Fig.11.1 from [AEC by Silverman, Chap XI]
        """
        if not isinstance(n, int):
            raise TypeError(f'Invalid type {type(n)} for multiplication-by-m map')
        Q = self
        R = WeierstrassCoord(self.field, self.eqn, None, None) if n % 2 == 0 else self
        t = n.bit_length() - 1
        for i in range(1, t+1):
            Q = Q + Q
            if (n & (1 << i)) != 0:
                R = R + Q
        return R


    def __str__(self):
        return f'({self.x.__str__()}, {self.y.__str__()})'
