#!/usr/bin/python
"""Convert a .mat matrix and variable list into a .tab file.

EXAMPLE USE:
  python matlab_fname=mymat.mat tab_fname=mydata.raw.tab
"""
import sys
import scipy.io as sio
import numpy as np

def main(matlab_fname=None, tab_fname=None, matrix_name="M"):

  matlab_fname = sys.argv[1]
  tab_fname = sys.argv[2]

  M = sio.loadmat(matlab_fname)[matrix_name]
  fp = open(tab_fname)
  assert fp.next()[0] == '#'
  varlist = [s.split('\t')[0] for s in fp]
  fp.close()
  assert varlist[-1]
  assert len(varlist) == np.size(M,0)

  for i, row in enumerate(M):
    print varlist[i] + '\t' + '\t'.join(["%f"%v for v in row])


if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
