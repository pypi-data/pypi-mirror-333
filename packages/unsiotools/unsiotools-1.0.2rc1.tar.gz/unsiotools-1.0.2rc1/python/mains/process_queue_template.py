#!/usr/bin/env python
import numpy as np
import os,time

from multiprocessing import Process

import Queue
import multiprocessing

# detect #cores 
nprocs=multiprocessing.cpu_count()

zz=20

def myFunc(q):
  global zz 
  stop=False
  while (not stop):
    try:  
      time.sleep(.5)
      x=q.get(True,0.01) # get one more element, True,0.01, allow to have empty queue
      zz= zz+1
      print "%04d"%(x*x) , os.getpid() , x, zz
    except Queue.Empty:
      print "queue empty"
      stop=True

if __name__ == '__main__':

  # create a Queue variable to store jobs todo
  q=multiprocessing.Queue()

  # fill queue with jobs to do
  for i in np.arange(30):
    q.put(i)

  # list to store processes which will be created
  processes=[]

  # loop to create parallel processes in respect to #cores requested
  for i in range(nprocs):
    p = Process(target=myFunc, args=(q,))  # create process
    print "start process #",i
    p.start()  # start process in parallel
    processes.append(p) # append list of process, used for joining 


  # wait all processes to complete
  try:
    for p in processes:
     print ("waiting.. ",p)
     p.join()
  except KeyboardInterrupt: # allow to interupt all workers with  CTRL+C
    for p in processes:
      print ("Terminating.. ",p)
      p.terminate()
      p.join()

  while not q.empty():
    q.get(block=False)
