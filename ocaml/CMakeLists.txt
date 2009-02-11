OCAML_ADD_LIBRARY(OCaml_SimpleSetup
  SimpleSetup.cpp
  simpleSetup.ml
)

OCAML_LINK_LIBRARIES(OCaml_SimpleSetup
  Extensions_SetupHelpers
)
