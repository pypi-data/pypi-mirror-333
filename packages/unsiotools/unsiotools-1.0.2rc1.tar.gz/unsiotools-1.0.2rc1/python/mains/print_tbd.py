#!/usr/bin/env python
from __future__ import print_function

import sys
import numpy as np
import argparse
from unsiotools.uns_simu import *
import os.path
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():

     # help
    parser = argparse.ArgumentParser(description="Print xxx.npy file belonging to TBD analysis directory",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('npy', help='simulation name OR TBD npy file')
    parser.add_argument('--rect', help='rectify (0 or 1)', default=1, type=int)

    args = parser.parse_args()

    # start main funciton
    process(args)

# -----------------------------------------------------
#
def checkSimu(simname):
    sql3 = UnsSimu()
    #sql3.printInfo(simname)

    r = sql3.getInfo(simname)
    if (r) :
        tbd_dir=r['dir']+'/ANALYSIS/Tbd'
        tbd_f_yes=tbd_dir+'/frac_jj_'+simname+"_rectyes.npy"
        tbd_f_no=tbd_dir+'/frac_jj_'+simname+"_rect.npy"
        return tbd_dir,tbd_f_yes,tbd_f_no
    else:
        print("\nUnknown simulation : [",simname,"]\n")
        return None,None,None

# -----------------------------------------------------
# process, is the core function
def process(args):

    fnpy=args.npy
    if (not os.path.exists(fnpy)):
        dnpy,fnpy_yes,fnpy_no=checkSimu(args.npy)
        if args.rect != 0:
            fnpy=fnpy_yes
        else:
            fnpy=fnpy_no

    try:
        data = np.load(fnpy)
    except:
        print ("\nUnable to load file [%s]\n"%(fnpy))
        sys.exit()

    for i in range(data.size/3):
        print (' '.join(list(map(str,data[:,i]))))


# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
