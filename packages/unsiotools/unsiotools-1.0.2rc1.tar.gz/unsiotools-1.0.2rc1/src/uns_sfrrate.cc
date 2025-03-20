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
#include "ctree.h"
#include "cneibors.h"
#include "ctimer.h"
#include <nemo.h>       

using namespace std; // prevent writing statment like 'std::cerr'
using namespace jcltree;
using namespace jclut;

class CHII {
public:
  CHII (const float _x, const float _y, const float _z,
        const float _sradius, const float _mass):x(_x),y(_y),z(_z),sradius(_sradius),mass(_mass) {

  }
  const CHII& operator=(const CHII& m) {
    x = m.x;
    y = m.y;
    z = m.z;
    sradius = m.sradius;
    mass = m.mass;
    return *this;
  }
  float getX() { return x; }
  float getY() { return y; }
  float getZ() { return z; }
  float getSRadius() { return sradius; }
  float getMass() { return mass; }

private:
  float x,y,z,sradius,mass;
};

typedef std::vector <CHII> CHIIVector;
CHIIVector chiiv;
//------------------------------------------------------------------------------
//                             M   A   I   N                                    
//------------------------------------------------------------------------------
// NEMO parameters
const char * defv[] = {  // use `::'string because of 'using namespace std'
  "in=???\n            input file uns file (ramses preferred)        ",
  "out=???\n           output file (NEMO format)     ",
  "agemax=30\n         maximum age of stars",
  "times=all\n         selected time                   ",
  "first=f\n           add a trailing numbering to the first output file",
  "offset=0.01\n       +/- time offset",
  "verbose=f\n         verbose mode                    "
  "VERSION=1.0\n       compiled on <" __DATE__ "> JCL   ",
  NULL
};
const char * usage="Compute stars formation rate";

void abortOnFalse(const bool status, std::string message)
{
  if (!status) {
    std::cerr << "Program aborted because:\n";
    std::cerr << message<<"\n";
    std::exit(1);
  }
}

//------------------------------------------------------------------------------
// readHiiFile
void readHiiFile(const std::string simname, CHIIVector & chiiv)
{
  // keep filename untill last /
  std::string indir=simname;
  int found=indir.find_last_of("/");
  if (found != (int) std::string::npos && (int) indir.rfind("output_")<found) {
    indir.erase(found,indir.length()-found);
  }
  std::string s_run_index;
  std::cerr << "indir =" << indir <<"\n";

  found=(int) indir.rfind("output_");
  if (found!=(int) std::string::npos) {
    s_run_index= indir.substr(found+7,indir.length()-1); // output_ = 7 characters

    while ((found=s_run_index.find_last_of("/"))>0) { // remove trailing "/"
      s_run_index.erase(found,found);
    }

    std::cerr << "Run index = " << s_run_index << "\n";

  }
  std::string  infile = indir + "/part_" + s_run_index + ".out_HII_data";
  //if (verbose)
  std::cerr << "HII input file =" << infile <<"\n";

  // Get the HII regions locations
  ifstream HIIFile;

  HIIFile.open(infile.c_str(),std::ios::in);

  if (! HIIFile.is_open()) {
    std::cerr <<
      "Unable to open HII input file ["<<infile<<"] aborting..\n\n";
    std::exit(1);
  }
  while (! HIIFile.eof()) {           // while ! eof
    std::string line;
    getline(HIIFile,line);
    if ( ! HIIFile.eof()) {
      float x,y,z,sradius,mass;
      std::istringstream ss(line);
      ss >> x; // read
      ss >> y; // read
      ss >> z; // read
      ss >> sradius; // read
      ss >> mass; // read
      CHII * cii = new CHII(x,y,z,sradius,mass);
      chiiv.push_back(*cii);
      //vi.push_back(index);
    }
  }
}

