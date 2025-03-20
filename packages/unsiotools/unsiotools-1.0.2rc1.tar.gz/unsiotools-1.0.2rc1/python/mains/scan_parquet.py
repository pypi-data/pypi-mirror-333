#!/usr/bin/env python
import parquet
import json
from math import *

#
# cf https://github.com/jcrobak/parquet-python
#
cpt=0
with open("/home/jcl/N1.parquet") as fo:
   for row in parquet.reader(fo, columns=['alpha', 'delta','distance']):
      cpt=cpt+1
      #print(",".join([str(r) for r in row]))
      #if row[3] > 0:
      x=row[2]*sin(row[1])*cos(row[0])
      y=row[2]*sin(row[1])*sin(row[0])
      z=row[2]*cos(row[1])
        #print x,y,z,row[3]

print cpt
