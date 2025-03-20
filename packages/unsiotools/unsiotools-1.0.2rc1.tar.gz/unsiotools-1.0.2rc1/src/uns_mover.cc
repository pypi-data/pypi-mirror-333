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
//-----------------------------------------------------------------------------+
#include <iostream>                                // C++ I/O                   
#include <fstream>                                 // C++ file I/O              
#include <iomanip>                                 // C++ I/O formatting        
#include <sstream>
#include <assert.h>
#include <nemo.h>
#include "uns.h"
//------------------------------------------------------------------------------
const char * defv[] = {
  "in=???\n           UNS input file                                     ",
  "out=???\n          output file for snapshots (NEMO format)            ",
  "select=???\n       component selected (disk,stars,halo,gas,range,all) ",
  "times=all\n        selected time                                      ",
  "xrot=\n            rotation about x axis, done first  (degrees)       ",
  "yrot=\n            rotation about y axis, done second (degrees)       ",
  "zrot=\n            rotation about z axis, done third  (degrees)       ",
  "first=f\n          add a trailing numbering to the first output file  ",
  "offset=0.01\n      +/- time offset                                    ",
  "verbose=f\n        verbose mode                                       ",
   NULL };
//------------------------------------------------------------------------------
const char * usage = "uns_mover - rotates UNS snapshots\n";
//------------------------------------------------------------------------------
using namespace std; // prevent writing statment like 'std::cerr'
//------------------------------------------------------------------------------
// rotatex
void rotatex (const double _cxr,
	      const double _sxr,
	      double &_y,  double &_z,
	      double &_vy, double &_vz){

  register double newy=_cxr*_y + _sxr*_z, newvy=_cxr*_vy + _sxr*_vz;

  _z  = _cxr*_z  - _sxr*_y;
  _vz = _cxr*_vz - _sxr*_vy;
  _y  = newy;
  _vy = newvy;
}
//------------------------------------------------------------------------------
// rotatey
void rotatey (const double _cyr,
	      const double _syr,
	      double &_x,  double &_z,
	      double &_vx, double &_vz){

  register double newx=_cyr*_x - _syr*_z, newvx=_cyr*_vx - _syr*_vz;

  _z  = _cyr*_z  + _syr*_x;
  _vz = _cyr*_vz + _syr*_vx;
  _x  = newx;
  _vx = newvx;
}
//------------------------------------------------------------------------------
// rotatez
void rotatez (const double _czr,
	      const double _szr,
	      double &_x,  double &_y,
	      double &_vx, double &_vy){

  register double newx=_czr*_x + _szr*_y, newvx=_czr*_vx + _szr*_vy;

  _y  = _czr*_y  - _szr*_x;
  _vy = _czr*_vy - _szr*_vx;
  _x  = newx;
  _vx = newvx;
}
double xr,yr,zr;
double cxr,sxr,cyr,syr,czr,szr;
//------------------------------------------------------------------------------
// processComponent
// read pos,vel,mass of the components
// if component exist AND it has been selected, then respecting comp's data are
// prepared to be saved
void processComponent(std::string comp, uns::CunsIn * uns,
                      uns::CunsOut * unsout)
{
  float * pos, * vel, * mass;
  int n1,n2,n3;
  bool ok1,ok2,ok3;
  
  ok1 = uns->snapshot->getData(comp,"pos" ,&n1,&pos );
  ok2 = uns->snapshot->getData(comp,"vel" ,&n2,&vel );
  ok3 = uns->snapshot->getData(comp,"mass",&n3,&mass);
  if (ok1 && ok2 && ok3) {
    assert(n1==n2);
    assert(n1==n3);
    std::cerr << "--> "<< std::left << std::setfill('.')<<
        std::setw(8) << comp << ":" << std::setfill(' ')<<
        std::right   << std::setw(10) << n1 <<"\n";
    for (int i=0;i<n1;i++) {
      double 
          tmpx =pos[i*3+0],
          tmpy =pos[i*3+1],
          tmpz =pos[i*3+2],
          tmpvx=vel[i*3+0],
          tmpvy=vel[i*3+1],
          tmpvz=vel[i*3+2];
      
      if(xr) rotatex(cxr,sxr,tmpy,tmpz,tmpvy,tmpvz);
      if(yr) rotatey(cyr,syr,tmpx,tmpz,tmpvx,tmpvz);
      if(zr) rotatey(czr,szr,tmpx,tmpy,tmpvx,tmpvy);

      pos[i*3+0] = tmpx;
      pos[i*3+1] = tmpy;
      pos[i*3+2] = tmpz;
      vel[i*3+0] = tmpvx;
      vel[i*3+1] = tmpvy;
      vel[i*3+2] = tmpvz;      
    }
    unsout->snapshot->setData(comp,n1,mass,pos,vel,false);
    
  }  
}
                                                                 
