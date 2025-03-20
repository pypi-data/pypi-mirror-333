#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import os,time,glob
import sys
import argparse,textwrap

#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

import unsiotools.simulations.corbits as orbs

#from IPython import embed

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():

    # help
    parser = argparse.ArgumentParser(description="Compute different quantities on orbits",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dpath', help="DISTANCE PATH",default=None)
    parser.add_argument('--outfile', help="output file name",default=None)


    # parse
    args = parser.parse_args()
    # start main function
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    mypath=args.dpath

    # BIG ARRAY INDICES
    index_dmax=np.array([2,4,6,8])
    index_dmin=np.array([10,12,14,16])
    index_abs =np.array([18,20,22])
    index_time=np.array([1,3,5,7,9,11,13,15,17,19,21])
    first=True
    nn=0
    for i in glob.glob(mypath+"/orbits_*_data.npy"):
        index=(os.path.basename(i)).split("_")[1]
        print(i,"\n",nn)
        new_data=np.load(mypath+"/orbits_"+str(index)+"_data.npy")
        new_time=np.load(mypath+"/orbits_"+str(index)+"_time.npy")
        if first:
            first=False
            tab_data=np.zeros((new_data[:,0].size,23)) # id (0) t/dmax (1-8) t/dmin (9-16) t/|x| (17-18) t/|y| (19-20) t/|z| (21-22)

            tab_data[:,0]         =new_data[:,0]   # ids
            tab_data[:,index_dmax]=new_data[:,1:5] # dmax
            tab_data[:,index_dmin]=new_data[:,1:5] # dmin
            tab_data[:,index_abs] =new_data[:,5:8] # /x,y,z/
            tab_data[:,index_time]=new_time        # set time
        else:
            # proceed on max
            ii=1
            for i in index_dmax:
                print(i)
                v=np.where(new_data[:,ii]>tab_data[:,i])
                tab_data[v,i]=new_data[v,ii] # copy new dmax
                tab_data[v,i-1]=new_time     # copy new time
                ii = ii + 1
            # proceed on min
            ii=1
            for i in index_dmin:
                print(i)
                v=np.where(new_data[:,ii]<tab_data[:,i])
                tab_data[v,i]=new_data[v,ii] # copy new dmin
                tab_data[v,i-1]=new_time     # copy new time
                ii = ii + 1
            # proceed on |x| |y| |z|
            ii=1
            for i in index_abs:
                print(i)
                v=np.where(new_data[:,ii]>tab_data[:,i])
                tab_data[v,i]=new_data[v,ii] # copy new |value|
                tab_data[v,i-1]=new_time     # copy new time
                ii = ii + 1
        nn = nn+1
        if nn == -1:
           break

    outfile="tab_data"
    if args.outfile is not None :
        outfile=args.outfile
    np.save(outfile,tab_data)


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
