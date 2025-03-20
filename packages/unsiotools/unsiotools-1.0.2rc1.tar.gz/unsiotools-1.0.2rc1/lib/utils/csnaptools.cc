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
#include <assert.h>
#include <cstring>
#include <algorithm>
#include <cvecutils.h>
#include "csnaptools.h"

using namespace jclut;
#define   MyPI         3.141592653589793238462643
#define DEG2RAD MyPI/180.0

//
// ----------------------------------------------------------------------------
// isFileExist
bool CSnaptools::isFileExist(std::string test_file, bool abortOnFalse)
{
    bool ok=false;
    std::ifstream fd; // file descriptor

    fd.open(test_file.c_str(), std::ios::in); // open file

    if (fd.is_open()) {
        ok=true;
        fd.close();
    }
    else ok = false;
    if (!ok && abortOnFalse) {
      std::cerr << "File [" << test_file << "] does not exist, aborting...\n";
      std::exit(1);
    }
    return ok;
}

//
// ----------------------------------------------------------------------------
// getTimeDataFile
template <class T>  bool CSnaptools::getTimeDataFile(std::string input_file,const T time,const int n,T data[],const T offset,const  bool verbose)
{
  bool ok=false;
  std::ifstream fd; // file descriptor
  if (verbose) {;}
  fd.open(input_file.c_str(), std::ios::in); // open file

  if (fd.is_open()) {
    bool stop=false;
    std::string line;

    while (!stop && ! fd.eof() ) {
      // Read line
      getline(fd,line);
      if (! fd.eof()) {
        double r_time;
        std::istringstream ss(line);
        ss >> r_time;
        if (r_time-offset <= time && time <= r_time+offset) { // found good time
          stop = true;
          ok = true;
          for (int i=0; i<n; i++) { // read cod
            ss >> data[i];
          }
        }
      }
    }
  }
  if (fd.is_open()) {
      fd.close();
  }
  return ok;

}
template bool CSnaptools::getTimeDataFile<float>(std::string input_file,const float time,const int n,float data[],const float offset,const  bool verbose);
template bool CSnaptools::getTimeDataFile<double>(std::string input_file,const double time,const int n,double data[],const double offset,const  bool verbose);
//
// ----------------------------------------------------------------------------
// fixFortran
std::string CSnaptools::fixFortran(const char * _ff, const bool lower)
{
  static char buff[200], * p;
  memset( buff, '\0', 200 );
  if (lower) {;}
  //std::cerr << "Fortran string ["<<_ff<<"]\n";
  
  p=(char *) strchr(_ff,'\\');
  if (p) {
    //std::cerr << "Got \\ \n";
    assert (p-_ff<=200);
    strncpy(buff,_ff,p-_ff);
  }
  else {
    p=(char *) strchr(_ff,'#');
    if (p) {
      //std::cerr << "Got #\n";
      assert (p-_ff<=200);
      strncpy(buff,_ff,p-_ff);
    } else {
      //std::cerr << "Got nothing.....\n";
      strcpy(buff,_ff);
    }
  } 
  //std::cerr << "Buff ["<<buff<<"]\n";
  if (lower)
    return tolower(std::string(buff));
  else
    return std::string(buff);
}
//
// ----------------------------------------------------------------------------
// fixFortran
std::string CSnaptools::fixFortran(const char * _ff, const int len, const bool lower)
{
  char * buff = new char[len+1];
  strncpy(buff,_ff,len);
  buff[len]='\0';
  std::string str=buff;
  delete [] buff;
  if (lower) {;}
  std::cerr << "fix_fortran =["<<str<<"]\n";
  
  size_t found;
  found=str.find_last_not_of(" ");
  if (found!=std::string::npos)
    str.erase(found+1);
  else
    str.clear();            // str is all whitespace
  
  std::cerr << '"' << str << '"' << std::endl;
  
  return str;
}
// ----------------------------------------------------------------------------
// tolower
std::string CSnaptools::tolower(std::string s)
{
  std::transform(s.begin(),s.end(),s.begin(),(int(*)(int)) std::tolower);
  return s;
}
// ----------------------------------------------------------------------------
// tolupper
std::string CSnaptools::toupper(std::string s)
{
  std::transform(s.begin(),s.end(),s.begin(),(int(*)(int)) std::toupper);
  return s;
}

