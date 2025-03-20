#!/usr/bin/env python

from __future__ import print_function
import sys
import numpy as np
import argparse
#from IPython import embed

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    

    # help
    parser = argparse.ArgumentParser(description="create rectify jobs",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='UNS simulation')
        
    # parse
    args = parser.parse_args()
    
    print ("uns_rectify.pl --simname %s --select=stars --codcomp=halo,disk,stars --rho=f --times=2:10"%(args.simname))
    print ("uns_rectify.pl --simname %s --select=stars --codcomp=stars --rho=f --times=2:10"%(args.simname))
    print ("uns_rectify.pl --simname %s --select=gas    --codcomp=stars --rho=f --rcut=10.0 --times=2:10"%(args.simname))

# -----------------------------------------------------
# main program
commandLine()   # parse command line
