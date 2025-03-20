#!/usr/bin/python

# coding: utf-8

## Example of howto get gravity using falcon library directly from Python 

# In[1]:

from py_unstools import *         # import py_unstools package
from py_unsio import *            # import py_unsio package
import numpy as np                # arrays are treated as numpy arrays
import time

t0=time.time()

simname="mdf001%1500" 
components="stars" 
times="all" 
verbose=False
uns = CunsIn(simname,components,times,verbose)
bits=""         # select properties, "" means all
ok=uns.nextFrame(bits)   # load data from disk

# Instantiate falcon object
falcon=cfalcon()

# Load positions and masses
comp="stars" 

ok,pos = uns.getArrayF(comp,"pos")
ok,mass = uns.getArrayF(comp,"mass")

print "Nbody = ",pos.size/3

# softening
eps=0.05

# get_gravity has following parameters
# falcon.get_gravity(numpy pos, numpy mass, float eps, float G=1. float theta=0.6, int kernel_type=1, int ncrit=6)

# init returns array
acc = np.zeros(pos.size,'f')   # acc is 3D !!
phi = np.zeros(mass.size,'f')
# compute gravity
ok=falcon.compute_gravity(pos,mass,acc,phi,0.05)

# print
print ok,acc,phi

# init returns arrays
rho=np.zeros(mass.size,'f')
hsml=np.zeros(mass.size,'f')
# compute density
ok=falcon.compute_density(pos,mass,rho,hsml)
print ok,rho,hsml

print time.time() - t0, "seconds cpu time"
