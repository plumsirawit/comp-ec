import arithutil

gf = arithutil.init_extended_field(2, 2)


def mult_order_of(x):
    i = 1
    t = x
    lim = 100
    for _ in range(lim):
        if t == gf(1):
            return i
        t = t * x
        i += 1
    print('DBG: Lim hit', t)


print('base_poly:', gf.base_poly)
bf = gf.base_field
print('enumeration:')
a = gf(arithutil.Polynomial([bf(0)], bf))
print(a, mult_order_of(a))
b = gf(arithutil.Polynomial([bf(1)], bf))
print(b, mult_order_of(b))
c = gf(arithutil.Polynomial([bf(0), bf(1)], bf))
print(c, mult_order_of(c))
d = gf(arithutil.Polynomial([bf(1), bf(1)], bf))
print(d, mult_order_of(d))
