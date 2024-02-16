"""
Miller's algorithm to compute the Weil pairing

This implementation follows Fig.11.6 from [AEC by Silverman, Chap XI].
"""
import arithutil


def h(P, Q, T):
    """
    $h_{P,Q}(T)$ from the definition in [AEC by Silverman, XI.8.1a].
    """
    field = P.field
    if (P.x is None and P.y is None) or (Q.x is None and Q.y is None):
        return field(1)
    elif P.x == Q.x and P.y == Q.y:
        # duplicate this point
        lmb = (P.field(3) * P.x * P.x + P.field(2) * P.eqn.a2 * P.x + P.eqn.a4 -
               P.eqn.a1 * P.y) / (P.field(2) * P.y + P.eqn.a1 * P.x + P.eqn.a3)
    elif P.x == Q.x:
        return T.x - P.x
    else:
        # add points with different x's
        lmb = (Q.y - P.y) / (Q.x - P.x)
    return (T.y - P.y - lmb * (T.x - P.x)) / (T.x + P.x + Q.x - lmb * lmb - P.eqn.a1 * lmb + P.eqn.a2)


def miller(P, N, S):
    """
    Computes $f_P(S) \in K(E)$ such that $\mathrm{div}(f_P) = N(P) - ([N]P) - (N-1)(O)$.
    """
    t = N.bit_length() - 1
    f = P.field(1)
    T = P
    for i in range(t - 1, -1, -1):
        f = f * f * h(T, T, S)
        T = T + T
        if (N & (1 << i)) != 0:
            f = f * h(T, P, S)
            T = T + P
    return f

def weil(N, P, Q):
    """
    Computes the N-Weil pairing for (P, Q).
    """
    # Randomize S until P, P-S, Q, Q+S are all distinct.
    E = P.eqn
    while True:
        S = E.random_element()
        if len({S, P-S, Q, Q+S}) == 4:
            break
    return miller(P, N, Q+S) * miller(Q, N, -S) / (miller(P, N, S) * miller(Q, N, P-S))
