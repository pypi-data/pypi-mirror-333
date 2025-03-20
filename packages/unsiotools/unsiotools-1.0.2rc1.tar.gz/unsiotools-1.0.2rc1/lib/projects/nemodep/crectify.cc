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
#include "csnaptools.h"
#include <cstdio>
#include "crectify.h"
extern "C" {
//#include "nrutil.h"
float **fmatrix(long nrl, long nrh, long ncl, long nch);
float *fvector(long nl, long nh);
#include "nr.h"
}
#include <cvecutils.h>
#include <iomanip>


using namespace uns_proj;
using namespace jclut;
using namespace std;

//------------------------------------------------------------------------------
// PUBLIC CRectify
//------------------------------------------------------------------------------
//
CRectify::CRectify(bool _verbose)
{
  verbose=_verbose;
  only_eigen_values=false;
  w_sum_ok=false;
  init();
}

//------------------------------------------------------------------------------
// Rectify
// this method rectify position and vitesse for tge current time, according to
// the followings rules :
// _use_rho = true, use density as weighting factor, if _rho array is empty then
//            local density is computed
//          = false, use mass as weighting factor
// _threshold=when compute density, program will keep only particles above threshold
//            which must be a value between 0.0% and 100.0%
// _rectify = true, positions and velocities will be rectified
//          = false, vectors only are computed
// _cod_file= is a filename contening COD of snapshots
//            if you don't provide this file, you must set _use_tho=true
// _rect_file=output file with results of the rectification, with the following format
//            time 6xCOD 9xVectors
//
bool CRectify::rectify(const int _nbody,const float _time,
                       float * _pos, float * _vel,float * _mass, float * _rho,
                       const bool _use_rho, const bool _rectify,
                       std::string _cod_file,std::string _rect_file, const float _radius,const float _dmin, const float _dmax)
{
  nbody= _nbody;
  pos  = _pos;
  vel  = _vel;
  mass = _mass;
  rho  = _rho;
  time = _time;

  radius = _radius;
  dmin = _dmin;
  dmax = _dmax;
  cod_file  = _cod_file;
  rect_file = _rect_file;

  rect      = _rectify;
  use_rho   = _use_rho;

  process();

  return w_sum_ok;
}

// PUBLIC CDataIndex
//------------------------------------------------------------------------------
//
bool CDataIndex::sortData(const CDataIndex &a, const CDataIndex &b)
{
  return a.data < b.data;
}

