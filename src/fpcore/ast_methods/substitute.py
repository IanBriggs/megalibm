from fpcore.ast import ASTNode, Atom, FPCore, Operation
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


@add_method(ASTNode)
def substitute(self, *args, **kwargs):
    # Make sure calling substitute leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"substitute not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def substitute(self, old, new):
    if self == old:
        return new
    return self


@add_method(Operation)
def substitute_floatop(self):
    new_args = [arg.substitute_floatop() if isinstance(arg, Operation) else arg for arg in self.args]
    if self.op in _UNOP_SET:
        return Operation(self.op + 'f', *new_args)
    return Operation(self.op, *new_args)


@add_method(Operation)
def substitute(self, old, new):
    if self == old:
        return new
    new_args = [arg.substitute(old, new) for arg in self.args]
    return Operation(self.op, *new_args)


@add_method(FPCore)
def substitute(self, old, new):
    if self == old:
        return new
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.substitute(old, new))


