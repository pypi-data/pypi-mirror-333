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
#include <iostream>                                   // C++ I/O
#include <fstream>                                    // C++ file I/O
#include <sstream>
#include <cstdio>
#include <cstdlib>
#include <assert.h>
#include <cmath>
#include <nemo.h>
#include <iomanip>

// ------------------------------------------------------------
// Include file
#include "uns.h"
#include "crectify.h"
#include "csnaptools.h"

using namespace jclut;
// ------------------------------------------------------------
// Nemo variable
const char * defv[] = {
  "in=???\n		         UNS input snapshot",
  "out=???\n           NEMO output file                     ",
  "select=???\n        component selected (disk,stars,halo,gas,range,all",
  "rectf=???\n         rectified info file",
  "times=all\n		     selected time",
  "first=f\n           add a trailing numbering to the first output file",
  "verbose=f\n         verbose on/off",
  "VERSION=1.0\n       compiled on <" __DATE__ "> JCL  ",
  NULL,
};
const char * usage="Rectify an UNS snapshot from a rectify file";

using namespace uns_proj;
using namespace std;
//------------------------------------------------------------------------------
//                             M   A   I   N
//------------------------------------------------------------------------------
// main
int main(int argc, char ** argv )
{
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  if (argc) {;} // remove compiler warning :)
  // Get input parameters
  std::string simname  (getparam ((char *) "in"      ));
  std::string outname  (getparam ((char *) "out"     ));
  std::string rectf    (getparam ((char *) "rectf"   ));
  std::string select_c (getparam ((char *) "select"  ));
  std::string select_t (getparam ((char *) "times"    ));
  bool        first    (getbparam((char *) "first"     ));
  bool        verbose = getbparam((char *) "verbose"  );

  bool one_file=false;
  bool stop=false;
  bool special_nemo=false;
  if (outname=="-" || outname==".") special_nemo=true;
  uns::CunsOut * unsout=NULL; // out object
  bool first_out=true;

  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);

  if (uns->isValid()) { // input file is known by UNS lib
    int cpt=0;
    while(uns->snapshot->nextFrame()&&!stop) { // there is a new frame
      std::cerr << "Input file is of type :"<<uns->snapshot->getInterfaceType()<<"\n";
      bool ok;
      int cnbody,nbody;
      float * pos=NULL, * vel=NULL, * mass=NULL, * rho=NULL, * hsml=NULL,time;
      // get the input number of bodies according to the selection
      ok=uns->snapshot->getData("nsel",&nbody);
      assert(ok==true);
      // get the simulation time
      ok=uns->snapshot->getData("time",&time);
      // get POS from input snapshot
      ok=uns->snapshot->getData("pos" ,&cnbody,&pos);
      assert(ok==true);
      // get VEL from input snapshot
      ok=uns->snapshot->getData("vel" ,&cnbody,&vel);
      // get MASS from input snapshot
      ok=uns->snapshot->getData("mass",&cnbody,&mass);
      assert(ok==true);

      // get RHO if exist
      ok=uns->snapshot->getData(select_c,"rho",&cnbody,&rho);

      // get HSML if exist
      ok=uns->snapshot->getData(select_c,"hsml",&cnbody,&hsml);

      std::cerr << "nbody=" << nbody << " time="<<time <<"\n";


      std::cerr << "Snapshot ="<< uns->snapshot->getFileName() << "\n";

      int status;
      ok=CRectify::snapTransform(nbody,time,pos,vel,rectf,status);

      if (ok) {
        stringstream number("");
        number << cpt++;
        std::string out_name=std::string(outname);;
        if (! special_nemo) { // ! standard output && ! "."
          if (one_file || (cpt==1 && !first)) {
            out_name=std::string(outname);
            if (one_file) stop = true; // do not continue
          } else {
            stringstream ss("");
            ss << std::string(outname) << "." << setw(5) << setfill('0') << number.str();
            //out_name=std::string(outname)+"."+number.str();
            out_name=ss.str();
          }
          // create a new UNS out object
          unsout = new uns::CunsOut(out_name,"nemo",verbose);
        } else {
          if (first_out) {
            first_out = false;
            // instantiate only once unsout, because outname="-"
            unsout = new uns::CunsOut(out_name,"nemo",verbose);
          }
        }
        std::cerr << "output filename=["<<out_name<<"]\n";

        unsout->snapshot->setData("time",time);
        unsout->snapshot->setData("pos" ,nbody,pos,false);
        if (vel)
          unsout->snapshot->setData("vel" ,nbody,vel,false);
        unsout->snapshot->setData("mass" ,nbody,mass,false);
        if (rho)
          unsout->snapshot->setData("rho" ,nbody,rho ,false);
        if (hsml)
          unsout->snapshot->setData("hsml",nbody,hsml,false);
        unsout->snapshot->save();
        if (!special_nemo) {
          delete unsout;
        }
      }

    }
  }

}

