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
#include <cstdio>
#include <iomanip>
#include <vector>
#include "uns.h"
#include <nemo.h>       
#include "cfalcon.h"
#include "csnaptools.h"
#include "cfitsellipse.h"
using namespace std; // prevent writing statment like 'std::cerr'
using namespace jclut;
using namespace uns_proj;
// NEMO parameters
const char * defv[] = {  // use `::'string because of 'using namespace std'
  "in=???\n           input file (gadget|nemo)        ",
  "select=???\n       component selected (disk,stars,halo,gas,range,all)",
  "mesh=300\n         #mesh for the grid",
  "rmax=20.0\n        half size of the grid",
  "com=t\n            center according to com",
  "rho=f\n            compute density",
  "out=\n             output file                     ",
  "times=all\n        selected time                   ",
  "verbose=f\n        verbose mode                    "
  "VERSION=1.0\n      compiled on <" __DATE__ "> JCL   ",
  NULL
};
const char * usage="Fit ellipse on simulation data";

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
  std::string select_c (getparam ((char *) "select"  ));
  std::string select_t (getparam ((char *) "times"    ));
  int mesh   = getiparam ((char *) "mesh"     );
  float rmax= getdparam ((char *) "rmax"    );
  bool   com         = getbparam((char *) "com"     );
  bool   rho         = getbparam((char *) "rho"     );
  
  bool        verbose = getbparam((char *) "verbose"  );
 
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);
  
  if (uns->isValid()) { // input file is known by UNS lib        
    
    // ellipse object
    CFitsEllipse * ellipse = new CFitsEllipse(0,1,mesh,rmax);
    
    while(uns->snapshot->nextFrame()) { // there is a new frame
      std::cerr << "Input file is of type :"<<uns->snapshot->getInterfaceType()<<"\n";
      bool ok;
      int cnbody,nbody;      
      float * pos, * vel, * mass, time;
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
      std::cerr << "nbody=" << nbody << " time="<<time <<"\n";
      if (com) CSnaptools::moveToCom<float>(nbody,pos,mass); // COM centering
      if (rho) {
        // Instantiate a density object  
        CDensity * density = new CDensity(nbody,pos,mass);     
        density->compute(0,32,1,8); // estimate density     
        
        // build grid
        ellipse->buildGrid(nbody,pos,density->getRho());
      } else {
        ellipse->buildGrid(nbody,pos,mass);
      }
      ellipse->displayGrid();
      ellipse->saveGrid(outname);
    }
  }
}
