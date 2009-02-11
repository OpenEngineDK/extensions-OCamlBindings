// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!! WARNING: This is unsafe code !!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

extern "C" {
#include <pthread.h>
#include <caml/mlvalues.h>
#include <caml/memory.h>
#include <caml/alloc.h>
#include <caml/custom.h>
}

#include <Utils/SimpleSetup.h>
#include <string>

using namespace OpenEngine;

extern "C" {

// Helper to get the C++ pointer out of an OCaml wrapper
#define SimpleSetup_val(v) (*((Utils::SimpleSetup **) Data_custom_val(v)))

    static struct custom_operations simple_setup_ops = {
        (char*)"oe.simple_setup",
        custom_finalize_default,
        custom_compare_default,
        custom_hash_default,
        custom_serialize_default,
        custom_deserialize_default
    };

    // Allocate a OCaml wrapper for a simple setup
    static value alloc_window(Utils::SimpleSetup* s) {
        value v = alloc_custom(&simple_setup_ops, sizeof(Utils::SimpleSetup *), 0, 1);
        SimpleSetup_val(v) = s;
        return v;
    }

    // Thread identifier
    pthread_t t;

    // Create a new simple setup (unsafe if you create two)
    CAMLprim value
    ocaml_simple_setup_create(value name) {
        Utils::SimpleSetup* s = new Utils::SimpleSetup(std::string(String_val(name)));
        return alloc_window(s);
    }

    // Start simple setup (threaded)
    void* _ocaml_simple_setup_start (void* s) {
        ((Utils::SimpleSetup*)s)->GetEngine().Start();
        pthread_exit(NULL);
    }
    CAMLprim value
    ocaml_simple_setup_start(value setup) {
        pthread_create(&t, NULL, _ocaml_simple_setup_start, SimpleSetup_val(setup));
        return Val_unit;
    }

    // Stop simple setup (potentially unsafe)
    CAMLprim value
    ocaml_simple_setup_stop(value setup) {
        SimpleSetup_val(setup)->GetEngine().Stop();
        return Val_unit;
    }

}
