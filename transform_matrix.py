#!/usr/bin/python
import random
import sys
import numpy as np
import cPickle as pickle

def permute_rows(M):
  """Randomly permute values in rows of M. Preserve masks."""
  random.seed()
  for i in xrange(np.size(M,0)):
    random.shuffle(M[i,:])

def rank_rows(M):
  """Rank order rows of M. Preserve masks."""
  random.seed()
  for i in xrange(np.size(M,0)):
    try:
      mask = M.mask
    except AttributeError:
      M[i,:] = M[i,:].argsort().argsort()
    else:
      n_values = np.sum(M[i,:].mask)
      M[i,:].data = M[i,:].argsort().argsort()
      # Mask any rank over the total number of values
      M[i,:].mask = (M[i,:].data >= n_values)


def main(f="permute", fname=None, tag=""):
  print "Loading %s..." % (fname)
  M = pickle.load(fname)
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

if __name__ == "__main__":
  print sys.argv
  main(**dict([s.split('=') for s in sys.argv[1:]]))
