#!/usr/bin/env python
from __future__ import print_function
#import sys
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path
#from .cmovie import *
from unsiotools.uns_simu import *
from unsiotools.simulations.csnapshot import *

import argparse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None

    # help
    parser = argparse.ArgumentParser(description="Display simulation final time",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options

    parser.add_argument('simname', help='Simulation name')

    parser.add_argument('--save', help='Save file',dest='save',action='store_true',default=False)
    parser.add_argument('--filename',help='Filename to save final time, if None uses simulation directory', default=None)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode on', dest="verbose", action="store_true", default=False)
    #parser.add_argument('--no-verbose',help='verbose mode off', dest="verbose", action="store_false", default=True)

    # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    sql3 = UnsSimu(args.simname)
    #sql3.printInfo(simname)

    r = sql3.getInfo(args.simname)

    if (r):
        snap_list=sql3.getSnapshotList()
        latest=snap_list[-1]
        print("Latest snapshot [%s]\n"%(latest),file=sys.stderr)
        s=CSnapshot(latest)
        ok=s.unsin.nextFrame("I")
        ok,t=s.unsin.getData("time")
        if ok:
            print("Latest time [%f]\n"%(t),file=sys.stderr)
            print("%f"%(t))
            if args.save:
                filename=args.filename
                if args.filename is None: #simulation dir
                    filename=r['dir']+"/final_time.txt"
                print("Save to <%s>\n"%(filename),file=sys.stderr)
                index=(latest.split("/")[-1]).split("_")[-1]
                try:
                    f=open(filename,"w")
                    f.write("simname %s\n"%(args.simname))
                    f.write("last_file %s\n"%(latest))
                    f.write("last_index %s\n"%(index))
                    f.write("last_time %f\n"%(t))
                    f.close()
                except:
                    print("\n\nUnable to save in <%s>, aborting....\n"%(filename),file=sys.stderr)
                    sys.exit()

# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
