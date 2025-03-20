#!/usr/bin/python

# coding: utf-8

## Example of howto get gravity using falcon library directly from Python 

# In[1]:

#from py_unstools import *         # import py_unstools package
from py_unsio import *            # import py_unsio package
import numpy as np                # arrays are treated as numpy arrays
import time
import sys
sys.path.append('/home/jcl/works/GIT/uns_projects/py/modules/')
sys.path.append('/home/jcl/works/GIT/uns_projects/py/modules/simulations')
from uns_simu import *
from cfalcon import *

t0=time.time()

simname="mdf001%1500" 
components="stars" 
times="all" 
verbose=False
uns = CunsIn(simname,components,times,verbose)
bits=""         # select properties, "" means all
ok=uns.nextFrame(bits)   # load data from disk

# Instantiate falcon object
falcon=CFalcon()

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
#acc = np.zeros(pos.size,'f')   # acc is 3D !!
#phi = np.zeros(mass.size,'f')
# compute gravity
#ok=falcon.compute_gravity(pos,mass,acc,phi,0.05)

ok,acc,phi=falcon.getGravity(pos,mass,eps)
t1=time.time()
print ok,acc,phi

# get density
ok,rho,hsml=falcon.getDensity(pos,mass)
t2=time.time()
print ok,rho,hsml

print time.time() - t0, "Whole seconds cpu time"
print t1 - t0, "Gravity : seconds cpu time"
print t2 - t1, "Density : seconds cpu time"

