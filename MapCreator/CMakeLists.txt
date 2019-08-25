########################################################
# cmake file for building Marlin example Package
# @author Jan Engels, Desy IT
CMAKE_MINIMUM_REQUIRED(VERSION 2.6 FATAL_ERROR)
########################################################

# project name
PROJECT( MapCreatorForPolya )

### DEPENDENCIES ############################################################

FIND_PACKAGE( ILCUTIL REQUIRED COMPONENTS ILCSOFT_CMAKE_MODULES )

# load default settings from ILCSOFT_CMAKE_MODULES
INCLUDE( ilcsoft_default_settings )

FIND_PACKAGE( ROOT REQUIRED COMPONENTS ) # minimum required Marlin version
INCLUDE_DIRECTORIES( ${ROOT_INCLUDE_DIRS} )
LINK_LIBRARIES( ${ROOT_LIBRARIES} )
ADD_DEFINITIONS( ${ROOT_DEFINITIONS} )

### LIBRARY #################################################################

# definitions to pass to the compiler
ADD_DEFINITIONS( "-Wall -ansi -pedantic -std=c++11" )
ADD_DEFINITIONS( "-Wno-long-long" )

#include directories
INCLUDE_DIRECTORIES( ./include )

#add library
AUX_SOURCE_DIRECTORY( ./src library_sources )

# display some variables and write them to cache
DISPLAY_STD_VARIABLES()

SET (createMap ./createMap.cxx)


#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "../bin/")

ADD_EXECUTABLE( createMap ${createMap} ${headers} ${sources} )


TARGET_LINK_LIBRARIES( createMap ${ROOT_COMPONENT_LIBRARIES} )


INSTALL(TARGETS createMap RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}/bin)
