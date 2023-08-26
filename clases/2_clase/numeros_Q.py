from fxpmath import Fxp
import numpy as np

M      = 2
N      = 14
SIGNED = True

if(SIGNED):
    MIN    = -2**(M-1)
    MAX    = 2**(M-1)-1/2**N
else:
    MIN    = 0
    MAX    = 2**(M)-1/2**N



for i in range(2**(M+N)):
    Q = Fxp(i/(2**N)+MIN, signed = SIGNED, n_word = M+N, n_frac  = N,rounding  = "trunc")    # create fixed-point object
    print("decimal: {0:.20f} \tbinary: {1:} \thex: {2:}"
          .format(i/2**N+MIN, Fxp.bin(Q),Fxp.hex(Q)))

