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

// ------------------------------------------------------------
// Nemo variable
const char * defv[] = {
  "in=???\n		      UNS input snapshot",  
  "time=???\n		      selected time",
  "offset=0.01\n              +/- time offset",
  "verbose=f\n                verbose on/off",
  "VERSION=1.O\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};
const char * usage="Return the minimal range time + the filename which match the given time";
using namespace std;

// ------------------------------------------------------------
// main program
int main(int argc, char ** argv )
{
  if (argc) {;}
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  // get input parameters
  std::string simname(getparam ((char *) "in"      ));
  float match_time= getdparam ((char *) "time"   );
  float   offset   = getdparam((char *) "offset"   );
  bool   verbose     = getbparam((char *) "verbose" );  

  bool stop=false;
    
  float time_last=0.0;
  int cpt=0;
  
  stringstream ss("");
  ss << match_time-offset <<":"<<match_time+offset;
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,"all",ss.str(),verbose);
  
  if (uns->isValid()) { // input file is known by UNS lib        
    while(uns->snapshot->nextFrame()&& !stop) { // there is a new frame
      float time;
      // get the simulation time
      uns->snapshot->getData("time",&time);
      std::cerr << "time = " << time << "\n";
      if (time >= match_time) {
        stop=true;
        if (cpt>0) {
          std::stringstream ss("");
          ss << (time+time_last)/2. << ":" << time;
          std::cout << ss.str() << " " << uns->snapshot->getFileName();
        } else {
          std::cout << time << " " << uns->snapshot->getFileName();
        }          
      }      
      //
      cpt++;
      time_last=time;
    }
  } else {
    std::cerr << "It's not a valid UNS simulation\n";
  }

  delete uns;
  //   finish NEMO
  finiparam();
}
// ------------------------------------------------------------

