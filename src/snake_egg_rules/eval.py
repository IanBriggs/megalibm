

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

def eval(op, args):
    if type(op) in {int, float, str, fractions.Fraction}:
        try:
            f = fractions.Fraction(op)
            if f.denominator == 1:
                return int(f.numerator)
            return None
        except ValueError as e:
            logger("Treating as variable: '{}'", op)
            return None

    if op in lambdas:
        res = lambdas[op](*args)
        if type(res) == int:
            return res
        return None

    return None
