import mpmath
from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
from utils import add_method

mpmath.prec = 2**14

_CONST_MAPPING = {
    "E": mpmath.e,
    "INFINITY": mpmath.inf,
    "LN10": mpmath.log(10),
    "LN2": mpmath.log(2),
    "LOG10E": mpmath.log10(mpmath.e),
    "LOG2E": mpmath.log(mpmath.e, b=2),
    "M_1_PI": 1 / mpmath.pi,
    "M_2_PI": 2 / mpmath.pi,
    "M_2_SQRTPI": 2 / mpmath.sqrt(mpmath.pi),
    "PI_2": mpmath.pi / 2,
    "PI_4": mpmath.pi / 4,
    "PI": mpmath.pi,
    "SQRT1_2": 1 / mpmath.sqrt(2),
    "SQRT2": mpmath.sqrt(2),
}

_UNOP_MAPPING = {
    "-": lambda x: -x,
    "acos": lambda x: mpmath.acos(x),
    "acosh": lambda x: mpmath.acosh(x),
    "asin": lambda x: mpmath.asin(x),
    "asinh": lambda x: mpmath.asinh(x),
    "atan": lambda x: mpmath.atan(x),
    "atanh": lambda x: mpmath.atanh(x),
    "cbrt": lambda x: mpmath.cbrt(x),
    "ceil": lambda x: mpmath.ceil(x),
    "cos": lambda x: mpmath.cos(x),
    "cosh": lambda x: mpmath.cosh(x),
    "erf": lambda x: mpmath.erf(x),
    "erfc": lambda x: mpmath.erfc(x),
    "exp": lambda x: mpmath.exp(x),
    "exp2": lambda x: mpmath.power(2, x),
    "expm1": lambda x: mpmath.expm1(x),
    "fabs": lambda x: mpmath.fabs(x),
    "floor": lambda x: mpmath.floor(x),
    "lgamma": lambda x: mpmath.loggamma(x),
    "log": lambda x: mpmath.log(x),
    "log10": lambda x: mpmath.log10(x),
    "log1p": lambda x: mpmath.log1p(x),
    "log2": lambda x: mpmath.log(x, b=2),
    "sin": lambda x: mpmath.sin(x),
    "sinh": lambda x: mpmath.sinh(x),
    "sqrt": lambda x: mpmath.sqrt(x),
    "tan": lambda x: mpmath.tan(x),
    "tanh": lambda x: mpmath.tanh(x),
    "tgamma": lambda x: mpmath.gamma(x),
}

_BINOP_MAPPING = {
    "-": lambda a, b: a - b,
    "!=": lambda a, b: a != b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "+": lambda a, b: a + b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "atan2": lambda a, b: mpmath.atan2(a, b),
    "fdim": lambda a, b: max(0, a - b),
    "fmax": lambda a, b: max(a, b),
    "fmin": lambda a, b: min(a, b),
    "fmod": lambda a, b: mpmath.fmod(a, b),
    "hypot": lambda a, b: mpmath.hypot(a, b),
    "pow": lambda a, b: mpmath.power(a, b),
}


@add_method(ASTNode)
def eval(self, *args, **kwargs):
    # Make sure calling eval leads to an error if not overridden
    class_name = type(self).__name__
    msg = "eval not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Constant)
def eval(self, assignment):
    try:
        return _CONST_MAPPING[self.source]
    except KeyError:
        raise NotImplementedError(f"Unknown constant '{self.source}'")


@add_method(Variable)
def eval(self, assignment):
    if self.source not in assignment:
        raise NameError("{} not in evaluation environment".format(self.source))
    return mpmath.mpf(assignment[self.source])


@add_method(Number)
def eval(self, assignment):
    return mpmath.mpf(self.source)


@add_method(Operation)
def eval(self, assignment):
    f_args = [arg.eval(assignment) for arg in self.args]

    if len(f_args) == 1 and self.op in _UNOP_MAPPING:
        return _UNOP_MAPPING[self.op](f_args[0])

    if len(f_args) == 2 and self.op in _BINOP_MAPPING:
        return _BINOP_MAPPING[self.op](f_args[0], f_args[1])

    msg = f"Operation not yet supported for eval: '{self.op}'"
    raise NotImplementedError(msg)


@add_method(FPCore)
def eval(self, *args):
    # Check that arity matches
    expected = len(self.arguments)
    actual = len(args)
    if expected != actual:
        msg = f"FPCore expected {expected} arguments, got {actual}"
        raise TypeError(msg)

    # Assign variables to values and eval
    assignment = {name.source: arg for name, arg in zip(self.arguments, args)}
    return self.body.eval(assignment)
