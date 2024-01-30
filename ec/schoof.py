"""
Schoof's algorithm to count the number of points on an elliptic curve over a finite field

This implementation follows Fig.11.4 from [AEC by Silverman, Chap XI].
"""

def schoof(E):
    field = E.field
    q = field.card
    A = 1
    l = 3
    while A < 4*q**0.5:
        for n in range(l):
            pass