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

asin = fpcore.parse("(FPCore (x) (asin x))")
linear_cutoff = "1.38777878078144552146e-17"




reference_impl = "amd_ref_asin.c"
lambda_expression = \
    InflectionLeft(
        InflectionRight(
            Horner(
                FixedMultiPolynomial(
                    asin,
                    Interval("0", "0.5"),
                    fpcore.parse("(FPCore (x p q) (+ x (/ p q)))"),
                    [1, 2, 3, 4, 5, 6],
                    [" 0.227485835556935010735943483075",
                     "-0.445017216867635649900123110649",
                     " 0.275558175256937652532686256258",
                     "-0.0549989809235685841612020091328",
                     " 0.00109242697235074662306043804220",
                     " 0.0000482901920344786991880522822991"],
                    [0, 1, 2, 3, 4],
                    [" 1.36491501334161032038194214209",
                     "-3.28431505720958658909889444194",
                     " 2.76568859157270989520376345954",
                     "-0.943639137032492685763471240072",
                     " 0.105869422087204370341222318533"]), useDD = True, split_expr=fpcore.parse_expr("(* x x)")),
            [ExprIfLess(None, fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"), "double-double", compute="dd"),
             ExprIfLess(fpcore.parse_expr("(* x x)"), fpcore.parse_expr("(/ (- 1 x) 2)"), "double")],
            [ExprIfLess(None, fpcore.parse_expr("(- (/ PI 2) (* 2 y))"), "double", compute="dd")], useDD=True),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))

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
#TODO
lambda_expression.type_check()
dsl_func_name = "dsl_amd_ref_asin"
dsl_sig, dsl_src = lambdas.generate_c_code(lambda_expression, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_amd_ref_asin"
libm_sig = "double libm_dsl_amd_ref_asin(double x);"
with open(path.join(GIT_DIR, "examples", "amd_ref_asin.c"), "r") as f:
    text = f.read()
    text = text.replace("amd_ref_asin", "libm_dsl_amd_ref_asin")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (asin x))")
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
generators = [str(lambda_expression)]

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
