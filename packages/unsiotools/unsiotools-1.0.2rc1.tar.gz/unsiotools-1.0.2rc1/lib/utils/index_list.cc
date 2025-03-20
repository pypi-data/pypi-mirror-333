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
#include <vector>
#include <algorithm>
#include "csnaptools.h"

using namespace jclut;
using namespace std;
namespace lia_lib_index {

std::vector <int>   vi;    // vector to store indexes    

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

// C++ implementation
void readIndexList(std::string listname);
bool sortList(const int i,const int j);
void storeIds(int * ids, int nids);
void findIdsfromList();

extern "C" { // declare as extern to be called fron fortran and C
// wrapper which can be called from a fortran program
int get_index_sel_id_(const char * filename, int * list_id, int * nid, int * tab_index, 
                      int * size_tab,  unsigned int l1);

}
//------------------------------------------------------------------------------
// get_index_sel_id 
// return a tab  of indexes which match the indexes stored in a file
int get_index_sel_id_(const char * filename, int * list_id, int * nid, int * tab_index, int * size_tab, unsigned int l1)
{
  std::string str=CSnaptools::fixFortran(filename,l1,false);
  //std::cerr << "l1="<<l1<< "  file=["<<filename<<"] ("<< str << ")\n";
  readIndexList(str); // read index from list
  storeIds(list_id,*nid);  // store and sort ids for later processing
  findIdsfromList();             // find ids from the list
  
  // store particles according to the selection
  int ii=0;
  for (std::vector<CPartI>::iterator i=selvec.begin(); i<selvec.end(); i++) {
    int index = (*i).itab;
    assert(ii<=*size_tab);
    tab_index[ii] = index+1; // +1 because of fortran
    ii++;
  }
  return ii;
}


//------------------------------------------------------------------------------
// buildList
// build the final list of particles
void findIdsfromList()
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
// storeIds
// store Ids in a sorted vector
void storeIds(int * ids, int nids)
{
  // put particles into a vector
  for (int i=0;i<nids;i++){
    CPartI p(i,ids[i]);
    pvec.push_back(p);
  }
  
  // sort vector of particles
  std::sort(pvec.begin(),pvec.end(),CPartI::mysort);
}

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
  fd.close();
}



} // namespace