//
// moveToCod
// move particles positions and velocities to center of density
//template <class T> void CSnaptools<T>::moveToCod(const int nbody,T * pos, T * mass)
template <class T> void CSnaptools::moveToCod(const int nbody,T * pos,T * vel, T * mass, T * rho, double cod[6], bool move, bool verbose)
{
  double codp[3] = {0., 0., 0.};
  double codv[3] = {0., 0., 0.};
  double w_i, w_sum=0.0;
  // loop on all the bodies
  for (int i=0; i<nbody;i++) {
    w_i    = rho[i] * mass[i]; // weight = rho * mass
    w_sum += w_i;              // sum
    if (pos) {
      codp[0] +=(pos[i*3  ]*w_i);
      codp[1] +=(pos[i*3+1]*w_i);
      codp[2] +=(pos[i*3+2]*w_i);
    }
    if (vel) {
      codv[0] +=(vel[i*3  ]*w_i);
      codv[1] +=(vel[i*3+1]*w_i);
      codv[2] +=(vel[i*3+2]*w_i);
    }    
  }
  assert(w_sum>0.0); // total weight must be positif
  if (pos) {
    codp[0] /= w_sum;
    codp[1] /= w_sum;
    codp[2] /= w_sum;
  }
  cod[0] = codp[0]; cod[1] = codp[1]; cod[2] = codp[2];
  if (vel) {
    codv[0] /= w_sum;
    codv[1] /= w_sum;
    codv[2] /= w_sum;
    
  }
  cod[3] = codv[0]; cod[4] = codv[1]; cod[5] = codv[2];
  if (verbose) {
    std::cerr << "COD = " << cod[0]<<" "<< cod[1]<<" "<< cod[2]<<" "
        << cod[3]<<" "<< cod[4]<<" "<< cod[5]<<"\n";
  }
  if (move) {
    // move to cod requested
    for (int i=0; i<nbody;i++) {
      for (int j=0;j<3;j++) {
        if (pos)
          pos[i*3+j] -= codp[j]; // pos
        if (vel)
          vel[i*3+j] -= codv[j]; // vel
      }
    }
  }
}
template void CSnaptools::moveToCod(const int nbody,float * pos,float * vel, float * mass, float * rho, double cod[6], bool move, bool verbose);
template void CSnaptools::moveToCod(const int nbody,double * pos,double * vel, double * mass, double * rho, double cod[6], bool move, bool verbose);
//
// moveToCom
// move particles positions to center of mass
//template <class T> void CSnaptools<T>::moveToCom(const int nbody,T * pos, T * mass)
template <class T> void CSnaptools::moveToCom(const int nbody,T * data, T * mass, bool verbose)
{
  double com[3] = {0., 0., 0.};
  double np=0.,masstot=0;;
  for (int i=0; i<nbody;i++) {
    float massi;
    if (mass) massi = mass[i];
    else      massi = 1.0;
    masstot+=massi;
    np++;
    int jndex= i;
    com[0] +=(data[jndex*3  ]*massi);
    com[1] +=(data[jndex*3+1]*massi);
    com[2] +=(data[jndex*3+2]*massi);
  }
  if (!mass) {
    std::cerr << "No mass in the snapshot, we assum mass=1.0 for each particles...\n";
  }
  if (verbose) {
    std::cerr <<"COM     ="<<com[0]<<" "<<com[1]<<" "<<com[2]<<"\n";
    std::cerr <<"np      ="<<np<<"\n";
    std::cerr <<"mass tot="<<masstot<<"\n";
  }
  // center
  for (int i=0; i<nbody;i++) {
    data[i*3+0] -= (com[0]/masstot);
    data[i*3+1] -= (com[1]/masstot);
    data[i*3+2] -= (com[2]/masstot);
  }  
}
template void CSnaptools::moveToCom<float>(const int nbody,float * pos, float * mass, bool verbose);
template void CSnaptools::moveToCom<double>(const int nbody,double * pos, double * mass, bool verbose);
//
// basename
std::string  CSnaptools::basename(const std::string str)
{
  size_t found=str.find_last_of("/\\");
  return str.substr(found+1);
}

