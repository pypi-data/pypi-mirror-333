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

namespace nos { // use namespace to avoid conflict between
// typedef char * string from stdinc.h
// and using std::string from ccfits.h
typedef char * string;
#include "getparam.h"
}
// --------------------------------------------------------------
#include "uns.h"
#include "csnaptools.h"
#include "ctree.h"
#include "cneibors.h"
#include "ctimer.h"

using namespace jclut;
using namespace jcltree;

// --------------------------------------------------------------
const char * defv[] = {
  "in=???\n		      UNS input snapshot",
  "intp=???\n		  UNS input test particles snapshot",
  "out=???\n          output snapshot",
  "select=???\n       select particles (range, or component name)",
  "neib=6\n           minimum #neibours",
  "direct=f\n         use direct method (very slow)",
  //"smr=f\n            stop max radius?",
  "times=all\n		  selected time",
  "verbose=f\n        verbose on/off"
  "VERSION=1.O\n      compiled on <" __DATE__ "> JCL  ",
  NULL,
};

const char * usage="compute density on test particles";
const long long one=1;
// --------------------------------------------------------------
// main
int main(int argc, char ** argv )
{
  if (argc) {;}
  //   start  NEMO
  nos::initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  
  /* recuperation des parametres en entree */
  std::string simname(nos::getparam((char *) "in"     ));
  std::string simnametp(nos::getparam((char *) "intp"     ));
  std::string outname(nos::getparam((char *) "out"     ));
  std::string select_c(nos::getparam((char *) "select" ));
  std::string select_t(nos::getparam((char *) "times"  ));

  int  neib=nos::getiparam((char *) "neib"  );
  bool   direct      = (nos::getbparam((char *) "direct"  ));
  //bool   smr         = (nos::getbparam((char *) "smr"    ));
  bool   verbose     = (nos::getbparam((char *) "verbose"));
  
  // instantiate a new uns object
  //s::Cuns * uns = new uns::Cuns(simname,select_c,select_t);
  float * postp=NULL, *masstp=NULL, *veltp=NULL;
  int *idtp=NULL;
  int nbodytest=0;
  uns::CunsIn * unstp = new uns::CunsIn(simnametp,"all","all",verbose);
  if (unstp->isValid()) {
    if (unstp->snapshot->nextFrame("mxvI")) {
      bool ok;
      // get the input number of bodies for tests particles
      ok=unstp->snapshot->getData("nsel",&nbodytest);
      assert(ok);
      ok = unstp->snapshot->getData("pos",&nbodytest,&postp);
      assert(ok);
    }
  }
  // instantiate a new uns object
  //s::Cuns * uns = new uns::Cuns(simname,select_c,select_t);
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);
  if (uns->isValid()) {    
    while(uns->snapshot->nextFrame("mxvI")) {

      int nbody;      
      float time;
      // get the input number of bodies according to the selection
      uns->snapshot->getData("nsel",&nbody);
      // get the simulation time
      uns->snapshot->getData("time",&time);
      std::cerr << "nbody=" << nbody << " time="<< time <<"\n";
      std::cerr << "filename = " << uns->snapshot->getFileName() << "\n";
      bool ok;
      float * pos=NULL, * mass=NULL, *vel=NULL;
      int * id=NULL;
      ok = uns->snapshot->getData("id",&nbody,&id);
      ok = uns->snapshot->getData("mass",&nbody,&mass);
      ok = uns->snapshot->getData("vel",&nbody,&vel);
      ok = uns->snapshot->getData("pos",&nbody,&pos);
      CTimer timing;
      double time_maketree;
      if (ok) {
        CTree<float> * tree = new CTree<float>(nbody,pos,(float *) NULL);
        time_maketree = timing.cpu();
        std::cerr << "Tree done in :" << time_maketree << " secondes\n";
        timing.restart();
        // create neibors object
        CNeibors<float> * neibors = new CNeibors<float>(tree);
        std::vector<CDistanceId> tabneib;

        float * rho = new float[nbodytest];
        float * hsml= new float[nbodytest];
        double rmax=tree->getRsize()/ double(one<<(tree->getLevelMax()/2));
        double pi=acos(-1);
        double vsphere=4*pi/3.0;
        int count_search=0;        

        double radius=tree->getRsize()/ double(one<<(tree->getLevelMax()));
        std::cerr << "First Radius = "<<radius<<"\n";
                std::cerr << "Rmax = "<<rmax<<"\n";
        if (direct) {
          std::cerr << "Using direct method...";
        } else {
          std::cerr << "Using tree method...\n";
        }
        float onepercent=0.;
        for (int i=0; i<nbodytest;i++) {
          tabneib.clear();
          //radius /= 2.0;
          //double radius=tree->distanceBodyToMesh(i)*1.5;
          assert(radius>=0.);

          //neibors->setStopAtMaxRadius(smr);
          //neibors->setMaxRadius((radius)*1.5);
          float * pp=postp+(i*3);
          if (!direct) {
            neibors->process(pp,neib,&tabneib);
          } else {
            neibors->direct(pp,neib,&tabneib);
          }
          onepercent++;
          if (onepercent>=0.1*nbodytest/100.) {
            onepercent=0.;
            fprintf(stderr,"\rcompleted : %.2f %%",i*100./nbodytest);
          }
          int nneib=1;
          radius = tabneib[tabneib.size()-1].getDistance();
          nneib=   tabneib.size();
          count_search++;

          //std::cerr << "#neibs = "<<nneib<<"\n";
          assert(radius>=0.);
          assert(nneib>=neib);

          //rho[i]=(Level(tree->getBodyData()+i))/radius/radius/radius;
          rho[i]=nneib/(vsphere*radius*radius*radius);
          hsml[i]=radius;
          //std::cerr << "i="<< i<< " radius ="<<radius << " rho="<<rho<< " level=" << Level(tree->getBodyData()+i)<<"\n";
        }
        std::cerr << "\n";
        std::cerr << "Search neighbours :"<<timing.cpu() << " secondes\n";
        std::cerr << "Level max="<<tree->getLevelMax() << "\n";
        std::cerr << "TREE Level min="<<tree->getLevelMin() << "\n";

        uns::CunsOut * unsout = new uns::CunsOut(outname,"nemo",verbose);
        unsout->snapshot->setData("time",time);
        unsout->snapshot->setData("all","pos",nbodytest,postp,false);
        if (masstp)
          unsout->snapshot->setData("all","mass",nbodytest,masstp,false);
        if (veltp)
          unsout->snapshot->setData("all","vel",nbodytest,veltp,false);
        if (rho)
          unsout->snapshot->setData("all","rho",nbodytest,rho,false);
        if (hsml)
          unsout->snapshot->setData("all","hsml",nbodytest,hsml,false);
        if (idtp)
          unsout->snapshot->setData("all","id",nbodytest,idtp,false);
        // save snapshot
        unsout->snapshot->save();
        delete tree;
        delete neibors;
        /*
        if (pos)  delete [] pos;
        if (vel)  delete [] vel;
        if (mass) delete [] mass;
        if (id)   delete [] id;
        */
        if (rho)  delete [] rho;
        if (hsml) delete [] hsml;
        delete unsout;
      }

    }
  }
  
  //   finish NEMO
  nos::finiparam();
} 
	      
//
