
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
#include "uns.h"
#include "cfalcon.h"
#include <nemo.h>

using namespace std; // prevent writing statment like 'std::cerr'
using namespace jclut;
//------------------------------------------------------------------------------
//                             M   A   I   N                                    
//------------------------------------------------------------------------------
// NEMO parameters
const char * defv[] = {  // use `::'string because of 'using namespace std'
  "in=???\n           input file (gadget|nemo)        ",
  "out=???\n          output file                     ",
  "select=???\n       component selected (disk,stars,halo,gas,range,all)",
  "times=all\n         selected time                   ",
  "eps=0.05\n         >=0: softening length\n"
  "                   < 0: use individual fixed softening lengths        ",
  "kernel=1\n         softening kernel                                   ",
  "theta=0.6\n        tolerance parameter at M=M_tot                     ",
  "ncrit=6\n          max # bodies in un-split cells",
  "grav=1\n           Newton's constant of gravity (0-> no self-gravity) ",
  "first=f\n          add a trailing numbering to the first output file",
  "offset=0.01\n      +/- time offset",
  "verbose=f\n        verbose mode                    "
  "VERSION=1.0\n       compiled on <" __DATE__ "> JCL   ",
  NULL
};
const char * usage="Add gravity to an UNS file, the output will be in NEMO format";
//------------------------------------------------------------------------------
// processComponent
// read pos,vel,mass of the components
// if component exist AND it has been selected, then respecting comp's data are
// prepared to be saved
void processComponent(std::string comp, uns::CunsIn * uns,
                      uns::CunsOut * unsout, float eps, float theta, int kernel,
                      int ncrit, float grav)
{
  float * pos, * vel, * mass;
  int n1,n2,n3;
  bool ok1,ok2,ok3;
  
  ok1 = uns->snapshot->getData(comp,"pos" ,&n1,&pos );
  ok2 = uns->snapshot->getData(comp,"vel" ,&n2,&vel );
  ok3 = uns->snapshot->getData(comp,"mass",&n3,&mass);
  if (ok1 && ok2 && ok3) {
    assert(n1==n2);
    assert(n1==n3);
    n2 = 100; // for testing only
    float * acc = new float[n2*3];
    float * pot = new float[n2];
    cfalcon::addGravity2(n1,pos,mass,n2,pos,acc,pot,false,eps,grav,theta,kernel,ncrit);
    std::cerr << "--> "<< std::left << std::setfill('.')<<
        std::setw(8) << comp << ":" << std::setfill(' ')<<
        std::right   << std::setw(10) << n1 <<"\n";
    unsout->snapshot->setData(comp,n2,mass,pos,vel,false);
    unsout->snapshot->setData(comp,"acc",n2,acc,false);
    unsout->snapshot->setData(comp,"pot",n2,pot,false);
    delete [] acc;
    delete [] pot;
  }  
}
//------------------------------------------------------------------------------
// main
int main(int argc, char ** argv )
{
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  if (argc) {;} // remove compiler warning :)
  // Get input parameters
  std::string simname (getparam ((char *) "in"      ));
  std::string outname (getparam ((char *) "out"     ));
  std::string select_c(getparam ((char *) "select"  ));
  std::string select_t(getparam ((char *) "times"    ));

  float eps   = getdparam ((char *) "eps");
  float theta = getdparam ((char *) "theta");
  int   kernel= getiparam ((char *) "kernel");
  int   ncrit = getiparam ((char *) "ncrit");
  float grav  = getdparam ((char *) "grav");
  bool first=getbparam((char *) "first"     );
  float       offset= getdparam((char *) "offset"   );
  bool        verbose =getbparam((char *) "verbose" );
    
  bool one_file=false;
  bool stop=false;

  // in case of an input simulation from the database
  // and with just one time requested,
  // we create a range of time to speedup the searching
  if (select_t!="all" && select_t.find(":",0)==std::string::npos) {
    float match_time;
    stringstream ss;
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
  uns::CunsIn * unsin = new uns::CunsIn(simname,select_c,select_t,verbose);
  int cpt=0;
  if (unsin->isValid()) { // input file is known by UNS lib        
    while(unsin->snapshot->nextFrame("mxv")&&!stop) { // there is a new frame
      //std::string itype = unsin->snapshot->getInterfaceType();

      int nbody;      
      float time;
      // get the input number of bodies according to the selection
      unsin->snapshot->getData("nsel",&nbody);
      // get the simulation time
      unsin->snapshot->getData("time",&time);
      //      
      std::cerr << "nbody=" << nbody << " time="<<time <<"\n";
      if (nbody>0) { // there are particles
        // OUTPUT operations
        // create an output filename : basename +  integer
        // example : myoutput.0 myoutput.1 ...... etc
        stringstream number;
        number << cpt++;
        std::string out_name;
        if (one_file || (cpt==1 && !first)) {
          out_name=std::string(outname);
          if (one_file) stop = true; // do not continue
        } else {
          stringstream ss;
          ss << std::string(outname) << "." << setw(5) << setfill('0') << number.str();
          //out_name=std::string(outname)+"."+number.str();
          out_name=ss.str();
        }
        std::cerr << "output filename=["<<out_name<<"]\n";
        // -----------------------------------------------
        // Instantiate a UNS output snapshot in "nemo" format (for writing)
        uns::CunsOut * unsout = new uns::CunsOut(out_name,"nemo",verbose);      
        // save time
        unsout->snapshot->setData("time",time);
        // processing
        processComponent("all"  ,unsin,unsout,eps,theta,kernel,ncrit,grav); // only all particles selected
        // save snapshot
        unsout->snapshot->save();
        delete unsout; // remove object      
      }
    }
  } else {
    std::cerr << "Unknown UNS file format["<<simname<<"]\n";
  }
  delete unsin;
  //   finish NEMO
  finiparam();
  
}
