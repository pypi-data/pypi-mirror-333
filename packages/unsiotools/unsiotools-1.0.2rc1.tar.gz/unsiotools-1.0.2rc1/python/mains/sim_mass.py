#!/usr/bin/env python

from __future__ import print_function
import sys
from unsio import *            # import unsio package (UNSIO)
import argparse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    time="0.0"
    verbose=False
    
     # help
    parser = argparse.ArgumentParser(description="Return mass of a component from uns simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('component', help='Simulation component')
    parser.add_argument('--time',help='simulation time', default=time)
    parser.add_argument('--verbose',help='verbosity', default=verbose)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args.simname,args.component,args.time,args.verbose)


# -----------------------------------------------------
# process, is the core function
def process(simname,component,time,verbose):
    #print (simname, " " , time,file=sys.stderr)
    # Create a UNSIO object
    uns = CunsIn(simname,component,time,verbose)
    find=False
    bits="m"
    while (uns.nextFrame(bits)):  # loop while there is something to read
        ok,timex = uns.getValueF("time")
        ok,nbody = uns.getValueI("nsel")
        ok,mass  = uns.getArrayF(component,"mass")
        if ok:
            find=True
            print ( simname, component, timex, nbody,mass[0], nbody*mass[0])
            break;

    if not find:
         print ("none")
    
# -----------------------------------------------------
# main program
commandLine()   # parse command line
