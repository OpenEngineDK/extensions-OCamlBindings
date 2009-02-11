#!/usr/bin/env python
# -------------------------------------------------------------------
# Wrapper for compiling ocaml programs.
# -------------------------------------------------------------------
# Copyright (C) 2007 OpenEngine.dk (See AUTHORS) 
# 
# This program is free software; It is covered by the GNU General 
# Public License version 2 or any later version. 
# See the GNU General Public License for more details (see LICENSE). 
#--------------------------------------------------------------------

import string, sys, subprocess, os, os.path as path

# reuse the helpers from repo.py
#from dist import printCommands, error, execute, system, ExecError, cores

class ExecError(Exception):
    "Exception thrown if execute(cmd) exited with error code != 0"

def execute(cmd):
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    if proc.returncode != 0:
        raise ExecError("%s exited with error code %i\n"
                        % (cmd, proc.returncode))

def error(err):
    print err
    sys.exit(1)

def relpath(path):
    return path.replace(os.getcwd(), "")

def abspath(p):
    return path.join(os.getcwd(), p)

class OCaml:

    def __init__(self):
        self.output = None
        self.mktop  = False
        self.thread = False

        # C options, libraries and files
        self.ccopt  = []
        self.cclib  = []

        # OCaml options, libraries and files
        self.ocinc  = []
        self.oclib  = []
        
        # Unknown arguments
        self.unknown = []

        # List denoted by last flag
        self.optlst = self.unknown

    def parse(self, lst):
        if len(lst) == 0: return
        x = lst.pop()
        newoptlst = self.unknown

        if x == "-I":
            newoptlst = self.ocinc

        elif x == "-o":
            self.output = lst.pop()

        elif x == "--mktop":
            self.mktop = True

        elif x == "-thread":
            self.thread = True

        elif x.startswith("-L"):
            self.ccopt.append(x)

        elif x.endswith(".so") \
          or x.endswith(".a")  \
          or x.startswith("-l"):
            self.cclib.append(x)

        elif x.endswith(".o"):
            self.cclib.append(abspath(x))

        elif x.endswith(".cmxa") or x.endswith(".cmx") \
          or x.endswith(".cma")  or x.endswith(".cmo") \
          or x.endswith(".ml")   or x.endswith(".mli"):
            self.oclib.append(x)

        #elif self.optlst == self.unknown:
        #    print "Warning: unknown argument: ", x

        else:
            self.optlst.append(x)
            newoptlst = self.optlst

        # reset optlst and continue parsing
        self.optlst = newoptlst
        self.parse(lst)
        

    def run(self):
    
        # parse input
        cmd = sys.argv[1]
        input = list(sys.argv[2:])
        input.reverse()
        self.parse(input)

        comps = ["ocamlopt", "ocamlc"]
        if self.mktop: comps.append("ocamlmktop")
        out  = self.output
        flag = ""

        if cmd in ("exe", "lib"):
            execute("touch %s" % out)

        if cmd == "exe":
            pass #comps = map(lambda s: s+" -custom", comps)
        if cmd == "obj":
            flag = "-c"
        if cmd == "lib":
            out += ".cma"
            flag = "-a"

        bin_ext = {"ocamlopt":".opt", "ocamlc":".byte", "ocamlmktop":".top"}

        for comp in comps:
            lib = ext(comp)(".cma")
            c_out = out + (cmd == "exe" and bin_ext[comp] or "")
            c_flag = flag + (comp != "ocamlopt" and " -custom" or "")
            exe = ("%s %s %s -o %s %s %s %s %s %s" % 
               (comp, c_flag,
                self.thread and " -thread unix%s threads%s" % (lib, lib) or "",
                ext(comp)(c_out),
                " ".join(map(lambda s: "-ccopt %s" % s, self.ccopt)),
                " ".join(map(lambda s: "-cclib %s" % s, self.cclib)),
                " ".join(map(lambda s: "-I %s" % s, self.ocinc)),
                # add the unknowns as OCaml archives (need to fix this...)
                " ".join(map(lambda s: s+lib, self.unknown)),
                " ".join(map(ext(comp), self.oclib)),
                ))
            execute(exe)

        if self.mktop:
            p = out+".py"
            f = open(p,"w")
            try:
                f.write(
"""#!/usr/bin/env python
# This is an auto-generated file to start a custom OCaml toplevel
# with include directories known at compile time.
import subprocess, sys, os
cmd = "%s.top %s"
try:
  if subprocess.call(["rlwrap", "-v"], stdout=subprocess.PIPE) == 0:
    cmd = "rlwrap " + cmd
except OSError:
  pass
proc = subprocess.Popen(cmd, shell=True)
while proc.poll() is None:
  try:
    proc.wait()
  except KeyboardInterrupt:
    pass
sys.exit(proc.returncode)
""" % (abspath(out),
       " ".join(map(lambda s: "-I %s" % s, self.ocinc))))
                os.chmod(p, 0755)
            finally:
                f.close()

def byte_ext(s):
    return s.replace(".cmxa", ".cma").replace(".cmx", ".cmo")
def opt_ext(s):
    return s.replace(".cma", ".cmxa").replace(".cmo", ".cmx")
def ext(c):
    return (c == "ocamlopt") and opt_ext or byte_ext

if __name__ == '__main__':
    try:
        OCaml().run()
    except ExecError, e:
        print e
        sys.exit(1)
