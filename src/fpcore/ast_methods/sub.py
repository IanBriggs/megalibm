

from fpcore.ast import ASTNode, Atom, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def __sub__(self, other):
    # Make sure calling __sub__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = "__sub__ not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def __sub__(self, other):
    return Operation("-", self, other)

@add_method(Operation)
def __sub__(self, other):
    return Operation("-", self, other)

@add_method(FPCore)
def __sub__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  Operation("-", self.body, other.body))
