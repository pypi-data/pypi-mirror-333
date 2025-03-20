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
#ifndef CSIMTOOLS_H
#define CSIMTOOLS_H
#include "uns.h"
using namespace uns;
namespace jclut {
  
  class CSimtools
  {
  public:
    CSimtools(CunsIn *);
    
    
  private:
    CunsIn * unsin;
    
    void loadCod();
  };
}
#endif // CSIMTOOLS_H
