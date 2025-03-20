// ============================================================================
// Copyright Jean-Charles LAMBERT - 2008-2025
//           Centre de donneeS Astrophysiques de Marseille (CeSAM)          
// e-mail:   Jean-Charles.Lambert@lam.fr                                      
// address:  Aix Marseille Universite, CNRS, LAM 
//           Laboratoire d'Astrophysique de Marseille                          
//           Pole de l'Etoile, site de Chateau-Gombert                         
//           38, rue Frederic Joliot-Curie                                     
//           13388 Marseille cedex 13 France                                   
//           CNRS UMR 7326                                       
// ============================================================================

/* 
  @author Jean-Charles Lambert <Jean-Charles.Lambert@lam.fr>
 */
#ifndef NOSQLITE3  // do not compite if no sqlite3 lib
#include "snapshotsim.h"
#include "snapshotgadget.h"
#include "snapshotgadgeth5.h"
#include "snapshotnemo.h"
#include "snapshotramses.h"
#include "ctools.h"
#include <sstream>
#include <iomanip>
#include <iostream>

#include <cstdio>
#include <cstdlib>

#define DEBUG 0
#include "unsdebug.h"
#include "uns.h"

namespace uns {
// ASCII database
template <class T>  std::string uns::CSnapshotInterfaceIn<T>::sim_db_file="/pil/programs/DB/sim_info.txt";
template <class T>  std::string uns::CSnapshotInterfaceIn<T>::nemo_range_file="/pil/programs/DB/nemo_range.txt";
template <class T>  std::string uns::CSnapshotInterfaceIn<T>::eps_db_file="/pil/programs/DB/sim_eps.txt";
// SQLITE database

// ----------------------------------------------------------------------------
// constructor
template <class T> CSnapshotSimIn<T>::CSnapshotSimIn(const std::string _name,
                               const std::string _comp,
                               const std::string _time,
                               const bool        verb)
  :CSnapshotInterfaceIn<T>(_name, _comp, _time, verb)
{
  snapshot = NULL;
  sql      = NULL;
  nframe   = 0;   // # frames read
  nemosim  = "";
  this->verbose  = verb;
  sim_filename = this->filename;
  sel_from_index = false;
  force_stop = false;
  checkSimIndex(); // check if index has been specified with simname
  if (0) {
    this->valid=openDbFile();
  } else { // SQLite3
    this->valid=openSqlDb();
  }
}
// ----------------------------------------------------------------------------
// constructor
template <class T> CSnapshotSimIn<T>::~CSnapshotSimIn()
{
  if (snapshot) delete snapshot;
  if (sql) delete sql;
}
// ============================================================================
// getSnapshotRange                                                            
template <class T> ComponentRangeVector * CSnapshotSimIn<T>::getSnapshotRange()
{
  assert(snapshot != NULL);
  assert(snapshot->isValidData());
  if ((tools::Ctools::tolower(this->interface_type) == "nemo") && nemosim != "" && crv.size()>0) {
    return &crv;
  }
  else {
    return snapshot->getSnapshotRange();
  }
}
// ============================================================================
// getSnapshotRange 
template <class T> int CSnapshotSimIn<T>::nextFrame(uns::UserSelection &user_select)
{
  assert(snapshot != NULL);
  assert(snapshot->isValidData()==true);
  snapshot->setNsel(this->nsel);
  return (snapshot->nextFrame(user_select));
}
// ============================================================================
// nextFrame 
template <class T> int CSnapshotSimIn<T>::nextFrameSelect(ComponentRangeVector * crvs)
{
  snapshot->user_select.setSelection(this->getSelectPart(),crvs);
  this->setNsel(snapshot->user_select.getNSel());
  snapshot->setReqBits(this->req_bits);
  snapshot->setNsel(snapshot->user_select.getNSel());
  return(snapshot->nextFrame(snapshot->user_select));
}
// ============================================================================
// checkSimIndex
template <class T> bool CSnapshotSimIn<T>::checkSimIndex()
{
  std::size_t found = sim_filename.find("%");
  if (found!= std::string::npos) { // % found
    std::string name=sim_filename.substr(0,found);
    std::string index=sim_filename.substr(found+1,sim_filename.length()-1);
    std::istringstream s_nframe(index);
    s_nframe >> nframe; // convert string to int
    if (this->verbose) {
      std::cerr << "checkSimIndex name =" << name << " index=" << index << " nframe="<< nframe <<"\n";
    }
    sim_filename=name; // set a correct name for the simulation
    sel_from_index = true;
  }
  return sel_from_index;
}

//                     - - - - - - - - - - - - - - 
//                           SQlite database       
//                     - - - - - - - - - - - - - - 

// ============================================================================
// openSqlDb                                                                   
template <class T> bool CSnapshotSimIn<T>::openSqlDb(std::string db)
{
  sqlite_db = db;
  std::string mydbname=this->parseConfig("dbname");
  if (mydbname != "" ) {
    sqlite_db = mydbname;
  }
  if (this->verbose) {
    std::cerr << "Using sqlite3 database file [" << sqlite_db << "]\n";
  }
  sql = new jclt::CSQLite3(sqlite_db);
  bool status=sql->isOpen();
  if (! status) {
    std::cerr << "Unable to load sqlite3 database file [" << sqlite_db << "]\n";
    //std::cerr << __FILE__<< " " << __LINE__ << "Aborting ....\n";
    //std::exit(1);
  } else {
    status = findSqlSim();
    if (status) {
      eps_exist = readSqlEps();
    } else {
      eps_exist = false;
    }
  }
  return status;
}
// ============================================================================
// findSqlSim                                                                  
template <class T> bool CSnapshotSimIn<T>::findSqlSim()
{
  std::string select="select * from info where name='"+sim_filename+"'";
  if (this->verbose) std::cerr << "select = "<<select <<"\n";
  int status = sql->exe(select);
  if (status) {
    if (this->verbose) sql->display();
    assert(sql->vdata[0]==sim_filename);
    simname        = sql->vdata[0];
    simtype        = sql->vdata[1];
    dirname        = sql->vdata[2];
    basename       = sql->vdata[3];
    
    this->interface_type = simtype;
#if 0  // off since march/07/2016
    if (tools::Ctools::tolower(this->interface_type) == "gadget") this->interface_index=1;
    else
      if (tools::Ctools::tolower(this->interface_type) == "nemo") this->interface_index=0;
      else
        if (tools::Ctools::tolower(this->interface_type) == "ramses") this->interface_index=2;
        else {
          std::cerr <<"CSnapshotSimIn<T>::findSqlSim => Unknown interface type....\n";
        }
#endif
  }
  return status;
}
// ============================================================================
// readSqlEps                                                                  
template <class T> bool CSnapshotSimIn<T>::readSqlEps()
{
  std::string select="select * from eps where name='"+sim_filename+"'";
  if (this->verbose) std::cerr << "select = "<<select <<"\n";
  int status = sql->exe(select);
  if (status) {
    if (this->verbose) sql->display();
    assert(sql->vdata[0]==sim_filename);
    std::stringstream str("");
    for (unsigned int i=1; i< sql->vdata.size(); i++) {
      str << sql->vdata[i];  // convert string to stream string
      str >> this->eps[i-1];       // convert to float
    }
  }
  return status;
}
// ============================================================================
// fillSqlNemoRange                                                            
// look for simulation in Sql Database file                                    
template <class T> bool CSnapshotSimIn<T>::fillSqlNemoRange()
{
  std::string select="select * from nemorange where name='"+sim_filename+"'";
  if (this->verbose) std::cerr << "select = "<<select <<"\n";
  int status = sql->exe(select);
  if (status) {
    if (this->verbose) sql->display();
    int offset=0;
    assert(sql->vdata[0]==sim_filename);
    addNemoComponent(offset,sql->vdata[1],"all"  );
    addNemoComponent(offset,sql->vdata[2],"disk" );
    addNemoComponent(offset,sql->vdata[3],"bulge");
    addNemoComponent(offset,sql->vdata[4],"halo" );
    addNemoComponent(offset,sql->vdata[5],"halo2");
    addNemoComponent(offset,sql->vdata[6],"gas"  );
    addNemoComponent(offset,sql->vdata[7],"bndry");
    addNemoComponent(offset,sql->vdata[8],"stars");
  }
  return status;
}
//                       - - - - - - - - - - - - - - 
//                             ASCII database        
//                       - - - - - - - - - - - - - - 

// ============================================================================
// opendbFile                                                                  
template <class T> bool CSnapshotSimIn<T>::openDbFile()
{
  bool status=true;
  fi.open(this->sim_db_file.c_str(),std::ios::in);
  if (! fi.is_open()) {
    std::cerr << "Unable to open file ["<<sim_filename<<"] for reading, aborting...\n";
    status = false;
  }
  if (status) {
    status = findSim();
    if (status) {
      eps_exist = readEpsFile();
    } else {
      eps_exist = false;
    }
  }
  return status;
}
// ============================================================================
// findSim                                                                     
// look for simulation in Database file                                        
template <class T> bool CSnapshotSimIn<T>::findSim()
{
  bool status=false;
  bool stop = false;
  while (!stop && ! fi.eof()) {           // while ! eof
    std::string line;
    getline(fi,line); // read on eline
    if ( ! fi.eof()) {
      std::istringstream str(line);  // stream line
      std::string parse;
      // following loop parse each lines previously read
      //
      int cpt=0;
      while (  str >> parse   &&              // something to read
               parse[0] != '#' &&             // not commented out
               parse[0] != '!'                // not commented out
               ) {
        cpt++;
        if (cpt==1) { // simname
          simname=parse;
        }
        if (cpt==2) { // sim type
          //std::istringstream ss(parse);
          //ss >> simtype;
          simtype=parse;
          this->interface_type = simtype;
//          if (this->interface_type == "Gadget") this->interface_index=1;
//          else
//            if (this->interface_type == "Nemo") this->interface_index=0;
//            else {
//              std::cerr <<"CSnapshotSimIn<T>::findSim => Unknown interface type....\n";
//            }
        }
        if (cpt==3) { // sim's dirname
          dirname=parse;
        }
        if (cpt==4) { // sim's basename
          basename=parse;
        }
      }
      if (simname == sim_filename) { // we found simulation
        stop   = true; // we have a snapshot
        status = true; // so we can stop reading
        std::cerr << "SIM DB:Found simulation ["<<simname<<"] in database !\n";
      }
      if (cpt != 4) {
        std::cerr << "\n\nWarning, bad #strings ["<<cpt<<"] parsed\n"
                  << "during CSnapshotSimIn<T>::findSim()....\n";
      }
    }
    else { // end of file
      stop   = true;
      status = false;
    }
  }
  return status;
}
// ============================================================================
// readEpsFile                                                                 
// Read Eps database file                                                      
template <class T> bool CSnapshotSimIn<T>::readEpsFile()
{
  bool stop = false;
  bool status=true;

  std::ifstream fi;
  std::string simname;
  fi.open(this->eps_db_file.c_str(),std::ios::in);
  if (! fi.is_open()) {
    std::cerr << "Warning !!! Unable to open file ["<<sim_filename<<"] for reading...\n";
    status = false;
  }
  if (status) {
    while (!stop && ! fi.eof()) {           // while ! eof
      std::string line;
      getline(fi,line); // read on eline
      if ( ! fi.eof()) {
        std::istringstream str(line);  // stream line
        std::string parse;
        // following loop parse each lines previously read
        //
        int cpt=0;
        while (  str >> parse    &&             // something to read
                 parse[0] != '#' &&             // not commented out
                 parse[0] != '!'                // not commented out
                 ) {
          cpt++;
          if (cpt==1) { // simname
            simname=parse;
            if (simname == sim_filename) { // we found simulation
              //stop   = true; // we have a snapshot
              status = true; // we have all components
              std::cerr << "EPS:Found simulation ["<<simname<<"] in database !\n";
            }
          }
          if (simname == sim_filename) { // we found simulation
            std::istringstream ss(parse);
            if (cpt < MAX_EPS+2) { //
              ss >> this->eps[cpt-2];    // file EPS array
            }
          }
        } // while ( str ....
        //
        if (simname == sim_filename) {
          stop=true;     // simulation has been found
          assert(cpt>1); // we must have read at least one eps

          // copy last eps read to next eps
          // it's a trick for NEMO simulations
          // which have only one eps
          for (int i=cpt-1; i<MAX_EPS; i++) {
            std::cerr << "eps shift i="<<i<<" cpt="<<cpt<<" eps="<<this->eps[cpt-2]<<"\n";
            this->eps[i] = this->eps[cpt-2];
          }
        }
      } // if !eof ...
      else { // end of file
        stop   = true;
        status = false;
      }
    } // while (!stop ...
  } // if (status....
  if (! status) {
    std::cerr<<"\n\nWARNING, simulation ["<<sim_filename<<"] has no entry in the"
            <<"EPS datafile ["<<uns::CSnapshotInterfaceIn<T>::eps_db_file<<"]\n\n";
  }
  return status;
}

// ============================================================================
// getEps                                                                      
// return the component according to the component requested                   
// if eps does not exist return -1                                             
template <class T> T CSnapshotSimIn<T>::getEps(const std::string comp)
{
  T status=-1.0;
  if (eps_exist) {
    if (comp == "gas"  ) status=this->eps[0];
    if (comp == "halo" ) status=this->eps[1];
    if (comp == "disk" ) status=this->eps[2];
    if (comp == "bulge") status=this->eps[3];
    if (comp == "stars") status=this->eps[4];
  }
  //std::cerr << "comp ="<<comp<<" status="<<status<<" eps_exist="<<eps_exist<<"\n";
  return status;
}
// ============================================================================
// fillNemoRange                                                               
// look for simulation in Database file                                        
template <class T> bool CSnapshotSimIn<T>::fillNemoRange()
{
  bool stop = false;
  bool status=true;

  std::ifstream fi;
  int offset;
  fi.open(this->nemo_range_file.c_str(),std::ios::in);
  if (! fi.is_open()) {
    std::cerr << "Unable to open file ["<<sim_filename<<"] for reading, aborting...\n";
    status = false;
  }
  if (status) {
    while (!stop && ! fi.eof()) {           // while ! eof
      std::string line;
      getline(fi,line); // read on eline
      if ( ! fi.eof()) {
        std::istringstream str(line);  // stream line
        std::string parse;
        // following loop parse each lines previously read
        //
        int cpt=0;
        while (  str >> parse    &&             // something to read
                 parse[0] != '#' &&             // not commented out
                 parse[0] != '!'                // not commented out
                 ) {
          cpt++;
          if (cpt==1) { // simname
            simname=parse;
            if (simname == sim_filename) { // we found simulation
              stop   = true; // we have a snapshot
              status = true; // we have all components
              std::cerr << "Found simulation ["<<simname<<"] in database !\n";
              crv.clear();
              offset=0;
            }
          }
          if (simname == sim_filename) { // we found simulation
            if (cpt==2) { // #total
              addNemoComponent(offset,parse,"all");
            }
            if (cpt==3) { // #disk
              addNemoComponent(offset,parse,"disk");
            }
            if (cpt==4) { // #bulge
              addNemoComponent(offset,parse,"bulge");
            }
            if (cpt==5) { // #halo
              addNemoComponent(offset,parse,"halo");
            }
            if (cpt==6) { // #halo2
              addNemoComponent(offset,parse,"halo2");
            }
          }
        } // while ( str ....
      } // if !eof ...
      else { // end of file
        stop   = true;
        status = false;
      }
    } // while (!stop ...
  } // if (status....

  return status;
}
// ============================================================================
// addNemoComponent                                                            
template <class T> int CSnapshotSimIn<T>::addNemoComponent(int& offset, std::string parse,
                                     std::string comp )
{
#if 0
  int nbody;
  std::istringstream ss(parse);
  ss >> nbody;
  if (nbody) {
    uns::ComponentRange cr;
    cr.setData(offset,nbody-1,comp);
    crv.push_back(cr);
    if (comp!="all") {
      offset+=nbody;
    }
  }
  return offset;
#else
  if (parse!="") { // there is something for the component
    std::size_t found = parse.find(":");

    std::istringstream ss("");
    //std::cerr << "substr=[" << parse.substr(0,found-1) << "]\n";
    ss.str(parse.substr(0,found));
    int start;
    ss >> start;
    ss.clear();
    ss.str(parse.substr(found+1));
    int end;
    ss >> end;
    uns::ComponentRange cr;
    //std::cerr << "parse="<< parse << " start="<< start << " end="<< end << " comp="<<comp << "\n";
    cr.setData(start,end,comp);
    crv.push_back(cr);
  }
  return 1;
#endif
}
// ============================================================================
// isNewFrame                                                                  
template <class T> bool CSnapshotSimIn<T>::isNewFrame()
{
  bool status=false;
  if (this->valid) {
    if (tools::Ctools::tolower(simtype)=="gadget" ||
        tools::Ctools::tolower(simtype)=="gadget3") {
      status=buildAllGadgetFile();
    }
    else {
      if (tools::Ctools::tolower(simtype)=="nemo") {
        status=buildNemoFile();
      }
      else {
        if (tools::Ctools::tolower(simtype)=="ramses") {
          status=buildRamsesFile();
        }
        else {          
          std::cerr <<"\nUnknown simulation type ["<<simtype<<"]\n";
        }
      }
    }
    if (status) {
      this->interface_type  = snapshot->getInterfaceType();
      this->interface_index = snapshot->getInterfaceIndex();
    }
  }
  return status;
}
// ============================================================================
// buildNemoFile                                                             
template <class T> bool CSnapshotSimIn<T>::buildNemoFile()
{
  bool status=false;
  if (nemosim != "") {
    status = true;
  }
  else {
    std::string myfile=dirname+'/'+basename;
    if (snapshot) delete snapshot;
    if (0) { // ASCII database
      if (fillNemoRange()) {
        if (this->verbose) uns::ComponentRange::list(&crv);
      }
    } else {
      if (fillSqlNemoRange()) {
        if (this->verbose) uns::ComponentRange::list(&crv);
      }
    }
    // try to open NEMO sim
    PRINT("trying top instantiate  CSnapshotNemo("<<myfile<<") verbose="<<this->verbose<<"\n";)
        snapshot = new CSnapshotNemoIn<T>(myfile, this->select_part, this->select_time,this->verbose);
    if (snapshot->isValidData()) {
      status=true;
      nemosim=myfile;
    } else {
      status=false;
    }
  }
  return status;
}

// ============================================================================
// buildAllGadgetFile (gadget 1,2 or 3 format)
template <class T> bool CSnapshotSimIn<T>::buildAllGadgetFile()
{
  bool stop=false,status=false;
  int cpt=1;
  // loop on all the possibility of file
  // dirname+basename+nframe
  // ex : gas001_0 gas001_00 gas001_000
  while (!force_stop && !stop && cpt<=5) {
    std::stringstream ss("");
    ss << std::setw(cpt) << std::setfill('0') << nframe;
    std::string myfile = dirname+'/'+basename+'_'+ss.str();
    PRINT("CSnapshotSimIn<T>::buildGadgetFile()  myfile=["<<myfile<<"]\n";)

    if (snapshot) delete snapshot;
    // try to open Gadget1/2 file
    snapshot = new CSnapshotGadgetIn<T>(myfile, this->select_part, this->select_time, this->verbose);
    if (!snapshot->isValidData()) {
      delete snapshot;

      // try to open gadget3 file with ".hdf5 extension"
      snapshot = new CSnapshotGadgetH5In<T>(myfile+".hdf5", this->select_part, this->select_time, this->verbose);

      if (!snapshot->isValidData()) {
        delete snapshot;
        // try to open gadget3 file without ".hdf5 extension"
        snapshot = new CSnapshotGadgetH5In<T>(myfile, this->select_part, this->select_time, this->verbose);
      }

    }
    if (snapshot->isValidData()) {                // file exist
      T t;
      bool ok=snapshot->getData("time",&t);
      if (ok && this->checkRangeTime(t)) {              //  time in range
        status=true;                              //   valid snap
        stop=true;                                //   get out loop
      } else {                                    //  time out of range
        delete snapshot;                          //   del object
        snapshot = NULL;                          //   NULL for the next
        nframe++;                                 //   try next frame
      }
    }
    else {                                        // file does not exist
      delete snapshot;
      snapshot = NULL;
      cpt++;
    }
  }

  if (status) {
    nframe++;  // next frame index
  }
  if (sel_from_index) { // occurs only one time
    force_stop = true;
  }
  return status;
}
// ============================================================================
// buildRamsesFile
template <class T> bool CSnapshotSimIn<T>::buildRamsesFile()
{
  bool status=false;

  std::string myfile = dirname+'/'+basename;
  if (nframe==0) {
    snapshot = new CSnapshotRamsesIn<T>(myfile, this->select_part, this->select_time, this->verbose);
    if (snapshot->isValidData()) {                // file exist
      T t;
      bool ok=snapshot->getData("time",&t);
      if (ok && this->checkRangeTime(t)) {              //  time in range
        status=true;                              //   valid snap
        nframe++;
      } else {                                    //  time out of range
        delete snapshot;                          //   del object
        snapshot = NULL;                          //   NULL for the next
        nframe++;                                 //   try next frame
      }
    }
    else {                                        // file does not exist
      delete snapshot;
      snapshot = NULL;
    }
  }
  return status;
}
// ============================================================================
// getCod
// returns: 
// -2 file exist but can't open
// -1 file does not exist
// 0  time does not exist
// 1  time found 

template <class T> int CSnapshotSimIn<T>::getCod(const std::string select,
                           const float time, float * tcod,
                           const std::string base, const std::string ext)
{
  int status=-3;  // sim not valid
  if (this->valid) {
    std::string codfile=dirname+'/'+base+'/'+simname+'.'+select+'.'+ext;
    if (tools::Ctools::isFileExist(codfile)) { // cod file exist
      std::cerr << "cod file = "<< codfile << "\n";
      std::ifstream fi;
      status = 0;
      fi.open(codfile.c_str(),std::ios::in);
      if (! fi.is_open()) {
        std::cerr << "Unable to open file ["<<codfile<<"] for reading...\n";
        status = -2;
      }
      else {
        bool stop=false;
        while (!stop && ! fi.eof()) {           // while ! eof
          status = 0; // time not match
          std::string line;
          getline(fi,line); // read line by line
          if ( ! fi.eof()) {
            std::istringstream str(line);  // stream line
            std::string parse;
            int cpt=0;
            // get time
            str >> parse;                 // read time
            std::stringstream str2(""); // convert to stream
            str2 << parse;
            str2 >> tcod[cpt++];              // convert to float
            if (tcod[0]-0.00001 < time && tcod[0]+0.00001 > time) {
              while (  str >> parse    &&             // something to read
                       parse[0] != '#' &&             // not commented out
                       parse[0] != '!'                // not commented out
                       ) {
                assert(cpt < 7);
                std::stringstream str2(parse); // read cod data
                str2 >> tcod[cpt++];          // store in float array
              } // while str >> ...
              assert(cpt==7); // bc cpt+1
              status=1;  // match cod time
              stop=true; //  we can stop so read
            } // if (tcod[0]-0.00
          } // !fi.eof
        } // while !stop....
      } // else
      fi.close(); // close cod file
    } else { // cod file does not exist
      status=-1;
      std::cerr << "cod file = "<< codfile << " does not exist\n";
    }
  }
  return status;
}
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Templates instantiation MUST be declared **AFTER** templates declaration
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// C++11
//extern template class CSnapshotSimIn<float>;
template class CSnapshotSimIn<float>;
//extern template class CSnapshotSimIn<double>;
template class CSnapshotSimIn<double>;
} // end of namespace
#endif // NOSQLITE3
