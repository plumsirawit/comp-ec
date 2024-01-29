'''
Pollard's p-1 algorithm implementation

This implementation follows Fig.11.2 from [AEC by Silverman, Chap XI].
'''
import math


def modpow(base, expo, modulus):
    if expo == 0:
        return 1
    elif base == 0:
        return 0
    half = modpow(base, expo // 2, modulus)
    if expo % 2 == 1:
        return half * half * base % modulus
    else:
        return half * half % modulus


def pollard_grp_fac(N):
    for a in range(2, N):
        A = a
        i = 1
        while True:
            A = modpow(A, i, N)
            F = math.gcd(A-1, N)
            if 1 < F < N:
                return F
            elif F == N:
                break
            i += 1
