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
  "select=all\n               select particles (range, or component name)\n"
  "                   component: gas,halo,disk,bulge,stars,bndry",
  "display=t\n                display array's content (t|f)",
  "bits=\n         (default: all , but you cat set \"mxvpXRIUMAHT\" physicals quantities that you want to display\n",
  "float=t\n        real format used, t=float, f=double",
  "maxline=2\n                max lines per components",  
  "times=all\n		      selected time",
  "verbose=f\n                verbose on/off",
  "VERSION=2.2\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};
const char * usage="Print information about an UNS file";
using namespace std;
template <class T> void displayInfo(bool display,int maxlines, std::string comp, uns::CunsIn2<T> * uns);
template <class T> void displayFormat(int maxlines,std::string text, T * array, int dim, int size, int np);
bool component_exist=false;
// ------------------------------------------------------------
//  displayInfo
template <class T> void displayInfo(bool display,int maxlines, std::string comp, uns::CunsIn2<T> * uns)
{
  T * pos, * vel, * mass, * pot , *acc, *eps;
  int * id;
  int nbody=0;
  bool ok=false;

  T * nullp;
  ok = uns->snapshot->getData(comp,"nbody" ,&nbody,&nullp);
  if (ok) component_exist=true;
  if (ok) {
    std::cout << setw(50) << setfill('=') << ""<<"\n";
    std::cout<< setfill(' ');
    std::cout<< left<< setw(8) << comp << ":" << setw(9) << right << nbody << "\n";
  }
  if (uns->snapshot->getReqBits()&MASS_BIT) {
    ok = uns->snapshot->getData(comp,"mass",&nbody,&mass);
    if (ok && display) {
      displayFormat(maxlines,"mass[1] = ",mass,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&POS_BIT) {
    ok = uns->snapshot->getData(comp,"pos" ,&nbody,&pos );
    if (ok && display) {
      displayFormat(maxlines,"pos [3] = ",pos ,3,nbody, 1);
    }
  }
  if (uns->snapshot->getReqBits()&VEL_BIT) {
    ok = uns->snapshot->getData(comp,"vel" ,&nbody,&vel );
    if (ok && display) {
      displayFormat(maxlines,"vel [3] = ",vel ,3,nbody, 1);
    }
  }
  if (uns->snapshot->getReqBits()&POT_BIT) {
    ok = uns->snapshot->getData(comp,"pot" ,&nbody,&pot );
    if (ok && display) {
      displayFormat(maxlines,"pot [1] = ",pot ,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&EPS_BIT) {
    ok = uns->snapshot->getData(comp,"eps" ,&nbody,&eps );
    if (ok && display) {
      displayFormat(maxlines,"eps [1] = ",eps ,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&ACC_BIT) {
    ok = uns->snapshot->getData(comp,"acc" ,&nbody,&acc );
    if (ok && display) {
      displayFormat(maxlines,"acc [3] = ",acc ,3,nbody, 1);
    }
  }
  if (uns->snapshot->getReqBits()&ID_BIT) {
    ok = uns->snapshot->getData(comp,"id"  ,&nbody,&id);
    if (ok && display) {
      displayFormat(maxlines,"id  [1] = ",id  ,1,nbody, 3);
    }
  }
  //if (comp == "gas") {
  T * rho, * u, * hsml, * temp, * nh, * sfr, * metal;
  if (uns->snapshot->getReqBits()&RHO_BIT) {
    ok = uns->snapshot->getData(comp,"rho" ,&nbody,&rho );
    if (ok && display) {
      displayFormat(maxlines,"rho [1] = ",rho ,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&U_BIT) {
    ok = uns->snapshot->getData(comp,"u"   ,&nbody,&u );
    if (ok && display) {
      displayFormat(maxlines,"u   [1] = ",u   ,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&HSML_BIT) {
    ok = uns->snapshot->getData(comp,"hsml",&nbody,&hsml);
    if (ok && display) {
      displayFormat(maxlines,"hsml[1] = ",hsml,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&TEMP_BIT) {
    ok = uns->snapshot->getData(comp,"temp",&nbody,&temp);
    if (ok && display) {
      displayFormat(maxlines,"temp[1] = ",temp,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&METAL_BIT) {
    ok = uns->snapshot->getData(comp,"metal",&nbody,&metal);
    if (ok && display) {
      displayFormat(maxlines,"metal[1]= ",metal,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&NH_BIT) {
    ok = uns->snapshot->getData(comp,"nh",&nbody,&nh);
    if (ok && display) {
      displayFormat(maxlines,"nh   [1]= ",nh,1,nbody, 3);
    }
  }
  if (uns->snapshot->getReqBits()&SFR_BIT) {
    ok = uns->snapshot->getData(comp,"sfr",&nbody,&sfr);
    if (ok && display) {
      displayFormat(maxlines,"sfr  [1]= ",sfr,1,nbody, 3);
    }
  }
  // RAMSES hydro
  if (comp=="gas") {
    int nvarh=0;
    ok = uns->getData("nvarh",&nvarh);
    if (ok) {
      std::cerr << "nvarh=" << nvarh << "\n";
      for (int i=0; i<std::min(nvarh,20); i++) {
        T * hydro;
        stringstream s_int("");
        s_int << i;
        ok = uns->snapshot->getData("hydro",s_int.str(),&nbody,&hydro);
        if (ok && display) {
          displayFormat(maxlines,"hydro["+s_int.str()+"] = ",hydro,1,nbody, 3);
        }
      }
    }
  }
  //}
  //if (comp == "stars") {
  T * age;//, * metal;
  if (uns->snapshot->getReqBits()&AGE_BIT) {
    ok = uns->snapshot->getData(comp,"age" ,&nbody,&age );
    if (ok && display) {
      displayFormat(maxlines,"age [1] = ",age,1,nbody, 3);
    }
  }
  T * im;
  if (uns->snapshot->getReqBits()&IM_BIT) {
    ok = uns->snapshot->getData(comp,"im" ,&nbody,&im );
    if (ok && display) {
      displayFormat(maxlines,"im [1] = ",im,1,nbody, 3);
    }
  }
  T * ssl;
  if (uns->snapshot->getReqBits()&SSL_BIT) {
    ok = uns->snapshot->getData(comp,"ssl" ,&nbody,&ssl );
    if (ok && display) {
      displayFormat(maxlines,"ssl [1] = ",ssl,1,nbody, 3);
    }
  }
  T * zs,* zsmt;
  int czs, czsmt, nzs, nzsmt;
  if (uns->snapshot->getReqBits()&ZS_BIT) {
    ok = uns->snapshot->getData(comp,"zs" ,&nzs,&zs );
    if (ok && display) {
      ok = uns->snapshot->getData("czs"   ,&czs );
      std::cerr << "nzs="<< nzs<<" czs ="<<czs<<"\n";
      displayFormat(maxlines,"zs [1] = ",zs,1,nzs, 3);
    }
  }
  if (uns->snapshot->getReqBits()&ZSMT_BIT) {
    ok = uns->snapshot->getData(comp,"zsmt" ,&nzsmt,&zsmt );
    if (ok && display) {
      ok = uns->snapshot->getData("czsmt"   ,&czsmt );
      std::cerr << "nzsmt="<< nzsmt<<"  czsmt ="<<czsmt<<"\n";
      displayFormat(maxlines,"zsmt[1] = ",zsmt,1,nzsmt, 3);
    }
  }
  T * cm; int ncm;
  if (uns->snapshot->getReqBits()&CM_BIT) {
    ok = uns->snapshot->getData(comp,"cm" ,&ncm,&cm );
    if (ok && display) {
      displayFormat(maxlines,"cm [1] = ",cm,1,ncm, 3);
    }
  }
//  ok = uns->snapshot->getData(comp,"metal" ,&nbody,&metal );
//  if (ok && display) {
//    displayFormat(maxlines,"metal[1] = ",metal,1,nbody, 3);
//  } 
  //}
}
// ------------------------------------------------------------
// displayFormat
template <class T>  void displayFormat(int maxlines,std::string text, T * array, int dim, int size, int np)
{
  std::cout << scientific << left << setw(11) << text;
  // First line
  for (int k=0;k<std::min(size,np);k++) {
    for (int j=0;j<dim;j++) {
      std::cout << array[k*dim+j] << " ";
    }
  }
  std::cout << "\n";
  // other lines
  for (int i=1; i<std::min(maxlines,size/min(size,np)); i+=1) {
    std::cout << left << setw(11) << "";
    for (int k=0;k<std::min(size,np);k++) {
      for (int j=0;j<dim;j++) {
        std::cout << array[(k+(i*np))*dim+j] << " ";
      }
    }
    std::cout << "\n";
  }  
  std::cout << left << setw(11) << "" << ". . .\n";
}
// ------------------------------------------------------------
// start program
template <class T> void start()
{

  // get input parameters
  char * simname     = getparam ((char *) "in"      );
  char * select_c    = getparam ((char *) "select"  );
  bool   display     = getbparam((char *) "display" );
  std::string bits   =(getparam ((char *) "bits"    ));
  int    maxlines    = getiparam((char *) "maxline" );
  char * select_t    = getparam ((char *) "times"   );
  bool   verbose     = getbparam((char *) "verbose" );  
  
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn2<T> * uns = new uns::CunsIn2<T>(simname,select_c,select_t,verbose);

  if (!display) bits="none"; // we don't read anything
  if (uns->isValid()) { // input file is known by UNS lib        
    while(uns->snapshot->nextFrame(bits)) { // there is a new frame
      std::string stype = uns->snapshot->getInterfaceType();
      std::string file_structure=uns->snapshot->getFileStructure();
      std::cout << setw(50) << setfill('*') << ""<<"\n";
      std::cout << "File name : "<<uns->snapshot->getFileName()<<"\n";
      std::cout << "File type : "<<stype<<"\n";
      int nbody; T time;
      //std::vector<T> vrect=uns->snapshot->getData("","/PartType1/Coordinates");
      // get the input number of bodies according to the selection
      uns->snapshot->getData("nsel",&nbody);
      // get the simulation time
      uns->snapshot->getData("time",&time);

      std::cout << "Nbody selected = " << nbody << "\nTime="<<time <<"\n";

      if (nbody >0) {
        if (0 && file_structure=="range") {
          displayInfo(display,maxlines,"all",uns);
        } else {
          component_exist=false;
          displayInfo(display,maxlines,"gas"  ,uns);
          displayInfo(display,maxlines,"halo" ,uns);
          displayInfo(display,maxlines,"disk" ,uns);
          displayInfo(display,maxlines,"bulge",uns);
          displayInfo(display,maxlines,"stars",uns);
          displayInfo(display,maxlines,"bndry",uns);
          if (!component_exist) { // no comp, diplay all
            displayInfo(display,maxlines,"all",uns);
          }
        }
      }
    }
  }
  delete uns;

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
// ------------------------------------------------------------
