#!/usr/bin/env python3
#
# Eventually input should look like this:
#  * we might want to wrap it as an FPCore and highjack the fpcore parser
#
# (InflectionLeft
#   (- x)
#   (- y)
#   (SplitDomain
#     [(Interval 0 1.38777878078144552145514e-17)
#        (HornerForm
#          (Polynomial
#            (asin x)
#            (Interval 0 1.38777878078144552145514e-17)
#            [1]
#            [1]))]
#     [(Interval 1.38777878078144552145514e-17 1)
#         (InflectionRight
#           (sqrt (/ (- 1 x) 2))
#           (- (/ PI 2) (* 2 y))
#           (EstrinForm
#             (Polynomial
#               (asin x)
#               (Interval 0 0.5)
#               [1 3 5 7 9 11 13 15 17 19 21 23 25]
#               [ 1
#                 0.1666666666666477004
#                 0.07500000000417969548
#                 0.04464285678140855751
#                 0.03038196065035564039
#                 0.0223717279703189581
#                 0.01736009463784134871
#                 0.01388184285963460496
#                 0.01218919111033679899
#                 0.00644940526689945226
#                 0.01972588778568478904
#                -0.01651175205874840998
#                 0.03209627299824770186]))))

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

asin = fpcore.parse("(FPCore (x) (asin x))")[0]
# This is the value that corresponds to AMD's code
linear_cutoff = "1.38777878078144552145514403413465714614676459320581451695186814276894438080489635467529296875e-17"

mlm = \
    InflectionLeft(
        SplitDomain({
            Interval("0", linear_cutoff):
            Horner(
                FixedPolynomial(
                    asin,
                    Interval("0", linear_cutoff),
                    1,
                    [1],
                    [1]
                )),
            Interval(linear_cutoff, "1"):
            InflectionRight(
                Estrin(
                    FixedPolynomial(
                        asin,
                        Interval("0", "0.5"),
                        13,
                        [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
                        [1,
                         0.1666666666666477004,
                         0.07500000000417969548,
                         0.04464285678140855751,
                         0.03038196065035564039,
                         0.0223717279703189581,
                         0.01736009463784134871,
                         0.01388184285963460496,
                         0.01218919111033679899,
                         0.00644940526689945226,
                         0.01972588778568478904,
                         -0.01651175205874840998,
                         0.03209627299824770186, ]),
                         split=1),
                fpcore.parse("(FPCore (x) (sqrt (/ (- 1 x) 2)))")[0].body,
                fpcore.parse("(FPCore (x) (- (/ PI 2) (* 2 y)))")[0].body)}),
        fpcore.parse("(FPCore (x) (- x))")[0].body,
        fpcore.parse("(FPCore (x) (- y))")[0].body)

better_linear_cutoff = "2.14910850667675e-08"
better_mlm = \
    InflectionLeft(
        SplitDomain({
            Interval("0", better_linear_cutoff):
            Horner(
                FixedPolynomial(
                    asin,
                    Interval("0", better_linear_cutoff),
                    1,
                    [1],
                    [1]
                )),
            Interval(better_linear_cutoff, "1"):
            InflectionRight(
                    Estrin(
                        MinimaxPolynomial(
                            asin,
                            Interval("0", "0.5"),
                            15),
                        split=1),
                fpcore.parse("(FPCore (x) (sqrt (/ (- 1 x) 2)))")[0].body,
                fpcore.parse("(FPCore (x) (- (/ PI 2) (* 2 y)))")[0].body)}),
        fpcore.parse("(FPCore (x) (- x))")[0].body,
        fpcore.parse("(FPCore (x) (- y))")[0].body)

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
dsl_func_name = "dsl_amd_fast_asin"
dsl_sig, dsl_src = lambdas.generate_c_code(mlm, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# better
better_mlm.type_check()
better_dsl_func_name = "better_dsl_amd_fast_asin"
better_dsl_sig, better_dsl_src = lambdas.generate_c_code(better_mlm, better_dsl_func_name)
logger.blog("C function", "\n".join(better_dsl_src))

# amd
libm_func_name = "libm_dsl_amd_fast_asin"
libm_sig = "double libm_dsl_amd_fast_asin(double x);"
with open(path.join(GIT_DIR, "examples", "amd_fast_asin.c"), "r") as f:
    text = f.read()
    text = text.replace("amd_fast_asin", "libm_dsl_amd_fast_asin")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (asin x))")[0]
domain = Interval(-1, 1)
target = lambdas.types.Impl(func, domain)
mpfr_func_name = "mpfr_dsl_amd_fast_asin"
mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(target, mpfr_func_name)

# output directory
name = dsl_func_name
start = os.getcwd()
if not path.isdir(name):
    os.mkdir(name)
os.chdir(name)

# header
header_lines = assemble_header([libm_sig, mpfr_sig, dsl_sig, better_dsl_sig])
header_fname = "funcs.h"
with open(header_fname, "w") as f:
    f.write("\n".join(header_lines))

# all 3 functions
func_lines = assemble_functions([libm_src, mpfr_src + dsl_src + better_dsl_src], header_fname)
func_fname = "funcs.c"
with open(func_fname, "w") as f:
    f.write("\n".join(func_lines))

domains = [("-1", "1"),
           ("0", "0.5"),
           ("0", float(linear_cutoff) + 3e-8),
           ("0.4375", "0.5625"),]
func_body = func.to_html()
generators = [str(mlm)]

# Error measurement
main_lines = assemble_error_main(name, func_body,
                                 mpfr_func_name,
                                 [libm_func_name, dsl_func_name, better_dsl_func_name],
                                 generators,
                                 header_fname, domains)
main_fname = "error_main.c"
with open(main_fname, "w") as f:
    f.write("\n".join(main_lines))

# Timing measurement
main_lines = assemble_timing_main(name, func_body,
                                  [libm_func_name, dsl_func_name, better_dsl_func_name],
                                  header_fname, domains)
main_fname = "timing_main.c"
with open(main_fname, "w") as f:
    f.write("\n".join(main_lines))

# |                                                                           |
# +---------------------------------------------------------------------------+
