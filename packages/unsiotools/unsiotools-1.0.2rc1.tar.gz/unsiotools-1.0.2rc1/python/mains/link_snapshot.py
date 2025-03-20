#!/usr/bin/env python
from __future__ import print_function
import sys
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path
#from simulations.cmovie import * 
import argparse
import os,glob


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None

    # help
    parser = argparse.ArgumentParser(description="Link snapshot with one unit incremental",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options

    parser.add_argument('snapshot', help='snapshot path, ie : runs/snapshot')


    parser.add_argument('--verbose',help='verbose mode on', dest="verbose", action="store_true", default=False)

    # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    snap_list =     sorted(glob.glob(args.snapshot+'_?'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_??'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_???'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_????'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_?????'))

    cpt=0
    for mysnap in snap_list:
        mylink="snapshot_"+str(cpt)
        if not os.path.islink(mylink):
            print(mysnap,"snapshot_"+str(cpt))
            os.symlink(mysnap,mylink)
        cpt=cpt+1

# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
