#!/usr/bin/env python3
#
# Eventually input should look like this:
#  * we might want to wrap it as an FPCore and highjack the fpcore parser
#
# (InflectionLeft
#   (- x)
#   (- y)
#   (SplitDomain
#      [(Interval 1 1)
#        (Horner (Polynomial (asin x)
#          (Interval 1 1) [0] [PI_2])]
#      [(Interval 0  7.450580596923828125e-9)
#        (Horner (Polynomial (asin x)
#          (Interval 0 7.450580596923828125e-9) [1] [1])]
#      [(Interval 7.450580596923828125e-9 1.0)
#         (InflectionRight
#           (sqrt (/ (- 1 x) 2))
#           (- (/ PI 2) (* 2 y))
#           (Horner (RationalPolynomial (asin x)
#              (Interval 0 0.5)
#              x
#              [3 5 7 9 11 13]
#              [ 1.66666666666666657415e-01
#               -3.25565818622400915405e-01
#                2.01212532134862925881e-01
#               -4.00555345006794114027e-02
#                7.91534994289814532176e-04
#                3.47933107596021167570e-05]
#              [0 2 4 6 8]
#              [ 1
#               -2.40339491173441421878e+00
#                2.02094576023350569471e+00
#               -6.88283971605453293030e-01
#                7.70381505559019352791e-02]))]))


import os
import os.path as path
import sys


EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)

import fpcore
import lambdas

from lambdas import InflectionLeft, InflectionRight, Horner, FixedRationalPolynomial, SplitDomain, FixedPolynomial
from assemble_c_files import assemble_timing_main, assemble_error_main, assemble_functions, assemble_header
from interval import Interval
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)

# +---------------------------------------------------------------------------+
# | Should be handled by a new parser                                         |
# |                                                                           |

asin = fpcore.parse("(FPCore (x) (asin x))")[0]

one_i = Interval("1", "1")
linear_cutoff = "7.450580596923828125e-9"
linear_i = Interval("0", linear_cutoff)
HPI = fpcore.parse("(FPCore () PI_2)")[0].body

mlm = \
    InflectionLeft(
        SplitDomain({
            one_i: Horner(FixedPolynomial(asin, one_i, 1, [0], [HPI])),
            linear_i: Horner(FixedPolynomial(asin, linear_i, 1, [1], [1])),
            Interval(linear_cutoff, "1"):
                InflectionRight(
                    Horner(
                        FixedRationalPolynomial(
                            asin,
                            Interval("0", "0.5"),
                            fpcore.parse("(FPCore (x) x)")[0].body,
                            [3, 5, 7, 9, 11, 13],
                            [ 1.66666666666666657415e-01,
                             -3.25565818622400915405e-01,
                              2.01212532134862925881e-01,
                             -4.00555345006794114027e-02,
                              7.91534994289814532176e-04,
                              3.47933107596021167570e-05],
                            [0, 2, 4, 6, 8],
                            [ 1,
                             -2.40339491173441421878e+00,
                              2.02094576023350569471e+00,
                             -6.88283971605453293030e-01,
                              7.70381505559019352791e-02])),
                    fpcore.parse("(FPCore (x) (sqrt (/ (- 1 x) 2)))")[0].body,
                    fpcore.parse("(FPCore (x) (- (/ PI 2) (* 2 y)))")[0].body),
        }),
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
dsl_func_name = "dsl_sun_asin"
dsl_sig, dsl_src = lambdas.generate_c_code(mlm, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_sun_asin"
libm_sig = "double libm_dsl_sun_asin(double x);"
with open(path.join(GIT_DIR, "examples", "sun_asin.c"), "r") as f:
    text = f.read()
    text = text.replace("sun_asin", "libm_dsl_sun_asin")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (asin x))")[0]
domain = Interval(-1, 1)
target = lambdas.types.Impl(func, domain)
mpfr_func_name = "mpfr_dsl_sun_asin"
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
