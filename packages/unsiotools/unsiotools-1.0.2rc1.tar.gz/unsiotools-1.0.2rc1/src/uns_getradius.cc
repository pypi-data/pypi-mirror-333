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

// --------------------------------------------------------------
#include "uns.h"
#include "csnaptools.h"
using namespace jclut;

// --------------------------------------------------------------
const char * defv[] = {
  "in=???\n		      UNS input snapshot",
  
  "select=???\n               select particles (range, or component name)",
  "percen=99\n                max percentage of particles to retreive",
  "com=t\n                    center according to com",
  "times=all\n		      selected time",
  "verbose=f\n                verbose on/off"
  "VERSION=1.O\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};

const char * usage="return the radius where max percentage of particles belong";

#define BINS 2000
// --------------------------------------------------------------
// getRadius
float getRadius(int tab[BINS],const float percen,const int nbody)
{
  bool stop=false;
  int cpt=0,total=0;
  while (cpt<BINS && !stop) {
    total += tab[cpt];
    if (total> (nbody*percen/100.)) { // reach maximum
      stop=true;
    } 
    //    std::cerr << total << " " << (nbody*percen/100.) << "\n";
    cpt++;
  }
  return (cpt * 0.5);
}
// --------------------------------------------------------------
// findRadius
void findRadius(uns::CunsIn * uns, const float percen,const bool com, const int nbody)
{
  int maxXY[BINS],maxXZ[BINS];
  
  for (int i=0; i<BINS; i++) {
    maxXY[i] = 0;
    maxXZ[i] = 0;
  }
  bool ok;
  int cnbody;
  float * pos,* mass;
  // get POS from input snapshot
  ok=uns->snapshot->getData("pos" ,&cnbody,&pos);
  if (!ok) {
    std::cerr << "No positions, aborted !\n";
    std::exit(1);
  }
  // get MASS from input snapshot
  ok=uns->snapshot->getData("mass",&cnbody,&mass);

  if (com) CSnaptools::moveToCom<float>(nbody,pos,mass);
  
  for (int i=0; i<nbody; i++) {
    float x=pos[i*3+0];
    float y=pos[i*3+1];
    float z=pos[i*3+2];
    
    // XY plan
    float radiusXY= sqrt(x*x+y*y);
    int index=(int) ((radiusXY*BINS)/1000.);
    index=std::min(index,BINS-1);
    maxXY[index]++;
    // XZ plan
    float radiusXZ= sqrt(x*x+z*z);
    index=(int) ((radiusXZ*BINS)/1000.);
    index=std::min(index,BINS-1);
    maxXZ[index]++;
  }
  
  float rxy,rxz;
  rxy = getRadius(maxXY,percen,nbody);
  rxz = getRadius(maxXZ,percen,nbody);
  if (nbody) {
    float time;
    ok=uns->snapshot->getData("time",&time);
    std::cout << time << " " << rxy << " " << rxz << "\n";
  }
  else
    std::cout << -1 << " " << -1 << " " << -1 << "\n";
}

// --------------------------------------------------------------
// main
int main(int argc, char ** argv )
{
  if (argc) {;}
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  
  /* recuperation des parametres en entree */
  char * simname     = getparam ((char *) "in"     );
  char * select_c    = getparam ((char *) "select" );
  float  percen      = getdparam((char *) "percen" );
  char * select_t    = getparam ((char *) "times"  );
  bool   com         = getbparam((char *) "com"    );
  bool   verbose     = getbparam((char *) "verbose");
  
  
  // instantiate a new uns object
  //s::Cuns * uns = new uns::Cuns(simname,select_c,select_t);
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);
  if (uns->isValid()) {    
    while(uns->snapshot->nextFrame("mx")) {

      int nbody;      
      float time;
      // get the input number of bodies according to the selection
      uns->snapshot->getData("nsel",&nbody);
      // get the simulation time
      uns->snapshot->getData("time",&time);
      std::cerr << "nbody=" << nbody << " time="<< time <<"\n";
      std::cerr << "filename = " << uns->snapshot->getFileName() << "\n";      
      findRadius(uns, percen, com, nbody);
    }
  }
  
  //   finish NEMO
  finiparam();
} 
	      
//
