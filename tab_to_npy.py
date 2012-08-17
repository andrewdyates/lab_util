#!/usr/bin/python
import numpy as np

# http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html#numpy.genfromtxt
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html#numpy.loadtxt

def name_iter(fp, varlist):
  """Yield next row of floats w/o ID in first column; append ID to varlist.

  Args:
    fp: [*str] of readable file-pointer-like iterator, yields tab delimited line
    varlist: [str] of row IDs to append to
  """
  for line in fp:
    if line[0] in ('#','\n'): continue
    name,c,row = line.partition('\t')
    varlist.append(name)
    yield row

class FakeFile(object):
  def __init__(self, line_generator):
    self.s = line_generator
  def __iter__(self):
    return self
  def next(self):
    return self.s.next()
  def read(self):
    return "".join([q for q in self.s])
  def readline(self):
    return self.s.next()

def tab_to_npy(tab_fname):
  """Return masked numpy array and in-order variable list from row-labeled .tab matrix.

  Args:
    tab_fname: str of path to .tab plain text matrix of floats; first column is row ID
  Returns:
    (np.MaskedArray, [str]) of float data and list of row IDs in order
  """
  varlist = []
  s = name_iter(open(tab_fname), varlist)
  try:
    M = np.genfromtxt(s, usemask=True, delimiter='\t')
  except TypeError:
    # handle numpy1.5 error regarding missing 'read' and 'readline' functions
    S = FakeFile(s)
    M = np.genfromtxt(S, usemask=True, delimiter='\t')
  return M, varlist
