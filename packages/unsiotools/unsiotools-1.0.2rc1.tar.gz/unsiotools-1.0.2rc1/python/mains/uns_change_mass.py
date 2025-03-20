#!/usr/bin/env python

import sys
import unsio.output as u_out
import unsio.input as u_in

import argparse
import numpy as np

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None
    ncores=None

     # help
    parser = argparse.ArgumentParser(description="Change masses and velocities from mdf IC",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('input', help='Simulation name')
    parser.add_argument('output', help=' output file')
    parser.add_argument('mass_f', help='mass factor value',type=float)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

def readAndWrite(comp,tag,uns_snap,outsnap,mass_f,verbose):
    ok,data=uns_snap.getData(comp,tag)
    if verbose:
        print("Type :",data.dtype," tag=",tag)
    if ok:
        print(" ",tag,end="")
        if tag=="mass":
            data=data*mass_f
        if tag=="vel":
            data=data*(mass_f**0.5)
        # save array
        outsnap.setData(data,comp,tag)

# -----------------------------------------------------
# process, is the core function
def process(args):

    uns_snap=u_in.CUNS_IN(args.input,"all",verbose_debug=args.verbose)
    ok_load = uns_snap.nextFrame()
    ok,timex=uns_snap.getData("time")
    # open for writing snapshot
    outsnap=u_out.CUNS_OUT(args.output,uns_snap.getInterfaceType())
    print ("Time :",timex)

    if ok_load:

        for comp in (["halo","gas","stars","disk","bulge"]):
            print("COMP [%s]"%comp,end="")
            for tag in (["pos","vel","mass","id","rho","hsml","acc","pot","u"]):
                readAndWrite(comp,tag,uns_snap,outsnap,args.mass_f,args.verbose)
            print("\n")
        outsnap.save()
    else:
        print ("unable to load snapshot")

#
# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
