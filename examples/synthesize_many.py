#!/usr/bin/env python3

import os
import os.path as path
import sys
import time

EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)


import fpcore
import lambdas
import numeric_types
import cmd_sollya

from synthesize import synthesize
from assemble_c_files import *
from interval import Interval
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.QUIET)
logger.set_log_level(Logger.HIGH)




def generate_all_code(function, domain, name):
    target = lambdas.types.Impl(function, domain)

    my_lambdas = synthesize(target)

    libm_funcname = f"libm_{name}"
    libm_sig, libm_src = lambdas.generate_libm_c_code(target, libm_funcname)
    logger.blog("C libm function", "\n".join(libm_src))

    mpfr_funcname = f"mpfr_{name}"
    mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(target, mpfr_funcname)
    logger.blog("C mpfr function", "\n".join(mpfr_src))

    gen_sigs = list()
    gen_srcs = list()
    gen_funcnames = list()
    for i,lam in enumerate(my_lambdas):
        try:
            funcname = f"my_{name}_{i}"
            sig, src = lambdas.generate_c_code(lam, funcname)
            logger.blog("C function", "\n".join(src))
            gen_sigs.append(sig)
            gen_srcs.append(src)
            gen_funcnames.append(funcname)
        except cmd_sollya.FailedGenError:
            logger("Unable to generate polynomial, skipping")

    header_lines = assemble_header([libm_sig, mpfr_sig] + gen_sigs)
    header_fname = f"{name}.h"
    with open(header_fname, "w") as f:
        f.write("\n".join(header_lines))

    func_lines = assemble_functions([libm_src, mpfr_src] + gen_srcs, header_fname)
    func_fname = f"{name}.c"
    with open(func_fname, "w") as f:
        f.write("\n".join(func_lines))

    fstr = str(function)
    if any(f in fstr for f in {"sin", "cos", "tan"}):
        domains = [("-M_PI/4", "M_PI/4"),
                   ("-M_PI", "M_PI"),
                   ("-10*M_PI", "10*M_PI"),
                   ("-100*M_PI", "100*M_PI"),]
    elif float(domain.inf) == 0:
        domains = [("0.0", "0.175"),
                   ("0.0", "0.7"),
                   ("0.0", "7"),
                   ("0.0", "70"),]
    else:
        domains = [("-0.1", "0.1"),
                   ("-1", "1"),
                   ("-10", "10"),
                   ("-100", "100"),]

    main_lines = assemble_error_main(mpfr_funcname,
                                     [libm_funcname] + gen_funcnames,
                                     header_fname, domains)
    main_fname = f"main_{name}.c"
    with open(main_fname, "w") as f:
        f.write("\n".join(main_lines))


def main(argv):
    name = argv[1]
    func = argv[2]
    low = argv[3]
    high = argv[4]
    logger("Func: {}", func)
    logger("Name: {}", name)
    logger("Low: {}", low)
    logger("High: {}", high)
    fpc = fpcore.parse(func)
    domain = Interval(low, high)
    generate_all_code(fpc, domain, name)

if __name__ == "__main__":
    main(sys.argv)
