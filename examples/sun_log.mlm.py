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
from assemble_c_files import *
from interval import Interval
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)

# +---------------------------------------------------------------------------+
# | Should be handled by a new parser                                         |
# |                                                                           |

log = fpcore.parse("(FPCore (x) (log x))")
domain = Interval(fpcore.parse_expr("(/ (sqrt 2) 2)"),
                  fpcore.parse_expr("(sqrt 2)"))

x_to_f_remap = fpcore.parse("(FPCore (x) (- x 1))")
f_log = fpcore.parse("(FPCore (f) (log (+ f 1)))")
f_domain = Interval(fpcore.parse_expr("(- (/ (sqrt 2) 2) 1)"),
                    fpcore.parse_expr("(- (sqrt 2) 1)"))

f_to_s_remap = fpcore.parse("(FPCore (f) (/ f (+ 2 f)))")
s_log = fpcore.parse("(FPCore (s) (- (log (+ 1 s)) (log (- 1 s))))")
s_domain = Interval(
    fpcore.parse_expr("(/ (- (/ (sqrt 2) 2) 1) (+ 2 (- (/ (sqrt 2) 2) 1)))"),
    fpcore.parse_expr("(/ (- (sqrt 2) 1) (+ 2 (- (sqrt 2) 1)))"))

zero_point = Interval(0, 0)

mac_domain = Interval(-9.5367431640625e-7,
                      9.536743161842053950749686919152736663818359375e-7)

mlm = \
    Multiplicative(
        Recharacterize(
            log,
            x_to_f_remap,
            SplitDomain({
                zero_point:
                Horner(FixedPolynomial(f_log, zero_point, [0], [0])),
                mac_domain:
                Horner(
                    FixedPolynomial(f_log, mac_domain,
                                    [1, 2, 3],
                                    [1, -1 / 2, 1 / 3]),
                                    split=1),
                f_domain:
                Recharacterize(
                    f_log,
                    f_to_s_remap,
                    Horner(
                        FixedMultiPolynomial(
                            s_log,
                            s_domain,
                            fpcore.parse(
                                "(FPCore (x p q) (+ (* 2 x) (* x (+ p q))))"),
                            [4, 8, 12],
                            ["3.999999999940941908e-01",
                             "2.222219843214978396e-01",
                             "1.531383769920937332e-01",],
                            [2, 6, 10, 14],
                            ["6.666666666666735130e-01",
                             "2.857142874366239149e-01",
                             "1.818357216161805012e-01",
                             "1.479819860511658591e-01"]),
                        split=0))})))


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
dsl_func_name = "dsl_sun_log"
dsl_sig, dsl_src = lambdas.generate_c_code(mlm, dsl_func_name)
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
           ("1", "1.1716"),
           ("0", "1"),
           ("1.1716", "5")]
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
