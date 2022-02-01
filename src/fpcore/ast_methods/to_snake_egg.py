

from fpcore.ast import ASTNode, Number, Constant, Operation, FPCore, Variable
from utils import add_method, Logger

import snake_egg_rules

import snake_egg

import fractions


logger = Logger(level=Logger.EXTRA)


operations = snake_egg_rules.operations

const_mapping = {
  "PI":  operations.CONST_PI,
  "E":   operations.CONST_E
}

unop_mapping = {
  "thefunc":    operations.thefunc,
  "+":          operations.uadd,
  "-":          operations.neg,
  "acos":       operations.acos,
  "acosh":      operations.acosh,
  "asin":       operations.asin,
  "asinh":      operations.asinh,
  "atan":       operations.atan,
  "atanh":      operations.atanh,
  "cbrt":       operations.cbrt,
  "cos":        operations.cos,
  "cosh":       operations.cosh,
  "erf":        operations.erf,
  "erfc":       operations.erfc,
  "exp":        operations.exp,
  "expm1":      operations.expm1,
  "fabs":       operations.fabs,
  "log":        operations.log,
  "log1p":      operations.log1p,
  "sin":        operations.sin,
  "sinh":       operations.sinh,
  "sqrt":       operations.sqrt,
  "tan":        operations.tan,
  "tanh":       operations.tanh,
  "uadd":       operations.uadd,
  "ceil":       operations.ceil,
  "exp2":       operations.exp2,
  "fdim":       operations.fdim,
  "floor":      operations.floor,
  "isnormal":   operations.isnormal,
  "lgamma":     operations.lgamma,
  "log10":      operations.log10,
  "log2":       operations.log2,
  "nearbyint":  operations.nearbyint,
  "round":      operations.round,
  "signbit":    operations.signbit,
  "tgamma":     operations.tgamma,
}

binop_mapping = {
  "+":          operations.add,
  "-":          operations.sub,
  "*":          operations.mul,
  "/":          operations.div,
  "atan2":      operations.atan2,
  "pow":        operations.pow,
  "hypot":      operations.hypot,
  "remainder":  operations.remainder,
  "fmax":       operations.fmax,
  "fmin":       operations.fmin,
  "fmod":       operations.fmod,
}

triop_mapping = {
  "fma":  operations.fma,
}


@add_method(ASTNode)
def to_snake_egg(self, to_rule):
    # Make sure calling to_snake_egg leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_snake_egg not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Variable)
def to_snake_egg(self, to_rule):
    if to_rule:
        return snake_egg.Var(self.source)
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
    return const_mapping[self.source]()


@add_method(Operation)
def to_snake_egg(self, to_rule):
    se_args = [a.to_snake_egg(to_rule) for a in self.args]

    if len(se_args) == 1 and self.op in unop_mapping:
        return unop_mapping[self.op](se_args[0])

    if len(se_args) == 2 and self.op in binop_mapping:
        return binop_mapping[self.op](se_args[0], se_args[1])

    if len(se_args) == 3 and self.op in triop_mapping:
        return triop_mapping[self.op](se_args[0], se_args[1], se_args[2])

    logger.error("Unsupported operation: {}", self.op)


@add_method(FPCore)
def to_snake_egg(self, to_rule=False):
    return self.body.to_snake_egg(to_rule)
