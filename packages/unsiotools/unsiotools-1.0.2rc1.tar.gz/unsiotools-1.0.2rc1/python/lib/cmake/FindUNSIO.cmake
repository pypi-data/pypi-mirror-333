# -*-cmake-*-
# ============================================================================
# Copyright Jean-Charles LAMBERT - 2008-2015
#           Centre de donneeS Astrophysiques de Marseille (CeSAM)       
# e-mail:   Jean-Charles.Lambert@lam.fr                                      
# address:  Aix Marseille Universite, CNRS, LAM 
#           Laboratoire d'Astrophysique de Marseille                          
#           Pole de l'Etoile, site de Chateau-Gombert                         
#           38, rue Frederic Joliot-Curie                                     
#           13388 Marseille cedex 13 France                                   
#           CNRS UMR 7326    
# ============================================================================
# CMake module to detect UNSIO library
# ============================================================================

if (NOT UNSIO_SETUP)

  set (UNSIO_SETUP 1) 
  typed_cache_set ( STRING "unsio setup" UNSIO_SETUP  1  )

  SET(UNSIO_FOUND FALSE)

  set (UNSIOLIB UNSIOLIB-NOTFOUND)

  if ( UNSIOPATH ) # user configure cmake with variable -DUNSIO_INSTALLPATH="/unsio/path"

    find_library(UNSIOLIB NAMES unsio PATHS ${UNSIOPATH}/lib)
    MESSAGE (STATUS "UNSIOLIB = " ${UNSIOLIB})
    if (NOT  ${UNSIOLIB} STREQUAL  UNSIOLIB-NOTFOUND)
      MESSAGE(STATUS "Found UNSIOLIB =" ${UNSIOLIB})
      SET(UNSIO_FOUND TRUE)
    else ()
    endif()
  endif ()

  if (NOT UNSIO_FOUND) # try NEMO
    MESSAGE (STATUS "UNSIOLIB = " ${UNSIOLIB} "  NEMO=" $ENV{NEMO})
    find_library(UNSIOLIB NAMES unsio PATHS /usr/${LIB_SUFFIX} $ENV{NEMO}/lib)
    MESSAGE (STATUS "UNSIOLIB = " ${UNSIOLIB} "  NEMO=" $ENV{NEMO})
    if ( NOT  ${UNSIOLIB} STREQUAL  UNSIOLIB-NOTFOUND)
      MESSAGE(STATUS "Found UNSIOLIB in NEMO =" ${UNSIOLIB})
      SET(UNSIO_FOUND TRUE)
      #SET(UNSIOPATH $ENV{NEMO})
      get_filename_component(UNSIOPATH ${UNSIOLIB} DIRECTORY )
      MESSAGE(STATUS "UNSIOPATH = " ${UNSIOPATH} )
    else ()
      MESSAGE(STATUS ">>>>>2")

    endif()
  endif()

  if (NOT UNSIO_FOUND) # try $HOME/local
    find_library(UNSIOLIB NAMES unsio PATHS $ENV{HOME}/local/unsio/lib)
    MESSAGE (STATUS "UNSIOLIB = " ${UNSIOLIB} " -- "  $ENV{HOME})
    if (NOT  ${UNSIOLIB} STREQUAL  UNSIOLIB-NOTFOUND)
      MESSAGE(STATUS "Found UNSIOLIB in $ENV{HOME}/local/unsio/ =" ${UNSIOLIB})
      SET(UNSIO_FOUND TRUE)
      SET(UNSIOPATH $ENV{HOME}/local/unsio)
    else ()
    endif()
  endif()

  if (NOT UNSIO_FOUND) #  ABORT
    message(SEND_ERROR "UNSIO not found - skipping building tests")
  else()
    typed_cache_set ( STRING "UNSIOPATH location"  UNSIOPATH ${UNSIOPATH}  )  
  endif()

endif () #NOT UNSIO_SETUP
