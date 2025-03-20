// ============================================================================
// Copyright Jean-Charles LAMBERT - 2008-2025
//           Centre de donneeS Astrophysiques de Marseille (CeSAM)              
// e-mail:   Jean-Charles.Lambert@lam.fr                                      
// address:  Aix Marseille Universite, CNRS, LAM 
//           Laboratoire d'Astrophysique de Marseille                          
//           Pole de l'Etoile, site de Chateau-Gombert                         
//           38, rue Frederic Joliot-Curie                                     
//           13388 Marseille cedex 13 France                                   
//           CNRS U.M.R 7326                                                   
// ============================================================================

/* 
	@author Jean-Charles Lambert <Jean-Charles.Lambert@lam.fr>
 */
#define _FILE_OFFSET_BITS 64

#include <cstdio>
#include <assert.h>
#define _vectmath_h // put this statement to avoid conflict with C++ vector class
namespace nos { // use namespace to avoid conflict between
// typedef char * string from stdinc.h
// and using std::string from ccfits.h
typedef char * string;
#include "getparam.h"
}
#include <CCfits>
#include <uns.h>

#include <cmath>
#include <limits>

// The library is enclosed in a namespace.

using namespace CCfits;
// -------------`-----------------------------------------------
// Nemo variable
const char * defv[] = {  // use `::'string because of 'using namespace std'
                         "in=???\n           Fits input file ",
                         "out=???\n          output file",
                         "type=nemo\n        nemo|gadget2",
                         "dmin=\n            minimum data value",
                         "dmax=\n            maximum data value",
                         "zmin=\n            #z plane min",
                         "zmax=\n            #z plane max",
                         "verbose=f\n        verbose mode",
                         "VERSION=1.0\n      compiled on <" __DATE__ "> JCL   ",
                         NULL
                      };
const char * usage="Simple converter fits to uns compatible output format";

int readImage(std::string in, std::string out, std::string type);
float dmin = std::numeric_limits<float>::min();
float dmax = std::numeric_limits<float>::max();
int   zmin = std::numeric_limits<int>::min();
int   zmax = std::numeric_limits<int>::max();

int main(int argc, char ** argv )
{
    if (argc) {;} // remove compiler warning :)
    //   start  NEMO
    nos::initparam(const_cast<char**>(argv),const_cast<char**>(defv));
    // Get input parameters
    std::string simname (nos::getparam ((char *) "in"      ));
    std::string outname (nos::getparam ((char *) "out"     ));
    if (nos::hasvalue((char *) "zmin")) {
        zmin=(nos::getiparam ((char *) "zmin"     ));
    }
    if (nos::hasvalue((char *) "zmax")) {
        zmax=(nos::getiparam ((char *) "zmax"     ));
    }
    if (nos::hasvalue((char *) "dmin")) {
        dmin=(nos::getdparam ((char *) "dmin"     ));
    }
    if (nos::hasvalue((char *) "dmax")) {
        dmax=(nos::getdparam ((char *) "dmax"     ));
    }
    std::string typeout   = (nos::getparam ((char *) "type"    ));
    bool        verbose   = (nos::getbparam((char *) "verbose" ));

    if (verbose)
        FITS::setVerboseMode(true);
    else
        FITS::setVerboseMode(false);

    try  {
        if (!readImage(simname,outname,typeout))
            std::cerr << " readImage() ok \n";
    }
    catch (FitsException&) {
        // will catch all exceptions thrown by CCfits, including errors
        // found by cfitsio (status != 0)
        std::cerr << " Fits Exception Thrown by test function \n";
    }
    return 0;

    nos::finiparam();
}

