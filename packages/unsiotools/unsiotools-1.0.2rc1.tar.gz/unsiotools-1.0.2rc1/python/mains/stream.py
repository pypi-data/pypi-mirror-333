#!/usr/bin/env python

from __future__ import print_function
import sys
from unsio.input import *        # import unsio package (UNSIO)
import argparse

import time


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    timex="0.0"
    verbose=False
    
     # help
    parser = argparse.ArgumentParser(description="Return blockname from uns simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('blockname', help='Simulation blockname')
    parser.add_argument('--time',help='simulation time', default=timex)
    parser.add_argument('--verbose',help='verbosity', default=verbose)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args.simname,args.blockname,args.time,args.verbose)


# -----------------------------------------------------
# process, is the core function
def process(simname,blockname,timex,xverbose):
    #print (simname, " " , time,file=sys.stderr)
    # Create a UNSIO object
    uns = CUNS_IN(simname,"all",timex,verbose_debug=xverbose)
    find=False
    bits="x"
    while (uns.nextFrame(bits)):  # loop while there is something to read
        ok,timex = uns.getData("time")
        ok,nbody = uns.getData("nsel")
        t1=time.time()
        ok,data  = uns.getData("STREAM",blockname)
        t2=time.time()
        print ("time = ",t2-t1)
        if ok:
            find=True
            print ( simname, blockname, timex, data.size, data)
            break;
        
        print ( timex)

    if not find:
         print ("none")
    
# -----------------------------------------------------
# main program
commandLine()   # parse command line
