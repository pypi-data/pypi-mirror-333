#!/usr/bin/env python

import sys
#from unsiotools.uns_simu import *
#from simulations.ccod import *
import argparse

#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None
    ncores=None
    fastcod=True
    threshold=10000
     # help
    parser = argparse.ArgumentParser(description="Build continuation fro MDF",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):

    pass


# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
