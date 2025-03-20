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
    array   = None
    hsml   = None
    rho    = None
    metal  = None
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    f_hsml=0.1
    parser = argparse.ArgumentParser(description="Save selected array into gas density field",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', help='UNS input file with array particle')
    parser.add_argument('output', help="gadget2 output file ")
    parser.add_argument('comp', help="component to select")
    parser.add_argument('array', help="array to select")
    parser.add_argument('--hsml', help='hsml value',type=float,default=f_hsml)
        
    #parser.add_argument('time', help="time of reference to keep stars particles")
                        

    args = parser.parse_args()

    process(args.input,args.output,args.comp,args.array,args.hsml)



# -----------------------------------------------------
# selectarray
def selectarray(snap,f_hsml):

    #select=(snap.array>=(snap.time-snap.time*dt/100.))   # select particles in the ramge of array
    select=(snap.array>-1000000)   # select particles in the ramge of array

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

    # rescale array
    snap.array = snap.array[select]
    
    # hsml
    snap.hsml=np.zeros(snap.array.size,dtype='float32')
    snap.hsml += f_hsml
    
    
# -----------------------------------------------------
# Compute, is the core function
def process(simname,out,components,array_tag,f_hsml):
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
        ok,snap.array = uns.getArrayF(components,array_tag)
        if ( ok ) :
            #print "ok ",ok, snap.array
            print ("min=", snap.array.min()," max=",snap.array.max(),file=sys.stderr)
            #embed()
            ok,snap.time = uns.getValueF("time")
            ok,snap.pos  = uns.getArrayF(components,"pos")
            ok,snap.vel  = uns.getArrayF(components,"vel")
            ok,snap.mass = uns.getArrayF(components,"mass")

            # select array 
            #selectarray(snap,f_hsml)
            # hsml
            snap.hsml=np.zeros(snap.array.size,dtype='float32')
            snap.hsml += f_hsml
            
            # instantiate output object
            unso=CunsOut(out,"gadget2",verbose);    # output file

            # save data
            unso.setValueF("time",snap.time)       # save time
            unso.setArrayF("gas","pos",snap.pos)   # save pos
            #unso.setArrayF("all","vel",snap.vel)   # save vel
            unso.setArrayF("gas","mass",snap.mass) # save mass
            unso.setArrayF("gas","rho",snap.array)  # save array to rho
            unso.setArrayF("gas","hsml",snap.hsml) # save hsml

            unso.save()
            
        else:
            print ("there are no array %s in this snapshot !!!"%(array_tag),file=sys.stderr)
        
        
    else :
        print ("Didn't load anything....",file=sys.stderr)


# -----------------------------------------------------
# main program
commandLine()   # parse command line
