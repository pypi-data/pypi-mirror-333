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
#include "ctree.h"
#undef NDEBUG // to keep assert() calls working
#include <cassert>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <cvecutils.h>

namespace jcltree {

using  namespace vectutils;
// ============================================================================
// Constructor
template <class T>
CTree<T>::CTree(const int _nbody, const T * pos, const T * mass,
                                const double _fcells,const double _rsize)
{
  init(_nbody,pos,mass,_fcells,_rsize);
}
// ============================================================================
// Destructor
template <class T>
CTree<T>::~CTree()
{
  //if (ctab) delete [] ctab;
  for (unsigned int i=0; i<ctab.size(); i++) {
    delete [] ctab[i];
  }
  ctab.clear();
  if (btab) delete [] btab;
}
// ============================================================================
// initialize
template <class T>
void CTree<T>::init(const int _nbody, const T * pos, const T * mass,
                    const double _fcells,const double _rsize)
{
  ctab.clear();
  nbody     = _nbody;
  fcells    = _fcells;
  rsize     = _rsize;
  totalcell = 0;
  level_max = 0;
  level_min = 1000000;
  samepos.clear();
  setvs(rmin,0.0); // set rmin to [0,0,0] coordinate

  // init stats
  for (int i=0; i<LMAX ; i++) {
    stat_levels[i]=0;
  }
  // allocate memory for body tree structure
  btab = new body[nbody];

  // Load data into tree structure
  // store data in body structure
  T * pp= (T *) pos; // ptr on pos array
  bodyptr bp=btab;
  for (int i = 0; i < nbody; i++) {
    Type(bp) = BODY;    // body type
    Id(bp)   = i;       // original pos index
    if (mass)
      Mass(bp) = mass[i];
    else
      Mass(bp) = 1.;    // force mass to 1.
    double ppp[3];
    for (int i=0; i<3;i++)  ppp[i]=pp[i]; // convert to double in case of float input
    setv(Pos(bp), (double *) ppp);
    //std::cerr << "--- " << Pos(bp)[0] << " " << Pos(bp)[1] << " " << Pos(bp)[2] << "\n";
    pp += NDIM;
    bp++;
  }

  // Create tree
  makeTree();

  if (samepos.size()>0){
    std::cerr << "["<<samepos.size()<<"] couple of particles have identical positions !!!\n";
  }
}

// ============================================================================
// MAKETREE: initialize tree structure
template <class T>
void CTree<T>::makeTree()
{
  bodyptr p;

  if (ctab.size()==0) {	           // first time through?
      maxcell = fcells * nbody;	   //   typ. need: 0.5 nbody
      cellptr p = new cell[maxcell];    // alloc  cells
      ctab.push_back(p);
    }
    ncell = 0;			        // reset cells in use
    troot = NULL;			// deallocate current tree

    for (p = btab;p <btab+nbody; p++) { // loop over all bodies<<
      if (Mass(p) != 0.0) {		//   only load massive ones
        expandBox(p);			//     expand root to fit
        loadTree(p);	        //     insert into tree
      }
    }
    hackCofm(troot,0);			// find c-of-m coordinates
}
// ============================================================================
// LOADTREE: descend tree and insert a particle
template <class T>
void CTree<T>::loadTree(bodyptr p)
{
  int_hack l, xp[NDIM], xq[NDIM];
  nodeptr *qptr;
  cellptr c;

  do {
    assert(intCoord(xp, Pos(p)));		// form integer coords
    l = IMAX >> 1;				// start with top bit
    qptr = &troot;				// start with tree root
    while (*qptr != NULL) {			// loop descending tree
      //dprintf(1,"loadtree: descending tree  l = %o\n", l);
      // assert(l != 0);			//   dont run out of bits
      if(l==0) {
        //int offset = p-btab;
        //std::cerr<< "loadtree: ran out of bits for particle "<<offset+1<<"\n";
        break;
      }
      if (l==0) {
        std::cerr << "L  ======== 0\n";
      }
      if (Type(*qptr) == BODY) {		//   reached a "leaf"?
        //dprintf(1,"loadtree: replacing body with cell\n");
        c = makeCell();                         //     alloc a new cell
        assert(intCoord(xq, Pos(*qptr)));	//     get integer coords
        Subp(c)[subIndex(xq, l)] = *qptr;	//     put body in cell
        *qptr = (nodeptr) c;                    //     link cell in tree
      }
      qptr = &Subp(*qptr)[subIndex(xp, l)];	//   move down one level

      l = l >> 1;				//   and test next bit
    }
    if (l==0) {
      //std::cerr << "Warning : Two particles at the same position, id["<<p-btab+1<<"] skipping...\n";
      if (*qptr != NULL && Type(*qptr) == BODY) { // particles with same positions
        CSamePos ids(Id(p),Id(*qptr));
        samepos.push_back(ids);
      }
      break;
    }

  } while (l==0);
  //dprintf(1,"loadtree: installing body  l = %o\n", l);
  *qptr = (nodeptr) p;			// found place, store p

}
// ============================================================================
// EXPANDBOX: enlarge cubical "box", salvaging existing tree structure
template <class T>
void CTree<T>::expandBox(bodyptr p)
{
  int_hack k, xtmp[NDIM], xmid[NDIM];
  double rmid[3];
  cellptr newt;

  while (! intCoord(xtmp, Pos(p))) {		// expand box (rarely)
    //dprintf(1,"expandbox: expanding box\n");
    addvs(rmid, rmin, 0.5 * rsize);             //   find box midpoint
    for (k = 0; k < NDIM; k++)                  //   loop over dimensions
      if (Pos(p)[k] < rmid[k])                  //     is p left of mid?
        rmin[k] -= rsize;                       //       extend to left
    rsize = 2.0 * rsize;                        //   double length of box
    //if (debug)
      //dprintf(0,"\t   rmin = [%8.4f,%8.4f,%8.4f]\trsize = %8.4f\n",
      //        rmin[0], rmin[1], rmin[3], rsize);
    if (troot != NULL) {                        //   repot existing tree?
      newt = makeCell();                        //     create new root cell
      assert(intCoord(xmid, rmid));             //     locate old root cell
      k = subIndex(xmid, IMAX >> 1);            //     find old tree index
      Subp(newt)[k] = troot;                    //     graft old on new
      //dprintf(1,"expandbox: old root goes in subcell %d\n", k);
      troot = (nodeptr) newt;                   //     plant new tree
    }
  }
}
// ============================================================================
// INTCOORD: compute integerized coordinates.
// Returns: TRUE unless rp was out of bounds.
template <class T>
bool CTree<T>::intCoord(int_hack xp[3], double rp[3])
{
  int k;
  bool inb;
  double xsc;

  //dprintf(1,"intcoord: rp = [%8.4f,%8.4f,%8.4f]\n", rp[0], rp[1], rp[2]);
  inb = true;			          // use to check bounds
  for (k = 0; k < NDIM; k++) {		  // loop over dimensions
    xsc = (rp[k] - rmin[k]) / rsize;      //   scale to range [0,1)
    if (0.0 <= xsc && xsc < 1.0)          //   within unit interval?
      xp[k] = floor(IMAX * xsc);          //     then integerize
    else                                  //   out of range
      inb = false;                        //     then remember that
  }
  //dprintf(1,"\t  xp = [%8x,%8x,%8x]\tinb = %d\n", xp[0], xp[1], xp[2], inb);
  return inb;
}
// ============================================================================
// SUBINDEX: determine which subcell to select.
template <class T>
int_hack CTree<T>::subIndex(int_hack x[3], int_hack l)
{
  int_hack i, k;

  //dprintf(1,"subindex: x = [%8x,%8x,%8x]\tl = %8x\n", x[0],x[1],x[2],l);
  i = 0;                                   //  sum index in i
  for (k = 0; k < NDIM; k++)               // check each dimension
    if (x[k] & l)                          //   if beyond midpoint
      i += NSUB >> (k + 1);                //     skip over subcells
  //dprintf(1,"          returning %d\n", i);
  return i;
}
// ============================================================================
// MAKECELL: allocation routine for cells.
template <class T>
cellptr CTree<T>::makeCell()
{
  cellptr c;
  int i;

  if (ncell >= maxcell) {
    std::cerr << "makecell: need more than [" << maxcell <<"] reallocating\n";
    maxcell = 1000;
    ncell=0;
    cellptr p = new cell[maxcell];    // alloc  cells
    ctab.push_back(p);
    std::cerr << "Ctab vector="<<ctab.size()<<"\n";
  }
  c = ctab[ctab.size()-1] + ncell;
  ncell++;
  totalcell++;
  //dprintf(1,"cell %d allocated at address 0%o\n", ncell, (int) c);
  Type(c) = CELL;
  for (i = 0; i < NSUB; i++)
    Subp(c)[i] = NULL;
  return (c);
}

// ============================================================================
// HACKCOFM: descend tree finding center-of-mass coordinates.
template <class T>
void CTree<T>::hackCofm(nodeptr q, int_hack l)             // pointer into body-tree
{
   int i;
   nodeptr r;
   static double tmpv[3];

  if (Type(q) == CELL) {                      // is this a cell?
    Mass(q) = 0.0;                            //   init total mass
    clrv(Pos(q));                             //   and c. of m.
    for (i = 0; i < NSUB; i++) {              //   loop over subcells
      r = Subp(q)[i];
      if (r != NULL) {                        //     does subcell exist?
        hackCofm(r,l+1);                          //       find subcell cm
        Mass(q) += Mass(r);                   //       sum total mass
        mulvs(tmpv, Pos(r), Mass(r));         //       find moment
        addv(Pos(q), Pos(q), tmpv);           //       sum tot. moment
      }
    }
    divvs(Pos(q), Pos(q), Mass(q));           //   rescale cms position
  } else {                                    // it's a body
    Level(q) = l;                             // save tree level for the particle
    level_max = std::max(level_max,l);
    level_min = std::min(level_min,l);
    stat_levels[l]++; // one more particle for the level
  }
}
// ============================================================================
// distanceBodyToMesh : compute closest between particles and mesh cube
template <class T>
double CTree<T>::distanceBodyToMesh(const int i)
{
  double pos0[3];
  // get particle positions
  setv(pos0,Pos(getBodyData()+i));

  double mylevel=(one<<Level(getBodyData()+i));
  double mesh_size=rsize/mylevel;

  // compute closest mesh coordinates for every particles dimension
  double px_mesh=fabs(mesh_size*round(pos0[0]/mesh_size));
  double py_mesh=fabs(mesh_size*round(pos0[1]/mesh_size));
  double pz_mesh=fabs(mesh_size*round(pos0[2]/mesh_size));

  double closest_distance=std::min(fabs(fabs(pos0[0])-px_mesh),
      std::min(fabs(fabs(pos0[1])-py_mesh),fabs(fabs(pos0[2])-pz_mesh)));
  return closest_distance;
}
// ============================================================================
// display level stat
template <class T>
void CTree<T>::displayLevelStats()
{
  for (int i=0; i<LMAX ; i++) {
    if (stat_levels[i]!=0) {
      std::cerr << i << " : " << stat_levels[i] << "\n";
    }
  }
}
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Templates instantiation MUST be declared **AFTER** templates declaration
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// C++11
//extern template class CSnapshotGadgetIn<float>;
template class CTree<float>;

//extern template class CSnapshotGadgetIn<double>;
template class CTree<double>;

}
