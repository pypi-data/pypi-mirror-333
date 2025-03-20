#!/usr/bin/env python

import yt
import numpy as np
import sys
from unsio import *
from yt.data_objects.particle_filters import add_particle_filter
import math
import argparse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    keep=0.1
     # help
    parser = argparse.ArgumentParser(description="Convert Enzo simulation to gadget2",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('input', help='Input enzo file name')
    parser.add_argument('output', help='Output gadget2 file name')
    parser.add_argument('--keep', help='percentage of particles to keep',default=keep,type=float)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    ds = yt.load(args.input)  
    data = ds.all_data() # read all data

    #load positions
    pos=np.append([] ,data['x'])# 
    pos=np.append(pos,data['y'])#
    pos=np.append(pos,data['z'])#
    pos=np.reshape(pos,(-1,int(pos.size/3)))
    pos=np.reshape(pos.T,pos.size)
    pos=np.asarray(pos,np.float32) # convert to numpy array
    pos=pos*1000.  # multiply by 1000 to fix texture pb in glnemo2

    #load velocities
    vel=np.append([] ,data[("gas","velocity_x")].in_units("km/s"))
    vel=np.append(vel,data[("gas","velocity_y")].in_units("km/s"))
    vel=np.append(vel,data[("gas","velocity_z")].in_units("km/s"))
    vel=np.reshape(vel,(-1,int(vel.size/3)))
    vel=np.reshape(vel.T,vel.size)
    vel=np.asarray(vel,np.float32) # convert to numpy array

    # load dx
    dx=data[('gas','dx')]
    # load rho
    rho=np.asarray(data[('gas',"density")],np.float32)
    # load temperature
    temp=np.asarray(data[('gas',"temperature")],np.float32)
    # create hsml
    hsml=np.asarray(dx*math.sqrt(2.),np.float32)
    hsml=hsml*1000. # multiply by 1000 to fix texture pb in glnemo2

    # sort rho to select particles to highest density point
    rsort=np.argsort(1./rho)
    select_part=rsort[0:rsort.size*args.keep]
    print (select_part.size)

    # reformat positions and velocities according to selection
    pos2=np.reshape(pos,(-1,3))
    print (pos2[select_part])
    pos2=np.reshape(pos2[select_part],(-1))

    vel2=np.reshape(vel,(-1,3))
    print (vel2[select_part])
    vel2=np.reshape(vel2[select_part],(-1))

    # save in gadget2
    uns=CunsOut(args.output,"gadget2")
    uns.setArrayF("gas","pos",pos2)
    uns.setArrayF("gas","vel",vel2)
    uns.setArrayF("gas","rho",rho[select_part])
    uns.setArrayF("gas","hsml",hsml[select_part])
    uns.setArrayF("gas","temp",temp[select_part])
    uns.save()
# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
