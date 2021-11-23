

from fpcore.ast import ASTNode, Atom, Constant, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def to_wolfram(self):
    # Make sure calling to_wolfram leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_wolfram not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def to_wolfram(self):
    return self.source

@add_method(Constant)
def to_wolfram(self):
    mapping = {
        "PI" : "Pi",
        "INFINITY" : "Infinity"
    }
    return mapping[self.source]

@add_method(Operation)
def to_wolfram(self):
    w_args = list()
    for a in self.args:
        w_args.append(a.to_wolfram())

    if len(w_args) == 1 and self.op in {"+", "-"}:
        return "({}{})".format(self.op, w_args[0])

    if len(w_args) == 2 and self.op in {"+", "-", "*", "/"}:
        return "({}{}{})".format(w_args[0], self.op, w_args[1])

    mapping = {
        "sin"  : "Sin",
        "cos"  : "Cos",
        "tan"  : "Tan",
        "asin" : "ArcSin",
        "acos" : "ArcCos",
        "atan" : "ArcTan",
    }
    op = mapping.get(self.op, self.op)
    return "{}[{}]".format(op, ", ".join(w_args))

@add_method(FPCore)
def to_wolfram(self):
    return self.body.to_wolfram()
