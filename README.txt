Author: OpenEngine Team

Get the latest version with:
  darcs get http://openengine.dk/code/extensions/OCamlBindings

This is an exploratory extension to integrate OCaml with OpenEngine.
The extension provides a series of new CMake macros to configure
OCaml. An example CMakeLists.txt file could look like this:

{{{
# Create an executable with our OCaml file.
# This creates a machine code executable 'demo.opt' and a byte-code
# executable 'demo.byte' that is linked with the OCaml run-time.
OCAML_ADD_EXECUTABLE(demo demo.ml)

# Create a top-level out of the executable.
# This will create both 'demo.top' and 'demo.py'.
# To start the top-level run the demo.py script.
OCAML_MAKE_TOPLEVEL(demo)

# Link to other OE OCaml modules
OCAML_LINK_LIBRARIES(demo OCaml_SimpleSetup)
}}}
