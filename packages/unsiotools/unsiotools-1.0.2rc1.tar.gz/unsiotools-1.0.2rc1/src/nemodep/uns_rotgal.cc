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
using namespace std; // prevent writing statment like 'std::cerr'
using namespace jclut;
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
// CPartI
// class to store index and id of particles
class CPartI {
public:
  CPartI(float _rho, int _index) {
    rho=_rho; index=_index;
  }
  static bool mysort(const CPartI& a, const CPartI& b) {
    return a.rho > b.rho;
  }
  int index;
  float rho;  
};


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
  
  // 
  uns::CunsOut * unsout=NULL; // UNS out object

  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);
  
  if (uns->isValid()) { // input file is known by UNS lib        
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
      // Instantiate a density object  
      CDensity * density = new CDensity(nbody,pos,mass);     
      density->compute(0,32,1,8); // estimate density
      // shift to COD
      double cod[6];
      CSnaptools::moveToCod<float>(nbody,pos,vel,mass,density->getRho(),cod,true);
      
      std::vector <CPartI> pvec;
      for (int i=0;i<nbody;i++) {
        CPartI p(density->getRho()[i],i);
        pvec.push_back(p);
      }
      // sort vector of particles
      std::sort(pvec.begin(),pvec.end(),CPartI::mysort);
//      for (int i=0;i<5;i++) {
//        int ii= pvec.at(i).index;
//        std::cerr << pos[ii*3+0] << " " << pos[ii*3+1] << " "<< pos[ii*3+2] << " " << pvec.at(i).rho << " " << density->getRho()[ii] << "\n";
//      }
      //float * pos1 = new float[3*pvec.size()];
      std::vector<float> pos1;
      std::cerr << "pos1 vector capacity ="<< pos1.capacity()<<"\n";
      pos1.reserve(pvec.size()*3);
      std::cerr << "pos1 vector capacity ="<< pos1.capacity()<<"\n";
      std::cerr << "pos1 vector maxsize  ="<< pos1.max_size()<<"\n";
      std::cerr << "Pos1 vector size="<<pos1.size()<<"\n";
      //float * vel1 = new float[3*pvec.size()];
      float * mass1= new float[  pvec.size()];
      float * rho1 = new float[  pvec.size()];
      float * hsml1= new float[  pvec.size()];
      int cpt=0;
      for (int i=0.2*nbody; i<0.25*nbody; i++) {
        int ii= pvec.at(i).index;
#if 0        
        pos1[cpt*3+0] =pos[ii*3+0];
        pos1[cpt*3+1] =pos[ii*3+1];
        pos1[cpt*3+2] =pos[ii*3+2];
#endif
        pos1.push_back(pos[ii*3+0]);
        pos1.push_back(pos[ii*3+1]);
        pos1.push_back(pos[ii*3+2]);
        mass1[cpt] = mass[ii];
        rho1[cpt]  = density->getRho()[ii];
        hsml1[cpt] = density->getHsml()[ii];
        cpt++;
      }
      unsout = new uns::CunsOut(outname,"nemo",verbose); 
      unsout->snapshot->setData("time",time);
      unsout->snapshot->setData("pos" ,pos1.size()/3,&pos1[0],false);
      unsout->snapshot->setData("mass" ,cpt,mass1,false);
      unsout->snapshot->setData("rho" ,cpt,rho1 ,false);
      unsout->snapshot->setData("hsml",cpt,hsml1,false);
      unsout->snapshot->save();
    }
  }
  //   finish NEMO
  finiparam();
}    
// ----------- End Of [unsio_demo.cc] ------------------------------------
