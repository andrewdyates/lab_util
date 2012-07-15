#!/usr/bin/python
"""Convert a .mat matrix and variable list into a .tab file.

EXAMPLE USE:

python matlab_to_tab.py matlab_fname=/Users/qq/Dropbox/biostat/study_data/GSE15745/GSE15745.GPL6104.normed.mat  tab_fname=/Users/qq/Dropbox/biostat/study_data/GSE15745/GSE15745.GPL6104.mRNA.raw.tab > /Users/qq/Dropbox/biostat/study_data/GSE15745/GSE15745.GPL6104.mRNA.normed.tab

UPDATE: replaces 'nan' with empty string
"""
import sys
import scipy.io as sio
import numpy as np

def main(matlab_fname=None, tab_fname=None, matrix_name="M"):

  assert matlab_fname and tab_fname and matrix_name

  M = sio.loadmat(matlab_fname)[matrix_name]
  fp = open(tab_fname)
  # consume headers
  varlist = []
  for s in fp:
    if s[0] != '#':
      varlist.append(s.split('\t')[0])
      break
  varlist = varlist + [s.split('\t')[0] for s in fp]
  fp.close()
  assert varlist[-1]
  assert len(varlist) == np.size(M,0)

  for i, row in enumerate(M):
    print varlist[i] + '\t' + '\t'.join([to_str(v) for v in row])

def to_str(x):
  """Don't return nan. Return empty string."""
  s = "%f"%x
  if s == "nan":
    return ""
  else:
    return s

if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
