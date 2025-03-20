#!/usr/bin/env python
# -----------------------------------------------------------------------
# For more information about how to use UNSIO, visit:
# http://projets.lam.fr/projects/unsio/
# -----------------------------------------------------------------------
#  Copyright Jean-Charles LAMBERT (CeSAM)- 2008-2016
#
#  e-mail:   Jean-Charles.Lambert@lam.fr                                      
#  address:  Centre de donneeS Astrophysique de Marseille (CeSAM)         
#            Laboratoire d'Astrophysique de Marseille                          
#            Pole de l'Etoile, site de Chateau-Gombert                         
#            38, rue Frederic Joliot-Curie                                     
#            13388 Marseille cedex 13 France                                   
#            CNRS U.M.R 6110
# -----------------------------------------------------------------------

# unsio module loading
# ==> do not forget to update PYTHONPATH environment variable with
#     unsio location path
from __future__ import print_function
from unsio import *

import numpy as np
# cmd line
import sys, getopt


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# compute
def compute(file,out,comp,take,bits,mmult):
    compchk="gas,halo,disk,bulge,stars,bndry"
    uns=CunsIn(file,comp,"all")

    if uns.nextFrame(bits):
        unso=CunsOut(out,"gadget2")
        ok,tsnap=uns.getValueF("time") # return snasphot time
        print ("Snapshot time : ","%.03f"%tsnap)
        unso.setValueF("time",tsnap) # save snapshot time

        # loop on all components stored in comp variable
        for onecomp in (compchk.split(",")):
            printAndSaveProp(uns,unso,onecomp,take,mmult) # print properties for the component
        unso.save()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# keepEveryTake:
