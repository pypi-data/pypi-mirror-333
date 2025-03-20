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
#include "uns.h"
#include <nemo.h>

namespace lia_lib_get_param_sim {
// C++ implementation
std::string getParam(std::string simname, std::string filename, std::string select, bool verbose);
std::string processParam(std::string filename, std::string select);

extern "C" { // declare as extern to be called from fortran and C
// wrapper which can be called from a fortran program
int get_param_simu_(const char * filename, const char * select, float * data, int l1, int l2);
int get_param_model_(const char * filename, const char * select, float * data, int l1, int l2);
int get_last_info_(const char * filename, const char * select, float * data, int l1, int l2);
}

//------------------------------------------------------------------------------
// get_last_info_
int get_last_info_(const char * _name, const char * _field, float * data, int l1, int l2)
{
  int ret=0;
  std::string simname  = tools::Ctools::fixFortran(_name,l1,false);
  std::string field = tools::Ctools::fixFortran(_field,l2,false);
  std::string value=getParam(simname,"final_time.txt", field, false);
  if (value.length()>0) {
    ret=1;
    std::istringstream istr(value);
    istr >> *data;
    //std::cerr << "Data = " << *data << "\n";
  }
  return ret;
}
//------------------------------------------------------------------------------
// get_param_model_
int get_param_model_(const char * _name, const char * _field, float * data, int l1, int l2)
{  
  int ret=0;
  std::string simname  = tools::Ctools::fixFortran(_name,l1,false);
  std::string field = tools::Ctools::fixFortran(_field,l2,false);
  std::string value=getParam(simname,"model_param.txt", field, false);
  if (value.length()>0) {
    ret=1;
    std::istringstream istr(value);
    istr >> *data;
    //std::cerr << "Data = " << *data << "\n";
  }
  return ret;
}
//------------------------------------------------------------------------------
// get_param_simu_
int get_param_simu_(const char * _name, const char * _field, float * data, int l1, int l2)
{  
  int ret=0;
  std::string simname  = tools::Ctools::fixFortran(_name,l1,false);
  std::string field = tools::Ctools::fixFortran(_field,l2,false);
  std::string value=getParam(simname,"gadget.param", field, false);
  if (value.length()>0) {
    ret=1;
    std::istringstream istr(value);
    istr >> *data;
    //std::cerr << "Data = " << *data << "\n";
  }
  return ret;
}
//------------------------------------------------------------------------------
// processParam
std::string processParam(std::string filename, std::string select)
{
  std::ifstream         // File Handler
    fd;                 // file desc
  std::string param="";
  
  // open simulation param file
  fd.open(filename.c_str(),std::ios::in);
  if ( ! fd.is_open()) {
    std::cerr <<
      "Unable to open ["<<filename<<"] for input\n\n";
    param="";
  } 
  else {
    bool stop=false;
    // Read  file
    while (! fd.eof() && !stop) {           // while ! eof
      std::string line;
      getline(fd,line);
      if ( ! fd.eof()) {
        std::istringstream istr(line);  // stream line      
        std::string parse;
        // parse first variable read
        bool match=false;
        while ( istr >> parse   &&      // something to read 
                parse[0] != '#' &&      // not commented 
                parse[0] != '%' &&      // not commented
                parse[0] != ';' &&      // not commented
                !match      )      {    // not yet found
          if (parse==select) {   // we found the key !
            istr >> param;
            match=true;
          }
        }        
      }
    }
    fd.close();
  }
  return param;
}
//------------------------------------------------------------------------------
// getParam
std::string getParam(std::string simname,std::string filename,  std::string select, bool verbose)
{
  std::string ret="";
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * unsin = new uns::CunsIn(simname,"all","all",verbose);
  
  if (unsin->isValid()) { // input file is known by UNS lib        
      std::string  param=unsin->snapshot->getSimDir()+"/"+filename;
      std::cerr << "File :"<<param<<"\n";
      ret = processParam(param, select);
      if (ret.length()>0) {
        //std::cerr << "found:"<<select << " : "<< ret << "\n";
      }
  } else {
    std::cerr << "Unknown UNS file format["<<simname<<"]\n";
  }
  delete unsin;  
  
  return ret;
}
} // namespace
//------------------------------------------------------------------------------
// End
