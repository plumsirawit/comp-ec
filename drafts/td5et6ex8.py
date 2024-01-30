from ec.grpformula import *


def order_of(P, lim=100):
    i = 1
    Q = P
    for _ in range(lim):
        if Q == WeierstrassCoord.INFTY:
            return i
        Q = Q + P
        i += 1


def td5et6ex8():
    gf7 = arithutil.init_prime_field(7)
    eqn = WeierstrassEquation(gf7, gf7(0), gf7(0), gf7(0), gf7(0), gf7(2))
    print('===GF(7)===')
    for i in range(7):
        for j in range(7):
            if eqn.eval(gf7(i), gf7(j)) == gf7(0):
                P = WeierstrassCoord(gf7, eqn, gf7(i), gf7(j))
                print((i, j), order_of(P))
    gf49 = arithutil.init_extended_field(7, 2)
    gf49z = gf49(arithutil.Polynomial([gf49.base_field(0)], gf49.base_field))
    gf49two = gf49(arithutil.Polynomial([gf49.base_field(2)], gf49.base_field))
    eqn2 = WeierstrassEquation(gf49, gf49z, gf49z, gf49z, gf49z, gf49two)
    print('===GF(49)===')
    prec = []
    for i in range(7):
        for j in range(7):
            prec.append(gf49(arithutil.Polynomial(
                [gf49.base_field(i), gf49.base_field(j)], gf49.base_field)))
    for i in range(49):
        for j in range(49):
            if eqn2.eval(prec[i], prec[j]) == prec[0]:
                P = WeierstrassCoord(gf49, eqn2, prec[i], prec[j])
                print((i, j), order_of(P))


td5et6ex8()
