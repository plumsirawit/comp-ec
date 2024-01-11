from arithutil import Polynomial, init_prime_field

p = 5
n = 3
gf = init_prime_field(p)
a = Polynomial([gf(2), gf(3), gf(1)], gf)

r = (p**n-1)//(p-1)
l = r.bit_length()
print(l)
ts = [Polynomial([a.field(0)], gf), a.frobj(1)]
for i in range(2, l+1):
    ts.append(ts[-1] * ts[-1].frobj(2**(i-2)))

print('ts', list(map(str, ts)))

g = n-1
buf = Polynomial([a.field(0)], gf)

print(g)
while g > 0:
    print('DBG', g.bit_length())
    buf = buf + ts[g.bit_length()].frobj(g-2**(g.bit_length()-1))
    g -= 2**(g.bit_length()-1)
den = buf * a

print(buf, den*den*den*den)
res = a
for i in range(123):
    res = res * a
print(res)