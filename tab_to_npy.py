#!/usr/bin/python
import numpy as np
import os

TEST_FILE=os.path.expanduser("~/Dropbox/biostat/eqtl_data/GSE25935/GSE25935.GPL4133.eQTL.nooutliers.tab")

# this does not (yet) work
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html#numpy.genfromtxt
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html#numpy.loadtxt

# handles comments correctly, but not variable names
def name_iter(fp, varlist):
  for line in fp:
    if line[0] == '#': continue
    name,c,row = line.partition('\t')
    varlist.append(name)
    yield row

varlist = []
M = np.genfromtxt(name_iter(open(TEST_FILE), varlist), usemask=True, delimiter='\t')



