// ============================================================================
// Copyright Jean-Charles LAMBERT - 2008-2025                                       
// e-mail:   Jean-Charles.Lambert@lam.fr                                      
// address:  Aix Marseille Universite, CNRS, LAM 
//           Laboratoire d'Astrophysique de Marseille                          
//           Pole de l'Etoile, site de Chateau-Gombert                         
//           38, rue Frederic Joliot-Curie                                     
//           13388 Marseille cedex 13 France                                   
//           CNRS UMR 7326                                       
// ============================================================================
#include <iostream>                                   // C++ I/O     
#include <fstream>                                    // C++ file I/O
#include <sstream>
#include <cstdio>                    // changed from stdio.h  WD, Sep 2008
#include <cstdlib>                   // changed from stdlib.h WD, Sep 2008
#include <assert.h>

#include "uns.h"
#define DEBUG 0
#include "unsdebug.h"

#define _vectmath_h // put this statement to avoid conflict with C++ vector class
extern "C" {
#include <nemo.h>                                     // NEMO basics
  int io_nemo(const char *, const char *,...);
}

using namespace std; // prevent writing statment like 'std::cerr'

//------------------------------------------------------------------------------
//                             M   A   I   N                                    
//------------------------------------------------------------------------------
// NEMO parameters
const char * defv[] = {  // use `::'string because of 'using namespace std'
  "in=???\n           input file (gadget|nemo)          ",
  "select=???\n       component selected (disk,stars,halo,gas,range)",
  "time=all\n         selected time",
  "VERSION=1.0\n       compiled on <" __DATE__ "> JCL  ",
  NULL
};
const char * usage="test uns library";

//------------------------------------------------------------------------------
// main
int main(int argc, char ** argv )
{
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  if (argc) {;} // remove compiler warning :)
  // Get parameters
  char * simname   = getparam((char *) "in"    );
  char * select_c  = getparam((char *) "select");
  char * select_t  = getparam((char *) "time"  );
  
  // instantiate a new uns object
  //s::Cuns * uns = new uns::Cuns(simname,select_c,select_t);
  uns::CunsIn * unsi = new uns::CunsIn(simname,select_c,select_t);
  if (unsi->isValid()) {
    while(unsi->snapshot->nextFrame()) {
      int nbody;
      float time;
      // get the input number of bodies according to the selection
      unsi->snapshot->getData("nsel",&nbody);
      // get the simulation time
      unsi->snapshot->getData("time",&time);
      std::cerr << "nbody=" << nbody << " time="<<time <<"\n";
      float tcod[7];
      
      //int status=uns->snapshot->getCod(std::string("all"),time,tcod);
      int status=unsi->snapshot->getCod(select_c,time,tcod);
      if (status == 1) {
        for (int i=0; i<7;i++) {
          std::cerr << tcod[i] << "\t";
        }
        std::cerr << "\n";
      }
    }
  }
  else {
    std::cerr << "Unknown UNS file format["<<simname<<"]\n";
  }
  //   finish NEMO
  finiparam();
}
// ----------- End Of [stress_io_nemo.cc] ------------------------------------
