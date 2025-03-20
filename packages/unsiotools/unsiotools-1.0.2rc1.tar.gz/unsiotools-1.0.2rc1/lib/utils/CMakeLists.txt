# ============================================================================

cmake_minimum_required(VERSION 3.15)
 
# project name
project (lib_utils)

# contains the full path to the top level directory of your build tree
MESSAGE( STATUS "PROJECT_BINARY_DIR: " ${PROJECT_BINARY_DIR} )

# contains the full path to the root of your project source directory,
MESSAGE( STATUS "PROJECT_SOURCE_DIR: " ${PROJECT_SOURCE_DIR} )

# Find all the sources for the utils LIB
if ( NEMO_INSTALLED )
   FILE(GLOB LIBUTILS ${PROJECT_SOURCE_DIR}/*.cc ${PROJECT_SOURCE_DIR}/*.c ${PROJECT_SOURCE_DIR}/nemodep/*.cc)
else ()
   FILE(GLOB LIBUTILS ${PROJECT_SOURCE_DIR}/*.cc ${PROJECT_SOURCE_DIR}/*.c)
endif ()

# create the library "JCLutils"
add_library (JCLutils SHARED ${LIBUTILS})
target_link_libraries(JCLutils nemo unsio cpgplot pgplot X11 gfortran quadmath WDutils falcON) # WDutils falcON gomp c++)
if(OSX)   
   set_target_properties(JCLutils PROPERTIES LINK_FLAGS "-undefined suppress -flat_namespace")
endif(OSX)

if (APPLE)
  if (NOT NO_RPATH)
     MESSAGE(STATUS "RPATH activated for JCLutils library")
     SET_TARGET_PROPERTIES(JCLutils PROPERTIES MACOSX_RPATH TRUE)
  else ()
     # to deactivate RPATH compile with -DNO_RPATH=1
     # it's mandatory to build wheel on MacOSX
     MESSAGE(STATUS "RPATH not-activated for JCLutils library")
  endif()

endif (APPLE)
# install target
if (SKBUILD_PROJECT_NAME)
    INSTALL(FILES  ${PROJECT_BINARY_DIR}/lib/libJCLutils.${SOEXT} DESTINATION unsiotools)
else()
    INSTALL(FILES  ${PROJECT_BINARY_DIR}/lib/libJCLutils.${SOEXT} DESTINATION ${PREFIX_LIB})
    INSTALL(FILES  ${PROJECT_SOURCE_DIR}/nemodep/cfalcon.h DESTINATION inc/uns)
    INSTALL(FILES  ${PROJECT_SOURCE_DIR}/csnaptools.h DESTINATION inc/uns)
    INSTALL(FILES  ${PROJECT_SOURCE_DIR}/ctimer.h DESTINATION inc/uns)
endif()

