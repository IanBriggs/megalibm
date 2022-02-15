

from fpcore.ast import ASTNode, Atom, Constant, Operation, FPCore, Variable, Number
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def extract_t(self):
    # Make sure calling extract_t leads to an error if not overridden
    class_name = type(self).__name__
    msg = "extract_t not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Variable)
def extract_t(self):
    return Variable(self.source)

@add_method(Number)
def extract_t(self):
    return Number(self.source)

@add_method(Constant)
def extract_t(self):
    return Constant(self.source)

@add_method(Operation)
def extract_t(self):
    if self.op == "thefunc":
        return Variable("x")
    new_args = [arg.extract_t() for arg in self.args]
    return Operation(self.op, *new_args)

@add_method(FPCore)
def extract_t(self):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.extract_t())
