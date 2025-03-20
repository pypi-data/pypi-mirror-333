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
# CMake module to detect RPC library
# ============================================================================


SET(RPC_FOUND FALSE)
SET(DNORPC "-DNORPC") # if RPC does not exist
SET(RPC_LIB_PATH "")
SET(RPC_H_PATH "")
SET(RPC_LIB "")
SET(RPC_NAME_LIB "")
SET (RPC_H "RPC_H-NOTFOUND")
find_file(RPC_H "rpc/rpc.h" PATHS /usr/include /usr/include/tirpc NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
MESSAGE (STATUS "RPC_H = " ${RPC_H})
IF (EXISTS ${RPC_H})
  get_filename_component(RPC_H_PATH  ${RPC_H} PATH)
  SET(RPC_H_PATH ${RPC_H_PATH}/..)
  MESSAGE(STATUS "Found rpc.h:" ${RPC_H})
  MESSAGE(STATUS "Found rpc.h path:" ${RPC_H_PATH})
  find_library(RPC NAMES tirpc PATH /usr/lib64 /usr/lib /usr/lib/x86_64-linux-gnu)
  IF (RPC)
    SET(RPC_FOUND TRUE)
    SET(DNORPC "") # RPC exist
    SET(RPC_LIB RPC)
    SET(RPC_NAME_LIB "tirpc")
    MESSAGE(STATUS "Found library here :" ${RPC})
    get_filename_component(RPC_LIB_PATH  ${RPC} PATH)
    MESSAGE(STATUS "Found library PATH :" ${RPC_LIB_PATH})    
  ENDIF(RPC)
else ()
    if ( _CMAKE_APPLE_ARCHS_DEFAULT STREQUAL "arm64" )
       MESSAGE(STATUS "OSX :" ${_CMAKE_APPLE_ARCHS_DEFAULT} )
    else()
       MESSAGE(SEND_ERROR "rpc.h not found - please install the corresponding package")
    endif()
ENDIF() 
