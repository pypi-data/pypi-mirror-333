#!/usr/bin/env python
from __future__ import print_function

import sys
#sys.path=['/home/jcl/works/GIT/uns_projects/py/modules/','/home/jcl/works/GIT/uns_projects/py/modules/simulations']+sys.path

#from py_unstools import *         # import py_unstools package
#from unsio import *
#from general.ctools import *
import argparse
import os,subprocess

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line
def commandLine():
    dbname=None

     # help
    parser = argparse.ArgumentParser(description="test operation on files and directories",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # options
    parser.add_argument('file', help='input file, dir or link name')
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)
     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)


# -----------------------------------------------------
# process, is the core function
def process(args):
    r,f=rotateFile(args.file,debug=True)

    print(r,f)

# -----------------------------------------------------
# process, is the core function
def process1(args):
    if os.path.exists(args.file):
        print("yes [%s] exist.."%(args.file),file=sys.stderr)
        rotateFile(args.file)

def rotate(myfile):
    cpt=0
    stop=False
    while not stop:
        myfile="%s.%d"%(myfile,cpt)
        if not os.path.exists(myfile):
            stop=True
        else:
            cpt=cpt+1

    print("Rotate file [%s]"%(myfile))
# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()
