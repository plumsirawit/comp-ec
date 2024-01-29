from arithutil import Polynomial, init_prime_field, init_extended_field, is_irreducible

p = 5
n = 3
gf = init_prime_field(p)
a = Polynomial([gf(2), gf(3), gf(1)], gf)
init_extended_field(p, n)
MOD = Polynomial([gf(1), gf(1), gf(0), gf(1)], gf)

r = (p**n-1)//(p-1)
l = r.bit_length()
print('a', a)
ts = [Polynomial([a.field(0)], gf), a.frobj(1)]
for i in range(2, l):
    ts.append(ts[-1] * ts[-1].frobj(2**(i-2)) % MOD)

print('ts', list(map(str, ts)))

# exit(0)

g = n-1
buf = Polynomial([a.field(0)], gf)

print(g)
while g > 0:
    print('DBG', g.bit_length(), ts[g.bit_length()].frobj(
        g-2**(g.bit_length()-1)))
    buf = buf + ts[g.bit_length()].frobj(g-2**(g.bit_length()-1))
    g -= 2**(g.bit_length()-1)
den = buf * a % MOD

print('here', MOD, den)
res = a
for i in range(30):
    res = res * a
print(res % MOD)
