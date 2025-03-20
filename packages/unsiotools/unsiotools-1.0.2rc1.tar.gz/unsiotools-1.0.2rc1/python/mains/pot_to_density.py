#!/usr/bin/env python
# 

from __future__ import print_function
# 
# save stars particles to density field for displaying with glnemo2

# MANDATORY
from unsio import *            # import unsio package (UNSIO)
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse

import sys

#from IPython import embed

class snap:
    time   = None
    nbody  = None
    mass   = None
    pos    = None
    vel    = None
    ids    = None
    pot   = None
    hsml   = None
    rho    = None
    metal  = None
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    dt=3
    f_hsml=0.1
    parser = argparse.ArgumentParser(description="Save pot into density field of a NEMO snapshot ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', help='UNS input file with pot particle')
    parser.add_argument('output', help="NEMO output file ")
    parser.add_argument('comp', help="component to select")
    parser.add_argument('--dt', help="save particles:[age > time-time*dt%%],(time=current time)",default=dt,type=float)
    parser.add_argument('--hsml', help='hsml value',type=float,default=f_hsml)
        
    #parser.add_argument('time', help="time of reference to keep stars particles")
                        

    args = parser.parse_args()

    process(args.input,args.output,args.comp,args.dt,args.hsml)



# -----------------------------------------------------
# selectpot
def selectpot(snap,dt,f_hsml):

    #select=(snap.pot>=(snap.time-snap.time*dt/100.))   # select particles in the ramge of pot
    select=(snap.pot>-1000000)   # select particles in the ramge of pot

    snap.pos=np.reshape(snap.pos,(-1,3)) # pos reshaped in a 2D array [nbody,3]

    # rescale pos
    snap.pos = snap.pos[select]
    snap.pos = np.reshape(snap.pos,snap.pos.size) # flatten the array (mandatory for unsio)
    
    # rescale vel
    if snap.vel.size > 0:
      print ("yo")
      snap.vel=np.reshape(snap.vel,(-1,3)) # pos reshaped in a 2D array [nbody,3]
      snap.vel = snap.vel[select]
      snap.vel = np.reshape(snap.vel,snap.vel.size) # flatten the array (mandatory for unsio)

    #rescale mass
    snap.mass = snap.mass[select]

    # rescale pot
    snap.pot = snap.pot[select]
    
    # hsml
    snap.hsml=np.zeros(snap.pot.size,dtype='float32')
    snap.hsml += f_hsml
    
# -----------------------------------------------------
# compute, is the core function
def process(simname,out,components,dt,f_hsml):
    verbose=False

    #timef=float(times)
    
    # Create a UNSIO object
    uns = CunsIn(simname,components,"all",verbose)
#    bits="I"         # select properties, particles Identities only here

    # get file name
#    sim_name=uns.getFileName()

    print ("simname=",simname, " out=",out,file=sys.stderr)
    print ("components=",components,file=sys.stderr)
    print ("hsml=",f_hsml,file=sys.stderr)
    
    # load frame
    ok=uns.nextFrame("")
    #print ok

    if (ok) :
        ok,snap.pot = uns.getArrayF(components,"pot")
        if ( ok ) :
            #print "ok ",ok, snap.pot
            print ("min=", snap.pot.min()," max=",snap.pot.max(),file=sys.stderr)
            #embed()
            ok,snap.time = uns.getValueF("time")
            ok,snap.pos  = uns.getArrayF(components,"pos")
            ok,snap.vel  = uns.getArrayF(components,"vel")
            ok,snap.mass = uns.getArrayF(components,"mass")

            # select pot according to dt
            selectpot(snap,dt,f_hsml)
            
            # instantiate output object
            unso=CunsOut(out,"gadget2",True);    # output file

            # save data
            unso.setValueF("time",snap.time)       # save time
            unso.setArrayF("gas","pos",snap.pos)   # save pos
            #unso.setArrayF("all","vel",snap.vel)   # save vel
            unso.setArrayF("gas","mass",snap.mass) # save mass
            unso.setArrayF("gas","rho",snap.pot)  # save pot to rho
            unso.setArrayF("gas","hsml",snap.hsml) # save hsml

            unso.save()
            
        else:
            print ("there are no age for stars in this snapshot !!!",file=sys.stderr)
        
        
    else :
        print ("Didn't load anything....",file=sys.stderr)


# -----------------------------------------------------
# main program
commandLine()   # parse command line
