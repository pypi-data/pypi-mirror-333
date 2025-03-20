#!/usr/bin/python
from __future__ import print_function

import sys
sys.path.insert(0,'/home/jcl/works/GIT/uns_projects/py/modules/simulations')
sys.path.insert(0,'/home/jcl/works/GIT/uns_projects/py/modules')
from uns_simu import *
from simulations.csnapshot import *
import argparse

class myargs:
    simname="mdf040%100"
    select="all"
    float=True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    dbname=None
    select="all"
    real_32bits=True;
     # help
    parser = argparse.ArgumentParser(description="UNS test python",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('--select',help='components', default=select)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    float_parser=parser.add_mutually_exclusive_group(required=True)
    float_parser.add_argument('--float',    help='floating format operation',action='store_true')
    float_parser.add_argument('--double', help='double format operation',  action='store_true')



     # parse
    args = parser.parse_args()

    # start main funciton
    process_sq3(args)
    #process_snaps(args)


# -----------------------------------------------------
# process, is the core function
def process_sq3(args):
    sql3 = UnsSimu(args.dbname)
    sql3.printInfo(args.simname)

    r = sql3.getInfo(args.simname)

    snap_list = sql3.getSnapshotList(args.simname)
    
    if (snap_list):
        for i in snap_list:
            print(">> ", i)

# -----------------------------------------------------
# process, is the core function
def process_snaps(args):
    print ("args.float=",args.float)
    try:
        snap = CSnapshot(args.simname,args.select,float32=args.float)
        ok=snap.nextFrame()
        ok,data1=snap.getData("stars,gas","pos")
        ok,data2=snap.getData("gas,stars","pos")
        print ("ok=",ok," data1=",data1.size,data1,type(data1[0]))
        print ("ok=",ok," data2=",data2.size,data2,type(data2[0]))

        ok,timex=snap.getData("time")
        print  ("Time =", timex,type(timex))

    except RuntimeError,e:
        print("Unknow sim : ",e)
    
    
# -----------------------------------------------------
# main program
# parse command line
if __name__ == '__main__':
    commandLine()
