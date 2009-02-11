# Determine the compiler to use for OCaml programs.
# Quick hack based on CMakeDetermineCCompiler.cmake

# The environment variable OCAML_COMPILER may be used to specify the
# desired compiler.

# Sets the following variables:
#  CMAKE_OCaml_COMPILER

IF(NOT CMAKE_OCaml_COMPILER)

  # Prefer the environment variable OCaml_COMPILER
  IF($ENV{OCAML_COMPILER} MATCHES ".+")
    GET_FILENAME_COMPONENT(CMAKE_OCaml_COMPILER_INIT $ENV{OCAML_COMPILER}
			   PROGRAM PROGRAM_ARGS CMAKE_OCaml_FLAGS_ENV_INIT)
    IF(CMAKE_OCaml_FLAGS_ENV_INIT)
      SET(CMAKE_OCaml_COMPILER_ARG1 "${CMAKE_OCaml_FLAGS_ENV_INIT}" CACHE STRING "First argument to OCaml compiler")
    ENDIF(CMAKE_OCaml_FLAGS_ENV_INIT)
    IF(NOT EXISTS ${CMAKE_OCaml_COMPILER_INIT})
      MESSAGE(FATAL_ERROR "Could not find compiler set in environment variable OCaml_COMPILER:\n$ENV{OCaml_COMPILER}.") 
    ENDIF(NOT EXISTS ${CMAKE_OCaml_COMPILER_INIT})
  ENDIF($ENV{OCAML_COMPILER} MATCHES ".+")

  # Compilers list
  IF(CMAKE_OCaml_COMPILER_INIT)
    SET(CMAKE_OCaml_COMPILER_LIST ${CMAKE_OCaml_COMPILER_INIT})
  ELSE(CMAKE_OCaml_COMPILER_INIT)
    SET(CMAKE_OCaml_COMPILER_LIST "ocamlc ocamlopt")
  ENDIF(CMAKE_OCaml_COMPILER_INIT)

  # The usual paths
  SET(OCaml_BIN_PATHS
    /usr/bin
    /usr/local/bin
    # windows path (please check more wrt. windows as this is not tested)
    "c:\\Program Files\\Objective Caml\\"
    )

  # Find the compiler.
  FIND_PROGRAM(CMAKE_OCaml_COMPILER
    NAMES ${CMAKE_OCaml_COMPILER_LIST}
    PATHS ${OCaml_BIN_PATHS}
    DOC "OCaml Compiler"
    )

  IF(CMAKE_OCaml_COMPILER_INIT AND NOT CMAKE_OCaml_COMPILER)
    SET(CMAKE_OCaml_COMPILER "${CMAKE_OCaml_COMPILER_INIT}" CACHE FILEPATH "OCaml Compiler" FORCE)
  ENDIF(CMAKE_OCaml_COMPILER_INIT AND NOT CMAKE_OCaml_COMPILER)

ENDIF(NOT CMAKE_OCaml_COMPILER)

# configure variables set in this file for fast reload later on
FIND_FILE(CMAKE_OCaml_COMPILER_TEMPLATE "CMakeOCamlCompiler.cmake.in"
  PATHS ${CMAKE_ROOT}/Modules ${CMAKE_MODULE_PATH}
  )
CONFIGURE_FILE(${CMAKE_OCaml_COMPILER_TEMPLATE}
  "${CMAKE_PLATFORM_ROOT_BIN}/CMakeOCamlCompiler.cmake"
  @ONLY IMMEDIATE # IMMEDIATE must be here for compatibility mode <= 2.0
  )

SET(CMAKE_OCaml_COMPILER_ENV_VAR "OCAML_COMPILER")
