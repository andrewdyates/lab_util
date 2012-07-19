#!/usr/bin/python
"""
  python r_histogram.py 
"""
import sys, os
import numpy as np

from rpy2 import robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

r_base = importr('base')
grdevices = importr('grDevices')
stats = importr('stats')
graphics = importr('graphics')


def main(npyfname, outdir):
  M = np.load(npyfname)

  # Draw plot
  plot_pdfname = os.path.join(outdir, "%s_hist.png" % os.path.basename(npyfname))
  print "Plotting %s..." % plot_pdfname
  grdevices.png(plot_pdfname)
  graphics.hist(M, prob=True, main=os.path.basename(npyfname), xlab="score", col="grey")
#  graphics.lines(stats.density(M), col="blue")
#  graphics.rug(M, col="black")
  grdevices.dev_off()

if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
