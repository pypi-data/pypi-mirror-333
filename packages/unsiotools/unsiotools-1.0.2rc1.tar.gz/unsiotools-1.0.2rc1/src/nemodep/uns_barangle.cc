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
#include <nemo.h>
#include "uns.h"
//#include "cfalcon.h"
//#include "csnaptools.h"
#include "cbar.h"
using namespace std; // prevent writing statment like 'std::cerr'
////using namespace jclut;
//using namespace uns_proj;

// NEMO parameters
const char * defv[] = {  // use `::'string because of 'using namespace std'
  "in=???\n           input file (gadget|nemo)        ",
  "out=???\n          angle output file               ",
  "select=???\n       component selected (disk,stars,halo,gas,range,all)",
  "dmin=70\n          density min used",
  "dmax=95\n          density max used",
  "rotate=0\n         0: no rotate, 1: rotate along X, 2: rotate along Y",
  "first=f\n           add a trailing numbering to the first output file",
  "offset=0.01\n      +/- time offset",
  "times=all\n         selected time                   ",
  "mvcod=t\n           move to COD\n",
  "outnemo=\n         nemo output file               ",
  "verbose=f\n        verbose mode                    "
  "VERSION=1.0\n       compiled on <" __DATE__ "> JCL   ",
  NULL
};
const char * usage="Detect galaxy rotation angle";

ofstream anglefile;

//------------------------------------------------------------------------------
//
void buildHeader()
{
  
}

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
  std::string outnemo  (getparam ((char *) "outnemo"     ));
  std::string select_c (getparam ((char *) "select"  ));
  std::string select_t (getparam ((char *) "times"    ));
  float dmin =          getdparam((char *) "dmin"    );
  float dmax =          getdparam((char *) "dmax"    );
  int   rot  =          getiparam((char *) "rotate"    );
  bool first=getbparam((char *) "first"     );
  float       offset= getdparam((char *) "offset"   );
  bool        verbose = getbparam((char *) "verbose"  );
  bool        mvcod=getbparam((char *) "mvcod");
  //
  bool one_file=false;
  bool special_nemo=false;
  if (outname=="-" || outname==".") special_nemo=true;
  // in case of an input simulation from the database
  // and with just one time requested,
  // we create a range of time to speedup the searching
  if (select_t!="all" && select_t.find(":",0)==std::string::npos) {
    float match_time;
    stringstream ss("");
    ss << select_t;
    ss >> match_time; // convert string time to float
    ss.str(std::string()); // empty stringstream
    ss.clear();            // empty stringstream (mandatory after >>)
    ss << match_time-offset<<":"<<match_time+offset;
    select_t = ss.str();
    one_file=true;
    std::cerr << "Modified selected time =["<<select_t<<"]\n";
  }
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);

  // create header file
  anglefile.open(outname.c_str(), ios::out);
  if ( ! anglefile.is_open()) {  
    cerr << "Unable to open file for writing :["<<outname<<"], aborting\n";
    std::exit(1);
  }
  anglefile << simname << " " << select_c << "\n";
  anglefile << dmin << " " << dmax << "\n";
  int cpt=0;
  if (uns->isValid()) { // input file is known by UNS lib        
    while(uns->snapshot->nextFrame("mxvRHIX")) {
      bool ok;
      int nbody;      
      float time;
      // get the input number of bodies according to the selection
      ok=uns->snapshot->getData("nsel",&nbody);
      // get the simulation time
      ok=uns->snapshot->getData("time",&time);
      std::cerr << "nbody=" << nbody << " time="<< time <<"\n";
      std::cerr << "filename = " << uns->snapshot->getFileName() << "\n";   
      float * pos, * vel, * mass, * rho=NULL, * hsml=NULL;
      int * id=NULL;
      // get POS from input snapshot
      ok=uns->snapshot->getData("pos" ,&nbody,&pos);
      assert(ok==true);
      // get VEL from input snapshot
      ok=uns->snapshot->getData("vel" ,&nbody,&vel);
      // get MASS from input snapshot
      ok=uns->snapshot->getData("mass",&nbody,&mass);
      assert(ok==true);
      // !!!!! we must use temporary [nbody] variable
      // !!!!! for nbody when trying to get rho | hsml
      int nb; // temporary nbody variable
      // get rho from input snapshot
      ok=uns->snapshot->getData(select_c,"rho" ,&nb,&rho);
      ok=uns->snapshot->getData(select_c,"hsml" ,&nb,&hsml);
      ok=uns->snapshot->getData(select_c,"id" ,&nb,&id);

      uns_proj::CBar * bar = new uns_proj::CBar(nbody,pos, vel,mass,rho,hsml,id);
            
#if 1
      float phi;
      if (dmin<0 || dmax<0)
        phi=bar->computeAngle(mvcod);
      else
        phi=bar->computeAngle(dmin/100.,dmax/100.,mvcod);
      
      //bar->saveAllRho(outname);
      std::cerr << "range ["<<dmin<<":"<<dmax<<"] Phi="<< 
          phi <<" radian, "<<phi*180/acos(-1.)<<" degree\n"; 
      std::cerr <<"result="<< scientific << left << setw(11);
      std::cerr << time << " " << phi << " " << phi*180/acos(-1.) << " " << uns->snapshot->getFileName()<< "\n";
      anglefile << time << " " << phi << " " << phi*180/acos(-1.) << " " << uns->snapshot->getFileName()<< "\n";
      if (outnemo != "") {
        if (rot==1) {
          bar->rotateOnX(phi);
        }
        if (rot==2) {
          bar->rotateOnY(phi);
        }       
        // OUTPUT operations
        // create an output filename : basename +  integer
        // example : myoutput.0 myoutput.1 ...... etc
        stringstream number("");
        number << cpt++;
        std::string out_name=std::string(outnemo);;
        if (! special_nemo) { // ! standard output && ! "."
          if (one_file || (cpt==1 && !first)) {
            out_name=std::string(outnemo);
          } else {
            stringstream ss("");
            ss << std::string(outnemo) << "." << setw(5) << setfill('0') << number.str();
            //out_name=std::string(outname)+"."+number.str();
            out_name=ss.str();
          }
        } 
        std::cerr << "output filename=["<<out_name<<"]\n";        
        bar->save(out_name,time,true);        
      }
#else
      // allow to display every rotation angle from
      // 0 to 100 % of density (rho)
      for (int i=0;i<100;i++) {
        float phi=bar->computeAngle(i/100.,(i+1)/100.,true);
        //bar->saveAllRho(outname);
        std::cerr << "range ["<<i<<":"<<i+1<<"] Phi="<< 
            phi <<" radian, "<<phi*180/acos(-1.)<<" degree\n";          
      }
#endif
      // garbage collecting  
      delete bar;
    }
  }
  anglefile.close();
  //   finish NEMO
  finiparam();
}    
// ----------- End Of [unsio_demo.cc] ------------------------------------

