#!/usr/bin/env python3

import os
import os.path as path
import sys

EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)

import fpcore
import lambdas

from lambdas import *
from assemble_c_files import assemble_timing_main, assemble_error_main, assemble_functions, assemble_header
from interval import Interval
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)

# +---------------------------------------------------------------------------+
# | Should be handled by a new parser                                         |
# |                                                                           |

exp = fpcore.parse("(FPCore (x) (exp x))")

exp_poly = \
    Horner(
        FixedMultiPolynomial(
            exp,
            Interval("0",
                     "(log 2)"),
            fpcore.parse("(FPCore (x p q) (+ 1 (* 2 (/ p (- q p)))))"),
            [1, 3, 5],
            ["9.99999999999999999910E-1",
             "3.02994407707441961300E-2",
             "1.26177193074810590878E-4"],
            [0, 2, 4, 6],
            ["2.00000000000000000009E0",
             "2.27265548208155028766E-1",
             "2.52448340349684104192E-3",
             "3.00198505138664455042E-6"]),
        split=0)

mlm = \
    RepeatExp(exp_poly, 18, 1)



# |                                                                           |
# +---------------------------------------------------------------------------+

# +---------------------------------------------------------------------------+
# | Should be handled by a new runscript                                      |
# |                                                                           |

# Setup generated directory
start = os.getcwd()
if not path.isdir("generated"):
    os.mkdir("generated")
os.chdir("generated")

# dsl
mlm.type_check()
dsl_func_name = "dsl_vdt_exp"
dsl_sig, dsl_src = lambdas.generate_c_code(mlm, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_vdt_exp"
libm_sig = "double libm_dsl_vdt_exp(double x);"
with open(path.join(GIT_DIR, "examples", "vdt_exp.c"), "r") as f:
    text = f.read()
    text = text.replace("vdt_exp", "libm_dsl_vdt_exp")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (exp x))")
domain = Interval(-1, 1)
target = lambdas.types.Impl(func, domain)
mpfr_func_name = "mpfr_dsl_vdt_exp"
mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(target, mpfr_func_name)

# output directory
name = dsl_func_name
start = os.getcwd()
if not path.isdir(name):
    os.mkdir(name)
os.chdir(name)

# header
header_lines = assemble_header(
    [libm_sig, mpfr_sig, dsl_sig])
header_fname = "funcs.h"
with open(header_fname, "w") as f:
    f.write("\n".join(header_lines))

# all 3 functions
func_lines = assemble_functions(
    [libm_src, mpfr_src + dsl_src], header_fname)
func_fname = "funcs.c"
with open(func_fname, "w") as f:
    f.write("\n".join(func_lines))

domains = [("-7", "7"),
           ("0", "0.75"),
           ("0", "32"),
           ("-32", "0")]
func_body = func.to_html()
generators = [str(mlm)]

# Error measurement
main_lines = assemble_error_main(name, func_body,
                                 mpfr_func_name,
                                 [libm_func_name, dsl_func_name,
                                  ],
                                 generators,
                                 header_fname, domains)
main_fname = "error_main.c"
with open(main_fname, "w") as f:
    f.write("\n".join(main_lines))

# Timing measurement
main_lines = assemble_timing_main(name, func_body,
                                  [libm_func_name, dsl_func_name,
                                   ],
                                  header_fname, domains)
main_fname = "timing_main.c"
with open(main_fname, "w") as f:
    f.write("\n".join(main_lines))

# |                                                                           |
# +---------------------------------------------------------------------------+