# from an input numpy array keep one particle every take
# input array MUST be a 1d array
# dim match to the array stride
def keepEveryTake(array,dim,take):
    if (dim==1):             # 1D array arrangement
        array=array[::take]  # keep one particle every take
        array=array*1 # we *1 to have a contiguous array
    else:                    # > 1D array arrangment
        # first reshape in n X "dim", then keep every take
        array=np.reshape(array,(-1,dim))[::take]
        # reshape in 1D array
        array=np.reshape(array,array.size)
    return array
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# printAndSaveProp
# print properties for the component comp given as argument
# keep one particle over tale
# and save them in gadget2 file
def printAndSaveProp(uns,unso,comp,take,mmult):
    info="""\
    ----------------------------------------------
    Component : [%s]
    ----------------------------------------------
    """
    print (info % (comp))
    # return a 1D numpy data array with mass
    ok,mass=uns.getArrayF(comp,"mass")
    if ok:
        print ("mass =",mass.size,mass)
        mass=keepEveryTake(mass,1,take)
        if mmult==1:
            mass=mass*take # multiply mass by take
        print ("mass =",mass.size,mass)
        unso.setArrayF(comp,"mass",mass) # save mass
        
    # return a 1D numpy data array with pos
    ok,pos=uns.getArrayF(comp,"pos")
    if ok:
        print ("pos =",pos)
        pos=keepEveryTake(pos,3,take)
        unso.setArrayF(comp,"pos",pos) # save pos
        
    # return a 1D numpy data array with vel
    ok,vel=uns.getArrayF(comp,"vel")
    if ok:
        print ("vel =",vel)
        vel=keepEveryTake(vel,3,take)
        unso.setArrayF(comp,"vel",vel) # save vel

    # return a 1D numpy data array with acc 
    ok,acc=uns.getArrayF(comp,"acc")
    if ok:
        print ("acc =",acc)
        acc=keepEveryTake(acc,3,take)
        unso.setArrayF(comp,"acc",acc) # save vel

   # return a 1D numpy data array with rho
    ok,rho=uns.getArrayF(comp,"rho")
    if ok:
        print ("rho =",rho)
        rho=keepEveryTake(rho,1,take)
        unso.setArrayF(comp,"rho",rho) # save rho

    # return a 1D numpy data array with temperature
    ok,temp=uns.getArrayF(comp,"temp")
    if ok:
        print ("temp =",temp)
        temp=keepEveryTake(temp,1,take)
        unso.setArrayF(comp,"temp",temp) # save temperature

    # return a 1D numpy data array with internal energy (U)
    ok,u=uns.getArrayF(comp,"u")
    if ok:
        print ("u =",u.size,u.dtype,u)
        u=keepEveryTake(u,1,take)
        print ("u =",u.size,u.dtype,u)
        unso.setArrayF(comp,"u",u) # save internal energy

    # return a 1D numpy data array with hsml
    ok,hsml=uns.getArrayF(comp,"hsml")
    if ok:
        print ("hsml =",hsml)
        hsml=keepEveryTake(hsml,1,take)
        unso.setArrayF(comp,"hsml",hsml) # save hsml

    # return a 1D numpy data array with particles age
    ok,age=uns.getArrayF(comp,"age")
    if ok:
        print ("age =",age)
        age=keepEveryTake(age,1,take)
        unso.setArrayF(comp,"age",age) # save age

    # return a 1D numpy data array with mettalicity
    ok,metal=uns.getArrayF(comp,"metal")
    if ok:
        print ("metal =",metal)
        metal=keepEveryTake(metal,1,take)
        unso.setArrayF(comp,"metal",metal) # save mettalicity

    # return a 1D numpy data array with potential 
    ok,pot=uns.getArrayF(comp,"pot")
    if ok:
        print ("pot =",pot)
        pot=keepEveryTake(pot,1,take)
        unso.setArrayF(comp,"pot",pot) # save mettalicity



    # return a 1D numy data array with id
    ok,indexes=uns.getArrayI(comp,"id")
    if ok:
        print ("indexes =", indexes)
        indexes=keepEveryTake(indexes,1,take)
        unso.setArrayI(comp,"id",indexes) # save id

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# main
def main(argv):
    prog = argv.pop(0) # program name
    infile=''
    out=''
    take=0
    comp='all'
    times='all'
    bits=''
    mmult=1

    try:
        opts,args=getopt.getopt(argv,"hi:o:k:c:b:m:",["in=","out=","take=","comp=","bits=","mmult="])

    except getopt.GetoptError:
        print ("\nUnknown parameters, please check ....\n\n")
        printHelp(prog)
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            printHelp(prog)
            sys.exit()
        elif opt in ("-i", "--in"):
            infile = arg
        elif opt in ("-o", "--out"):
            out = arg
        elif opt in ("-c", "--comp"):
            comp = arg
        elif opt in ("-k", "--take"):
            take = int(arg)
        elif opt in ("-b", "--bits"):
            bits = arg
        elif opt in ("-m", "--mmult"):
	            mmult = int(arg)


    if (infile != '' and out != '' and take !=0):
        compute(infile,out,comp,take,bits,mmult)
    else:
        print ("\nYou must provide input, output files and number of particles to take.....\n\n")
        printHelp(prog)
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# printHelp
def printHelp(prog):
    help= """\
    --------------------------------------------------
    From an input UNS input file:
    - Keep one particles every "take" particles, and
    - multiply masses by "take" and save into a gadget2 file
    --------------------------------------------------
    
    Syntaxe : %s  -i <inputfile> -o <outfile> -c <components> -k <taKe> -b <bits> -m <mmult>
    Example : %s  -i gtr118_1912 -o myfile.g2 -c all -k 10
    
    Notes :
        inputfile  : UNS input snapshot

        outfile    : gadget2 out filename
        
        components : specify just one or a coma separeted list of components
                     among => disk,gas,stars,halo,bulge,bndry or all
                     exemple : -c disk,stars
                     
        take       : number of particles to take

        bits       : you specify which array you want to process
                     example:
                       bits="mxvIU" (pos,mass,vel,id,internal energy)
                       bits="" (every array, default)    
        mmult      : multiply mass by take (default 1 - yes,  else  0 -  no)

    """
    print (help % (prog,prog))
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# main
if __name__ == "__main__":
    main(sys.argv[0:])
