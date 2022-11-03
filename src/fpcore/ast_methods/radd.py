from fpcore.ast import ASTNode, Atom, FPCore, Number, Operation
from fpcore.ast_methods.add import typecase_and_add
from utils import add_method


@add_method(ASTNode)
def __radd__(self, *args, **kwargs):
    # Make sure calling __radd__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__radd__ not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def __radd__(self, other):
    return typecase_and_add(other, self)


@add_method(Operation)
def __radd__(self, other):
    return typecase_and_add(other, self)


@add_method(FPCore)
def __radd__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  typecase_and_add(other, self))
