#!/usr/bin/env python
from __future__ import print_function

import sys
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

#from py_unstools import *         # import py_unstools package
from unsio import *

import argparse
import os,subprocess

from unsiotools.simulations.creducesim import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None

     # help
    parser = argparse.ArgumentParser(description="Remove halo from a simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='UNS Simulation name')
    parser.add_argument('--dir', help='directory to store new files',default=None)
    parser.add_argument('--keep', help='keep halo every frequency',default=10,type=int)
    parser.add_argument('--overwrite',help='overwrite new frame if present', dest="overwrite", action="store_true", default=False)
    parser.add_argument('--test',help='test without doing anything', dest="test",action="store_true", default=False)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)
     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        simu=CReducesim(simname=args.simname,keep=args.keep,overwrite=args.overwrite,dir=args.dir,test=args.test,verbose=args.verbose)
    except Exception as x :
        print (x.message)
    else:
        simu.resizeSim()

# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
