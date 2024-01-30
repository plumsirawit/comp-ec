"""
ElGamal Public Key Cryptosystem implementation (Menezes-Vanstone variant)

This implementation follows [AEC by Silverman, XI.4.4] and [AEC by Silverman, Exercise 11.10].
"""
import random


class ElGamalContext:
    def __init__(self, field, curve, point):
        self.field = field
        self.curve = curve
        self.point = point


def alice_init(ctx):
    q = ctx.field.card
    a = random.randint(0, q-1)  # secret key
    A = ctx.point.mul(a)        # public key
    return a, A

# Alice publishes A.


def bob(ctx, m, A):
    q = ctx.field.card
    k = random.randint(q // 2, q - 1)
    m1 = ctx.field(m // q)
    m2 = ctx.field(m % q)
    B1 = ctx.point.mul(k)
    B2 = A.mul(k)
    x, y = B2.x, B2.y
    c1 = x*m1
    c2 = y*m2
    return (B1, c1, c2)


def alice_receive(a, B1, c1, c2):
    B2 = B1.mul(a)
    x, y = B2.x, B2.y
    m1 = c1/x
    m2 = c2/y
    return (m1, m2)
