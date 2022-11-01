from fpcore.ast import ASTNode, Atom, FPCore, Number, Operation
from utils import add_method


@add_method(ASTNode)
def __sub__(self, *args, **kwargs):
    # Make sure calling __sub__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__sub__ not implemented for class '{class_name}'".format(
        class_name)
    raise NotImplementedError(msg)


def typecase_and_sub(a, b):
    # Extract body expressions of FPCores
    if type(a) == FPCore:
        a = a.body
    if type(b) == FPCore:
        b = b.body

    # Force number types into AST nodes
    if type(a) in {int, float}:
        a = Number(str(a))
    if type(b) in {int, float}:
        b = Number(str(b))

    # Error if no AST Nodes
    if not issubclass(type(a), ASTNode):
        msg = "FPCore does not support subtraction by '{}'"
        raise TypeError(msg.format(type(a)))
    if not issubclass(type(b), ASTNode):
        msg = "FPCore does not support subtraction by '{}'"
        raise TypeError(msg.format(type(b)))

    # Make the new node
    return Operation("-", a, b)


@add_method(Atom)
def __sub__(self, other):
    return typecase_and_sub(self, other)


@add_method(Operation)
def __sub__(self, other):
    return typecase_and_sub(self, other)


@add_method(FPCore)
def __sub__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  typecase_and_sub(self, other))
