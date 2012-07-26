#!/usr/bin/python
"""Output masked array to tab-delimited text."""
  
def yield_m_to_txt(M):
  for row in M:
    yield row_to_txt(row) + "\n"
    
def row_to_txt(row):
  s = []
  for i in range(len(row)):
    if row.mask[i]:
      s.append("")
    else:
      s.append("%.6f"%row[i])
  return "\t".join(s)
