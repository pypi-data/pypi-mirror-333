#!/usr/bin/env python
from __future__ import print_function

import sys
sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

#from py_unstools import *         # import py_unstools package
#from unsio import *
#from uns_simu import *

import argparse
import os


from simulations.ctestunsio import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():

     # help
    parser = argparse.ArgumentParser(description="Test UNSIO library",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('--nbody', help='#bodies to test', type=int, default=100000)
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)
    parser.add_argument('--double',help='test with double real',dest="double", action="store_true", default=False)
    parser.add_argument('--uns2uns',help='save intermediate file with uns2uns',dest="uns2uns", action="store_true", default=False)
     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def process(args):
    uns=CTestunsio(nbody=args.nbody,single=not args.double, uns2uns=args.uns2uns)
    #uns.saveModel("")
    uns.testIO()


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()


