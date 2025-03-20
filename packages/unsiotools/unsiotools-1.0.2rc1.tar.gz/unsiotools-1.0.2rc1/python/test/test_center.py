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
from csnapshot import *

t0=time.time()

simname="mdf001%50" 
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
ok,vel = uns.getArrayF(comp,"vel")
ok,mass = uns.getArrayF(comp,"mass")

print "Nbody = ",pos.size/3

# softening
eps=0.05

# get density
ok,rho,hsml=falcon.getDensity(pos,mass,eps)
t2=time.time()
print ok,rho,hsml

snap = CSnapshot()

print "POS =", pos 
com = snap.center(pos,vel,rho*mass,center=False)

print "POS =", pos
print "VEL =", vel


print "Coordinates center :", com

