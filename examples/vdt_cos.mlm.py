#!/usr/bin/env python3

import os
import os.path as path
import sys

EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)

from assemble_c_files import *
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)

# +---------------------------------------------------------------------------+
# | Should be handled by a new parser                                         |
# |                                                                           |

import fpcore
import lambdas

from interval import Interval
from lambdas import *

cos = fpcore.parse("(FPCore (x) (cos x))")
sin = fpcore.parse("(FPCore (x) (sin x))")

pi_over_4 = fpcore.parse_expr("(/ PI 4)")
pi_over_2 = fpcore.parse_expr("(/ PI 2)")

neg_pi_over_4 = - pi_over_4

negate_x = fpcore.parse_expr("(- x)")
negate_y = fpcore.parse_expr("(- y)")
id_y = fpcore.parse_expr("y")

cos_poly = \
    Add(
        fpcore.parse_expr("(- 1 (* (* x x) 0.5))"),
        Add(
            fpcore.parse_expr("1"),
            Horner(
                FixedPolynomial(
                    fpcore.parse("(FPCore (x) (- (+ (cos x) (/ (* x x) 2)) 1))"),
                    Interval(neg_pi_over_4,
                             pi_over_4),
                    [4, 6, 8, 10, 12, 14],
                    ["4.16666666666665929218E-2",
                     "-1.38888888888730564116E-3",
                     "2.48015872888517045348E-5",
                     "-2.75573141792967388112E-7",
                     "2.08757008419747316778E-9",
                     "-1.13585365213876817300E-11"]))))

sin_poly = \
    Horner(
        FixedPolynomial(
            sin,
            Interval(neg_pi_over_4,
                     pi_over_4),
            [1, 3, 5, 7, 9, 11, 13],
            ["1",
             "-1.66666666666666307295E-1",
             "8.33333333332211858878E-3",
             "-1.98412698295895385996E-4",
             "2.75573136213857245213E-6",
             "-2.50507477628578072866E-8",
             "1.58962301576546568060E-10"]),
        split=1)

periodic_cases = {
    0: cos_poly,
    1: TransformOut(in_node=sin_poly, expr=negate_y),
    2: TransformOut(in_node=cos_poly, expr=negate_y),
    3: sin_poly,
}

reference_impl = "vdt_cos.c"
lambda_expression = \
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
lambda_expression.type_check()
dsl_func_name = "dsl_vdt_cos"
dsl_sig, dsl_src = lambdas.generate_c_code(lambda_expression, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_vdt_cos"
libm_sig = "double libm_dsl_vdt_cos(double x);"
with open(path.join(GIT_DIR, "examples", "vdt_cos.c"), "r") as f:
    text = f.read()
    text = text.replace("vdt_cos", "libm_dsl_vdt_cos")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (cos x))")
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
generators = [str(lambda_expression)]

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
