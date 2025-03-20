#!/usr/bin/env python

# unsio
from unsio import *
import numpy as np
# cnd line
import sys, getopt,os.path


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# main
def main(argv):
    prog = os.path.basename(argv.pop(0)) # program name
    file=''
    listf=''
    out=''

    try:
        opts,args=getopt.getopt(argv,"hi:o:l:",["in=","list="])

    except getopt.GetoptError:
        printHelp(prog)
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            printHelp(prog)
            sys.exit()
        elif opt in ("-i", "--in"):
            file = arg
        elif opt in ("-o", "--out"):
            out = arg
        elif opt in ("-l", "--list"):
            listf = arg

        
    if (file!='' and out!='' and listf!=''):
        if (not os.path.isfile(listf)):
            print "\n\nFile :",listf," does not exist, aborting\n\n"
            sys.exit()
        #bigage=np.array( readAge(listf))
        bigage=readAge(listf)
        print "bigage >>>> =",bigage," size=",bigage.size
        compute(file,out,bigage)
                    
    else:
        printHelp(prog)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# printHelp
def printHelp(prog):
    help= """\
    
    ----------------------------------------------
    Add age properties on snapshots which have been
    artificially multiplied by 40
    ----------------------------------------------
    
    Syntaxe : %s  -i <inputfile> -o <outputfile> -l <liste>

    Notes :
      inputfile  : UNS snapshot with stars component
      outputfile : gadget2 out filename
      list       : list of 10 snapshots used to increase number of particles
      
    """
    print help % (prog) 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# compute
#@profile
def compute(file,out,bigage):
    print "file=",file, ' bigage=', bigage
    time="all"
    comp="all"
    unsi=CunsIn(file,comp,time);  # input file

    unso=CunsOut(out,"gadget2");    # output file
    
    # load frame
    ok=unsi.nextFrame("")
    print ok

    ok,nsel=unsi.getValueI("nsel")
    if (nsel != bigage.size):
        err="""
        Inconsistent number of particles :
        
        nsel[%d] particles read from snapshot[%s], is different
        from #stars[%d] particles read from list of snaphots
        aborting....
        
        """
        print err  % (nsel,file,bigage.size)
        sys.exit()
        
    ok,time=unsi.getValueF("time")
    print "time=",time
    ok=unso.setValueF("time",time)
    
    # ids
    ok,id=unsi.getArrayI(comp, "id")
    if ok:
        ok=unso.setArrayI(comp,"id",id)

    # pos,vel,mass
    processData("pos",unsi,unso)
    processData("vel",unsi,unso)
    processData("mass",unsi,unso)

    #save ages
    print "bigage :", bigage.size, bigage.shape, type(bigage), bigage.dtype.name
    
    ok=unso.setArrayF("stars","age",bigage)

    # save on disk
    unso.save()
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# processData
#@profile
def processData(prop,unsi,unso):
    # get data
    ok,data=unsi.getArrayF(prop)
    print "processing:",prop," type=",type(data),data.dtype.name
    if ok:
        ok=unso.setArrayF("stars",prop,data)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# readAge
#@profile
def readAge(listf):
    # open list of files
    try:
        f = open(listf,'r')
    except IOError:
        print 'Cannot open file [',listf,'] aborting'
        sys.exit()
        
    totage=0
    bigage=np.array([],dtype='float32')
    for line in f:  # read line by line
        print((line.rstrip()))  # print filename
        time="all"
        comp="stars"
        uns=CunsIn(line.rstrip(),comp,time);
        if (not uns.isValid()) :
            print "File [",line.rstrip(),"] is not a valide uns file, aborting..."
            sys.exit()
        # load frame
        ok=uns.nextFrame("")
        if not ok:
            print "Unable to load snapshot [",line.rstrip(),"] aborting...."
            sys.exit()
        # get data
        prop="age"
        ok,age=uns.getArrayF(prop)
        print ok
        print age, age.size
        totage+=age.size
        bigage=np.append(bigage,age)
        del uns
        
    print "total age = ", totage
    print "bage.size = ", bigage.size
    bigage4 = np.array([],dtype='float32')
    for i in range(4):
        bigage4 = np.append(bigage4,bigage)
    return bigage4
    

if __name__ == "__main__":
    main(sys.argv[0:])




