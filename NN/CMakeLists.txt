########################################################
# cmake file for building Marlin example Package
# @author Jan Engels, Desy IT
CMAKE_MINIMUM_REQUIRED(VERSION 2.6 FATAL_ERROR)
########################################################

# project name
PROJECT( NNpolya )

# project version
SET( ${PROJECT_NAME}_VERSION_MAJOR 0 )
SET( ${PROJECT_NAME}_VERSION_MINOR 1 )
SET( ${PROJECT_NAME}_VERSION_PATCH 0 )

### DEPENDENCIES ############################################################

FIND_PACKAGE( ILCUTIL REQUIRED COMPONENTS ILCSOFT_CMAKE_MODULES )

# load default settings from ILCSOFT_CMAKE_MODULES
INCLUDE( ilcsoft_default_settings )


FIND_PACKAGE( ROOT REQUIRED COMPONENTS TMVA) # minimum required Marlin version
INCLUDE_DIRECTORIES( ${ROOT_INCLUDE_DIRS} )
LINK_LIBRARIES( ${ROOT_LIBRARIES} )
ADD_DEFINITIONS( ${ROOT_DEFINITIONS} )


### DOCUMENTATION ###########################################################

OPTION( INSTALL_DOC "Set to OFF to skip build/install Documentation" OFF )

IF( INSTALL_DOC AND EXISTS "${PROJECT_SOURCE_DIR}/doc/CMakeLists.txt" )
    ADD_SUBDIRECTORY( ./doc )
ENDIF()

### LIBRARY #################################################################

# definitions to pass to the compiler
ADD_DEFINITIONS( "-Wall -ansi -pedantic -std=c++11" )
ADD_DEFINITIONS( "-Wno-long-long" )

# include directories
INCLUDE_DIRECTORIES( ./include )

# display some variables and write them to cache
DISPLAY_STD_VARIABLES()

SET (Reg ./src/TMVARegression.cxx)
SET (RegApp ./src/TMVARegressionApplication.cxx)

#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "../bin/")

ADD_EXECUTABLE(TMVARegression ${Reg} )
ADD_EXECUTABLE(TMVARegressionApplication ${RegApp} )

TARGET_LINK_LIBRARIES(TMVARegression ${ROOT_COMPONENT_LIBRARIES})
TARGET_LINK_LIBRARIES(TMVARegressionApplication ${ROOT_COMPONENT_LIBRARIES})

INSTALL( TARGETS TMVARegression TMVARegressionApplication RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}/bin )
