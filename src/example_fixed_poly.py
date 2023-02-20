

import os
import os.path as path
import sys
from utils.logging import Logger
import fpcore
from interval import Interval
import lambdas
from assemble_c_files import assemble_functions, assemble_header


EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)



logger = Logger(color=Logger.cyan, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)


function = fpcore.parse("(FPCore (x) (sin x))")[0]
domain = Interval("0.0", "(/ PI 2)")
monomials = [1, 3, 5, 7, 9]
coefficients = [1, -0.1666, 0.008333, -0.00019841269, 0.00000275573]
terms = 5

poly = lambdas.FixedPolynomial(function, domain, terms, monomials, coefficients, symmetry=1)
poly.type_check()
logger(poly)
logger("  Type: {}", poly.out_type)


horner = lambdas.Horner(poly)
logger(horner)
# logger("  Type: {}", horner.out_type)

gen_poly, gen_src = lambdas.generate_c_code(horner, "sin")
start = os.getcwd()
if not path.isdir("generated_poly"):
    os.mkdir("generated_poly")
os.chdir("generated_poly")

func_lines = assemble_functions([gen_src], "funcs.h")
with open("funcs.c", "w") as f:
    f.write("\n".join(func_lines))