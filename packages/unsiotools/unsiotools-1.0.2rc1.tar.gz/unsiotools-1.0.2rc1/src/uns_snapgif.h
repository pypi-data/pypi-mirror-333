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

#ifndef UNS_SNAPGIF_H
#define UNS_SNAPGIF_H

void set_graph(char * dev,float h,float w);
int depht_sort_a(t_pt * i, t_pt *j);
int depht_sort_d(t_pt * i, t_pt *j);
void snapcompute(float tsnap,float * data,int nbody,int * nret,float range[3][2], float h, float w, bool * first char * outfile,char * dev,char * title,char * pvar);
void setrange(float range[],char * ch_range);

#endif
