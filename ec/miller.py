"""
Miller's algorithm to compute the Weil pairing

This implementation follows Fig.11.6 from [AEC by Silverman, Chap XI].
"""
import arithutil

def h(P, Q):
    """
    $h_{P,Q}$ from the definition in [AEC by Silverman, XI.8.1a].
    """
    field = P.field
    if (P.x is None and P.y is None) or (Q.x is None and Q.y is None):
        return arithutil.RationalFunction(field(1), field)
    elif P.x == Q.x and P.y == Q.y:
        # duplicate this point
        lmb = (P.field(3) * P.x * P.x + P.field(2) * P.eqn.a2 * P.x + P.eqn.a4 -
               P.eqn.a1 * P.y) / (P.field(2) * P.y + P.eqn.a1 * P.x + P.eqn.a3)
    elif P.x == Q.x:
        return arithutil.RationalFunction(arithutil.Polynomial([-P.x, 1], field), field)
    else:
        # add points with different x's
        lmb = (Q.y - P.y) / (Q.x - P.x)
    # TODO: implement
    pass

def miller(P, N):
    """
    Computes $f_P \in K(E)$ such that $\mathrm{div}(f_P) = N(P) - ([N]P) - (N-1)(O)$.
    """
    t = N.bit_length() - 1
    f = arithutil.RationalFunction(P.field(1), P.field)
    T = P
    for i in range(t-1, -1, -1):
        f = f * f * h(T, T)
        T = T+T
        if (N & (1 << i)) != 0:
            f = f * h(T, P)
            T = T + P
    return f