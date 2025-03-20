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
#include "cneibors.h"
#include "cvecutils.h"
#include <cmath>
#include <iostream>
#include <cassert>
#include <algorithm>

namespace jcltree {
using  namespace vectutils;

// ============================================================================
// Constructor
template <class T>
CNeibors<T>::CNeibors(const CTree<T> * _tree, const double _rneib0)
{
  tree   =  (CTree<T> * ) _tree; // connect to tree
  rneib  = _rneib0;           // initial searching radius
  max_radius = rneib;         // set max searching radius
  stop_max_radius = false;    // by default false
}

// ============================================================================
// process : find neighbors using tree search algorithm
template <class T>
void CNeibors<T>::process(const T * _pos0, const int _nneib, std::vector<CDistanceId> * _neib)
{
  // set variables
  nneib = _nneib;  // #neibors to find
  neib  = _neib;   // vector of neibors

  neib->clear(); // clear neibors vector

  // convert float to double if necessary
  pos0[0]=_pos0[0];
  pos0[1]=_pos0[1];
  pos0[2]=_pos0[2];

  countPartInRadius();
}
// ============================================================================
// process : find neighbors using tree search algorithm on self particles from tree
template <class T>
void CNeibors<T>::process(const int i, const int _nneib, std::vector<CDistanceId> * _neib)
{
  // set variables
  nneib = _nneib;  // #neibors to find
  neib  = _neib;   // vector of neibors

  neib->clear(); // clear neibors vector

  int nbody=tree->getNbody();
  assert(i<nbody);

  // convert float to double if necessary
  setv(pos0,Pos(tree->getBodyData()+i));

#if 0
  double radius=tree->getRsize()/ double(one<<(1+Level(tree->getBodyData()+i)));
  rneib = radius*1.5;
#else
  double radius=tree->getRsize()/ double(one<<(1+Level(tree->getBodyData()+i)))*1.5+
                tree->distanceBodyToMesh(i);
  rneib = radius;
#endif
  //std::cerr << "rneib estimated="<<rneib <<" L="<<Level(tree->getBodyData()+i) <<"\n";
  countPartInRadius();
}

// ============================================================================
// direct : find neighbors with brute methode
template <class T>
void CNeibors<T>::direct(const T * _pos0, const int _nneib, std::vector<CDistanceId> * _neib)
{
  // set variables
  nneib = _nneib;  // #neibors to find
  neib  = _neib;   // vector of neibors

  // convert float to double if necessary
  pos0[0] = _pos0[0];
  pos0[1] = _pos0[1];
  pos0[2] = _pos0[2];

  neib->clear(); // clear neibors vector

  int    nbody  = tree->getNbody();
  bodyptr p     = tree->getBodyData();
  double disp[3],r2;
  for (int i=0; i<nbody;  i++,p++) {
    subv(disp,Pos(p),pos0);
    dotvp(r2,disp,disp);
    CDistanceId ri(r2,Id(p));
    neib->push_back(ri);                  // one more neibor
  }
  // sort neibor array
  std::sort(neib->begin(),neib->end(),CDistanceId::sortD);
}

// ============================================================================
// count particles in a given radius
template <class T>
void CNeibors<T>::countPartInRadius()
{
  double dis0=0.0;
  double dismax=1.1e30;

  double * rmin = tree->getRmin();
  double  rsize = tree->getRsize();
  nodeptr troot = tree->getRoot();

  bool stop= false;

  total = 0;       // #neibors currently found
  while (!stop && ((total < nneib) || total > nneib*10)) {
    total = 0;     // reset for the current radius
    neib->clear(); // reset vector of neibors

    double croot[3];
    for(int i=0; i<3; i++) {
      croot[i]=rmin[i]+rsize*0.5;
    }
    searchTree(troot, croot, rsize); // search in tree
    if (stop_max_radius && rneib>= max_radius) {
      stop=true;
     // std::cerr << "Force stop because max radius reached\n";
    }
    //assert(rneib!=0. && total!=0);
    if(total < nneib) {
      dis0=rneib;
      if(dismax < 1e30){
        rneib=(dismax+dis0)*0.5;
      }else{
        rneib=rneib*1.5;
      }
    }

    if(total > nneib*10){
      dismax=rneib;
      rneib=(rneib+dis0)*0.5;
    }
    if (stop_max_radius) {
      rneib=std::min(rneib,max_radius);
    }

  }
  // sort neibor array
  std::sort(neib->begin(),neib->end(),CDistanceId::sortD);

  // compute new radius
  double nneibr=nneib; // MANDATORY to have division by total not in INTEGER !!!
  rneib = 1.5*rneib*pow(nneibr/total,0.333333);

  if (stop_max_radius) {
    rneib=std::min(rneib,max_radius);
  }
  //std::cerr <<"new rneib="<<rneib<<"\n";
}
// ============================================================================
// search particles, recursively into the tree, which match to
// the criterium
template <class T>
void CNeibors<T>::searchTree(nodeptr p, double * cpos, double d)
{
  nodeptr *pp;
  double offset, r2;
  double cpossub[3], disp[3];

  offset = d*0.25;

  if (Type(p) == BODY){ // it's a leave
    r2=0.0;
    subv(disp, Pos(p), pos0);               // compute displacement
    dotvp(r2, disp, disp);                  // and find dist squared
    if(r2 < rneib*rneib){
      total++;
      CDistanceId ri(r2,Id(p));
      neib->push_back(ri);                  // one more neibor
    }
  }
  else {                // it's a node
    if (openTreeNode( cpos, d)) {           // should p be opened?
      pp = & Subp(p)[0];                         //   point to sub-cells
      int i,j;
      for (int k = 0; k < NSUB; k++) {           //   loop over sub-cells
        for( i=NDIM-1, j=1; i>=0; i--, j*=2){
          if(j&k){
            cpossub[i]=cpos[i]+offset;
          }else{
            cpossub[i]=cpos[i]-offset;
          }
        }
        if (*pp != NULL)                    //     not empty
          searchTree(*pp, cpossub, d*0.5);  //     descent tree

        pp++;                               //     point to next one
      }
    }
  }
}
// ============================================================================
// decide is a node tree must be opened, return true if yes
template <class T>
bool CNeibors<T>::openTreeNode(double * cpos,   // geometrical center of the node
                            double d)        // size of cell squared
{
  double dr[3];
  double drsq, lcrit;
  subv(dr, cpos, pos0);                     // compute displacement
  for (int i=0; i<3; i++){
    if(fabs(dr[i]) > rneib+d*0.5){          // node to far from particles
      return false;
    }
  }
  dotvp(drsq, dr, dr);                      // and find dist squared
  lcrit= rneib + 0.875*d;	            // critical separation
  lcrit = lcrit*lcrit;
  return (drsq < lcrit);                    // use geometrical rule
}

// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Templates instantiation MUST be declared **AFTER** templates declaration
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// C++11
//extern template class CSnapshotGadgetIn<float>;
template class CNeibors<float>;

//extern template class CSnapshotGadgetIn<double>;
template class CNeibors<double>;

} // end of namespace
