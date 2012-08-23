#!/usr/bin/python
import os, errno
# this is used frequently enough to be imported into __init__; leave as module for back compatibility
from tab_to_npy import *

def make_dir(outdir):
  try:
    os.makedirs(outdir)
  except OSError, e:
    if e.errno != errno.EEXIST: raise
  return outdir
