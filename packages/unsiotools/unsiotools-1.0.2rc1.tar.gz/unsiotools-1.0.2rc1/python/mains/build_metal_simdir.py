#!/usr/bin/env python
from __future__ import print_function
import sys
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path
from unsiotools.simulations.cmovie import * 
import argparse
import os,glob,subprocess


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None

    # help
    parser = argparse.ArgumentParser(description="Build directory for new metal simulation",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options

    parser.add_argument('srcdir', help='src directory ie : 30_idf401_init_gal3_-2_0.45')
    parser.add_argument('destdir',help="dest directory ei: /rydata/mdf/idf401_01")

    parser.add_argument('--basedir',help="basedir of sergey''s run with new metalicity",
                        default="/home/seger/data/accretion_project/workspace/untop_runs")

    parser.add_argument('--verbose',help='verbose mode on', dest="verbose", action="store_true", default=False)

    # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    if not os.path.isdir(args.destdir):
        print("create dir [%s]"%(args.destdir))
        os.makedirs(args.destdir)
    mylink=args.destdir+"/run"
    metaldir=args.basedir+"/"+args.srcdir
    print("metaldir : ",metaldir)
    if not  os.path.islink(mylink) and os.path.isdir(metaldir):
        print ("gonna link :",mylink," on ", metaldir)
        os.symlink(metaldir,mylink)
    simname=args.destdir.split('/')[-1]
    cmd="unsio_sql3_update_info.pl --simname %s --type Gadget --dir %s --base run/untop_run/snapshot"%(simname,args.destdir)
    print (cmd)
    subprocess.call(cmd,shell=True)
# -----------------------------------------------------
# main program
if __name__ == '__main__':
    commandLine()
