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

from assemble_c_files import assemble_error_main, assemble_functions, assemble_header
from interval import Interval
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)


function = fpcore.parse("(FPCore (x) (exp x))")[0]
domain = Interval("0.0", "(log 2)")
monomials = [0, 1, 2, 3]

poly = lambdas.FullPolynomial(function, domain, monomials, list())
logger(poly)
logger("  Type: {}", poly.out_type)

horner = lambdas.Horner(poly)
logger(horner)
logger("  Type: {}", horner.out_type)

my_exp = lambdas.RepeatExp(horner)
logger(my_exp)
logger("  Type: {}", my_exp.out_type)

gen_sig, gen_src = lambdas.generate_c_code(my_exp, "my_exp")
logger(gen_sig)

gen_src = ["#include <math.h>", "#include <assert.h>\n\n"] + gen_src

logger.blog("C function", "\n".join(gen_src))

type = lambdas.types.Impl(function, domain)

libm_funcname = f"libm_exp"
libm_sig, libm_src = lambdas.generate_libm_c_code(type, libm_funcname)

mpfr_funcname = f"oracle_exp"
mpfr_sig, mpfr_src = lambdas.generate_mpfr_c_code(type, mpfr_funcname)

start = os.getcwd()
if not path.isdir("generated_exp"):
    os.mkdir("generated_exp")
os.chdir("generated_exp")

header_lines = assemble_header([libm_sig, mpfr_sig, gen_sig])
with open("funcs.h", "w") as f:
    f.write("\n".join(header_lines))

func_lines = assemble_functions([libm_src, mpfr_src, gen_src], "funcs.h")
with open("funcs.c", "w") as f:
    f.write("\n".join(func_lines))

domains = [("-1.4", "2.1"),
           ("0", "0.69")]

main_lines = assemble_error_main("exp", function.to_html(),
                                 "oracle_exp",
                                 ["libm_exp", "my_exp"],
                                 "funcs.h", domains)
with open("main.c", "w") as f:
    f.write("\n".join(main_lines))
