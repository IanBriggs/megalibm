#!/usr/bin/env python3
#
# Eventually input should look like this:
#  * we might want to wrap it as an FPCore and highjack the fpcore parser
#
# (InflectionLeft
#   (- x)
#   (- y)
#   (InflectionRight
#     (sqrt (\ (- 1 x) 2))
#     (- (\ PI 2) 2 y)
#     (Horner
#       (RationalPolynomial
#         (asin x)
#         (Interval 0 0.5)
#         x
#         [3 5 7 9 11 13]
#         [ 0.227485835556935010735943483075
#          -0.445017216867635649900123110649
#           0.275558175256937652532686256258
#          -0.0549989809235685841612020091328
#           0.00109242697235074662306043804220
#           0.0000482901920344786991880522822991]
#         [2 4 6 8 10]
#         [ 1.36491501334161032038194214209
#          -3.28431505720958658909889444194
#           2.76568859157270989520376345954
#          -0.943639137032492685763471240072
#           0.105869422087204370341222318533]))))


import os
import os.path as path
import sys


EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)

import fpcore
import lambdas

from lambdas import InflectionLeft, InflectionRight, Horner, FixedRationalPolynomial, SplitDomain
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
linear_cutoff = " 1.38777878078144552145514403413465714614676459320581451695186814276894438080489635467529296875e-17"
# A much better value is
# linear_cutoff = " 2.14910850667674987607097081103446623018271566252224147319793701171875e-8"

mlm = \
    InflectionLeft(
        InflectionRight(
            Horner(
                FixedRationalPolynomial(
                    asin,
                    Interval("0", "0.5"),
                    fpcore.parse("(FPCore (x) x)")[0].body,
                    [3, 5, 7, 9, 11, 13],
                    [ 0.227485835556935010735943483075,
                     -0.445017216867635649900123110649,
                      0.275558175256937652532686256258,
                     -0.0549989809235685841612020091328,
                      0.00109242697235074662306043804220,
                      0.0000482901920344786991880522822991],
                    [0, 2, 4, 6, 8],
                    [ 1.36491501334161032038194214209,
                     -3.28431505720958658909889444194,
                      2.76568859157270989520376345954,
                     -0.943639137032492685763471240072,
                      0.105869422087204370341222318533])),
            fpcore.parse("(FPCore (x) (sqrt (/ (- 1 x) 2)))")[0].body,
            fpcore.parse("(FPCore (x) (- (/ PI 2) (* 2 y)))")[0].body),
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
dsl_func_name = "dsl_amd_ref_asin"
dsl_sig, dsl_src = lambdas.generate_c_code(mlm, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_amd_ref_asin"
libm_sig = "double libm_dsl_amd_ref_asin(double x);"
with open(path.join(GIT_DIR, "examples", "amd_ref_asin.c"), "r") as f:
    text = f.read()
    text = text.replace("amd_ref_asin", "libm_dsl_amd_ref_asin")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (asin x))")[0]
domain = Interval(-1, 1)
target = lambdas.types.Impl(func, domain)
mpfr_func_name = "mpfr_dsl_amd_ref_asin"
mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(target, mpfr_func_name)

# output directory
name = dsl_func_name
start = os.getcwd()
if not path.isdir(name):
    os.mkdir(name)
os.chdir(name)

# header
header_lines = assemble_header([libm_sig, mpfr_sig, dsl_sig])
header_fname = "funcs.h"
with open(header_fname, "w") as f:
    f.write("\n".join(header_lines))

# all 3 functions
func_lines = assemble_functions([libm_src, mpfr_src + dsl_src], header_fname)
func_fname = "funcs.c"
with open(func_fname, "w") as f:
    f.write("\n".join(func_lines))

domains = [("-1", "1"),
           ("0", "1"),
           (float(linear_cutoff) - 1e-8, float(linear_cutoff) + 1e-8),
           ("0.4375", "0.5625"),]
func_body = func.to_html()
generators = [str(mlm)]

# Error measurement
main_lines = assemble_error_main(name, func_body,
                                 mpfr_func_name,
                                 [libm_func_name, dsl_func_name],
                                 generators,
                                 header_fname, domains)
main_fname = "error_main.c"
with open(main_fname, "w") as f:
    f.write("\n".join(main_lines))

# Timing measurement
main_lines = assemble_timing_main(name, func_body,
                                  [libm_func_name, dsl_func_name],
                                  header_fname, domains)
main_fname = "timing_main.c"
with open(main_fname, "w") as f:
    f.write("\n".join(main_lines))

# |                                                                           |
# +---------------------------------------------------------------------------+