// PRIVATE
//------------------------------------------------------------------------------
//
void CRectify::init()
{
  density=NULL;
  nbody=0;
  initOldFrame();

}
//------------------------------------------------------------------------------
// process
// run all the process on snapshot
void CRectify::process()
{

  if (cod_file.length()!=0 &&!CSnaptools::isFileExist(cod_file)) {
    std::cerr << "\nRequested codfile["<<cod_file<<"] does not exist, abort\n\n";
    std::exit(1);
  }
  if (density) delete density;

  findCenter();
  findMoment();
  computeVectors();
  if (rect) {
      snapTransform();
  }
  saveRectVector();
}
//------------------------------------------------------------------------------
// findCenter
// center snapshots
void CRectify::findCenter()
{
  bool is_codfile=false;
  if (cod_file.length()!=0) { // read cod from file
    is_codfile=CSnaptools::getTimeDataFile<double>(cod_file,(double)time,6,cod);
    if (! is_codfile ) {
      std::cerr << "From file ["<<cod_file<<"] unable to find corresponding time ["<<time<<"]"
                << "aborting program....\n";
      std::exit(1);
    }

  }
  if (use_rho) { // compute density, and COD from rho
    // compute density
    processRho();
    // compute cod if ! codfile
    if (! is_codfile)
      CSnaptools::moveToCod<float>(vmass.size(),&vpos[0],&vvel[0],&vmass[0],&vrho[0],cod,false); // compute cod don't move
  }

  if (!is_codfile && !use_rho) {
    std::cerr << "Program aborted, because you MUST provide a valid COD file or/and you MUST enable \"rho=t\" variable\n";
    std::exit(1);
  }

  // cod double to float
  for (int i=0; i<6; i++) {
    codf[i] = (float) cod[i];
  }

}
//------------------------------------------------------------------------------
// processRho
// compute rho if requested
void CRectify::processRho()
{

  if (!rho) {
    std::cerr << "Computing rho........\n";
    // Instantiate a density object
    density = new CDensity(nbody,&pos[0],&mass[0]);
    density->compute(0,32,1,8); // estimate density
  }

  rho_di.clear();

  // store rho in structure
  for (int i=0; i<nbody; i++) {
    CDataIndex p;
    p.foo();
    if (rho) {
      p.setDI(rho[i],i);
    } else {
      p.setDI(density->getRho()[i],i);
    }
    rho_di.push_back(p);
  }

  // sort by rho
  std::sort(rho_di.begin(),rho_di.end(),CDataIndex::sortData);

  double minrho=log(rho_di[0].data);
  double maxrho=log(rho_di[rho_di.size()-1].data);

  vpos.clear();
  vvel.clear();
  vmass.clear();
  vrho.clear();

  // keep only particles > threshold
  int ii=0;
  for (std::vector<CDataIndex>::iterator it=rho_di.begin(); it != rho_di.end(); it++) {
    float logrho = log((*it).data);
    if (((logrho - minrho)*100./(maxrho-minrho))>=dmin &&
        ((logrho - minrho)*100./(maxrho-minrho))<=dmax) { // we keep particles
      int sindex=(*it).index;
      vpos.push_back(pos[sindex*3+0]);
      vpos.push_back(pos[sindex*3+1]);
      vpos.push_back(pos[sindex*3+2]);
      if (vel) {
        vvel.push_back(vel[sindex*3+0]);
        vvel.push_back(vel[sindex*3+1]);
        vvel.push_back(vel[sindex*3+2]);
      }
      vmass.push_back(mass[sindex]);
      if (rho) {
        vrho.push_back(rho[sindex]);
      } else {
        vrho.push_back(density->getRho()[ii]); //[sindex]);
      }
      ii++;
    }

  }
  // compute COD without shifting
  if (cod_file.length()==0) { // we must compute COD

  }

}
//------------------------------------------------------------------------------
// findMoment
// compute moment
void CRectify::findMoment()
{
  CLRM(w_qpole);
  double w_sum=0.0;
  float distance=0.0;

  if ( use_rho) { // data are stored in Vectors

    float tmpv[3], pos_b[3];
    matrix tmpm;
    for (unsigned int i=0; i<vmass.size(); i++) {
      vectutils::subv(pos_b, &vpos[i*3], codf); // shift to cod
      ABSV(distance,pos_b);
      if (distance <=radius) {
        w_sum += (vrho[i] * vmass[i]);
        float w_b = vrho[i] * vmass[i];
        //vectutils::subv(pos_b, &vpos[i*3], codf); // shift to cod
        MULVS(tmpv, pos_b, w_b);
        OUTVP(tmpm, tmpv, pos_b);
        ADDM(w_qpole, w_qpole, tmpm);
      }
    }
  } else {  // data are stored in arrays

    float tmpv[3], pos_b[3];
    matrix tmpm;
    for ( int i=0; i<nbody; i++) {
      vectutils::subv(pos_b, &pos[i*3], codf); // shift to cod
      ABSV(distance,pos_b);
      if (distance <=radius) {
        w_sum += mass[i];
        float w_b = mass[i];
        //vectutils::subv(pos_b, &pos[i*3], codf); // shift to cod
        MULVS(tmpv, pos_b, w_b);
        OUTVP(tmpm, tmpv, pos_b);
        ADDM(w_qpole, w_qpole, tmpm);
      }
    }
  }
  if (w_sum>0) {
    DIVMS(w_qpole, w_qpole, w_sum);
    w_sum_ok=true;
  }

}
//------------------------------------------------------------------------------
// computeVectors
// compute  Vectors
void CRectify::computeVectors()
{
  // computing Eigen vectors according to moment w_qpole
  eigenFrame(frame, w_qpole);

  if (! only_eigen_values) { // does not compute only eigen values
    float tmp;
    vectutils::dotvp(tmp,oldframe[0], frame[0]);
    if (tmp < 0.0)
      vectutils::mulvs(frame[0], frame[0], (float) -1.0);
    vectutils::dotvp(tmp,oldframe[2], frame[2]);
    if (tmp < 0.0)
      vectutils::mulvs(frame[2], frame[2], (float )-1.0);
    CROSSVP(frame[1], frame[2], frame[0]);
    if (verbose) {
      printvec("e_x:", frame[0]);
      printvec("e_y:", frame[1]);
      printvec("e_z:", frame[2]);
    }

    // update old frame vectors
    for (int i = 0; i < NDIM; i++)
      vectutils::setv(oldframe[i], frame[i]);
  }
}
//------------------------------------------------------------------------------
// snapTransform STATIC
// rectify positions and velocities using rect_file
// this function returns :
// true if time value has been found in rect file
// false otherwise
bool CRectify::snapTransform(const int nbody,const float time,
                             float * pos, float * vel,
                             std::string rect_file, int &status)
{
  bool ok=false;
  if (!CSnaptools::isFileExist(rect_file)) {
    std::cerr << "\nRequested rect file["<<rect_file<<"] does not exist, abort\n\n";
    std::exit(1);
  }
  if (status) {;} // remove compiler warning
  
  float data[15];
  ok=CSnaptools::getTimeDataFile<float>(rect_file,time,15,data);

  if (ok) {
    float pos_b[3], vel_b[3];
    // LOOP on all particles not only those from threshold !!!
    for ( int i=0; i<nbody; i++) {
      // center according to COD
      vectutils::subv(&pos[i*3], &pos[i*3], data);   // cod x data[0-2]
      vectutils::subv(&vel[i*3], &vel[i*3], data+3); // cod v data[3-5]
      // transfor according eigens vectors
      for (int ii = 0; ii < NDIM; ii++) {
        vectutils::dotvp(pos_b[ii],&pos[i*3], data+6+ii*3); // data[6-8,9-11,12-14]
        vectutils::dotvp(vel_b[ii],&vel[i*3], data+6+ii*3); // data[6-8,9-11,12-14]
        //acc_b[i] = dotvp(Acc(b), frame[i]);
      }
      vectutils::setv(&pos[i*3], pos_b);
      vectutils::setv(&vel[i*3], vel_b);
      //SETV(Acc(b), acc_b);
    }
  }
  return ok;
}

