

from fpcore.ast import ASTNode, Constant, Variable, Number, Operation, FPCore
from utils import add_method, Logger

import mpmath

mpmath.prec = 1024

logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def eval(self, *args, **kwargs):
    # Make sure calling eval leads to an error if not overridden
    class_name = type(self).__name__
    msg = "eval not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Constant)
def eval(self, assignment):
    mapping = {
        "E": mpmath.e,
        "LOG2E": mpmath.log(mpmath.e, b=2),
        "LOG10E": mpmath.log10(mpmath.e),
        "LN2": mpmath.log(2),
        "LN10": mpmath.log(10),
        "PI": mpmath.pi,
        "PI_2": mpmath.pi / 2,
        "PI_4": mpmath.pi / 4,
        "M_1_PI": 1 / mpmath.pi,
        "M_2_PI": 2 / mpmath.pi,
        "M_2_SQRTPI": 2 / mpmath.sqrt(mpmath.pi),
        "SQRT2": mpmath.sqrt(2),
        "SQRT1_2": 1 / mpmath.sqrt(2),
        "INFINITY": mpmath.inf,
    }
    return mapping[self.source]


@add_method(Variable)
def eval(self, assignment):
    return mpmath.mpf(assignment[self.source])


@add_method(Number)
def eval(self, assignment):
    return mpmath.mpf(self.source)


@add_method(Operation)
def eval(self, assignment):
    f_args = [arg.eval(assignment) for arg in self.args]

    if len(f_args) == 1:
        mapping = {
            "-": (lambda x: -x),
            "fabs": (lambda x: mpmath.fabs(x)),
            "exp": (lambda x: mpmath.exp(x)),
            "exp2": (lambda x: mpmath.power(2, x)),
            "expm1": (lambda x: mpmath.expm1(x)),
            "log": (lambda x: mpmath.log(x)),
            "log10": (lambda x: mpmath.log10(x)),
            "log2": (lambda x: mpmath.log(x, b=2)),
            "log1p": (lambda x: mpmath.log1p(x)),
            "sqrt": (lambda x: mpmath.sqrt(x)),
            "cbrt": (lambda x: mpmath.cbrt(x)),
            "sin": (lambda x: mpmath.sin(x)),
            "cos": (lambda x: mpmath.cos(x)),
            "tan": (lambda x: mpmath.tan(x)),
            "asin": (lambda x: mpmath.asin(x)),
            "acos": (lambda x: mpmath.acos(x)),
            "atan": (lambda x: mpmath.atan(x)),
            "sinh": (lambda x: mpmath.sinh(x)),
            "cosh": (lambda x: mpmath.cosh(x)),
            "tanh": (lambda x: mpmath.tanh(x)),
            "asinh": (lambda x: mpmath.asinh(x)),
            "acosh": (lambda x: mpmath.acosh(x)),
            "atanh": (lambda x: mpmath.atanh(x)),
            "erf": (lambda x: mpmath.erf(x)),
            "erfc": (lambda x: mpmath.erfc(x)),
            "tgamma": (lambda x: mpmath.gamma(x)),
            "lgamma": (lambda x: mpmath.loggamma(x)),
            "ceil": (lambda x: mpmath.ceil(x)),
            "floor": (lambda x: mpmath.floor(x)),
        }
        return mapping[self.op](f_args[0])

    if len(f_args) == 2:
        mapping = {
            "+": (lambda a, b: a + b),
            "-": (lambda a, b: a - b),
            "*": (lambda a, b: a * b),
            "/": (lambda a, b: a / b),
            "pow": (lambda a, b: mpmath.power(a, b)),
            "hypot": (lambda a, b: mpmath.hypot(a, b)),
            "atan2": (lambda a, b: mpmath.atan2(a, b)),
            "fmod": (lambda a, b: mpmath.fmod(a, b)),
            "fmax": (lambda a, b: max(a, b)),
            "fmin": (lambda a, b: min(a, b)),
            "fdim": (lambda a, b: max(0, a - b)),
            "<": (lambda a, b: a < b),
            ">": (lambda a, b: a > b),
            "<=": (lambda a, b: a <= b),
            ">=": (lambda a, b: a >= b),
            "==": (lambda a, b: a == b),
            "!=": (lambda a, b: a != b),
        }
        return mapping[self.op](f_args[0], f_args[1])

    msg = "Operation not yet supported for eval: '{}'".format(repr(self))
    raise NotImplementedError(msg)


@add_method(FPCore)
def eval(self, *args):
    assert len(args) == len(self.arguments)
    assignment = {name: arg for name, arg
                  in zip(self.arguments, args)}
    return self.body.eval(assignment)
