# -*-cmake-*-
# ============================================================================
# Copyright Jean-Charles LAMBERT - 2008-2025
#           Centre de donneeS Astrophysiques de Marseille (CeSAM)       
# e-mail:   Jean-Charles.Lambert@lam.fr                                      
# address:  Aix Marseille Universite, CNRS, LAM 
#           Laboratoire d'Astrophysique de Marseille                          
#           Pole de l'Etoile, site de Chateau-Gombert                         
#           38, rue Frederic Joliot-Curie                                     
#           13388 Marseille cedex 13 France                                   
#           CNRS UMR 7326    
# ============================================================================
# CMakeListst.txt file to compile UNSIO library
# ============================================================================

cmake_minimum_required(VERSION 3.15)

if (POLICY CMP0054)
  cmake_policy(SET CMP0054 NEW)
endif()

# project name
project (UNS_PROJECTS)

# extra path for NEMO
SET(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH} )
MESSAGE( STATUS "CMAKE_MODULE_PATH=" ${CMAKE_MODULE_PATH} )

# load setup flags
include(SetupFlags)

# use ccache if any
find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
  set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
  set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ccache)
endif(CCACHE_FOUND)

# Cpack Generator detection
include(DetectCpackGenerator)

# contains the full path to the top level directory of your build tree
MESSAGE( STATUS "PROJECT_BINARY_DIR: " ${PROJECT_BINARY_DIR} )

# contains the full path to the root of your project source directory,
# i.e. to the nearest directory where CMakeLists.txt contains the PROJECT() command
MESSAGE( STATUS "PROJECT_SOURCE_DIR: " ${PROJECT_SOURCE_DIR} )

MESSAGE( STATUS "CMAKE_BUILD_TYPE =" ${CMAKE_BUILD_TYPE} )
MESSAGE( STATUS "CMAKE_CXX_FLAGS  =" ${CMAKE_CXX_FLAGS} )
MESSAGE( STATUS "LIBRARY TYPE     =" ${LIBTYPE} )

MESSAGE( STATUS "core OPT  =" ${OPT} )
MESSAGE( STATUS "OSX detected =" ${OSX} )
MESSAGE( STATUS "BUILD_TYPE =" ${RELEASE} )

MESSAGE( STATUS "EXTRA_INCLUDES =" ${EXTRA_INCLUDES} )
MESSAGE( STATUS "EXTRA_LINK_DIRS =" ${EXTRA_LINK_DIRS} )

# require NEMO
FIND_PACKAGE(NEMO REQUIRED)
# require UNSIO
FIND_PACKAGE(UNSIO REQUIRED)
# require RPC
FIND_PACKAGE(RPCH REQUIRED)

# Sqlite3
#FIND_PACKAGE(SQLITE3)
# Boost (deprecated)
FIND_PACKAGE(BOOST)

MESSAGE( STATUS "NEMOLIB : " $ENV{NEMO}/lib )
MESSAGE( STATUS "DEHNEN :  " ${DEHNEN} )
MESSAGE( STATUS "PROJECT_BINARY_DIR: " ${PROJECT_BINARY_DIR} )
MESSAGE( STATUS "PROJECT_SOURCE_DIR: " ${PROJECT_SOURCE_DIR} )

# Make sure the linker can find the Hello library once it is built.
link_directories ( ${UNSIOPATH}/${LIB_SUFFIX} $ENV{NEMOLIB} /opt/homebrew/lib /opt/local/lib ${UNSIOPATH}/lib ${UNSIOPATH}/lib64 ${DEHNEN}/falcON/lib ${DEHNEN}/utils/lib $ENV{PGPLOT_DIR}  ${G2C_DIR} ${PROJECT_BINARY_DIR}/lib /usr/lib64 /usr/X11/lib ${RPC_LIB_PATH} ${FC_GFORT_PATH} ${FC_G77_PATH} ${EXTRA_LINK_DIRS})

# Destination path for the lib
SET(LIBRARY_OUTPUT_PATH lib)

# compilation options
#add_definitions(${OPT} -DNO_CUDA -DfalcON_NEMO -DfalcON_SINGLE  -funroll-loops -Wall ${DNOBOOST})

add_definitions(${OPT} -DNO_CUDA -DfalcON_NEMO -DfalcON_SINGLE  -Wall ${DNOBOOST})
SET(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${WARNCPP})
SET(CMAKE_C_FLAGS ${CMAKE_C_FLAGS} ${WARNC} )
SET(CMAKE_Fortran_FLAGS ${CMAKE_Fortran_FLAGS} ${WARNF})
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++03" )
MESSAGE( STATUS "CMAKE_CXX_FLAGS  =" ${CMAKE_CXX_FLAGS} )

