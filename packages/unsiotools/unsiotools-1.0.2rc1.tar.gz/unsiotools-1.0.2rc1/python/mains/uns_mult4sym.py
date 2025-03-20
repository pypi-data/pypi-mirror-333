# unsio
from unsio import *
import numpy as np
# cnd line
import sys, getopt

def main(argv):
    prog = argv.pop(0) # program name
    file=''
    comp=''
    prop=''

    try:
        opts,args=getopt.getopt(argv,"hi:c:p:",["in=","comp=","prop="])

    except getopt.GetoptError:

        print prog,' -i <inputfile> -c <component> -p <properties>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print prog,' -i <inputfile> -c <component> -p <properties>'
            sys.exit()
        elif opt in ("-i", "--in"):
            file = arg
        elif opt in ("-c", "--comp"):
            comp = arg
        elif opt in ("-p", "--prop"):
            prop = arg

    compute(file,comp,prop)
    
def compute(file,comp,prop):
    print "file=",file," comp=",comp," prop=",prop
    time="all"
    uns=CunsIn(file,comp,time);

    # load frame
    ok=uns.nextFrame("")
    print ok
    
    # get data
    ok,data=uns.getArrayF(comp,prop)
    print ok
    print data

    if (prop=="pos" or prop=="vel" or prop=="acc"):
        # reshap 1D to 2D
        data=np.reshape(data,(-1,3))
        
        # get col 1 to x
        x = data[:,0]
        
        # get col 2 to y
        y = data[:,1]


if __name__ == "__main__":
    main(sys.argv[0:])
