import numpy as np
import math

# bezier curve
def bernstein(n, i, t):
    ncr = math.factorial(n) / (math.factorial(i) * math.factorial((n - i)))
    return ncr * t**i * (1 - t)**(n-i)

def bezier(n, t, q):
    p = np.zeros(2)
    for i in range(n + 1):
        p += bernstein(n, i, t) * q[i]
    return p

