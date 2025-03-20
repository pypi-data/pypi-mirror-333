#!/usr/bin/env python
# 


# 
# save stars particles to density field for displaying with glnemo2

from __future__ import print_function
# MANDATORY
from unsio import *            # import unsio package (UNSIO)
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse
import sys
#from IPython import embed


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():

    parser = argparse.ArgumentParser(description="Save stars particles born before/after a specific time")
    parser.add_argument('input', help='UNS input file')
    parser.add_argument('output', help="NEMO output file ")
    parser.add_argument('select', help="select component ")
    #parser.add_argument('time', help="time of reference to keep stars particles")
                        

    args = parser.parse_args()

    compute(args.input,args.output,args.select)#,args.time)


# -----------------------------------------------------
# compute, is the core function
def compute(simname,out,comp): #,times):
    components=comp
    verbose=False

    #timef=float(times)
        
    # Create a UNSIO object
    uns = CunsIn(simname,components,"all",verbose)
#    bits="I"         # select properties, particles Identities only here

    # get file name
#    sim_name=uns.getFileName()

    print ("simname=",simname, " out=",out,file=sys.stderr) #," times=",times
    
    # load frame
    ok=uns.nextFrame("")
    #print ok

    if (ok) :
        if ( ok ) :
            ok,timec= uns.getValueF("time")
            ok,pos  = uns.getArrayF("all","pos")
            ok,vel  = uns.getArrayF("all","vel")
            if (ok) :
                vel=np.reshape(vel,(-1,3))        # pos reshaped in a 2D array [nbody,3]
                #embed()
                velnorm=np.sum(vel**2,axis=-1)**(1./2)
                vel=np.reshape(vel,pos.size)
            ok,mass = uns.getArrayF("all","mass")

            hsml=np.zeros(pos.size/3,dtype='float32')
            hsml += 1.0
            #print "HSML :", hsml.size , hsml, hsml.dtype
            
            # instantiate output object
            unso=CunsOut(out,"nemo");    # output file

            # save data
            unso.setValueF("time",timec)      # save time
            unso.setArrayF("all","pos",pos)   # save pos
            unso.setArrayF("all","vel",vel)   # save vel
            #unso.setArrayF("all","mass",mass) # save mass
            unso.setArrayF("all","rho",velnorm)  # save ages to rho
            unso.setArrayF("all","hsml",hsml) # save hsml

            unso.save()
            #embed()
        else:
            print ("there are no age for stars in this snapshot !!!")
        
        
    else :
        print ("Didn't load anything....")


# -----------------------------------------------------
# main program
commandLine()   # parse command line
