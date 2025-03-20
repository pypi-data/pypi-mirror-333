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
  "out=???\n          output snapshot",
  "select=???\n       select particles (range, or component name)",
  "nl=0.2\n           level_max-nl*level_max ncrit level",
  "neib=6\n           maximum neibours number",
  "smr=f\n            stop max radius?",
  "hf=4.0\n           hsml factor",
  "times=all\n		  selected time",
  "verbose=f\n        verbose on/off"
  "VERSION=1.O\n      compiled on <" __DATE__ "> JCL  ",
  NULL,
};

const char * usage="compute octree around snapshot";
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
  std::string outname(nos::getparam((char *) "out"     ));
  std::string select_c(nos::getparam((char *) "select" ));
  std::string select_t(nos::getparam((char *) "times"  ));
  double nl=nos::getdparam((char *) "nl"    );
  if (nl) {;}
  double hf=nos::getdparam((char *) "hf"    );
  int  neib=nos::getiparam((char *) "neib"  );
  bool   smr         = (nos::getbparam((char *) "smr"    ));
  bool   verbose     = (nos::getbparam((char *) "verbose"));
  
  
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

        float * rho = new float[nbody];
        float * hsml= new float[nbody];
        double rmax=tree->getRsize()/ double(one<<(tree->getLevelMax()/2));
        double pi=acos(-1);
        double vsphere=4*pi/3.0;
        int count_search=0;
        long long stat_levels[128];
        for (int i=0; i<128 ; i++) {
          stat_levels[i]=0;
        }

        for (int i=0; i<nbody;i++) {
          tabneib.clear();
          int mylevel=Level(tree->getBodyData()+i);
          if (mylevel+1 == tree->getLevelMax()) {
            //std::cerr << "yo\n";
            //mylevel--;
          }

          //double radius=tree->getRsize()/ double(one<<(mylevel));
          //radius /= 2.0;
          double radius=tree->distanceBodyToMesh(i)*1.5;
          assert(radius>=0.);
          if (radius < 1.10e-8) {
            radius=tree->getRsize()/ double(one<<(mylevel+1));
            assert(radius>=0.);
          }

#if 0
          //double bestradius=tree->distanceBodyToMesh(i);
          if ((mylevel) > (tree->getLevelMax()-nl*tree->getLevelMax())) {
#else
          if (i%10==0 && false) {

#endif
            neibors->setStopAtMaxRadius(smr);
            neibors->setMaxRadius((radius)*1.5);
            neibors->process(i,neib,&tabneib);
            stat_levels[mylevel]++;
          }

          int nneib=1;
          if (tabneib.size()>1) { // proceed on particles with more 1 neib
            radius = tabneib[tabneib.size()-1].getDistance();
            nneib=   tabneib.size();
            count_search++;
          } else {
            radius = std::min(radius,rmax);
          }
          assert(radius>=0.);
          //rho[i]=(Level(tree->getBodyData()+i))/radius/radius/radius;
          rho[i]=nneib/(vsphere*radius*radius*radius);
          hsml[i]=radius*hf;//10./pow(2.,(Level(tree->getBodyData()+i)+1));
          //std::cerr << "i="<< i<< " radius ="<<radius << " rho="<<rho<< " level=" << Level(tree->getBodyData()+i)<<"\n";
        }
        std::cerr << "Search neighbours :"<<timing.cpu() << " secondes\n";
        std::cerr << "Level max="<<tree->getLevelMax() << "\n";
        std::cerr << "TREE Level min="<<tree->getLevelMin() << "\n";
        std::cerr << "Count search= " << count_search*100./nbody << " % nbody\n";
        tree->displayLevelStats();
        std::cerr << " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n";
        for (int i=0; i<128 ; i++) {
          if (stat_levels[i]!=0) {
            std::cerr << i << " : " << stat_levels[i] << "\n";
          }
        }
        uns::CunsOut * unsout = new uns::CunsOut(outname,"nemo",verbose);
        unsout->snapshot->setData("time",time);
        unsout->snapshot->setData("all","pos",nbody,pos,false);
        if (mass)
          unsout->snapshot->setData("all","mass",nbody,mass,false);
        if (vel)
          unsout->snapshot->setData("all","vel",nbody,vel,false);
        if (rho)
          unsout->snapshot->setData("all","rho",nbody,rho,false);
        if (hsml)
          unsout->snapshot->setData("all","hsml",nbody,hsml,false);
        if (id)
          unsout->snapshot->setData("all","id",nbody,id,false);
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
