#!/usr/bin/python

import sys
sys.path.append('/home/jcl/works/GIT/uns_projects/py/modules/')
sys.path.append('/home/jcl/works/GIT/uns_projects/py/modules/simulations')
from uns_simu import *
from ccod import * 
import argparse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    dbname=None
    ncores=None
    fastcod=True
    threshold=10000
     # help
    parser = argparse.ArgumentParser(description="UNS test COD python",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('select', help='Selected component')
    parser.add_argument('--fastcod', help='compute density by selecting particles from octree',default=fastcod)
    parser.add_argument('--threshold', help='number of particles used for fastcod (<0 percentage)',default=threshold,type=int)
    parser.add_argument('--ncores', help='Use ncores, None means all',default=ncores,type=int)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    cod = CCod(simname=args.simname,verbose_debug=args.verbose,dbname=args.dbname)
    cod.compute(select=args.select,ncores=args.ncores,fastcod=args.fastcod,threshold=args.threshold)
    

# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
