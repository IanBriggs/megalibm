

from fpcore.ast import ASTNode, Atom, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def __neg__(self):
    # Make sure calling __neg__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = "__neg__ not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Atom)
def __neg__(self):
    return Operation("-", self)

@add_method(Operation)
def __neg__(self):
    return Operation("-", self)

@add_method(FPCore)
def __neg__(self):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  Operation("-", self.body))
