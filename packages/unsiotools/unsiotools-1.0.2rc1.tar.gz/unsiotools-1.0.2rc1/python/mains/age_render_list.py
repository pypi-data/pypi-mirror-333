#!/usr/bin/env python
# 


from __future__ import print_function
import sys
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse
#from IPython import embed


    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# process
def process(input,output,dt):
    list = x=np.loadtxt(input,dtype=str)

    for ff in list:
        # get file
        _file = str.split(ff,"/")[-1]
        # get index
        _index = int(str.split(_file,'_')[-1])
        # create output name
        frame="%s.%05d.jpg"%(output,_index)

        print("age_to_density.py %s - --dt=%f | glnemo2 - all screenshot=%s"%(ff,dt,frame))
    # get index
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    output="shot"
    
    parser = argparse.ArgumentParser(description="Create a rendering list of age to density glnemo2 process",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', help='input list')
    parser.add_argument('dt', help='dt value, see age_to_density.py',type=float)
    
    parser.add_argument('--output', help='output name frame',default=output)
        


    args = parser.parse_args()

    process(args.input,args.output,args.dt)



# -----------------------------------------------------
# main program
commandLine()   # parse command line
