

from fpcore.ast import ASTNode, Atom, Constant, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def to_libm_c(self):
    # Make sure calling to_libm_c leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_libm_c not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def to_libm_c(self):
    return self.source

@add_method(Constant)
def to_libm_c(self):
    mapping = {
        "PI" : "M_PI"
    }
    return mapping[self.source]

@add_method(Operation)
def to_libm_c(self):
    c_args = [arg.to_libm_c() for arg in self.args]

    if len(c_args) == 1 and self.op in {"+", "-"}:
        return "({}{})".format(self.op, c_args[0])

    if len(c_args) == 2 and self.op in {"+", "-", "*", "/"}:
        return "({}{}{})".format(c_args[0], self.op, c_args[1])

    return "{}({})".format(self.op, ", ".join(c_args)) 

@add_method(FPCore)
def to_libm_c(self):
    return self.body.to_libm_c()
