

import snake_egg
import snake_egg_rules as ops

import fractions

from utils import Logger

logger = Logger(level=Logger.HIGH)


lambdas = {
    ops.neg: lambda x: -x,

    ops.add: lambda x, y: x + y,
    ops.sub: lambda x, y: x - y,
    ops.mul: lambda x, y: x * y,
    ops.div: lambda x, y: x / y,
}

REPORTED = set()


def eval(op, args):
    global REPORTED
    if type(op) in {int, float, str, fractions.Fraction}:
        try:
            f = fractions.Fraction(op)
            if f.denominator != 1:
                return None
            if f.numerator < 0:
                logger("Negative literal: {}", f.numerator)
            return int(f.numerator)
        except ValueError as e:
            if op not in REPORTED:
                logger("Treating as variable: '{}'", op)
                REPORTED.add(op)
            return None

    if op in lambdas:
        res = lambdas[op](*args)
        if type(res) != int:
            return None
        if res < 0:
            return None
        return int(res)

    return None