int readImage(std::string in, std::string out, std::string type)
{
    //        std::auto_ptr<FITS> pInfile(new FITS("/windows7/JDL/ngc6503.fits",Read,true));
    std::auto_ptr<FITS> pInfile(new FITS(in,Read,false));

    //PHDU& image = pInfile->pHDU();
    //ExtHDU& image = pInfile->extension(0);
    HDU * image;// = &pInfile->extension(1);

    std::cerr << " Begin \n";
    std::valarray<float>  contents;
#if 1
    try {
        image =  &pInfile->pHDU();
        std::cerr << "There is a pHDU\n";
        std::cerr << "#axis ="<<image->axes() << std::endl;
        if (image->axes() < 2) {
            throw CCfits::FITS::OperationNotSupported("",true);
        } else {
            //(pInfile->pHDU()).read(contents);
            ((PHDU *) image)->read(contents);
        }


    } catch (FitsException& e) {
        image  = &pInfile->extension(1);
        std::cerr << "There is an extension\n";
        std::cerr << "#axis ="<<image->axes() << std::endl;
        //(pInfile->extension(1)).read(contents);
        ((ExtHDU *) image)->read(contents);

    }
#else
    try {
        image  = &pInfile->extension(1);
        std::cerr << "There is an extension\n";
        std::cerr << "#axis ="<<image->axes() << std::endl;
        //(pInfile->extension(1)).read(contents);
        ((ExtHDU *) image)->read(contents);

        throw CCfits::FITS::OperationNotSupported("",true);

    } catch (FitsException& e) {
        image =  &pInfile->pHDU();
        std::cerr << "There is a pHDU\n";
        std::cerr << "#axis ="<<image->axes() << std::endl;
        //(pInfile->pHDU()).read(contents);
        ((PHDU *) image)->read(contents);
    }
#endif
    // read all user-specifed, coordinate, and checksum keys in the image
    image->readAllKeys();

    std::cerr << "#axis ="<<image->axes() << std::endl;

    
    //image->read(contents);

    std::cerr << "#axis ="<<image->axes() << std::endl;
    for (int i=0;i<image->axes();i++) {
        std::cerr << "axis["<<i<<"]="<<image->axis(i)<<"\n";
    }
    // this doesn't print the data, just header info.
    //std::cerr << *image << std::endl;

    long ax(image->axis(0));
    long ay(image->axis(1));
    long az;
    if (image->axes()>=3) {
        az=(image->axis(2));
    } else {
        az=0;
    }

    std::vector <float> pos,hsml,rho;
    long nan=0;
    std::cerr << "value = " << contents.size() << "\n";
    for (unsigned long i=0; i<contents.size(); i++) {

        if (std::isfinite(contents[i]) && contents[i]>=dmin && contents[i]<=dmax) {

            long z_i=int(i/(ax*ay)); // current Z plane
            assert(z_i<=az);
            if (z_i>=zmin && z_i<=zmax) { // inside Z selection
                long nxy=i-z_i*(ax*ay);// #pixels (x/y) of the latest Z plane
                long y_i=int(nxy/ax);  // current Y coordinate
                assert(y_i<ay);
                long x_i=nxy-(y_i*ax); // current X coordinate
                assert(z_i<=az);
                pos.push_back(x_i*1.0);
                pos.push_back(y_i*1.0);
                pos.push_back(z_i*1.0);
                rho.push_back(contents[i]);
                hsml.push_back(0.8);
            }
            //std::cerr << x_i << " " << y_i << " " << z_i << " " << contents[i] << "\n";
        } else { // NAN or INF
            nan++;
        }
    }
    std::cerr << " #NAN values = "<< nan << "\n";
    std::cerr << " #bodies valids = "<< rho.size() << "\n";
    uns::CunsOut * unsout = new uns::CunsOut(out,type,false);
    std::string comp="gas";
    if (type=="nemo") comp="all";
    unsout->snapshot->setData("time",0.0);
    unsout->snapshot->setData(comp,"pos",pos.size()/3,&pos[0],false);
    unsout->snapshot->setData(comp,"rho",rho.size(),&rho[0],false);
    unsout->snapshot->setData(comp,"hsml",hsml.size(),&hsml[0],false);
    // save snapshot
    unsout->snapshot->save();

    return 0;

}
