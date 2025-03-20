#!/usr/bin/env python

from __future__ import print_function
import sys
from unsio import *            # import unsio package (UNSIO)
import numpy as np
import argparse
#from IPython import embed

class snap:
    time   = None
    nbody  = None
    mass   = None
    pos    = None
    vel    = None
    ids    = None

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    time="all"
    verbose=False

    # help
    parser = argparse.ArgumentParser(description="Select components by their id",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name or snapshot')
    parser.add_argument('outname', help='Output name snapshot')
    parser.add_argument('component', help='Simulation component')
    parser.add_argument('massratio', help='galaxies mass ratio separated by comma (ex: "m1/m2,m1")')
    parser.add_argument('idgal', help='index of galaxy to extract',type=int)

    #parser.add_argument('--time',help='simulation time', default=time)
    parser.add_argument('--verbose',help='verbosity', default=verbose)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args.simname,args.outname,args.component,args.massratio,args.idgal,time,args.verbose)
    
# -----------------------------------------------------
#
def saveSnapshot(snap,idnew,outname):
    snap.pos=np.reshape(snap.pos,(-1,3))        # pos reshaped in a 2D array [nbody,3]
    snap.vel=np.reshape(snap.vel,(-1,3))        # pos reshaped in a 2D array [nbody,3]

    print ("pos size:",snap.pos.size,snap.pos.shape)
    # rescale pos
    snap.pos = snap.pos[idnew] # keep only good ids
    snap.pos = np.reshape(snap.pos,snap.pos.size) # flatten the array (mandatory for unsio)
    #print ("pos size:",snap.pos.size,snap.pos.shape)

    # rescale vel
    snap.vel = snap.vel[idnew] # keep only good ids
    snap.vel = np.reshape(snap.vel,snap.vel.size) # flatten the array (mandatory for unsio)

    # rescale mass
    snap.mass = snap.mass[idnew]

    # save data
    unso=CunsOut(outname,"nemo") # instantiate object
    
    unso.setValueF("time",snap.time)       # save snapshot time
    
    unso.setArrayF("all","pos",snap.pos)   # save pos
    unso.setArrayF("all","vel",snap.vel)   # save vel
    unso.setArrayF("all","mass",snap.mass) # save mass
    
    unso.save()
    

# -----------------------------------------------------
#
def getComponentByIds(snap,massratio,idgal):

    print("ID min %d / max %d"%(snap.ids.min(),snap.ids.max()),file=sys.stderr)

    #embed()
    
    # parse massratio variable
    m1om2,m1=massratio.split(",")
    m1om2 = float(m1om2)      # m1 / m2   massration of the 2 galaxies
    m1    = float(m1)         # m1 mass of gal1
    m2    = m1 / m1om2        # m2 mass of gal2
    mtot  = m1 + m2           # mtot total mass
    print ("m1om2=%f m1=%f m2=%f mtot=%f"%(m1om2,m1,m2,mtot),file=sys.stderr)
    #compute #bodies per galaxy
    nbody    = np.zeros(2)             # array to store #bodies ofr each particles
    nbody[0] = m1 * snap.nbody / mtot  # nbody gal1
    nbody[1] = m2 * snap.nbody / mtot  # nbody gal2
    nbody=nbody.astype(int)            # convert to int
    
    print("nbody :",nbody)

    offset = snap.ids.min() # first ID value for the component
    if (idgal==1):
        istart=offset            # first ID of gal1
        iend=istart+nbody.max()  # end of ID
    else:
        istart=offset+nbody.max() # according to Sergey, massive galaxy always first so we put nbody.max()
        iend=istart+nbody.min()


    if (iend-istart > snap.nbody) :
        print("Error, iend %d computed > %d bodies"%(iend-istart,snap.nbody),file=sys.stderr)
        sys.exit()

    #embed()
    idnew   = (snap.ids>=istart) & (snap.ids<=iend) # selection criteria
    indexes = np.array((idnew.nonzero())).reshape(-1,) # retreive indexes array
    #embed()
    print(idnew,indexes)
    
    return True,indexes
# -----------------------------------------------------
# process, is the core function
def process(simname,outname,component,massratio,idgal,time,verbose):
    #print (simname, " " , time,file=sys.stderr)
    # Create a UNSIO object
    uns = CunsIn(simname,component,time,verbose)
    find=False
    bits="mxvI"
    while (uns.nextFrame(bits)):  # loop while there is something to read
        ok,snap.time  = uns.getValueF("time")
        ok,snap.nbody = uns.getValueI("nsel")
        ok,snap.mass  = uns.getArrayF(component,"mass")
        ok,snap.pos   = uns.getArrayF(component,"pos")
        ok,snap.vel   = uns.getArrayF(component,"vel")
        ok,snap.ids   = uns.getArrayI(component,"id")
        if ok:
            find=True
            print ( simname, component, snap.time, snap.nbody,snap.mass[0], snap.nbody*snap.mass[0])
            break;

    if not find:
        print ("none")
    else:
        ok,idnew=getComponentByIds(snap,massratio,idgal)
        if ok:
            saveSnapshot(snap,idnew,outname)
# -----------------------------------------------------
# main program
commandLine()   # parse command line
