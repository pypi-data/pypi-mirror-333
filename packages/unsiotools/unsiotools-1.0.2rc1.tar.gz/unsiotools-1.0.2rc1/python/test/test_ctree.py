#!/usr/bin/python

import sys
sys.path.append('/home/jcl/works/GIT/uns_projects/py/modules/')
sys.path.append('/home/jcl/works/GIT/uns_projects/py/modules/simulations')
from uns_simu import *
from ctree import *
from csnapshot import *
import argparse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None
    ncores=None
    threshold=10000
     # help
    parser = argparse.ArgumentParser(description="UNS test COD python",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('inputfile', help='Input file')
    parser.add_argument('outfile', help='output file')
    parser.add_argument('select', help='Selected component')
    parser.add_argument('--threshold', help='number of particles used for cod (<0 percentage)',default=threshold,type=int)
    parser.add_argument('--ncores', help='Use ncores, None means all',default=ncores,type=int)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()
    if args.outfile=="None":
        args.outfile=None
    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    #cod = CCod(inputfile=args.inputfile,verbose_debug=args.verbose,dbname=args.dbname)
    #cod.compute(args.select,args.ncores)
    uns_snap=CSnapshot(args.inputfile,args.select)
    ok=uns_snap.unsin.nextFrame("mxv")

    if ok:
        ok,timex=uns_snap.unsin.getData("time")
        ok,pos=uns_snap.unsin.getData(args.select,"pos")
        #ok,vel=uns_snap.unsin.getData(args.select,"vel")
        ok,mass=uns_snap.unsin.getData(args.select,"mass")

        ctree=CTree(pos,None,mass,time=timex)
        print("Time = ",timex)
        cxv=ctree.fastCod3(args.threshold,outfile=args.outfile)
        print ("TCXV : ",cxv)

# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
