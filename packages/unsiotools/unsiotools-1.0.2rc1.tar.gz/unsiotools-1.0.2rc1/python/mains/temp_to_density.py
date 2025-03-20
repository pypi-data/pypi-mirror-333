#!/usr/bin/env python
# 


# 
# save gas particles temperature to density field for displaying with glnemo2

# MANDATORY
from unsio import *            # import unsio package (UNSIO)
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    f_hsml=0.0001

    parser = argparse.ArgumentParser(description="Save gas particles temperature into density field of a NEMO snapshot ")
    parser.add_argument('input', help='UNS input file with gas particle')
    parser.add_argument('output', help="NEMO output file ")
    parser.add_argument('z', help="cut in z",type=float)
    parser.add_argument('--hsml', help='hsml value',type=float,default=f_hsml)
                 

    args = parser.parse_args()

    compute(args.input,args.output,args.z,args.hsml)


# -----------------------------------------------------
# compute, is the core function
def compute(simname,out,z,f_hsml):
    components="gas" 
    verbose=False

    
    # Create a UNSIO object
    uns = CunsIn(simname,components,"all",verbose)
#    bits="I"         # select properties, particles Identities only here

    # get file name
#    sim_name=uns.getFileName()

    print "simname=",simname, " out=",out," z=",z
    
    # load frame
    ok=uns.nextFrame("")
    print ok

    if (ok) :
        ok,temp = uns.getArrayF("gas","temp")
        if ( ok ) :
            print "ok ",ok, temp
            print "min=", temp.min()," max=",temp.max()

            ok,timec= uns.getValueF("time")
            ok,pos  = uns.getArrayF("gas","pos")
            print  "in:",pos.size, pos.shape
            pos=np.reshape(pos,(-1,3))        # pos reshaped in a 2D array [nbody,3]
            ok,vel  = uns.getArrayF("gas","vel")
            vel=np.reshape(vel,(-1,3))        # vel reshaped in a 2D array [nbody,3]
            ok,mass = uns.getArrayF("gas","mass")

            
            ok,rho=uns.getArrayF("gas","rho")

            idmax=np.argmax(rho)
            x=pos[idmax,0]
            y=pos[idmax,1]
            z=pos[idmax,2]

            pos[:,0] -= x
            pos[:,1] -= y
            pos[:,2] -= z
            
            mask_z = ((pos[:,2] > -z) & (pos[:,2]<z))
            print "mask_z:", mask_z,mask_z.size, mass.size
            
            # instantiate output object
            unso=CunsOut(out,"nemo");    # output file
            
            # reshape in 1D array
            pos = np.reshape(pos[mask_z],pos[mask_z].size)
            print  "out:",pos.size, pos.shape
            vel = np.reshape(vel[mask_z],vel[mask_z].size)
            mass = mass[mask_z]
            temp = temp[mask_z]

            hsml  = np.zeros(temp.size,dtype='float32')
            hsml += f_hsml
            #ok,hsml=uns.getArrayF("gas","hsml")
            #hsml = hsml[mask_z]
            print "HSML :", hsml.size , hsml, hsml.dtype
            
            # save data
            unso.setValueF("time",timec)      # save time
            unso.setArrayF("all","pos",pos)   # save pos
            unso.setArrayF("all","vel",vel)   # save vel
            unso.setArrayF("all","mass",mass) # save mass
            unso.setArrayF("all","rho",temp)  # save temp to rho
            unso.setArrayF("all","hsml",hsml) # save hsml

            unso.save()
            
        else:
            print "there are no temperature for gas in this snapshot !!!"
        
        
    else :
        print "Didn't load anything...."


# -----------------------------------------------------
# main program
commandLine()   # parse command line
