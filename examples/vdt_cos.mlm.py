#!/usr/bin/env python3
#
# Eventually input should look like this:
#  * we might want to wrap it as an FPCore and highjack the fpcore parser
#


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

cos = fpcore.parse("(FPCore (x) (cos x))")[0]
sin = fpcore.parse("(FPCore (x) (sin x))")[0]

cos_poly = \
    Horner(
        FixedPolynomial(
            cos,
            Interval("(- (+ (/ PI 4) 3.24128e-11))",
                     "(+ (/ PI 4) 3.24128e-11)"),
            8,
            [0, 2, 4, 6, 8, 10, 12, 14],
            ["1",
             "-0.5",
             "4.16666666666665929218E-2",
             "-1.38888888888730564116E-3",
             "2.48015872888517045348E-5",
             "-2.75573141792967388112E-7",
             "2.08757008419747316778E-9",
             "-1.13585365213876817300E-11"]),
        split=2)

sin_poly = \
    Horner(
        FixedPolynomial(
            sin,
            Interval("(- (+ (/ PI 4) 3.24128e-11))",
                     "(+ (/ PI 4) 3.24128e-11)"),
            7,
            [1, 3, 5, 7, 9, 11, 13],
            ["1",
             "-1.66666666666666307295E-1",
             "8.33333333332211858878E-3",
             "-1.98412698295895385996E-4",
             "2.75573136213857245213E-6",
             "-2.50507477628578072866E-8",
             "1.58962301576546568060E-10"]),
        split=1)


pi_over_4 = fpcore.parse("(FPCore (y) (/ PI 4))")[0].body
pi_over_2 = fpcore.parse("(FPCore (y) (/ PI 2))")[0].body

negate_x = fpcore.parse("(FPCore (x) (- x))")[0].body
negate_y = fpcore.parse("(FPCore (y) (- y))")[0].body
id_y = fpcore.parse("(FPCore (y) y)")[0].body

periodic_cases = {
    0: cos_poly,
    1: TransformOut(in_node=sin_poly, expr=negate_y),
    2: TransformOut(in_node=cos_poly, expr=negate_y),
    3: sin_poly,
}

mlm = \
    InflectionLeft(
        CodyWaite(cos,
                  pi_over_2,
                  periodic_cases,
                  53 - 30,
                  2),
        negate_x,
        id_y)

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
dsl_func_name = "dsl_vdt_cos"
dsl_sig, dsl_src = lambdas.generate_c_code(mlm, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_vdt_cos"
libm_sig = "double libm_dsl_vdt_cos(double x);"
with open(path.join(GIT_DIR, "examples", "vdt_cos.c"), "r") as f:
    text = f.read()
    text = text.replace("vdt_cos", "libm_dsl_vdt_cos")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (cos x))")[0]
domain = Interval(-1, 1)
target = lambdas.types.Impl(func, domain)
mpfr_func_name = "mpfr_dsl_vdt_cos"
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
           ("0", "3"),
           ("0", "32"),
           ("-0.75", "0.75")]
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
