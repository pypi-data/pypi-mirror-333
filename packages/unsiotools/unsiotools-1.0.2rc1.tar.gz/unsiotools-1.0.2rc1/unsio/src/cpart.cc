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

#include <cstdlib>
#include <sstream>
#include <iomanip>
#include "cpart.h"
namespace ramses {
  using namespace std;
// ----------------------------------------------------------------------------
// READING constructor                                                                 
CPart::CPart(const std::string _indir, const bool _v)
{
  valid=false;
  nbody     = 0;  
  ndm       = 0;
  ndm_box   = 0;
  nstar_box = 0;
  nselect   = 0;
  verbose=_v;
  indir = _indir;
  infile="";
  exist_family=false;
  
  // keep filename untill last /
  int found=indir.find_last_of("/");
  if (found != (int) string::npos && (int) indir.rfind("output_")<found) {
    indir.erase(found,indir.length()-found);
  }
  if (verbose)
    std::cerr << "indir =[" << indir <<"]\n";
  
  found=(int) indir.rfind("output_"); 
  if (found!=(int) std::string::npos) {
    s_run_index= indir.substr(found+7,indir.length()-1); // output_ = 7 characters
    
    while ((found=s_run_index.find_last_of("/"))>0) { // remove trailing "/"
      s_run_index.erase(found,found);
    }
    if (verbose)
      std::cerr << "Run index = " << s_run_index << "\n";
    infile = indir + "/part_" + s_run_index + ".out00001";
    if (verbose)
      std::cerr << "infile =[" << infile <<"]\n";
    // check if new ramses format with family
    std::ifstream fi;
    fi.open(std::string(indir+"/part_file_descriptor.txt").c_str());
    if (fi.is_open()) {
      exist_family=true;
      fi.close();
    } else {
      exist_family=false;
    }
  }
}

// ----------------------------------------------------------------------------
// Destructor                                                                 
CPart::~CPart()
{
  part.close();
}
// ----------------------------------------------------------------------------
//
bool CPart::isValid()
{    
  if (part.open(infile)) {
    valid=true;
    readHeader();
    part.close();
  }
  else
    valid=false;
  return valid;
}

// ============================================================================
// readHeader
int CPart::readHeader()
{
  part.readDataBlock((char *) &ncpu);
  part.readDataBlock((char *) &ndim);
  part.readDataBlock((char *) &npart);
  part.skipBlock();
  part.readDataBlock((char *) &nstar);  
  return 1;
}
// ============================================================================
// loadData
template int CPart::loadData<float>(uns::CParticles<float> * particles,
                    const unsigned int req_bits, const unsigned int comp_bits);
template int CPart::loadData<double>(uns::CParticles<double> * particles,
                    const unsigned int req_bits, const unsigned int comp_bits);
template <class T> int CPart::loadData(uns::CParticles<T> * particles,
                    const unsigned int req_bits, const unsigned int comp_bits)
{
  int offset=0;
  for (int i=0; i<ncpu; i++) {
    std::ostringstream osf("");
    osf << std::fixed << std::setw(5) << std::setfill('0') <<i+1;
    std::string infile = indir + "/part_" + s_run_index + ".out" + osf.str();
    if (verbose) std::cerr << "reading file : " << infile << "\n";
    part.open(infile);
    readHeader();

    double * tmp[7];//=new double[npart];
    for (int i=0;i<7;i++) {
       tmp[i] = NULL;
    }
    part.skipBlock(3);

    // read positions
    for (int j=0; j<ndim; j++) {
      tmp[j] = new double[npart]; // alloc
      part.readDataBlock((char *) tmp[j]);
    }

    // read velocities
    for (int j=0; j<ndim; j++) {
      tmp[3+j] = new double[npart]; // alloc
      part.readDataBlock((char *) tmp[3+j]);
    }

    // read masses
    tmp[6] = new double[npart]; // alloc
    part.readDataBlock((char *) tmp[6]);
    double * agetmp, * metaltmp=NULL;
    int * id=NULL;
    char * family=NULL;

    if (req_bits&ID_BIT) {
      id = new int[npart];
      part.readDataBlock((char *) id); // read identity
    } else {
      part.skipBlock(); // skip identity
    }

    if (nstar>0) { // || 1) { // there are stars

      part.skipBlock(); // skip level
      if (exist_family) {
        family = new char[npart];
        part.readDataBlock((char *) family); // read family
        part.skipBlock(); // skip tag
      }
      agetmp = new double[npart];
      part.readDataBlock((char *) agetmp);

      bool found_metal=false;
      if (req_bits&METAL_BIT) {
        metaltmp = new double[npart];
        int status=part.readDataBlock((char *) metaltmp, false);
        found_metal=true; // found metallicity what happen...
        if (! status) { // no metallicity block
          for (int i=0; i<npart; i++) metaltmp[i] = -1.0; // we put -1.0 when no metellicity
        }
        //std::cerr << "Metalicity status =" << status << "\n";

      }
      for (int k=0; k<npart; k++) {
        bool ok_stars=false, ok_dm=false;
        if (exist_family) {
          if (family[k]==2) { // stars
            ok_stars=true;
          }
          if (family[k]==1) { // stars
            ok_dm=true;
          }
        } else {
          if (agetmp[k]!=0.) { // stars
            ok_stars=true;
          } else {            // dm
            ok_dm=true;
          }
        }
        if ((ok_dm && (comp_bits&HALO_BIT))  ||  // it's DM
            (ok_stars&& (comp_bits&STARS_BIT))) {  // its' stars
          if ((tmp[0][k]>=xmin && tmp[0][k]<=xmax) &&
              (tmp[1][k]>=ymin && tmp[1][k]<=ymax) &&
              ((ndim<3)||(tmp[2][k]>=zmin && tmp[2][k]<=zmax))
              ) {

            bool take=false;
            for (int l=0;l<ndim;l++) {
              if (req_bits&POS_BIT) {
                particles->pos.push_back(tmp[l][k]);
                particles->load_bits |= POS_BIT;
                take=true;
              }
              if (req_bits&VEL_BIT) {
                particles->vel.push_back(tmp[3+l][k]);
                particles->load_bits |= VEL_BIT;
                take=true;
              }
            }
            if (ndim<3) { // for 2D only
              if (req_bits&POS_BIT) {
                particles->pos.push_back(0.0);
              }
              if (req_bits&VEL_BIT) {
                particles->vel.push_back(0.0);
              }
            }
            if (req_bits&MASS_BIT) {
              particles->mass.push_back(tmp[6][k]);
              particles->load_bits |= MASS_BIT;
              take=true;
            }
            //if (agetmp[k]!=0 && req_bits&AGE_BIT) { // stars only (age)
            if (ok_stars && req_bits&AGE_BIT) { // stars only (age)
              particles->age.push_back(agetmp[k]);
              particles->load_bits |= AGE_BIT;
            }
            //if (agetmp[k]!=0 && req_bits&METAL_BIT && found_metal) { // stars only (metallicity)
            if (ok_stars && req_bits&METAL_BIT && found_metal) { // stars only (metallicity)
	      //std::cerr << "Stars => "<<metaltmp[k]<<"\n";
              particles->metal.push_back(metaltmp[k]);
              particles->load_bits |= METAL_BIT;
            }
            //if (agetmp[k]==0 && req_bits&METAL_BIT && found_metal) { // stars only (metallicity)
            if (ok_dm && req_bits&METAL_BIT && found_metal) { // stars only (metallicity)
	      //if ( tmp[6][k] == 0.0 ) 
	      //std::cerr << "DM => "<<metaltmp[k]<<" mass=" << tmp[6][k] << "\n";
              //particles->metal.push_back(tmp[6][k]); // put mass for dark matter
              particles->metal.push_back(-1.0); // put -1 for dark matter after discussion with valentin 18-jul-2016
//           Centre de donneeS Astrophysiques de Marseille (CeSAM)
              particles->load_bits |= METAL_BIT;
            }
            if (req_bits&ID_BIT) {
              particles->id.push_back(id[k]); // save real id for dm or stars
              particles->load_bits |= ID_BIT;
            }
            if ( (take && ok_stars) || (!req_bits && ok_stars)) { // !req_bits for uns_info and siplay=f
               particles->indexes.push_back(4); // save star positions
               particles->nstars++;               
            }
            if ((take && ok_dm) || (!req_bits && ok_dm)) {
               particles->indexes.push_back(1); // save DM positions
               particles->ndm++;
            }

            particles->ntot++; // one more total particles

            offset++;
            //assert(offset<=nselect);
          }
        }
      }
      // garbage
      delete [] agetmp;
      delete [] family;
      if (req_bits&ID_BIT) {
        delete [] id;
      }
      if (req_bits&METAL_BIT) {
        delete [] metaltmp;
      }
    }
    else {  // there are no stars
      if (comp_bits&HALO_BIT) { // DM sel
        for (int k=0; k<npart; k++) {        
          if ((tmp[0][k]>=xmin && tmp[0][k]<=xmax) &&
              (tmp[1][k]>=ymin && tmp[1][k]<=ymax) &&
              ((ndim<3)||(tmp[2][k]>=zmin && tmp[2][k]<=zmax))
              ) {
            bool take=false;
            for (int l=0;l<ndim;l++) {
              if (req_bits&POS_BIT) {
                particles->pos.push_back(tmp[l][k]);
                take=true;
              }
              if (req_bits&VEL_BIT) {
                particles->vel.push_back(tmp[3+l][k]);
                take=true;
              }
            }
            if (ndim<3) { // for 2D only
              if (req_bits&POS_BIT) {
                particles->pos.push_back(0.0);
              }
              if (req_bits&VEL_BIT) {
                particles->vel.push_back(0.0);
              }
            }
            if (req_bits&MASS_BIT) {
              particles->mass.push_back(tmp[6][k]);
              take=true;
            }
            if (req_bits&ID_BIT) {
              particles->id.push_back(id[k]); // save real id for dm or stars
              particles->load_bits |= ID_BIT;
            }
            if (req_bits&METAL_BIT) {
              particles->metal.push_back(-1.0); // !!!! we put -1.0 when no metallicity
              particles->load_bits |= METAL_BIT;
            }
            if (take || !req_bits) { // !req_bits for uns_info and siplay=f
               particles->indexes.push_back(1); // save DM positions
               particles->ndm++;               
            }
            particles->ntot++; // one more total particles
            offset++;
            //assert(offset<=nselect);
          }
        }      
      }
      if (req_bits&ID_BIT) {
        delete [] id;
      }
    }
    // garbage collecting
    for (int i=0; i<7; i++)
      if (tmp[i]) {
        delete [] tmp[i];
      }
    part.close(); // close current file
  } // for ...
  return 1;
}
} // namespace ramses
