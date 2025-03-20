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
#include <cstdio>                    // changed from stdio.h  WD, Sep 2008
#include <cstdlib>                   // changed from stdlib.h WD, Sep 2008
#include <assert.h>
#include <vector>
#include "uns.h"
#define _vectmath_h // put this statement to avoid conflict with C++ vector class
#include <nemo.h>                                     // NEMO basics
#include <io_nemo.h>                                     // NEMO basics
#include "ctimer.h"
#include <algorithm>

using namespace std; // prevent writing statment like 'std::cerr'

//------------------------------------------------------------------------------
//                             M   A   I   N                                    
//------------------------------------------------------------------------------
// NEMO parameters
const char * defv[] = {  // use `::'string because of 'using namespace std'
  "in=???\n           UNS input file          ",
  "out=???\n          Nemo output file                        ",
  "index=???\n        glnemo2 indexes input file     ",
  "select=???\n       component selected (disk,stars,halo,gas,range)",
  "time=all\n         selected time",
  "VERSION=1.0\n       compiled on <" __DATE__ "> JCL  ",
  NULL
};
const char * usage="Save in NEMO format a glnemo indexes list input file";

std::vector <float> vr;    // vector to store positions 
std::vector <float> vv;    // vector to store velocities
std::vector <float> vm;    // vector to store masses    
std::vector <int>   vi;    // vector to store indexes    
using namespace jclut;

// CPartI
// class to store index and id of particles
class CPartI {
public:
  CPartI(int a, int b) {
    itab=a; iid=b;
  }
  int itab,iid;
  static bool mysort(const CPartI& a, const CPartI& b) {
    return a.iid < b.iid;
  }
};
// sort function for "vi" vector
bool sortList(const int i,const int j) 
{ 
  return (i<j); 
}

std::vector <CPartI> pvec;   // vector of particles loaded
std::vector <CPartI> selvec; // vector of particles finally selected
//------------------------------------------------------------------------------
// readIndexList
// read the list of index selected from glnemo2 interface
void readIndexList(std::string listname)
{
  std::ifstream         // File Handler
    fd;               // manipfile file desc
  
  // open file of velocities table
  fd.open(listname.c_str(),std::ios::in);
  if ( ! fd.is_open()) {
    std::cerr <<
      "Unable to open ["<<listname<<"] for input, aborting..\n\n";
    std::exit(1);
  }
  std::string line;
  // Read Header
  getline(fd,line);
  if (line != "#glnemo_index_list") {
    std::cerr <<"Input file ["<<listname<<" is not a know glnemo"
	      <<"index list file....aborting\n";
    std::exit(1);
  }
  // Read 
  while (! fd.eof()) {           // while ! eof
    std::string line;
    getline(fd,line);
    if ( ! fd.eof()) {
      int index;
      std::istringstream ss(line);
      ss >> index; // read index
      vi.push_back(index);
    }
  }
  // sort list
  std::sort(vi.begin(),vi.end(),sortList);
}
//------------------------------------------------------------------------------
// buildList
// build the final list of particles

void buildList()
{
  std::vector<CPartI>::iterator p1=pvec.begin();
  // loop on sorted list of index selected by glnemo2
  for (std::vector<int>::iterator v=vi.begin(); v<vi.end(); v++) {
    bool stop=false;
    // loop on all sorted particles in the snapshot
    for (std::vector<CPartI>::iterator p=p1; p<pvec.end()&&!stop; p++) {
      if ((*p).iid == (*v)) { // found !
        selvec.push_back(*p); // keep the particles
        stop=true; // we can stop to search
        p1=p;      // advance the pointer to the ltest found
                   // bc the 2 lists are sorted, then
                   // it speeds up a lot the processing
      }
    }
  }
}

