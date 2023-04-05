from fpcore.ast import Operation
from utils import add_method

_UNOP_SET = {
    "acos",
    "acosh",
    "asin",
    "asinh",
    "atan",
    "atanh",
    "cbrt",
    "cos",
    "cosh",
    "erf",
    "erfc",
    "exp",
    "exp",
    "expm1",
    "fabs",
    "inv",
    "tgamma",
    "lgamma",
    "log1p",
    "log10",
    "log",
    "log2",
    "sin",
    "sinh",
    "sqrt",
    "tan",
    "tanh"
}


@add_method(Operation)
def substitute_op(self):
    new_args = [arg.substitute_op() if isinstance(arg, Operation) else arg for arg in self.args]
    if self.op in _UNOP_SET:
        return Operation(self.op + 'f', *new_args)
    return Operation(self.op, *new_args)