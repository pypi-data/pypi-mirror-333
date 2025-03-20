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
  "com=t\n                    center according to com",
  "xrange=-5.0:5.0\n          x scaling",
  "yrange=-5.0:5.0\n          y scaling",
  "zrange=-5.0:5.0\n          z scaling",
  "pvar=x\n                   plotting variable, x (position) | v (velocity)",
  "h=14.0\n                    windows's height (cm)",
  "w=14.0\n                    windows's width (cm)",
  "title=Simulation\n         simulation title",
  "times=all\n		      selected time",
  "verbose=f\n                verbose on/off"
  "VERSION=1.O\n              compiled on <" __DATE__ "> JCL  ",
  NULL,
};

const char * usage="Plot in a GIF file, y=f(x) and z=f(x)";

#define size_buff 5000
#define COMMENT 0

float      
    * timeptr  = NULL,
    * phase_ptr = NULL,
    * pos      = NULL,
    * vel      = NULL,
    * massptr  = NULL;

int nbody;

int iter;

/* About colors */
#define NBCOLORS 8  /* # of different colors */

struct tab {
  const char * color;
  int    index;
} tab_c[NBCOLORS] = { 
{ "black",1},{"red",2},{"green",3},{"blue",4},
{"cyan",5},{"magenta",6},{"yellow",7},{"orange",8} };

int ncolor_sel = 0; /* #color selected */
int index_sel[NBCOLORS]; /* array of selected colors index */

typedef struct point
{ float x,y,z;
  int col;
} t_pt;

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
/* ------------------------------------------------------------ *\
   |* depht_sort_a : 
   |* sort according the z depht (ascending)
   \* ------------------------------------------------------------ */
int depht_sort_a(const void * i, const void *j)
{   
  if (((t_pt*)i)->z > ((t_pt*)j)->z)
    return 1;
  if (((t_pt*)i)->z < ((t_pt*)j)->z)
    return -1;
  return 0;
  
}
/* ------------------------------------------------------------ *\
   |* depht_sort_d : 
   |* sort according the z depht (descending)
   \* ------------------------------------------------------------ */
int depht_sort_d(const void * i, const void *j)
{   
  if (((t_pt*)i)->z > ((t_pt*)j)->z)
    return -1;
  if (((t_pt*)i)->z < ((t_pt*)j)->z)
    return 1;
  return 0;
  
}

/* -------------------------------------------------------------- *\ 
   |* snapcompute :
   |* Plot the frame on the specific device and according the colors
   |* of selecting particles
   \* -------------------------------------------------------------- */
