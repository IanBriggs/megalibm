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
logger.set_log_level(Logger.QUIET)
#logger.set_log_level(Logger.HIGH)



function = fpcore.parse("(FPCore (x) (- 1 (cos x)))")
domain = Interval("(- PI)", "PI")
monomials = list(range(2,26,2))

p = lambdas.Polynomial(function, domain, monomials, list())
logger(p)
logger("  Type: {}", p.out_type)

g = lambdas.Horner(p)
logger(g)
logger("  Type: {}", g.out_type)

n = lambdas.Narrow(g, Interval("0.0", "PI"))
logger(n)
logger("  Type: {}", n.out_type)

rf = lambdas.RepeatFlip(n)
logger(rf)
logger("  Type: {}", rf.out_type)

ri = lambdas.RepeatInf(rf)
logger(ri)
logger("  Type: {}", ri.out_type)

my_versin = lambdas.MirrorAboutZeroX(ri)
logger(my_versin)
logger("  Type: {}", my_versin.out_type)

sig, src = lambdas.generate_c_code(my_versin, "my_versin")
logger(sig)

print("\n".join(src))

src = ["#include <math.h>", "#include <assert.h>\n\n"] + src
logger.blog("C function", "\n".join(src))
