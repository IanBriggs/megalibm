import fractions

from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
from snake_egg import Var
from snake_egg_rules import operations
from utils import add_method

_CONST_MAPPING = {
    "E": operations.CONST_E,
    "INFINITY": operations.CONST_INFINITY,
    "PI": operations.CONST_PI,
    "PI_2": lambda : operations.add(operations.CONST_PI(), operations.CONST_PI()),
}

_UNOP_MAPPING = {
    "-": operations.neg,
    "+": operations.uadd,
    "acos": operations.acos,
    "acosh": operations.acosh,
    "asin": operations.asin,
    "asinh": operations.asinh,
    "atan": operations.atan,
    "atanh": operations.atanh,
    "cbrt": operations.cbrt,
    "ceil": operations.ceil,
    "cos": operations.cos,
    "cosh": operations.cosh,
    "erf": operations.erf,
    "erfc": operations.erfc,
    "exp": operations.exp,
    "exp2": operations.exp2,
    "expm1": operations.expm1,
    "fabs": operations.fabs,
    "fdim": operations.fdim,
    "floor": operations.floor,
    "isnormal": operations.isnormal,
    "lgamma": operations.lgamma,
    "log": operations.log,
    "log10": operations.log10,
    "log1p": operations.log1p,
    "log2": operations.log2,
    "nearbyint": operations.nearbyint,
    "round": operations.round,
    "signbit": operations.signbit,
    "sin": operations.sin,
    "sinh": operations.sinh,
    "sqrt": operations.sqrt,
    "tan": operations.tan,
    "tanh": operations.tanh,
    "tgamma": operations.tgamma,
    "thefunc": operations.thefunc,
    "uadd": operations.uadd,
}

_BINOP_MAPPING = {
    "-": operations.sub,
    "*": operations.mul,
    "/": operations.div,
    "+": operations.add,
    "atan2": operations.atan2,
    "fmax": operations.fmax,
    "fmin": operations.fmin,
    "fmod": operations.fmod,
    "hypot": operations.hypot,
    "pow": operations.pow,
    "remainder": operations.remainder,
}

_TRIOP_MAPPING = {
    "fma": operations.fma,
}


@add_method(ASTNode)
def to_snake_egg(self, *args, **kwargs):
    # Make sure calling to_snake_egg leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"to_snake_egg not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Variable)
def to_snake_egg(self, to_rule):
    if to_rule:
        return Var(self.source)
    return self.source


@add_method(Number)
def to_snake_egg(self, to_rule):
    try:
        return int(self.source)
    except ValueError:
        pass

    return fractions.Fraction(self.source)


@add_method(Constant)
def to_snake_egg(self, to_rule):
    try:
        return _CONST_MAPPING[self.source]()
    except KeyError:
        raise NotImplementedError(f"Unknown constant '{self.source}'")


@add_method(Operation)
def to_snake_egg(self, to_rule):
    se_args = [a.to_snake_egg(to_rule) for a in self.args]

    if len(se_args) == 1 and self.op in _UNOP_MAPPING:
        return _UNOP_MAPPING[self.op](se_args[0])

    if len(se_args) == 2 and self.op in _BINOP_MAPPING:
        return _BINOP_MAPPING[self.op](se_args[0], se_args[1])

    if len(se_args) == 3 and self.op in _TRIOP_MAPPING:
        return _TRIOP_MAPPING[self.op](se_args[0], se_args[1], se_args[2])

    msg = f"Operation not yet supported for to_snake_egg: '{self.op}'"
    raise NotImplementedError(msg)


@add_method(FPCore)
def to_snake_egg(self, to_rule=False):
    return self.body.to_snake_egg(to_rule)
