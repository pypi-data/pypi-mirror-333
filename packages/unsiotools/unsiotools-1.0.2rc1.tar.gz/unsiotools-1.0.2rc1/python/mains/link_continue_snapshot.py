#!/usr/bin/env python
from __future__ import print_function
import sys
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path
import argparse
import os,glob
import errno
#from uns_simu import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None

    # help
    parser = argparse.ArgumentParser(description="Link snapshot snapshot on continue MDF simulations",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options

    parser.add_argument('simname', help='simulation name path')

    parser.add_argument('contdir', help='continuation sim dir')

    parser.add_argument('--verbose',help='verbose mode on', dest="verbose", action="store_true", default=False)

    # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
dirname="/rudata/mdf"
def process(args):
    for ff in sorted(glob.glob(args.contdir+"/"+args.simname+"/SNAPS/snapshot*")):
        try:
            ff2,ext=ff.split(".")
        except:
            pass
        base=os.path.basename(ff)
        name,id=base.split("_")
        try:
            id,dummy=id.split(".")
        except:
            pass
        target=dirname+"/"+args.simname+"/SNAPS/"+args.simname+"_"+id
        if not os.path.islink(target):
            print("target ",target)
            print("ff =",ff)
            try:
                os.symlink(ff,target)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    try:
                        os.remove(target)
                        os.symlink(ff,target)
                    except:
                        print("unable to remove ",target)
                else:
                    raise e


# -----------------------------------------------------
# process, is the core function
def process1(args):

    snap_list =     sorted(glob.glob(args.snapshot+'_?'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_??'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_???'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_????'))
    snap_list = snap_list+sorted(glob.glob(args.snapshot+'_?????'))

    cpt=0
    for mysnap in snap_list:
        mylink="snapshot_"+str(cpt)
        if not os.path.islink(mylink):
            print(mysnap,"snapshot_"+str(cpt))
            os.symlink(mysnap,mylink)
        cpt=cpt+1


# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
