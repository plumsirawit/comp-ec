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
    
    def eval(self, x, y):
        if not isinstance(x, self.field.FieldElem):
            raise TypeError('x is not a field element')
        if not isinstance(y, self.field.FieldElem):
            raise TypeError('y is not a field element')
        return y*y + self.a1*x*y + self.a3*y - x*x*x - self.a2*x*x - self.a4*x - self.a6

class WeierstrassCoord:
    INFTY = None
    # Treat this (x, y) as a point [x, y, 1] in P^2.
    def __init__(self, field, eqn, x, y):
        self.field = field
        self.eqn = eqn
        if eqn.field != field:
            raise TypeError('Field mismatched between field and eqn')
        self.x = x
        if not isinstance(x, field.FieldElem):
            raise TypeError('x is not a field element')
        self.y = y
        if not isinstance(y, field.FieldElem):
            raise TypeError('y is not a field element')
    def __add__(P, Q):
        if P.field != Q.field:
            raise ValueError('Base field for P and Q mismatched')
        if P.eqn != Q.eqn:
            raise ValueError('Base eqn for P and Q mismatched')
        if P.x == Q.x and P.y == Q.y:
            # duplicate this point
            lmb = (P.field(3)*P.x*P.x + P.field(2)*P.eqn.a1*P.x + P.eqn.a4 - P.eqn.a1*P.y)/(P.field(2)*P.y + P.eqn.a1*P.x + P.eqn.a3)
            nx = lmb*lmb + P.eqn.a1*lmb - P.eqn.a2 - P.x - P.x
            nu = (P.field(-1)*P.x*P.x*P.x + P.eqn.a4*P.x + P.field(2)*P.eqn.a6 - P.eqn.a3*P.y)/(P.field(2)*P.y + P.eqn.a1*P.x + P.eqn.a3)
            ny = P.field(-1)*(lmb + P.eqn.a1)*nx - nu - P.eqn.a3
            return WeierstrassCoord(P.field, P.eqn, nx, ny)
        elif P.x == Q.x:
            return WeierstrassCoord.INFTY
        else:
            # add points with different x's
            lmb = (Q.y - P.y)/(Q.x - P.x)
            nx = lmb*lmb + P.eqn.a1*lmb - P.eqn.a2 - P.x - Q.x
            nu = (P.y*Q.x - Q.y*P.x)/(Q.x - P.x)
            ny = P.field(-1)*(lmb + P.eqn.a1)*nx - nu - P.eqn.a3
            return WeierstrassCoord(P.field, P.eqn, nx, ny)
    def __str__(self):
        return f'({self.x.__str__()}, {self.y.__str__()})'

def order_of(P):
    i = 1
    Q = P
    while True:
        if Q == WeierstrassCoord.INFTY:
            return i
        Q = Q + P
        i += 1

def td5et6ex8():
    gf7 = arithutil.init_prime_field(7)
    eqn = WeierstrassEquation(gf7, gf7(0), gf7(0), gf7(0), gf7(0), gf7(2))
    for i in range(7):
        for j in range(7):
            if eqn.eval(gf7(i), gf7(j)) == gf7(0):
                P = WeierstrassCoord(gf7, eqn, gf7(i), gf7(j))
                print((i, j), order_of(P))

td5et6ex8()