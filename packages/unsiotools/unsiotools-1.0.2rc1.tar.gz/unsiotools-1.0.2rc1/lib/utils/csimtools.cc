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

#include <iostream>
#include <fstream>                                    // C++ file I/O
#include <cmath>
#include <sstream>
#include "csimtools.h"

using namespace jclut;
using namespace uns;
// ============================================================================
// constructor
CSimtools::CSimtools(CunsIn * _uns)
{
  unsin = _uns;
}
// ============================================================================
// loadCod
void CSimtools::loadCod()
{
  std::ifstream         // File Handler
      fd;               // manipfile file desc

  std::string codfile=unsin->snapshot->getSimDir()+
                      "ANALYSIS/"+
                      unsin->snapshot->getFileName()+".";
}

// ============================================================================

// ============================================================================

// ============================================================================
