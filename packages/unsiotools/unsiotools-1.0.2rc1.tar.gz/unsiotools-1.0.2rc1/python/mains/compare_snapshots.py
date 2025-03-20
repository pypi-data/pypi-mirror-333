#!/usr/bin/env python

#
# This program test unsio library by readind and saving same file in different output
# file format (gadget2, nemo) and comparing all arrays with original one
#
from __future__ import print_function    
import sys
import argparse
import numpy as np                # arrays are treated as numpy arrays

import os.path
#dirname, filename = os.path.split(os.path.abspath(__file__))
#sys.path.append(dirname+'../modules/')  # trick to find modules directory
from unsio import *
import copy
import tempfile
#from IPython import embed

class snap:
    time   = None
    nbody  = None
    mass   = None
    pos    = None
    vel    = None
    acc    = None
    pot    = None
    u      = None
    id     = None
    age    = None
    hsml   = None
    rho    = None
    metal  = None
    interface = ""
 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    # help
    parser = argparse.ArgumentParser(description="Compare to given snapshot arrays vs arrays",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('snapshot_1', help='UNS snapshot')
    parser.add_argument('snapshot_2', help='UNS snapshot')
    parser.add_argument('component', help='component name')
    float_parser=parser.add_mutually_exclusive_group(required=True)
    float_parser.add_argument('--float',    help='floating format operation',action='store_true')
    float_parser.add_argument('--double', help='double format operation',  action='store_true')
    parser.add_argument('--out', help='save output file name ?',default="")
        # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

# -----------------------------------------------------
def readSnap(simname, comp, single):
    components=comp 
    verbose=False

    
    #timef=float(times)
    
    # Create a UNSIO object
    if (single) :
        #print("Float format object")
        uns = CunsIn(simname,components,"all",verbose)
    else:
        #print("Double format object")
        uns = CunsInD(simname,components,"all",verbose)

    #print ("simname=",simname,file=sys.stderr)

    mysnap=snap() # instantiate a snap object
    # load frame
    ok=uns.nextFrame("")
    #print ok

    if (ok) :
        #embed()
        mysnap.interface = uns.getInterfaceType()
        ok,mysnap.time = uns.getValueF("time")
        ok,mysnap.pos  = uns.getArrayF(comp,"pos")
        ok,mysnap.vel  = uns.getArrayF(comp,"vel")
        ok,mysnap.mass = uns.getArrayF(comp,"mass")
        ok,mysnap.hsml = uns.getArrayF(comp,"hsml")
        ok,mysnap.rho  = uns.getArrayF(comp,"rho")
        ok,mysnap.u    = uns.getArrayF(comp,"u")
        ok,mysnap.age  = uns.getArrayF(comp,"age")
        ok,mysnap.acc  = uns.getArrayF(comp,"acc")
        ok,mysnap.pot  = uns.getArrayF(comp,"pot")
        ok,mysnap.metal= uns.getArrayF(comp,"metal")
        if ok:
            mysnap.metal=fixMetal(mysnap.metal)
        ok,mysnap.id   = uns.getArrayI(comp,"id")
        uns.close()
        return True,copy.deepcopy(mysnap)
        
    else :
        print ("Didn't load anything....",file=sys.stderr)

    return False
  
# -----------------------------------------------------
def compareArray(CA,CB,attr):
    #embed()
    A=getattr(CA,attr)
    B=getattr(CB,attr)
    ok=False
    disp=True
    if notCompare(CA,CB,attr):
        disp=False
    else:
        if attr=="time":
            ok = (A==B)
        else:
            ok=(A==B).all()
            if ok :
                if (A.size):
                    disp=True
                else:
                    disp=False

    if (disp):
        print("[",attr,"]",ok)
        if not ok:
            print("\tA:",A[0:2],"\n\tB:",B[0:2])

# -----------------------------------------------------
# do not compare in the following cases
def notCompare(CA,CB,attr):
    status=False
    if (CA.interface=="Nemo" or CB.interface=="Nemo"):
        if attr=="metal":
            status=True
        if attr=="age":
            status=True
        if status:
            print("<",attr,"> attribute not supported with NEMO format")
    A=getattr(CA,attr)
    if (attr != "time" and A.size==0):
        status=True
        #print("In <",attr,"> attribute not tested")
    B=getattr(CB,attr)
    if (attr != "time" and A.size!=0 and B.size==0):
        print("In <",attr,"> attribute missing in B")
        status=True
    return status
        
# -----------------------------------------------------
def compare(CA,CB,comp):
    print("-----------------------------------------------------")
    print("Comparing : <%s> [%s] vs [%s]\n"%(comp,CA.interface,CB.interface))
    for attr in ("pos","vel","mass","age","hsml","rho","metal","acc","pot","u", "id","time"):
        compareArray(CA,CB,attr)

# -----------------------------------------------------
def fixMetal(metal):
    if (metal==-1.0).all() :
        print("fixing metal....")
        return np.empty(0)
    else:
        return metal

# -----------------------------------------------------
# process
def process(args):

    if args.component == "all":
        comp_sel=["halo", "gas", "stars", "disk", "bulge", "bndry"]
    else:
        comp_sel=[args.component]
    for comp in (comp_sel):
        ok,insnap1=readSnap(args.snapshot_1,comp,args.float)
        ok,insnap2=readSnap(args.snapshot_2,comp,args.float)
        compare(insnap1,insnap2,comp)


# -----------------------------------------------------
# main program
commandLine()   # parse command line
#
