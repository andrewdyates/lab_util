#!/usr/bin/python
"""Print a squareform numpy matrix as a text symmetric matrix.

EXAMPLE USE:
  python to_square.py npyfname=mymatrix.npy n=5
"""
from py_symmetric_matrix import *
import numpy as np
import sys

def main(npyfname=None, n=None):
    assert npyfname, n is not None
    M = np.load(npyfname)
    n = int(n)
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                idx = sym_idx(i,j,n)
                row.append(M[idx])
        print " ".join(["%.4f"%x for x in row])

if __name__ == "__main__":
    main(**dict([s.split('=') for s in sys.argv[1:]]))
