# -*-cmake-*-
# ============================================================================
# Copyright Jean-Charles LAMBERT - 2008-2025
# e-mail:   Jean-Charles.Lambert@oamp.fr
# address:  Dynamique des galaxies
#           Centre de donneeS Astrophysique de Marseille (CeSAM)
#           Laboratoire d'Astrophysique de Marseille
#           Pole de l'Etoile, site de Chateau-Gombert
#           38, rue Frederic Joliot-Curie
#           13388 Marseille cedex 13 France
#           CNRS U.M.R 6110
# ============================================================================
# CMake module to detect UNSIO library
# ============================================================================

if (NOT UNSIO_SETUP)

  set (UNSIO_SETUP 1) 
  typed_cache_set ( STRING "unsio setup" UNSIO_SETUP  1  )

  SET(UNSIO_FOUND FALSE)

  set (UNSIOLIB UNSIOLIB-NOTFOUND)

  if ( UNSIOPATH ) # user configure cmake with variable -DUNSIO_INSTALLPATH="/unsio/path"

    find_library(UNSIOLIB NAMES unsio PATHS ${UNSIOPATH}/lib  ${UNSIOPATH}/lib64 NO_DEFAULT_PATH)
    MESSAGE (STATUS "UNSIOLIB = " ${UNSIOLIB})
    if (NOT  ${UNSIOLIB} STREQUAL  UNSIOLIB-NOTFOUND)
      MESSAGE(STATUS "Found UNSIOLIB =" ${UNSIOLIB})
      SET(UNSIO_FOUND TRUE)
    else ()
    endif()
  endif ()

  if (NOT UNSIO_FOUND) # try system 
    MESSAGE (STATUS "Trying UNSIOLIB = " ${UNSIOLIB} "  from system=/usr/${LIB_SUFFIX}" )
    find_library(UNSIOLIB NAMES unsio PATHS /usr/${LIB_SUFFIX} NO_DEFAULT_PATH)
    if ( NOT  ${UNSIOLIB} STREQUAL  UNSIOLIB-NOTFOUND)
      MESSAGE(STATUS "Found UNSIOLIB in system =" ${UNSIOLIB})
      SET(UNSIO_FOUND TRUE)
      SET(UNSIOPATH /usr)
      MESSAGE(STATUS "UNSIO found in /usr/${LIB_SUFFIX}")
    else ()
      MESSAGE(STATUS "UNSIO not found in /usr/${LIB_SUFFIX}")
    endif()
  endif()

  if (NOT UNSIO_FOUND) # try $HOME/local
    find_library(UNSIOLIB NAMES unsio PATHS $ENV{HOME}/local/unsio/${LIB_SUFFIX} NO_DEFAULT_PATH)
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

  message(STATUS "UNSIOPATH = " ${UNSIOPATH})
endif () #NOT UNSIO_SETUP