//------------------------------------------------------------------------------
//snapTransform
// rectify positions and velocities using vectors
void CRectify::snapTransform()
{
  float pos_b[3], vel_b[3];
  // LOOP on all particles not only those from threshold !!!
  for ( int i=0; i<nbody; i++) {
    vectutils::subv(&pos[i*3], &pos[i*3], codf);
    vectutils::subv(&vel[i*3], &vel[i*3], codf+3);
    for (int ii = 0; ii < NDIM; ii++) {
      vectutils::dotvp(pos_b[ii],&pos[i*3], frame[ii]);
      vectutils::dotvp(vel_b[ii],&vel[i*3], frame[ii]);
      //acc_b[i] = dotvp(Acc(b), frame[i]);
    }
    vectutils::setv(&pos[i*3], pos_b);
    vectutils::setv(&vel[i*3], vel_b);
    //SETV(Acc(b), acc_b);
  }

}
//------------------------------------------------------------------------------
// eigenFrame
// compute eigen values
void CRectify::eigenFrame(float frame[3][3], matrix mat)
{
  float **q, *d, **v;
  int i, j, nrot;

  q = fmatrix(1, 3, 1, 3);
  for (i = 1; i <= 3; i++)
    for (j = 1; j <= 3; j++)
      q[i][j] = mat[i-1][j-1];
  d = fvector(1, 3);
  v = fmatrix(1, 3, 1, 3);
  jacobi(q, 3, d, v, &nrot);
  eigsrt(d, v, 3);
  for (i = 1; i <= 3; i++)
    for (j = 1; j <= 3; j++)
      frame[i-1][j-1] = v[j][i];
}
//------------------------------------------------------------------------------
// printVec
// print vectors
void CRectify::printvec(std::string name, float vec[3])
{
  double PI=acos(-1.);
  float rtp[3];	/* radius - theta - phi */
  xyz2rtp(vec,rtp);
  fprintf(stderr,"%12s  %10.5f  %10.5f  %10.5f  %10.5f   %5.1f %6.1f\n",
    name.c_str(), rtp[0], vec[0], vec[1], vec[2],
    rtp[1]*180.0/PI, rtp[2]*180.0/PI);
}
//------------------------------------------------------------------------------
//
void CRectify::xyz2rtp(float xyz[3], float rtp[3])
{
  double PI=acos(-1.);
  float z = xyz[2];
  float w = sqrt((xyz[0]*xyz[0])+(xyz[1]*xyz[1]));
  rtp[1] = atan(w/z);                 /* theta: in range 0 .. PI */
  if (z<0) rtp[1] += PI;
  rtp[2] = atan2(xyz[1], xyz[0]);     /* phi: in range  -PI .. PI */
  rtp[0] = sqrt(z*z+w*w);
}
//------------------------------------------------------------------------------
// saveRectVector
// save informations in rect file with the following format"
// time codx cody codz codvx codvy codvz v11 v12 v12 v21 v22 v23 v31 v32 v33
void CRectify::saveRectVector()
{ 
  std::fstream fd; // file descriptor

  if (rect_file.length() != 0) {
    fd.open(rect_file.c_str(),std::ios::in | std::ios::out | std::ios::app); // open file for appending
    if (fd.is_open()) {
      //fd << scientific << left << time;
      std::stringstream ss("");
      // save time
      ss << scientific << left << time << " ";
      // save cod
      for (int i=0; i<6;i++ ){
        ss << codf[i]  << " ";
      }
      // save vectors
      for (int i=0; i<3;i++ ){
        ss << frame[i][0] << " " << frame[i][1] << " " << frame[i][2] << " ";
      }
      ss << "\n";
      fd << ss.str(); // save one line

      fd.close();

    } else {
      std::cerr << "Unable to open file ["<< rect_file.c_str()<<"] in appending mode, abort...\n";
      std::exit(1);
    }
  }

}
