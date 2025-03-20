#!/usr/bin/env python
from __future__ import print_function

import sys
import numpy as np
from unsio import *
import argparse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
# commandLine, parse the command line 
def commandLine():
    format="gadget2"
    select="gas,stars"
     # help
    parser = argparse.ArgumentParser(description="Convert output data from code (Semelin & Combes 2000) to uns format (gadget2/gadget3/nemo)."
                                     " This program is based on UNSIO API, please visit https://projets.lam.fr/projects/unsio/wiki/Wiki ",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('snap_in', help='input file')
    parser.add_argument('snap_out',help='output file')
    parser.add_argument('--select',help='selected components (stars,gas,dm or all)',default=select)
    parser.add_argument('--format',help='output format (gadget2,gadegt3,nemo)', default=format)

     # parse
    args = parser.parse_args()

    if (args.format != "nemo" and args.select=="all"):
        args.select="dm,gas,stars"
    # start main funciton
    process(args)

# -----------------------------------------------------
# process
def process(args):
    f=open(args.snap_in)
    line=f.readline() # read components nbodies

    # array of components nbodies (0:all, 1:gas, 2:stars, 3:dm|halo)    
    comp=np.zeros(0)  
    for i in line.split():
        print ("i",i,type(i))
        comp=np.append(comp,int(i))

    # components
    cmp={'all':0,'gas':1,'stars':2,'dm':3,'halo':3}
    comp=np.append(comp,comp[0]-comp[1]-comp[2])

    # create components range
    range={'all':slice(0,comp[0]),
           'gas':slice(0,comp[1]),
           'stars':slice(comp[1],comp[1]+comp[2]),
           'dm':slice(comp[1]+comp[2],comp[1]+comp[2]+comp[3]),
           }
    print ("comp:",comp)
    print ("range:",range)
    for i in cmp:
        print ("comp[",i,"]",comp[cmp[i]])


    line=f.readline() # skip
    line=f.readline() # skip
    line=f.readline() # read time

    time=float(line.split()[0])
    print ("time=",time)
    
    #read all data after header
    data=np.genfromtxt(args.snap_in,dtype=np.float32,skip_header=4,usecols=(1,2,3,4,5,6,7,8))

    pos=np.zeros(0,dtype=np.float32)
    vel=np.zeros(0,dtype=np.float32)
    mass=np.zeros(0,dtype=np.float32)
    pot=np.zeros(0,dtype=np.float32)

    print (pos,pos.size)
    print(vel,vel.size)
    print(mass,mass.size)
    print(pot,pot.size)

    unso=CunsOut(args.snap_out,args.format)    # output file

    unso.setValueF("time",time)       # save time
        
    for s in args.select.split(","):
        if args.format != "nemo":  # reset arrays
            pos=np.zeros(0,dtype=np.float32)
            vel=np.zeros(0,dtype=np.float32)
            mass=np.zeros(0,dtype=np.float32)
            pot=np.zeros(0,dtype=np.float32)
        if comp[cmp[s]]>0:
            print ("process :",s)
            # pos
            tmp=data[range[s],0:3]
            tmp=np.reshape(tmp,tmp.size)
            pos=np.append(pos,tmp)
            # vel
            tmp=data[range[s],3:6]
            tmp=np.reshape(tmp,tmp.size)
            vel=np.append(vel,tmp)
            # mass
            mass=np.append(mass,data[range[s],6])
            # pot
            pot=np.append(pot,data[range[s],7])

            if args.format != "nemo":
                if pos.size :
                    print (range[s],":",pos.size/3)
                    unso.setArrayF(s,"pos",pos)   # save pos
                if vel.size:
                    unso.setArrayF(s,"vel",vel)   # save vel
                if mass.size:
                    unso.setArrayF(s,"mass",mass) # save mass
                if pot.size:
                    unso.setArrayF(s,"pot",pot) # save hsml
    
                
    # formaat "nemo" save all
    if args.format == "nemo":
        if pos.size :
            unso.setArrayF("all","pos",pos)   # save pos
        if vel.size:
            unso.setArrayF("all","vel",vel)   # save vel
        if mass.size:
            unso.setArrayF("all","mass",mass) # save mass
        if pot.size:
            unso.setArrayF("all","pot",pot) # save hsml

    
    # instantiate output object

    # save data
    unso.save()

# -----------------------------------------------------
# main program
# parse command line
if __name__ == '__main__':
    commandLine()
