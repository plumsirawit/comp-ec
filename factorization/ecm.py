"""
Lenstra's Elliptic Curve Factorization Algorithm implementation

This implementation follows Fig.11.3 from [AEC by Silverman, Chap XI].
"""
import math
import arithutil
import random
import ec


def random_curve_and_point(R):
    N = R.char
    A = R(random.randint(0, N - 1))
    x0 = R(random.randint(0, N - 1))
    y0 = R(random.randint(0, N - 1))
    B = y0 * y0 - x0 * x0 * x0 - A * x0
    E = ec.grpformula.WeierstrassEquation(R, R(0), R(0), R(0), A, B)
    return E, ec.grpformula.WeierstrassCoord(R, E, x0, y0)


def ecm_fac(N):
    # we should replace N with p here, but we don't know p in advance...
    L = int(math.exp(math.sqrt(math.log(N) * math.log(math.log(N)))))
    R = arithutil.init_ring_Z_mod_nZ(N)
    while True:
        E, P = random_curve_and_point(R)
        Q = P
        for i in range(2, L + 1):
            try:
                Q = Q.mul(i)
            except ZeroDivisionError as e:
                _, a = e.args
                if a != 0:
                    return math.gcd(a, N)
