from mpmath import iv
from expect import expect_implemented
from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
import interval
from utils import add_method

iv.prec = 2**14

_CONST_MAPPING = {
    "E": iv.e,
    "INFINITY": iv.inf,
    "LN10": iv.log(10),
    "LN2": iv.log(2),
    "LOG10E": iv.log10(iv.e),
    "LOG2E": iv.log(iv.e, b=2),
    "M_1_PI": 1 / iv.pi,
    "M_2_PI": 2 / iv.pi,
    "M_2_SQRTPI": 2 / iv.sqrt(iv.pi),
    "PI_2": iv.pi / 2,
    "PI_4": iv.pi / 4,
    "PI": iv.pi,
    "SQRT1_2": 1 / iv.sqrt(2),
    "SQRT2": iv.sqrt(2),
}

_UNOP_MAPPING = {
    "-": lambda x: -x,
    "acos": lambda x: iv.acos(x),
    "acosh": lambda x: iv.acosh(x),
    "asin": lambda x: iv.asin(x),
    "asinh": lambda x: iv.asinh(x),
    "atan": lambda x: iv.atan(x),
    "atanh": lambda x: iv.atanh(x),
    "cbrt": lambda x: iv.cbrt(x),
    "ceil": lambda x: iv.ceil(x),
    "cos": lambda x: iv.cos(x),
    "cosh": lambda x: iv.cosh(x),
    "erf": lambda x: iv.erf(x),
    "erfc": lambda x: iv.erfc(x),
    "exp": lambda x: iv.exp(x),
    "exp2": lambda x: iv.power(2, x),
    "expm1": lambda x: iv.expm1(x),
    "fabs": lambda x: iv.fabs(x),
    "floor": lambda x: iv.floor(x),
    "lgamma": lambda x: iv.loggamma(x),
    "log": lambda x: iv.log(x),
    "log10": lambda x: iv.log10(x),
    "log1p": lambda x: iv.log1p(x),
    "log2": lambda x: iv.log(x, b=2),
    "sin": lambda x: iv.sin(x),
    "sinh": lambda x: iv.sinh(x),
    "sqrt": lambda x: iv.sqrt(x),
    "tan": lambda x: iv.tan(x),
    "tanh": lambda x: iv.tanh(x),
    "tgamma": lambda x: iv.gamma(x),
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
    "atan2": lambda a, b: iv.atan2(a, b),
    "fdim": lambda a, b: max(0, a - b),
    "fmax": lambda a, b: max(a, b),
    "fmin": lambda a, b: min(a, b),
    "fmod": lambda a, b: iv.fmod(a, b),
    "hypot": lambda a, b: iv.hypot(a, b),
    "pow": lambda a, b: iv.power(a, b),
}


@add_method(ASTNode)
def interval_eval(self, *args, **kwargs):
    expect_implemented("interval_eval", self)


@add_method(Constant)
def interval_eval(self, assignment):
    try:
        return _CONST_MAPPING[self.source]
    except KeyError:
        raise NotImplementedError(f"Unknown constant '{self.source}'")


@add_method(Variable)
def interval_eval(self, assignment):
    if assignment is not None and self.source not in assignment:
        raise NameError("{} not in evaluation environment".format(self.source))
    val = assignment[self.source]
    if type(val) == interval.Interval:
        inf = val[0]
        sup = val[1]
        if hasattr(inf, "eval"):
            inf = inf.eval()
        if hasattr(sup, "eval"):
            sup = sup.eval()
        return iv.mpf([inf, sup])
    return iv.mpf(val)


@add_method(Number)
def interval_eval(self, assignment):
    return iv.mpf(self.source)


@add_method(Operation)
def interval_eval(self, assignment):
    f_args = [arg.interval_eval(assignment) for arg in self.args]

    if len(f_args) == 1 and self.op in _UNOP_MAPPING:
        return _UNOP_MAPPING[self.op](f_args[0])

    if len(f_args) == 2 and self.op in _BINOP_MAPPING:
        return _BINOP_MAPPING[self.op](f_args[0], f_args[1])

    # TODO: What if we want the function to be interval_evaluated?
    if self.op == "thefunc":
        return iv.mpf("NaN")

    msg = ("Operation not yet supported for interval_eval with"
           f" {len(f_args)} arguments: '{self.op}'")
    raise NotImplementedError(msg)


@add_method(FPCore)
def interval_eval(self, *args):
    # Check that arity matches
    expected = len(self.arguments)
    actual = len(args)
    if expected != actual:
        msg = f"FPCore expected {expected} arguments, got {actual}"
        raise TypeError(msg)

    # Assign variables to values and interval_eval
    assignment = {name.source: arg for name, arg in zip(self.arguments, args)}
    return self.body.interval_eval(assignment)