//------------------------------------------------------------------------------
// processComponent
// read pos,vel,mass of the components
// if component exist AND it has been selected, then respecting comp's data are
// prepared to be saved
void process(uns::CunsIn * uns, float agemax, uns::CunsOut * unsout)
{
  float * gpos, // gas   pos
        * gvel, // gas   vel 
        * gmass,// gas   mass
        * gtemp,// gas temperature
        * spos, // stars pos
        * mass, // stars mass
        * age,  // stars age
        * hsml, // gas hsml
        * rho,  // gas density
        * massamr;
  int ngas,nstars;
  bool ok;
  double alpha=0.28;                      // fraction of He in mass
  double mu=4./(8.-5.*alpha);
  double mh=1.67E-24;                     // proton mass in g
  double kb=1.38E-16;                     // Boltzmann constant in erg.K-1

  CHIIVector chiiv;
  // Try to read HII file
  readHiiFile(uns->snapshot->getFileName(),chiiv);
  std::cerr << "There are ["<<chiiv.size()<<"] ionised particles found\n";

#if 0
  for (unsigned int i=0; i<chiiv.size(); i++) {
    std::cerr << chiiv[i].getX() << " "
              << chiiv[i].getY() << " "
              << chiiv[i].getZ() << " "
              << chiiv[i].getSRadius() << " "
              << chiiv[i].getMass() << " "
              << "\n";
  }
  std::exit(1);
#endif
  // load gas data
  ok = uns->snapshot->getData("gas","pos" ,&ngas,&gpos );
  abortOnFalse(ok,"Gas Pos are missing");
  ok = uns->snapshot->getData("gas","vel" ,&ngas,&gvel );
  abortOnFalse(ok,"Gas Vel are missing");
  ok = uns->snapshot->getData("gas","mass" ,&ngas,&gmass );
  abortOnFalse(ok,"Gas mass are missing");
  ok = uns->snapshot->getData("gas","rho" ,&ngas,&rho );
  abortOnFalse(ok,"Gas Rho are missing");
  ok = uns->snapshot->getData("gas","hsml",&ngas,&hsml);
  abortOnFalse(ok,"Gas hsml are missing");
  ok = uns->snapshot->getData("gas","temp",&ngas,&gtemp);
  abortOnFalse(ok,"Gas temp are missing");
  massamr = new float[ngas*3];
  for (int i=0; i<ngas*3; i++ ) massamr[i] = 0.0;

  // load stars data
  ok = uns->snapshot->getData("stars","pos" ,&nstars,&spos );
  abortOnFalse(ok,"Stars Pos are missing");
  ok = uns->snapshot->getData("stars","age" ,&nstars,&age );
  abortOnFalse(ok,"Stars Age are missing");
  ok = uns->snapshot->getData("stars","mass",&nstars,&mass);
  abortOnFalse(ok,"Stars mass are missing");

  CTimer timing;
  double time_maketree, time_neighbors;

  // Put gas particles into an octree and make tree
  std::cerr << "Start tree building.....\n";
  CTree<float> * tree = new CTree<float>(ngas,gpos,(float *) NULL);
  time_maketree = timing.cpu();
  std::cerr << "Tree done in :" << time_maketree << " secondes\n";

  // create neibors object
  CNeibors<float> * neibors = new CNeibors<float>(tree);

  // find neibors
  timing.restart();
  std::cerr << "Start finding neighbors.....\n";
  std::vector<CDistanceId> tabneib;
  int cpt=0;

  for (unsigned int i=0; i<chiiv.size(); i++) {
    //std::cerr << "i="<<i<<"\n";
    //if ((age[i]*14.90703773)<= agemax) {
      cpt++;
      CHII * chii = &chiiv[i];

      neibors->setMaxRadius(chii->getSRadius());
      neibors->setStopAtMaxRadius(true);

      float spos[3];
      spos[0] = chii->getX(); // x
      spos[1] = chii->getY(); // y
      spos[2] = chii->getZ(); // z
      neibors->process(spos,ngas,&tabneib);
      massamr[tabneib[0].getId()*3] += chii->getMass();
    //}
  }
  time_neighbors = timing.cpu();
  std::cerr << "Neibs done in :" << time_neighbors << " secondes\n";

  std::cerr << cpt << "/" << nstars << " processed\n";
  cpt=0;
  for (int i=0; i<ngas; i++) {
    if (massamr[i*3]!=0.0) {
      cpt++;
      massamr[i*3] /= agemax;
      massamr[i*3] *= 1.E3;
      //std::cerr << "i="<<i<<" massamr="<<massamr[i]<<" hsml="<<hsml[i]<<"\n";
    }
    massamr[i*3+1]=(1.0E14*mu*mh/kb)*gtemp[i]; // we put temperature in 2nd dimension of array
  }
  std::cerr << cpt << " amr cells  processed\n";
  std::string comp="gas";
  // save data
  unsout->snapshot->setData(comp,"pos",ngas,gpos,false);
  unsout->snapshot->setData(comp,"vel",ngas,gvel,false);
  unsout->snapshot->setData(comp,"rho",ngas,rho,false);
  unsout->snapshot->setData(comp,"hsml",ngas,hsml,false);
  unsout->snapshot->setData(comp,"mass",ngas,gmass,false);
  unsout->snapshot->setData(comp,"acc",ngas,massamr,false);
  //unsout->snapshot->setData(comp,"temp",ngas,gtemp,false);

  delete [] massamr;

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
  float agemax=        getdparam((char *) "agemax"   );
  std::string select_t(getparam ((char *) "times"    ));
  bool  first=         getbparam((char *) "first"     );
  float       offset=  getdparam((char *) "offset"   );
  bool        verbose =getbparam((char *) "verbose" );
    
  bool one_file=false;
  bool stop=false;
  bool special_nemo=false;
  if (outname=="-" || outname==".") special_nemo=true;
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
    std::cerr << "Modified selected time =["<<select_t<<"]\n";
  }

  uns::CunsOut * unsout=NULL; // out object
  bool first_out=true;
  // -----------------------------------------------
  // instantiate a new UNS input object (for reading)
  uns::CunsIn * unsin = new uns::CunsIn(simname,"gas,stars",select_t,verbose);
  
  if (unsin->isValid()) { // input file is known by UNS lib
    int cpt=0;
    while(unsin->snapshot->nextFrame("mxvTRHXIA")&&!stop) { // there is a new frame
      std::string itype = unsin->snapshot->getInterfaceType();
      std::cerr << "Input file is of type :"<<itype<<"\n";

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
        std::string out_name=std::string(outname);;
        if (! special_nemo) { // ! standard output && ! "."
          if (one_file || (cpt==1 && !first)) {
            out_name=std::string(outname);
            if (one_file) stop = true; // do not continue
          } else {
            stringstream ss("");
            ss << std::string(outname) << "." << setw(5) << setfill('0') << number.str();
            //out_name=std::string(outname)+"."+number.str();
            out_name=ss.str();
          }
          // create a new UNS out object
          unsout = new uns::CunsOut(out_name,"gadget2",verbose);
        } else {
          if (first_out) {
            first_out = false;
            // instantiate only once unsout, because outname="-"
            unsout = new uns::CunsOut(out_name,"gadget2",verbose);
          }
        }
        std::cerr << "output filename=["<<out_name<<"]\n";

        // save time
        unsout->snapshot->setData("time",time);


        // processing
        process(unsin,agemax, unsout); // only all particles selected
        // save snapshot
        unsout->snapshot->save();

        if (!special_nemo) {
          delete unsout; // remove object
        }

      }
    }
  } else {
    std::cerr << "Unknown UNS file format["<<simname<<"]\n";
  }
  delete unsin;
  //   finish NEMO
  finiparam();
}
// ----------- End Of [unsio_demo.cc] ------------------------------------
