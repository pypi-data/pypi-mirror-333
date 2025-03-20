#!/usr/bin/env python
import numpy as np
import os,time
import sys
import argparse,textwrap
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

from unsiotools.simulations.crectify import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():

    # help
    parser = argparse.ArgumentParser(description="Convert eigens vectors to rect file",
                                     formatter_class=argparse.RawTextHelpFormatter)
                                    #formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    hh=textwrap.dedent('''\
       Simulation name
       if not empty, all EV files from ANALYSIS/rectify directory
       will be converted to rect files''')
    parser.add_argument('--simname', help=hh,default=None)
    parser.add_argument('--ev', help='Eigen vector input file',default=None)
    parser.add_argument('--rect',help='Rectify output file', default=None)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    try:
        c=CRectify()
        c.buildRectFile(simname=args.simname,ev_in=args.ev,rect_out=args.rect)
    except Exception as x :
        print (x.message)


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
