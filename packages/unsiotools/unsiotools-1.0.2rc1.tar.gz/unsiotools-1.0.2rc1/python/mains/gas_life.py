#!/usr/bin/env python
# 


# Find out gas life of  particles


# MANDATORY
from unsio import *            # import unsio package (UNSIO)
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():

    output="gas_life.txt"  # default output
    parser = argparse.ArgumentParser(description="Compute gas particles end of life")
    parser.add_argument('input', help='Simulation name or list of files')
    parser.add_argument('-o', '--output', help="output file, default [%s]"%(output), default=output)

    args = parser.parse_args()

    compute(args.input,args.output)

# -----------------------------------------------------
# loadData, loads Ids of particles
def loadData(comp,uns):
    
    ok,time=uns.getValueF("time")
    
    
    #get Ids
    ok,id = uns.getArrayI(comp,"id")
    
    #return time,id(soretd),indexes   
    return time,id[id.argsort()],id.argsort()

# -----------------------------------------------------
# compute, is the core function
def compute(simname,out):
    components="gas" 
    times="all" 
    verbose=False

    # Create a UNSIO object
    uns = CunsIn(simname,components,times,verbose)
    bits="I"         # select properties, particles Identities only here

    # get file name
    sim_name=uns.getFileName()

    comp="gas"
    first=True

    fo = open(out, "w")  # open output file for writing
    
    while (uns.nextFrame(bits)):  # loop while there is something to read
        time,ids,index=loadData(comp,uns)  # returns time, array of Ids sorted, array of indexes sorted
        print time

        if first:  # The first time....
            time_last=time           # save current time
            ids_ref=np.copy(ids)     # make a copy of ids array into ids_ref array
            index_ref=np.copy(index) # make a copy of index array into index_ref array

            first=False              # end of first time
            fo.write("%s\n"%(sim_name)) # write simulation name or filename
        else:      # all others time
            #print ids
            print "ref size :",ids_ref.size, index_ref.size
            print "new size :",ids.size, index.size
            inter=np.in1d(ids_ref,ids)  # compute intersection of old ids_ref and new ids array

            idfinal=ids_ref[inter==False] # create an array of particles which have vanished into stars

            fo.write("%f %d %s\n"%(time_last,idfinal.size,uns.getFileName())) # write into file, time and #partciles which ended their gas life

            for a,b in zip(index_ref[inter==False],idfinal):
                fo.write("%d %d\n"%(a,b)) # write into file, particles index, particles ID which have ended their gas life

            ids_ref=ids_ref[inter==True]                 # create new ID_ref, ie particles IDs which are still gas
            index_ref=index_ref[inter==True]             # create new index_ref, ie particles indexes which are still gas
            print "time [%f] ids_ref [%d] end of life[%d]:"%(time_last,ids_ref.size,idfinal.size)
            time_last=time                               # save last time
        
    fo.close() # close file
 
    print "First must be false, here first = ", first

    print ids.size,ids_ref.size, idfinal.size, time_last


# -----------------------------------------------------
# main program
commandLine()   # parse command line
