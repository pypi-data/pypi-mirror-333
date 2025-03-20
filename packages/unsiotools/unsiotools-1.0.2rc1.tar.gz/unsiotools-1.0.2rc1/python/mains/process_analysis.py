#!/usr/bin/env python
from __future__ import print_function
import os,time
import sys
from multiprocessing import Process
import Queue
import multiprocessing
import numpy as np
import argparse
import matplotlib
matplotlib.use('Agg')
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

from simulations.cuns_analysis import *

#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    dbname=None
    ncores=None

     # help
    parser = argparse.ArgumentParser(description="Parallel pipeline analysis program",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('script', help='Analysis script')
    parser.add_argument('--ncores', help='Use ncores, None means all',default=ncores,type=int)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

    print ("Matplotlib backend Using:",matplotlib.get_backend(),file=sys.stderr)
    
     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        analysis=CUnsAnalysis(simname=args.simname, script=args.script,verbose_debug=args.verbose)
    except Exception as x :
        print (x.message)
    else:
        analysis.compute(args.ncores)
  
  
# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()



