from arithutil import init_prime_field, init_extended_field, Polynomial
import itertools

p = 5
n = 3
gf = init_prime_field(p)
# 3*x^0 + 4*x^1 + 4*x^2 + 1*x^3
base_poly = Polynomial([gf(3), gf(4), gf(4), gf(1)], gf)
# base_poly = Polynomial([gf(3), gf(1), gf(2), gf(1)], gf)
ef = init_extended_field(p, n, base_poly)


def enumelem(ef):
    p = ef.char
    gf = ef.base_field
    bd = ef.base_poly.deg
    prod = itertools.product(map(gf, range(p)), repeat=bd)
    return [ef(Polynomial([it[i] for i in range(bd)], gf)) for it in prod]


elems = enumelem(ef)
print('ELEMS:')
# invs = [ef(1)/el if el != ef(0) else ef(0) for el in elems]
for i in range(len(elems)):
    acc = ef(1)
    for j in range(p**n):
        acc = acc * elems[i]
    print(i, '%30s :: %30s' % (elems[i], acc))
    # print(elems[i] * invs[i])
    # print('%25s :: %25s' % (str(elems[i]), str(invs[i])))
