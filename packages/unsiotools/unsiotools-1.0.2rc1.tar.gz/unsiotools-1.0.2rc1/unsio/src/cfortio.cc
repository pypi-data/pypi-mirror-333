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
#include <cstdlib>
#include <sstream>
#include <iomanip>
#include "cfortio.h"
// ============================================================================
//
CFortIO::CFortIO()
{
}
// ============================================================================
//
CFortIO::~CFortIO()
{
  close();
}
// ============================================================================
//
void CFortIO::close()
{
  if (!fake_reading && in.is_open()) {
    in.close();
  }
}
// ============================================================================
// open() :                                                                    
// open file and return :                                                                                                       
int CFortIO::open(const std::string myfile, bool fake,bool _swap)
{
  int ret=1;
  fake_reading = fake;
  infile = myfile;
  swap = _swap;
  if (!fake_reading) {
    in.clear();
    in.open(myfile.c_str(),std::ios::in | std::ios::binary);
    if ( ! in.is_open()) {
      //std::cerr << "Unable to open file ["<<myfile<<"]...\n";
      ret=0;
    }
  }
  return ret;
}
