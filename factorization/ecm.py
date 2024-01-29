'''
Lenstra's Elliptic Curve Factorization Algorithm implementation

This implementation follows Fig.11.3 from [AEC by Silverman, Chap XI].
'''
import math
import arithutil


def ecm_fac(N):
    # we should replace N with p here but we don't know p in advance...
    L = math.exp(math.sqrt(math.log(N)*math.log(math.log(N))))
    R = arithutil.init_ring_Z_mod_nZ(N)
    pass
    # TODO: complete this
