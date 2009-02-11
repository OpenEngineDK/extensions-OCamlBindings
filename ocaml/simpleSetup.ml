
type t
external create : string -> t = "ocaml_simple_setup_create"
external start : t -> unit = "ocaml_simple_setup_start"

external stop : t -> unit = "ocaml_simple_setup_stop"

