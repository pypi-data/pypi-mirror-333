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
  "out=???\n                  UNS output snapshot",
  "mass=1.0\n                 default mass value",
  "verbose=f\n                verbose on/off",
  "VERSION=1.O\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};
const char * usage="add mass to an UNS file";
using namespace std;

// ------------------------------------------------------------
// main program
int main(int argc, char ** argv )
{
  if (argc) {;}
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  // get input parameters
  char * simname     = getparam ((char *) "in"      );
  char * outname     = getparam ((char *) "out"     );
  float  dmass       = getdparam((char *) "mass"    );
  bool   verbose     = getbparam((char *) "verbose" );  
  
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,"all","all",verbose);
  // -----------------------------------------------
  // Instantiate a UNS output snapshot (for writing)
  uns::CunsOut * unsout = new uns::CunsOut(outname,uns->snapshot->getInterfaceType(),verbose); 
  
  if (uns->isValid()) { // input file is known by UNS lib        
    while (uns->snapshot->nextFrame()) { // there is a new frame
      
      float * pos, * vel, * mass;
      int n1,n2,n3;
      bool ok1,ok2,ok3;
    
      ok1 = uns->snapshot->getData("all","pos" ,&n1,&pos );
      ok2 = uns->snapshot->getData("all","vel" ,&n2,&vel );
      ok3 = uns->snapshot->getData("all","mass",&n3,&mass);
      
      if (ok1) {
        unsout->snapshot->setData("all","pos",n1,pos);
      }
      if (ok2) {
        unsout->snapshot->setData("all","vel",n2,vel);
      }
      if (!ok3) {
        mass = new float[n1];
        for (int i=0; i<n1;i++) {
          mass[i] = dmass;
        }
      }
      unsout->snapshot->setData("all","mass",n1,mass);
      unsout->snapshot->save();
    }
  }
}
