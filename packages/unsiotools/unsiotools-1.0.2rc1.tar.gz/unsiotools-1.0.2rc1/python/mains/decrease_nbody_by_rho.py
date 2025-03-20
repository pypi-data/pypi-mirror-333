#!/usr/bin/env python

from unsio import *
import numpy as np

import argparse
EMBED=False
if EMBED:
    from IPython import embed

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():
    keep=0.1
    bins=50
    mult=1.
     # help
    parser = argparse.ArgumentParser(description="Convert Enzo simulation to gadget2",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('input', help='Uns simulation with GAS component')
    parser.add_argument('output', help='Output gadget2 file name')
    parser.add_argument('--keep', help='percentage of particles to keep',default=keep,type=float)
    parser.add_argument('--bins', help='rho cut in #bins',default=bins,type=float)
    parser.add_argument('--mult', help='multiply pos and hsml by this value',default=mult,type=float)
    parser.add_argument('--verbose',help='verbose mode', default=False)

     # parse
    args = parser.parse_args()

    # start main funcion
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):

    uns=CunsIn(args.input,"gas","all",True)

    if uns.isValid() and uns.nextFrame("mxRH"):

        ok,rho=uns.getArrayF("gas","rho")
        print ("Read rho",rho.min(),rho.max())
        if EMBED:
            embed()
        if ok:
            # sort rho to select particles to highest density point
            rsort=np.argsort(1./rho)          
            print ("sort rho",rho.min(),rho.max())  
            if EMBED:
                embed()
            tt=np.arange(args.bins)
            select_part=np.arange(0)
            for i in tt:
                start=i*(rho.size/tt.size)
                stop=start+(rho.size/tt.size)*args.keep
                print (start,stop)
                select_part=np.append(select_part,rsort[start:stop])

            print ">>", select_part.size
            #select_part=rsort[0:rsort.size*args.keep]
            #select_part=sel
            print (select_part.size)
            if EMBED:
                embed()
            
            # read hsml
            ok,hsml=uns.getArrayF("gas","hsml")
            hsml=hsml*args.mult
            # read pos
            ok,pos=uns.getArrayF("gas","pos")
            pos = pos*args.mult
            print (">> pos",pos.min(),pos.max())
            if EMBED:
                embed()
            # reformat positions and velocities according to selection
            pos2=np.reshape(pos,(-1,3))
            print (pos2[select_part])
            pos2=np.reshape(pos2[select_part],(-1))

            # save in gadget2
            unso=CunsOut(args.output,"gadget2")
            unso.setArrayF("gas","pos",pos2)
            unso.setArrayF("gas","rho",rho[select_part])
            unso.setArrayF("gas","hsml",hsml[select_part])
            unso.save()
# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
