#!/usr/bin/python
"""Convert a .mat matrix and variable list into a .tab file.

Assumes that target matrix in .mat file is named 'M' (or `matrix_name`)

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
  # consume headers
  varlist = []
  for line in open(tab_fname):
    if line[0] in ('#', '\n'): continue
    varlist.append(s.partition('\t')[0])
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
