# -*-cmake-*-
# ============================================================================
# Copyright Jean-Charles LAMBERT - 2008-2025
# e-mail:   Jean-Charles.Lambert@lam.fr
# address:  Dynamique des galaxies
#           Centre de donneeS Astrophysique de Marseille (CeSAM)
#           Laboratoire d'Astrophysique de Marseille
#           Pole de l'Etoile, site de Chateau-Gombert
#           38, rue Frederic Joliot-Curie
#           13388 Marseille cedex 13 France
#           CNRS U.M.R 7326
# ============================================================================
# Detect OS and architecture to select right CPACK Generator
# ============================================================================
#
# Inspired from :
# http://www.cmake.org/pipermail/cmake/2010-July/038268.html
# http://www.cmake.org/pipermail/cmake/attachments/20100722/04976a73/attachment-0001.obj
#



# define a set of string with may-be useful readable name
# this file is meant to be included in a CMakeLists.txt
# not as a standalone CMake script
set(SPECIFIC_COMPILER_NAME "")
set(SPECIFIC_SYSTEM_VERSION_NAME "")
set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "")
set(LINUX_NAME "")
set(MY_OS "")

if (OSX)
  set(LIB_SUFFIX "lib")
endif (OSX)

if(UNIX)
  if(CMAKE_SYSTEM_NAME MATCHES "Linux")
    set(SPECIFIC_SYSTEM_VERSION_NAME "${CMAKE_SYSTEM_NAME}")
    set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "TGZ")
    set(LINUX_NAME "")
    set(LINUX_ISSUE "")
    set(LIB_SUFFIX "lib64")

    if(EXISTS "/etc/system-release")
      file(READ "/etc/system-release" LINUX_ISSUE)
      elseif (EXISTS "/etc/issue")
	file(READ "/etc/issue" LINUX_ISSUE)
      elseif (EXISTS "/etc/redhat-release")
	file(READ "/etc/redhat-release" LINUX_ISSUE)
    endif(EXISTS "/etc/system-release")      

      # Mageia case
      if(LINUX_ISSUE MATCHES "Mageia")
	set(MY_OS "Mageia")
        string(REGEX MATCH "release ([0-9]+)" MAGEIA "${LINUX_ISSUE}")
        set(LINUX_NAME "mga${CMAKE_MATCH_1}")  
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "RPM")      
	MESSAGE (STATUS "Mageia :" ${LINUX_NAME})
      endif(LINUX_ISSUE MATCHES "Mageia")
      # Arch Linux
      if(LINUX_ISSUE MATCHES "Arch")
        set(MY_OS "Arch")
        set(LINUX_NAME "arch")  
        #set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "RPM")      
        MESSAGE (STATUS "Arch Linux :" ${LINUX_NAME})
      endif(LINUX_ISSUE MATCHES "Arch")
      # Fedora case
      if(LINUX_ISSUE MATCHES "Fedora")
	set(MY_OS "Fedora")
        string(REGEX MATCH "release ([0-9]+)" FEDORA "${LINUX_ISSUE}")
        set(LINUX_NAME "fc${CMAKE_MATCH_1}")  
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "RPM")      
      endif(LINUX_ISSUE MATCHES "Fedora")
      # Scientific case
      if(LINUX_ISSUE MATCHES "Scientific")
        set(MY_OS "Scientific")
        string(REGEX MATCH "release ([0-9]+)" SCIENTIFIC "${LINUX_ISSUE}")
        set(LINUX_NAME "el${CMAKE_MATCH_1}")
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "RPM")
      endif(LINUX_ISSUE MATCHES "Scientific")
      if(LINUX_ISSUE MATCHES "CentOS")
        set(MY_OS "CentOS")
        string(REGEX MATCH "release ([0-9]+)" CENTOS "${LINUX_ISSUE}")
        set(LINUX_NAME "el${CMAKE_MATCH_1}")
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "RPM")
      endif(LINUX_ISSUE MATCHES "CentOS")
      # Ubuntu case
      if(LINUX_ISSUE MATCHES "Ubuntu")
        set (CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON) 
	set(MY_OS "Ubuntu")
        string(REGEX MATCH "buntu ([0-9]+\\.[0-9]+)" UBUNTU "${LINUX_ISSUE}")
        set(LINUX_NAME "ubuntu${CMAKE_MATCH_1}")        
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "DEB")
        set(LIB_SUFFIX "lib/x86_64-linux-gnu")
      endif(LINUX_ISSUE MATCHES "Ubuntu")
      # Mint case
      if(LINUX_ISSUE MATCHES "Mint")
        set (CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
        set(MY_OS "Mint")
        string(REGEX MATCH "Mint ([0-9]+\\.[0-9]+)" MINT "${LINUX_ISSUE}")
        set(LINUX_NAME "mint${CMAKE_MATCH_1}")
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "DEB")
        set(LIB_SUFFIX "lib/x86_64-linux-gnu")
      endif(LINUX_ISSUE MATCHES "Mint")
      # Debian case
      if(LINUX_ISSUE MATCHES "Debian")
        set (CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON) 
        string(REGEX MATCH "Debian .*ux ([a-zA-Z]*/?[a-zA-Z]*) .*" DEBIAN "${LINUX_ISSUE}")
        set(LINUX_NAME "debian-${CMAKE_MATCH_1}")
        string(REPLACE "/" "_" LINUX_NAME ${LINUX_NAME}) 
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "DEB")       
        set(LIB_SUFFIX "lib/x86_64-linux-gnu")
      endif(LINUX_ISSUE MATCHES "Debian")      
      # Open SuSE case
      if(LINUX_ISSUE MATCHES "SUSE")
	set(MY_OS "Suse")
        string(REGEX MATCH "SUSE ([a-zA-Z]*/?[a-zA-Z]*) ([0-9]+\\.[0-9]+)" SUSE "${LINUX_ISSUE}")
        if (NOT ${CMAKE_MATCH_2} STREQUAL "")
           set(LINUX_NAME "opensuse${CMAKE_MATCH_2}")
        else()
           set(LINUX_NAME "opensuse${CMAKE_MATCH_1}")
        endif()
        string(REPLACE "/" "_" LINUX_NAME ${LINUX_NAME})   
        set(SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR "RPM")     
      endif(LINUX_ISSUE MATCHES "SUSE")
      # Mandriva case
      # TODO      
      if(LINUX_NAME) 
         set(SPECIFIC_SYSTEM_VERSION_NAME "${CMAKE_SYSTEM_NAME}-${LINUX_NAME}")
      endif(LINUX_NAME)    
  endif(CMAKE_SYSTEM_NAME MATCHES "Linux")
  set(SPECIFIC_SYSTEM_VERSION_NAME "${SPECIFIC_SYSTEM_VERSION_NAME}-${CMAKE_SYSTEM_PROCESSOR}")
  set(SPECIFIC_COMPILER_NAME "")
endif(UNIX)

if    (NOT SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR STREQUAL "" )
  set(CPACK_GENERATOR ${SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR} )
endif (NOT SPECIFIC_SYSTEM_PREFERED_CPACK_GENERATOR STREQUAL "" )

if    (NOT MY_OS STREQUAL "" )
  message(STATUS "---- Detect CPACK ----")
  message(STATUS "Linux distribution :" ${MY_OS})
  message(STATUS "OS version         :" ${LINUX_NAME})
  message(STATUS "Generator          :" ${CPACK_GENERATOR})
endif (NOT MY_OS STREQUAL "" )


