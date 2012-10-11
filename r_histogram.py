#!/usr/bin/python
"""
  python r_histogram.py

This module still outputs histograms with obnoxious "density"
estimates rather than simple count/total probabilities. I don't
know yet how to fix this.
"""
import sys, os
import numpy as np
import random

from rpy2 import robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

r_base = importr('base')
grdevices = importr('grDevices')
stats = importr('stats')
graphics = importr('graphics')


def main(npyfname, outdir, n_samples=1000, xlabel='value', rug=True):
  if rug.lower() in ('', 'f', 'false', 'none'):
    rug = False
    
  M = np.load(npyfname)
  M = M.ravel()
  M = M[~np.isnan(M)]

  # Draw plot
  plot_pdfname = os.path.join(outdir, "%s_hist.png" % os.path.basename(npyfname))
  print "Plotting %s..." % plot_pdfname
  make_hist(M, plot_pdfname, n_samples, rug, xlabel)


def make_hist(M, outname, n_samples=1000, rug=True, xlabel='value', title=""):
  assert len(M.shape) == 1
  assert np.sum(np.isnan(M)) == 0
  ext = outname.rpartition('.')[2].lower()
  assert ext == "pdf", 'only pdf file extension supported'
  
  a=random.sample(xrange(M.shape[0]), n_samples)
  A = np.take(M, a)
  grdevices.pdf(outname)
  graphics.hist(A, prob=True, main=title, xlab=xlabel, col="grey")
  if rug:
    graphics.lines(stats.density(A), col="blue")
    graphics.rug(A, col="black")
  grdevices.dev_off()
  
if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))


