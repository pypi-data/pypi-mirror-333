#
import numpy as np
import os

from multiprocessing import Pool

import Queue
import multiprocessing

zz=20

q=multiprocessing.Queue()

for i in np.arange(30):
  q.put(i)

def f(x):
    global zz
    try:
      a=q.get() # get one more element
      zz = zz+1
      print x*x , os.getpid() , x, zz, " >> a= ",a
      return x*x
    except Queue.Empty:
      print "queue empty"

if __name__ == '__main__':
    p = Pool(5)

    a=list(p.map(f,np.arange(30) ))
    print ">>>",a
    print "zz=",zz
