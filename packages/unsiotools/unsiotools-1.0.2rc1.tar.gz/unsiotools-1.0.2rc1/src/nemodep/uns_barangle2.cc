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
#include "csnaptools.h"
#include "crotgal.h"
using namespace std; // prevent writing statment like 'std::cerr'
using namespace jclut;
using namespace uns_proj;

// NEMO parameters
const char * defv[] = {  // use `::'string because of 'using namespace std'
  "in=???\n           input file (gadget|nemo)        ",
  "out=???\n          output file                     ",
  "select=???\n       component selected (disk,stars,halo,gas,range,all)",
  "times=all\n         selected time                   ",
  "verbose=f\n        verbose mode                    "
  "VERSION=1.0\n       compiled on <" __DATE__ "> JCL   ",
  NULL
};
const char * usage="Detect galaxy rotation angle";

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
  bool        verbose = getbparam((char *) "verbose"  );
  
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);
  
  if (uns->isValid()) { // input file is known by UNS lib        
    CRotgal * rotgal1 = new CRotgal(uns);
    rotgal1->loadData();
    rotgal1->process();
    rotgal1->selectPart();
    
    CRotgal * rotgal = new CRotgal(uns);
    while(rotgal->loadData()) { // there is a new frame
      std::cerr << ">> 1\n";
      rotgal->process();
      std::cerr << ">> 2\n";
#if 1      
      rotgal->saveSelectPart(outname,&rotgal1->pvecselect);
#else
      rotgal->saveSelectPart(&rotgal1->pvecselect);      
      rotgal->computeRotation();

      std::cerr << ">> 3\n";      
      // next step
      delete rotgal1;
      rotgal1 = rotgal;
      rotgal1->sortRho();
      rotgal1->selectPart();
      rotgal = new CRotgal(uns);
#endif
    }
  }
  //   finish NEMO
  finiparam();
}    
// ----------- End Of [unsio_demo.cc] ------------------------------------

