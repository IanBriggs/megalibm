from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, Constant, FPCore, Operation
from utils import add_method

_CONST_MAPPING = {
    "PI": "Pi",
    "INFINITY": "Infinity"
}

_UNOP_MAPPING = {
    "acos": "ArcCos",
    "asin": "ArcSin",
    "atan": "ArcTan",
    "cos": "Cos",
    "sin": "Sin",
    "tan": "Tan",
}


@add_method(ASTNode)
def to_wolfram(self, *args, **kwargs):
    expect_implemented("to_wolfram", self)


@add_method(Atom)
def to_wolfram(self):
    return self.source


@add_method(Constant)
def to_wolfram(self):
    try:
        return _CONST_MAPPING[self.source]
    except KeyError:
        raise NotImplementedError(f"Unknown constant '{self.source}'")


@add_method(Operation)
def to_wolfram(self):
    w_args = [arg.to_wolfram() for arg in self.args]

    if len(w_args) == 1 and self.op in {"+", "-"}:
        return "({}{})".format(self.op, w_args[0])

    if len(w_args) == 2 and self.op in {"+", "-", "*", "/"}:
        return "({}{}{})".format(w_args[0], self.op, w_args[1])

    if len(w_args) == 1 and self.op in _UNOP_MAPPING:
        op = _UNOP_MAPPING[self.op]
        return f"{op}[{w_args[0]}]"

    msg = f"Operation not yet supported for to_wolfram: '{self.op}'"
    raise NotImplementedError(msg)


@add_method(FPCore)
def to_wolfram(self):
    return self.body.to_wolfram()
