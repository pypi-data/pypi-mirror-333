#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import os,time
import sys
import argparse,textwrap
import scipy.ndimage as ndi

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# commandLine, parse the command line 
def commandLine():

    # help
    parser = argparse.ArgumentParser(description="Test grid",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--out', help="if blank display on screen, else on given file ",default="",type=str)
    parser.add_argument('--sigma', help="gaussian sigma ",default=6.,type=float)
    parser.add_argument('--noxz',help='no XZ projection',dest="noxz", action="store_true", default=False)
    parser.add_argument('--contour',help='toggle contour display',dest="contour", action="store_true", default=False)
    parser.add_argument('--cmap', help="color map (see mathplotlib colormap)",default="jet")
    parser.add_argument('--verbose',help='verbose mode',dest="verbose", action="store_true", default=False)

     # parse
    args = parser.parse_args()

    # start main funciton
    process(args)

# -----------------------------------------------------
# process, is the core function
def process(args):
    # select matplotlib backend 
    if args.out!= "": # non interactive
        import matplotlib
        matplotlib.use('Agg')

    try:
        fullProcess(out=args.out,sigma=args.sigma,cmap=args.cmap,noxz=args.noxz, contour=args.contour)
    except Exception as x :
        print (x.message,file=sys.stderr)
    except KeyboardInterrupt:
        sys.exit()


#
#
#
def fullProcess(out,sigma,noxz=False, contour=False, cmap="jet",ncols=3):
    import matplotlib.colors
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
        
    t0=time.time()
    sigma_ori=sigma

    # set up grid display
    nrows=2
    if noxz: # no XZ projection
        nrows=1
    ncols=ncols

    # compute aspect ratio
    mydpi=80

    if nrows<ncols:
        inches=19
        #inches = 1920./mydpi # 1920
        w=inches
        h=inches*nrows/ncols
    else: # nrows>ncols
        inches = 1080./mydpi
        w=inches*ncols/nrows
        h=inches

    print("w/h=",w,h,w*mydpi,h*mydpi)

    # specify figure dimensions
    fig=plt.figure(figsize=(w,h),dpi=mydpi)
    #fig=plt.figure(figsize=(w,h))
    print ("FIG DPI =",fig.dpi)
    # create grid
    gs = gridspec.GridSpec(nrows, ncols)#,wspace=0,hspace=0)#height_ratios=h,width_ratios=w)

    for r in range(nrows):
        for c in range(ncols):
            ax = plt.subplot(gs[r, c])        
            ax.set(aspect=1)
            zz=np.random.random((102,102))
            qq=ndi.gaussian_filter(zz,sigma=1.6,order=0)
            im = ax.imshow(qq, norm = matplotlib.colors.LogNorm(), cmap=cmap)
            plt.contour(qq,cmap="Paired")
            ax.set_xticks([])
            ax.set_yticks([])
            if r != nrows-1:
                ax.set_xticks([])
            if  c!=0:
                ax.set_yticks([])
            ax.set_xticklabels("Hey")
            fig.subplots_adjust(hspace=0.,wspace=0.)

    fig.subplots_adjust(hspace=0.,wspace=0.)
    print("Overall time [%.3f] sec"%(time.time()-t0),file=sys.stderr)
    if (out==''):
        plt.show()
    else:
        outfile=out
        print (">> ",outfile)
        plt.savefig(outfile, bbox_inches=0,dpi=fig.dpi)
    plt.close(fig)


# -----------------------------------------------------
# main program
if __name__ == '__main__':
  commandLine()


