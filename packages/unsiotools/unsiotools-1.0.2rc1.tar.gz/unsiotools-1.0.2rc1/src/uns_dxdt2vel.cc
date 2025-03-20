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
#include <nemo.h>
#include <vector>
#include <map>

// ------------------------------------------------------------
// Include file
#include "uns.h"
#include "csnaptools.h"
using namespace std;
using namespace jclut;


const char * defv[] = {  // use `::'string because of 'using namespace std'
                         "in=???\n           uns input file ",
                         "out=???\n          uns output file (gagdet|nemo)",
                         "select=???\n       select input particles to be saved (range or component)",
                         "bits=\n            physicals quantities that you want to save\n",
                         "times=all\n         selected time                   ",
                         "first=f\n           add a trailing number to the first output file",
                         "offset=0.01\n      +/- time offset",
                         "verbose=f\n        verbose mode                    "
                         "VERSION=1.0\n       compiled on <" __DATE__ "> JCL   ",
                         NULL
                      };
const char * usage="Compute velocities from two consecutives displacements";


//------------------------------------------------------------------------------
//                             M   A   I   N
//------------------------------------------------------------------------------
int main(int argc, char ** argv )
{
  // global bariable
  std::string typein,file_structin, file_structout;
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  if (argc) {;} // remove compiler warning :)

  // Get input parameters
  std::string simname   = (getparam ((char *) "in"      ));
  std::string outname   = (getparam ((char *) "out"     ));
  std::string select    = (getparam ((char *) "select"  ));
  std::string bits      = (getparam ((char *) "bits"    ));
  std::string select_t  = (getparam ((char *) "times"   ));
  bool        first     = (getbparam((char *) "first"   ));
  float       offset    = (getdparam((char *) "offset"  ));
  bool        verbose   = (getbparam((char *) "verbose" ));

  bool one_file=false;
  bool stop=false;
  bool special_nemo=false;
  if (outname=="-" || outname==".") {
      special_nemo=true;
    }
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
  uns::CunsOut * unsout=NULL; // out object
  bool first_out=true;

  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * unsin = new uns::CunsIn(simname,select,select_t,verbose);
  if (unsin->isValid()) { // input file is known by UNS lib
      int cpt=0;
      float * pos1, * mass1, * rho1, * hsml1, time1=0;
      float * pos , * mass , * rho , * hsml,  time, * vel = NULL;
      int n1,n2,n3,n4, nbody;
      while(unsin->snapshot->nextFrame(bits)&&!stop) { // there is a new frame
          bool ok1,ok2,ok3,ok4;
          // get the simulation time
          ok1=unsin->snapshot->getData("time",&time);
          // read position
          ok1 = unsin->snapshot->getData("pos"  ,&n1,&pos );
          ok2 = unsin->snapshot->getData("mass" ,&n2,&mass );
          ok3 = unsin->snapshot->getData("rho"  ,&n3,&rho );
          ok4 = unsin->snapshot->getData("hsml" ,&n4,&hsml );



          // allocate memory for velocities vector
          if (cpt==0)  vel = new float[n1*3];

          if (cpt!=0 ){
              assert(n1==nbody); // 2 consecutives snapshots must have same number of particles
              // compute velocities  v = dx/dt
              for (int i=0;i<n1; i++) {
                  for (int j=0;j<3;j++) {
                      vel[i*3+j] = (pos[i*3+j]-pos1[i*3+j])/(time-time1);
                    }
                }
              // OUTPUT operations
              // create an output filename : basename +  integer
              // example : myoutput.0 myoutput.1 ...... etc
              stringstream number("");
              number << cpt;
              std::string out_name=std::string(outname);;
              if (! special_nemo) { // ! standard output && ! "."
                  if (one_file || (cpt==0 && !first)) {
                      out_name=std::string(outname);
                      if (one_file) stop = true; // do not continue
                    } else {
                      stringstream ss("");
                      ss << std::string(outname) << "." << setw(5) << setfill('0') << number.str();
                      //out_name=std::string(outname)+"."+number.str();
                      out_name=ss.str();
                    }
                  // create a new UNS out object
                  unsout = new uns::CunsOut(out_name,"nemo",verbose);
                } else {
                  if (first_out) {
                      first_out = false;
                      // instantiate only once unsout, because outname="-"
                      unsout = new uns::CunsOut(out_name,"nemo",verbose);
                    }
                }
              std::cerr << "output filename=["<<out_name<<"]\n";
              // save time
              std::string comp="all";
              unsout->snapshot->setData("time",time);
              if (ok1)
                unsout->snapshot->setData(comp,"pos",n1,pos,false);
              unsout->snapshot->setData(comp,"vel",n1,vel,false);
              if (ok2)
                unsout->snapshot->setData(comp,"mass",n2,mass,false);
              if (ok3)
                unsout->snapshot->setData(comp,"rho",n3,rho,false);
              if (ok4)
                unsout->snapshot->setData(comp,"hsml",n4,hsml,false);
              // save snapshot
              unsout->snapshot->save();

              if (!special_nemo) {
                  delete unsout; // remove object
                }

            }
          // save current for the next snaphots
          if (ok1) {
              if (cpt==0) pos1 = new float[n1*3];
              memcpy(pos1,pos,sizeof(float)*n1*3);
            }
          if (ok2) {
              if (cpt==0) mass1 = new float[n2];
              memcpy(mass1,mass,sizeof(float)*n2);
            }
          if (ok3) {
              if (cpt==0) rho1 = new float[n3];
              memcpy(rho1,rho,sizeof(float)*n3);
            }
          if (ok4) {
              if (cpt==0) hsml1 = new float[n4];
              memcpy(hsml1,hsml,sizeof(float)*n4);
            }
          //  save nbody
          nbody = n1;
          time1=time; // save time
          cpt++;
        }
    } else {
      std::cerr << "Unknown UNS file format["<<simname<<"]\n";
    }
  delete unsin;
  //   finish NEMO
  finiparam();
}
// ----------- End Of [uns_dxdt2vel.cc] ------------------------------------
