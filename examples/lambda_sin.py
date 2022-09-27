#!/usr/bin/env python3

import os
import os.path as path
import sys
import time

EXAMPLE_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(EXAMPLE_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
sys.path.append(SRC_DIR)


import fpcore
import lambdas
import numeric_types

from interval import Interval
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)
logger.set_log_level(Logger.HIGH)




function = fpcore.parse("(FPCore (x) (sin x))")[0]
domain = Interval("0.0", "(/ PI 2)")
monomials = [0, 1, 3]

p = lambdas.OddPolynomial(function, domain, monomials, list())
logger(p)
logger("  Type: {}", p.out_type)

g = lambdas.Horner(p)
logger(g)
logger("  Type: {}", g.out_type)

rf = lambdas.RepeatFlip(g)
logger(rf)
logger("  Type: {}", rf.out_type)

rn = lambdas.RepeatNegate(rf)
logger(rn)
logger("  Type: {}", rn.out_type)

ri = lambdas.RepeatInf(rn)
logger(ri)
logger("  Type: {}", ri.out_type)

my_sin = lambdas.FlipAboutZeroX(ri)
logger(my_sin)
logger("  Type: {}", my_sin.out_type)

sig, src = lambdas.generate_c_code(my_sin, "my_sin")
logger(sig)

src = ["#include <math.h>", "#include <assert.h>\n\n"] + src
logger.blog("C function", "\n".join(src))