void snapcompute(float tsnap,float * data,int nbody,int * nret,float range[3][2],
		 float h, float w, bool * first,
		 char * outfile,char * dev,char * title,char * pvar)
{
  int i,j,ny,symb=-1;
  float * pp;
  
  int save_color; /* save pile_z color */
  
  float buff_x[size_buff], /* buffer to */
  buff_y[size_buff]; /* store point */
  
  //static t_pt * pt;
  static int n_pt,i_pvar=0;
  const char * label[6]={ "x","y","z","vx","vy","vz" },
  * lx=label[0], * ly=label[1], * lz=label[2];
  if (nret||outfile) {;}
  /* viewport coordinates */
  float st=0.05,
  wx1,wx2,wy1,wy2;
  
  char chaine[500];
  set_graph(dev,h,w); /* setup the graphic environnement */
  
  if (*first) {
    *first = false;
#if 0
    n_pt=0;
    for (j=0; j<ncolor_sel; j++) {
      n_pt+=nret[j];
    }
    std::cerr << "n_pt="<<n_pt<<"\n";
    pt = (t_pt *) malloc(sizeof(t_pt)*n_pt);
    
    if (!pt) {
      fprintf(stderr,"Memory allocation error on array : [pt] n_pt=%d ncolor_sel=%d\n",n_pt,ncolor_sel);
      exit(1);
    }
#endif
    if (pvar[0]=='x') {
      i_pvar=0;
      fprintf(stderr,"Positions being plotted....\n");
      lx = label[0];
      ly = label[1];
      lz = label[2];
    }
    else 
      if (pvar[0]=='v') {
      i_pvar=3;
      fprintf(stderr,"Velocities being plotted....\n");
      lx = label[3];
      ly = label[4];
      lz = label[5];
    }
    else {
      lx = label[0];
      ly = label[1];
      lz = label[2];
      fprintf(stderr,"BAD 'pvar'=[%s] parameter, positons assumed...\n",
              pvar);
    }
  } /* if first.... */
  
  t_pt * pt = new t_pt[nbody];;
  cpgpage();  /* clear screen */
  
  cpgsvp(0.0,1.0,0.0,1.0 /*0.90*/); /* set viewport */
  
  cpgswin(0.0,200.0,0.0,100.0);   /* set window */
  cpgptxt(10.0,95.0,0.0,0.0,title); /* print title */
  
  /* convert "floating" time in caracter array */
  sprintf(chaine,"%3.3f",tsnap);
  cpgsci(1);
  cpgtext(110.0,95.0,chaine); /* print snap time */
  /* print out X abciss */
  cpgsch(1.1);  /* set caracter height */
  cpgsci(1);
  cpgptxt(50.,89.0,0.0,0.5,label[0]); 
  cpgptxt(150.,89.0,0.0,0.5,lx); 
  
  /* processing the LEFT PART y=f(x) */
  
  /* Set the viewport to the rectangle left part */
  wx1=st;
  wx2=0.5-st;
  wy1=st;
  wy2=st+2*(wx2-wx1);
  cpgsvp(wx1,wx2,wy1,wy2);
  
  /* set the window to the world coordinates for the left part */
  cpgswin(range[0][0],range[0][1],range[1][0],range[1][1]);
  
  /* Box "look & feel" */
  cpgsch(1.1);  /* set caracter height */
  cpgbox("BCNST",0.0,0,"BCNST",0.0,0);
  cpglab(lx,ly,""); 
  cpgsch(1.5);  /* set caracter height */
  
  /* initialisation .... */
  ny = 0;
  /* loop on all particles */
  for (i=0 ,pp=data+i_pvar; i<nbody; i++, pp+=3) {
    /* loop on selected colors */
    for (j=0; j<ncolor_sel ; j++) {
      /* check if the particle is visible */
      if (
          pp[0] >= range[0][0] &&
          pp[0] <= range[0][1] &&
          pp[1] >= range[1][0] &&
          pp[1] <= range[1][1] ) {
        
        pt[ny].x  = pp[0];
        pt[ny].y = pp[1];
        pt[ny].z = pp[2];
        pt[ny].col = index_sel[j];
        ny++;
      }
    }
  }
  n_pt=ny;
  qsort(pt,n_pt,sizeof(t_pt),depht_sort_a);  
  /* according to z axis, plot from depht<0 to depht>0 */
  ny=0;
  save_color = pt[0].col;
  for (i=0; i<n_pt; i++) {
    if ((ny == size_buff-1) ||      /* full buffer */
        (pt[i].col != save_color))  {/* new color */
      /* plot the buffer */
      cpgsci(save_color);
      cpgpt(ny,buff_x,buff_y,symb);
      
      /* reset parameters */
      save_color = pt[i].col;
      ny = 0;
    }
    buff_x[ny] = pt[i].x;
    buff_y[ny] = pt[i].y;
    ny++;
  }
  /* flush the buffer */
  cpgsci(save_color);
  cpgpt(ny,buff_x,buff_y,symb);
  
  cpgsci(1);  /* restore default color */
  
  /* processing the RIGHT PART z=f(x) */
  /* Set the viewport to the rectangle right part */
  wx1=0.5+st,
  wx2=1-st,
  wy1=st,
  wy2=st+2*(wx2-wx1);
  cpgsvp(wx1,wx2,wy1,wy2);
  
  /* set the window to the world coordinates for the right part */
  cpgswin(range[0][0],range[0][1],range[2][0],range[2][1]);
  cpgsch(1.1);  /* set caracter height */
  cpgbox("BCNST",0.0,0,"BCNST",0.0,0);
  cpglab(lx,lz,""); 
  cpgsch(1.5);  /* set caracter height */
  
  /* initialisation .... */
  ny = 0;
  /* loop on all particles */
  for (i=0, pp=data+i_pvar; i<nbody; i++, pp+=3) {
    /* loop on selected colors */
    for (j=0; j<ncolor_sel ; j++) {
      /* check if the particle is visible */
      if (
          pp[0] >= range[0][0] &&
          pp[0] <= range[0][1] &&
          pp[2] >= range[2][0] &&
          pp[2] <= range[2][1]) {
        
        pt[ny].x = pp[0];
        pt[ny].y = pp[2];
        pt[ny].z = pp[1];
        pt[ny].col = index_sel[j];
        ny++;
      }
    }
    
  }
  n_pt=ny;
  qsort(pt,n_pt,sizeof(t_pt),depht_sort_d);  
  
  /* according y axis, plot from depht>0 to depht<0 */
  ny=0;
  save_color = pt[0].col;
  for (i=0; i<n_pt; i++) {
    if ((ny == size_buff-1) ||       /* full buffer */
        (pt[i].col != save_color)) { /* new color */
      /* plot the buffer */
      cpgsci(save_color);
      cpgpt(ny,buff_x,buff_y,symb);
      
      /* reset parameters */
      save_color = pt[i].col;
      ny = 0;
    }
    buff_x[ny] = pt[i].x;
    buff_y[ny] = pt[i].y;
    ny++;
  }
  
  /* flush the buffer */
  cpgsci(save_color);
  cpgpt(ny,buff_x,buff_y,symb);
  
  cpgsci(1);  /* restore default color */
  delete [] pt;
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
  
  
  //char *  select_pts[NBCOLORS];      /* selected data */
  
  char   outgif[80];
  
  int    nret[NBCOLORS];
  
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
  char * pvar        = getparam ((char *) "pvar"   );
  float  h           = getdparam((char *) "h"      );
  float  w           = getdparam((char *) "w"      );
  char * title       = getparam ((char *) "title"  );
  bool   com         = getbparam((char *) "com"    );
  bool   verbose     = getbparam((char *) "verbose");
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
  
  ncolor_sel=0;
  /* get the particles range according to the colors */

  for (int i=0; i<NBCOLORS; i++) {
    if (!strcmp(getparam((char *) "color"),tab_c[i].color)) { /* color i selected */
      /* get the particle range */
      //select_pts[ncolor_sel] = (char *) "dummy";
      
      /* get the color index */ 
      index_sel[ncolor_sel] = tab_c[i].index; 
      ncolor_sel++; /* #ncolor_sel is increase by one */
      
    }
  } 

  // instantiate a new uns object
  //s::Cuns * uns = new uns::Cuns(simname,select_c,select_t);
  uns::CunsIn * uns = new uns::CunsIn(simname,select_c,select_t,verbose);
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
      if (com) moveToCom(nbody,pos,mass);
      
      /* call engine */
      snapcompute(time,pos,nbody,nret,range,h,w,
                  &first,outfile,outgif,title,pvar);
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
