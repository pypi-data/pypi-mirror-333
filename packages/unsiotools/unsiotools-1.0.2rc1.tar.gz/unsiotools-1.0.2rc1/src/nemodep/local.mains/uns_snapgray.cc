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
#include <cmath>
#include <nemo.h>

/* -------------------------------------------------------------- *\
   |* Include file
   \* -------------------------------------------------------------- */

#include <cpgplot.h>
#include "uns.h"

/* -------------------------------------------------------------- *\
   |* Nemo variable
   \* -------------------------------------------------------------- */
const char * defv[] = {
  "in=???\n		      UNS input snapshot",
  "out=???\n                  output gif file",
  "select=???\n               select particles (range, or component name)",
  "range=\n                   -range < x|y|z > +range",
  "color=red\n                particles's color black,red,green,blue,cyan,magenta,yellow,orange",
  "no=0\n                     output file's index",
  "pixel=20\n                  size in pixel of the gaussian",
  "dimx=1024\n                 internal image size",
  "dimy=1024\n                 internal image size",
  "gp=5.\n                     gaussian parameter",
  "com=t\n                    center according to com",
  "xrange=-5.0:5.0\n          x scaling",
  "yrange=-5.0:5.0\n          y scaling",
  "zrange=-5.0:5.0\n          z scaling",
  "pvar=x\n                   plotting variable, x (position) | v (velocity)",
  "times=all\n		      selected time",
  "verbose=f\n                verbose on/off"
  "VERSION=1.O\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};

const char * usage="Plot in a GIF file, y=f(x) and z=f(x)";

float      
    * timeptr  = NULL,
    * phase_ptr = NULL,
    * pos      = NULL,
    * vel      = NULL,
    * massptr  = NULL;

int nbody;

int iter;


//
// moveToCom
// move particles positions to center of mass
void moveToCom(const int nbody,float * pos, float * mass)
{
  double com[3] = {0., 0., 0.};
  double np=0.,masstot=0;;
  for (int i=0; i<nbody;i++) {
    masstot+=mass[i];
    np++;
    int jndex= i;
    com[0] +=(pos[jndex*3  ]*mass[i]);
    com[1] +=(pos[jndex*3+1]*mass[i]);
    com[2] +=(pos[jndex*3+2]*mass[i]);
  }
  std::cerr <<"COM     ="<<com[0]<<" "<<com[1]<<" "<<com[2]<<"\n";
  std::cerr <<"np      ="<<np<<"\n";
  std::cerr <<"mass tot="<<masstot<<"\n";
  // center
  for (int i=0; i<nbody;i++) {
    pos[i*3+0] -= (com[0]/masstot);
    pos[i*3+1] -= (com[1]/masstot);
    pos[i*3+2] -= (com[2]/masstot);
  }
  
}
/* ------------------------------------------------------------ *\
   |* set_graph : 
   |* set graph parameters => dev (device) h
   \* ------------------------------------------------------------ */
void set_graph(char* dev,float h,float w)
    
{ 
  if (h) {;}
  if (cpgbeg(0,dev,1,1)!=1) /* open output device */
    exit(EXIT_FAILURE); 
  
  fprintf(stderr,"Device = [%s]\n",dev);
  cpgpap(2.*w/2.54,0.5);  /* 0.5 = h/(2.0*w) */
  cpgscf(2.0);    /* set caracter font */
  cpgsch(1.5);  /* set caracter height */
  cpgslw(1);    /* set line with */
  
  /* Reverse video color */
  cpgscr(0,1.0,1.0,1.0);
  cpgscr(1,0.0,0.0,0.0);
  
}
//
float *  computeGaussian(const int pixel, float g)
{
  float * tabgauss=new float[pixel*pixel];
  
  float pi=atan(1.0)*4.;
  float sqrtpi=sqrt(2*pi);
  float halfp=(float )pixel/2.;
  for (int i=0; i<pixel; i++) {
    for (int j=0; j<pixel; j++) {
      float distance=sqrt((i-halfp)*(i-halfp)+(j-halfp)*(j-halfp));
      float gauss=exp(-(distance)*(distance)/g/g/2.0)/sqrtpi/g;
      
      tabgauss[i*pixel+j]=gauss;
    }
  } 
  
  return tabgauss;
}
//
void applyGaussian(float * tab, float * tabgauss, const int pixel,const int dimx,const int dimy, const int x, const int y)
{
  float halfp=(float )pixel/2.;
  int nindex=0;
  for (int i=0; i<pixel; i++) {
    for (int j=0; j<pixel; j++) {
      if ((x-halfp+j)>=0 && (x-halfp+j)<dimx && (y-halfp+i)>=0 && (y-halfp+i)<dimy) {
	int index=(int) ((y-halfp+i)*dimx+(x-halfp+j));
	if ( index <0 or index > (dimx*dimx)) {
	  std::cerr << "error index = " << index << "\n";
	  nindex++;
	} else {
	  tab[index]+=tabgauss[i*pixel+j];
	}
      }
    }
  }
}

//
void computeDataTab(float * data,int nbody, float range[3][2], float *tabgauss, const int pixel,const int dimx , const int dimy,float*tab, float & zmin, float &zmax, const int axis)
{
  for (int i=0;i<dimy; i++)
    for (int j=0;j<dimx; j++)
      tab[i*dimx+j] = 0.0;
  
  zmin=zmax=0.;
  float * pp=data;
  int np=0;
  int f=axis;
  /* loop on all particles */
  for (int i=0 ; i<nbody; i++, pp+=3) {
    if (
	pp[0] >= range[0][0] &&
	pp[0] <= range[0][1] &&
	pp[f] >= range[f][0] &&
	pp[f] <= range[f][1] ) {
      
      np++;
      // dimx*(x-xmin)/(xmax-xmin)
      int x=((pp[0]-range[0][0])/(range[0][1]-range[0][0]))*dimx;
      int y=((pp[f]-range[f][0])/(range[f][1]-range[f][0]))*dimy;
      assert(x<dimx);
      assert(y<dimy);
      //tab[y*dimx+x] += 1.;
      applyGaussian(tab,tabgauss,pixel,dimx,dimy,x,y);
    }
  }
  std::cerr << np << " points in the range !\n";
  // find zmin zmax
  zmin=10000000.0;
  for (int i=0;i<dimy; i++)
    for (int j=0;j<dimx; j++) {
    zmax=std::max(zmax, tab[i*dimx+j]);
    float zzmin=std::min(zmin, tab[i*dimx+j]);
    if (zzmin != 0.0)  zmin=zzmin;
    
  }
  
  for (int i=0;i<dimy; i++)
    for (int j=0;j<dimx; j++) {
    if (tab[i*dimx+j]==0.0) tab[i*dimx+j]=zmin ;
    
  }
  
  std::cerr << "FIRST zmax="<<zmax<<" zmin="<<zmin<<"\n";
#if 1
  //zmid = log(zmid);
  zmax=log(zmax);
  zmin=log(zmin);
  for (int i=0;i<dimy; i++)
    for (int j=0;j<dimx; j++) {
    if (tab[i*dimx+j] != 0.0) {
      tab[i*dimx+j] = log(tab[i*dimx+j]);///zmax; // normalize
    }
  }
#endif     
  
}
//
void snapgradient(char * dev,float * data,int nbody, float range[3][2], float *tabgauss, const int pixel,const int dimx , const int dimy )
{
  
  float zmin,zmax;  
  float * tab = new float[dimx*dimy];
  
  
  float bright=0.5;
  float contrast=1.0;
  
  float RL[9] = {-0.5, 0.0, 0.17, 0.33, 0.50, 0.67, 0.83, 1.0, 1.7};
  float RR[9] = { 0.0, 0.0,  0.0,  0.0,  0.6,  1.0,  1.0, 1.0, 1.0};
  float RG[9] = { 0.0, 0.0,  0.0,  1.0,  1.0,  1.0,  0.6, 0.0, 1.0};
  float RB[9] = { 0.0, 0.3,  0.8,  1.0,  0.3,  0.0,  0.0, 0.0, 1.0};
  
  cpgbeg(0,dev,2,1);
  // compute Data on XY
  computeDataTab(data,nbody,range,tabgauss,pixel,dimx,dimy,tab,zmin,zmax,1);
  
  float xmin=range[0][0];
  float xmax=range[0][1];
  float ymin=range[1][0];
  float ymax=range[1][1];
  float tr[6] = { xmin, (xmax-xmin)/(float)dimx, 
		  0, ymin, 
		  0, (ymax-ymin)/(float)dimy};
  
  //  cpgopen(dev);
  cpgenv(xmin,xmax,ymin,ymax,1,0);
  
  cpgctab(RL, RR, RG, RB, 9, contrast, bright);
  cpgimag(tab,dimx,dimy,1,dimx,1,dimy,zmin,zmax,tr);
  cpglab("X","Y","Faceon");
  
  // compute Data on XZ
  computeDataTab(data,nbody,range,tabgauss,pixel,dimx,dimy,tab,zmin,zmax,2);
  
  xmin=range[0][0];
  xmax=range[0][1];
  ymin=range[2][0];
  ymax=range[2][1];
  float tr1[6] = { xmin, (xmax-xmin)/(float)dimx, 
                   0, ymin, 
                   0, (ymax-ymin)/(float)dimy};
  
  //  cpgopen(dev);
  cpgenv(xmin,xmax,ymin,ymax,1,0);
  
  cpgctab(RL, RR, RG, RB, 9, contrast, bright);
  cpgimag(tab,dimx,dimy,1,dimx,1,dimy,zmin,zmax,tr1);
  cpglab("X","Y","Edgeon");
  
  cpgask(1);
  cpgend(); 
  
  delete [] tab;
  
}
/* -------------------------------------------------------------- *\ 
   |* setrange :
   |* Converti une chaine du type "-2.0:1.5" en deux reels :
   |* range[0]=-2.0 et range[1]=1.5
   \* -------------------------------------------------------------- */
void setrange(float range[],const char * ch_range)
{
  char * p;
  
  p = strchr((char *) ch_range,':');
  if (p) {
    range[0] = atof(ch_range);
    range[1] = atof(p+1);
  }
  else {
    range[0] = 0.0;
    range[1] = atof(ch_range);
  }
}


/* -------------------------------------------------------------- *\ 
   |* programme principal
   \* -------------------------------------------------------------- */ 
int main(int argc, char ** argv )
{
  
  
  char   outgif[80];
  
  bool   first = true;
  
  float range[3][2];
  if (argc) {;}
  //   start  NEMO
  initparam(const_cast<char**>(argv),const_cast<char**>(defv));
  
  /* recuperation des parametres en entree */
  char * simname     = getparam ((char *) "in"     );
  int    no_frame    = getiparam((char *) "no"     );
  char * outfile     = getparam ((char *) "out"    );
  char * select_c    = getparam ((char *) "select" );
  char * select_t    = getparam ((char *) "times"  );
  bool   com         = getbparam((char *) "com"    );
  bool   verbose     = getbparam((char *) "verbose");
  int    pixel       = getiparam((char *) "pixel"  );
  int    dimx        = getiparam((char *) "dimx"   );
  int    dimy        = getiparam((char *) "dimy"   );
  float  gp          = getdparam((char *) "gp"     );
  std::string rr     = getparam ((char *) "range"  );
  
  if (rr.length()!=0) {
    std::string srange="-"+rr+":"+rr;
    setrange(range[0],srange.c_str());
    setrange(range[1],srange.c_str());
    setrange(range[2],srange.c_str());
  } 
  else {
    setrange(range[0],getparam((char *)"xrange"));
    setrange(range[1],getparam((char *)"yrange"));
    setrange(range[2],getparam((char *)"zrange"));
  }
  
  
  // instantiate a new uns object
  //s::Cuns * uns = new uns::Cuns(simname,select_c,select_t);
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);
  
  float * tabgauss = computeGaussian(pixel,gp);
  
  if (uns->isValid()) {    
    while(uns->snapshot->nextFrame()) {      
      bool ok;
      int cnbody,nbody;      
      float * pos, * mass, time;
      // get the input number of bodies according to the selection
      ok=uns->snapshot->getData("nsel",&nbody);
      // get the simulation time
      ok=uns->snapshot->getData("time",&time);
      // get POS from input snapshot
      ok=uns->snapshot->getData("pos" ,&cnbody,&pos);
      if (!ok) {
        std::cerr << "No positions, aborted !\n";
        std::exit(1);
      }
      // get MASS from input snapshot
      ok=uns->snapshot->getData("mass",&cnbody,&mass);
      if (com && mass) moveToCom(nbody,pos,mass);
      
      /* Gif Name */
      if (outfile[0] == '?') {
        sprintf(outgif,"%s",outfile);
      } else {
        sprintf(outgif,"%s.%05d.gif/gif",outfile,no_frame);
      }
      /* call engine */
      snapgradient(outgif,pos,nbody,range,tabgauss,pixel,dimx,dimy);
      
      /* iteration */
      no_frame++;
      
    }
    if (! first)
      cpgend();
    
    //   finish NEMO
    finiparam();
    return 1;
  } 
}	      
/* -------------------------------------------------------------- *\ 
   |* Fin de snapraster.c 
   \* -------------------------------------------------------------- */ 
