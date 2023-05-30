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

log = fpcore.parse("(FPCore (x) (log x))")
domain = Interval(fpcore.parse_expr("(/ (sqrt 2) 2)"),
                  fpcore.parse_expr("(sqrt 2)"))

x_to_f_remap = fpcore.parse("(FPCore (x) (- x 1))")
f_log = fpcore.parse("(FPCore (f) (log (+ f 1)))")
f_log_sub_f = fpcore.parse("(FPCore (f) (- (log (+ f 1)) f))")
f_domain = Interval(fpcore.parse_expr("(- (/ (sqrt 2) 2) 1)"),
                    fpcore.parse_expr("(- (sqrt 2) 1)"))

f_to_s_remap = fpcore.parse("(FPCore (f) (/ f (+ 2 f)))")
s_log = fpcore.parse("(FPCore (s) (- (log (+ 1 s)) (log (- 1 s))))")
s_log_sub_two_s = fpcore.parse(
    "(FPCore (s) (- (- (log (+ 1 s)) (log (- 1 s))) (* 2 s)))")
s_domain = Interval(
    fpcore.parse_expr("(/ (- (/ (sqrt 2) 2) 1) (+ 2 (- (/ (sqrt 2) 2) 1)))"),
    fpcore.parse_expr("(/ (- (sqrt 2) 1) (+ 2 (- (sqrt 2) 1)))"))

zero_point = Interval(0, 0)
zero_polynomial = Horner(FixedPolynomial(f_log, zero_point, [0], [0]))

mac_domain = Interval(-9.5367431640625e-7,
                      9.536743161842053950749686919152736663818359375e-7)
mac_polynomial = \
    Add(fpcore.parse_expr("f"),
        Horner(
            FixedPolynomial(f_log_sub_f,
                            mac_domain,
                            [2, 3],
                            ["-0.5", "0.3333333333333333"])))

extra_domain = Interval(0.3799991607666015625,
                        f_domain.sup)

f_polynomial = \
    Recharacterize(
        f_log,
        f_to_s_remap,
        Rewrite(
            fpcore.parse_expr("(* 2 s)"),
            fpcore.parse_expr("(fma (- s) f f)"),
            Add(fpcore.parse_expr("(* 2 s)"),
                Horner(
                FixedMultiPolynomial(
                    s_log_sub_two_s,
                    s_domain,
                    fpcore.parse(
                        "(FPCore (x p q) (* x (+ p q)))"),
                    [4, 8, 12],
                    ["3.999999999940941908e-01",
                     "2.222219843214978396e-01",
                     "1.531383769920937332e-01",],
                    [2, 6, 10, 14],
                    ["6.666666666666735130e-01",
                     "2.857142874366239149e-01",
                     "1.818357216161805012e-01",
                     "1.479819860511658591e-01"])))))

reference_impl = "sun_log.c"
lambda_expression = \
    Multiplicative(
        Recharacterize(
            log,
            x_to_f_remap,
            SplitDomain({
                zero_point: zero_polynomial,
                mac_domain: mac_polynomial,
                extra_domain: f_polynomial,
                f_domain: f_polynomial,
            })))


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
dsl_func_name = "dsl_sun_log"
dsl_sig, dsl_src = lambdas.generate_c_code(lambda_expression, dsl_func_name)
logger.blog("C function", "\n".join(dsl_src))

# amd
libm_func_name = "libm_dsl_sun_log"
libm_sig = "double libm_dsl_sun_log(double x);"
with open(path.join(GIT_DIR, "examples", "sun_log.c"), "r") as f:
    text = f.read()
    text = text.replace("sun_log", "libm_dsl_sun_log")
    libm_src = [line.rstrip() for line in text.splitlines()]

# oracle
func = fpcore.parse("(FPCore (x) (log x))")
domain = Interval(-1, 1)
target = lambdas.types.Impl(func, domain)
mpfr_func_name = "mpfr_dsl_sun_log"
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

domains = [("0", "10"),
           ("7.999969482421875", "8.000030517578125"),
           ("5.4", "5.8"),
           ("2.772588", "5.545177")]
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
