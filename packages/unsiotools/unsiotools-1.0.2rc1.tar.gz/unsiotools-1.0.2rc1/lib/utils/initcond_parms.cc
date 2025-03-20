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
#include <cstring>                  
#include <assert.h>
#include <cstdio>
#include <iomanip>
#include <vector>
#include <map>
#include "csnaptools.h"
#include "uns.h"

using namespace jclut;
using namespace std;

namespace lia_lib_initcond {

std::string splitSetParam(std::string filename, std::string select);
  bool findPotex(std::string data, unsigned int &spos, int * rtype, float * rdata, char * rfile);
  void printMap(const std::map<std::string, int> &map_param, const std::map<std::string, int> &map_rtype);

extern "C" { // declare as extern to be called fron fortran and C
  // wrapper which can be called from a fortran program
  bool get_initcond_param_(const char * filename, const char * tag, float * dataf, char * datas, 
			   unsigned int l1, unsigned int l2, unsigned int l3);

  bool get_initcond_potex_(const char * filename, const char * tag,
			   int * rtype1, float * rdata1, char * rfile1,
			   int * rtype2, float * rdata2, char * rfile2,
			   int l1, int l2, int l3, int l4);

}
void printMap(const std::map<std::string, int> &map_param, const std::map<std::string, int> &map_rtype)
{
  // reversed maps
  std::map<int,std::string> rev_param;
  std::map<int,int        > rev_rtype;
  
  // reverse the maps
  std::map<std::string, int>::const_iterator itp,itr;
  for (itp=map_param.begin(),itr=map_rtype.begin(); itp != map_param.end(); ++itp, ++itr) {
    rev_param[itr->second] = itp->first;
    rev_rtype[itr->second] = itp->second;
  }

  // display sorted mad
  std::map<int,std::string>::const_iterator ritp;
  std::map<int,int        >::const_iterator ritr;
  for (ritp=rev_param.begin(),ritr=rev_rtype.begin(); ritp != rev_param.end(); ++ritp, ++ritr) {
    std::cout << "TAG = "         << setw(35)<< left<< ritp->second 
	      << " / #param="     <<                   ritr->second 
	      << " / return type="<<                   ritr->first
	      << std::endl;
  }

}
//------------------------------------------------------------------------------
// get_initcond_potex_
bool get_initcond_potex_(const char * filename, const char * tag,
			 int * rtype1, float * rdata1, char * rfile1,
			 int * rtype2, float * rdata2, char * rfile2,
			 int l1, int l2, int l3, int l4)
{
  bool status;
  float dataf;
  char  datas[200]; //
  if (l3 || l4 ) {;}
  status = get_initcond_param_(filename,tag,&dataf,datas,l1,l2,200);
  if (status) { // tag is valid
    std::string data(datas);
    // split the string to a vector
    std::vector<std::string> parse=CSnaptools::stringToVector<std::string>(data,0,"");
    status=false;
    unsigned int spos=0; // position in the data string
    if (findPotex(data,spos,rtype1,rdata1,rfile1)) {
      status=true;
      if (spos<parse.size()) { // a second tag should exist ?
	std::cerr << "Trying a second tag\n";
	if (findPotex(data,spos,rtype2,rdata2,rfile2)) { // 2nd potex exist
	  status=true;
	} else { // 2nd potex does not exist, error !
	  std::cerr << "Error while detecting second tag...aborting\n";
	  status=false;
	}
      }
    }
  } else {  // tag is not valid
    std::cerr << "Tag ["<<tag<<"] unknown....\n";
  }
  return status;
}
//------------------------------------------------------------------------------
// findPotex
bool findPotex(std::string data,unsigned int &spos, int * rtype, float * rdata, char * rfile)
{
  bool status=false;

  // build maps
  std::map<std::string, int> map_param, map_rtype;
  std::string pot;

  // 
  //  Spherical symmetric systems
  int type=1;
  pot="plum,a#M_tot";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="hernq,a#M_tot";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="dehnen,gamma#a#M_tot";
  map_param[pot] = 3;
  map_rtype[pot] = type++;

  pot="loghalo,a#v_inf";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="nfw,a#C";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="nfw,a#M0";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="h93halo,r_core#r_cutoff#M_tot";
  map_param[pot] = 3;
  map_rtype[pot] = type++;

  pot="liahalo,rc#rs#gamma#a#b#rt#C";
  map_param[pot] = 7;
  map_rtype[pot] = type++;


  //
  // Axissymetrics systems
  type=100;
  pot="exp_disk,h#z0#M_tot";
  map_param[pot] = 3;
  map_rtype[pot] = type++;

  pot="miynag,a#b#M_tot";
  map_param[pot] = 3;
  map_rtype[pot] = type++;

  pot="GalPot,file";
  map_param[pot] = 1;
  map_rtype[pot] = type++;

  //
  // Axial systems
  type=200;
  pot="ferrers,a#b#c#p#ro0";
  map_param[pot] = 5;
  map_rtype[pot] = type++;


  // Cuting or modifications
  type=500;
  pot="sph_expcut,r_cut";
  map_param[pot] = 1;
  map_rtype[pot] = type++;

  pot="sph_dehnencut,r1#r2";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="cyl_expRcut,R_cut";
  map_param[pot] = 1;
  map_rtype[pot] = type++;

  pot="cyl_dehnenRcut,R1#R2";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="cylfromsph,a#c";
  map_param[pot] = 2;
  map_rtype[pot] = type++;

  pot="3dfromsph,a#b#c";
  map_param[pot] = 3;
  map_rtype[pot] = type++;

  // printing
  //printMap(map_param, map_rtype);

  // split the string to a vector of strings
  std::vector<std::string> parse=CSnaptools::stringToVector<std::string>(data,0,"");
  
  if (parse.size()-spos >=2) { // enough strings
    std::string model=parse[spos]+","+parse[spos+1]; // build potex string
    spos+=2;
    std::cerr << "Trying tag = " << model << "\n";
    int index=0;

    // test if key exist
    std::map<std::string, int>::const_iterator it=map_param.find(model);
    if (it == map_param.end()){
      std::cerr << "findPotex :: error, map not find = "<<model<< "\n";
    } else {
      //std::cerr << "map_param="<<map_param[model]<<"\n";
      //std::cerr << "map_rtype="<<map_rtype[model]<<"\n";
      if ((int)(parse.size()-spos)>=map_param[model]) { // enough parameters ?
	*rtype=map_rtype[model]; // return type
	bool error=false;
	for (int i=0;i<map_param[model];i++) {
	  float dataf;
	  if (! CSnaptools::isStringANumber<float>(parse[spos],dataf)) {
	    if (map_param[model] == 1) {
	      std::cerr << "findPotex:: assuming that the parameter["<<parse[spos]<<"] is a file...\n";
	      strcpy(rfile,parse[spos].c_str());
	    } else {
	      std::cerr << "findPotex :: error, parsing ["<<parse[spos]<<"] is not a number !!\n";
	      error=true;
	    }
	  } else { // it's a number
	    rdata[index++] = dataf; // return value
	  }
	  spos++; // shift spos index
	}
	if (!error) {
	  status=true;
	  //spos+=map_param[model];
	}
      } else {
	std::cerr << "findPotex :: there are not enough remaining parameters\n";
	std::cerr << "parse.size="<<parse.size()<<" spos="<<spos<<" map_rtype="<<map_rtype[model]<<"\n";
      }
    }
  }
  return status;
}
//------------------------------------------------------------------------------
// get_initcond_param_
bool get_initcond_param_(const char * _filename, const char * _tag, float * dataf, char * _datas, unsigned int l1, unsigned int l2, unsigned int l3)
{  

  bool status=false;
  std::string filename  = tools::Ctools::fixFortran(_filename,l1,false);
  std::string tag       = tools::Ctools::fixFortran(_tag,l2,false);
  std::string datas     = tools::Ctools::fixFortran(_datas,l3,false);

  std::string param=splitSetParam(filename,tag);
  std::cerr << "Param = "<< param << "\n";
  datas[0]='\0';
  if (param.length() > 0) {
    status=true;
    if (l3<param.length()) {
      std::cerr << "The string to store value is not long enough, aborting....\n";
      std::exit(1);
    }
    strcpy(_datas,param.c_str());

    // check if tag is a number
    if (CSnaptools::isStringANumber<float>(param,*dataf)) {
      std::cerr << "Float = "<< *dataf << "\n";
    } else {
      *dataf=-666.666;
    }
  } else {
    *dataf=-666.666;
    param="none";
    strcpy(_datas,param.c_str());
  }  
  // add trailing blank for fortran string compatibility
  for (unsigned int i=param.length();i<l3;i++) {
    _datas[i]=' ';
  }
  return status;
}

//------------------------------------------------------------------------------
// splitSetParam
std::string splitSetParam(std::string filename, std::string select)
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
	  size_t found=parse.find(select);
          if (found!=std::string::npos &&         // we found the key ! ex:rmax rmax=300
              ((found>0&&parse[found-1]==' ') ||  // and previous character is empty
               (found == 0))) {                   // or  select at the beginning
	    size_t found=parse.find("=");
	    if (found!=std::string::npos) {   // we found the = !
	      param = parse.substr(found+1);  //    copy 300 to param
	      while ((found=param.find("'"))!=std::string::npos) {
	      	param.replace(found,1,"");
	      }
	      match=true;
	    }
          }
        }        
      }
    }
    fd.close();
  }
  return param;
}
} 
//------------------------------------------------------------------------------
// End
