#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

# cnd line
import sys, getopt,os.path
#sys.path.append('/home/jcl/works/SVN/uns_projects/trunk/py/modules/')
from unsiotools.uns_simu import *
import argparse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# main
def main(argv):
    prog = os.path.basename(argv.pop(0)) # program name

    dt=0.005 # check cpu time between 2 dt
    file="cpu.txt"
    tf=0.0    # time first
    tl=-1.    # time last
    out=''    # if blank plot on screen, else on png file
    tmax=10.  # gadget.param file
    smooth=0  # smooth or not curve
    try:
        opts,args=getopt.getopt(argv,"h",["in=","tm=","out=","dt=","tf=","tl=","smooth="])

    except getopt.GetoptError:
        printHelp(prog,file,dt,tf,tl,out,smooth)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            printHelp(prog,file,dt,tf,tl,out)
            sys.exit()
        elif opt in ("--in"):
            file = arg
        elif opt in ("--dt"):
            dt = float(arg)
        elif opt in ("--tf"):
            tf = float(arg)
        elif opt in ("--tl"):
            tl = float(arg)
        elif opt in ("--out"):
            out = arg
        elif opt in ("--tm"):
            tmax = float(arg)
        elif opt in ("--smooth"):
            smooth  = int(arg)

    fig = plt.figure(figsize=(8,8),dpi=100)

    #status,gparam=parseGadgetParam(param) # parse gadget param file

    #if len(gparam)>1:
    #    dt = float(gparam['MaxSizeTimestep'])
    #    print "Overwrite dt from gadget.patam = ",dt

    for f in file.split(","):
        try:
            cpu_file,mylegend=f.split(":") # parse filename:legend

        except ValueError:
            f_label=f
            cpu_file=f
        else:
            f_label=mylegend

        # try database
        if (os.path.basename(cpu_file)!="cpu.txt"):
            simname=cpu_file
            sql3 = UnsSimu()
            r = sql3.getInfo(simname)
            sql3.printInfo(simname)
            if (r):
                cpu_file=r['dir']+"/SNAPS/cpu.txt"
                print "cpu_file = ",cpu_file
            else:
                print "Simulation [",cpu_file,"] does not exist in unsio database..."
                sys.exit()

        time,cpu,ncores=parseCPU(cpu_file,dt,tf,tl)
        f_label=f_label+" cpus=%d"%ncores
        if tmax>0 and (tmax-time[-1])>0.01:
            mcp=min(10,cpu.size)
            meancpu=cpu[cpu.size-mcp:].mean(dtype=np.float64)
            print "last cpu :",time[-1],cpu[-1],mcp,meancpu
            sec=(tmax-time[-1])/dt*meancpu
            #print "Secondes remaining :",sec,time[-1],cpu[-1]
            dhms=getHMS(int(sec),"ETA")
            print "HMS=",dhms
            f_label=f_label+"\n%s"%(dhms)
        print time.size
        elapsed=np.sum(cpu)#-cpu[0])
        print "Elapsed : ",elapsed, " cpu0=",cpu[0],cpu[-1]
        ddd=getHMS(int(elapsed),"ELD")
        f_label=f_label+"\n%s"%(ddd)
        if (smooth):
            z=np.polyfit(time,cpu,4)
            f4=np.poly1d(z)
            plt.plot(time,f4(time),label=f_label)
        else:
            plt.plot(time,cpu,label=f_label)


    plt.xlabel('Simulation time')
    plt.ylabel('Cpu time (seconds)')
    plt.title('Cpu time every dt='+'%f'%dt)
    leg=plt.legend(loc='best', fancybox=True)
    leg.get_frame().set_alpha(0.5)

    if (out==''):
        plt.show()
    else:
        print "out fig=",out
        plt.savefig(out)#, bbox_inches=0)

    plt.close(fig)

    sys.exit()

# Parse gadget.param file and return a dictionary key pair value
def parseGadgetParam(param):
    print "Trying file[",param,"]"
    gparam={}
    try:
        gp=open(param,"r")
    except IOError:
        print "no gadget param"
        return False,gparam

    for line in gp:
        data=line.split()
        if (len(data)>1 and data[0]!='%' and data[0]!='#'):
            gparam[data[0]] = data[1]
            #print data

    return True,gparam

def getHMS(sec,tag):
    days = sec / 86400
    sec -= 86400*days

    hrs = sec / 3600
    sec -= 3600*hrs

    mins = sec / 60
    sec -= 60*mins

    dhms="%s :%dd %dh %dmn %ds"%(tag,days,hrs,mins,sec)
    print dhms
    return dhms

def parseCPU(file,dt,tf,tl):

    print "Processing file[",file,"]"
    a = open(file, "r")

    time=np.array([], dtype=np.float32)
    cpu =np.array([], dtype=np.float32)
    print "cpu.size = ", cpu.size
    first=True
    tlast=0.0
    t=0.0
    cputotlast=0.0
    cputot=0.0
    ncores=0

    for line in a:
        if line.startswith("Step"):     # Step line
            if (tl != -1 and t>tl):     # exit if time last reach
                break
            t = float(line.split()[3].split(",")[0]) # get simu time
            if first:
                ncores=int(line.split()[5])
            cputot=float(a.next().split()[1])        # get from next line cpu time

        if (t>=tf and first):   # time >= time first and first
            tlast= t            # save time
            cputotlast=cputot   # save cpu time
            first=False
        elif (first==False and (tl<0 or t<=tl)): # not first and time in selected range
            diff_t =  (t-tlast)            # diff time current and last
            diff_cpu = (cputot-cputotlast) # diff cput time current and last
            if ( (diff_t)>=dt) :   # reach dt time
                tlast=t
                cputotlast=cputot
                #total=a.readline()
                #print "diff =",t, diff_t,diff_cpu

                idx=time.size
                time.resize(idx+1)
                time[idx]=t
                cpu.resize(idx+1)
                cpu[idx]=diff_cpu
                #time=np.append(time,t)       # save time in numpy array
                #cpu=np.append(cpu,diff_cpu)  # save cputime in numpy array

    a.close()
    print "cpu.size = ", cpu.size
    return time,cpu,ncores

def printHelp(prog,file,dt,tf,tl,out,smooth):
    help= """\

    ----------------------------------------------
    Plot gadget3 cpu time between 2 delta time
    ----------------------------------------------

    Syntaxe : %s  --in <inputfile[:legend]> --dt <delta time> --tf <time first> --tl <time last> --out <image name> --smooth <1|0>

    Notes :
        inputfile  : cpu.txt file from gadget3 simulation [%s]
                     or simulation belonging to unsio database
                     you can give several files separated by ","
                     you can set a legend by giving a name after a ":"
                     cpu.txt:mdf001
        dt         : delta time to compute cpu time [%f]
        tf         : simulation time first [%f]
        tl         : simulation time last [%f]
        out        : output image filename, or plot on screen if blank [%s]
        smooth     : curve fit smoothing.... [%d]

    """
    print help % (prog,file,dt,tf,tl,out,smooth)

if __name__=='__main__':
    main(sys.argv[0:])
