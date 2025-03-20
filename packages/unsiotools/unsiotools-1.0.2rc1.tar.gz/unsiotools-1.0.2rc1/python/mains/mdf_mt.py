#!/usr/bin/env python

from __future__ import print_function
import sys
import numpy as np
import argparse
#from IPython import embed

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    infile="/rudata/mdf/ganalysis/merging_times/mdf_merging_times.txt"

    # help
    parser = argparse.ArgumentParser(description="Return merging time of an mdf simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='MDF simulation name')
    parser.add_argument('--infile', help='input file with merging time', default=infile)
    
    # parse
    args = parser.parse_args()
    
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    data=np.genfromtxt(args.infile,dtype=None,names=['strvar','fltvar','fltvar','fltvar'])
    found=False
    for i in data:
        if (i[0] == args.simname):
            found=True
            s=""
            for j in i:
                s = s+" "+str(j)
            print (s)

    if ( not found ):
        print ("none", 0., 0., 0.)
    #embed()


# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
