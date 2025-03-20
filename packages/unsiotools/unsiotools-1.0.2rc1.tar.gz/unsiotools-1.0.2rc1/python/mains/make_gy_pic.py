#!/usr/bin/env python
# 


from __future__ import print_function
import sys
import numpy as np                # arrays are treated as numpy arrays
import math
import argparse
import subprocess 
#from IPython import embed

#convert -size 100x40 xc:transparent  -pointsize 19 -fill white  -draw "text 14,25 '0.2 Gy'" linuxandlife.png
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# process
def process(args):
    for index in xrange(args.first, args.last+1):
        frame = str("%s.%05d.png"%(args.output,index))
        time=args.time+(index-args.first)*args.dt
        gy = str("%.2f Gyears"%(time))
        #cmd=str("convert -size 180x60 xc:transparent  -pointsize 28 -fill white  -draw \"text 1,30 '%s'\" %s"%(gy,frame)) 
        cmd=str("convert -size 180x60 xc:black  -pointsize 28 -fill white  -draw \"text 1,30 '%s'\" %s"%(gy,frame)) 
        print (frame, gy)
        print (cmd)
        subprocess.call(cmd,shell=True)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    output="frame"
    dt=0.005
    parser = argparse.ArgumentParser(description="Create pictures to display simulation time in Gyears ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('first', help='first frame index',type=int)
    parser.add_argument('last', help='last frame index',type=int)
    parser.add_argument('time', help='start time',type=float)
    parser.add_argument('--dt', help='delta t time',type=float,default=dt)
    
    parser.add_argument('--output', help='output name frame',default=output)
        


    args = parser.parse_args()

    process(args)



# -----------------------------------------------------
# main program
commandLine()   # parse command line
