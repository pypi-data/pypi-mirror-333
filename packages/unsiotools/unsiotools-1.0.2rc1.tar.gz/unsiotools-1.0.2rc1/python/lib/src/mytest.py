from py_unsio import *            # import py_unsio package
import numpy as np                # arrays are treated as numpy arrays
from py_unstools import *


simname="/rudata/mdf/mdf001/SNAPS/mdf001_026" 
components="disk,gas,stars" 
times="all" 
verbose=False
uns = CunsIn(simname,components,times,verbose)
bits=""         # select properties, "" means all
ok=uns.nextFrame(bits)   # load data from disk

comp="stars" 

ok,pos = uns.getArrayF(comp,"pos")  # pos is a 1D numpy array, it returns pos for disk component
ok,vel = uns.getArrayF(comp,"vel")  # pos is a 1D numpy array, ipt returns pos for disk component
ok,mass = uns.getArrayF(comp,"mass")  # pos is a 1D numpy array, ipt returns pos for disk component

acc=np.arange(pos.size,dtype=np.float32)
phi=np.arange(mass.size,dtype=np.float32)
