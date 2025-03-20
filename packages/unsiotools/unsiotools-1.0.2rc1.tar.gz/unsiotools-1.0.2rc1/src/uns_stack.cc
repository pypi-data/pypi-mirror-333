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
#include <cstdio>  
#include <cstdlib> 
#include <assert.h>
#include <cmath>
#include <nemo.h>
#include <iomanip>
#include <vector>
#include <cvecutils.h>

// ------------------------------------------------------------
// Include file
#include "uns.h"
#include "csnaptools.h"

// class used to store global
// information in case of COM
template <class T> class CSnapshot {
public:
  CSnapshot() {}
  std::vector<T> pos,mass,vel;
  std::map<std::string, std::vector<int> > range;
};

// ------------------------------------------------------------
// Nemo variable
const char * defv[] = {
  "in1=???\n		      UNS input snapshot",  
  "in2=???\n		      UNS input snapshot",
  "out=???\n	              output snapshot",
  "deltar=0.0,0.0,0.0\n	      position of in1 w.r.t. in2",
  "deltav=0.0,0.0,0.0\n	      velocity of in1 w.r.t. in2",
  "shift=1\n                  Shift over 1st or 2nd one?",
  "zerocm=f\n                 Centering On Mass after stacking?",
  "float=t\n                  t=float, f=double",
  "time=0.0\n                 set output snapshot time",
  "verbose=f\n                verbose on/off",
  "VERSION=2.O\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};
const char * usage="stack two UNS systems on top of each other";
using namespace std;
using namespace uns;
using namespace jclut;
bool com;
int shift;
std::vector<double> deltar;
std::vector<double> deltav;


// ------------------------------------------------------------
// addArray
template <class T>
void shiftObject(T * data, const int n, std::vector<double> &_delta)
{
  std::vector<T> delta(_delta.begin(),_delta.end());

  for (int i=0; i<n;i++) {
    vectutils::addv(&data[i*3],&data[i*3],&delta[0]);
  }
}

// ------------------------------------------------------------
// addArray
template <class T>
bool addArray(CSnapshot<T> &mysnap,std::string comp, std::string name, int dim, uns::CunsIn2<T> * uns1,uns::CunsIn2<T> * uns2, uns::CunsOut2<T> * unsout, bool verbose)
{
  bool status=false;
  T * d=NULL, * d1=NULL, * d2=NULL;
  int n,n1=0,n2=0;
  bool ok1 = uns1->snapshot->getData(comp,name ,&n1,&d1);
  bool ok2 = uns2->snapshot->getData(comp,name ,&n2,&d2);
  n=0;
  if (ok1 || ok2) {
    std::cerr << "comp["<<comp<<"] name["<<name<<"]\n";
    std::cerr << "n1="<<n1<<" n2="<<n2 << "\n";
    n = n1+n2;
    assert(n>0);
    if (shift==1) {
      if (name=="pos") shiftObject(d1,n1,deltar);
      if (name=="vel") shiftObject(d1,n1,deltav);
    } else {
      if (name=="pos") shiftObject(d2,n2,deltar);
      if (name=="vel") shiftObject(d2,n2,deltav);
    }
    if (!com || (name!="pos" && name !="vel" && name !="mass")) {
      // COM not requested
      // or name != pos|vel|mass
      d = new T[n*dim];
      if (verbose)
        std::cerr << "* INFO * addArray getData["<<comp<<","<<name<<"] n1="<<n1<<" n2="<<n2<<"\n";
      memcpy(d         ,d1,sizeof(T)*n1*dim); // copy first array
      memcpy(d+(n1*dim),d2,sizeof(T)*n2*dim); // copy second array
      // prepare data to be saved
      unsout->snapshot->setData(comp,name,n,d,false);
      delete [] d;
    }
    else {
      // COM requested
      // we accumulate for all components pos,vel,mass
      // it's needed to compute later COM
      if (name=="pos") {
        unsigned int ss=mysnap.pos.size(); // #elements in vector
        mysnap.pos.resize(ss+n*dim);       // expand up to fit 2 arrays
        memcpy(&mysnap.pos[ss],d1,sizeof(T)*n1*dim); // copy first array
        memcpy(&mysnap.pos[ss+n1*dim],d2,sizeof(T)*n2*dim); // copy second array
        mysnap.range[comp+":pos"].push_back(ss);
        mysnap.range[comp+":pos"].push_back(mysnap.pos.size()-1);
      }
      if (name=="vel") {
        unsigned int ss=mysnap.vel.size(); // #elements in vector
        mysnap.vel.resize(ss+n*dim);       // expand up to fit 2 arrays
        memcpy(&mysnap.vel[ss],d1,sizeof(T)*n1*dim); // copy first array
        memcpy(&mysnap.vel[ss+n1*dim],d2,sizeof(T)*n2*dim); // copy second array
        mysnap.range[comp+":vel"].push_back(ss);
        mysnap.range[comp+":vel"].push_back(mysnap.vel.size()-1);
      }
      if (name=="mass") {
        unsigned int ss=mysnap.mass.size(); // #elements in vector
        mysnap.mass.resize(ss+n*dim);       // expand up to fit 2 arrays
        memcpy(&mysnap.mass[ss],d1,sizeof(T)*n1*dim); // copy first array
        memcpy(&mysnap.mass[ss+n1*dim],d2,sizeof(T)*n2*dim); // copy second array
        mysnap.range[comp+":mass"].push_back(ss);
        mysnap.range[comp+":mass"].push_back(mysnap.mass.size()-1);
      }
    }
    status=true;
  } else {
    if (ok1 | ok2) {
      if (!ok1)
        std::cerr << "* ERROR * addArray on file<"<<uns1->snapshot->getFileName()<<">\n"
            "getData["<<comp<<","<<name<<"] failed, aborting....\n";
      if (!ok2)
        std::cerr << "* ERROR * addArray on file<"<<uns2->snapshot->getFileName()<<">\n"
            "getData["<<comp<<","<<name<<"] failed, aborting....\n";
      std::exit(1);
    } else {
      if (verbose)
        std::cerr << "* WARNING * addArray getData["<<comp<<","<<name<<"] failed, skipping...\n";
    }
  }
  return status;
}
// ------------------------------------------------------------
// addComponent
template <class T>
void addComponent(CSnapshot<T> &mysnap,std::string comp, uns::CunsIn2<T> * uns1,uns::CunsIn2<T> * uns2,
                  uns::CunsOut2<T> * unsout, bool verbose)
{
  addArray(mysnap,comp,"pos" ,3,uns1,uns2,unsout,verbose);
  addArray(mysnap,comp,"vel" ,3,uns1,uns2,unsout,verbose);
  addArray(mysnap,comp,"mass",1,uns1,uns2,unsout,verbose);
  addArray(mysnap,comp,"pot",1,uns1,uns2,unsout,verbose);
  addArray(mysnap,comp,"acc",3,uns1,uns2,unsout,verbose);
  if (comp == "gas") {
    addArray(mysnap,comp,"u"    ,1,uns1,uns2,unsout,verbose);
    addArray(mysnap,comp,"hsml" ,1,uns1,uns2,unsout,verbose);
    addArray(mysnap,comp,"rho"  ,1,uns1,uns2,unsout,verbose);
    addArray(mysnap,comp,"temp"  ,1,uns1,uns2,unsout,verbose);
    addArray(mysnap,comp,"metal" ,1,uns1,uns2,unsout,verbose);
  }
  if (comp == "stars") {
    addArray(mysnap,comp,"age"    ,1,uns1,uns2,unsout,verbose);
    addArray(mysnap,comp,"metal" ,1,uns1,uns2,unsout,verbose);
  }

}
// ------------------------------------------------------------
// process
template <class T>
void process(uns::CunsIn2<T> * uns1,uns::CunsIn2<T> * uns2, char * out, bool verbose, T otime)
{
  // object to store merged pos,vel.mass
  CSnapshot<T> mysnap;

  // -----------------------------------------------
  // Instantiate a UNS output snapshot (for writing)
  uns::CunsOut2<T> * unsout = new uns::CunsOut2<T>(out,uns1->snapshot->getInterfaceType(),verbose);
  
  if (uns1->snapshot->getInterfaceType() == "Nemo") {
    addComponent(mysnap,"all",uns1,uns2,unsout,verbose);
    addArray(mysnap,"all","hsml" ,1,uns1,uns2,unsout,verbose);
    addArray(mysnap,"all","rho"  ,1,uns1,uns2,unsout,verbose);
  }
  else {
    addComponent(mysnap,"gas"  ,uns1,uns2,unsout,verbose);
    addComponent(mysnap,"halo" ,uns1,uns2,unsout,verbose);
    addComponent(mysnap,"disk" ,uns1,uns2,unsout,verbose);
    addComponent(mysnap,"bulge",uns1,uns2,unsout,verbose);
    addComponent(mysnap,"stars",uns1,uns2,unsout,verbose);
    addComponent(mysnap,"bndry",uns1,uns2,unsout,verbose);
  }
  if (com) {
    // move to COM
    if (mysnap.pos.size()>0) {
      assert(mysnap.mass.size() == mysnap.pos.size()/3.);
      jclut::CSnaptools::moveToCom(mysnap.mass.size(),&mysnap.pos[0],&mysnap.mass[0]);
    }
    if (mysnap.vel.size()>0) {
      assert(mysnap.mass.size() == mysnap.vel.size()/3.);
      jclut::CSnaptools::moveToCom(mysnap.mass.size(),&mysnap.vel[0],&mysnap.mass[0]);
    }
    // save all components/properties recentered
    typename std::map<std::string, std::vector<int> >::iterator ii;
    for (ii=mysnap.range.begin(); ii !=mysnap.range.end(); ii++) {
      std::cerr << "first = " << (*ii).first << "\n";
      std::string mystring=(*ii).first;
      std::string comp=CSnaptools::parseString(mystring,":");
      std::string prop=CSnaptools::parseString(mystring,":");
      std::cerr << "comp = " << comp << " prop =" << prop << "\n";
      std::cerr << "range ["<< ((*ii).second)[0] << ":" << ((*ii).second)[1] << "]\n";
      int n= 1+((*ii).second)[1]-((*ii).second)[0];
      if (prop=="mass") {
        unsout->setData(comp,prop,n,&mysnap.mass[((*ii).second)[0]]);
      }
      if (prop=="pos") {
        unsout->setData(comp,prop,n/3,&mysnap.pos[((*ii).second)[0]]);
      }
      if (prop=="vel") {
        unsout->setData(comp,prop,n/3,&mysnap.vel[((*ii).second)[0]]);
      }
    }
  }

  unsout->snapshot->setData("time",otime); // snapshot time
  unsout->snapshot->save();  // save file
}

// ------------------------------------------------------------
// start program
template <class T>
void start()
{

  // get input parameters
  char * in1     = getparam ((char *) "in1"      );
  char * in2     = getparam ((char *) "in2"      );
  char * out     = getparam ((char *) "out"      );
  char * dr      = getparam ((char *) "deltar"   );
  char * dv      = getparam ((char *) "deltav"   );
         com     = getbparam((char *) "zerocm"   );
         shift   = getiparam((char *) "shift"    );
  bool   verbose = getbparam((char *) "verbose"  );  
  float  otime   = getdparam((char *) "time"     );

  // convert string to vector
  deltar=CSnaptools::stringToVector<double>(dr,3,0.0);
  deltav=CSnaptools::stringToVector<double>(dv,3,0.0);

  // instantiate a new UNS input object (for reading)
  uns::CunsIn2<T> * uns1 = new uns::CunsIn2<T>(in1,"all","all",verbose);
  
  // instantiate a new UNS input object (for reading)
  uns::CunsIn2<T> * uns2 = new uns::CunsIn2<T>(in2,"all","all",verbose);

  // some checking
  if (!uns1->isValid()) {
    std::cerr << "File ["<<in1<<"] is not an UNS known file format\n";
    std::exit(1);
  }
  if (!uns2->isValid()) {
    std::cerr << "File ["<<in2<<"] is not an UNS known file format\n";
    std::exit(1);
  }
  // read first time
  bool ok1=uns1->snapshot->nextFrame();
  bool ok2=uns2->snapshot->nextFrame();
  
  if (ok1&&ok2) {        
    // snapshot type must be identical
    if (uns1->snapshot->getInterfaceType() != uns2->snapshot->getInterfaceType()) {
      std::cerr << "UNS files types are not identical, aborting....\n";
      std::exit(1);
    }
    process<T>(uns1,uns2,out,verbose,otime);
  } else {
    std::cerr << "Can't read nextFrame ....\n";
  }

}
//------------------------------------------------------------------------------
//                             M   A   I   N
//------------------------------------------------------------------------------
int main(int argc, char ** argv )
{
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  if (argc) {;} // remove compiler warning :)
  bool single  =(getbparam ((char *) "float"  ));

  if (single) start<float>();
  else        start<double>();

  //   finish NEMO
  finiparam();

}

// ----------- End Of [uns2uns.cc] ------------------------------------
