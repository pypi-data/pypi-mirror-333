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

#ifndef CBAR_H
#define CBAR_H
#include <string>
#include "cfalcon.h"
#include <cassert>
#include <vector>
#include "csnaptools.h"

namespace uns_proj {
  class CBar;
  //------------------------------------------------------------------------------
  // CPartVec
  // class to store rho, index and id of particles
  class CVecRho {
  public:
    CVecRho(CBar * _bar, int _index) {
      index = _index;
      bar = _bar;
    }
    static bool sortRho(const CVecRho& a, const CVecRho& b);
    static bool sortId (const CVecRho& a, const CVecRho& b);
    int index;
    CBar * bar;      
  };
  
  class CBar {
  public:
    CBar();
    CBar(const int _nbody, float * _pos, float * _vel, float * mass, 
         float * _rho, float *_hsml, int *_id);
    ~CBar();
    float * getRho() { return rho;}
    float computeAngle(const float dmin, const float dmax, const bool mvcod=false);
    float computeAngle(const bool mvcod=false);
    void rotateOnX(const float);
    void rotateOnY(const float);
    void saveAllRho(std::string out);
    void save(std::string out, const float timu,const bool mvcod);
  private:
    int nbody;
    float * pos, * vel, *mass, *rho, *hsml;
    int *id;
    jclut::CDensity * density;
    int data_histo[100]; // store #particles per percentage
    std::vector <CVecRho> vec_rho;
    
    void sortRho();
    void rotate(const float angle);
   
  }; // end of class
} // namespace

extern "C" {
// fortran wrapper, parameters
// IN[integer] rot : 0 no rotate, 1 along X axis, 2 along y axis
// IN[integer] nbody : #bodies
// IN[real4]       time
// IN[real4 array] pos, vel, mass
// IN[integer array] id
// IN[float]       dmin (%density min)
// IN[float]       dmax (%density max)
// IN[integer]     move_to_cod : 0 or 1 to move to cod

// for mdf (stars, set move_to_cod=0 is you use rectify before)
// set dmin=75, dmax=90

bool rotate_bar_(const int * rot, const int * nbody,
                float * pos, float * vel, float * mass,
                int *id,
                float * dmin, float *dmax, const int * mvcod) {

  float * hsml=NULL;
  float * rho=NULL;
  uns_proj::CBar * bar = new uns_proj::CBar(*nbody,pos, vel,mass,rho,hsml,id);
  float phi;
  if (*dmin<0 || *dmax<0)
    phi=bar->computeAngle(*mvcod);
  else
    phi=bar->computeAngle((*dmin)/100.,(*dmax)/100.,true);
  if (*rot==1) {
    bar->rotateOnX(phi);
  }
  if (*rot==2) {
    bar->rotateOnY(phi);
  }
  delete bar;
  return true;
}

}
#endif // CBAR_H
