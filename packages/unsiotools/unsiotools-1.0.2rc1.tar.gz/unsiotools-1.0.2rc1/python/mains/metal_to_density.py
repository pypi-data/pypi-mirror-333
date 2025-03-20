#!/usr/bin/env python
# 


# 
# save stars particles to density field for displaying with glnemo2

# MANDATORY
from unsio import *            # import unsio package (UNSIO)
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():

    f_hsml=0.0001
    parser = argparse.ArgumentParser(description="Save stars/gas metalicity into density field of a NEMO snapshot",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', help='UNS input file with stars or gas particles')
    parser.add_argument('output', help="NEMO output file ")
    parser.add_argument('component', help='stars|gas component')
    parser.add_argument('--hsml', help='hsml value',type=float,default=f_hsml)

    args = parser.parse_args()

    compute(args.input,args.component,args.output, args.hsml)


# -----------------------------------------------------
# compute, is the core function
def compute(simname,component,out,f_hsml):

    verbose=False

    # Create a UNSIO object
    uns = CunsIn(simname,component,"all",verbose)
#    bits="I"         # select properties, particles Identities only here

    # get file name
#    sim_name=uns.getFileName()

    print "simname=",simname, " out=",out
    
    # load frame
    ok=uns.nextFrame("")
    print ok

    if (ok) :
        ok,metal = uns.getArrayF(component,"metal")
        if ( ok ) :
            print "ok ",ok, metal
            print "min=", metal.min()," max=",metal.max()
            mask=(metal>0.0)
            metal=metal[mask]
            
            ok,timec= uns.getValueF("time")
            ok,pos  = uns.getArrayF(component,"pos")
            if ok:
                pos=np.reshape(pos,(-1,3))  # reshaped in a 2D array [nbody,3]
                pos=np.reshape(pos[mask],pos[mask].size) # mask and reshape to 1d array,
            ok,vel  = uns.getArrayF(component,"vel")
            if ok:
                vel=np.reshape(vel,(-1,3))  # reshaped in a 2D array [nbody,3]
                vel=np.reshape(vel[mask],vel[mask].size) # mask and reshape to 1d array,
                
            ok,mass = uns.getArrayF(component,"mass")
            if ok:
                mass=mass[mask]

            hsml=np.zeros(metal.size,dtype='float32')
            hsml += f_hsml
            print "HSML :", hsml.size , hsml, hsml.dtype
            
            # instantiate output object
            unso=CunsOut(out,"nemo");    # output file

            # save data
            unso.setValueF("time",timec)      # save time
            unso.setArrayF("all","pos",pos)   # save pos
            unso.setArrayF("all","vel",vel)   # save vel
            unso.setArrayF("all","mass",mass) # save mass
            unso.setArrayF("all","rho",metal)  # save metal to rho
            unso.setArrayF("all","hsml",hsml) # save hsml

            unso.save()
            
        else:
            print "there are no age for component[",component,"] in this snapshot !!!"
        
        
    else :
        print "Didn't load anything...."


# -----------------------------------------------------
# main program
commandLine()   # parse command line
