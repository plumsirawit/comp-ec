'''
Shanks-Tonelli algorithm for square root in a cyclic group.
'''
import math

def pow2(b, e):
    '''
    Compute $b^{2^e}$ where `b`, representing $b$, is a FieldElement and `e`, representing $e$, is a natural.
    '''
    c = b
    for _ in range(e):
        c = c * c
    return c

def sqrt_cyclic(field, elem):
    z = field(1)
    p = field.char
    n = round(math.log(field.card)/math.log(p))
    if elem == field(0):
        return elem
    if p == 2:
        return pow2(elem, n-1)
    if elem ** ((p**n - 1) // 2) != field(1):
        raise ValueError(f'no solution exists for x^2 == {elem} in GF({p}^{n})')
    while z ** ((p**n - 1)//2) != field(-1):
        z = field.random_element()
    Q = p**n - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    R = elem ** ((Q+1) // 2)
    if elem ** Q == field(1):
        return R
    t = R * R / elem
    buf = z ** Q
    for i in range(1, S):
        if pow2(t, S-i-1) == field(1):
            b = field(1)
        else:
            b = buf
        R = R * b
        t = t * b * b
        buf = buf * buf
    return R