//
// dirname
std::string CSnaptools::dirname(const std::string str)
{
  size_t found=str.find_last_of("/\\");
  return str.substr(0,found);
}
//
// parseString
std::string CSnaptools::parseString(std::string & next_string, const std::string sep)
{
  std::string return_string;
  std::string::size_type coma=next_string.find(sep,0);  // try to find separator sep ","
  if (coma != std::string::npos) { // found "separator"
    return_string = next_string.substr(0,coma);
    next_string   = next_string.substr(coma+1,next_string.length());
  } else {                         // not found
    return_string = next_string;
    next_string = "";
  }
  return return_string;
  
}
//
// isStringANumber
// return true if string is a number of type T. Set data to this number
template <class T> bool CSnaptools::isStringANumber(const std::string mystring, T &data)
{
  bool status=true;
  std::stringstream stream("");
  stream << mystring;
  stream >> data;
  if (! stream.eof()) {
    //std::cerr << "conversion failed\n";
    status=false;
  }
  return status;
}
template bool CSnaptools::isStringANumber<double>(const std::string mystring, double &data);
template bool CSnaptools::isStringANumber<float> (const std::string mystring, float  &data);
template bool CSnaptools::isStringANumber<int>   (const std::string mystring, int    &data);
//
// mapStringVectorIndexes
// should parse strings like : gas@0:100,200:3000:2+disk@1000:2000
// into a map string of vector
// gas  vec[0:100,200:3000:2]
// disk vec[1000:2000]
std::map<std::string, std::vector<int> > CSnaptools::mapStringVectorIndexes(const std::string s, const int max, std::string sep1,std::string sep2,std::string sep3)
{
  std::map<std::string, std::vector<int> > sOfv;
  std::string current_s,next_s;
  next_s = s;              // string to be parsed
 
  // parse a+b+c
  while ((current_s=parseString(next_s,sep1)) != "") {  // look for XXXX,YYYY,ZZZZ strings
    // current_s =  gas@0:100,200:300  
    std::string comp=parseString(current_s,sep2); // 
    // comp=gas current_s=0:100,200:300
    std::vector<int> vec=CSnaptools::rangeToVectorIndexes<int>(current_s,max,sep3);
    sOfv[comp]=vec;
  }
  return sOfv;
}

//
// rangeToVector
template <class T> std::vector<T> CSnaptools::rangeToVectorIndexes(const std::string s, const int max, std::string sep)
{
  std::string current_s,next_s;
  next_s = s;              // string to be parsed
  
  std::vector <T> vec;
  // parse 
  while ((current_s=parseString(next_s,sep)) != "") {  // look for XXXX,YYYY,ZZZZ strings
    // look for   a[:b[:c]] sting
    T va,vb,vc=(T)1;
    std::string a=parseString(current_s,":");
    if (a=="all") { // special case for all
      va=0; vb=max-1;
      // feed up the vector
      while (va <= vb) {
        vec.push_back(va);
        va += vc;
      }
    }
    else { 
      if (a!="") { // a ?
        va = stringToNumber<T>(a);
        std::string b =parseString(current_s,":");
        if (b!="") { // b ?
          vb = stringToNumber<T>(b);
          std::string c =parseString(current_s,":");
          if (c!="") { // c ?
            vc = stringToNumber<T>(c);
          } // c 
          else vc = (T)1;
        } // b 
        else vb = va;
        // feed up the vector
        while (va <= vb) {
          vec.push_back(va);
          va += vc;
        }
      } // a 
    }
  }
  return vec;  
}
template std::vector<float > CSnaptools::rangeToVectorIndexes<float >(const std::string s, const int max, std::string sep);
template std::vector<double> CSnaptools::rangeToVectorIndexes<double>(const std::string s, const int max, std::string sep);
template std::vector<int   > CSnaptools::rangeToVectorIndexes<int   >(const std::string s, const int max, std::string sep);
//
// stringToVector
template <class T>  std::vector<T> CSnaptools::stringToVector(const std::string s, const int min, T val, std::string sep)
{
  std::string current_s,next_s;
  next_s = s;              // string to be parsed
  
  std::vector <T> vec;
  T value;
  // parse 
  while ((current_s=parseString(next_s,sep)) != "") {  
    std::stringstream parse(""); // string parsed
    parse << current_s;      // read value
    parse >> value;          // convert value
    vec.push_back(value);
  }
  // complete to default value if size < min
  for (int i=vec.size(); i<min; i++) {
    vec.push_back(val); // default value;
  }  
  return vec;
}
template std::vector<float > CSnaptools::stringToVector<float >(const std::string s, const int min, float  val, std::string sep);
template std::vector<double> CSnaptools::stringToVector<double>(const std::string s, const int min, double val, std::string sep);
template std::vector<int   > CSnaptools::stringToVector<int   >(const std::string s, const int min, int    val, std::string sep);
template std::vector<std::string> CSnaptools::stringToVector<std::string  >(const std::string s, const int min, std::string  val, std::string sep);
//
// minArray
template <class T> T CSnaptools::minArray(const int nbody, const T * array)
{
  T min = array[0];
  for (int i=1;i<nbody;i++) {
    min = std::min(min,array[i]);
  }
  return min;
}
template float  CSnaptools::minArray(const int nbody, const float  * array);
template double CSnaptools::minArray(const int nbody, const double * array);
template int    CSnaptools::minArray(const int nbody, const int    * array);
//
// maxArray
template <class T> T CSnaptools::maxArray(const int nbody, const T * array)
{
  T max = array[0];
  for (int i=1;i<nbody;i++) {
    max = std::max(max,array[i]);
  }
  return max;
}
template float  CSnaptools::maxArray(const int nbody, const float  * array);
template double CSnaptools::maxArray(const int nbody, const double * array);
template int    CSnaptools::maxArray(const int nbody, const int    * array);
//
// zrotate
template <class T>  void CSnaptools::zrotate(const int nbody,T * pos, T * vel, T * acc,const double angle) {

  T rmat[NDIM][NDIM];
  int i;

  vectutils::setmi(rmat);
  rmat[0][0] =    rmat[1][1] = cos(DEG2RAD * angle);
  rmat[0][1] =  -(rmat[1][0] = sin(DEG2RAD * angle));	/* PJT */

  for (i = 0; i < nbody; i++) {
    if (pos) CSnaptools::rotatevec(pos+i*3, &rmat[0][0]);
    if (vel) CSnaptools::rotatevec(vel+i*3, &rmat[0][0]);
    if (acc) CSnaptools::rotatevec(acc+i*3, &rmat[0][0]);
  }

}
template void CSnaptools::zrotate (const int nbody,float  * pos, float  * vel, float  * acc,const double angle);
template void CSnaptools::zrotate (const int nbody,double * pos, double * vel, double * acc,const double angle);

