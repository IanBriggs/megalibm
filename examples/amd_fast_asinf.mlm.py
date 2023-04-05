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
#     (- (\ PI 2) (* 2 y))
#     (EstrinForm
#       (Polynomial
#         (asin x)
#         (Interval 0 0.5)
#         [1 3 5 7 9 11]
#         [ 1
#           0.1666679084300994873
#           0.07494434714317321777
#           0.04555018618702888489
#           0.02385816909372806549
#           0.04263564199209213257]))))

import os
import os.path as path
import sys


EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)

import fpcore
import lambdas


from lambdas import InflectionLeft, InflectionRight, Horner, FixedPolynomial, Estrin
from numeric_types import fp32
from assemble_c_files import assemble_timing_main, assemble_error_main, assemble_functions, assemble_header
from interval import Interval
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)

# +---------------------------------------------------------------------------+
# | Should be handled by a new parser                                         |
# |


asin = fpcore.parse("(FPCore (x) (asin x))")[0]

mlm = \
    InflectionLeft(
        InflectionRight(
            Estrin(
                FixedPolynomial(
                    asin,
                    Interval("0", "0.5"),
                    6,
                    [1, 3, 5, 7, 9, 11],
                    [ "1.0f",
                      "0.1666679084300994873f",
                      "0.07494434714317321777f",
                      "0.04555018618702888489f",
                      "0.02385816909372806549f",
                      "0.04263564199209213257f"]), split=1),
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
dsl_func_name = "dsl_amd_fast_asinf"
dsl_sig, dsl_src = lambdas.generate_c_code(mlm, dsl_func_name, numeric_type=fp32)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_amd_fast_asinf"
libm_sig = "double libm_dsl_amd_fast_asinf(double x);"
with open(path.join(GIT_DIR, "examples", "amd_fast_asinf.c"), "r") as f:
    text = f.read()
    text = text.replace("amd_fast_asinf", "libm_dsl_amd_fast_asinf")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (asin x))")[0]
domain = Interval(-1, 1)
target = lambdas.types.Impl(func, domain)
mpfr_func_name = "mpfr_dsl_amd_fast_asinf"
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
           ("0", "0.5"),
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
