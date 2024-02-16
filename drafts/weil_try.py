'''
Example 8.3 from [AEC by Silverman, Chap XI].
'''

import arithutil
import ec

p = 631
gf = arithutil.init_prime_field(p)

E = ec.WeierstrassEquation(gf, gf(0), gf(0), gf(0), gf(30), gf(34))
P = ec.WeierstrassCoord(gf, E, gf(36), gf(60))
Q = ec.WeierstrassCoord(gf, E, gf(121), gf(387))

print(ec.weil(5, P, Q))
# 242 -- correct