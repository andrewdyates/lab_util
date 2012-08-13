#!/usr/bin/python
import numpy as np
import os

# http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html#numpy.genfromtxt
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html#numpy.loadtxt

# handles comments correctly, but not variable names
def name_iter(fp, varlist):
  for line in fp:
    if line[0] in ('#','\n'): continue
    name,c,row = line.partition('\t')
    varlist.append(name)
    yield row

def tab_to_npy(tab_fname):
  varlist = []
  M = np.genfromtxt(name_iter(open(tab_fname), varlist), usemask=True, delimiter='\t')
  return M, varlist
