import arithutil
import ec

p = 2**255-19
gf = arithutil.init_prime_field(p)
eqn = ec.WeierstrassEquation(gf, gf(0), gf(486662), gf(0), gf(1), gf(0))
x0 = gf(9)
y0 = gf(14781619447589544791020593568409986887264606134616475288964881837755586237401)
base_point = ec.WeierstrassCoord(gf, eqn, x0, y0)
ctx = ec.ElGamalContext(gf, eqn, base_point)

# a, A = ec.alice_init(ctx)
# print('privkey:', a, 'pubkey:', A)
a = 57129898734736257057139890655186600157903241342451384718617037783145307976196
A = ec.WeierstrassCoord(gf, eqn, gf(48272915282627254591303957411811913476869743597450481423681623354793831685857), gf(4589540048341746297949945697709704689681956343002619342185734254093111092244))

# Bob wants to send the message 4211265535 to Alice
B1, c1, c2 = ec.bob(ctx, 4211265535, A)
print(B1, c1, c2)

# B1 = ec.WeierstrassCoord(gf, eqn, gf(21506225312030459844903898252018370611659366429008955615703263628049848546302), gf(10764869784543944751455335707079181470574056193809831146504394843320299991655))
# c1 = gf(0)
# c2 = gf(8430434742040993105380064088652981008655240107894019955578862321823994936177)

# Alice recovers the message
m1, m2 = ec.alice_receive(a, B1, c1, c2)
print(m1.a * p + m2.a)