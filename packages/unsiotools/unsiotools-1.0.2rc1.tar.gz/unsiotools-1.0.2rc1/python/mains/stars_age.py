#!/usr/bin/env python
# 


# 
# save stars particles born before/after a specific time

# MANDATORY
from unsio import *            # import unsio package (UNSIO)
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():

    parser = argparse.ArgumentParser(description="Save stars particles born before/after a specific time")
    parser.add_argument('input', help='UNS input file with stars particle')
    parser.add_argument('output', help="NEMO output file ")
    parser.add_argument('time', help="time of reference to keep stars particles")
    parser.add_argument('before',help="if true, save before time, otherwise after",type=int)
                        

    args = parser.parse_args()

    compute(args.input,args.output,args.time,args.before)


# -----------------------------------------------------
# compute, is the core function
def compute(simname,out,times,before):
    components="stars" 
    verbose=False

    timef=float(times)
    
    # Create a UNSIO object
    uns = CunsIn(simname,components,"all",verbose)
#    bits="I"         # select properties, particles Identities only here

    # get file name
#    sim_name=uns.getFileName()

    print "simname=",simname, " out=",out," times=",times," before=",before
    
    # load frame
    ok=uns.nextFrame("")
    print ok

    if (ok) :
        ok,ages = uns.getArrayF("stars","age")
        if ( ok ) :
            print "ok ",ok, ages
            print "min=", ages.min()," max=",ages.max()

            ok,timec= uns.getValueF("time")
            ok,pos  = uns.getArrayF("stars","pos")
            print  "in:",pos.size, pos.shape
            pos=np.reshape(pos,(-1,3))        # pos reshaped in a 2D array [nbody,3]
            ok,vel  = uns.getArrayF("stars","vel")
            vel=np.reshape(vel,(-1,3))        # vel reshaped in a 2D array [nbody,3]
            ok,mass = uns.getArrayF("stars","mass")

            mask_age = ()

            if (before==1) :
                mask_age=(ages<=timef)
            else :
                mask_age=(ages>timef)
            print "mask age ", mask_age, mask_age[mask_age==True].size

            # instantiate output object
            unso=CunsOut(out,"nemo");    # output file

            # mask particles according to selected ages
            
            # reshape in 1D array
            pos = np.reshape(pos[mask_age],pos[mask_age].size)
            print  "out:",pos.size, pos.shape
            vel = np.reshape(vel[mask_age],vel[mask_age].size)

            mass = mass[mask_age]

            # save data
            unso.setValueF("time",timec)      # save time
            unso.setArrayF("all","pos",pos)   # save pos
            unso.setArrayF("all","vel",vel)   # save vel
            unso.setArrayF("all","mass",mass) # save mass

            unso.save()
            
        else:
            print "there are no age for stars in this snapshot !!!"
        
        
    else :
        print "Didn't load anything...."


# -----------------------------------------------------
# main program
commandLine()   # parse command line
