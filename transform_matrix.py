#!/usr/bin/python
import random
import sys
import numpy as np
import cPickle as pickle
from scipy.stats import mstats

def permute_rows(M):
  """Randomly permute values in rows of M. Preserve masks."""
  for i in xrange(np.size(M,0)):
    try:
      M.mask
    except AttributeError:
      random.shuffle(M[i,:])
    else:
      n_masked = np.sum(M[i,:].mask)
      row = M[i,:].compressed()
      assert np.sum(np.isnan(row)) == 0
      row = list(row)
      row.extend([np.nan]*n_masked)
      random.shuffle(row)
      M[i,:] = row
      M[i,:].mask = np.isnan(row)


def rank_rows(M):
  """Rank order rows of M. Preserve masks.

  fill value for M must be the maximum value for that array.
  """
  #scipy.stats.mstats.rankdata
  for i in xrange(np.size(M,0)):
    try:
      mask = M.mask
    except AttributeError:
      M[i,:] = mstats.rankdata(M[i,:]) -1
    else:
      assert np.sum(M == M.fill_value) == 0
      mask = np.copy(M[i,:].mask)
      M[i,:] = mstats.rankdata(M[i,:].data) -1
      M[i,:].mask = mask
      
      
def main(f="permute", fname=None, tag=""):
  random.seed()
  print "Loading %s..." % (fname)
  M = pickle.load(open(fname))
  if f == "permute":
    permute_rows(M)
    outname = "%s.rand%s.pkl" % (fname, tag)
  elif f == "rank":
    rank_rows(M)
    outname = "%s.rank%s.pkl" % (fname, tag)
  else:
    print "Unknown function %s." % f
    sys.exit(1)
  pickle.dump(M, open(outname,'w'))
  print "Saved %s transformed matrix as %s." % (f, outname)


def test():
  Q = np.array([1.5,2,3,4,5,10.5,20,30,30,50]).reshape((2,5))
  print Q
  permute_rows(Q)
  print Q
  permute_rows(Q)
  print Q
  rank_rows(Q)
  print Q
  rank_rows(Q)
  print Q
  print "masked"
  Q = np.ma.MaskedArray(np.array([1.5,2,3,4,5,20,20,30,40,50]).reshape((2,5)), mask=np.array([0,0,1,0,0,0,0,1,1,0]).reshape((2,5)))
  print Q
  permute_rows(Q)
  print Q
  permute_rows(Q)
  print Q
  rank_rows(Q)
  print Q
  rank_rows(Q)
  print Q


  
if __name__ == "__main__":
  print sys.argv
  kwds = dict([s.split('=') for s in sys.argv[1:]])
  if kwds['f'] == "test":
    test()
  else:
    main(**kwds)

  
