#!/usr/bin/env python
#
# TEST CFalcon class
#
import unsiotools.simulations.cfalcon as falcon
from hashlib import sha1
import numpy as np


def commandLine():
    np.random.seed(666)
    pos=np.float32(np.random.random_sample((300,)))
    mass=np.float32(np.random.random_sample((100,)))

    cf=falcon.CFalcon()

    ok,rho,hsml=cf.getDensity(pos,mass)

    print(ok,np.round(rho,2))
    ref_rho=int('88bb0a5448795aaf2d460e081f2433d19448eb62',16)
    ref_hsml=int('05dfcb44cfd4f88c11b72a7b7e8aaafbb58f551d',16)
    sha1_rho=int(sha1(np.round(rho,2)).hexdigest(),16)
    sha1_hsml=int(sha1(np.round(hsml,3)).hexdigest(),16)

    print("Reference :")
    print("sha1(rho )=",ref_rho)
    print("sha1(hsml)=",ref_hsml)
    print("Computed :")
    print("sha1(rho )=",sha1_rho)
    print("sha1(hsml)=",sha1_hsml)
    print("diff:",ref_rho-sha1_rho," ",ref_hsml-sha1_hsml)
    if ((ref_rho-sha1_rho)==0 and (ref_hsml-sha1_hsml)==0 ):
        print("test OK")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# main
if __name__ == "__main__":
    commandLine()
