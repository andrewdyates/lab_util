#!/usr/bin/python
"""Output masked array to tab-delimited text."""
  
def yield_m_to_txt(M, fmt):
  for row in M:
    yield row_to_txt(row, fmt) + "\n"
    
def row_to_txt(row, fmt='%.6f'):
  s = []
  for i in range(len(row)):
    if row.mask[i]:
      s.append("")
    else:
      s.append(fmt%row[i])
  return "\t".join(s)

def masked_npy_to_tab(*args, **kwds):
  """Alias for npy_to_tab"""
  npy_to_tab(*args, **kwds)

def npy_to_tab(M, fp, varlist=None, fmt='%.6f'):
  """Write masked numpy matrix to tab delimited text.

  Args:
    M: np.MaskedArray of floats
    fp: [str*] writable for output
    varlist: [str] of variable names; do not write if not provided
    fmt: format string for numeric entries
  """
  for i, row in enumerate(yield_m_to_txt(M, fmt)):
    if varlist is not None:
      fp.write("%s\t" % varlist[i])
    fp.write(row)
