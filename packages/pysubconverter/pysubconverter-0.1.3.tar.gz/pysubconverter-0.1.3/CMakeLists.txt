cmake_minimum_required(VERSION 3.25)
message(STATUS "CMAKE VERSION:${CMAKE_VERSION}")

project(
  pysubconverter
  LANGUAGES CXX C
  HOMEPAGE_URL "https://github.com/msclock/pysubconverter"
  DESCRIPTION "A wrapper from subconverter")

# Project default module
find_package(cmake-modules REQUIRED)
include(cmake-modules/ProjectDefault)
include(ConfigureVersion)

add_subdirectory(src)