//------------------------------------------------------------------------------
// main
int main(int argc, char ** argv )
{
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  if (argc) {;} // remove compiler warning :)
  // Get input parameters
  std::string simname (getparam ((char *) "in"      ));
  std::string outname (getparam ((char *) "out"     ));
  std::string select_c(getparam ((char *) "select"  ));
  
  std::string select_t(getparam ((char *) "times"   ));
  bool first         = getbparam((char *) "first"    );
  float       offset = getdparam((char *) "offset"   );
  bool        verbose= getbparam((char *) "verbose"  );
  
  xr    = 0.017453292*(getdparam((char *) "xrot"    ));
  yr    = 0.017453292*(getdparam((char *) "yrot"    ));
  zr    = 0.017453292*(getdparam((char *) "zrot"    ));
    
  bool one_file=false;
  bool stop=false;
  
  
  cxr=cos(xr);sxr=sin(xr);
  cyr=cos(yr);syr=sin(yr);
  czr=cos(zr);szr=sin(zr);

  // in case of an input simulation from the database
  // and with just one time requested,
  // we create a range of time to speedup the searching
  if (select_t!="all" && select_t.find(":",0)==std::string::npos) {
    float match_time;
    stringstream ss("");
    ss << select_t;
    ss >> match_time; // convert string time to float
    ss.str(std::string()); // empty stringstream
    ss.clear();            // empty stringstream (mandatory after >>)
    ss << match_time-offset<<":"<<match_time+offset;
    select_t = ss.str();
    one_file=true;
    std::cerr << "Modified selected time =["<<select_t<<"]\n";
  }
  
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * unsin = new uns::CunsIn(simname,select_c,select_t,verbose);
  int cpt=0;
  if (unsin->isValid()) { // input file is known by UNS lib        
    while(unsin->snapshot->nextFrame("mxv")&&!stop) { // there is a new frame
      //std::string itype = unsin->snapshot->getInterfaceType();

      int nbody;      
      float time;
      // get the input number of bodies according to the selection
      unsin->snapshot->getData("nsel",&nbody);
      // get the simulation time
      unsin->snapshot->getData("time",&time);
      //      
      std::cerr << "nbody=" << nbody << " time="<<time <<"\n";
      if (nbody>0) { // there are particles
        // OUTPUT operations
        // create an output filename : basename +  integer
        // example : myoutput.0 myoutput.1 ...... etc
        stringstream number("");
        number << cpt++;
        std::string out_name;
        if (one_file || (cpt==1 && !first)) {
          out_name=std::string(outname);
          if (one_file) stop = true; // do not continue
        } else {
          stringstream ss("");
          ss << std::string(outname) << "." << setw(5) << setfill('0') << number.str();
          //out_name=std::string(outname)+"."+number.str();
          out_name=ss.str();
        }
        std::cerr << "output filename=["<<out_name<<"]\n";
        // -----------------------------------------------
        // Instantiate a UNS output snapshot in "nemo" format (for writing)
        uns::CunsOut * unsout = new uns::CunsOut(out_name,"nemo",verbose);      
        // save time
        unsout->snapshot->setData("time",time);
        // processing
        processComponent("all"  ,unsin,unsout); // only all particles selected
        // save snapshot
        unsout->snapshot->save();
        delete unsout; // remove object      
      }
    }
  } else {
    std::cerr << "Unknown UNS file format["<<simname<<"]\n";
  }
  delete unsin;
  //   finish NEMO
  finiparam();
}
 