template <class T>  void CSnaptools::rotatevec(T * vec, T * mat) {
  T tmp[3];

  vectutils::mulmv(tmp, mat , vec);
  vectutils::setv(vec, tmp);
}
template void CSnaptools::rotatevec(float  * vec, float  * mat);
template void CSnaptools::rotatevec(double * vec, double * mat);

//
// Fortran Interface
//
extern "C" {
   // center positions and velocities according to cod
   //
    void center_on_cod_file_(const char * codfile, const float * time, const int * nbody,float * pos, float * vel, float * mass, const int lenstring ) {
     std::string filename=jclut::CSnaptools::fixFortran(codfile,lenstring);
     double cod[6];
     bool is_codfile=false;
     if (mass) {;}
     jclut::CSnaptools::isFileExist(filename,true);
     is_codfile=jclut::CSnaptools::getTimeDataFile<double>(filename,(double)(*time),6,cod, 0.001);
     if (! is_codfile ) {
       std::cerr << "From file ["<<filename<<"] unable to find corresponding time ["<<*time<<"]"
                 << "aborting program....\n";
       std::exit(1);
     }
     // move to cod requested
     for (int i=0; i<*nbody;i++) {
       for (int j=0;j<3;j++) {
         if (pos)
           pos[i*3+j] -= cod[j]; // pos
         if (vel)
           vel[i*3+j] -= cod[3+j]; // vel
       }
     }
   }
   // rotate pos, vel and acc around z axis according to angle
   //
   void derotate_f_(const char * rotatefile, const float * time,const int * nbody,float * pos, float * vel, float * acc, const int lenstring ) {
     std::string filename=jclut::CSnaptools::fixFortran(rotatefile,lenstring);
     bool is_rectfile=false;
     double data[1];
     jclut::CSnaptools::isFileExist(filename,true);
     is_rectfile=jclut::CSnaptools::getTimeDataFile<double>(filename,(double)(*time),1,data, 0.001);
     if (! is_rectfile ) {
       std::cerr << "From file ["<<filename<<"] unable to find corresponding time ["<<*time<<"]"
                 << "aborting program....\n";
       std::exit(1);
     }
     std::cerr << "From file ["<<filename<<" time "<< *time << " angle="<<data[0] << "\n";
     jclut::CSnaptools::zrotate(*nbody,pos,vel,acc,-data[0]);
   }
}
