from fpcore.ast import ASTNode, Atom, FPCore, Operation
from utils import add_method


@add_method(ASTNode)
def __div__(self, *args, **kwargs):
    # Make sure calling __div__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__div__ not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def __div__(self, other):
    return Operation("/", self, other)


@add_method(Operation)
def __div__(self, other):
    return Operation("/", self, other)


@add_method(FPCore)
def __div__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  Operation("/", self.body, other.body))
