from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method


@add_method(ASTNode)
def __neg__(self, *args, **kwargs):
    # Make sure calling __neg__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__neg__ not implemented for class '{class_name}'"
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