//------------------------------------------------------------------------------
// nemoOut
void nemoOut(char * select,uns::CunsIn * uns, int nbody,std::string outnemo,float * pos, float *vel, 
	     float * mass)
{

  int nsel;
  float timex, *x,*v,*m;
  int *id;
  CTimer timing,ttot;
  // clear vectors
  selvec.clear();
  if (select) {;}
  pvec.clear();
  // read data
  uns->snapshot->getData("time",&timex);
  uns->snapshot->getData("pos" ,&nsel,&x);
  uns->snapshot->getData("vel" ,&nsel,&v);
  uns->snapshot->getData("mass",&nsel,&m);
  bool ok = uns->snapshot->getData("id",&nsel,&id);
  
  if (!ok) {
    id = new int[nsel];
    std::cerr << "ID field is missing, we create one for you....\n";
    for (int i=0;i<nsel;i++){
      id[i] = i;
    }
  }
  
  float * t = &timex;
  
  // put particles into a vector
  for (int i=0;i<nsel;i++){
    CPartI p(i,id[i]);
    pvec.push_back(p);
  }
  
  timing.restart();
  // sort vector of particles
  std::sort(pvec.begin(),pvec.end(),CPartI::mysort);
  std::cerr << "Sorting  cpu time : "<< timing.cpu() << "\n";
  
  timing.restart();
  // find selected particles in the snapshot
  // create a vector "selvec"
  buildList();
  assert(selvec.size()==vi.size());
  
  std::cerr << "build List  cpu time : "<< timing.cpu() << "\n";
  std::cerr << "nbody=" << nbody << " time="<<timex <<"\n";
    
  timing.restart();
  // store particles according to the selection
  int ii=0;
  for (std::vector<CPartI>::iterator i=selvec.begin(); i<selvec.end(); i++) {
    int index = (*i).itab;
    // mass
    mass[ii] = m[index];
    // pos
    pos[ii*3+0] = x[index*3+0];
    pos[ii*3+1] = x[index*3+1];
    pos[ii*3+2] = x[index*3+2];
    // vel
    vel[ii*3+0] = v[index*3+0];
    vel[ii*3+1] = v[index*3+1];
    vel[ii*3+2] = v[index*3+2];
    ii++;
  }
  int    nn = vi.size(); // number of indexes
  assert(ii==nn);
  int   * n = &nn;
  io_nemo((char *) (outnemo.c_str()),(char *)"info,float,save,n,t,x,v,m",&n,&t,
	  &pos,&vel,&mass);

  std::cerr << "Work done cpu time : "<< ttot.cpu() << "\n";
  std::cerr << "Work done elapsed  : "<< ttot.elapsed() << "\n";
  
}
//------------------------------------------------------------------------------
// main
int main(int argc, char ** argv )
{
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  if (argc) {;} // remove compiler warning :)
  // Get parameters
  std::string simname (getparam((char *) "in"    ));
  std::string outnemo (getparam((char *) "out"   ));
  std::string listname(getparam((char *) "index" ));
  char * select_c  = getparam((char *) "select");
  char * select_t  = getparam((char *) "time"  );

  readIndexList(listname);
  float * pos = new float[3*vi.size()];
  float * vel = new float[3*vi.size()];
  float * mass= new float[  vi.size()];

  //int ok=1;
  // instantiate a new uns object
  //s::Cuns * uns = new uns::Cuns(simname,select_c,select_t);
  uns::CunsIn * uns = new uns::CunsIn(simname.c_str(),select_c,select_t);
  if (uns->isValid()) {
    while(uns->snapshot->nextFrame("mxvI")) {
      int nbody;
      // get the input number of bodies according to the selection
      uns->snapshot->getData("nsel",&nbody);
      nemoOut(select_c,uns,nbody,outnemo,pos,vel,mass);
      
    }
    io_nemo(const_cast<char *>(outnemo.c_str()),(char *)"close");
  } else {
    std::cerr << "Unknown UNS file format["<<simname<<"]\n";
  }

  //   finish NEMO
  finiparam();
}
// ----------- End Of [cell2nemo.cc] --------------------------------------------
