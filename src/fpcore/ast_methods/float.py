

from fpcore.ast import ASTNode, Constant, Variable, Number, Operation, FPCore
from utils import add_method, Logger

import math


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def __float__(self, *args, **kwargs):
    # Make sure calling __float__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = "__float__ not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Constant)
def __float__(self):
    mapping = {
        "E": math.e,
        "LOG2E": math.log2(math.e),
        "LOG10E": math.log10(math.e),
        "LN2": math.log(2),
        "LN10": math.log(10),
        "PI": math.pi,
        "PI_2": math.pi/2,
        "PI_4": math.pi/4,
        "M_1_PI": 1/math.pi,
        "M_2_PI": 2/math.pi,
        "M_2_SQRTPI": 2/math.sqrt(math.pi),
        "SQRT2": math.sqrt(2),
        "SQRT1_2": 1/math.sqrt(2),
        "INFINITY": math.inf,
    }
    return mapping[self.source]


@add_method(Variable)
def __float__(self):
    msg = "can not convert Variable to float: '{}'".format(repr(self))
    raise ValueError(msg)


@add_method(Number)
def __float__(self):
    return float(self.source)


@add_method(Operation)
def __float__(self):
    f_args = [float(arg) for arg in self.args]

    if len(f_args) == 1:
        mapping = {
            "-": (lambda x: -x)
        }
        return mapping[self.op](f_args[0])

    if len(f_args) == 2:
        mapping = {
            "+": (lambda x, y: x+y),
            "-": (lambda x, y: x-y),
            "*": (lambda x, y: x*y),
            "/": (lambda x, y: x/y),
        }
        return mapping[self.op](f_args[0], f_args[1])

    msg = "Operation not yet supported for __float__: '{}'".format(repr(self))
    raise NotImplementedError(msg)


@add_method(FPCore)
def __float__(self):
    return float(self.body)
