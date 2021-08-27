

from fpcore.ast import ASTNode, Atom, Constant, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def to_sollya(self):
    # Make sure calling to_sollya leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_sollya not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def to_sollya(self):
    return self.source

@add_method(Constant)
def to_sollya(self):
    mapping = {
        "PI" : "pi"
    }
    return mapping[self.source]

@add_method(Operation)
def to_sollya(self):
    s_args = [arg.to_sollya() for arg in self.args]

    if len(s_args) == 1 and self.op in {"+", "-"}:
        return "({}{})".format(self.op, s_args[0])

    if len(s_args) == 2 and self.op in {"+", "-", "*", "/"}:
        return "({}{}{})".format(s_args[0], self.op, s_args[1])

    return "{}({})".format(self.op, ", ".join(s_args)) 

@add_method(FPCore)
def to_sollya(self):
    return self.body.to_sollya()
