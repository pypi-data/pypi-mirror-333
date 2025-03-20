# ============================================================================

cmake_minimum_required(VERSION 3.15)
 
# project name
project (mains)

# contains the full path to the top level directory of your build tree
MESSAGE( STATUS "PROJECT_BINARY_DIR: " ${PROJECT_BINARY_DIR} )

# contains the full path to the root of your project source directory,
MESSAGE( STATUS "PROJECT_SOURCE_DIR: " ${PROJECT_SOURCE_DIR} )

# Find all exes sources files
if ( NEMO_INSTALLED )
   FILE(GLOB execpp_sources *.cc nemodep/*.cc)
else ()
   FILE(GLOB execpp_sources *.cc)
endif ()
# build cpp executables according to the source
if (NEMO_INSTALLED)
  set (LINK_NEMO "-lnemo")
else ()
    set (LINK_NEMO "")
endif()

FOREACH(exe_cpp ${execpp_sources})

    # add executables
    get_filename_component(exe_name ${exe_cpp} NAME_WE)
    MESSAGE( STATUS "New executable ==> " ${exe_name})
    add_executable (${exe_name} ${exe_cpp})

    # TARGET links
    if ( NEMO_INSTALLED )
        # with fits
        # target_link_libraries (${exe} JCLprojects JCLutils cpgplot pgplot.a ${FC_GFORT_LIB} ${FC_G77_LIB}  CCfits cfitsio X11 nemo unsio WDutils falcON gomp ${LIBBOOST} pthread dl)
        # without fits
        #target_link_libraries (${exe_name} JCLprojects JCLutils cpgplot pgplot ${FC_GFORT_LIB} ${FC_G77_LIB} X11 ${LINK_NEMO} unsio WDutils falcON gomp quadmath ${LIBBOOST} ${RPC_NAME_LIB} pthread dl)
        target_link_libraries (${exe_name} JCLprojects JCLutils)
    else ()
        # with fits
        # target_link_libraries (${exe} JCLprojects JCLutils ${FC_GFORT_LIB} ${FC_G77_LIB} CCfits cfitsio nemo unsio gomp ${LIBBOOST} dl)
        # without fits
        target_link_libraries (${exe_name} JCLprojects JCLutils)
    endif ()

    # INSTALL TARGETS
    if (NOT SKBUILD_PROJECT_NAME)
        if (APPLE)
            SET_TARGET_PROPERTIES(${exe_name} PROPERTIES MACOSX_RPATH TRUE)
            set_target_properties(${exe_name} PROPERTIES INSTALL_RPATH "@loader_path/../${LIB_SUFFIX}")#;${DEHNEN}/falcON/lib;${DEHNEN}/utils/lib")
        else()
            set_target_properties(${exe_name} PROPERTIES INSTALL_RPATH "$ORIGIN/../${LIB_SUFFIX}")
        endif()
        install(TARGETS ${exe_name} RUNTIME DESTINATION bin)
    endif()

ENDFOREACH(exe_cpp ${execpp_sources})

