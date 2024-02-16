from arithutil import init_prime_field, init_extended_field, Polynomial, sqrt_cyclic
import itertools

p = 7
n = 3
gf = init_prime_field(p)
ef = init_extended_field(p, n)


def enumelem(ef):
    p = ef.char
    gf = ef.base_field
    bd = ef.base_poly.deg
    prod = itertools.product(map(gf, range(p)), repeat=bd)
    return [ef(Polynomial([it[i] for i in range(bd)], gf)) for it in prod]


elems = enumelem(ef)
for i in range(p**n):
    try:
        sol = sqrt_cyclic(ef, elems[i])
        print(sol*sol - elems[i])
    except ValueError as e:
        print(e)