# remove -DNDEBUG in RElease mode to keep activated assert calls
STRING(REPLACE "-DNDEBUG" ""  CMAKE_CXX_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})
message (STATUS "CMAKE_CXX_FLAGS_RELEASE = " ${CMAKE_CXX_FLAGS_RELEASE}  )

# Executable output path
set(EXECUTABLE_OUTPUT_PATH bin)
MESSAGE( STATUS "EXECUTABLE_OUTPUT_PATH: " ${EXECUTABLE_OUTPUT_PATH} )

# Make sure the compiler can find include files from our Hello library.
include_directories (${PROJECT_SOURCE_DIR}/src )
include_directories (${PROJECT_SOURCE_DIR}/lib/utils ${PROJECT_SOURCE_DIR}/lib/utils/nemodep )
include_directories (${PROJECT_SOURCE_DIR}/lib/projects ${PROJECT_SOURCE_DIR}/lib/projects/nemodep)
include_directories (/usr/include/CCfits /usr/include/cfitsio /opt/usr/include /opt/usr/include/CCfits ${RPC_H_PATH})
include_directories (${EXTRA_INCLUDES})
if ( FALCON_INSTALLED )
  include_directories (${DEHNEN}/falcON/utils/inc ${DEHNEN}/falcON/inc)
endif()
include_directories (${UNSIOPATH}/lib ${UNSIOPATH}/include ${UNSIOPATH}/include/nemo ${UNSIOPATH}/include/uns $ENV{NEMO}/inc $ENV{NEMO}/inc/uns $ENV{NEMO}/lib)
include_directories (/usr/include/malloc)

# ----------------------------------------------------------
# Install SETUP
# ----------------------------------------------------------
mark_as_advanced(CMAKE_INSTALL_PREFIX)

if ( "XX${CMAKE_INSTALL_PREFIX}" STREQUAL "XX$ENV{NEMO}" )
  SET(PREFIX_LIB lib)
else()
  SET(PREFIX_LIB ${LIB_SUFFIX})
endif()

if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT) 
  set (CMAKE_INSTALL_PREFIX ${UNSIOPATH})
endif()
MESSAGE( STATUS "--------> CMAKE_INSTALL_PREFIX =" ${CMAKE_INSTALL_PREFIX} )

# special flags for MacOSX
if (OSX)
  set(CMAKE_MACOSX_RPATH ON)
  message(STATUS ">>>> CMAKE_MACOSX_RPATH = " ${CMAKE_MACOSX_RPATH})
endif()


# for installation
IF   (OSX) # Mac OSX
  SET(SOEXT "dylib")
ELSE (OSX) # Linux
  SET(SOEXT "so")
ENDIF(OSX)

# use, i.e. don't skip the full RPATH for the build tree
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
# when building, don't use the install RPATH already
# (but later on when installing)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/${PREFIX_LIB}")

# add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# the RPATH to be used when installing, but only if it's not a system directory
LIST(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/${PREFIX_LIB}" isSystemDir)
IF("${isSystemDir}" STREQUAL "-1")
   SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/${PREFIX_LIB}")
   message(STATUS "SKBUILD_PLATLIB_DIR = " ${SKBUILD_PLATLIB_DIR})
ENDIF("${isSystemDir}" STREQUAL "-1")

# ----------------------------------------------------------
# add different sub-projects
# add lib/utils
add_subdirectory(${PROJECT_SOURCE_DIR}/lib/utils)
# add lib/projects
add_subdirectory(${PROJECT_SOURCE_DIR}/lib/projects)
# add src
if (NOT SKBUILD_PROJECT_NAME)
  add_subdirectory(${PROJECT_SOURCE_DIR}/src)
endif()

# ----------------------------------------------------------
# python module
IF (SKBUILD_PROJECT_NAME)
  # -----------------------------------
  # trigger by python installation
  # pip install .
  # python -m build
  # -----------------------------------
  # Python binding
  add_subdirectory(${PROJECT_SOURCE_DIR}/python)

ELSE()
  # ----------------------------------------------------------
  # remaining install stuffs

  # Manuals
  FILE(GLOB manuals  ${PROJECT_SOURCE_DIR}/man/*.1)
  FOREACH(install_man ${manuals})
    INSTALL(FILES  ${install_man}  DESTINATION man/man1)
  ENDFOREACH()
ENDIF()
#
