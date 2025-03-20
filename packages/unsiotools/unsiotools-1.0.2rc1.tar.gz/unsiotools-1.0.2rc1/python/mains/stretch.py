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
    ages   = None
    hsml   = None
    rho    = None
    metal  = None
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    comp="all"
    parser = argparse.ArgumentParser(description="Stretch uns snapshot along Z axis ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', help='UNS input file with stars particle')
    parser.add_argument('output', help="NEMO output file ")
    parser.add_argument('stretch', help="stretch value",type=int)
    parser.add_argument('--comp', help='component selected',default=comp)
        
    #parser.add_argument('time', help="time of reference to keep stars particles")
                        
    args = parser.parse_args()

    process(args.input,args.output,args.stretch,args.comp)



# -----------------------------------------------------
# stretchAxis 
def stretchAxis(snap,stretch):


    snap.pos=np.reshape(snap.pos,(-1,3)) # pos reshaped in a 2D array [nbody,3]

    # compute random value on axis
    #raxis=abs(np.modf(np.sin(snap.pos[:,0]*12.9898+snap.pos[:,1]*78.233)*43758.5453)[0])
    #raxis=abs(np.modf(np.sin(snap.pos[:,0]*12.9898+snap.pos[:,2]*78.233)*43758.5453)[0])
    a = 12.9898;
    b = 78.233;
    c = 43758.5453;
    #dt= snap.pos[:,0]*12.9898+snap.pos[:,2]*78.233
    dt= snap.rho*12.9898+snap.rho*78.233
    sn= np.mod(dt,3.14);
    raxis=np.modf(np.sin(sn)*c)[0]
    #raxis= np.random.random(snap.pos.size/3)
    neg=(raxis<0.0)

    print ("neg=",raxis[neg==True])
    #raxis=1
    print ("raxis=",raxis)
    #x = snap.pos[:,0]
    #y = snap.pos[:,1]
    #raxis=np.sin(x*12.9898+y*78.233)*43758.5453
    #snap.pos[:,2] = snap.pos[:,2] + (snap.pos[:,2]*stretch-snap.pos[:,2]) * raxis     
    snap.pos[:,2] = snap.pos[:,2]*stretch + stretch * raxis     

    print ("z=",snap.pos[:,2])
    # rescale pos
    snap.pos = np.reshape(snap.pos,snap.pos.size) # flatten the array (mandatory for unsio)
    
    
# -----------------------------------------------------
# compute, is the core function
def process(simname,out,stretch,comp): #,times):
    verbose=False

    #timef=float(times)
    
    # Create a UNSIO object
    uns = CunsIn(simname,comp,"all",verbose)
#    bits="I"         # select properties, particles Identities only here

    # get file name
#    sim_name=uns.getFileName()

    print ("simname=",simname, " out=",out,file=sys.stderr)
    
    # load frame
    ok=uns.nextFrame("")
    #print ok

    if (ok) :
        if ( ok ) :
            #embed()
            ok,snap.time = uns.getValueF("time")
            ok,snap.pos  = uns.getArrayF(comp,"pos")
            ok,snap.vel  = uns.getArrayF(comp,"vel")
            ok,snap.mass = uns.getArrayF(comp,"mass")
            ok,snap.rho  = uns.getArrayF(comp,"rho")
            ok,snap.hsml = uns.getArrayF(comp,"hsml")

            # select ages according to dt
            stretchAxis(snap,stretch)
            
            # instantiate output object
            unso=CunsOut(out,"nemo");    # output file

            # save data
            unso.setValueF("time",snap.time)       # save time
            unso.setArrayF("all","pos",snap.pos)   # save pos
            #unso.setArrayF("all","vel",snap.vel)   # save vel
            #unso.setArrayF("all","mass",snap.mass) # save mass
            unso.setArrayF("all","rho",snap.rho)  # save ages to rho
            unso.setArrayF("all","hsml",snap.hsml) # save hsml

            unso.save()
            
        else:
            print ("there are no age for stars in this snapshot !!!",file=sys.stderr)
        
        
    else :
        print ("Didn't load anything....",file=sys.stderr)


# -----------------------------------------------------
# main program
commandLine()   # parse command line
