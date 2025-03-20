#!/usr/bin/env python

from __future__ import print_function    
import sys
import argparse
import numpy as np                # arrays are treated as numpy arrays

import os.path
dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.append(dirname+'../modules/')  # trick to find modules directory
from uns_simu import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    dbname=None
    save_orbits=False
        # help
    parser = argparse.ArgumentParser(description="Display statistics on orbits computed with taxon program",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('simname', help='Simulation name')
    parser.add_argument('--save', help='save orbits indexes ?',default=save_orbits)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)

        # parse
    args = parser.parse_args()

    # start main funciton
    process(args.simname, args.dbname, args.save)


# -----------------------------------------------------
# process, is the core function
def process(simname,dbname,save_orbits):
    sql3 = UnsSimu(dbname)
    #sql3.printInfo(simname)
    
    r = sql3.getInfo(simname)
    if (r) :
        taxon_dir=r['dir']+'/ANALYSIS/taxon'
        orbits_cl=taxon_dir+"/orbits.cl"
        if os.path.exists(orbits_cl) : # orbits files exist
            stats(orbits_cl,save_orbits)	  
        else :
	    print("\nOrbits files [",orbits_cl,"] does not exist...\n")
    else:
        print("\nUnknown simulation : [",simname,"]\n")
            
            
# -----------------------------------------------------
# stats
def stats(orbits_cl,save_orbits):
    data=np.loadtxt(orbits_cl)
    print("\n\nStats from file : ",orbits_cl,"\n")
    print("\n#orbits processed : %d\n"%(data[:,1].size))
    ss =np.array([0,100,111,120,121,122,123,200,210,211,212,213,220,221,222,223,300,310,312,313,320,321,322,323,400])
    print(repr("code").rjust(3),repr("#").rjust(4),repr("%").rjust(7))
    for code in ss:
        x=(data[:,1]==code)
        if  (data[x].size!=0):
            myfile="id.%d"%(code)
            percen=data[x,1].size*100./data[:,1].size
            print(repr(code).rjust(3), repr(data[x,1].size).rjust(7),("%02.02f%%"%(percen)).rjust(7),myfile.rjust(7))
        if (save_orbits):
            np.savetxt(myfile,data[x,8],fmt="%d",header="#glnemo_index_list",comments='')

    print("\n")
            
# -----------------------------------------------------
# main program
commandLine()   # parse command line
