#!/usr/bin/env python
# -----------------------------------------------------------------------
# For more information about how to use UNSIO, visit:
# http://projets.lam.fr/projects/unsio/
# -----------------------------------------------------------------------
#  Copyright Jean-Charles LAMBERT (CeSAM)- 2008-2017
#
#  e-mail:   Jean-Charles.Lambert@lam.fr                                      
#  address:  Centre de donneeS Astrophysique de Marseille (CeSAM)         
#            Laboratoire d'Astrophysique de Marseille                          
#            Pole de l'Etoile, site de Chateau-Gombert                         
#            38, rue Frederic Joliot-Curie                                     
#            13388 Marseille cedex 13 France                                   
#            CNRS U.M.R 6110
# -----------------------------------------------------------------------
from __future__ import print_function
# unsio module loading
# ==> do not forget to update PYTHONPATH environment variable with
#     unsio location path
from unsio import *

import numpy as np
# cmd line
import sys, argparse, os

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# load indexes from file
def loadIds(args):
    if not os.path.isfile(args.id_file):
        print("File <%s> does not exist, aborting...\n"%(args.id_file),file=sys.stderr)
        sys.exit()
    else:
        data=np.genfromtxt(args.id_file,dtype=np.int,skip_header=1)
        print("Size [%d]\n"%(data.size),data)
        return data
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# compute
def process(args):

    # load ids
    id_list=loadIds(args)

    if args.select=="all":
        args.select="gas,halo,disk,bulge,stars,bndry"

    uns=CunsIn(args.input,args.select,"all",args.verbose)

    if not uns.isValid():
        print("Unknown UNS date from file <%s>, aborting..."%(args.input),file=sys.stderr)
        sys.exit()

    cpt=0
    while uns.nextFrame(args.bits):
        outfile=args.output
        if cpt==0 and args.tfirst or cpt>0:
            outfile="%s_%05d"%(outfile,cpt)
        unso=CunsOut(outfile,"gadget2")
        ok,tsnap=uns.getValueF("time") # return snasphot time
        #print "Snapshot time : ","%.03f"%tsnap

        nsave=0
        # loop on all components stored in select variable
        for onecomp in (args.select.split(",")):
            nsave += selectByIds(args,onecomp,id_list,uns,unso)

        if nsave > 0:
            unso.setValueF("time",tsnap) # save snapshot time
            unso.save()
            cpt += 1
        else:
            print("Nothing to save for file <%s>."%(args.input),file=sys.stderr)
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# select particles from their id
# and save them in gadget2 file
def selectByIds(args,comp,id_list,uns,unso):

    info="""\
    ----------------------------------------------
    Component : [%s]
    ----------------------------------------------
    """%(comp)
    print("%s"%(info),file=sys.stderr)

    status=0

    # return a 1D numy data array with id
    ok,indexes=uns.getArrayI(comp,"id")
    if ok:
        good_id=np.in1d(indexes,id_list)
        if indexes[good_id].size == 0:
            print("\n No ids match this component [%s], skipping...\n"%(comp),file=sys.stderr)
            return 0
    else:
        print("\nThere are no IDS in input file....\n",file=sys.stderr)
        return status

    print(good_id)

    # return a 1D numpy data array with mass
    ok,mass=uns.getArrayF(comp,"mass")
    if ok:
        status=1
        print("mass =",mass.size,mass,file=sys.stderr)
        mass=mass[good_id]
        print ("mass =",mass.size,mass,file=sys.stderr)
        unso.setArrayF(comp,"mass",mass) # save mass
        
    # return a 1D numpy data array with pos
    ok,pos=uns.getArrayF(comp,"pos")
    if ok:
        status=1
        print ("pos =",pos,file=sys.stderr)
        pos = np.reshape(pos,(-1,3))
        pos = np.reshape(pos[good_id],pos[good_id].size)
        unso.setArrayF(comp,"pos",pos) # save pos
        
    # return a 1D numpy data array with vel
    ok,vel=uns.getArrayF(comp,"vel")
    if ok:
        status=1
        print ("vel =",vel,file=sys.stderr)
        vel = np.reshape(vel,(-1,3))
        vel = np.reshape(vel[good_id],vel[good_id].size)        
        unso.setArrayF(comp,"vel",vel) # save vel

    # return a 1D numpy data array with acc 
    ok,acc=uns.getArrayF(comp,"acc")
    if ok:
        status=1
        print ("acc =",acc,file=sys.stderr)
        acc = np.reshape(acc,(-1,3))
        acc = np.reshape(acc[good_id],acc[good_id].size)
        unso.setArrayF(comp,"acc",acc) # save vel

   # return a 1D numpy data array with rho
    ok,rho=uns.getArrayF(comp,"rho")
    if ok:
        status=1
        print ("rho =",rho,file=sys.stderr)
        rho=rho[good_id]
        unso.setArrayF(comp,"rho",rho) # save rho

    # return a 1D numpy data array with temperature
    ok,temp=uns.getArrayF(comp,"temp")
    if ok:
        status=1
        print ("temp =",temp,file=sys.stderr)
        temp=temp[good_id]
        unso.setArrayF(comp,"temp",temp) # save temperature

    # return a 1D numpy data array with internal energy (U)
    ok,u=uns.getArrayF(comp,"u")
    if ok:
        status=1
        print ("u =",u.size,u.dtype,u,file=sys.stderr)
        u=u[good_id]
        print ("u =",u.size,u.dtype,u,file=sys.stderr)
        unso.setArrayF(comp,"u",u) # save internal energy

    # return a 1D numpy data array with hsml
    ok,hsml=uns.getArrayF(comp,"hsml")
    if ok:
        status=1
        print ("hsml =",hsml,file=sys.stderr)
        hsml=hsml[good_id]
        unso.setArrayF(comp,"hsml",hsml) # save hsml

    # return a 1D numpy data array with particles age
    ok,age=uns.getArrayF(comp,"age")
    if ok:
        status=1
        print ("age =",age,file=sys.stderr)
        age=age[good_id]
        unso.setArrayF(comp,"age",age) # save age

    # return a 1D numpy data array with mettalicity
    ok,metal=uns.getArrayF(comp,"metal")
    if ok:
        status=1
        print ("metal =",metal,file=sys.stderr)
        metal=metal[good_id]
        unso.setArrayF(comp,"metal",metal) # save mettalicity

    # return a 1D numpy data array with potential 
    ok,pot=uns.getArrayF(comp,"pot")
    if ok:
        status=1
        print ("pot =",pot,file=sys.stderr)
        pot=pot[good_id]
        unso.setArrayF(comp,"pot",pot) # save mettalicity

    # return a 1D numy data array with id
    ok,indexes=uns.getArrayI(comp,"id")
    if ok:
        status=1
        print ("indexes =", indexes,file=sys.stderr)
        indexes=indexes[good_id]
        unso.setArrayI(comp,"id",indexes) # save id

    return status
       
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    dbname=None

    # help
    parser = argparse.ArgumentParser(description="Select particles by their ids given from file",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    
    parser.add_argument('input',  help='UNS input file')
    parser.add_argument('output', help='UNS output file')
    parser.add_argument('select', help='selected components separated by coma')
    parser.add_argument('id_file', help='input file with particles\'s id (aka glnemo2 index file)')
    parser.add_argument('--bits', help='specify which array you want to proces\nexample:\nbits=\"mxvIU\" (pos,mass,vel,id,internal energy)\nbits=\"\" (every array, default)',default="")
    parser.add_argument('--tfirst ',help='add trailing number to the first snapshot', dest="tfirst", action="store_true", default=False)
    parser.add_argument('--dbname',help='UNS database file name', default=dbname)
    parser.add_argument('--verbose',help='verbose mode on', dest="verbose", action="store_true", default=False)

    # parse
    args = parser.parse_args()   
    print ("tfirst=",args.tfirst)
    # start main funciton
    process(args)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# main
if __name__ == "__main__":
    commandLine()
