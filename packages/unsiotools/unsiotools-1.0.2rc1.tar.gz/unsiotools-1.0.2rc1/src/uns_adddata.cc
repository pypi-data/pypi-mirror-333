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
// ============================================================================
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
  "mass=\n                    default mass value",
  "aux=\n                     default mass value",
  "dens=\n                    default mass value",
  "verbose=f\n                verbose on/off",
  "VERSION=1.O\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};
const char * usage="add data to an UNS file";
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
  bool   verbose     = getbparam((char *) "verbose" );  
  float dmass=0.,daux=0.,ddens=0.;
  bool ismass,isdens,isaux;
  
  if ((ismass=hasvalue((char*)"mass"))) {
    dmass=getdparam((char *) "mass"    );  
  }
  if ((isaux=hasvalue((char*)"aux"))) {
    daux=getdparam((char *) "aux"    );  
  }
  if ((isdens=hasvalue((char*)"dens"))) {
    ddens=getdparam((char *) "dens"    );  
  }
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,"all","all",verbose);
  // -----------------------------------------------
  // Instantiate a UNS output snapshot (for writing)
  uns::CunsOut * unsout = new uns::CunsOut(outname,uns->snapshot->getInterfaceType(),verbose); 
  
  if (uns->isValid()) { // input file is known by UNS lib        
    while (uns->snapshot->nextFrame("mxvXR")) { // there is a new frame
      
      float * pos, * vel, * mass;
      int n1,n2,n3;            
      bool ok;
      
      if (uns->snapshot->getData("all","pos" ,&n1,&pos )) {        
        unsout->snapshot->setData("all","pos",n1,pos);
      }
      
      if (uns->snapshot->getData("all","vel" ,&n2,&vel )) {
        unsout->snapshot->setData("all","vel",n2,vel);
      }
      
      // mass
      ok=uns->snapshot->getData("all","mass",&n3,&mass);
      if (ismass) {
        if (!ok) mass = new float[n1];
        for (int i=0; i<n1;i++) {
          mass[i] = dmass;
        }
        ok = true; // we must save masse
      }
      if (ok) unsout->snapshot->setData("all","mass",n1,mass);     
      // aux
      float * aux;
      ok=uns->snapshot->getData("all","aux",&n3,&aux);
      
      if (isaux) {
        if (!ok) aux = new float[n1];
        for (int i=0; i<n1;i++) {
          aux[i] = daux;
        }
        ok = true; // we must save aux
      }
      if (ok) unsout->snapshot->setData("all","aux",n1,aux);
      // dens
      float * dens;
      ok=uns->snapshot->getData("all","rho",&n3,&dens);
      
      if (isdens) {
        if (!ok) dens = new float[n1];
        for (int i=0; i<n1;i++) {
          dens[i] = ddens;
        }
        ok = true; // we must save dens
      }
      if (ok) {
        for (int i=0; i<n1;i++) {
          dens[i] = fabs(dens[i]);
        }
        unsout->snapshot->setData("all","rho",n1,dens);
      }
      
      // save time
      float time=0.0;
      unsout->snapshot->setData("time",time);
      
      unsout->snapshot->save();
    }
  } else {
    std::cerr << "It's not a vlaid snapshot\n";
  }
}
