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

project(PYTHON_UNSIOTOOLS)

if (NOT SKBUILD_PROJECT_NAME)
  # extra path for NEMO
  SET(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/../cmake ${CMAKE_MODULE_PATH} )
  # load setup flags
  include(SetupFlags)
  # Cpack Generator detection
  include(DetectCpackGenerator)

  # require NEMO
  FIND_PACKAGE(NEMO REQUIRED)
  # require UNSIO
  FIND_PACKAGE(UNSIO REQUIRED)
  add_definitions(-DfalcON_NEMO -DfalcON_SINGLE -DNOBOOST)
  add_compile_options($<$<COMPILE_LANGUAGE:CXX>:-std=c++03>)
  link_directories ( ${UNSIOPATH}/${LIB_SUFFIX} $ENV{NEMOLIB} /opt/local/lib ${UNSIOPATH}/lib ${UNSIOPATH}/lib64 ${DEHNEN}/falcON/lib ${DEHNEN}/utils/lib $ENV{PGPLOT_DIR}  ${G2C_DIR} ${PROJECT_BINARY_DIR}/lib /usr/lib64 /usr/X11/lib ${RPC_LIB_PATH} ${FC_GFORT_PATH} ${FC_G77_PATH} ${EXTRA_LINK_DIRS})
  MESSAGE(STATUS "==> NOT IN SKBUILD_PROJECT_NAME process")
endif()
# package required to build python wrapper
FIND_PACKAGE(SWIG REQUIRED)
FIND_PACKAGE(Python REQUIRED Interpreter Development.Module)

MESSAGE(STATUS "==== python wrapper ====")
MESSAGE(STATUS "SWIG_EXECUTABLE =" ${SWIG_EXECUTABLE})
MESSAGE(STATUS "Python_EXECUTABLE =" ${Python_EXECUTABLE})
MESSAGE(STATUS "CMAKE_CURRENT_SOURCE_DIR =" ${CMAKE_CURRENT_SOURCE_DIR})
MESSAGE(STATUS "CMAKE_CURRENT_BINARY_DIR =" ${CMAKE_CURRENT_BINARY_DIR})
MESSAGE(STATUS "SKBUILD_PROJECT_NAME =" ${SKBUILD_PROJECT_NAME})

MESSAGE(STATUS "CMAKE_INSTALL_RPATH=" ${CMAKE_INSTALL_RPATH})
# Grab the variables from a local Python installation F2PY headers
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "import numpy; print(numpy.get_include())"
  OUTPUT_VARIABLE NUMPY_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE)
MESSAGE(STATUS "NUMPY_INCLUDE_DIR =" ${NUMPY_INCLUDE_DIR})

# Generate the wrapper files
add_custom_command(
  OUTPUT py_unstools.py py_unstools_wrap.cxx
  COMMAND ${SWIG_EXECUTABLE} -c++ -python -I${CMAKE_CURRENT_SOURCE_DIR}/../src -I${CMAKE_CURRENT_SOURCE_DIR}/../lib/projects 
           -I${CMAKE_CURRENT_SOURCE_DIR}/../lib/projects/nemodep -I${CMAKE_CURRENT_SOURCE_DIR}/../lib/utils 
           -I${CMAKE_CURRENT_SOURCE_DIR}/../lib/utils/nemodep
           -outdir ${CMAKE_CURRENT_BINARY_DIR}
           -o ${CMAKE_CURRENT_BINARY_DIR}/py_unstools_wrap.cxx 
           ${CMAKE_CURRENT_SOURCE_DIR}/py_unstools.i 
  VERBATIM
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/py_unstools.i
)

python_add_library(
  _py_unstools
  MODULE
  WITH_SOABI
  ${CMAKE_CURRENT_BINARY_DIR}/py_unstools_wrap.cxx
)

target_include_directories(_py_unstools PUBLIC  ${NUMPY_INCLUDE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/../src ${CMAKE_CURRENT_SOURCE_DIR}/../lib/projects 
  ${CMAKE_CURRENT_SOURCE_DIR}/../lib/projects/nemodep ${CMAKE_CURRENT_SOURCE_DIR}/../lib/utils 
  ${CMAKE_CURRENT_SOURCE_DIR}/../lib/utils/nemodep $ENV{NEMO}/usr/dehnen/falcON/inc 
  $ENV{NEMO}/usr/dehnen/falcON/inc/utils $ENV{NEMO}/inc)

# 
if (APPLE)
    set_target_properties(_py_unstools PROPERTIES INSTALL_RPATH "@loader_path")
else()
    set_target_properties(_py_unstools PROPERTIES INSTALL_RPATH "$ORIGIN")
endif()
target_link_libraries(_py_unstools PUBLIC JCLutils JCLprojects)

install(TARGETS _py_unstools DESTINATION unsiotools)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/py_unstools.py DESTINATION unsiotools)

