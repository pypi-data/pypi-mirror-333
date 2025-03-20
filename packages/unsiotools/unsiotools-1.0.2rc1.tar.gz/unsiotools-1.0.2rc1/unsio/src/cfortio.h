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
#ifndef CFORTIO_H
#define CFORTIO_H

#include <string>
#include <assert.h>
#include <fstream>
#include <iostream>

#define CHAR 1
class CFortIO
{
public:
  CFortIO();
  ~CFortIO();
  int open(const std::string myfile, bool _fake=false,bool _swap=false);
  void close();
  bool good() { 
    if (!fake_reading) return in.good();
    else return true;}
  inline int readDataBlock(char * ptr, bool abort=true) {
    if (!fake_reading) {
      int len1=readFRecord(abort);
      readData(ptr,1,len1);
      int len2=readFRecord(abort);
      if (len2==len1) ; // remove warning....
      if (abort)
        assert(good() && len1==len2);
      return len1;
    } else return 1;
  }
  inline std::streampos getPos() {
    return in.tellg();
  }
  inline void setPos(const std::streampos position) {
    in.seekg(position);
  }
  inline int readData(char * ptr,const size_t size_bytes,const  int items) {
    if (!fake_reading) {
      // get data from file
      in.read(ptr,size_bytes*items);
      //assert(in.good());
      if (! in.good()) return 0;
      
      // We SWAP data
      if (swap && (size_bytes != CHAR)) { // swapping requested
        for (int i=0; i<items; i++) {
          swapBytes(ptr,size_bytes);
          ptr += size_bytes;
        }
      }
    }
    return 1;
  }
  
  // read fortran record
  inline int readFRecord(bool abort=true) {
    if (!fake_reading) {
      int len; in.read((char *) &len,sizeof(int));
      // We SWAP data
      if (swap) { // swapping requested
        swapBytes(&len,sizeof(int));
      }
      if (abort)
        assert(in.good());
      else {
        if (! in.good()) len=0;
      }
      return len;
    } 
    else return 1;
  }
  // skip Block
  inline int skipBlock(int n=1) {
    int cpt=0;
    if (!fake_reading) {
      for (int i=0;i<n;i++) {
        int len1 = readFRecord();
        cpt+=len1;
        in.seekg(len1,std::ios::cur);
        int len2 = readFRecord();
        if (len2==len1) ; // remove warning....
        assert(in.good() && len1==len2);
      }      
    }
    return cpt;
}
private:
  std::ifstream in;
  bool swap;
  std::string infile;
  bool fake_reading;
  // swap bytes
  inline void swapBytes(void * x,const int size) {
    char * p=(char *) x;
    for (int i=0;i<size/2;i++) {
      int t=*(p+i); *(p+i)=*(p+size-i-1); *(p+size-i-1)=t;
    }
  }
};

#endif // CFORTIO_H
