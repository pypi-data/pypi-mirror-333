#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import os,time
import sys
import argparse,textwrap

#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

import unsiotools.simulations.corbits as orbs

#from IPython import embed

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():

    # help
    parser = argparse.ArgumentParser(description="Compute different quantities on orbits",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('snapshot', help="uns input snapshot",default=None)
    parser.add_argument('component', help="selected component",default=None)
    parser.add_argument('codfile', help="cod file for the component",default=None)
    parser.add_argument('--outfile', help="output file name",default=None)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)

    # parse
    args = parser.parse_args()
    # start main function
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        ff = args.snapshot.split("/")[-1]
        print(ff)
        orbits=orbs.COrbits()
        orbits.computeDistance(snapshot=args.snapshot,component=args.component,
                               outfile=args.outfile,codfile=args.codfile)
    except Exception as x :
        print (x.message,file=sys.stderr)
    except KeyboardInterrupt:
        sys.exit()

# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
