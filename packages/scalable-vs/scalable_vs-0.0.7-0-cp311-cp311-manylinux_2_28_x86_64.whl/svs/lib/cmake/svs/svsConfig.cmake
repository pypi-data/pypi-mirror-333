# Copyright (C) 2023 Intel Corporation
#
# This software and the related documents are Intel copyrighted materials,
# and your use of them is governed by the express license under which they
# were provided to you ("License"). Unless the License provides otherwise,
# you may not use, modify, copy, publish, distribute, disclose or transmit
# this software or the related documents without Intel's prior written
# permission.
#
# This software and the related documents are provided as is, with no
# express or implied warranties, other than those that are expressly stated
# in the License.


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was ConfigLeanVec.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

# Flags for optional dependencies
set(SVS_EXPERIMENTAL_ENABLE_NUMA OFF)

# Use a custom find module for transitive dependencies
set(SVS_ORIGINAL_CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH})
list(INSERT CMAKE_MODULE_PATH 0 ${PACKAGE_PREFIX_DIR}/lib/cmake/svs)

# Find the necessary dependencies
include(CMakeFindDependencyMacro)
set(THREADS_PREFER_PTHREAD_FLAG TRUE)
find_dependency(Threads REQUIRED)
find_dependency(tsl-robin-map REQUIRED)
find_dependency(eve REQUIRED)
find_dependency(tomlplusplus REQUIRED)
find_dependency(fmt REQUIRED)
find_dependency(spdlog REQUIRED)

# # Dependencies that could be optional at build time.
if(SVS_EXPERIMENTAL_ENABLE_NUMA)
    find_dependency(Numa REQUIRED)
endif()

find_dependency(MKL REQUIRED)
set(MKL_THREADING sequential)

# Revert the CMAKE_MODULE_PATH to its original state
set(CMAKE_MODULE_PATH ${SVS_ORIGINAL_CMAKE_MODULE_PATH})

include("${CMAKE_CURRENT_LIST_DIR}/svs-targets.cmake")
check_required_components(svs)
